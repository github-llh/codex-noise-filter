# Python 场景

## Prompt

```text
$codex-noise-filter 诊断这个 pytest 失败；先不要改代码，给出根因证据和最小修复建议。
```

## 路由

- `references/01-engineering-baseline.md`
- `references/02-execution-workflow.md`
- `references/03-environment-and-validation.md`
- `references/06-python.md`

## 期望

- 尊重“诊断”只读边界。
- 从 `pyproject.toml`、lockfile 和虚拟环境确认真实命令。
- 区分 fixture/断言、依赖环境和实现错误。
