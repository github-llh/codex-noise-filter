#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# 保留旧 Codex 单包入口，路径校验与构建统一由跨平台实现负责。
exec python3 "$ROOT_DIR/scripts/build-distributions.py" --target codex --output "${1:-"$ROOT_DIR/dist/marketplace"}"
