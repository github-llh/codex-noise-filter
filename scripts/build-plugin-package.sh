#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="codex-noise-filter"
UNSAFE_OUTPUT_EXIT_CODE=2
OUT_ROOT="${1:-"$ROOT_DIR/dist/marketplace"}"

case "$OUT_ROOT" in
  /*) ;;
  *) OUT_ROOT="$(pwd)/$OUT_ROOT" ;;
esac

if [ "$OUT_ROOT" = "/" ] || [ "$OUT_ROOT" = "$ROOT_DIR" ]; then
  echo "拒绝使用不安全的输出根目录: $OUT_ROOT" >&2
  exit "$UNSAFE_OUTPUT_EXIT_CODE"
fi

case "$OUT_ROOT/" in
  "$ROOT_DIR/dist/"*) ;;
  "$ROOT_DIR/"*)
    echo "拒绝将构建产物写入源码目录: $OUT_ROOT" >&2
    exit "$UNSAFE_OUTPUT_EXIT_CODE"
    ;;
esac

PLUGIN_DIR="$OUT_ROOT/plugins/$PLUGIN_NAME"
STAGE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/${PLUGIN_NAME}-plugin.XXXXXX")"
trap 'rm -rf "$STAGE_DIR"' EXIT

python3 "$ROOT_DIR/scripts/validate-project.py"

mkdir -p "$STAGE_DIR/.codex-plugin" "$STAGE_DIR/skills/$PLUGIN_NAME"
cp "$ROOT_DIR/distribution/plugin/.codex-plugin/plugin.json" "$STAGE_DIR/.codex-plugin/plugin.json"
cp -R "$ROOT_DIR/distribution/plugin/hooks" "$STAGE_DIR/hooks"
cp "$ROOT_DIR/LICENSE" "$STAGE_DIR/LICENSE"
cp "$ROOT_DIR/SKILL.md" "$STAGE_DIR/skills/$PLUGIN_NAME/SKILL.md"
cp -R "$ROOT_DIR/agents" "$STAGE_DIR/skills/$PLUGIN_NAME/agents"
cp -R "$ROOT_DIR/references" "$STAGE_DIR/skills/$PLUGIN_NAME/references"

find "$STAGE_DIR" -name '.DS_Store' -delete
find "$STAGE_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$STAGE_DIR" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
python3 "$ROOT_DIR/scripts/validate-project.py" --plugin "$STAGE_DIR"

mkdir -p "$OUT_ROOT/plugins"
rm -rf "$PLUGIN_DIR"
mv "$STAGE_DIR" "$PLUGIN_DIR"
trap - EXIT
cp "$ROOT_DIR/distribution/marketplace.json" "$OUT_ROOT/marketplace.json"
python3 "$ROOT_DIR/scripts/validate-project.py" --marketplace-root "$OUT_ROOT"

echo "Marketplace 构建产物已写入: $OUT_ROOT"
