#!/usr/bin/env bash
# 构建 harness bundle 并推送为 GitHub 仓库的 harness 分支（分支根即 bundle）。
# 使用临时索引构造提交，不触碰 master 的索引与工作区；dist 是构建产物区。
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BRANCH="harness"
OUTPUT="dist/harness-release"
VERSION="$(python3 -c 'import json;print(json.load(open("distribution/plugin/.codex-plugin/plugin.json"))["version"])')"

if [[ -n "$(git status --porcelain -- "$OUTPUT")" ]]; then
    echo "错误: $OUTPUT 已被跟踪或存在用户改动，发布前请先处理" >&2
    exit 1
fi
rm -rf "$ROOT_DIR/$OUTPUT"

python3 scripts/build-distributions.py --target harness --output "$OUTPUT"

# 只把 bundle 目录写入临时索引；-f 绕过 .gitignore，绝不影响主索引。
INDEX_FILE="$ROOT_DIR/.git/publish-harness-index"
rm -f "$INDEX_FILE"
export GIT_INDEX_FILE="$INDEX_FILE"
git read-tree --empty
git add -f "$OUTPUT/codex-noise-filter"
TREE="$(git write-tree)"
COMMIT="$(git commit-tree "$TREE" -p master -m "release: dsh-codex-noise-filter ${VERSION} Harness bundle")"
unset GIT_INDEX_FILE

echo "bundle commit: $COMMIT"
echo "推送 $BRANCH 分支（失败时可稍后手动执行）:"
echo "  git push origin $COMMIT:refs/heads/$BRANCH"
git push origin "$COMMIT:refs/heads/$BRANCH"
