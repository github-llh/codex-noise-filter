# Java 后端规则

本文件按需读取。只有任务涉及 Java 后端代码、新建后端文件、Controller/Service/DTO/Entity/Enum/Lombok/参数校验/注释时打开。

## 后端分层

- 保持现有 API 契约。
- 修改前分析 Controller、Service、DAO、DTO、权限、事务和调用链。
- Controller 层保持简洁，只负责路由、参数接收与校验触发、权限注解、调用 Service、响应转换。
- 不要在 Controller 写业务编排、状态流转、复杂条件、数据库访问或跨系统调用。
- Service 接口层表达业务能力和契约，重要接口方法必须有清晰注释，说明业务语义、参数约束、返回含义和异常/权限边界。
- Service 实现层承载业务流程、状态流转、事务控制、幂等、缓存、消息和跨系统调用。
- Service 重要实现方法必须补充原因型注释，避免调用方只能靠阅读细节理解业务规则。
- 不绕过校验、认证、授权、数据权限和审计。
- 避免 N+1、全表扫描、无限分页、吞异常和不一致错误响应。

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

若无法确认归属地，先检索同名业务域、同类后缀和已有包结构，再查看 `pom.xml` 的 `modules`、依赖关系和已有调用链；仍不确定时，先汇报候选位置和依据，不直接新建文件。

## 注释规则

注释说明“为什么”，不重复说明代码正在“做什么”。

注释目标：

- 不冗余：命名、类型、注解和简单流程已经能说明的内容不写。
- 不缺失：接口契约、重要业务规则、边界条件、权限约束、状态流转和跨系统约定必须写清楚。
- 不杂乱：同一层级使用一致粒度，注释放在接口、类、方法或复杂分支入口，不在每行代码旁堆碎片。

必须写注释：

- Service 接口的对外能力、业务语义、关键入参、返回结果和异常边界。
- Service 实现层的重要实现方法，尤其是状态流转、权限/租户约束、事务边界、幂等、缓存、消息、跨系统调用和兼容逻辑。
- 复杂业务规则、临时兼容逻辑、魔法值来源、性能优化原因、风险边界。
- 数据交换层实体、数据库层实体等需要明确字段语义的实体。

禁止：

- 重复代码行为描述、无意义注释、注释掉的大段废弃代码、无负责人无背景的 TODO。
- 在 Controller 中用注释解释大段业务流程；出现这种情况通常说明业务逻辑应下沉到 Service。
- 同一业务规则在 Controller、Service 接口和 Service 实现中重复写三份不同口径的注释。

放置建议：Controller 只保留必要接口说明；Service 接口写对外承诺；Service 实现写实现原因；DAO/Mapper 写 SQL 与数据边界；DTO/VO/Entity 写字段业务含义、来源、单位、枚举值、兼容字段和跨系统映射。

## 枚举与常量

状态值、类型值、来源值、动作值、阶段值、结果值等明确不变且有固定集合的常量，优先使用业务 Enum，方便查看、跳转、复用和约束。

优先使用 Enum：

- 业务状态、类型分类、固定动作、固定结果。
- 明知不会频繁变动，且需要在多处判断、展示、持久化或跨层传递的值。
- 多处出现相同 `"status"`、`"type"`、`"source"`、`1/2/3` 等魔法值。

设计要求：

- 枚举名表达业务域，例如 `AuditTaskStatus`、`ReportType`，不要使用泛化的 `StatusEnum`。
- 枚举项命名稳定清晰，字段至少包含持久化 code 和展示/说明 label 或 desc。
- 提供按 code 反查的方法，并处理未知值；不要在业务代码里散写 `valueOf` 或手写字符串比较。
- 数据库存储、API 入参出参、前端展示必须保持兼容；新增枚举不能随意修改既有 code。
- 已存在项目统一枚举接口、序列化注解、字典体系或类型处理器时，优先复用。
- 动态字典、用户可配置项、运行期可扩展值，不强行写死为 Enum。
- 删除、改名、改 code 属于高风险变更，必须说明迁移和回滚方案。

跨模块契约使用的枚举放 api/contract/facade 类 module；仅实现内部使用的枚举放 service/biz/domain 类 module。不要依赖 `ordinal`。

## 参数校验分层

简单字段校验优先声明在 DTO、Request 或 Form 类上：

- 必填：`@NotNull`、`@NotBlank`、`@NotEmpty`。
- 数值范围：`@Min`、`@Max`、Hibernate Validator 的 `@Range`。
- 长度范围：`@Size`、`@Length`。
- 格式：`@Pattern`、`@Email`。
- 嵌套对象：字段使用 `@Valid`，Controller 入参使用 `@Validated` 或 `@Valid`。

Controller 只负责触发校验和交给统一异常处理：

- 不重复写 `input == null`、`field == null`、`field < min || field > max`。
- 不把每个字段校验失败都手写成 `return AjaxResult.error(...)`。
- 使用项目已有的全局异常处理、参数绑定错误处理和统一响应格式。

Service 只保留 Bean Validation 难以表达的业务校验：跨字段关系、数据库、权限、租户、状态机、配额、唯一性、幂等、外部系统或当前用户上下文校验。

迁移既有手写校验时，先确认项目是否已有 `MethodArgumentNotValidException`、`BindException`、`ConstraintViolationException` 统一处理。错误提示文案放在注解 `message` 中并保持兼容。`0 或 3-50` 这类非连续规则可用自定义注解或集中校验方法，避免堆在 Controller。

## Lombok 使用标准

使用前先确认项目已有 Lombok 依赖和风格；未批准不要新增 Lombok 依赖。

推荐：

- DTO、VO、Request、Response、配置属性类：按项目风格使用 `@Getter`、`@Setter`，或在确实需要时使用 `@Data`。
- 只读值对象或不可变对象：优先 `@Getter`、`@RequiredArgsConstructor`、`@Builder`，字段尽量 `final`。
- 构造器样板：使用 `@NoArgsConstructor`、`@AllArgsConstructor`、`@RequiredArgsConstructor`，但要确认框架反射、序列化和 ORM 要求。
- 日志：已有 Lombok 风格时使用 `@Slf4j`，不要重复声明 logger。

谨慎或避免：

- Entity、DO、PO 谨慎使用 `@Data`，避免 `equals`、`hashCode`、`toString` 引发懒加载、循环引用、性能、敏感字段或主键未赋值问题；优先显式 `@Getter`、`@Setter`。
- 继承结构避免无脑 `@EqualsAndHashCode`，必须确认 `callSuper` 是否符合语义。
- 敏感字段避免 `@ToString` 输出密码、token、密钥、身份证号等敏感信息。
- 有业务不变式、校验、派生字段或副作用的访问器不要用 Lombok 掩盖，应显式写方法并说明原因。
- API 契约类不要因 Lombok 改变序列化行为、字段命名、构造器可见性或框架绑定能力。

禁止手写无业务逻辑的 getter/setter；禁止 Lombok 注解和无意义手写 getter/setter 混杂；禁止为了少写代码滥用 `@Data`。
