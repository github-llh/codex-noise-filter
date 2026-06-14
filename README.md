# codex-noise-filter

编程任务专用的 Codex skill，用于减少无效上下文、强制调用链确认，并把全局工程规则沉淀到 skill 内，避免切换会话或窗口时遗漏规则。

## 中文说明

### 适用场景

- 编写、修改、调试、排查、重构、迁移、解释代码。
- 多文件排查、跨模块调用链分析、后端构建、前端页面修复、小程序原生/uni-app/Taro 治理、Python 脚本/服务/包/测试治理。
- 用户要求减少 token、压缩噪音、简洁可追溯或可复盘。

### 结构

```text
SKILL.md
references/
  00-index.md
  01-global-engineering-rules.md
  02-noise-filter-workflow.md
  03-maven-backend-build.md
  04-frontend-rules.md
  05-delivery-templates.md
  06-environment-discovery.md
  07-java-backend-architecture.md
  08-java-style-patterns.md
  09-concurrency-async-batch.md
  10-python-development.md
  11-frontend-vue-react.md
  12-miniprogram-development.md
```

`SKILL.md` 只保留触发、路由和硬约束；执行细则按索引进入对应文件，减少主文件负担。

### 效率策略

- 单个 reference 尽量保持入口化和主题化，避免一个文件堆到数百行。
- `01-global-engineering-rules.md` 只保留全局共用规则。
- Java 后端架构规则集中到 `07-java-backend-architecture.md`，只有涉及分层、归属地、注释、调用链时才读取。
- Java 代码风格规则集中到 `08-java-style-patterns.md`，只有涉及枚举、参数校验、Lombok、Optional、函数式、去重复时才读取。
- 并发、异步和批量规则集中到 `09-concurrency-async-batch.md`，只有涉及高并发、幂等、死锁、事件、中间件、线程池、虚拟线程、用户上下文传播时才读取。
- Python 规则集中到 `10-python-development.md`，只有涉及 `.py`、Python 语法、虚拟环境、依赖、运行、测试、lint、类型检查或 Python 性能时才读取。
- Vue/React 规则集中到 `11-frontend-vue-react.md`，只有涉及 Vue2/Vue3、React、Vite、组件语法、包管理、运行、测试、lint、类型检查或前端构建时才读取。
- 小程序规则集中到 `12-miniprogram-development.md`，只有涉及原生微信小程序、uni-app、Taro、分包、模拟器、`project.config.json`、`app.json`、`pages.json`、`app.config.*`、构建、发布或测试时才读取。
- Maven 构建只读 `03-maven-backend-build.md`；环境路径发现只读 `06-environment-discovery.md`。
- 索引路由用“关键词 + 任务意图 + 影响面”交叉确认，减少误读，同时避免把所有规则一次性读入。
- `SKILL.md` 硬约束视为常驻规则；优化索引性能时只减少无关 reference 读取，不减少必须执行的约束。
- 常见任务先按快速决策表读取最小组合，例如 Java Controller/Service 改动默认 `02 + 07`，命中枚举、校验、Lombok、Optional、重复逻辑时再追加 `08`。
- Python 任务默认读取 `02 + 10`，环境路径未知才追加 `06`，跨系统或前后端调用链明确时再追加对应 reference。
- 普通布局/状态契约任务默认读取 `02 + 04`；Vue/React 任务默认读取 `02 + 11`，环境路径未知才追加 `06`。
- 小程序任务默认读取 `02 + 12`；uni-app/Taro 命中 Vue/React 语法时追加 `11`，通用布局状态追加 `04`，开发者工具路径未知才追加 `06`。
- 执行中触碰范围扩大时，按索引追加 reference；不得为了少读文件而跳过不可绕过门禁、既有代码局部对齐、分层、注释、事务、并发和业务抽象规则。

### 内置重点

