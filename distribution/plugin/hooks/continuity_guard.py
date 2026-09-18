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


STATE_SCHEMA_VERSION = 2
LEGACY_STATE_SCHEMA_VERSION = 1
MAX_PENDING_REASONS = 8
MAX_RESPONSE_SCAN_CHARS = 32_768
MAX_RESPONSE_SCAN_DEPTH = 16
MAX_RESPONSE_SCAN_ITEMS = 1_024
MAX_STATE_FILES = 64
MAX_COUNTER_VALUE = 2_147_483_647
MAX_INPUT_CHARS = 8 * 1024 * 1024
MAX_STATE_CHARS = 65_536
SUCCESS_EXIT_CODE = 0

PLUGIN_DATA_ENV = "PLUGIN_DATA"
CLAUDE_PLUGIN_DATA_ENV = "CLAUDE_PLUGIN_DATA"
STATE_DIRECTORY_NAME = "continuity"
STATE_FILE_SUFFIX = ".json"
TEMP_FILE_SUFFIX = ".tmp"

EVENT_SESSION_START = "SessionStart"
EVENT_PRE_COMPACT = "PreCompact"
EVENT_POST_COMPACT = "PostCompact"
EVENT_USER_PROMPT_SUBMIT = "UserPromptSubmit"
EVENT_POST_TOOL_USE = "PostToolUse"
EVENT_POST_TOOL_USE_FAILURE = "PostToolUseFailure"
SUPPORTED_EVENTS = (
    EVENT_SESSION_START,
    EVENT_PRE_COMPACT,
    EVENT_POST_COMPACT,
    EVENT_USER_PROMPT_SUBMIT,
    EVENT_POST_TOOL_USE,
    EVENT_POST_TOOL_USE_FAILURE,
)

CONTEXT_KIND_RECOVERY = "recovery"
CONTEXT_KIND_ACTIVATION = "activation"
ACTIVATION_CONTEXT = (
    "当前任务若涉及真实代码、diff、配置、日志、构建、测试或 agent/skill/plugin，"
    "使用已安装的 codex-noise-filter，按 SKILL.md 索引读取必要规则。"
    "结合对话理解简短续问；纯翻译、文案和无仓库的常识问答不启用。"
    "区分只读与实施，保持用户模型、推理配置和质量验收要求。"
)

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
KNOWN_REASONS = frozenset(REASON_LABELS)

CONTINUITY_LEDGER_ITEMS = (
    "最新用户目标、验收条件与不可违反的高优先级约束",
    "已确认事实、根因假设、关键决策及其证据来源",
    "已修改文件、真实落盘状态和仍在运行的工具",
    "已运行验证、结果、未覆盖边界和外部操作的幂等性状态",
    "明确禁止重试的路径（doNotRetry）与唯一下一步",
)

RECOVERY_STEPS = (
    "重读最新用户目标、验收条件和高优先级指令，不要求用户重复已提供的信息。",
    "在宿主可访问工作区时核对 git status、git diff、落盘文件、运行中工具及外部写操作回执；缺少能力时说明边界。",
    "重建目标、约束、已确认事实、关键决策、已改文件、验证状态、doNotRetry 和唯一下一步。",
    "若旧摘要、旧模型结论或工具回执与当前证据冲突，以当前工作区和最新指令为准。",
    "从唯一下一步继续，不重复已经有成功回执或可能产生副作用的操作。",
)


def read_hook_input() -> dict[str, Any]:
    """有界读取宿主 Hook 输入，不读取 transcript 或改变原始工具结果。"""

    raw = sys.stdin.read(MAX_INPUT_CHARS + 1)
    if len(raw) > MAX_INPUT_CHARS:
        raise ValueError("Hook 输入超过扫描上限")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Hook 输入必须是 JSON 对象")
    return payload


