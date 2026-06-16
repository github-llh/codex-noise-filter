# 规则索引

只读取当前任务需要的文件，避免主文件和上下文膨胀。

## 路由原则

`SKILL.md` 的硬约束视为常驻规则，不因索引性能优化而丢失；`00-index.md` 只负责把任务导向最小 reference 集，不重复展开全部细则。

读取顺序按三段执行：

1. 先判定运行门禁和意图证据：涉及读取、修改、构建、测试、重构、报错日志、异常堆栈、构建/测试失败、Plan、Global/Goal、自动续跑、上下文恢复时，读 `02-noise-filter-workflow.md` 对应章节；涉及智能扩窗或 Git 历史时读 `13-read-expansion-and-history.md`。
2. 再判定业务域：Java 后端读 `07`，Java 风格读 `08`，Python 读 `10`，Vue/React 读 `11`，小程序读 `12`，通用前端读 `04`，并发/异步/批量读 `09`，构建读 `03`，统一环境发现读 `06`，栈级环境缓存读 `14`。
3. 最后按需补充：只在需要交付模板、Context Capsule、语言/工具细则、高风险说明时读 `05` 或 `01`。

性能优先级：

- 默认打开 `00-index.md` + 1 个主 reference。
- Java 后端修改通常打开 `02` + `07`，只有命中枚举、校验、Lombok、Optional、重复逻辑时再加 `08`。
- Python 修改通常打开 `02` + `10`；需要运行、测试、lint 或 type check 前先按 `06` + `14` 验证并复用环境缓存，命中跨服务/后端调用链时再加对应 reference。
- 涉及事务、高并发、幂等、异步、批量时，在 `07` 基础上加 `09`。
- 涉及 Maven 构建但不改代码时，优先 `03`，执行前先按 `06` + `14` 验证并复用 Maven/JDK 缓存。
- 涉及通用前端布局/表单/状态契约时优先 `04`；涉及 Vue/React/Vite/测试/构建时优先 `11`，接口契约或后端联动明确时再加后端 reference。
- 涉及小程序原生、uni-app、Taro、分包、模拟器、`project.config.json`、`app.json`、`pages.json` 或 `app.config.*` 时优先 `12`；uni-app/Taro 命中 Vue/React 语法再加 `11`，运行、预览、构建或发布前校验时先按 `06` + `14` 验证并复用环境缓存。
- 不为了“保险”一次性读取所有 reference；如果执行中发现触碰范围扩大，再按任务状态、代码证据、调用链和风险信号追加读取。

约束保真：

- 性能优化不能跳过 `SKILL.md` 硬约束、`02` 的不可绕过门禁、既有代码局部对齐、Controller 分层、Service 注释、实体 Lombok、业务抽象、事务与并发要求。
- 若一个任务同时命中性能限制和硬约束，硬约束优先，宁可多打开一个 reference，也不能漏掉触碰范围必须执行的规则。
- 新增、修改、续跑、Plan、Global/Goal、跨窗口恢复都使用同一套路由；不得因任务入口不同而降低规则集。

## 任务到文件映射

