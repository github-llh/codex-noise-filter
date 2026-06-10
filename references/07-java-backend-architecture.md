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
