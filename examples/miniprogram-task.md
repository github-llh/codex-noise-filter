# 小程序场景

## Prompt

```text
$codex-noise-filter 解决 uni-app 在 HBuilderX 中的启动失败，先判断宿主插件链还是业务源码问题。
```

## 路由

- `references/02-execution-workflow.md`
- `references/03-environment-and-validation.md`
- `references/08-miniprogram.md`
- 涉及 Vue/React 语法时追加 `references/07-frontend.md`

## 期望

- 确认 HBuilderX/CLI、插件、环境变量和生成链入口。
- 不修改 `unpackage/dist` 等产物来掩盖宿主故障。
- 无法运行宿主时明确静态验证与人工验证边界。