- 不可绕过执行门禁：`02-noise-filter-workflow.md#不可绕过执行门禁`
- 强规则命中后的自动升级：`02-noise-filter-workflow.md#强规则命中后的自动升级`
- 读取完整性与智能扩窗：`13-read-expansion-and-history.md#读取完整性与智能扩窗`
- Git 历史对比与回归防护：`13-read-expansion-and-history.md#git-历史对比与回归防护`
- 自动意图识别：`02-noise-filter-workflow.md#自动意图识别`
- 语言与标题规范：`01-global-engineering-rules.md#语言偏好`
- JetBrains 项目工具优先级：`01-global-engineering-rules.md#工具优先级`
- 修改前检查：`01-global-engineering-rules.md#修改前确认`
- 跨技术栈注释原则：`01-global-engineering-rules.md#跨技术栈注释原则`
- 跨技术栈文件归属与依赖边界：`01-global-engineering-rules.md#跨技术栈文件归属与依赖边界`
- 跨技术栈环境与命令：`01-global-engineering-rules.md#跨技术栈环境与命令`
- 跨技术栈验证策略：`01-global-engineering-rules.md#跨技术栈验证策略`
- 跨技术栈安全与外部边界：`01-global-engineering-rules.md#跨技术栈安全与外部边界`
- 跨技术栈编码风格智能化门禁：`01-global-engineering-rules.md#跨技术栈编码风格智能化门禁`
- 跨技术栈硬编码治理：`01-global-engineering-rules.md#跨技术栈硬编码治理`
- 跨技术栈重复逻辑治理：`01-global-engineering-rules.md#跨技术栈重复逻辑治理`
- 高风险变更：`01-global-engineering-rules.md#高风险变更`
- AGENTS 演进建议：`01-global-engineering-rules.md#项目演进规则`
- Plan 阶段门禁：`02-noise-filter-workflow.md#plan-阶段门禁`
- Global/Goal 模式门禁：`02-noise-filter-workflow.md#globalgoal-模式门禁`
- Skill 规则刷新与会话恢复：`02-noise-filter-workflow.md#skill-规则刷新与会话恢复`
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
- Vue/React 组件创建规则：`11-frontend-vue-react.md#组件创建规则`
- Vue/React 组件使用规则：`11-frontend-vue-react.md#组件使用规则`
- Vue/React 组件注释位置：`11-frontend-vue-react.md#组件注释位置`
- Vue 2 规则：`11-frontend-vue-react.md#vue-2-规则`
- Vue 3 规则：`11-frontend-vue-react.md#vue-3-规则`
- React 规则：`11-frontend-vue-react.md#react-规则`
- 前端环境与依赖：`11-frontend-vue-react.md#环境与依赖`
- 前端运行与构建：`11-frontend-vue-react.md#运行与构建`
- 前端环境缓存：`14-environment-cache-by-stack.md#node前端环境缓存`
- 前端测试与验证：`11-frontend-vue-react.md#测试与验证`
- 前端 lint/format/type check：`11-frontend-vue-react.md#lint格式化与类型检查`
- 小程序开发规则：`12-miniprogram-development.md`
- 小程序项目形态识别：`12-miniprogram-development.md#项目形态识别`
- 小程序语法与框架选择：`12-miniprogram-development.md#语法与框架选择`
- 小程序文件归属与依赖边界：`12-miniprogram-development.md#文件归属与依赖边界`
- 小程序分包与包体积：`12-miniprogram-development.md#分包与包体积`
- 小程序组件、页面与注释：`12-miniprogram-development.md#组件页面与注释`
- 小程序环境与运行：`12-miniprogram-development.md#环境与运行`
- 小程序环境缓存：`14-environment-cache-by-stack.md#小程序环境缓存`
- 小程序构建与发布：`12-miniprogram-development.md#构建与发布`
- 小程序测试与验证：`12-miniprogram-development.md#测试与验证`
- Java 枚举与常量：`08-java-style-patterns.md#枚举与常量`
- 配置外置化：`08-java-style-patterns.md#配置外置化`
- DTO 参数校验：`08-java-style-patterns.md#参数校验分层`
- Java 去硬编码与重复逻辑落地：`08-java-style-patterns.md#去硬编码与重复逻辑`
- 判空与函数式风格：`08-java-style-patterns.md#判空与函数式风格`
- Lombok 使用标准：`08-java-style-patterns.md#lombok-使用标准`
- token 预算与读取窗口：`02-noise-filter-workflow.md#上下文预算`
- 调用链闭环：`02-noise-filter-workflow.md#调用链确认`
- 既有代码修改一致性：`02-noise-filter-workflow.md#既有代码修改一致性`
- 失败回退：`02-noise-filter-workflow.md#失败处理`
- Maven 发行版与本地仓库：`03-maven-backend-build.md#本地-maven-环境`
- Maven/IDE 配置智能发现：`06-environment-discovery.md#发现顺序`
- Maven/Java 环境缓存：`14-environment-cache-by-stack.md#mavenjava-环境缓存`
- Python 环境缓存：`14-environment-cache-by-stack.md#python-环境缓存`
- 自动环境缓存维护：`06-environment-discovery.md#自动环境缓存维护`
- 环境缓存结构：`06-environment-discovery.md#缓存结构`
- 环境缓存策略：`06-environment-discovery.md#缓存策略`
- 多模块构建 root 节点：`03-maven-backend-build.md#多层-maven-结构构建`
- 后端验证命令：`03-maven-backend-build.md#后端构建与验证`
- 前端布局与组件：`04-frontend-rules.md#布局与组件`
- 前端状态与契约：`04-frontend-rules.md#状态契约与安全`
- 前端验证：`04-frontend-rules.md#前端验证`
- 各技术栈默认无操作验证：`01-global-engineering-rules.md#跨技术栈验证策略`
- 交付格式：`05-delivery-templates.md#最终回复结构`
- Context Capsule：`05-delivery-templates.md#上下文胶囊`
- Codex 会话上下文管理：`05-delivery-templates.md#codex-上下文管理`
- Codex 记忆管理：`05-delivery-templates.md#codex-记忆管理`

