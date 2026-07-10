#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_ROOT="${1:-"$ROOT_DIR/dist/marketplace"}"

case "$OUT_ROOT" in
  /*) ;;
  *) OUT_ROOT="$(pwd)/$OUT_ROOT" ;;
esac

if [ "$OUT_ROOT" = "/" ] || [ "$OUT_ROOT" = "$ROOT_DIR" ]; then
  echo "Refusing unsafe output root: $OUT_ROOT" >&2
  exit 2
fi

case "$OUT_ROOT/" in
  "$ROOT_DIR/dist/"*) ;;
  "$ROOT_DIR/"*)
    echo "Refusing to write build output into source directories: $OUT_ROOT" >&2
    exit 2
    ;;
esac

PLUGIN_DIR="$OUT_ROOT/plugins/codex-noise-filter"
STAGE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codex-noise-filter-plugin.XXXXXX")"
trap 'rm -rf "$STAGE_DIR"' EXIT

python3 "$ROOT_DIR/scripts/validate-project.py"

mkdir -p "$STAGE_DIR/.codex-plugin" "$STAGE_DIR/skills/codex-noise-filter"
cp "$ROOT_DIR/distribution/plugin/.codex-plugin/plugin.json" "$STAGE_DIR/.codex-plugin/plugin.json"
cp "$ROOT_DIR/LICENSE" "$STAGE_DIR/LICENSE"
cp "$ROOT_DIR/SKILL.md" "$STAGE_DIR/skills/codex-noise-filter/SKILL.md"
cp -R "$ROOT_DIR/agents" "$STAGE_DIR/skills/codex-noise-filter/agents"
cp -R "$ROOT_DIR/references" "$STAGE_DIR/skills/codex-noise-filter/references"

find "$STAGE_DIR" -name '.DS_Store' -delete
python3 "$ROOT_DIR/scripts/validate-project.py" --plugin "$STAGE_DIR"

mkdir -p "$OUT_ROOT/plugins"
rm -rf "$PLUGIN_DIR"
mv "$STAGE_DIR" "$PLUGIN_DIR"
trap - EXIT
cp "$ROOT_DIR/distribution/marketplace.json" "$OUT_ROOT/marketplace.json"
python3 "$ROOT_DIR/scripts/validate-project.py" --marketplace-root "$OUT_ROOT"

echo "Marketplace package written to: $OUT_ROOT"
