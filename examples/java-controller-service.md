# Java Controller / Service 场景

## 触发 Prompt

```text
$codex-noise-filter 检查这个 Controller 是否写了业务逻辑，并把应下沉的逻辑迁到 Service 实现层。
```

## 应读取

- `SKILL.md`
- `references/00-index.md`
- `references/02-noise-filter-workflow.md`
- `references/07-java-backend-architecture.md`
- 命中枚举、校验、Lombok、Optional、重复逻辑时追加 `references/08-java-style-patterns.md`

## 期望行为

- 先确认 Controller、Service 接口、Service 实现、DTO/VO/Entity、Mapper/Repository 的调用链。
- Controller 只保留路由、权限、校验触发、Service 调用和响应转换。
- 返回数据补全、列表加工、状态流转、数据库/缓存/远程调用迁到 Service 实现、Assembler 或项目已有业务组件。
- 同步补齐 Service 接口对外方法注释、重要实现方法注释、关键实体字段注释。

## 禁止行为

- 不在 Controller 中新增业务分支、循环加工、远程调用或数据库访问。
- 不只让新增代码遵守规则，忽略本次触碰的已有方法。
- 不为了少读 reference 跳过调用链和影响面确认。
