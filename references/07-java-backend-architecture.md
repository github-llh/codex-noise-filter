# Java 后端架构规则

本文件按需读取。只有任务涉及 Java 后端分层、新建文件归属地、Controller/Service/DAO/DTO/Entity、接口契约、注释和调用链时打开。Java 代码风格、枚举、参数校验、Lombok、Optional、去重复逻辑见 `08-java-style-patterns.md`。

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

## 事务管理

事务默认放在 Service 实现层的业务用例入口，不放在 Controller，不放在单纯 DTO/Mapper/工具类。

选择顺序：

1. 优先使用当前项目 Java/Spring 版本推荐且项目已启用的事务机制，例如 Spring `@Transactional`、`TransactionTemplate`、事务事件或现有事务工具。
2. 优先复用项目已有事务注解风格、传播级别、异常处理和全局事务管理配置。
3. 不新增事务框架或分布式事务组件，除非用户明确批准并完成影响评估。

修改前必须确认事务边界：

1. 本方法是否写数据库。
2. 是否跨多表、多 Mapper、多 Repository、多 Service。
3. 是否涉及状态流转、库存/额度/计数、审计、业务文件、缓存、消息、外部调用。
4. 调用链上是否已有事务，是否存在 self-invocation 导致 `@Transactional` 不生效。
5. 异常是否会被捕获吞掉，是否影响回滚。

使用规则：

- 只读查询优先标注或复用 `readOnly = true`，避免无意义写事务。
- 写操作按最小业务一致性边界加 `@Transactional`，不要把无关查询、远程调用、文件 IO、耗时计算包进长事务。
- 需要精确控制提交/回滚边界、返回值、异常转换、分段提交或部分失败保留时，优先使用项目已有事务管理器或 `TransactionTemplate` 这类函数式事务写法。
- 默认回滚运行时异常；需要对 checked exception 回滚时明确 `rollbackFor`。
- 不在事务内吞异常后继续返回成功；需要捕获时必须重新抛出、标记回滚或返回明确失败。
- 谨慎使用 `REQUIRES_NEW`、`NESTED`、手动事务，必须说明业务原因和回滚边界。
- 批量更新要关注事务大小、锁范围、分页/分批、超时和重试策略。

函数式事务：

- 优先复用项目已有 `PlatformTransactionManager`、`TransactionTemplate`、事务工具类或封装后的事务执行器。
- 适用于“某一段必须回滚、其他段允许提交”的批量处理、导入、补偿、重试和局部失败收集。
- 每个事务块必须有清晰输入、输出、异常策略和回滚说明，不把大量无关逻辑塞进一个 lambda。
- 部分回滚要显式记录成功/失败明细、失败原因、补偿入口和幂等键，避免调用方误以为全量成功。
- 不要在一个大事务里靠吞异常模拟部分成功；应拆分事务边界，或用事务模板分段提交。
- 需要强一致的核心状态流转，不要随意部分提交，除非业务规则明确允许。

示例形态：

```java
Result result = transactionTemplate.execute(status -> {
    try {
        return doBusiness();
    } catch (RecoverableException ex) {
        status.setRollbackOnly();
        return Result.failed(ex.getMessage());
    }
});
```

如果项目已有事务工具封装，优先使用项目封装，不重复创建 `TransactionTemplate`。

外部副作用：

- 事务内不要直接发送不可回滚的消息、HTTP 请求、文件删除、缓存删除等外部副作用。
- 需要事务提交后执行的动作，优先使用事务同步回调、事务事件、可靠消息或项目已有 outbox/afterCommit 机制。
- 缓存更新/删除要与数据库提交顺序一致；避免数据库回滚但缓存已经被改。

跨方法调用：

- 同类内部调用 `this.xxx()` 不会触发 Spring 代理事务；需要调整方法归属、通过代理调用或把事务放到外部入口。
- private 方法上的 `@Transactional` 通常无效；事务注解放在可被代理的方法上。
- 多 Service 调用时，入口 Service 负责定义整体事务边界，下游 Service 不随意扩大传播级别。

必须避免事务失效场景：

- 方法不是 Spring 管理 Bean 上的可代理方法。
- 同类内部自调用绕过代理。
- 方法为 private/final/static 或类/方法无法被代理。
- 异常被 catch 后吞掉，或转换成不会触发回滚的返回值。
- checked exception 未配置 `rollbackFor`。
- 异步线程、线程池、事件监听中误以为继承了调用方事务。
- 数据源、事务管理器、Mapper/Repository 不在同一个事务管理器下。
- 测试环境和生产环境代理方式不同，导致事务行为不一致。

验证要求：

- 涉及事务变更时，至少验证成功提交、异常回滚、部分失败、重复调用或并发边界中的关键路径。
- 涉及状态流转时，验证旧状态不满足条件时不会误更新。
- 涉及消息/缓存/外部调用时，验证事务失败不会留下错误副作用。

高并发、幂等、异步事件、中间件、批量多线程、虚拟线程、用户上下文传播和死锁规避见 `09-concurrency-async-batch.md`。

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
