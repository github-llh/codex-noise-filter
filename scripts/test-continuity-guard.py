#!/usr/bin/env python3
"""使用标准库对连续性 Hook 的关键事件进行回归测试。"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
HOOK_SCRIPT = ROOT_DIRECTORY / "distribution/plugin/hooks/continuity_guard.py"
HOOK_TIMEOUT_SECONDS = 5
SUCCESS_EXIT_CODE = 0


class ContinuityGuardTest(unittest.TestCase):
    """验证压缩、恢复、模型切换和网络失败的自动触发。"""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.plugin_data = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_hook(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        """在隔离的插件数据目录运行一次 Hook。"""

        environment = os.environ.copy()
        environment["PLUGIN_DATA"] = str(self.plugin_data)
        result = subprocess.run(
            ["python3", str(HOOK_SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=environment,
            timeout=HOOK_TIMEOUT_SECONDS,
            check=False,
        )
        self.assertEqual(SUCCESS_EXIT_CODE, result.returncode, result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else None

    @staticmethod
    def payload(event_name: str, model: str = "model-a", **extra: Any) -> dict[str, Any]:
        """创建不包含用户真实内容的测试事件。"""

        return {
            "session_id": "test-session",
            "cwd": "/workspace/project",
            "hook_event_name": event_name,
            "model": model,
            **extra,
        }

    def assert_context_contains(self, output: dict[str, Any] | None, text: str) -> None:
        """断言 Hook 输出包含模型可见的恢复上下文。"""

        self.assertIsNotNone(output)
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn(text, context)

    def test_compaction_is_recovered_without_user_prompt(self) -> None:
        """压缩后由 SessionStart 自动注入恢复要求。"""

        self.assertIsNone(self.run_hook(self.payload("PreCompact", trigger="auto")))
        self.assertIsNone(self.run_hook(self.payload("PostCompact", trigger="auto")))
        output = self.run_hook(self.payload("SessionStart", source="compact"))
        self.assert_context_contains(output, "上下文已完成压缩")

    def test_resume_is_recovered_without_pending_state(self) -> None:
        """重新连接或恢复会话时即使没有旧状态也自动复核。"""

        output = self.run_hook(self.payload("SessionStart", source="resume"))
        self.assert_context_contains(output, "会话恢复或重新连接")

    def test_model_switch_is_detected_on_next_prompt(self) -> None:
        """模型变化在下一次用户提交时自动触发。"""

        self.assertIsNone(self.run_hook(self.payload("UserPromptSubmit", prompt="first")))
        output = self.run_hook(
            self.payload("UserPromptSubmit", model="model-b", prompt="continue")
        )
        self.assert_context_contains(output, "活动模型已切换")

    def test_failed_network_tool_adds_recovery_context(self) -> None:
        """失败工具包含网络错误特征时立即注入幂等性复核。"""

        output = self.run_hook(
            self.payload(
                "PostToolUse",
                tool_name="Bash",
                tool_response={"exit_code": 1, "output": "connection timed out"},
            )
        )
        self.assert_context_contains(output, "工具出现网络或传输失败")

    def test_successful_tool_does_not_trigger_on_log_text(self) -> None:
        """成功输出仅提到旧网络错误时不误触发。"""

        output = self.run_hook(
            self.payload(
                "PostToolUse",
                tool_name="Bash",
                tool_response={
                    "exit_code": 0,
                    "output": "fixed connection timed out case",
                },
            )
        )
        self.assertIsNone(output)

    def test_private_state_excludes_user_and_workspace_content(self) -> None:
        """插件状态不得复制会话标识、工作区路径或用户 prompt。"""

        sensitive_prompt = "private-user-prompt"
        payload = self.payload("UserPromptSubmit", prompt=sensitive_prompt)
        self.run_hook(payload)
        state_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.plugin_data.rglob("*.json")
        )
        self.assertNotIn(payload["session_id"], state_text)
        self.assertNotIn(payload["cwd"], state_text)
        self.assertNotIn(sensitive_prompt, state_text)


if __name__ == "__main__":
    unittest.main()
