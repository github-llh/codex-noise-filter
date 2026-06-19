# Activation Check Prompt

```text
请先判断当前任务是否触发 codex-noise-filter。

判断时不要只看是否显式写出 skill 名，也不要受调用入口影响。任务来自任意第三方调用、App、终端/CLI、IDE 插件、MCP/ACP、hook、subagent、CI/chatops、`cc switch`、模型/供应商路由、未知 wrapper 或未来新增工具时，只要载荷包含代码、路径、命令、日志、diff、截图里的错误、项目结构、中文乱码、编码/charset 信号或工具链动作，就按本 skill 内部触发。平台名、agent 名和技术栈名只是示例；如果当前宿主、当前工具、cwd、文件扩展名、配置文件、命令、日志、diff、补丁、active cache path 或本机环境证据指向未列名平台/技术栈，也要按未知第三方中转处理，并动态追加本轮 reference、环境缓存和验证范围。

触发后先检查加载状态：如果当前宿主可用 skill 列表中存在 `codex-noise-filter`，标记为 `nativeSkill`；如果第三方没有 Codex 或只导入了 AGENTS 但文件可读，先取得第三方实际加载的配置文件路径，把其父目录记为 `HOST_CONFIG_DIR`，优先查找 `$HOST_CONFIG_DIR/skills/codex-noise-filter/SKILL.md` 和 `$HOST_CONFIG_DIR/codex-noise-filter/SKILL.md`，再从 AGENTS 文件所在目录查找随包分发路径，最后查项目级、用户级、`CODEX_HOME` 和兼容 `.codex` 路径；读取 `SKILL.md` 和 `references/00-index.md` 后标记为 `manualFileBootstrap`；如果既没有 skill discovery 也不能读取分发文件，标记为 `fallbackOnly`，并说明只能执行第三方兜底闭环。

如果触发，请只输出：
1. 命中的 skill 名称。
2. 加载状态：`nativeSkill` / `manualFileBootstrap` / `fallbackOnly`。
3. 实际读取或准备读取的 `SKILL.md` 路径。
4. 需要读取的最小 reference 列表。
5. 动态追加依据：当前宿主/工具、文件/配置/命令/日志/diff、active cache path 和命中的技术栈或未知技术栈处理方式。
6. 本次触碰范围。
7. 禁止触碰范围。
8. 修改前必须闭环的调用链或影响面。
9. 是否需要任务胶囊/快照、局部对齐、抽象抽离、编码/中文乱码检查、环境缓存。
10. 最小验证项。

如果不触发，请说明不触发原因，并只问一个最关键的澄清问题。
```
