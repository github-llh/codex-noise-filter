# Repository Install Snippet

把 skill 放到仓库级目录，适合团队共享同一套规则：

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  references/
  examples/
  templates/
```

建议首次接入后运行一次触发检查：

```text
请说明当前任务是否触发 codex-noise-filter；如果触发，请列出将读取的 reference、触碰范围、禁止触碰范围和验证项。
```

第三方接入约定：

- 任意第三方调用、App、终端/CLI、IDE 插件、MCP/ACP、hook、subagent、CI/chatops、`cc switch`、模型/供应商路由、未知 wrapper 或未来新增工具只要转发编程任务证据，就必须按本 skill 内部触发。
- 模型、供应商、CLI、App、插件或路由器变化只触发规则刷新和状态恢复，不能跳过索引、任务胶囊/快照、调用链、局部对齐、抽象抽离、编码/中文乱码检查、环境缓存和验证。
- 任何第三方已修改、已格式化、已验证或已处理乱码的结论都只是线索；必须回到当前文件、diff、active cache path 和最小验证命令复核。

团队约定：

- 不把个人机器绝对路径写进 skill 文档。
- 环境发现结果写入当前工作区 `.codex/local-environment.<profile>.json`；旧版 `.codex/local-environment.json` 只作为一次性迁移输入，迁移成功后不再 fallback。
- README、README.en、SKILL.md、references/00-index.md 发生触发或目录变化时保持同步。
- 示例和模板只表达接入方式，不承载必须执行的规则；硬约束以 `SKILL.md` 和 `references/` 为准。
