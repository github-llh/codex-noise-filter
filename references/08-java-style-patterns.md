# Java 代码风格模式

本文件按需读取。只承载 Java 落地写法；跨技术栈通用判断先看 `01-global-engineering-rules.md#跨技术栈硬编码治理` 和 `01-global-engineering-rules.md#跨技术栈重复逻辑治理`。只有任务涉及 Java 枚举、配置属性、Bean Validation、MapStruct/BeanUtils、Optional、Stream、函数式风格或 Lombok 时打开。

## 枚举与常量

先按 `01-global-engineering-rules.md#跨技术栈硬编码治理` 判断值的类型，再选择 Java 落地方式。不要只看变量名前缀；只要代码中出现参与业务判断、外部协议、消息格式、平台/渠道编码、序列化、持久化、HTTP header/content type/media type、默认值、阈值或时间窗的字符串/数字，触碰时都必须检查是否应使用 Java enum、集中常量、配置属性或动态字典。

状态值、类型值、来源值、动作值、阶段值、结果值等明确不变且有固定集合的常量，优先使用业务 Enum，方便查看、跳转、复用和约束。

优先使用 Enum：

- 业务状态、类型分类、固定动作、固定结果。
- 明知不会频繁变动，且需要在多处判断、展示、持久化或跨层传递的值。
- 多处出现相同 `"status"`、`"type"`、`"source"`、`1/2/3` 等魔法值。
- 固定来源、状态、类型、协议、模式、动作、结果等值需要反查、展示、校验、排序、兼容旧 code 或跨模块传递。

设计要求：

- 枚举名表达业务域，例如 `AuditTaskStatus`、`ReportType`，不要使用泛化的 `StatusEnum`。
- 枚举项命名稳定清晰，字段至少包含持久化 code 和展示/说明 label 或 desc。
- 提供按 code 反查的方法，并处理未知值；不要在业务代码里散写 `valueOf` 或手写字符串比较。
- 数据库存储、API 入参出参、前端展示必须保持兼容；新增枚举不能随意修改既有 code。
- 已存在项目统一枚举接口、序列化注解、字典体系或类型处理器时，优先复用。
- 动态字典、用户可配置项、运行期可扩展值，不强行写死为 Enum。
- 删除、改名、改 code 属于高风险变更，必须说明迁移和回滚方案。

跨模块契约使用的枚举放 api/contract/facade 类 module；仅实现内部使用的枚举放 service/biz/domain 类 module。不要依赖 `ordinal`。

常量处理边界：

- 固定业务集合：优先 Enum。
- 外部平台、消息格式、通知渠道、支付方式、登录来源、任务动作、导入导出类型等闭合集合：优先业务 Enum；如果只在前端/接口契约层使用，也要放到对应 contract/api module，而不是散在 Service 实现。
- HTTP header、content type、media type、charset、时间单位、状态码等技术标准值：优先使用 Spring/JDK/第三方 SDK 已有常量；没有可用常量时，集中到协议常量类或私有常量，并保留来源说明。
- 环境 URL、密钥、开关、阈值、时间窗、外部系统地址、超时、重试、线程池、缓存 TTL：优先配置属性类，不写死在 Service。
- 单一技术常量且不会跨层传递：可保留 `private static final`，但要命名清晰、靠近使用点并说明来源。
- 本次修改触碰到固定常量时，至少检查是否已有同类 Enum/配置；有则复用，没有则给出是否沉淀的判断。

## 配置外置化

满足以下任一条件时，优先写入 `application.yml`、`application-*.yml`、`application.properties` 或项目已有配置中心，并通过配置类注入：

- 不同环境会变化：URL、域名、端口、协议、账号、密钥、token、bucket、topic、queue、开关。
- 需要运维调整：超时时间、重试次数、批量大小、线程池参数、缓存 TTL、限流阈值、时间窗。
- 外部系统集成参数：baseUrl、appKey、secretKey、clientId、回调地址、协议版本。
- 风险或策略参数：阈值、评分、开关、灰度比例、保留天数、清理周期。
- 多处复用且不属于固定业务枚举的值。

