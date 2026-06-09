# 全局工程规则

本文件内化用户全局 `AGENTS.md` 的工程约束，避免切换会话或窗口后规则丢失。

## 语言偏好

- 默认使用简体中文回复。
- 分析、解释、计划、变更说明、验证结果、根因分析、下一步建议都用简体中文。
- 代码、命令、配置项、环境变量、文件名、类名、方法名、日志、异常信息保持原文。
- 不使用英文标题 `What Changed`、`Validation`、`Root Cause`、`Next Steps`、`Summary`。
- 使用中文标题：`变更内容`、`验证结果`、`根因分析`、`下一步`、`总结`。

## 工具优先级

JetBrains 项目必须优先使用 JetBrains MCP / IDE 工具完成代码读取、定位、修改和诊断。

- 只有 JetBrains MCP 明确不可用、超时或返回错误时，才允许使用 Shell。
- 禁止未尝试 JetBrains MCP 就直接用 Shell 扫描或修改 JetBrains 项目。
- 优先分析最小范围，不做无意义全仓扫描。
- 未明确要求时不要使用 Sub Agent。

非 JetBrains 项目可直接使用本地文件工具。搜索优先 `rg` 或 `rg --files`。

## 修改前确认

修改前必须确认：

1. 目标文件。
2. 问题根因。
3. 最小修改方案。
4. 不应受影响的模块、接口、数据结构、权限和业务逻辑。

修改前再次引用任务编号确认目标。若任务描述与实现方向不一致，立即停止并汇报。

## 核心规则

- 优先最小、安全、可回滚的修改。
- 除非任务明确要求，否则保持现有行为不变。
- 不修改无关文件，不随意重构正常工作的代码。
- 不随意修改 API、DTO、数据库字段、权限、路由、配置键和公共契约。
- 未明确批准不要新增依赖。
- 未批准不要执行数据迁移、删除操作、网络写入和影响工作区外部数据的命令。
- 参考类似代码风格和文件存放位置。
- 新建文件前必须确认归属地：所属 module、层级职责、包路径、同类文件位置和依赖方向；多层架构项目不得凭当前目录或类名随意放置。

## 可扩展性

- 优先复用现有模式。
- 避免硬编码。
- 保持接口清晰。
- 保留未来扩展点。

## 健壮性

- 做好输入校验。
- 保留认证、权限、租户隔离和审计逻辑。
- 处理空值、异常值和边界情况。
- 不吞异常。
- 避免 N+1 查询、全表扫描和无分页查询。

## 可维护性

- 保持模块职责单一。
- 优先清晰命名。
- 状态值、类型值、来源值、动作值、阶段值、结果值等明确不变且有固定集合的常量，优先使用 Enum，方便查看、跳转、复用和约束。
- 项目已使用 Lombok 时，优先用 Lombok 消除无意义 getter/setter、构造器和日志样板代码；不要手写只读写字段的机械方法。
- 复杂逻辑说明原因而不是描述代码行为。

## Lombok 使用标准

使用前先确认项目已有 Lombok 依赖和风格；未批准不要新增 Lombok 依赖。

推荐使用：

- DTO、VO、Request、Response、配置属性类：按项目风格使用 `@Getter`、`@Setter`，或在确实需要时使用 `@Data`。
- 只读值对象或不可变对象：优先 `@Getter`、`@RequiredArgsConstructor`、`@Builder`，字段尽量 `final`。
- 构造器样板：使用 `@NoArgsConstructor`、`@AllArgsConstructor`、`@RequiredArgsConstructor`，但要确认框架反射、序列化和 ORM 要求。
- 日志：已有 Lombok 风格时使用 `@Slf4j`，不要重复声明 logger。

谨慎或避免：

- Entity、DO、PO：谨慎使用 `@Data`，避免 `equals`、`hashCode`、`toString` 引发懒加载、循环引用、性能或主键未赋值问题；优先显式 `@Getter`、`@Setter`。
- 继承结构：避免无脑 `@EqualsAndHashCode`，必须确认 `callSuper` 是否符合语义。
- 敏感字段：避免 `@ToString` 输出密码、token、密钥、身份证号等敏感信息。
- 有业务不变式、校验、派生字段或副作用的访问器：不要用 Lombok 掩盖，应显式写方法并说明原因。
- API 契约类：不要因 Lombok 改变序列化行为、字段命名、构造器可见性或框架绑定能力。

禁止：

- 手写无业务逻辑的 getter/setter。
- Lombok 注解和手写同名 getter/setter 混杂，除非手写方法包含明确业务语义。
- 为了少写代码滥用 `@Data`，导致 equals/hashCode/toString 暴露风险。

检查标准：

- 该类是否只是数据承载，还是有业务不变式。
- 是否涉及 ORM、序列化、反序列化、框架代理、继承、懒加载或敏感字段。
- 是否已有同 module 同类文件的 Lombok 使用风格。
- 是否需要保留显式方法以表达业务含义。