def fingerprint(value: str) -> str:
    """生成不可逆指纹，避免把会话标识和本机路径写入状态文件。"""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_state_path(payload: dict[str, Any]) -> Path | None:
    """返回当前会话的插件私有状态文件；缺少宿主目录时安全降级。"""

    plugin_data = os.environ.get(PLUGIN_DATA_ENV) or os.environ.get(CLAUDE_PLUGIN_DATA_ENV)
    session_id = payload.get("session_id")
    if not plugin_data or not isinstance(session_id, str) or not session_id:
        return None
    state_directory = Path(plugin_data) / STATE_DIRECTORY_NAME
    return state_directory / f"{fingerprint(session_id)}{STATE_FILE_SUFFIX}"


def empty_state() -> dict[str, Any]:
    """创建不包含用户内容和工具原始输出的最小状态。"""

    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "model": "",
        "cwd_fingerprint": "",
        "last_event": "",
        "event_counts": {},
        "context_injection_count": 0,
        "last_context_event": "",
        "last_context_kind": "",
        "last_context_reasons": [],
        "pending_reasons": [],
    }


def normalize_reasons(value: Any) -> list[str]:
    """只保留守卫已知原因，防止私有状态被篡改后注入任意上下文。"""

    if not isinstance(value, list):
        return []
    reasons: list[str] = []
    for reason in value:
        if isinstance(reason, str) and reason in KNOWN_REASONS and reason not in reasons:
            reasons.append(reason)
    return reasons[-MAX_PENDING_REASONS:]


def normalize_counter(value: Any) -> int:
    """把持久化计数限制在稳定的非负整数范围。"""

    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        return 0
    return min(value, MAX_COUNTER_VALUE)


