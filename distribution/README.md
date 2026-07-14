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
  marketplace.json
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

这个输出目录本身就是 local marketplace root，`marketplace.json` 的 `source.path` 与插件位置一致。

## 源与产物

- 根目录 `SKILL.md`、`agents/`、`references/` 是 canonical skill source。
- `distribution/plugin/.codex-plugin/plugin.json` 是 canonical plugin manifest source。
- `distribution/plugin/hooks/` 是 canonical plugin continuity Hook source。
- `distribution/marketplace.json` 是 canonical marketplace source。
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
