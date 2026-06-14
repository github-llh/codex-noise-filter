# 小程序场景

## 触发 Prompt

```text
$codex-noise-filter 检查这个小程序页面，先识别原生/uni-app/Taro，再确认分包、依赖边界和模拟器验证方式。
```

## 应读取

- `SKILL.md`
- `references/00-index.md`
- `references/02-noise-filter-workflow.md`
- `references/12-miniprogram-development.md`
- uni-app/Taro 命中 Vue/React 语法时追加 `references/11-frontend-vue-react.md`
- 通用布局状态命中时追加 `references/04-frontend-rules.md`
- 开发者工具路径未知时追加 `references/06-environment-discovery.md`

## 期望行为

- 先识别原生微信小程序、uni-app、Taro 或其他跨平台框架。
- 按框架选择对应语法：原生走 `Page`、`Component`、`wxml`、`wxss`、`setData`；uni-app/Taro 复用 Vue/React 规则。
- 主包接近限制、首屏变慢、重功能局部使用或业务域天然独立时评估分包。
- 运行优先使用官方开发者工具模拟器或项目已有 CLI/CI，并说明是否需要真机验证。

## 禁止行为

- 不把 `dist/` 或 `unpackage/dist/` 当长期源码维护。
- 不凭旧经验写死平台包体积限制。
- 不忽略 appid、上传凭证、白名单、登录、支付、订阅消息等平台边界。
