# Changelog

本文件按真实 Git 记录维护。版本号只使用仓库已有 tag；未提交内容放入 `Unreleased`，不伪装成历史版本。

## Unreleased

- 扩展 `SKILL.md` 的 `description`，补充 Java 后端、Maven 多模块、事务并发、Python、Vue/React、小程序、Plan/Goal、上下文压缩、减少 token 和调用链确认等高频编程触发词。
- 补充中英文 README 的 `为什么用 / Why Use It`、Before/After 对比和可复制触发示例。
- 新增 `examples/` 五个典型场景：Java Controller/Service、Maven 多模块、Vue/React、Python、小程序。
- 新增 `templates/` 三个团队接入模板：轻量全局 AGENTS、仓库安装片段、触发检查 prompt。
- 新增本 `CHANGELOG.md`，并按真实 `git log` 和 tag 重新整理历史记录。
- 强化跨技术栈硬编码和重复逻辑治理，明确什么时候使用枚举、常量、配置、动态字典、mapper、converter、schema、策略或 helper，并将通用判断从 Java 专属规则抽到全局规则。
- 继续抽取各技术栈公共规则到 `01-global-engineering-rules.md`，覆盖文件归属、环境命令、验证策略和安全边界；`03`、`04`、`07`、`09`、`10`、`11`、`12` 只保留技术栈落地差异。
- 收敛 `02-noise-filter-workflow.md` 和 `06-environment-discovery.md`：`02` 只保留跨技术栈执行门禁与局部对齐流程，`06` 只保留环境发现、最小验证和缓存结构，技术栈差异下沉到对应 reference。

## 1.0.1 - 2026-06-14

Tag: `1.0.1`，commit: `0279ba8`

- `0279ba8` 补充 `codex-noise-filter` 使用说明，并同步中英文 README。
- `b7c4d79` 添加 Apache-2.0 开源协议，并在中英文 README 中说明协议边界。
- `be8c25a` 优化 README 展示风格，改为开源项目首页式顶部描述。
- `ebdde4e` 移除个人 Maven 绝对路径写法，明确先读 `.codex/local-environment.json`，未命中再发现、验证、写入缓存。
- `f55e955` 强化小程序原生、uni-app、Taro、分包、模拟器、测试与索引路由规则。

## 1.0.0 - 2026-06-14

Tag: `1.0.0`，commit: `50413f1`

### 2026-06-14

- `50413f1` 明确 React 列表 key、Vue slots、组件二次封装，以及表单、表格、弹窗、上传下载等高复用组件的状态保留要求。
- `2b9afd3` 强化 Vue/React 前端侧语法、版本识别、运行、测试、构建和索引性能策略。
- `029877d` 强化 Python 侧语法、环境、运行、测试、lint、类型检查和性能规则。

### 2026-06-12

- `98f847d` 强化索引性能，同时保留既有硬约束。
- `518a1f5` 压缩入口说明并强化索引性能，避免规则堆回 `SKILL.md`。
- `d3644fc` 明确新增、修改、Plan、Global/Goal、自动续跑、上下文恢复、跨窗口、局部补丁和后续修复都必须走索引、确认触碰范围并执行局部规则对齐。
- `3e7a088` 新增 Controller 触碰硬约束，要求迁出返回数据补全、列表加工、状态流转、跨系统取值、数据库/缓存访问等业务逻辑。

### 2026-06-10

- `29e5729` 强化配置写入 yml/properties、配置中心和配置类注入的判断规则。
- `cf0cc76` 强化 Plan 阶段门禁和 Global/Goal 模式兼容，计划必须列出适用 reference 和验收项。
- `43832a9` 新增既有代码修改一致性规则，要求触碰范围内的旧代码同步局部对齐。
- `8a9abca` 补强事务管理器、函数式事务和部分回滚规则。
- `96287a8` 强化事务、并发、幂等、异步、批量处理和索引性能，并新增并发异步批量 reference。
- `5dc2152` 完成整体索引性能优化，拆分 Java 后端架构和 Java 风格规则。
- `bef6eea` 强化 Java 判空与函数式风格规则。
- `ac2dd0e` 强化避免硬编码、重复赋值和重复判断的 Java 后端规则。

### 2026-06-09

- `a056370` 将过长 reference 拆分并强化索引命中效率。
- `edb9f3d` 强化 Lombok 使用标准。
- `d7f0a23` 强化简单校验迁移到 DTO/Request Bean Validation 的规则。
- `6da35f9` 强化稳定状态值和常量枚举化、新建文件归属地、Java 后端分层和注释约束。
- `a3a33a5` 引入更智能的 Maven 环境策略，不把 Maven 路径作为唯一硬编码规则，并新增环境发现 reference。
- `2385f7e` 将编程规则内化进 skill，建立 `SKILL.md` + `references/00-index.md` + 主题 reference 的索引结构，并补充中英文 README。
- `5952ac0` 初始化 skill 基础文件。
- `8930d84` 初始化 README。
