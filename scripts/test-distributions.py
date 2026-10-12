#!/usr/bin/env python3
"""验证跨宿主分发内容一致、可复现，以及构建不覆盖用户文件。"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("distributions", ROOT / "scripts/build-distributions.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class DistributionTest(unittest.TestCase):
    """实际生成包，检查安装入口与可执行脚本，而非只匹配文档措辞。"""

    def test_all_packages_share_canonical_rules_and_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            for target in builder.TARGETS:
                with self.subTest(target=target):
                    output = Path(temp) / target
                    plugin = builder.build_target(target, output)
                    skill = plugin if target == "skill" else plugin / "skills" / builder.NAME
                    self.assertEqual((ROOT / "SKILL.md").read_bytes(), (skill / "SKILL.md").read_bytes())
                    self.assertEqual(
                        {p.name: p.read_bytes() for p in (ROOT / "references").glob("*.md")},
                        {p.name: p.read_bytes() for p in (skill / "references").glob("*.md")},
                    )
                    if target in ("codex", "claude", "claude-windows"):
                        hooks = json.loads((plugin / "hooks/hooks.json").read_text(encoding="utf-8"))["hooks"]
                        self.assertIn("startup", hooks["SessionStart"][0]["matcher"])
                        self.assertEqual(target != "codex", "PostToolUseFailure" in hooks)
                        self.assertEqual(target == "codex", "PostToolUse" in hooks)
                        self.assertEqual((ROOT / "distribution/plugin/hooks/continuity_guard.py").read_bytes(), (plugin / "hooks/continuity_guard.py").read_bytes())
                        environment = os.environ.copy()
                        environment.pop("PLUGIN_DATA", None)
                        environment.pop("CLAUDE_PLUGIN_DATA", None)
                        variable = "PLUGIN_DATA" if target == "codex" else "CLAUDE_PLUGIN_DATA"
                        environment[variable] = str(Path(temp) / "data" / target)
                        result = subprocess.run([sys.executable, str(plugin / "hooks/continuity_guard.py")], input=json.dumps({"session_id": target, "hook_event_name": "SessionStart", "source": "startup"}), text=True, capture_output=True, env=environment, timeout=5)
                        self.assertEqual(0, result.returncode, result.stderr)
                        self.assertEqual("SessionStart", json.loads(result.stdout)["hookSpecificOutput"]["hookEventName"])
                    else:
                        self.assertFalse((plugin / "hooks").exists())

    def test_zip_is_reproducible_and_has_correct_upload_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            for target in builder.TARGETS:
                plugin = builder.build_target(target, Path(temp) / target)
                first, second = Path(temp) / f"{target}-1.zip", Path(temp) / f"{target}-2.zip"
                builder.archive(plugin, first, include_root=target == "skill")
                builder.archive(plugin, second, include_root=target == "skill")
                self.assertEqual(first.read_bytes(), second.read_bytes())
                with zipfile.ZipFile(first) as bundle:
                    names = set(bundle.namelist())
                    expected = {
                        "codex": ".codex-plugin/plugin.json",
                        "claude": ".claude-plugin/plugin.json",
                        "claude-windows": ".claude-plugin/plugin.json",
                        "portable": "plugin.json", "skill": f"{builder.NAME}/SKILL.md",
                        "harness": "package.json",
                    }[target]
                    self.assertIn(expected, names)
                    self.assertFalse(any("__pycache__" in name or ".." in Path(name).parts for name in names))

    def test_project_profiles_point_to_complete_skills(self) -> None:
        """项目规则指向当前包内真实路径，不把生成当作实际安装。"""
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            builder.build_projects(output)
            for host, (directory, instructions) in builder.PROJECT_PROFILES.items():
                skill = output / host / directory / builder.NAME
                self.assertEqual((ROOT / "SKILL.md").read_bytes(), (skill / "SKILL.md").read_bytes())
                if instructions:
                    text = (output / host / instructions).read_text(encoding="utf-8")
                    self.assertIn(f"{directory}/{builder.NAME}/SKILL.md", text)

    def test_harness_tarball_is_installable_layout_without_scripts(self) -> None:
        """npm tarball 包含 bundle 声明、入口与资源，不携带安装副作用。"""
        import tarfile
        with tempfile.TemporaryDirectory() as temp:
            plugin = builder.build_target("harness", Path(temp) / "source")
            first, second = Path(temp) / "one.tgz", Path(temp) / "two.tgz"
            builder.npm_archive(plugin, first)
            builder.npm_archive(plugin, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with tarfile.open(first) as bundle:
                manifest = json.load(bundle.extractfile("package/package.json"))
                self.assertNotIn("scripts", manifest)
                self.assertNotIn("dependencies", manifest)
                self.assertIn("package/" + manifest["main"], bundle.getnames())
                self.assertIn("package/" + manifest["dsh"]["bundle"]["patch"].removeprefix("./"), bundle.getnames())

    def test_unsafe_and_nonempty_outputs_preserve_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            occupied = Path(temp) / "occupied"
            occupied.mkdir()
            sentinel = occupied / "user-file.txt"
            sentinel.write_text("keep", encoding="utf-8")
            alias = Path(temp) / "source-alias"
            alias.symlink_to(ROOT, target_is_directory=True)
            for path in (ROOT, ROOT.parent, ROOT / "references/output", occupied, alias):
                result = subprocess.run([sys.executable, str(ROOT / "scripts/build-distributions.py"), "--output", str(path)], capture_output=True, text=True, timeout=10)
                self.assertNotEqual(0, result.returncode, str(path))
            self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
