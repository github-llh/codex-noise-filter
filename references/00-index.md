# 规则索引

只读取当前任务需要的文件，避免主文件和上下文膨胀。

## 路由原则

`SKILL.md` 的硬约束视为常驻规则，不因索引性能优化而丢失；`00-index.md` 只负责把任务导向最小 reference 集，不重复展开全部细则。

读取顺序按三段执行：

1. 先判定运行门禁：涉及读取、修改、构建、测试、重构、Plan、Global/Goal、自动续跑、上下文恢复时，读 `02-noise-filter-workflow.md` 对应章节。
2. 再判定业务域：Java 后端读 `07`，Java 风格读 `08`，Python 读 `10`，Vue/React 读 `11`，通用前端读 `04`，并发/异步/批量读 `09`，构建读 `03`，环境发现读 `06`。
3. 最后按需补充：只在需要交付模板、Context Capsule、语言/工具细则、高风险说明时读 `05` 或 `01`。

性能优先级：

- 默认打开 `00-index.md` + 1 个主 reference。
- Java 后端修改通常打开 `02` + `07`，只有命中枚举、校验、Lombok、Optional、重复逻辑时再加 `08`。
- Python 修改通常打开 `02` + `10`，只有命中环境路径发现时再加 `06`，命中跨服务/后端调用链时再加对应 reference。
- 涉及事务、高并发、幂等、异步、批量时，在 `07` 基础上加 `09`。
- 涉及 Maven 构建但不改代码时，优先 `03`，需要路径发现时才加 `06`。
- 涉及通用前端布局/表单/状态契约时优先 `04`；涉及 Vue/React/Vite/测试/构建时优先 `11`，接口契约或后端联动明确时再加后端 reference。
- 不为了“保险”一次性读取所有 reference；如果执行中发现触碰范围扩大，再按关键词追加读取。

约束保真：

- 性能优化不能跳过 `SKILL.md` 硬约束、`02` 的不可绕过门禁、既有代码局部对齐、Controller 分层、Service 注释、实体 Lombok、业务抽象、事务与并发要求。
- 若一个任务同时命中性能限制和硬约束，硬约束优先，宁可多打开一个 reference，也不能漏掉触碰范围必须执行的规则。
- 新增、修改、续跑、Plan、Global/Goal、跨窗口恢复都使用同一套路由；不得因任务入口不同而降低规则集。

## 任务到文件映射

