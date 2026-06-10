---
name: codex-noise-filter
description: |
  专用于编程相关、写代码/读代码/改代码场景。
  识别到编程任务时自动启用：先读规则、先收敛上下文、先确认调用链，再改代码。
  默认压缩噪音与冗余输出，并内置用户全局 AGENTS 规则，避免切换会话或窗口后规则丢失。
---

# codex-noise-filter

这是编程任务的默认执行入口。目标是在不牺牲质量的前提下减少无效上下文、避免重复扫描，并把修改控制在最小、安全、可回滚范围内。

## 触发条件

任一条件成立即启用：

- 用户意图是编写、修改、调试、排查、重构、迁移、解释代码。
- 任务涉及路径、文件名、类名、方法名、错误日志、调用链、构建、测试、前后端代码规范。
- 用户要求减少 token、压缩噪音、简洁可追溯、可复盘。
- 用户明确点名 `codex-noise-filter`。

不触发：纯生活对话、一般知识问答、无代码上下文的空泛“看下/查下”。模糊请求若无路径、片段、错误或工程上下文，先问一个简短澄清问题。

## 必读入口

先读 `references/00-index.md`，再按任务类型只打开对应文件。不要把所有 references 一次性读完。

最常用路由：

- 通用工程规则、语言、工具、修改前后约束：`references/01-global-engineering-rules.md`
- 上下文预算、调用链确认、失败回退：`references/02-noise-filter-workflow.md`
- Maven、本地仓库、后端多模块构建：`references/03-maven-backend-build.md`
- 前端代码规范、布局、状态、验证：`references/04-frontend-rules.md`
- 输出格式、交付清单、上下文胶囊：`references/05-delivery-templates.md`
- IDE、Maven、Node 等本机环境发现与缓存：`references/06-environment-discovery.md`
- Java 后端架构、归属地、分层和注释：`references/07-java-backend-architecture.md`
- Java 代码风格、枚举、校验、Lombok、Optional、去重复：`references/08-java-style-patterns.md`

## 硬约束

- 默认使用简体中文回复；代码、命令、配置项、文件名、类名、方法名、日志和异常保持原文。
- 修改前必须确认目标文件、问题根因、最小修改方案，以及不应影响的模块、接口、数据结构、权限和业务逻辑。
- 涉及代码修改前必须先确认调用链与影响面；未闭环时只能继续诊断，不直接改。
- 对 JetBrains 项目，优先使用 JetBrains MCP / IDE 工具读取、定位、修改和诊断；只有明确不可用、超时或错误时才使用 Shell。
- 不修改无关文件，不随意重构，不新增依赖，不改 API、DTO、数据库字段、权限、路由、配置键和公共契约，除非用户明确批准。
- 后端 Maven 多模块项目默认从聚合 root 节点构建；Maven 可执行文件和本地仓库先按环境发现规则读取缓存或 IDE 配置，未命中时再查找本机候选路径。
- 全局 `/Users/lilinhan/.codex/AGENTS.md` 建议保留为兜底；本 skill 已内化其规则，编程任务优先按 skill 索引执行。

## 执行节奏

1. 维护原始任务清单。
2. 按索引读取最小规则集。
3. 收敛候选文件和调用链。
4. 修改前再次引用任务编号确认目标。
5. 只做最小闭环改动。
6. 执行最轻量验证。
7. 用中文说明变更内容、影响范围和验证结果。