## 快速决策表

按第一条命中的任务形态选最小组合，再用高精度路由补充：

| 任务形态 | 默认读取 | 追加条件 |
| --- | --- | --- |
| 只问规则、解释 skill、优化索引 | `00` + 目标 reference | 需要同步说明时加 README |
| 报错日志/异常堆栈/构建失败/测试失败/启动失败 | `02` | 按日志识别技术栈：Maven 加 `06` + `03`，Python 加 `06` + `10`，Vue/React/Node 加 `06` + `11`，小程序加 `06` + `12`；触碰代码再加 `01` 和对应业务 reference |
| Plan/Global/Goal/续跑/上下文恢复 | `02` | 涉及代码层再加对应业务 reference |
| Git 历史/提交记录/回归风险/历史兼容 | `13` | 按文件类型和风险追加业务 reference；需要同步任务胶囊时加 `02`，需要理解具体技术栈语义时加 `07`/`08`/`10`/`11`/`12` |
| Java Controller/Service/Entity/DTO 修改 | `02` + `07` | 枚举/校验/Lombok/Optional/重复逻辑加 `08` |
| Java 事务/并发/批量/异步 | `02` + `07` + `09` | 需要构建验证时加 `03` |
| Java 枚举/配置/校验/Lombok/重复 if-set | `02` + `01` + `08` | 只问规则可省略 `02`；涉及分层或接口注释加 `07` |
| 文件归属/目录位置/依赖边界/生成目录 | `02` + `01` | 只问规则可省略 `02`；Java 加 `07`，Python 加 `10`，Vue/React 加 `11`，小程序加 `12` |
| 环境/运行/命令/包管理器/root/workspace | `02` + `01` + `06` + `14` | 只问规则可省略 `02`；执行工具链命令前按技术栈读取配置、验证/复用缓存，再按技术栈加 `03`/`10`/`11`/`12` |
| 测试/验证/lint/typecheck/build/模拟器 | `02` + `01` + `06` + `14` | 只问规则可省略 `02`；执行工具链命令前按技术栈读取配置、验证/复用缓存，再按技术栈追加 `03`/`04`/`10`/`11`/`12` |
| 密钥/权限/租户/审计/外部调用/上传下载/动态内容 | `02` + `01` | 只问规则可省略 `02`；并发副作用加 `09`，再按技术栈追加对应 reference |
| 编码风格智能化/魔法值/常量放置/抽象边界 | `02` + `01` | Java 加 `08`，Python 加 `10`，Vue/React 加 `11`，小程序加 `12`；触碰后端分层或业务抽象再加 `07` |
| Python 语法/脚本/服务/包/测试 | `02` + `10` | 运行/测试/lint/type check 前加 `06`，跨系统调用再加对应 reference |
| Maven 构建/测试/多模块 root | `06` + `14` + `03` | 先验证/复用 Maven/JDK 缓存，再执行 Maven 命令 |
| 环境路径发现/缓存/忽略规则 | `06` | 需要栈级缓存细节时加 `14`，需要构建命令时加 `03`；涉及代码修改时加 `02` |
| 前端页面/布局/表单/状态契约 | `02` + `04` | 涉及 Vue/React 语法或构建测试加 `11` |
| Vue/React/Vite/组件测试/前端构建 | `02` + `11` | 通用布局状态加 `04`；执行构建/typecheck/lint/test 前加 `06` |
| 小程序原生/uni-app/Taro/分包/模拟器 | `02` + `12` | uni-app/Taro 语法加 `11`，通用布局状态加 `04`；执行构建/编译/CI 前加 `06`；只有当前任务目标本身包含模拟器、预览、上传、真机或发布链路，且权限边界清楚时才查开发者工具路径 |
| 最终回复/交接/压缩上下文 | `05` | 长任务恢复时加 `02` |

最小组合不是放宽规则；它只是延迟打开无关 reference。执行中一旦触碰范围命中其他规则，立即追加对应 reference。

## 性能原则