- 不可绕过执行门禁：`02-noise-filter-workflow.md#不可绕过执行门禁`
- 语言与标题规范：`01-global-engineering-rules.md#语言偏好`
- JetBrains 项目工具优先级：`01-global-engineering-rules.md#工具优先级`
- 修改前检查：`01-global-engineering-rules.md#修改前确认`
- 高风险变更：`01-global-engineering-rules.md#高风险变更`
- AGENTS 演进建议：`01-global-engineering-rules.md#项目演进规则`
- Plan 阶段门禁：`02-noise-filter-workflow.md#plan-阶段门禁`
- Global/Goal 模式门禁：`02-noise-filter-workflow.md#globalgoal-模式门禁`
- Java 后端分层：`07-java-backend-architecture.md#后端分层`
- Controller 业务逻辑迁出：`07-java-backend-architecture.md#后端分层`
- 业务抽象与扩展性：`07-java-backend-architecture.md#业务抽象与扩展性`
- 事务管理：`07-java-backend-architecture.md#事务管理`
- 新建文件归属地：`07-java-backend-architecture.md#新建文件归属地`
- 注释规范：`07-java-backend-architecture.md#注释规则`
- 高并发可用性：`09-concurrency-async-batch.md#高并发可用性`
- 幂等性：`09-concurrency-async-batch.md#幂等性`
- 死锁规避：`09-concurrency-async-batch.md#死锁规避`
- 异步事件与中间件：`09-concurrency-async-batch.md#异步事件与中间件`
- 批量操作与并发执行：`09-concurrency-async-batch.md#批量操作与并发执行`
- 用户上下文传播：`09-concurrency-async-batch.md#用户上下文传播`
- Python 开发规则：`10-python-development.md`
- Python 版本与语法：`10-python-development.md#版本与语法`
- Python 环境与依赖：`10-python-development.md#环境与依赖`
- Python 运行与命令：`10-python-development.md#运行与命令`
- Python 测试与验证：`10-python-development.md#测试与验证`
- Python lint/format/type check：`10-python-development.md#lint格式化与类型检查`
- Python 性能与健壮性：`10-python-development.md#性能与健壮性`
- Vue/React 开发规则：`11-frontend-vue-react.md`
- Vue 2 规则：`11-frontend-vue-react.md#vue-2-规则`
- Vue 3 规则：`11-frontend-vue-react.md#vue-3-规则`
- React 规则：`11-frontend-vue-react.md#react-规则`
- 前端环境与依赖：`11-frontend-vue-react.md#环境与依赖`
- 前端运行与构建：`11-frontend-vue-react.md#运行与构建`
- 前端测试与验证：`11-frontend-vue-react.md#测试与验证`
- 前端 lint/format/type check：`11-frontend-vue-react.md#lint格式化与类型检查`
- 枚举与常量：`08-java-style-patterns.md#枚举与常量`
- 配置外置化：`08-java-style-patterns.md#配置外置化`
- DTO 参数校验：`08-java-style-patterns.md#参数校验分层`
- 去硬编码与重复逻辑：`08-java-style-patterns.md#去硬编码与重复逻辑`
- 判空与函数式风格：`08-java-style-patterns.md#判空与函数式风格`
- Lombok 使用标准：`08-java-style-patterns.md#lombok-使用标准`
- token 预算与读取窗口：`02-noise-filter-workflow.md#上下文预算`
- 调用链闭环：`02-noise-filter-workflow.md#调用链确认`
- 既有代码修改一致性：`02-noise-filter-workflow.md#既有代码修改一致性`
- 失败回退：`02-noise-filter-workflow.md#失败处理`
- Maven 发行版与本地仓库：`03-maven-backend-build.md#本地-maven-环境`
- Maven/IDE 配置智能发现：`06-environment-discovery.md#发现顺序`
- 环境缓存：`06-environment-discovery.md#缓存策略`
- 多模块构建 root 节点：`03-maven-backend-build.md#多层-maven-结构构建`
- 后端验证命令：`03-maven-backend-build.md#后端构建与验证`
- 前端布局与组件：`04-frontend-rules.md#布局与组件`
- 前端状态与契约：`04-frontend-rules.md#状态契约与安全`
- 前端验证：`04-frontend-rules.md#前端验证`
- 交付格式：`05-delivery-templates.md#最终回复结构`
- Context Capsule：`05-delivery-templates.md#上下文胶囊`
- Codex 会话上下文管理：`05-delivery-templates.md#codex-上下文管理`
- Codex 记忆管理：`05-delivery-templates.md#codex-记忆管理`

## 快速决策表

按第一条命中的任务形态选最小组合，再用高精度路由补充：

| 任务形态 | 默认读取 | 追加条件 |
| --- | --- | --- |
| 只问规则、解释 skill、优化索引 | `00` + 目标 reference | 需要同步说明时加 README |
| Plan/Global/Goal/续跑/上下文恢复 | `02` | 涉及代码层再加对应业务 reference |
| Java Controller/Service/Entity/DTO 修改 | `02` + `07` | 枚举/校验/Lombok/Optional/重复逻辑加 `08` |
| Java 事务/并发/批量/异步 | `02` + `07` + `09` | 需要构建验证时加 `03` |
| Java 枚举/配置/校验/Lombok/重复 if-set | `02` + `08` | 涉及分层或接口注释加 `07` |
| Python 语法/脚本/服务/包/测试 | `02` + `10` | 环境路径未知加 `06`，跨系统调用再加对应 reference |
| Maven 构建/测试/多模块 root | `03` | Maven/JDK 路径未知时加 `06` |
| 环境路径发现/缓存 | `06` | 需要构建命令时加 `03` |
| 前端页面/布局/表单/状态契约 | `02` + `04` | 涉及 Vue/React 语法或构建测试加 `11` |
| Vue/React/Vite/组件测试/前端构建 | `02` + `11` | 通用布局状态加 `04`，环境路径未知加 `06` |
| 最终回复/交接/压缩上下文 | `05` | 长任务恢复时加 `02` |

