# Vue / React 场景

## 触发 Prompt

```text
$codex-noise-filter 处理这个 Vue/React 组件问题，先确认框架版本、组件归属、状态契约和验证命令。
```

## 应读取

- `SKILL.md`
- `references/00-index.md`
- `references/02-noise-filter-workflow.md`
- `references/11-frontend-vue-react.md`
- 涉及通用布局、表单、状态契约时追加 `references/04-frontend-rules.md`
- 环境路径未知时追加 `references/06-environment-discovery.md` 和 `references/14-environment-cache-by-stack.md`

## 期望行为

- 先识别 Vue 2、Vue 3、React、Vite、包管理器和现有组件体系。
- 新建组件前确认归属、复用价值、公开契约、测试或示例入口。
- 使用组件时优先复用项目已有组件，保持 props、slots、children、emits/API 边界稳定。
- 注释放在 props/emits/slots、组件类型、Hook 或复杂契约附近。

## 禁止行为

- 不混用 npm/yarn/pnpm/bun。
- 不用硬编码掩盖后端契约问题。
- 不在未确认 Vue 版本时套用 Vue 3 语法到 Vue 2 项目，或反过来。