- 主文件只负责触发和路由；细节只在需要时打开。
- 先做主题判别，再读文件；同一任务默认只打开 1 个主 reference，跨层任务最多打开 2 到 3 个。
- `02` 只承载跨技术栈执行门禁、上下文预算、调用链和局部对齐流程；智能扩窗和 Git 历史细节进入 `13`，技术栈差异进入 `07`、`08`、`09`、`10`、`11`、`12`。
- `06` 只承载跨技术栈环境发现、最小验证、缓存结构和 `.codex/` 忽略规则；Maven/Java、Node/前端、Python、小程序栈级缓存细节进入 `14`，运行、构建、测试命令细节进入 `03`、`10`、`11`、`12`。
- 路由采用“任务意图 + 代码证据 + 影响面 + 风险信号”交叉确认，避免只凭单个词误读，也避免等待固定提示词才触发。
- 修改已有代码时，先读 `02-noise-filter-workflow.md#既有代码修改一致性`，再读对应主题规则。
- 优先 `rg --files`、符号检索、局部窗口读取，不做全仓无目的扫描。
- 默认读取 200 到 300 行窗口只是起点；修改代码时必须按 `13-read-expansion-and-history.md#读取完整性与智能扩窗` 和对应技术栈 reference 自动判断语义单元边界，不局限于 Java 方法/类。根据文件类型扩读 Java 类/方法/注解/字段、Python 模块/函数/类/docstring/import、Vue/React 组件与 hooks/state/template、小程序 Page/Component/wxml/wxss、SQL mapper/动态 SQL、配置块、脚本入口、测试 fixture、直接调用点和同文件相邻范式。
- 关键段最多 500 行是常规窗口，不是硬上限；若符号完整体或低风险强规则判断必须跨过该窗口，可分段读取同一文件的相邻区间，直到能证明触碰单元已闭环。
- 工具输出只保留结论、文件路径、行号和关键片段，不搬运大段日志。

## 高精度路由

