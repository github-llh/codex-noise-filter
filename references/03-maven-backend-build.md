# Maven 与后端构建

本文件只处理 Maven 环境、构建、验证和多模块定位。通用环境命令、验证策略和安全边界先按 `01-global-engineering-rules.md` 判断；Java 后端分层、注释、新建文件归属地见 `07-java-backend-architecture.md`；枚举、参数校验、Lombok、Optional 和去重复逻辑见 `08-java-style-patterns.md`。

## 本地 Maven 环境

Maven 配置不要只依赖硬编码路径。执行 Maven 构建前，先按 `06-environment-discovery.md#跨系统缓存文件命名` 解析 active cache path，再按 `14-environment-cache-by-stack.md#mavenjava-环境缓存` 读取缓存、`pom.xml`、`.mvn/*`、wrapper、IDE/项目配置、Java/Maven 版本约束和本机候选路径。

每个使用者的 Maven 安装路径和本地仓库都可能不同，skill 文档不得写死个人目录。构建命令必须使用本工作区 active cache path 中已验证的 `maven.executable` 与 `maven.localRepository`；没有缓存时先发现、验证，再写入 profile 环境缓存。

构建 Java/Maven 项目时，命令形态为：

```bash
<mavenExecutable> -Dmaven.repo.local=<localRepository>
```

Maven 命令选择顺序：

1. 读取当前目标模块和聚合 root 的 `pom.xml`，解析 `modules`、`parent`、`artifactId`、`java.version`、`maven.compiler.release/source/target` 和关键插件。
2. 读取 active cache path 中仍匹配当前 `mavenRoot`、`modulePath`、Java 版本约束、wrapper 和本地仓库的缓存。
3. 读取 IDE/项目 Maven 配置，例如 `.idea/misc.xml`、`.idea/workspace.xml`、`.mvn/maven.config`、`.mvn/jvm.config`、`.mvn/wrapper/maven-wrapper.properties`。
4. 如果项目已配置 Maven Wrapper 且项目规则要求使用 Wrapper，使用项目内 `./mvnw`。
5. 否则查找本机候选 Maven，例如 `~/dev/maven-*/bin/mvn`、`~/.sdkman/candidates/maven/*/bin/mvn`、`/opt/homebrew/bin/mvn`、`/usr/local/bin/mvn`、`mvn`。
6. 找到后执行 `mvn -version` 或 `<path>/mvn -version`，必要时带上匹配的 `JAVA_HOME` 验证，再缓存。
7. 只有上述路径都不可用且无法从项目配置、IDE 配置或本机候选验证出可用工具链时，才说明缺口并请求环境信息。

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
  pom.xml
  server/
    pom.xml
    service-a/
      pom.xml
```

构建 `server/service-a` 时优先在 `repo-root` 执行：

```bash
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl server/service-a -am test
```

如果模块路径无法作为 `-pl` 参数使用，再查 `artifactId`：

```bash
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl :artifact-id -am test
```

## 后端构建与验证

先执行 `01-global-engineering-rules.md#跨技术栈验证策略`，再选择 Maven 落地命令。

按风险选择最小充分验证：

- 默认验收以编译或构建通过为准，不默认跑接口、集成测试、外部系统联调或手工 API 操作。
- 只改一个类或方法：优先跑目标模块 `compile` 或 `package -DskipTests`。
- 改 Service、DAO、Mapper、DTO 映射：跑相关模块编译或构建。
- 改跨模块调用链：从 root 用 `-pl <module> -am` 编译或构建相关模块。
- 改公共契约、枚举、配置、SQL：增加调用方模块编译或构建验证。
- 只有当前任务目标是测试修复、需要复现 bug，或编译/语法无法覆盖原始问题、根因或调用链关键风险时，才跑目标单测、模块测试或集成测试。

常用命令：

```bash
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am compile
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am -DskipTests package
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am test
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am -Dtest=ClassNameTest test
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
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

## Maven 失败处理

- 依赖缺失时先确认本次使用的 `maven.localRepository` 是否来自缓存、IDE 配置或项目配置。
- Maven 版本不一致时先确认本次使用的 `maven.executable` 是否已验证并缓存。
- JDK、`release/source/target`、toolchain 或 Maven Wrapper 不匹配时，必须按 `14-environment-cache-by-stack.md#mavenjava-环境缓存` 重新读取 `pom.xml`、`.mvn/*`、wrapper、IDE 配置和本机 JDK/Maven 候选，更新缓存后用同一目标命令重试一次。
- 多模块找不到依赖时确认是否加了 `-am`。
- 指定测试不存在或跨模块时可加 `-Dsurefire.failIfNoSpecifiedTests=false`。
- 构建失败后先区分是本次改动、历史失败、依赖环境还是测试选择错误，不连续盲改。
