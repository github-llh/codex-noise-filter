# Maven 与后端构建

## 本地 Maven 环境

用户 Maven 发行版路径：

```bash
/Users/lilinhan/dev/maven-3.9.10
```

优先使用的 Maven 可执行文件：

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn
```

用户本地 Maven repository 路径：

```bash
/Users/lilinhan/maven-git
```

构建 Java/Maven 项目时，优先使用：

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git
```

命令选择顺序：

1. 如果项目已配置 Maven Wrapper 且项目规则要求使用 Wrapper，优先使用项目内 `./mvnw`。
2. 否则优先使用 `/Users/lilinhan/dev/maven-3.9.10/bin/mvn`。
3. 只有上述路径不可用时，才退回系统 `mvn`。

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

## Maven 失败处理

- 依赖缺失时先确认是否使用了 `/Users/lilinhan/maven-git`。
- Maven 版本不一致时先确认是否使用了 `/Users/lilinhan/dev/maven-3.9.10/bin/mvn`。
- 多模块找不到依赖时确认是否加了 `-am`。
- 指定测试不存在或跨模块时可加 `-Dsurefire.failIfNoSpecifiedTests=false`。
- 构建失败后先区分是本次改动、历史失败、依赖环境还是测试选择错误，不连续盲改。
