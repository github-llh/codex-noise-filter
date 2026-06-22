#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-"$ROOT_DIR/dist/codex-noise-filter-plugin"}"

case "$OUT_DIR" in
  /*) ;;
  *) OUT_DIR="$(pwd)/$OUT_DIR" ;;
esac

if [ "$OUT_DIR" = "$ROOT_DIR" ] || [ "$OUT_DIR" = "/" ]; then
  echo "Refusing to write plugin package into an unsafe output directory: $OUT_DIR" >&2
  exit 2
fi

SKILL_DIR="$OUT_DIR/skills/codex-noise-filter"

rm -rf "$OUT_DIR/.codex-plugin" "$SKILL_DIR"
mkdir -p "$SKILL_DIR" "$OUT_DIR/.codex-plugin"

cp "$ROOT_DIR/distribution/plugin/.codex-plugin/plugin.json" "$OUT_DIR/.codex-plugin/plugin.json"

for path in \
  SKILL.md \
  README.md \
  README.en.md \
  CHANGELOG.md \
  LICENSE \
  CODE_OF_CONDUCT.md \
  CONTRIBUTING.md \
  SECURITY.md \
  agents \
  examples \
  references \
  templates
do
  cp -R "$ROOT_DIR/$path" "$SKILL_DIR/"
done

find "$OUT_DIR" -name ".DS_Store" -delete

echo "Plugin package written to: $OUT_DIR"
