# Java Controller / Service 场景

## Prompt

```text
$codex-noise-filter 找到这个接口 500 的根因并修复，保护现有脏改，跑目标模块验证。
```

## 路由

- `references/01-engineering-baseline.md`
- `references/02-execution-workflow.md`
- `references/03-environment-and-validation.md`
- `references/04-java-backend.md`
- 涉及事务、缓存、MQ 或批处理时追加 `references/05-concurrency-and-data.md`

## 期望

- 从 route/Controller 追到错误数据来源和必要 Service/Mapper 边界。
- 业务逻辑留在 Service，保持 API、权限和事务语义。
- 使用项目 wrapper 和目标模块命令验证，不扩改无关代码。