def load_state(path: Path | None) -> dict[str, Any]:
    """读取并迁移状态；损坏或未知版本状态按空状态处理。"""

    if path is None or not path.exists():
        return empty_state()
    try:
        with path.open(encoding="utf-8") as source:
            raw = source.read(MAX_STATE_CHARS + 1)
        if len(raw) > MAX_STATE_CHARS:
            return empty_state()
        stored_state = json.loads(raw)
    except (OSError, ValueError, RecursionError):
        return empty_state()
    if not isinstance(stored_state, dict) or stored_state.get("schema_version") not in (
        LEGACY_STATE_SCHEMA_VERSION,
        STATE_SCHEMA_VERSION,
    ):
        return empty_state()

    state = empty_state()
    for field in ("model", "cwd_fingerprint", "last_event"):
        value = stored_state.get(field)
        if isinstance(value, str):
            state[field] = value
    state["pending_reasons"] = normalize_reasons(stored_state.get("pending_reasons"))

    if stored_state.get("schema_version") == STATE_SCHEMA_VERSION:
        stored_event_counts = stored_state.get("event_counts")
        if isinstance(stored_event_counts, dict):
            state["event_counts"] = {
                event_name: normalize_counter(stored_event_counts.get(event_name))
                for event_name in SUPPORTED_EVENTS
                if normalize_counter(stored_event_counts.get(event_name))
            }
        state["context_injection_count"] = normalize_counter(
            stored_state.get("context_injection_count")
        )
        for field in ("last_context_event", "last_context_kind"):
            value = stored_state.get(field)
            if isinstance(value, str):
                state[field] = value
        state["last_context_reasons"] = normalize_reasons(
            stored_state.get("last_context_reasons")
        )
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
    """原子写入私有状态；只在新会话建档时扫描历史目录。"""

    if path is None:
        return
    temporary_path = path.with_name(f"{path.name}.{os.getpid()}{TEMP_FILE_SUFFIX}")
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        is_new_session = not path.exists()
        temporary_path.write_text(
            json.dumps(state, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        temporary_path.chmod(0o600)
        temporary_path.replace(path)
        if is_new_session:
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

    if reason not in KNOWN_REASONS:
        return
    pending_reasons = normalize_reasons(state.get("pending_reasons"))
    if reason not in pending_reasons:
        pending_reasons.append(reason)
    state["pending_reasons"] = pending_reasons[-MAX_PENDING_REASONS:]


def remove_reason(state: dict[str, Any], reason: str) -> None:
    """移除已经被更精确状态替代的待恢复原因。"""

    state["pending_reasons"] = [
        value for value in normalize_reasons(state.get("pending_reasons")) if value != reason
    ]


def consume_reasons(state: dict[str, Any]) -> list[str]:
    """按稳定顺序消费待恢复原因，保证一次变化只注入一次。"""

    reasons = normalize_reasons(state.get("pending_reasons"))
    state["pending_reasons"] = []
    return reasons


def record_event(state: dict[str, Any], event_name: str) -> None:
    """记录有界事件计数，提供不包含用户内容的执行证据。"""

    if event_name not in SUPPORTED_EVENTS:
        return
    event_counts = state.get("event_counts")
    if not isinstance(event_counts, dict):
        event_counts = {}
    event_counts[event_name] = min(
        normalize_counter(event_counts.get(event_name)) + 1,
        MAX_COUNTER_VALUE,
    )
    state["event_counts"] = event_counts


def response_fragments(response: Any):
    """使用全局节点、深度和字符预算扫描副本，避免宽树或大字符串放大开销。"""

    stack = [(iter((response,)), 0)]
    visited = 0
    remaining = MAX_RESPONSE_SCAN_CHARS
    while stack and visited < MAX_RESPONSE_SCAN_ITEMS and remaining > 0:
        iterator, depth = stack[-1]
        try:
            value = next(iterator)
        except StopIteration:
            stack.pop()
            continue
        visited += 1
        yield value, remaining
        if isinstance(value, str):
            remaining -= min(len(value), remaining)
        elif depth < MAX_RESPONSE_SCAN_DEPTH:
            if isinstance(value, dict):
                stack.append((iter(value.values()), depth + 1))
            elif isinstance(value, list):
                stack.append((iter(value), depth + 1))


def is_network_failure(response: Any, failed_event: bool = False) -> bool:
    """失败信号与网络特征必须同时存在；只分析副本，不过滤模型的原始证据。"""

    failed = failed_event
    network = False
    for value, remaining in response_fragments(response):
        if isinstance(value, dict):
            failed = failed or any(
                isinstance(value.get(field), int)
                and not isinstance(value.get(field), bool)
                and value[field] != SUCCESS_EXIT_CODE
                for field in EXIT_CODE_FIELDS
            ) or any(value.get(field) is True for field in FAILURE_BOOLEAN_FIELDS)
            failed = failed or any(value.get(field) for field in FAILURE_VALUE_FIELDS)
            failed = failed or any(
                isinstance(value.get(field), str)
                and value[field].lower() in FAILURE_STATUSES
                for field in FAILURE_STATUS_FIELDS
            )
        elif isinstance(value, str):
            network = network or any(
                pattern.search(value[:remaining]) for pattern in NETWORK_FAILURE_PATTERNS
            )
        if failed and network:
            return True
    return False


def recovery_context(reasons: list[str]) -> str:
    """构造供模型执行的连续性复核要求。"""

    labels = [REASON_LABELS[reason] for reason in normalize_reasons(reasons)]
    reason_text = "、".join(labels) if labels else "连续性状态发生变化"
    steps = "\n".join(f"{index}. {step}" for index, step in enumerate(RECOVERY_STEPS, 1))
    ledger = "\n".join(f"- {item}" for item in CONTINUITY_LEDGER_ITEMS)
    return (
        f"连续性守卫已自动触发，原因：{reason_text}。"
        f"为避免过期上下文覆盖当前事实，继续任务前执行以下复核：\n{steps}\n"
        f"复核后的连续性账本至少覆盖：\n{ledger}"
    )


def context_output(
    state: dict[str, Any],
    event_name: str,
    context: str,
    context_kind: str,
    reasons: list[str],
) -> dict[str, Any]:
    """返回额外开发者上下文，并记录不包含用户内容的注入证据。"""

    state["context_injection_count"] = min(
        normalize_counter(state.get("context_injection_count")) + 1,
        MAX_COUNTER_VALUE,
    )
    state["last_context_event"] = event_name
    state["last_context_kind"] = context_kind
    state["last_context_reasons"] = normalize_reasons(reasons)

    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": context,
        }
    }


