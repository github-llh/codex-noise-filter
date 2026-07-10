# Activation Check Prompt

```text
请判断当前请求是否应使用 codex-noise-filter。

只有任务涉及真实代码库、代码/diff、路径、配置、报错日志、异常堆栈、构建/测试/lint/typecheck 输出、CI、skill/plugin 或 agent 配置审计时才使用。纯知识问答、没有仓库上下文的泛泛建议、翻译和文案改写不使用。

如果使用，请说明：任务模式（回答/诊断/审查/实施）、命中的 reference、预计触碰范围和验证方式。不要输出内部状态机或固定频率检查点。
```