- `Plan`、`计划`、`执行计划`、`分步实现`：先读 `02-noise-filter-workflow.md#plan-阶段门禁`。
- `Global`、`Goal`、`目标追踪`、`长期推进`、`自动续跑`、`跨轮推进`：先读 `02-noise-filter-workflow.md#globalgoal-模式门禁`。
- 上下文恢复、自动续跑、跨窗口继续、存在 Context Capsule、引用上一轮结论、当前工作区 skill/reference 有变更，或出现 `上个会话`、`接着问`、`刚更新 skill`、`更新了skill`、`为什么没触发`、`没触发skill`、`不符合skill约束`、`还是没执行`、`为什么没有改` 等恢复/规则失效信号：先读 `02-noise-filter-workflow.md#skill-规则刷新与会话恢复`，再按当前任务证据、触碰范围和技术栈追加对应 reference。
- `新增代码`、`修改已有代码`、`旧代码`、`自动续跑`、`跨窗口`、`不可绕过`、`强制执行`、`不可容忍`、`最小改动冲突`、`为什么没有更改`、`调用链深不深`、`涉及文件没几个`、`调用链相关文件`、`列入计划`、`任务胶囊`、`当前任务清单`、`同步修改`、`同时修改`：先读 `02-noise-filter-workflow.md#不可绕过执行门禁` 和 `02-noise-filter-workflow.md#强规则命中后的自动升级`。
- `git 历史`、`提交记录`、`历史提交`、`git log`、`git blame`、`git show`、`git diff`、`-S`、`-G`、`回归`、`改崩`、`历史兼容`、`原来为什么`、`最近谁改的`、`之前逻辑`、`旧逻辑`、`行为语义`、`演进原因`、`改动原因`、`删除旧逻辑`、`替换旧逻辑`、`最近多次变更`：先读 `13-read-expansion-and-history.md#git-历史对比与回归防护`，再按触碰文件技术栈追加对应 reference。
- `读取行数`、`行数限制`、`窗口不足`、`只读了局部`、`没读到`、`漏判`、`漏修`、`智能扩窗`、`扩读`、`完整逻辑`、`完整闭环`、`完整方法`、`完整类`、`完整组件`、`完整函数`、`完整模块`、`完整页面`、`完整 SQL`、`语义单元`、`符号完整体`、`局部规则扫描`、`未读区域`、`读到某些代码`、`自动判断`、`不等外部指定`：先读 `13-read-expansion-and-history.md#读取完整性与智能扩窗`，再按命中的技术栈追加 `07`/`08`/`10`/`11`/`12`。
- `报错`、`报错了`、`失败了`、`不行`、`还是这样`、`处理一下`、`看下这个`、`Exception`、`Caused by`、`Traceback`、`Error:`、`BUILD FAILURE`、`Failed to execute goal`、`Compilation failure`、`npm ERR`、`pnpm ERR`、`yarn error`、`pytest`、`AssertionError`、`TypeError`、`ReferenceError`、`NullPointerException`、`SQLSyntaxErrorException`、`HTTP 500`、`启动失败`、`测试失败`、`构建失败`：先读 `02-noise-filter-workflow.md#自动意图识别`，再按日志中的文件、命令、框架和工具链追加对应 reference。
- `Controller`、`Service`、`接口层`、`实现层`、`I*Service`、`返回实体`、`数据库实体`、`VO`、`DTO`、`DO`、`PO`、`Entity`、`业务代码下沉`、`URL 填充`、`列表加工`、`业务抽象`、`扩展性`、`可维护`、`健壮性`、`策略`、`handler map`、`Assembler`、`Converter`、`领域组件`、`事务`、`@Transactional`、`rollbackFor`、`module 归属`、`新建文件放哪`、`注释`：读 `07-java-backend-architecture.md`。
- `新建文件`、`文件归属`、`目录位置`、`放哪`、`module 归属`、`package`、`workspace`、`生成目录`、`构建产物`、`dist`、`build`、`target`、`unpackage/dist`、`miniprogram_npm`、`依赖方向`、`循环依赖`、`接口和实现分离`、`测试目录`：先读 `01-global-engineering-rules.md#跨技术栈文件归属与依赖边界`；Java 追加 `07`，Python 追加 `10`，Vue/React 追加 `11`，小程序追加 `12`。
- `环境`、`命令`、`运行`、`包管理器`、`lockfile`、`root`、`workspace`、`filter`、`版本`、`版本不匹配`、`构建失败后重算`、`JDK`、`Maven`、`Node`、`Python`、`虚拟环境`、`模拟器`、`开发者工具`、`CLI`、`全局安装`：先读 `01-global-engineering-rules.md#跨技术栈环境与命令`；只要准备执行工具链命令就追加 `06` 按技术栈读取配置、验证/复用缓存，并按技术栈追加 `03`/`10`/`11`/`12`。
- `测试`、`验证`、`lint`、`format`、`typecheck`、`build`、`unit test`、`e2e`、`pytest`、`mvn test`、`Vitest`、`Jest`、`Playwright`、`Cypress`、`浏览器点击`、`电脑屏幕`、`Browser`、`Computer Use`、`模拟器验证`、`真机验证`、`无法验证`：先读 `01-global-engineering-rules.md#跨技术栈验证策略`，再按技术栈追加 `03`/`04`/`10`/`11`/`12`。
- `密钥`、`token`、`secret`、`生产地址`、`appid`、`私钥`、`白名单`、`权限`、`认证`、`授权`、`租户`、`审计`、`脱敏`、`上传`、`下载`、`外部 API`、`超时`、`重试`、`动态 URL`、`富文本`、`eval`、`exec`、`反序列化`、`不可回滚副作用`：先读 `01-global-engineering-rules.md#跨技术栈安全与外部边界`；涉及异步、幂等、事务副作用追加 `09`，再按技术栈追加对应 reference。
- `编码风格智能化`、`写代码风格`、`魔法值`、`magic string`、`magic number`、`固定值`、`字面量`、`抽常量`、`常量`、`枚举`、`Enum`、`状态值`、`类型值`、`来源值`、`协议`、`模式`、`渠道`、`格式`、`默认值`、`阈值`、`时间窗`、`content-type`、`media type`、`平台编码`、`字典`：先读 `01-global-engineering-rules.md#跨技术栈编码风格智能化门禁` 和 `01-global-engineering-rules.md#跨技术栈硬编码治理`；Java 落地追加 `08`，Python 追加 `10`，Vue/React 追加 `11`，小程序追加 `12`。
- `重复 if`、`重复 set`、`重复赋值`、`重复映射`、`重复转换`、`字段不同逻辑相同`、`默认值填充`、`策略`、`handler map`、`mapper`、`converter`、`adapter`：先读 `01-global-engineering-rules.md#跨技术栈重复逻辑治理`；Java 落地追加 `08`，其他技术栈按文件类型追加对应 reference。
- `Enum`、`yml`、`properties`、`@ConfigurationProperties`、`@Value`、`Bean Validation`、`Lombok`、`@Data`、`getter/setter`、`Optional`、`Stream`、`MapStruct`、`BeanUtils`、`BiConsumer`、`Function`：Java 项目读 `08-java-style-patterns.md`。
- `Python`、`.py`、`pyproject.toml`、`requirements.txt`、`requirements-dev.txt`、`setup.py`、`tox.ini`、`noxfile.py`、`Pipfile`、`poetry.lock`、`uv.lock`、`.python-version`、`.venv/pyvenv.cfg`、`pytest`、`unittest`、`ruff`、`black`、`isort`、`mypy`、`pyright`、`venv`、`.venv`、`typing`、`dataclass`、`asyncio`、`脚本`、`包管理`、`虚拟环境`：读 `10-python-development.md`；执行命令前追加 `14-environment-cache-by-stack.md#python-环境缓存`。
- `Vue`、`Vue2`、`Vue 2`、`Vue3`、`Vue 3`、`.vue`、`SFC`、`Composition API`、`Options API`、`script setup`、`defineProps`、`defineEmits`、`props`、`emits`、`slots`、`Vuex`、`Pinia`、`Vue Router`、`React`、`JSX`、`TSX`、`Hooks`、`children`、`render prop`、`useState`、`useEffect`、`Vite`、`Vitest`、`Jest`、`Testing Library`、`Vue Test Utils`、`Cypress`、`Playwright`、`组件创建`、`组件使用`、`组件注释`、`package.json`、`pnpm`、`yarn`、`npm`、`bun`：读 `11-frontend-vue-react.md`。
- `小程序`、`微信小程序`、`weapp`、`mp-weixin`、`mini program`、`project.config.json`、`project.private.config.json`、`app.json`、`app.wxss`、`app.js`、`sitemap.json`、`wxml`、`wxss`、`wxs`、`wx:`、`setData`、`Component`、`Page`、`Behavior`、`miniprogramRoot`、`miniprogram_npm`、`subPackages`、`subpackages`、`preloadRule`、`independent`、`分包`、`主包`、`独立分包`、`分包预下载`、`分包异步化`、`模拟器`、`微信开发者工具`、`miniprogram-ci`、`miniprogram-simulate`：读 `12-miniprogram-development.md`；执行构建/编译/CI 前追加 `14-environment-cache-by-stack.md#小程序环境缓存`。
- `uni-app`、`uniapp`、`pages.json`、`manifest.json`、`App.vue`、`uni.scss`、`uni_modules`、`#ifdef MP`、`#ifdef MP-WEIXIN`、`unpackage/dist`：读 `12-miniprogram-development.md`；涉及 Vue 语法继续读 `11-frontend-vue-react.md`。
- `Taro`、`@tarojs`、`Taro.`、`app.config.js`、`app.config.ts`、`page.config.*`、`config/index.js`、`config/index.ts`、`TARO_ENV`、`dev:weapp`、`build:weapp`、`taro build --type weapp`：读 `12-miniprogram-development.md`；涉及 React/Vue 语法继续读 `11-frontend-vue-react.md`。
- `注释位置`、`注释原则`、`docstring`、`Javadoc`、`props 注释`、`slot 注释`、`hook 注释`、`配置注释`、`SQL 注释`：读 `01-global-engineering-rules.md#跨技术栈注释原则`，再按技术栈追加对应 reference。
- `高并发`、`幂等`、`死锁`、`异步`、`MQ`、`事件`、`线程池`、`虚拟线程`、`批量`、`用户上下文`、`创建人`、`修改人`：读 `09-concurrency-async-batch.md`。
- `mvn`、`pom.xml`、`.mvn/maven.config`、`.mvn/jvm.config`、`maven-wrapper.properties`、`JAVA_HOME`、`maven.compiler.release`、`java.version`、`-pl`、`-am`、`多模块构建`、`测试命令`：先读 `14-environment-cache-by-stack.md#mavenjava-环境缓存`，再读 `03-maven-backend-build.md`。
- `MAVEN_HOME`、`JAVA_HOME`、`Node`、`pnpm`、`IDE 配置路径`、`.codex/local-environment.json`、`local-environment.json`、`.codex/`、`.gitignore`、`check-ignore`、`环境缓存`、`缓存失效`、`验证路径`、`本机候选路径`、`项目配置变化`、`工具版本不匹配`：读 `06-environment-discovery.md#自动环境缓存维护`。
- `flex`、`grid`、`组件`、`页面`、`路由守卫`、`加载/空状态`：读 `04-frontend-rules.md`。
- `Context Capsule`、`最终回复`、`记忆管理`、`会话切换`：读 `05-delivery-templates.md`。