def handle_event(payload: dict[str, Any]) -> dict[str, Any] | None:
    """处理支持的连续性事件，并返回可选的 Hook 输出。"""

    event_name = str(payload.get("hook_event_name", ""))
    if event_name not in SUPPORTED_EVENTS:
        return None
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

    tool_event = event_name in (EVENT_POST_TOOL_USE, EVENT_POST_TOOL_USE_FAILURE)
    response = payload.get("error") if event_name == EVENT_POST_TOOL_USE_FAILURE else payload.get("tool_response")
    network_failure = tool_event and is_network_failure(
        response, failed_event=event_name == EVENT_POST_TOOL_USE_FAILURE
    )
    # 普通工具结果走只读快路径；恢复原因和元数据变化不能被快路径丢弃。
    if tool_event and not network_failure and not state["pending_reasons"]:
        return None
    record_event(state, event_name)
    output: dict[str, Any] | None = None
    if event_name == EVENT_PRE_COMPACT:
        add_reason(state, REASON_COMPACTION_PENDING)
    elif event_name == EVENT_POST_COMPACT:
        remove_reason(state, REASON_COMPACTION_PENDING)
        add_reason(state, REASON_COMPACTION_COMPLETED)
    elif event_name == EVENT_SESSION_START:
        source = payload.get("source")
        if source == SOURCE_RESUME:
            add_reason(state, REASON_SESSION_RESUMED)
        elif source == SOURCE_COMPACT:
            remove_reason(state, REASON_COMPACTION_PENDING)
            add_reason(state, REASON_COMPACTION_COMPLETED)
        pending_reasons = consume_reasons(state)
        if pending_reasons:
            output = context_output(
                state,
                event_name,
                ACTIVATION_CONTEXT + "\n" + recovery_context(pending_reasons),
                CONTEXT_KIND_RECOVERY,
                pending_reasons,
            )
    elif event_name == EVENT_USER_PROMPT_SUBMIT:
        pending_reasons = consume_reasons(state)
        if pending_reasons:
            output = context_output(
                state,
                event_name,
                ACTIVATION_CONTEXT + "\n" + recovery_context(pending_reasons),
                CONTEXT_KIND_RECOVERY,
                pending_reasons,
            )
    elif tool_event:
        if network_failure:
            add_reason(state, REASON_NETWORK_FAILURE)
        pending_reasons = consume_reasons(state)
        if pending_reasons:
            output = context_output(
                state, event_name,
                ACTIVATION_CONTEXT + "\n" + recovery_context(pending_reasons),
                CONTEXT_KIND_RECOVERY, pending_reasons,
            )

    if output is None and event_name in (EVENT_SESSION_START, EVENT_USER_PROMPT_SUBMIT):
        output = context_output(state, event_name, ACTIVATION_CONTEXT, CONTEXT_KIND_ACTIVATION, [])

    if current_model:
        state["model"] = current_model
    if current_cwd_fingerprint:
        state["cwd_fingerprint"] = current_cwd_fingerprint
    state["last_event"] = event_name
    save_state(state_path, state)
    return output


def main() -> int:
    """运行 Hook；状态目录不可用时仍以无状态方式安全执行。"""

    try:
        payload = read_hook_input()
        output = handle_event(payload)
    except (OSError, ValueError, RecursionError):
        print(json.dumps({"systemMessage": "连续性守卫无法处理本次输入，退回指令级复核；原始工具结果未修改。"}, ensure_ascii=False))
        return SUCCESS_EXIT_CODE
    if output is not None:
        print(json.dumps(output, ensure_ascii=False))
    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