注入方式：

- 一组相关配置优先使用 `@ConfigurationProperties` 建立类型安全配置类。
- 单个简单配置可按项目风格使用 `@Value`，但不要在多个类里重复散写同一个 key。
- 配置类要有清晰 prefix，例如 `camera.ezviz`、`audit.report`，字段名表达业务含义。
- 配置项要有默认值、校验或启动失败策略；密钥类配置不得在代码里给真实默认值。
- 优先复用项目已有配置类、配置前缀和配置中心接入方式。

不应外置到配置文件：

- 固定业务状态、类型、动作、结果等闭合集合，应优先 Enum。
- 只在一个方法内部使用的纯技术常量，且不会随环境变化，可保留局部常量。
- 用户可动态维护的数据字典或业务规则，应走数据库/配置中心/规则系统，而不是写死到 yml。

修改配置时：

- 同步更新配置类、示例配置、环境差异说明和必要的启动校验。
- 不提交真实密钥、token、生产地址或敏感账号。
- 改配置 key 属于兼容风险，优先保留旧 key 兼容或说明迁移方式。

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

## 去硬编码与重复逻辑

先按 `01-global-engineering-rules.md#跨技术栈重复逻辑治理` 判断是否需要收敛；本节只描述 Java 可用的落地手段。遇到字段不同但逻辑相同的多段 `if`、多段 `setXxx`、多段转换、校验或赋默认值时，不要机械复制一大串代码。

Java 中优先识别：

- 多个 `if` 只差字段名、阈值、错误文案或目标 setter。
- 多个 `setXxx(source.getXxx())` 只是字段不同。
- 多个 `if (xxx != null) target.setXxx(xxx)` 重复出现。
- 多个状态、类型、来源、动作分支在不同方法中重复判断。
- 同一批字段在 DTO、Entity、VO、Excel、导入导出对象之间反复手写转换。

优先选择当前项目技术栈已有能力：

- 对象映射：项目已有 MapStruct、BeanUtils、Spring `BeanUtils`、hutool `BeanUtil`、ModelMapper 等时，优先复用既有风格；不要为少量字段盲目新增依赖。
- MyBatis / ORM：动态 SQL、条件构造器、`set` 条件更新、类型处理器、枚举映射等已有能力优先使用。
- Bean Validation：简单字段校验用注解和统一异常处理，不堆 `if return AjaxResult.error`。
- 枚举策略：固定状态或类型分支优先下沉到业务 Enum、策略表、handler map 或多态实现。
- 集合/函数式：重复字段处理可用字段描述列表、函数引用、`BiConsumer`、`Function`、循环或小型 helper 收敛。
- 配置驱动：稳定规则但值可配置时，优先配置项或字典，不硬编码在多个方法里。

抽象必须减少真实重复，并让业务意图更清晰；不要为了“高级”而引入难读的反射、复杂泛型或过度函数式代码。三处以上相似逻辑默认需要考虑收敛。性能敏感路径谨慎使用反射型 Bean copy；优先编译期映射或显式 helper。

如果项目已有 MapStruct 等映射器，应优先使用项目既有 mapper，而不是新增 helper。

如果重复逻辑背后是业务状态、类型、来源、外部系统、处理模式或稳定扩展点，不要只抽成技术 helper；优先按 `07-java-backend-architecture.md#业务抽象与扩展性` 评估业务抽象，让新增业务类型时改动点更集中、更可测试。

## 判空与函数式风格

判空逻辑优先选择当前 Java 版本和项目技术栈支持的清晰写法，不机械堆叠多层 `if (x != null)`。

使用前先确认：

- `pom.xml`、`maven-compiler-plugin`、`maven.compiler.release/source/target`、IDE SDK 或 toolchain 指定的 Java 版本。
- 项目现有风格是否已经使用 `Optional`、Stream、lambda、方法引用、增强 `switch`、record 等语法。
- 团队是否已有 `StringUtils`、`CollectionUtils`、`ObjectUtils`、业务 helper 或统一空值处理工具。

