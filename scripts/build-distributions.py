#!/usr/bin/env python3
"""从单份规则生成各宿主分发包；不安装插件、不改用户配置、不覆盖已有产物。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "codex-noise-filter"
VERSION = json.loads((ROOT / "distribution/plugin/.codex-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
TARGETS = ("codex", "claude", "claude-windows", "harness", "portable", "skill")
PROJECT_PROFILES = {
    "cursor": (".cursor/skills", ".cursor/rules/codex-noise-filter.mdc"),
    "gemini": (".gemini/skills", "GEMINI.md"),
    "opencode": (".opencode/skills", "AGENTS.md"),
    "copilot": (".github/skills", ".github/copilot-instructions.md"),
    "harness": (".dsh/skills", None),
}
IGNORED = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def write_json(path: Path, value: dict) -> None:
    """写入稳定格式的宿主元数据。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validator():
    """复用仓库校验器，不增加第三方依赖。"""
    spec = importlib.util.spec_from_file_location("project_validator", ROOT / "scripts/validate-project.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_skill(destination: Path, codex_ui: bool = False) -> None:
    """所有分发共享同一份正文和 references，宿主 UI 元数据按需加入。"""
    destination.mkdir(parents=True)
    shutil.copy2(ROOT / "SKILL.md", destination / "SKILL.md")
    shutil.copy2(ROOT / "LICENSE", destination / "LICENSE")
    shutil.copytree(ROOT / "references", destination / "references", ignore=IGNORED)
    if codex_ui:
        shutil.copytree(ROOT / "agents", destination / "agents", ignore=IGNORED)


def build_target(target: str, output: Path) -> Path:
    """为单个宿主构造独立根目录；Claude 只使用其原生字段。"""
    manifest = json.loads((ROOT / "distribution/plugin/.codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if target == "skill":
        skill_root = output / NAME
        copy_skill(skill_root)
        return skill_root
    plugin = output / "plugins" / NAME if target in ("codex", "claude", "claude-windows") else output / NAME
    copy_skill(plugin / "skills" / NAME, codex_ui=target == "codex")
    shutil.copy2(ROOT / "LICENSE", plugin / "LICENSE")
    if target == "harness":
        write_json(plugin / "package.json", {
            "name": "dsh-codex-noise-filter", "version": manifest["version"],
            "description": manifest["description"], "type": "module", "main": "index.js",
            "files": ["index.js", "metadata.json", "cordis.patch.yml", "skills", "LICENSE"],
            "license": "Apache-2.0", "dsh": {"bundle": {"patch": "./cordis.patch.yml"}},
        })
        spec = importlib.util.spec_from_file_location("guard_build", ROOT / "distribution/plugin/hooks/continuity_guard.py")
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        _, description = validator().read_frontmatter(ROOT / "SKILL.md")
        write_json(plugin / "metadata.json", {"description": description, "activation": guard.ACTIVATION_CONTEXT})
        shutil.copy2(ROOT / "distribution/harness/index.js", plugin / "index.js")
        (plugin / "cordis.patch.yml").write_text("- insert:\n    - id: codex-noise-filter\n      name: dsh-codex-noise-filter\n", encoding="utf-8")
        return plugin
    if target == "portable":
        write_json(plugin / "plugin.json", {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            **{key: manifest[key] for key in ("name", "version", "description")},
        })
        return plugin
    (plugin / "hooks").mkdir()
    shutil.copy2(ROOT / "distribution/plugin/hooks/continuity_guard.py", plugin / "hooks/continuity_guard.py")
    hooks = json.loads((ROOT / "distribution/plugin/hooks/hooks.json").read_text(encoding="utf-8"))
    if target == "codex":
        write_json(plugin / ".codex-plugin/plugin.json", manifest)
        write_json(output / ".agents/plugins/marketplace.json", json.loads((ROOT / "distribution/marketplace.json").read_text(encoding="utf-8")))
    else:
        # 默认 hooks/hooks.json 自动发现，不在 manifest 再引用同一文件。
        write_json(plugin / ".claude-plugin/plugin.json", {
            key: manifest[key] for key in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")
        })
        # Claude 的失败工具走 PostToolUseFailure，且 PostToolUse 不提供 model 字段；去掉 PostToolUse 避免每次工具调用都启动 Python。
        hooks["hooks"].pop("PostToolUse", None)
        hooks["hooks"]["PostToolUseFailure"] = [{"hooks": [{"type": "command", "timeout": 5}]}]
        for groups in hooks["hooks"].values():
            for group in groups:
                for handler in group["hooks"]:
                    handler.pop("commandWindows", None)
                    handler.pop("statusMessage", None)
                    handler["command"] = 'python3 "${CLAUDE_PLUGIN_ROOT}/hooks/continuity_guard.py"'
                    if target == "claude-windows":
                        handler["shell"] = "powershell"
                        handler["command"] = 'py -3 "$env:CLAUDE_PLUGIN_ROOT/hooks/continuity_guard.py"'
        write_json(output / ".claude-plugin/marketplace.json", {
            "name": "codex-noise-filter-local", "owner": manifest["author"],
            "description": manifest["description"],
            "plugins": [{"name": NAME, "source": f"./plugins/{NAME}", "description": manifest["description"]}],
        })
    write_json(plugin / "hooks/hooks.json", hooks)
    return plugin


def archive(source: Path, destination: Path, include_root: bool) -> None:
    """固定时间、权限和排序，生成内容可复现的上传 ZIP。"""
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                name = path.relative_to(source.parent if include_root else source).as_posix()
                info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, path.read_bytes())


def build_projects(output: Path) -> None:
    """生成可审阅的项目入口，用户合并到实际项目后才生效。"""
    for host, (skill_directory, instruction_path) in PROJECT_PROFILES.items():
        project = output / host
        copy_skill(project / skill_directory / NAME)
        if instruction_path is None:
            continue
        instruction = project / instruction_path
        instruction.parent.mkdir(parents=True, exist_ok=True)
        text = (
            f"编程任务（代码、diff、配置、日志、构建、测试、CI、agent/skill/plugin）使用 `{NAME}`，"
            f"结合前文识别续问。先用宿主技能工具加载；必要时读取项目根目录下 `{skill_directory}/{NAME}/SKILL.md`，"
            "按索引只读取当前任务所需规则。纯翻译、文案和无仓库的常识问答不加载。\n\n"
            "保护已有改动，只读请求不修改；性能优化保持用户模型、推理强度、原始证据和质量验收。"
            "工具缺失时说明边界，不声称已执行。\n"
        )
        if host == "cursor":
            text = "---\ndescription: 编程任务语义路由\nalwaysApply: true\n---\n\n" + text
        instruction.write_text(text, encoding="utf-8")


def npm_archive(source: Path, destination: Path) -> None:
    """生成 npm 可安装的 tarball，无安装脚本或依赖下载。"""
    import gzip
    with destination.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w") as bundle:
            for path in sorted(source.rglob("*")):
                if path.is_file():
                    info = tarfile.TarInfo("package/" + path.relative_to(source).as_posix())
                    info.size = path.stat().st_size
                    info.mode = 0o644
                    with path.open("rb") as data:
                        bundle.addfile(info, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=(*TARGETS, "all"), default="all")
    parser.add_argument("--output", type=Path, default=ROOT / f"dist/release-{VERSION}")
    args = parser.parse_args()
    output = args.output.absolute()
    resolved = output.resolve()
    if output.is_symlink() or resolved == ROOT or resolved in ROOT.parents or (
        resolved.is_relative_to(ROOT) and not resolved.is_relative_to(ROOT / "dist")
    ):
        parser.error("输出必须位于 dist 或独立目录，且不能是源码根或其祖先")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error("输出目录非空；请指定新的目录，已有文件不会被覆盖")
    checks = validator()
    checks.validate_source(ROOT)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".noise-filter-build-", dir=output.parent) as temp:
        stage = Path(temp) / "release"
        stage.mkdir()
        for target in TARGETS if args.target == "all" else (args.target,):
            target_root = stage / target if args.target == "all" else stage
            plugin = build_target(target, target_root)
            if target == "codex":
                checks.validate_marketplace_root(target_root)
            elif target in ("claude", "claude-windows", "portable"):
                checks.validate_other_plugin(plugin, "portable" if target == "portable" else "claude")
            else:
                skill = plugin if target == "skill" else plugin / "skills" / NAME
                checks.read_frontmatter(skill / "SKILL.md")
                checks.validate_markdown_tree(skill)
            if args.target == "all":
                archive(plugin, stage / f"{NAME}-{target}.zip", include_root=target == "skill")
                if target == "harness":
                    npm_archive(plugin, stage / f"dsh-codex-noise-filter-{VERSION}.tgz")
        if args.target == "all":
            build_projects(stage / "projects")
            shutil.copy2(ROOT / "templates/chat-app-instructions.md", stage / "chat-app-instructions.md")
        if output.exists():
            output.rmdir()
        stage.rename(output)
    print(f"分发构建完成: {output}")
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
