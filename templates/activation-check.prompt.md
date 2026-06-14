# Activation Check Prompt

```text
请先判断当前任务是否触发 codex-noise-filter。

如果触发，请只输出：
1. 命中的 skill 名称。
2. 需要读取的最小 reference 列表。
3. 本次触碰范围。
4. 禁止触碰范围。
5. 修改前必须闭环的调用链或影响面。
6. 最小验证项。

如果不触发，请说明不触发原因，并只问一个最关键的澄清问题。
```