## 枚举与常量

优先使用 Enum 的场景：

- 业务状态：任务状态、审核状态、发布状态、启停状态、处理阶段。
- 类型分类：文件类型、报告类型、规则类型、消息类型、来源类型。
- 固定动作：创建、提交、撤回、通过、驳回、归档、重试。
- 固定结果：成功、失败、部分成功、跳过、待处理。
- 明知不会频繁变动，且需要在多处判断、展示、持久化或跨层传递的值。

不应继续散落字符串或数字常量的场景：

- 多处出现相同 `"status"`、`"type"`、`"source"`、`1/2/3` 等魔法值。
- Controller、Service、Mapper、DTO 或前端契约中重复判断同一批固定值。
- 注释必须反复解释某个数字或字符串含义。

枚举设计要求：

- 枚举名表达业务域，例如 `AuditTaskStatus`、`ReportType`，不要使用泛化的 `StatusEnum`。
- 枚举项命名稳定清晰，字段至少包含持久化 code 和展示/说明 label 或 desc。
- 提供按 code 反查的方法，并处理未知值；不要在业务代码里散写 `valueOf` 或手写字符串比较。
- 数据库存储、API 入参出参、前端展示必须保持兼容；新增枚举不能随意修改既有 code。
- 已存在项目统一枚举接口、序列化注解、字典体系或类型处理器时，优先复用。
- 临时、用户可配置、数据库字典动态维护的值，不强行写死为 Enum；可用字典/配置模型。

修改涉及枚举时：

- 先确认影响 API、DTO、数据库字段、前端选项、权限判断、历史数据和查询条件。
- 新增枚举项优先兼容旧逻辑。
- 删除或改名枚举项属于高风险变更，必须说明迁移和回滚方案。

## 新建文件归属地

新建任何源文件前必须先回答：

1. 它属于哪个业务域或技术域。
2. 它属于哪个 module。
3. 它属于哪一层：Controller、API/Facade、Service 接口、Service 实现、DAO/Mapper、DTO/VO、Entity、Enum、Config、Client、Job、Test。
4. 同类文件当前放在哪里，包名如何命名。
5. 新文件会被谁依赖，它又依赖谁，是否违反模块依赖方向。

多层 Maven 或多模块项目必须特别确认：

- Service 接口通常放在 API、contract、service-api 或 facade 类 module，不能误放到 impl module。
- Service 实现通常放在 service、service-impl、biz 或 server 类 module，不能误放到 interface/API module。
- Entity、DO、PO、Mapper 通常放在 domain、dao、repository、infrastructure 或 persistence 类 module，不能随意放进 controller 或 API module。
- DTO、Request、Response、VO 通常按现有契约 module 或 web/API module 约定放置，不能与数据库实体混放。
- Controller 通常放在 web、server、adapter 或 application 启动 module，不能反向依赖实现细节以外的内部类。
- 测试文件必须放在与被测模块对应的 `src/test`，不要为了方便放到聚合 root 或无关 module。

若无法确认归属地：

- 先检索同名业务域、同类后缀和已有包结构。
- 再查看 `pom.xml` 的 `modules`、依赖关系和已有调用链。
- 仍不确定时，先汇报候选位置和依据，不直接新建文件。

## 注释规则

注释说明“为什么”，不重复说明代码正在“做什么”。

注释目标：

- 不冗余：命名、类型、注解和简单流程已经能说明的内容不写。
- 不缺失：接口契约、重要业务规则、边界条件、权限约束、状态流转和跨系统约定必须写清楚。
- 不杂乱：同一层级使用一致粒度，注释放在接口、类、方法或复杂分支入口，不在每行代码旁堆碎片。

必须写注释的场景：

- Service 接口的对外能力、业务语义、关键入参、返回结果和异常边界。
- Service 实现层的重要实现方法，尤其是状态流转、权限/租户约束、事务边界、幂等、缓存、消息、跨系统调用和兼容逻辑。
- 复杂业务规则。
- 临时兼容逻辑。
- 魔法值来源。
- 性能优化原因。
- 风险边界。
- 数据交换层实体、数据库层实体等需要明确字段语义的实体。
- 无法通过命名理解的方法。

禁止：

- 重复代码行为描述。
- 无意义注释。
- 注释掉的大段废弃代码。
- 无负责人、无背景的 TODO。
- 在 Controller 中用注释解释大段业务流程；出现这种情况通常说明业务逻辑应下沉到 Service。
- 同一业务规则在 Controller、Service 接口和 Service 实现中重复写三份不同口径的注释。

优先说明业务原因、数据来源、权限约束、状态机流转原因、特殊兼容逻辑、跨系统调用和临时修复边界。

注释放置建议：