推荐使用：

- 可缺失的查询结果或中间计算结果，可用 `Optional<T>` 表达“可能没有值”。
- 链式取值、默认值、条件映射可用 `map`、`flatMap`、`filter`、`orElse`、`orElseGet`、`orElseThrow`。
- 集合转换、过滤、分组、聚合可用 Stream，但要保持可读性。
- 重复判空赋值可结合方法引用、`Consumer`、`Function` 或小型 helper。
- Java 版本支持时，可借鉴 Scala 的表达式化思路：用 `map/filter/flatMap`、不可变中间值、策略映射、增强 `switch` 表达清晰分支。

谨慎或避免：

- 不要把 `Optional` 用作 Entity、DTO、VO 字段类型、Controller 入参或 JSON 契约字段。
- 不要把集合包装成 `Optional<List<T>>`；空集合优先用空集合表达。
- 不要在业务代码里 `optional.get()` 后不检查。
- 不要为了函数式而写深层嵌套 Optional/Stream，导致调试困难。
- 简单直接的空判断如果更清楚，可以保留，不强行改成函数式链。
- 性能敏感路径、复杂异常处理、需要详细日志的流程，优先选择清晰的显式代码。

函数式风格必须服务业务表达：减少重复、减少空指针风险、让数据流更清楚；不能为了“像 Scala”而牺牲 Java 项目的可维护性。

## Lombok 使用标准

使用前先确认项目已有 Lombok 依赖和风格；未批准不要新增 Lombok 依赖。

推荐：

- DTO、VO、Request、Response、配置属性类：按项目风格使用 `@Getter`、`@Setter`，或在确实需要时使用 `@Data`。
- Entity、DO、PO：优先跟随项目同类实体范式；如果项目实体普遍使用 `@Data`，新增或触碰实体直接使用 `@Data`，不要手写无意义 getter/setter。
- 只读值对象或不可变对象：优先 `@Getter`、`@RequiredArgsConstructor`、`@Builder`，字段尽量 `final`。
- 构造器样板：使用 `@NoArgsConstructor`、`@AllArgsConstructor`、`@RequiredArgsConstructor`，但要确认框架反射、序列化和 ORM 要求。
- 日志：已有 Lombok 风格时使用 `@Slf4j`，不要重复声明 logger。

谨慎或避免：

- Entity、DO、PO 在存在 JPA/Hibernate 懒加载关联、双向关联、超大字段、敏感字段、主键未赋值即参与集合比较等风险时，避免无脑 `@Data`；此时优先 `@Getter`、`@Setter`，必要时显式控制 `@EqualsAndHashCode`、`@ToString`。
- 继承结构避免无脑 `@EqualsAndHashCode`，必须确认 `callSuper` 是否符合语义。
- 敏感字段避免 `@ToString` 输出密码、token、密钥、身份证号等敏感信息。
- 有业务不变式、校验、派生字段或副作用的访问器不要用 Lombok 掩盖，应显式写方法并说明原因。
- API 契约类不要因 Lombok 改变序列化行为、字段命名、构造器可见性或框架绑定能力。

触碰即检查：

- 新增实体、返回实体、DTO/VO 或配置属性类时，先找同包或同模块同类文件的 Lombok 注解范式并保持一致。
- 修改已有实体时，如果文件里只有无业务逻辑 getter/setter，且项目已有 Lombok 依赖和同类用法，优先改为 Lombok 注解。
- 只保留有业务含义的访问器，例如派生值、兼容字段、脱敏、格式化或副作用明确的方法，并用注释说明原因。

禁止手写无业务逻辑的 getter/setter；禁止 Lombok 注解和无意义手写 getter/setter 混杂；禁止为了少写代码滥用 `@Data`，但项目实体已形成 `@Data` 范式时应优先复用该范式。