- 默认简体中文回复。
- JetBrains 项目优先使用 JetBrains MCP / IDE 工具。
- 修改前确认目标文件、根因、最小方案和不影响范围。
- 修改前必须完成调用链和影响面确认。
- 无论新增、修改、Plan、Global/Goal、自动续跑、上下文恢复、跨窗口、局部补丁还是后续修复，只要属于编程任务，都必须执行 skill 索引、触碰范围确认、调用链确认和局部规则对齐。
- Plan/计划阶段也必须走 skill 索引，计划里要列出适用 reference、触碰范围、局部对齐项和验收检查。
- Global/Goal/目标追踪模式也必须走 skill 索引，每轮恢复目标、适用 reference、触碰范围、局部对齐项、验收检查和 Context Capsule。
- 规则同时适用于新增代码和已有代码修改；凡本次触碰的方法、类、DTO、SQL、测试和调用链，都要做局部规则对齐。
- Maven 后端项目优先读取 `.codex/local-environment.json`、IDE/项目配置和已验证本机候选路径。
- 当前已验证 Maven 候选为 `/Users/lilinhan/dev/maven-3.9.10/bin/mvn`，本地仓库候选为 `/Users/lilinhan/maven-git`。
- 多模块 Maven 项目默认从聚合 root 节点执行，并使用 `-pl <module> -am`。
- Python 项目先确认 `requires-python`、`.python-version`、IDE 解释器、`.venv` 或锁文件；优先复用 uv、poetry、pipenv、venv、tox、nox 等项目已有工具链，不直接使用全局 pip 乱装依赖。
- Python 代码遵守项目已有 `pyproject.toml`、Ruff/Black/isort/mypy/pyright/pytest 配置；公共函数、复杂返回值、跨模块 DTO/配置对象补类型标注和必要 docstring。
- Python 运行优先使用项目命令、`python -m ...`、`uv run ...`、`poetry run ...`；测试优先定向运行 `python -m pytest path::test` 或项目已有 `tox/nox` 命令。
- Python 修改要做最小验证：语法/导入、定向测试、lint/format/type check 中与触碰范围相关的项；无法验证时说明原因。
- 前端项目先确认 `package.json`、lockfile、`packageManager`、Node 版本和构建工具；不要混用 npm/yarn/pnpm/bun。
- Vue 项目必须先区分 Vue 2 与 Vue 3：Vue 2 默认 Options API 和 Vue Test Utils v1，Vue 3 可用 Composition API、`<script setup>`、Pinia 和 Vue Test Utils v2。
- React 项目先确认 React/React DOM 版本、框架和 TypeScript/JSX 配置；Hooks 只能在组件或自定义 Hook 顶层调用，副作用放 `useEffect`，纯派生值不额外存 state。
- Vue/React 新建组件前必须确认归属、复用价值、公开契约和测试/示例入口；组件使用优先复用项目已有组件，props/slots/children/API 边界要小而稳定。
- 小程序项目必须先识别原生、uni-app、Taro 或其他跨平台框架；不同构建方式走不同语法约束，uni-app/Taro 复用对应 Vue/React 规则，原生小程序走 `Page`、`Component`、`wxml`、`wxss`、`setData` 和官方 API 约束。
- 小程序运行优先使用官方开发者工具模拟器或项目已有 CLI/CI；先生成目标平台工程，再打开正确输出目录，不把 `dist/`、`unpackage/dist/` 当源码长期维护。
- 小程序分包要在主包接近平台限制、首屏变慢、重功能局部使用、多业务域天然独立或依赖只在局部使用时主动评估；平台包体积限制以官方文档、开发者工具和 CI 当前校验为准，不凭旧经验写死。
- 小程序 npm、插件、分包、独立分包、预下载、权限、登录、支付、订阅消息、web-view 等能力必须按目标平台官方限制处理，并保留密钥、appid、上传凭证和白名单安全边界。
- 小程序测试优先复用项目已有 `miniprogram-simulate`、`miniprogram-ci`、HBuilderX/uni-app 自动化测试、Taro/Jest/Vitest/Testing Library 或官方模拟器验证；高风险能力说明是否需要真机验证。
- 注释原则跨技术栈保持一致：注释放在对应技术栈最自然的契约位置，例如 Java Service 接口、Python docstring、Vue props/emits/slots 附近、React 组件/Hook/type 附近、SQL/配置定义处。
- Vue/React 修改优先运行项目已有 `lint`、`typecheck`、`test`、`build` 或定向测试；涉及交互和布局时用浏览器验证关键页面。
- 新建文件前必须确认 module、层级职责、包路径、同类文件位置和依赖方向，尤其注意接口、实现、实体、契约可能分属不同 module。
- 明确固定集合的状态、类型、来源、动作、阶段、结果等值优先写成业务 Enum，避免魔法字符串和数字散落。
- URL、密钥、开关、阈值、时间窗、线程池、缓存 TTL、外部系统参数等环境或运维可变值优先写入 yml/properties 或配置中心，并通过配置类注入。
- 简单入参校验优先写在 DTO/Request 的 Bean Validation 注解上，Controller 只触发校验并走统一异常处理。
- 多状态、多类型、多来源、多外部系统、重复流程、重复组装、重复字段映射或稳定扩展点必须评估业务抽象，优先沉淀到 Service 方法、领域组件、策略、枚举行为、Assembler/Converter、配置属性或项目已有扩展点。
- 避免字段不同但逻辑相同的一长串 `if`、`set`、转换或默认值代码，优先复用项目已有映射、校验、枚举策略、条件更新和 helper 能力。
- 判空逻辑可在 Java 版本和项目风格支持时使用 `Optional`、Stream、方法引用等函数式写法，但不要滥用于 DTO/Entity 字段或简单场景。
- 项目已使用 Lombok 时，不手写无意义 getter/setter；DTO/VO/Entity 按项目同类文件风格使用 Lombok，实体已有 `@Data` 范式时直接复用。
- Java 后端 Controller 保持轻薄，不写业务代码；返回数据补全、列表加工、URL/名称/状态填充、数据库/缓存/远程读取、状态流转和复杂条件必须下沉到 Service 实现、Assembler 或项目已有业务组件。
- Service 接口类和所有对外方法必须有契约注释；修改已有接口时，本次触碰的方法也要同步补齐，不等待用户提醒。
- 新增或修改返回实体、数据库实体、DTO/VO 时，类职责和关键字段注释必须同步补齐，尤其是状态、类型、来源、单位、外部映射、兼容字段和权限/脱敏含义。
- 事务默认放在 Service 实现层业务入口；需要精确控制提交/回滚、分段提交或部分失败保留时，优先复用项目事务管理器或 `TransactionTemplate` 函数式写法。
- 高并发默认考虑幂等、锁顺序、死锁规避、异步最终一致、批量分批和用户/租户/审计上下文传播。
- Service 接口和重要实现方法要有原因型注释，做到不冗余、不缺失、不杂乱。
- 前端优先修布局、组件属性和状态契约，不用硬编码掩盖后端问题。
- 编程任务规则已内化到 skill；全局 `/Users/lilinhan/.codex/AGENTS.md` 仍建议保留为兜底。
- 长任务、切换窗口或上下文压缩前，使用 Context Capsule 保留目标、证据、已改、回滚和下一步。

