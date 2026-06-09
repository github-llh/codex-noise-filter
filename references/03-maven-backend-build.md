# Maven 与后端构建

## 本地 Maven 环境

Maven 配置不要只依赖硬编码路径。执行 Maven 构建前，先按 `references/06-environment-discovery.md` 读取缓存、IDE/项目配置和本机候选路径。

当前已知可用候选：

```bash
/Users/lilinhan/dev/maven-3.9.10
/Users/lilinhan/dev/maven-3.9.10/bin/mvn
/Users/lilinhan/maven-git
```

构建 Java/Maven 项目时，使用发现到的 `mavenExecutable` 和 `localRepository` 组合。若本地缓存中仍是当前已知值，则命令形态为：

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git
```

Maven 命令选择顺序：

1. 读取 `.codex/local-environment.json` 中已验证的 `maven.executable` 和 `maven.localRepository`。
2. 读取 IDE/项目 Maven 配置，例如 `.idea/misc.xml`、`.idea/workspace.xml`、`.mvn/maven.config`、`.mvn/wrapper/maven-wrapper.properties`。
3. 如果项目已配置 Maven Wrapper 且项目规则要求使用 Wrapper，使用项目内 `./mvnw`。
4. 否则查找本机候选 Maven，例如 `/Users/lilinhan/dev/maven-*/bin/mvn`、`~/dev/maven-*/bin/mvn`、`/opt/homebrew/bin/mvn`、`/usr/local/bin/mvn`、`mvn`。
5. 找到后执行 `mvn -version` 或 `<path>/mvn -version` 验证，再缓存。
6. 只有上述路径都不可用时，才让用户确认 Maven 环境。

不要擅自修改用户 Maven settings，不新增远程仓库，不执行会写入外部系统的网络发布命令。

## 多层 Maven 结构构建

多模块 Maven 项目默认从聚合 root 节点执行构建，而不是在深层子模块目录直接构建。

root 节点识别顺序：

1. 当前仓库内最上层包含 `.git` 且存在 `pom.xml` 的目录。
2. `pom.xml` 中 `packaging` 为 `pom`，且含 `modules`。
3. 目标模块能在 root 的 `modules` 链路中被 `-pl` 引用。

多层结构例如：

```text
repo-root/
  pom.xml                  # 聚合 root
  server/
    pom.xml                # 二级聚合或业务模块
    service-a/
      pom.xml
```

构建 `server/service-a` 时优先在 `repo-root` 执行：

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl server/service-a -am test
```

如果模块路径无法作为 `-pl` 参数使用，再查 `artifactId`，使用：

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl :artifact-id -am test
```

## 后端构建与验证

按风险选择最轻量验证：

- 只改一个类或方法：优先跑目标单测。
- 改 Service、DAO、Mapper、DTO 映射：跑相关模块测试。
- 改跨模块调用链：从 root 用 `-pl <module> -am` 构建相关模块。
- 改公共契约、枚举、配置、SQL：增加调用方模块验证。

常用命令：

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am test
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -DskipTests package
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -Dtest=ClassNameTest test
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
```

## 后端调用链检查

修改前最少确认：

- Controller 或入口接口。
- Service 方法与事务边界。
- DAO、Mapper、Repository、SQL 或 ORM 条件。
- DTO、VO、Entity、Enum、字段映射。
- 权限、租户、审计、缓存、消息、定时任务。
- 异常响应与空值边界。

不得为了修前端表现绕过后端校验、认证、授权、数据权限或审计。

## 新建文件归属地检查

多层 Maven 项目中新建文件前，必须先确认 module 归属，不要按当前目录就近创建。

检查顺序：

1. 从聚合 root 查看 `pom.xml` 的 `modules`。
2. 查看目标业务域已有同类文件的位置和包名。
3. 查看 module 依赖方向，确认新文件不会造成 API module 依赖 impl、web module 依赖 persistence 细节等反向依赖。
4. 确认新文件层级：Controller、Service 接口、Service 实现、DAO/Mapper、DTO/VO、Entity、Enum、Config、Client、Job、Test。
5. 修改前说明“为什么放在这个 module 和包路径”。

常见归属：

- Controller：web、server、adapter、application 启动 module。
- Service 接口：api、contract、facade、service-api module。
- Service 实现：service、service-impl、biz、server module。
- Entity/DO/PO/Mapper/Repository：domain、dao、repository、infrastructure、persistence module。
- DTO/Request/Response/VO：api、contract、web 或现有契约 module。
- Feign/HTTP/RPC Client：client、integration、infrastructure 或现有外部调用 module。
- Job/Scheduler：job、task、server 或现有调度 module。
- Test：与被测类同 module 的 `src/test`。

