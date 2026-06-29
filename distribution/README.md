# Distribution

本目录保存分发相关模板，不是运行时 skill 入口。

## Skill vs Plugin

- `SKILL.md`、`references/`、`agents/openai.yaml` 是 skill 编写结构，适合仓库级或用户级直接安装。
- `.codex-plugin/plugin.json`、`skills/<name>/` 和 `marketplace.json` 是 plugin 分发结构，适合让 Codex App/CLI 通过插件目录安装。

## Build a Local Plugin Package

从仓库根目录运行：

```bash
scripts/build-plugin-package.sh
```

默认输出到：

```text
dist/codex-noise-filter-plugin/
  .codex-plugin/plugin.json
  skills/codex-noise-filter/
```

发布或放入 marketplace 时，使用 `dist/codex-noise-filter-plugin/` 作为插件根目录。

新增、删除或重命名 `references/`、`templates/`、`agents/` 或 manifest 相关文件后，先按 `references/19-installation-health-and-surface-audit.md` 检查 README、模板、构建脚本、manifest 和 marketplace 引用，再重新构建插件包。

## Repo Marketplace Example

`distribution/marketplace.json` 是 repo/team marketplace 示例。若使用它，把构建后的插件放到 marketplace 根目录的：

```text
plugins/codex-noise-filter/
```

然后让 marketplace 条目中的 `source.path` 保持：

```text
./plugins/codex-noise-filter
```

个人本机安装仍可直接使用 `$HOME/.agents/skills/codex-noise-filter/`，不强制走插件分发。
