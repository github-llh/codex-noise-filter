#!/usr/bin/env python3
"""在压缩、恢复、模型切换和网络失败后自动注入连续性复核要求。"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


STATE_SCHEMA_VERSION = 1
MAX_PENDING_REASONS = 8
MAX_RESPONSE_SCAN_CHARS = 32_768
MAX_STATE_FILES = 64
SUCCESS_EXIT_CODE = 0

PLUGIN_DATA_ENV = "PLUGIN_DATA"
STATE_DIRECTORY_NAME = "continuity"
STATE_FILE_SUFFIX = ".json"
TEMP_FILE_SUFFIX = ".tmp"

EVENT_SESSION_START = "SessionStart"
EVENT_PRE_COMPACT = "PreCompact"
EVENT_POST_COMPACT = "PostCompact"
EVENT_USER_PROMPT_SUBMIT = "UserPromptSubmit"
EVENT_POST_TOOL_USE = "PostToolUse"

SOURCE_RESUME = "resume"
SOURCE_COMPACT = "compact"
REASON_SESSION_RESUMED = "session_resumed"
REASON_COMPACTION_PENDING = "compaction_pending"
REASON_COMPACTION_COMPLETED = "compaction_completed"
REASON_MODEL_CHANGED = "model_changed"
REASON_WORKSPACE_CHANGED = "workspace_changed"
REASON_NETWORK_FAILURE = "network_failure"

FAILURE_BOOLEAN_FIELDS = ("isError", "failed")
FAILURE_VALUE_FIELDS = ("error", "exception")
FAILURE_STATUS_FIELDS = ("status", "state")
FAILURE_STATUSES = {"error", "failed", "failure"}
EXIT_CODE_FIELDS = ("exit_code", "exitCode", "returncode", "returnCode")

NETWORK_FAILURE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bnetwork (?:error|failure|unreachable)\b",
        r"\bconnection (?:reset|refused|timed out|closed|aborted)\b",
        r"\btemporary failure in name resolution\b",
        r"\bname or service not known\b",
        r"\b(?:econnreset|econnrefused|etimedout)\b",
        r"\bsocket hang up\b",
        r"\bbroken pipe\b",
        r"\bremote disconnected\b",
        r"\btransport error\b",
        r"\bcommunications link failure\b",
        r"\btls handshake (?:failed|error|timeout)\b",
        r"\bunexpected eof\b",
    )
)

REASON_LABELS = {
    REASON_SESSION_RESUMED: "会话恢复或重新连接",
    REASON_COMPACTION_PENDING: "上下文即将压缩",
    REASON_COMPACTION_COMPLETED: "上下文已完成压缩",
    REASON_MODEL_CHANGED: "活动模型已切换",
    REASON_WORKSPACE_CHANGED: "当前工作目录已变化",
    REASON_NETWORK_FAILURE: "工具出现网络或传输失败",
}

RECOVERY_STEPS = (
    "先重读最新用户目标和高优先级指令，不要求用户重复已提供的信息。",
    "再核对当前 git status、git diff、目标文件落盘状态和仍在运行的工具；外部写操作还要检查幂等性证据。",
    "在内部重建目标、已确认事实、已改文件、验证状态、doNotRetry 和唯一下一步；缺失事实必须重新验证，不得猜测。",
    "若旧摘要、旧模型结论或工具回执与当前证据冲突，以当前工作区和最新指令为准。",
)


def read_hook_input() -> dict[str, Any]:
    """读取并校验 Codex Hook 的标准输入。"""

    payload = json.load(sys.stdin)
    if not isinstance(payload, dict):
        raise ValueError("Hook 输入必须是 JSON 对象")
    return payload


def fingerprint(value: str) -> str:
    """生成不可逆指纹，避免把会话标识和本机路径写入状态文件。"""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_state_path(payload: dict[str, Any]) -> Path | None:
    """返回当前会话的插件私有状态文件；缺少宿主目录时安全降级。"""

    plugin_data = os.environ.get(PLUGIN_DATA_ENV)
    session_id = payload.get("session_id")
    if not plugin_data or not isinstance(session_id, str) or not session_id:
        return None
    state_directory = Path(plugin_data) / STATE_DIRECTORY_NAME
    try:
        state_directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    return state_directory / f"{fingerprint(session_id)}{STATE_FILE_SUFFIX}"


def empty_state() -> dict[str, Any]:
    """创建不包含用户内容和工具原始输出的最小状态。"""

    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "model": "",
        "cwd_fingerprint": "",
        "last_event": "",
        "pending_reasons": [],
    }


def load_state(path: Path | None) -> dict[str, Any]:
    """读取状态；损坏或旧版本状态按空状态处理。"""

    if path is None or not path.exists():
        return empty_state()
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return empty_state()
    if not isinstance(state, dict) or state.get("schema_version") != STATE_SCHEMA_VERSION:
        return empty_state()
    pending_reasons = state.get("pending_reasons")
    if not isinstance(pending_reasons, list):
        state["pending_reasons"] = []
    return state


def prune_state_files(directory: Path) -> None:
    """限制插件私有状态文件数量，避免长期运行后无界增长。"""

    state_files = sorted(
        directory.glob(f"*{STATE_FILE_SUFFIX}"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for stale_path in state_files[MAX_STATE_FILES:]:
        try:
            stale_path.unlink()
        except OSError:
            continue


def save_state(path: Path | None, state: dict[str, Any]) -> None:
    """原子写入插件私有状态，并清理最旧文件。"""

    if path is None:
        return
    temporary_path = path.with_name(f"{path.name}.{os.getpid()}{TEMP_FILE_SUFFIX}")
    try:
        temporary_path.write_text(
            json.dumps(state, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        temporary_path.replace(path)
        prune_state_files(path.parent)
    except OSError:
        return
    finally:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass


def add_reason(state: dict[str, Any], reason: str) -> None:
    """以稳定顺序追加去重后的待恢复原因。"""

    pending_reasons = [
        value for value in state.get("pending_reasons", []) if isinstance(value, str)
    ]
    if reason not in pending_reasons:
        pending_reasons.append(reason)
    state["pending_reasons"] = pending_reasons[-MAX_PENDING_REASONS:]


def serialize_response(response: Any) -> str:
    """仅在内存中截取工具响应文本，用于识别传输错误。"""

    try:
        text = json.dumps(response, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        text = str(response)
    return text[:MAX_RESPONSE_SCAN_CHARS]


def response_has_failure_signal(value: Any) -> bool:
    """递归识别常见失败字段，避免只因日志提到网络错误就误触发。"""

    if isinstance(value, dict):
        for field in EXIT_CODE_FIELDS:
            exit_code = value.get(field)
            if isinstance(exit_code, int) and exit_code != SUCCESS_EXIT_CODE:
                return True
        for field in FAILURE_BOOLEAN_FIELDS:
            if value.get(field) is True:
                return True
        for field in FAILURE_VALUE_FIELDS:
            if value.get(field):
                return True
        for field in FAILURE_STATUS_FIELDS:
            status = value.get(field)
            if isinstance(status, str) and status.lower() in FAILURE_STATUSES:
                return True
        return any(response_has_failure_signal(child) for child in value.values())
    if isinstance(value, list):
        return any(response_has_failure_signal(child) for child in value)
    return False


def is_network_failure(response: Any) -> bool:
    """仅在工具响应同时具有失败信号和网络错误特征时返回真。"""

    if not response_has_failure_signal(response):
        return False
    response_text = serialize_response(response)
    return any(pattern.search(response_text) for pattern in NETWORK_FAILURE_PATTERNS)


def recovery_context(reasons: list[str]) -> str:
    """构造供模型执行的连续性复核要求。"""

    labels = [REASON_LABELS.get(reason, reason) for reason in reasons]
    reason_text = "、".join(labels) if labels else "连续性状态发生变化"
    steps = "\n".join(f"{index}. {step}" for index, step in enumerate(RECOVERY_STEPS, 1))
    return f"连续性守卫已自动触发，原因：{reason_text}。继续任务前执行以下复核：\n{steps}"


def context_output(event_name: str, context: str) -> dict[str, Any]:
    """按官方 Hook 协议返回模型可见的额外开发者上下文。"""

    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": context,
        }
    }


def handle_event(payload: dict[str, Any]) -> dict[str, Any] | None:
    """处理支持的连续性事件，并返回可选的 Hook 输出。"""

    event_name = str(payload.get("hook_event_name", ""))
    state_path = get_state_path(payload)
    state = load_state(state_path)
    previous_model = state.get("model")
    previous_cwd_fingerprint = state.get("cwd_fingerprint")
    current_model = payload.get("model") if isinstance(payload.get("model"), str) else ""
    current_cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else ""
    current_cwd_fingerprint = fingerprint(current_cwd) if current_cwd else ""

    if previous_model and current_model and previous_model != current_model:
        add_reason(state, REASON_MODEL_CHANGED)
    if (
        previous_cwd_fingerprint
        and current_cwd_fingerprint
        and previous_cwd_fingerprint != current_cwd_fingerprint
    ):
        add_reason(state, REASON_WORKSPACE_CHANGED)

    output: dict[str, Any] | None = None
    if event_name == EVENT_PRE_COMPACT:
        add_reason(state, REASON_COMPACTION_PENDING)
    elif event_name == EVENT_POST_COMPACT:
        add_reason(state, REASON_COMPACTION_COMPLETED)
    elif event_name == EVENT_SESSION_START:
        source = payload.get("source")
        if source == SOURCE_RESUME:
            add_reason(state, REASON_SESSION_RESUMED)
        elif source == SOURCE_COMPACT:
            add_reason(state, REASON_COMPACTION_COMPLETED)
        pending_reasons = list(state.get("pending_reasons", []))
        if pending_reasons:
            output = context_output(event_name, recovery_context(pending_reasons))
            state["pending_reasons"] = []
    elif event_name == EVENT_USER_PROMPT_SUBMIT:
        pending_reasons = list(state.get("pending_reasons", []))
        if pending_reasons:
            output = context_output(event_name, recovery_context(pending_reasons))
            state["pending_reasons"] = []
    elif event_name == EVENT_POST_TOOL_USE and is_network_failure(payload.get("tool_response")):
        add_reason(state, REASON_NETWORK_FAILURE)
        output = context_output(event_name, recovery_context([REASON_NETWORK_FAILURE]))

    state["model"] = current_model
    state["cwd_fingerprint"] = current_cwd_fingerprint
    state["last_event"] = event_name
    save_state(state_path, state)
    return output


def main() -> int:
    """运行 Hook；状态目录不可用时仍以无状态方式安全执行。"""

    try:
        payload = read_hook_input()
        output = handle_event(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"systemMessage": f"连续性守卫执行失败：{exc}"}, ensure_ascii=False))
        return SUCCESS_EXIT_CODE
    if output is not None:
        print(json.dumps(output, ensure_ascii=False))
    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
