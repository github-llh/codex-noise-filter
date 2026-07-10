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
- `distribution/marketplace.json` 是 canonical marketplace source。
- `dist/` 是可重建产物，不直接编辑、不提交。

仓库 README、CHANGELOG、examples、templates 和维护脚本不会复制进运行时 skill，避免增加安装包上下文和重复事实。

## 验证

构建脚本会在复制前验证源码、复制后验证临时产物，并在写入 marketplace 后再次验证完整根目录。也可以独立运行：

```bash
python3 scripts/validate-project.py
python3 scripts/validate-project.py --plugin dist/marketplace/plugins/codex-noise-filter
python3 scripts/validate-project.py --marketplace-root dist/marketplace
```

本 plugin 不声明 hooks、MCP server 或 app；若未来增加，必须先有真实文件、权限说明和运行验证，再更新 manifest。
