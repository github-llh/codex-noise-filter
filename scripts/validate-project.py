#!/usr/bin/env python3
"""Validate the source skill and an optional built plugin using stdlib only."""

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


class ValidationError(Exception):
    pass


def read_frontmatter(skill_path: Path) -> tuple[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValidationError(f"{skill_path}: invalid YAML frontmatter delimiters")
    raw = text.split("\n---\n", 1)[0][4:]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValidationError(f"{skill_path}: unsupported multiline frontmatter")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    if set(fields) != {"name", "description"}:
        raise ValidationError(f"{skill_path}: frontmatter must contain only name and description")
    if not NAME_RE.fullmatch(fields["name"]):
        raise ValidationError(f"{skill_path}: invalid skill name")
    if not (40 <= len(fields["description"]) <= 600):
        raise ValidationError(f"{skill_path}: description length must be 40..600 characters")
    return fields["name"], fields["description"]


def validate_markdown_tree(skill_root: Path) -> None:
    markdown = [skill_root / "SKILL.md", *sorted((skill_root / "references").glob("*.md"))]
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if DIRECTIONAL.search(text):
            raise ValidationError(f"{path}: contains directional control characters")
        for target in LINK_RE.findall(text):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                raise ValidationError(f"{path}: broken local link {target}")

    skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    for reference in sorted((skill_root / "references").glob("*.md")):
        relative = reference.relative_to(skill_root).as_posix()
        if relative not in skill_text:
            raise ValidationError(f"SKILL.md does not link directly to {relative}")
        if len(reference.read_text(encoding="utf-8").splitlines()) > 100:
            raise ValidationError(f"{reference}: keep references under 100 lines or add a split")


def validate_repo_markdown(root: Path) -> None:
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts or "dist" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if DIRECTIONAL.search(text):
            raise ValidationError(f"{path}: contains directional control characters")
        for target in LINK_RE.findall(text):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target):
                continue
            if not (path.parent / target).resolve().exists():
                raise ValidationError(f"{path}: broken local link {target}")


def validate_source(root: Path) -> None:
    name, _ = read_frontmatter(root / "SKILL.md")
    if name != root.name:
        raise ValidationError(f"skill name {name!r} must match folder {root.name!r}")
    validate_markdown_tree(root)
    validate_repo_markdown(root)

    ui_text = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    required_ui = (
        f'display_name: "{name}"',
        "short_description:",
        "default_prompt:",
        "allow_implicit_invocation: true",
    )
    for field in required_ui:
        if field not in ui_text:
            raise ValidationError(f"agents/openai.yaml: missing or stale {field}")

    manifest = json.loads((root / "distribution/plugin/.codex-plugin/plugin.json").read_text())
    marketplace = json.loads((root / "distribution/marketplace.json").read_text())
    validate_manifest(manifest, root / "distribution/plugin/.codex-plugin/plugin.json")
    if manifest["name"] != name:
        raise ValidationError("plugin name must match skill name")
    validate_marketplace(marketplace, manifest["name"])


def validate_manifest(manifest: dict, path: Path) -> None:
    allowed = {
        "id", "name", "version", "description", "skills", "apps", "mcpServers",
        "interface", "author", "homepage", "repository", "license", "keywords",
    }
    unknown = set(manifest) - allowed
    if unknown:
        raise ValidationError(f"{path}: unsupported fields {sorted(unknown)}")
    required = {"name", "version", "description", "author", "skills", "interface"}
    missing = required - manifest.keys()
    if missing:
        raise ValidationError(f"{path}: missing fields {sorted(missing)}")
    if not NAME_RE.fullmatch(manifest["name"]):
        raise ValidationError(f"{path}: invalid plugin name")
    if not SEMVER_RE.fullmatch(manifest["version"]):
        raise ValidationError(f"{path}: invalid semantic version")
    if not manifest["skills"].startswith("./"):
        raise ValidationError(f"{path}: skills path must start with ./")
    if "hooks" in manifest or "mcpServers" in manifest or "apps" in manifest:
        raise ValidationError(f"{path}: undeclared runtime surface present")
    author = manifest["author"]
    if not isinstance(author, dict) or not author.get("name"):
        raise ValidationError(f"{path}: author.name is required")
    if author.get("url") and not author["url"].startswith("https://"):
        raise ValidationError(f"{path}: author.url must use https")

    interface = manifest["interface"]
    required_interface = {
        "displayName", "shortDescription", "longDescription", "developerName",
        "category", "capabilities", "defaultPrompt",
    }
    missing_interface = required_interface - interface.keys()
    if missing_interface:
        raise ValidationError(f"{path}: missing interface fields {sorted(missing_interface)}")
    if not isinstance(interface["capabilities"], list) or not all(
        isinstance(value, str) and value.strip() for value in interface["capabilities"]
    ):
        raise ValidationError(f"{path}: capabilities must be non-empty strings")
    if interface.get("websiteURL") and not interface["websiteURL"].startswith("https://"):
        raise ValidationError(f"{path}: websiteURL must use https")
    if interface.get("brandColor") and not HEX_COLOR_RE.fullmatch(interface["brandColor"]):
        raise ValidationError(f"{path}: brandColor must use #RRGGBB")
    prompts = interface.get("defaultPrompt", [])
    if len(prompts) > 3 or any(len(prompt) > 128 for prompt in prompts):
        raise ValidationError(f"{path}: defaultPrompt exceeds UI limits")


def validate_marketplace(marketplace: dict, plugin_name: str) -> None:
    entries = [item for item in marketplace.get("plugins", []) if item.get("name") == plugin_name]
    if len(entries) != 1:
        raise ValidationError("marketplace must contain exactly one matching plugin")
    entry = entries[0]
    path = entry.get("source", {}).get("path", "")
    if not path.startswith("./") or ".." in Path(path).parts:
        raise ValidationError("marketplace source.path must be a contained ./ relative path")
    policy = entry.get("policy", {})
    if not {"installation", "authentication"} <= policy.keys() or "category" not in entry:
        raise ValidationError("marketplace entry is missing policy/category")
    if policy["installation"] not in {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}:
        raise ValidationError("marketplace installation policy is invalid")
    if policy["authentication"] not in {"ON_INSTALL", "ON_USE"}:
        raise ValidationError("marketplace authentication policy is invalid")


def validate_plugin(plugin_root: Path) -> None:
    manifest_path = plugin_root / ".codex-plugin/plugin.json"
    manifest = json.loads(manifest_path.read_text())
    validate_manifest(manifest, manifest_path)
    skill_root = plugin_root / "skills" / manifest["name"]
    read_frontmatter(skill_root / "SKILL.md")
    validate_markdown_tree(skill_root)
    allowed = {".codex-plugin", "skills", "LICENSE"}
    extras = {path.name for path in plugin_root.iterdir()} - allowed
    if extras:
        raise ValidationError(f"plugin contains unexpected top-level files: {sorted(extras)}")


def validate_marketplace_root(root: Path) -> None:
    marketplace = json.loads((root / "marketplace.json").read_text())
    entries = marketplace.get("plugins", [])
    if not entries:
        raise ValidationError(f"{root}: marketplace contains no plugins")
    for entry in entries:
        source = entry.get("source", {})
        if source.get("source") != "local":
            continue
        raw_path = source.get("path", "")
        plugin_root = (root / raw_path).resolve()
        if not plugin_root.is_relative_to(root.resolve()):
            raise ValidationError(f"{root}: marketplace path escapes root")
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
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