如果项目命名与上述不同，以当前项目已有同类文件和依赖关系为准。

## Java 分层与注释

Controller 层：

- 只做路由、参数接收、基础校验触发、权限注解、调用 Service 和响应转换。
- 不写业务规则、复杂条件分支、状态流转、事务控制、数据库访问、远程调用编排。
- 不堆叠简单字段校验，例如空值、范围、长度、格式判断；这类校验优先放到 DTO/Request 的 Bean Validation 注解中。
- 如果 Controller 方法需要多段业务注释，优先把逻辑下沉到 Service。

Service 接口层：

- 表达业务能力和契约，不暴露实现细节。
- 重要接口方法必须注释业务语义、关键入参、返回含义、权限/租户/状态前置条件和异常边界。
- 注释要稳定，避免记录实现类内部步骤。

Service 实现层：

- 承载业务流程、事务边界、状态流转、幂等、缓存、消息和跨系统调用。
- 重要实现方法和复杂分支必须写原因型注释，说明为什么这样处理，而不是复述代码动作。
- 注释粒度与业务决策一致，避免每行碎片化注释。

注释质量检查：

- 命名能说明的，不写注释。
- 业务规则、权限边界、状态流转和兼容逻辑不能缺注释。
- 同一规则只在最合适层级写一次，其他层通过方法名和接口契约表达。
- 修改代码时同步清理过期注释，避免注释与行为不一致。

## 枚举与固定值

后端 Java 项目中，明知不会频繁变化的固定集合优先写成 Enum：

- 状态：任务状态、审核状态、流程状态、启停状态。
- 类型：文件类型、报告类型、规则类型、业务类型。
- 来源：系统来源、数据来源、触发来源。
- 动作：提交、撤回、通过、驳回、归档、重试。
- 结果：成功、失败、跳过、待处理、部分成功。

检查要求：

- 多处重复出现的字符串或数字常量，要优先收敛为业务 Enum。
- Enum 放置位置要符合 module 归属：跨模块契约使用的枚举放 api/contract/facade 类 module；仅实现内部使用的枚举放 service/biz/domain 类 module。
- Enum 必须保留稳定 code，避免直接依赖 ordinal。
- API、DTO、数据库、前端展示已有 code 时，新增 Enum 要兼容既有值。
- 动态字典、用户可配置项、运行期可扩展值，不强行枚举化。
- 涉及删除、改名、改 code 的枚举变更按高风险处理。

## DTO 参数校验

简单参数校验优先放在 DTO/Request 层：

- 必填用 `@NotNull`、`@NotBlank`、`@NotEmpty`。
- 数值范围用 `@Min`、`@Max` 或 `@Range`。
- 长度用 `@Size` 或 `@Length`。
- 格式用 `@Pattern`。
- 嵌套对象用 `@Valid`。

Controller 入参使用项目现有的 `@Validated` 或 `@Valid` 触发校验，并交给统一异常处理转换成 `AjaxResult` 或项目标准错误响应。

不要把以下代码形态继续堆在 Controller 或 Service：

```java
if (input.getSensitivityLevel() == null || input.getSensitivityLevel() < 1 || input.getSensitivityLevel() > 10) {
    return AjaxResult.error("探测灵敏度等级范围为1-10");
}
```

优先改为 DTO 字段约束：

```java
@NotNull(message = "探测灵敏度等级不能为空")
@Range(min = 1, max = 10, message = "探测灵敏度等级范围为1-10")
private Integer sensitivityLevel;
```

保留在 Service 的校验必须是业务校验，例如跨字段关系、状态机、数据库唯一性、权限/租户、外部系统依赖。非连续规则如 `0 或 3-50` 可使用自定义注解，或集中到专门校验方法，避免 Controller 中堆多个字段的 `if`。

## Maven 失败处理

- 依赖缺失时先确认本次使用的 `maven.localRepository` 是否来自缓存、IDE 配置或项目配置。
- Maven 版本不一致时先确认本次使用的 `maven.executable` 是否已验证并缓存。
- 多模块找不到依赖时确认是否加了 `-am`。
- 指定测试不存在或跨模块时可加 `-Dsurefire.failIfNoSpecifiedTests=false`。
- 构建失败后先区分是本次改动、历史失败、依赖环境还是测试选择错误，不连续盲改。
