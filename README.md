# codex-noise-filter

编程任务专用的 Codex skill，用于减少无效上下文、强制调用链确认，并把全局工程规则沉淀到 skill 内，避免切换会话或窗口时遗漏规则。

## 中文说明

### 适用场景

- 编写、修改、调试、排查、重构、迁移、解释代码。
- 多文件排查、跨模块调用链分析、后端构建、前端页面修复。
- 用户要求减少 token、压缩噪音、简洁可追溯或可复盘。

### 结构

```text
SKILL.md
references/
  00-index.md
  01-global-engineering-rules.md
  02-noise-filter-workflow.md
  03-maven-backend-build.md
  04-frontend-rules.md
  05-delivery-templates.md
  06-environment-discovery.md
```

`SKILL.md` 只保留触发、路由和硬约束；执行细则按索引进入对应文件，减少主文件负担。

### 内置重点

- 默认简体中文回复。
- JetBrains 项目优先使用 JetBrains MCP / IDE 工具。
- 修改前确认目标文件、根因、最小方案和不影响范围。
- 修改前必须完成调用链和影响面确认。
- Maven 后端项目优先读取 `.codex/local-environment.json`、IDE/项目配置和已验证本机候选路径。
- 当前已验证 Maven 候选为 `/Users/lilinhan/dev/maven-3.9.10/bin/mvn`，本地仓库候选为 `/Users/lilinhan/maven-git`。
- 多模块 Maven 项目默认从聚合 root 节点执行，并使用 `-pl <module> -am`。
- 新建文件前必须确认 module、层级职责、包路径、同类文件位置和依赖方向，尤其注意接口、实现、实体、契约可能分属不同 module。
- 明确固定集合的状态、类型、来源、动作、阶段、结果等值优先写成业务 Enum，避免魔法字符串和数字散落。
- Java 后端 Controller 保持轻薄，不写业务代码；业务契约放 Service 接口，业务流程放 Service 实现。
- Service 接口和重要实现方法要有原因型注释，做到不冗余、不缺失、不杂乱。
- 前端优先修布局、组件属性和状态契约，不用硬编码掩盖后端问题。
- 编程任务规则已内化到 skill；全局 `/Users/lilinhan/.codex/AGENTS.md` 仍建议保留为兜底。
- 长任务、切换窗口或上下文压缩前，使用 Context Capsule 保留目标、证据、已改、回滚和下一步。

### Maven 示例

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am test
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -DskipTests package
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
```

### 环境发现

- 首次使用 Maven、JDK、Node 或包管理器时，先读 IDE/项目配置。
- 如果配置中拿不到路径，再查找本机常见候选路径。
- 找到后必须执行最小验证，例如 `mvn -version`。
- 验证通过后写入 `.codex/local-environment.json`，后续优先复用缓存。
- 缓存失效或项目配置显式变化时，重新发现并更新缓存。

### Codex 上下文管理

- 主文件只负责触发和路由，细则通过 `references/00-index.md` 渐进读取。
- 长任务按“任务胶囊 -> 调用链确认 -> 最小修改 -> 轻量验证 -> Context Capsule”执行。
- 切换窗口或上下文压缩前输出 Context Capsule，避免丢失目标、证据、回滚点和下一步。
- 用户中途插入新目标时，先判断与主任务关系，不默认重置已有调用链。
- 全局 `AGENTS.md` 不需要承载全部细则，但建议保留为兜底入口。
- 长期 memory 只记录稳定偏好和跨任务规则；临时日志、一次性失败和未验证猜测不写入长期记忆。

英文说明见 [README.en.md](README.en.md)。