- Controller：只保留必要的接口说明或分组说明，不描述具体业务算法。
- Service 接口：写“对外承诺”，说明能力、参数约束、返回含义、权限或状态前置条件。
- Service 实现：写“实现原因”，说明为什么这样处理事务、状态、兼容、缓存、调用顺序或异常边界。
- DAO/Mapper：写 SQL 约束、索引依赖、数据权限、软删除、租户和特殊查询边界。
- DTO/VO/Entity：写字段业务含义、来源、单位、枚举值、兼容字段和跨系统映射。

## 后端规则

- 保持现有 API 契约。
- 修改前分析 Controller、Service、DAO、DTO、权限、事务和调用链。
- 新增 Controller、Service、ServiceImpl、Mapper、DTO、Entity、Enum、Client、Job、Config、Test 前，必须先确认对应 module 和包路径；多模块项目中接口、实现、实体和契约文件可能分属不同 module。
- 明确固定集合的状态、类型、来源、动作、阶段、结果等值，优先沉淀为业务 Enum；不要在 Controller、Service、Mapper、DTO 中散落魔法字符串或数字。
- 简单入参校验优先放在 DTO/Request 层使用 Bean Validation，例如 `@NotNull`、`@NotBlank`、`@Min`、`@Max`、`@Range`、`@Size`、`@Pattern`、`@Valid`、`@Validated`；不要在 Controller 或 Service 中堆大量空值和范围判断后手写 `AjaxResult.error`。
- 已使用 Lombok 的 Java 项目中，不手写无意义 getter/setter；Entity 谨慎使用 `@Data`，DTO/VO/Request/Response 按项目风格使用 Lombok。
- Controller 层保持简洁，只负责路由、参数接收与校验触发、权限注解、调用 Service、响应转换；不要在 Controller 写业务编排、状态流转、复杂条件、数据库访问或跨系统调用。
- Service 接口层表达业务能力和契约，重要接口方法必须有清晰注释，说明业务语义、参数约束、返回含义和异常/权限边界。
- Service 实现层承载业务流程、状态流转、事务控制、幂等、缓存、消息和跨系统调用；重要实现方法必须补充原因型注释，避免调用方只能靠阅读细节理解业务规则。
- 不绕过校验、认证、授权、数据权限和审计。
- 避免 N+1、全表扫描、无限分页、吞异常和不一致错误响应。

## 参数校验分层

简单字段校验应优先声明在 DTO、Request 或 Form 类上：

- 必填：`@NotNull`、`@NotBlank`、`@NotEmpty`。
- 数值范围：`@Min`、`@Max`、Hibernate Validator 的 `@Range`。
- 长度范围：`@Size`、`@Length`。
- 格式：`@Pattern`、`@Email`。
- 嵌套对象：字段使用 `@Valid`，Controller 入参使用 `@Validated` 或 `@Valid`。

Controller 层只负责触发校验和交给统一异常处理：

- 不在 Controller 中重复写 `input == null`、`field == null`、`field < min || field > max` 这类基础校验。
- 不在 Controller 中把每个字段校验失败都手写成 `return AjaxResult.error(...)`。
- 使用项目已有的全局异常处理、参数绑定错误处理和统一响应格式。

Service 层只保留 Bean Validation 难以表达的业务校验：

- 跨字段关系，例如 “A 为某值时 B 必填”。
- 依赖数据库、权限、租户、状态机、配额、唯一性、幂等的校验。
- 需要调用外部系统或根据当前用户上下文判断的校验。

迁移既有手写校验时：

- 先确认项目是否已有统一 `MethodArgumentNotValidException`、`BindException`、`ConstraintViolationException` 处理。
- 错误提示文案放在注解 `message` 中，保持与原有返回文案兼容。
- 如果原接口固定返回 `AjaxResult`，通过统一异常处理适配，不在每个 Controller 方法里散写。
- 对 `0 或 3-50` 这类非连续规则，可保留自定义注解或少量业务校验，但应集中封装，不把多个字段校验堆在 Controller。

## 跨层规则

- 先梳理完整调用链。
- 保证字段、类型、枚举、分页和权限一致。
- 不用前端硬编码掩盖后端问题。
- 契约变更优先兼容旧逻辑。

## 高风险变更

涉及 API、DTO、SQL、数据库字段、权限、状态管理、枚举或业务规则时：

1. 说明修改原因。
2. 列出影响范围。
3. 优先兼容旧逻辑。
4. 验证完整流程。

## 项目演进规则

项目结构、模块边界、核心业务流程或技术架构发生明显变化时，需要给出 AGENTS 更新建议；用户同意后再修改 AGENTS。

重大变化包括：

- 新增一级模块、微服务、独立前端应用、AI 能力模块。
- 新增数据库或存储组件、核心业务流程、公共 SDK。
- 新增跨模块共享能力、统一网关或认证体系。
- 大规模目录重构或重要架构调整。

新增规则必须向后兼容、避免重复、保持简洁，只补充增量内容。普通业务代码变更不要频繁修改 AGENTS。
