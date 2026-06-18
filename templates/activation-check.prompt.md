# Activation Check Prompt

```text
请先判断当前任务是否触发 codex-noise-filter。

判断时不要只看是否显式写出 skill 名，也不要受调用入口影响。任务来自任意第三方调用、App、终端/CLI、IDE 插件、MCP/ACP、hook、subagent、CI/chatops、`cc switch`、模型/供应商路由、未知 wrapper 或未来新增工具时，只要载荷包含代码、路径、命令、日志、diff、截图里的错误、项目结构或工具链动作，就按本 skill 内部触发。

如果触发，请只输出：
1. 命中的 skill 名称。
2. 需要读取的最小 reference 列表。
3. 本次触碰范围。
4. 禁止触碰范围。
5. 修改前必须闭环的调用链或影响面。
6. 最小验证项。

如果不触发，请说明不触发原因，并只问一个最关键的澄清问题。
```
