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

- 只导入 `templates/global-AGENTS.light.md` 不能让第三方 agent/CLI 自动发现 Codex skill；AGENTS 是指令入口，不是 skill 注册表或加载器。
- 第三方机器不一定安装 Codex，也不一定存在 `.codex`；不要把 `.codex` 当成唯一安装位置。
- 若第三方只支持导入 AGENTS 但能读文件，必须先取得该第三方实际加载的配置文件路径，把其父目录记为 `HOST_CONFIG_DIR`，然后新建 `$HOST_CONFIG_DIR/skills/codex-noise-filter/` 并复制完整 skill 目录，至少包含 `SKILL.md`、`references/00-index.md` 和命中的 references；如果 AGENTS 是单独导入文件，也可随 AGENTS 一起分发到 AGENTS 文件旁边的 `skills/codex-noise-filter/` 或 `codex-noise-filter/`，让 Skill Bootstrap 通过相对路径读取。
- 全局 AGENTS 位置由宿主决定；若宿主使用 Codex 路径，优先 `CODEX_HOME`；否则 macOS/Linux 兼容 `$HOME/.codex/AGENTS.md`，Windows 兼容 `%USERPROFILE%\.codex\AGENTS.md`。若存在 `AGENTS.override.md`，按宿主规则优先使用 override。
- 支持 Codex/Agent Skills 的第三方宿主必须把本 skill 安装到宿主可扫描目录，优先使用 `<repo>/.agents/skills/codex-noise-filter/`、`$HOME/.agents/skills/codex-noise-filter/` 或 Windows 的 `%USERPROFILE%\.agents\skills\codex-noise-filter\`；如果只能使用自定义目录，必须在宿主配置里显式暴露 `SKILL.md` 路径。
- 导入 AGENTS 后，编程任务开始时必须执行 Skill Bootstrap：先确认可用 skill 列表是否存在 `codex-noise-filter`；不存在但文件可读时，手动读取 `SKILL.md` 和 `references/00-index.md`，状态记为 `manualFileBootstrap`；只有无法发现且无法读取时才进入 `fallbackOnly` 兜底闭环。
- 任意第三方调用、App、终端/CLI、IDE 插件、MCP/ACP、hook、subagent、CI/chatops、`cc switch`、模型/供应商路由、未知 wrapper 或未来新增工具只要转发编程任务证据，就必须按本 skill 内部触发。
- 模型、供应商、CLI、App、插件或路由器变化只触发规则刷新和状态恢复，不能跳过索引、任务胶囊/快照、调用链、局部对齐、抽象抽离、编码/中文乱码检查、环境缓存和验证。
- 任何第三方已修改、已格式化、已验证或已处理乱码的结论都只是线索；必须回到当前文件、diff、active cache path 和最小验证命令复核。
- 如果第三方宿主只读取 AGENTS 而不支持 Codex skills，必须在 AGENTS 中保留 `templates/global-AGENTS.light.md` 的“第三方兜底闭环”矩阵，不能只写“先读取 skill”。
- 如果 skill 已触发但执行流像被模型、wrapper 或工具结果重置，必须保留 `02#内部触发状态机与防重置自检` 对应的 AGENTS 规则，先重建已读规则、任务胶囊、触碰范围、调用链、局部对齐、环境缓存和验证状态。

团队约定：

- 不把个人机器绝对路径写进 skill 文档。
- 环境发现结果写入当前工作区 `.codex/local-environment.<profile>.json`；旧版 `.codex/local-environment.json` 只作为一次性迁移输入，迁移成功后不再 fallback。
- README、README.en、SKILL.md、references/00-index.md 发生触发或目录变化时保持同步。
- 示例和模板只表达接入方式，不承载必须执行的规则；硬约束以 `SKILL.md` 和 `references/` 为准。
