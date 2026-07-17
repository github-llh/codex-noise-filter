#!/usr/bin/env python3
"""仅使用标准库验证源码 skill，以及可选的 plugin 构建产物。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
DIRECTIONAL = re.compile("[\u202a-\u202e\u2066-\u2069]")

MIN_DESCRIPTION_LENGTH = 40
MAX_DESCRIPTION_LENGTH = 600
MAX_REFERENCE_LINES = 100
MAX_DEFAULT_PROMPTS = 3
MAX_DEFAULT_PROMPT_LENGTH = 128
EXPECTED_MARKETPLACE_PLUGIN_COUNT = 1
SUCCESS_EXIT_CODE = 0
FAILURE_EXIT_CODE = 1
DELEGATION_REFERENCE_RELATIVE_PATH = Path("references/12-research-and-delegation.md")
DELEGATION_REQUIRED_MARKERS = {
    "不得为了占满并发槽启动 agent",
    "主智能体唯一拥有拆分、派发、追问、停止、综合和最终验收权",
    "委派严格单层",
    "一个通道同一时刻只能有一个所有者",
    "每个子智能体最多做一次有新信息目标的补充追问",
}

FRONTMATTER_OPENING = "---\n"
FRONTMATTER_CLOSING = "\n---\n"
RELATIVE_PATH_PREFIX = "./"
HTTPS_PREFIX = "https://"

SKILL_FRONTMATTER_FIELDS = {"name", "description"}
PLUGIN_ALLOWED_FIELDS = {
    "id",
    "name",
    "version",
    "description",
    "skills",
    "apps",
    "mcpServers",
    "interface",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "hooks",
}
PLUGIN_REQUIRED_FIELDS = {
    "name",
    "version",
    "description",
    "author",
    "skills",
    "hooks",
    "interface",
}
PLUGIN_FORBIDDEN_RUNTIME_FIELDS = {"mcpServers", "apps"}
PLUGIN_INTERFACE_REQUIRED_FIELDS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "defaultPrompt",
}
MARKETPLACE_INSTALLATION_POLICIES = {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}
MARKETPLACE_AUTHENTICATION_POLICIES = {"ON_INSTALL", "ON_USE"}
PLUGIN_ALLOWED_TOP_LEVEL_FILES = {".codex-plugin", "skills", "hooks", "LICENSE"}
PLUGIN_FORBIDDEN_PATH_NAMES = {".DS_Store", "__pycache__"}
PLUGIN_FORBIDDEN_FILE_SUFFIXES = {".pyc", ".pyo"}
LOCAL_SOURCE_TYPE = "local"
MARKETPLACE_MANIFEST_RELATIVE_PATH = Path(".agents/plugins/marketplace.json")
UNSUPPORTED_ROOT_MARKETPLACE_FILENAME = "marketplace.json"

HOOK_CONFIG_TOP_LEVEL_FIELD = "hooks"
HOOK_CONFIG_RELATIVE_PATH = "hooks/hooks.json"
HOOK_MANIFEST_PATH = f"{RELATIVE_PATH_PREFIX}{HOOK_CONFIG_RELATIVE_PATH}"
HOOK_SCRIPT_RELATIVE_PATH = "hooks/continuity_guard.py"
HOOK_COMMAND_MARKER = "$PLUGIN_ROOT/hooks/continuity_guard.py"
HOOK_WINDOWS_COMMAND_MARKER = "%PLUGIN_ROOT%\\hooks\\continuity_guard.py"
HOOK_REQUIRED_EVENTS = {
    "SessionStart",
    "PreCompact",
    "PostCompact",
    "UserPromptSubmit",
    "PostToolUse",
}
HOOK_ALLOWED_EVENTS = HOOK_REQUIRED_EVENTS
HOOK_REQUIRED_MATCHERS = {
    "SessionStart": "resume|compact",
    "PreCompact": "manual|auto",
    "PostCompact": "manual|auto",
    "PostToolUse": "Bash|mcp__.*",
}
HOOK_REQUIRED_SCRIPT_MARKERS = {
    "STATE_SCHEMA_VERSION = 2",
    "CONTINUITY_LEDGER_ITEMS",
    "normalize_reasons",
    "consume_reasons",
    '"event_counts"',
    '"context_injection_count"',
}
MIN_HOOK_TIMEOUT_SECONDS = 1
MAX_HOOK_TIMEOUT_SECONDS = 5


class ValidationError(Exception):
    pass


def read_frontmatter(skill_path: Path) -> tuple[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    frontmatter_body = text[len(FRONTMATTER_OPENING):]
    if not text.startswith(FRONTMATTER_OPENING) or FRONTMATTER_CLOSING not in frontmatter_body:
        raise ValidationError(f"{skill_path}: YAML frontmatter 分隔符无效")
    raw, _, _ = frontmatter_body.partition(FRONTMATTER_CLOSING)
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValidationError(f"{skill_path}: 不支持多行 frontmatter 字段")
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    if set(fields) != SKILL_FRONTMATTER_FIELDS:
        raise ValidationError(f"{skill_path}: frontmatter 只能包含 name 和 description")
    if not NAME_RE.fullmatch(fields["name"]):
        raise ValidationError(f"{skill_path}: skill 名称无效")
    if not MIN_DESCRIPTION_LENGTH <= len(fields["description"]) <= MAX_DESCRIPTION_LENGTH:
        raise ValidationError(
            f"{skill_path}: description 长度必须在 "
            f"{MIN_DESCRIPTION_LENGTH} 到 {MAX_DESCRIPTION_LENGTH} 个字符之间"
        )
    return fields["name"], fields["description"]


def validate_markdown_tree(skill_root: Path) -> None:
    markdown = [skill_root / "SKILL.md", *sorted((skill_root / "references").glob("*.md"))]
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if DIRECTIONAL.search(text):
            raise ValidationError(f"{path}: 包含方向控制字符")
        for target in LINK_RE.findall(text):
            target, _, _ = target.partition("#")
            if not target or re.match(r"^[a-z]+://", target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                raise ValidationError(f"{path}: 本地链接失效 {target}")

    skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    for reference in sorted((skill_root / "references").glob("*.md")):
        relative = reference.relative_to(skill_root).as_posix()
        if relative not in skill_text:
            raise ValidationError(f"SKILL.md 未直接链接 {relative}")
        if len(reference.read_text(encoding="utf-8").splitlines()) > MAX_REFERENCE_LINES:
            raise ValidationError(f"{reference}: reference 应控制在 {MAX_REFERENCE_LINES} 行内或继续拆分")


def validate_repo_markdown(root: Path) -> None:
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts or "dist" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if DIRECTIONAL.search(text):
            raise ValidationError(f"{path}: 包含方向控制字符")
        for target in LINK_RE.findall(text):
            target, _, _ = target.partition("#")
            if not target or re.match(r"^[a-z]+://", target):
                continue
            if not (path.parent / target).resolve().exists():
                raise ValidationError(f"{path}: 本地链接失效 {target}")


def validate_source(root: Path) -> None:
    name, _ = read_frontmatter(root / "SKILL.md")
    if name != root.name:
        raise ValidationError(f"skill 名称 {name!r} 必须与目录名 {root.name!r} 一致")
    validate_markdown_tree(root)
    validate_repo_markdown(root)

    delegation_reference = root / DELEGATION_REFERENCE_RELATIVE_PATH
    delegation_text = delegation_reference.read_text(encoding="utf-8")
    missing_delegation_markers = {
        marker for marker in DELEGATION_REQUIRED_MARKERS if marker not in delegation_text
    }
    if missing_delegation_markers:
        raise ValidationError(
            f"{delegation_reference}: 缺少受控委派与防循环边界 "
            f"{sorted(missing_delegation_markers)}"
        )

    ui_text = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    required_ui = (
        f'display_name: "{name}"',
        "short_description:",
        "default_prompt:",
        "allow_implicit_invocation: true",
    )
    for field in required_ui:
        if field not in ui_text:
            raise ValidationError(f"agents/openai.yaml: 字段缺失或已过期 {field}")

    manifest = json.loads((root / "distribution/plugin/.codex-plugin/plugin.json").read_text())
    marketplace = json.loads((root / "distribution/marketplace.json").read_text())
    validate_manifest(manifest, root / "distribution/plugin/.codex-plugin/plugin.json")
    if manifest["name"] != name:
        raise ValidationError("plugin 名称必须与 skill 名称一致")
    validate_marketplace(marketplace, manifest["name"])


def validate_manifest(manifest: dict, path: Path) -> None:
    unknown = set(manifest) - PLUGIN_ALLOWED_FIELDS
    if unknown:
        raise ValidationError(f"{path}: 包含不支持的字段 {sorted(unknown)}")
    missing = PLUGIN_REQUIRED_FIELDS - manifest.keys()
    if missing:
        raise ValidationError(f"{path}: 缺少字段 {sorted(missing)}")
    if not NAME_RE.fullmatch(manifest["name"]):
        raise ValidationError(f"{path}: plugin 名称无效")
    if not SEMVER_RE.fullmatch(manifest["version"]):
        raise ValidationError(f"{path}: 语义化版本无效")
    if not manifest["skills"].startswith(RELATIVE_PATH_PREFIX):
        raise ValidationError(f"{path}: skills 路径必须以 {RELATIVE_PATH_PREFIX} 开头")
    if manifest["hooks"] != HOOK_MANIFEST_PATH:
        raise ValidationError(f"{path}: hooks 路径必须是 {HOOK_MANIFEST_PATH}")
    if PLUGIN_FORBIDDEN_RUNTIME_FIELDS.intersection(manifest):
        raise ValidationError(f"{path}: 存在未声明的运行时表面")
    validate_hooks(path.parent.parent)
    author = manifest["author"]
    if not isinstance(author, dict) or not author.get("name"):
        raise ValidationError(f"{path}: 必须提供 author.name")
    if author.get("url") and not author["url"].startswith(HTTPS_PREFIX):
        raise ValidationError(f"{path}: author.url 必须使用 https")

    interface = manifest["interface"]
    missing_interface = PLUGIN_INTERFACE_REQUIRED_FIELDS - interface.keys()
    if missing_interface:
        raise ValidationError(f"{path}: 缺少 interface 字段 {sorted(missing_interface)}")
    if not isinstance(interface["capabilities"], list) or not all(
        isinstance(value, str) and value.strip() for value in interface["capabilities"]
    ):
        raise ValidationError(f"{path}: capabilities 必须是非空字符串数组")
    if interface.get("websiteURL") and not interface["websiteURL"].startswith(HTTPS_PREFIX):
        raise ValidationError(f"{path}: websiteURL 必须使用 https")
    if interface.get("brandColor") and not HEX_COLOR_RE.fullmatch(interface["brandColor"]):
        raise ValidationError(f"{path}: brandColor 必须使用 #RRGGBB 格式")
    prompts = interface.get("defaultPrompt", [])
    if len(prompts) > MAX_DEFAULT_PROMPTS or any(
        len(prompt) > MAX_DEFAULT_PROMPT_LENGTH for prompt in prompts
    ):
        raise ValidationError(
            f"{path}: defaultPrompt 超出 UI 限制，最多 {MAX_DEFAULT_PROMPTS} 条，"
            f"每条最多 {MAX_DEFAULT_PROMPT_LENGTH} 个字符"
        )


def validate_hooks(plugin_root: Path) -> None:
    hook_path = plugin_root / HOOK_CONFIG_RELATIVE_PATH
    if not hook_path.is_file():
        raise ValidationError(f"plugin 默认 Hook 文件不存在: {HOOK_CONFIG_RELATIVE_PATH}")
    hook_script = plugin_root / HOOK_SCRIPT_RELATIVE_PATH
    if not hook_script.is_file():
        raise ValidationError(f"plugin Hook 脚本不存在: {HOOK_SCRIPT_RELATIVE_PATH}")
    hook_script_text = hook_script.read_text(encoding="utf-8")
    missing_script_markers = {
        marker for marker in HOOK_REQUIRED_SCRIPT_MARKERS if marker not in hook_script_text
    }
    if missing_script_markers:
        raise ValidationError(
            f"{hook_script}: 缺少连续性保护实现 {sorted(missing_script_markers)}"
        )

    hook_config = json.loads(hook_path.read_text(encoding="utf-8"))
    if set(hook_config) != {HOOK_CONFIG_TOP_LEVEL_FIELD}:
        raise ValidationError(f"{hook_path}: 顶层只能包含 hooks")
    events = hook_config[HOOK_CONFIG_TOP_LEVEL_FIELD]
    if not isinstance(events, dict):
        raise ValidationError(f"{hook_path}: hooks 必须是对象")
    missing_events = HOOK_REQUIRED_EVENTS - events.keys()
    unknown_events = events.keys() - HOOK_ALLOWED_EVENTS
    if missing_events or unknown_events:
        raise ValidationError(
            f"{hook_path}: Hook 事件不完整，缺少 {sorted(missing_events)}，"
            f"未知 {sorted(unknown_events)}"
        )

    for event_name, matcher_groups in events.items():
        if not isinstance(matcher_groups, list) or not matcher_groups:
            raise ValidationError(f"{hook_path}: {event_name} 必须包含 matcher group")
        for matcher_group in matcher_groups:
            expected_matcher = HOOK_REQUIRED_MATCHERS.get(event_name)
            actual_matcher = matcher_group.get("matcher") if isinstance(matcher_group, dict) else None
            if expected_matcher is None and actual_matcher is not None:
                raise ValidationError(f"{hook_path}: {event_name} 不应声明 matcher")
            if expected_matcher is not None and actual_matcher != expected_matcher:
                raise ValidationError(
                    f"{hook_path}: {event_name} matcher 必须是 {expected_matcher}"
                )
            handlers = matcher_group.get("hooks") if isinstance(matcher_group, dict) else None
            if not isinstance(handlers, list) or not handlers:
                raise ValidationError(f"{hook_path}: {event_name} 必须包含 command Hook")
            for handler in handlers:
                if not isinstance(handler, dict) or handler.get("type") != "command":
                    raise ValidationError(f"{hook_path}: {event_name} 只允许 command Hook")
                command = handler.get("command")
                windows_command = handler.get("commandWindows")
                if not isinstance(command, str) or HOOK_COMMAND_MARKER not in command:
                    raise ValidationError(f"{hook_path}: {event_name} 必须通过 PLUGIN_ROOT 定位脚本")
                if (
                    not isinstance(windows_command, str)
                    or HOOK_WINDOWS_COMMAND_MARKER not in windows_command
                ):
                    raise ValidationError(f"{hook_path}: {event_name} 缺少 Windows 插件脚本路径")
                timeout = handler.get("timeout")
                if (
                    not isinstance(timeout, int)
                    or not MIN_HOOK_TIMEOUT_SECONDS <= timeout <= MAX_HOOK_TIMEOUT_SECONDS
                ):
                    raise ValidationError(
                        f"{hook_path}: {event_name} timeout 必须在 "
                        f"{MIN_HOOK_TIMEOUT_SECONDS} 到 {MAX_HOOK_TIMEOUT_SECONDS} 秒之间"
                    )


def validate_marketplace(marketplace: dict, plugin_name: str) -> None:
    entries = [item for item in marketplace.get("plugins", []) if item.get("name") == plugin_name]
    if len(entries) != EXPECTED_MARKETPLACE_PLUGIN_COUNT:
        raise ValidationError("marketplace 必须且只能包含一个同名 plugin")
    (entry,) = entries
    path = entry.get("source", {}).get("path", "")
    if not path.startswith(RELATIVE_PATH_PREFIX) or ".." in Path(path).parts:
        raise ValidationError(
            f"marketplace source.path 必须是以 {RELATIVE_PATH_PREFIX} 开头且不越界的相对路径"
        )
    policy = entry.get("policy", {})
    if not {"installation", "authentication"} <= policy.keys() or "category" not in entry:
        raise ValidationError("marketplace 条目缺少 policy 或 category")
    if policy["installation"] not in MARKETPLACE_INSTALLATION_POLICIES:
        raise ValidationError("marketplace installation 策略无效")
    if policy["authentication"] not in MARKETPLACE_AUTHENTICATION_POLICIES:
        raise ValidationError("marketplace authentication 策略无效")


def validate_plugin(plugin_root: Path) -> None:
    manifest_path = plugin_root / ".codex-plugin/plugin.json"
    manifest = json.loads(manifest_path.read_text())
    validate_manifest(manifest, manifest_path)
    skill_root = plugin_root / "skills" / manifest["name"]
    read_frontmatter(skill_root / "SKILL.md")
    validate_markdown_tree(skill_root)
    extras = {path.name for path in plugin_root.iterdir()} - PLUGIN_ALLOWED_TOP_LEVEL_FILES
    if extras:
        raise ValidationError(f"plugin 包含预期外的顶层文件: {sorted(extras)}")
    for path in plugin_root.rglob("*"):
        if PLUGIN_FORBIDDEN_PATH_NAMES.intersection(path.parts):
            raise ValidationError(f"plugin 包含缓存或系统文件: {path.relative_to(plugin_root)}")
        if path.is_file() and path.suffix in PLUGIN_FORBIDDEN_FILE_SUFFIXES:
            raise ValidationError(f"plugin 包含 Python 字节码: {path.relative_to(plugin_root)}")


def validate_marketplace_root(root: Path) -> None:
    manifest_path = root / MARKETPLACE_MANIFEST_RELATIVE_PATH
    unsupported_manifest_path = root / UNSUPPORTED_ROOT_MARKETPLACE_FILENAME
    if unsupported_manifest_path.exists():
        raise ValidationError(
            f"{root}: marketplace manifest 不应位于根目录，请使用 "
            f"{MARKETPLACE_MANIFEST_RELATIVE_PATH}"
        )
    marketplace = json.loads(manifest_path.read_text())
    entries = marketplace.get("plugins", [])
    if not entries:
        raise ValidationError(f"{root}: marketplace 中没有 plugin")
    for entry in entries:
        source = entry.get("source", {})
        if source.get("source") != LOCAL_SOURCE_TYPE:
            continue
        raw_path = source.get("path", "")
        plugin_root = (root / raw_path).resolve()
        if not plugin_root.is_relative_to(root.resolve()):
            raise ValidationError(f"{root}: marketplace 路径越出根目录")
        validate_plugin(plugin_root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin", type=Path)
    parser.add_argument("--marketplace-root", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        validate_source(root)
        if args.plugin:
            validate_plugin(args.plugin.resolve())
        if args.marketplace_root:
            validate_marketplace_root(args.marketplace_root.resolve())
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return FAILURE_EXIT_CODE
    print("验证通过")
    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
