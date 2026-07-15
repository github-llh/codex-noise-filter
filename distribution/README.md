# Distribution

`distribution/` 保存 plugin manifest 与 marketplace 源模板，不是运行时 skill 入口。

## 构建

从仓库根运行：

```bash
scripts/build-plugin-package.sh
```

默认生成：

```text
dist/marketplace/
  .agents/plugins/marketplace.json
  plugins/codex-noise-filter/
    .codex-plugin/plugin.json
    hooks/
      hooks.json
      continuity_guard.py
    LICENSE
    skills/codex-noise-filter/
      SKILL.md
      agents/openai.yaml
      references/
```

这个输出目录本身就是 local marketplace root。Codex 从 `.agents/plugins/marketplace.json` 发现 marketplace manifest；其中的 `source.path` 仍相对于 marketplace root 解析，并与 `plugins/codex-noise-filter/` 一致。

安装并检查本机发现结果：

```bash
codex plugin marketplace add ./dist/marketplace
codex plugin add codex-noise-filter@codex-noise-filter-local
codex plugin list
```

新建 Codex 任务后使用 `/hooks` 查看并信任首次加载的非托管 Hook。只复制 Skill 源码不会注册 Plugin Hook。

Hook 状态位于插件专属 `PLUGIN_DATA/continuity/`；v3.1 状态包含有界 `event_counts`、`context_injection_count` 和最近一次上下文注入事件/类型/原因，便于证明执行而不保存 prompt、transcript、原始工具输出或工作区路径。

## 源与产物

- 根目录 `SKILL.md`、`agents/`、`references/` 是 canonical skill source。
- `distribution/plugin/.codex-plugin/plugin.json` 是 canonical plugin manifest source。
- `distribution/plugin/hooks/` 是 canonical plugin continuity Hook source。
- `distribution/marketplace.json` 是 canonical marketplace source，构建时复制到 `.agents/plugins/marketplace.json`。
- `dist/` 是可重建产物，不直接编辑、不提交。

仓库 README、CHANGELOG、examples、templates、测试和维护脚本不会复制进运行时包，避免增加安装包上下文和重复事实。

## 验证

构建脚本会在复制前验证源码、复制后验证临时产物，并在写入 marketplace 后再次验证完整根目录。也可以独立运行：

```bash
python3 scripts/validate-project.py
python3 scripts/test-continuity-guard.py
python3 scripts/validate-project.py --plugin dist/marketplace/plugins/codex-noise-filter
python3 scripts/validate-project.py --marketplace-root dist/marketplace
```

本 Plugin 只声明连续性 Hook，不声明 MCP server 或 app。Hook 仅写插件专属 `PLUGIN_DATA`，不写项目目录、全局配置或长期 memory；非托管命令 Hook 仍遵守 Codex 首次信任审查。
