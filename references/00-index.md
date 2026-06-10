# 规则索引

只读取当前任务需要的文件，避免主文件和上下文膨胀。

## 先读顺序

1. 所有编程任务先读 `01-global-engineering-rules.md` 的相关章节。
2. 涉及定位、修改、排查、重构时读 `02-noise-filter-workflow.md`。
3. 涉及 Java、Spring、Maven、后端构建、测试时读 `03-maven-backend-build.md`。
4. 涉及 Java 后端分层、Controller/Service、模块归属、注释、调用链时读 `07-java-backend-architecture.md`。
5. 涉及 Java 枚举、参数校验、去硬编码、重复赋值、Optional、函数式风格、Lombok 时读 `08-java-style-patterns.md`。
6. 涉及前端、页面、组件、样式、交互时读 `04-frontend-rules.md`。
7. 需要最终说明、上下文压缩、交接时读 `05-delivery-templates.md`。
8. 涉及 Maven、JDK、Node、包管理器、IDE 配置路径时读 `06-environment-discovery.md`。

## 任务到文件映射

- 语言与标题规范：`01-global-engineering-rules.md#语言偏好`
- JetBrains 项目工具优先级：`01-global-engineering-rules.md#工具优先级`
- 修改前检查：`01-global-engineering-rules.md#修改前确认`
- 高风险变更：`01-global-engineering-rules.md#高风险变更`
- AGENTS 演进建议：`01-global-engineering-rules.md#项目演进规则`
- Java 后端分层：`07-java-backend-architecture.md#后端分层`
- 新建文件归属地：`07-java-backend-architecture.md#新建文件归属地`
- 注释规范：`07-java-backend-architecture.md#注释规则`
- 枚举与常量：`08-java-style-patterns.md#枚举与常量`
- DTO 参数校验：`08-java-style-patterns.md#参数校验分层`
- 去硬编码与重复逻辑：`08-java-style-patterns.md#去硬编码与重复逻辑`
- 判空与函数式风格：`08-java-style-patterns.md#判空与函数式风格`
- Lombok 使用标准：`08-java-style-patterns.md#lombok-使用标准`
- token 预算与读取窗口：`02-noise-filter-workflow.md#上下文预算`
- 调用链闭环：`02-noise-filter-workflow.md#调用链确认`
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

## 性能原则

- 主文件只负责触发和路由；细节只在需要时打开。
- 先做主题判别，再读文件；同一任务默认只打开 1 个主 reference，跨层任务最多打开 2 到 3 个。
- 路由采用“关键词 + 任务意图 + 影响面”三者交叉确认，避免只凭单个词误读。
- 优先 `rg --files`、符号检索、局部窗口读取，不做全仓无目的扫描。
- 默认读取 200 到 300 行窗口；关键段最多 500 行。
- 工具输出只保留结论、文件路径、行号和关键片段，不搬运大段日志。

## 高精度路由

- `Controller`、`Service`、`接口层`、`实现层`、`module 归属`、`新建文件放哪`、`注释`：读 `07-java-backend-architecture.md`。
- `Enum`、`常量`、`参数校验`、`Bean Validation`、`Lombok`、`Optional`、`Stream`、`重复 if/set`、`硬编码`、`函数式`：读 `08-java-style-patterns.md`。
- `mvn`、`pom.xml`、`-pl`、`-am`、`多模块构建`、`测试命令`：读 `03-maven-backend-build.md`。
- `MAVEN_HOME`、`JAVA_HOME`、`Node`、`pnpm`、`IDE 配置路径`、`.codex/local-environment.json`：读 `06-environment-discovery.md`。
- `flex`、`grid`、`组件`、`页面`、`路由守卫`、`加载/空状态`：读 `04-frontend-rules.md`。
- `Context Capsule`、`最终回复`、`记忆管理`、`会话切换`：读 `05-delivery-templates.md`。
