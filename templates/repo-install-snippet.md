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

团队约定：

- 不把个人机器绝对路径写进 skill 文档。
- 环境发现结果写入当前工作区 `.codex/local-environment.json`。
- README、README.en、SKILL.md、references/00-index.md 发生触发或目录变化时保持同步。
- 示例和模板只表达接入方式，不承载必须执行的规则；硬约束以 `SKILL.md` 和 `references/` 为准。