### Maven 示例

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am test
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -DskipTests package
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
```

### 环境发现

- 首次使用 Maven、JDK、Node、Python 或包管理器时，先读 IDE/项目配置。
- 如果配置中拿不到路径，再查找本机常见候选路径。
- 找到后必须执行最小验证，例如 `mvn -version`。
- 验证通过后写入 `.codex/local-environment.json`，后续优先复用缓存。
- 缓存失效或项目配置显式变化时，重新发现并更新缓存。

### Codex 上下文管理

- 主文件只负责触发和路由，细则通过 `references/00-index.md` 渐进读取。
- 长任务按“任务胶囊 -> 调用链确认 -> 最小修改 -> 轻量验证 -> Context Capsule”执行。
- 修改已有代码时，执行“触碰范围局部对齐”：不全量重构，但不能只让新增代码遵守规则。
- Global/Goal 模式每轮推进前恢复 Context Capsule，不能用“追求目标”绕过索引、调用链和局部对齐。
- 切换窗口或上下文压缩前输出 Context Capsule，避免丢失目标、证据、回滚点和下一步。
- 用户中途插入新目标时，先判断与主任务关系，不默认重置已有调用链。
- 全局 `AGENTS.md` 不需要承载全部细则，但建议保留为兜底入口。
- 长期 memory 只记录稳定偏好和跨任务规则；临时日志、一次性失败和未验证猜测不写入长期记忆。

英文说明见 [README.en.md](README.en.md)。