最小组合不是放宽规则；它只是延迟打开无关 reference。执行中一旦触碰范围命中其他规则，立即追加对应 reference。

## 性能原则

- 主文件只负责触发和路由；细节只在需要时打开。
- 先做主题判别，再读文件；同一任务默认只打开 1 个主 reference，跨层任务最多打开 2 到 3 个。
- 路由采用“关键词 + 任务意图 + 影响面”三者交叉确认，避免只凭单个词误读。
- 修改已有代码时，先读 `02-noise-filter-workflow.md#既有代码修改一致性`，再读对应主题规则。
- 优先 `rg --files`、符号检索、局部窗口读取，不做全仓无目的扫描。
- 默认读取 200 到 300 行窗口；关键段最多 500 行。
- 工具输出只保留结论、文件路径、行号和关键片段，不搬运大段日志。

## 高精度路由

- `Plan`、`计划`、`执行计划`、`分步实现`：先读 `02-noise-filter-workflow.md#plan-阶段门禁`。
- `Global`、`Goal`、`目标追踪`、`长期推进`、`自动续跑`、`跨轮推进`：先读 `02-noise-filter-workflow.md#globalgoal-模式门禁`。
- `新增代码`、`修改已有代码`、`旧代码`、`自动续跑`、`跨窗口`、`不可绕过`、`强制执行`：先读 `02-noise-filter-workflow.md#不可绕过执行门禁`。
- `Controller`、`Service`、`接口层`、`实现层`、`I*Service`、`返回实体`、`数据库实体`、`VO`、`DTO`、`DO`、`PO`、`Entity`、`业务代码下沉`、`URL 填充`、`列表加工`、`业务抽象`、`扩展性`、`可维护`、`健壮性`、`策略`、`handler map`、`Assembler`、`Converter`、`领域组件`、`事务`、`@Transactional`、`rollbackFor`、`module 归属`、`新建文件放哪`、`注释`：读 `07-java-backend-architecture.md`。
- `Enum`、`常量`、`固定值`、`状态值`、`类型值`、`来源值`、`协议`、`默认值`、`阈值`、`时间窗`、`yml`、`properties`、`@ConfigurationProperties`、`@Value`、`配置外置`、`参数校验`、`Bean Validation`、`Lombok`、`@Data`、`getter/setter`、`Optional`、`Stream`、`重复 if/set`、`硬编码`、`函数式`：读 `08-java-style-patterns.md`。
- `Python`、`.py`、`pyproject.toml`、`requirements.txt`、`setup.py`、`tox.ini`、`noxfile.py`、`Pipfile`、`poetry.lock`、`uv.lock`、`pytest`、`unittest`、`ruff`、`black`、`isort`、`mypy`、`pyright`、`venv`、`.venv`、`typing`、`dataclass`、`asyncio`、`脚本`、`包管理`、`虚拟环境`：读 `10-python-development.md`。
- `Vue`、`Vue2`、`Vue 2`、`Vue3`、`Vue 3`、`.vue`、`SFC`、`Composition API`、`Options API`、`script setup`、`defineProps`、`defineEmits`、`Vuex`、`Pinia`、`Vue Router`、`React`、`JSX`、`TSX`、`Hooks`、`useState`、`useEffect`、`Vite`、`Vitest`、`Jest`、`Testing Library`、`Vue Test Utils`、`Cypress`、`Playwright`、`package.json`、`pnpm`、`yarn`、`npm`、`bun`：读 `11-frontend-vue-react.md`。
- `高并发`、`幂等`、`死锁`、`异步`、`MQ`、`事件`、`线程池`、`虚拟线程`、`批量`、`用户上下文`、`创建人`、`修改人`：读 `09-concurrency-async-batch.md`。
- `mvn`、`pom.xml`、`-pl`、`-am`、`多模块构建`、`测试命令`：读 `03-maven-backend-build.md`。
- `MAVEN_HOME`、`JAVA_HOME`、`Node`、`pnpm`、`IDE 配置路径`、`.codex/local-environment.json`：读 `06-environment-discovery.md`。
- `flex`、`grid`、`组件`、`页面`、`路由守卫`、`加载/空状态`：读 `04-frontend-rules.md`。
- `Context Capsule`、`最终回复`、`记忆管理`、`会话切换`：读 `05-delivery-templates.md`。
