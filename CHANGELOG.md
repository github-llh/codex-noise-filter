# Changelog

## 3.2.0 - 2026-07-17

### 受控子智能体委派

- 新增一次性工作量判断：只有至少两个独立、非琐碎、可验收通道，且并行或上下文隔离收益高于协调与总 token 成本时才最小委派。
- 主智能体保持唯一调度权；子智能体严格单层、默认只读、不得再派生，也不得与主智能体或其他子智能体重复搜索和抢写同一范围。
- 增加有界派发、一次补充追问和明确停止条件，避免 skill 与模型重复调度、主从来回改写、无新证据重启相同角色等循环。
- 外部调研优先官方/一手资料；只在来源族或问题确实独立且资料量足够时并行，不让多个 agent 重复浏览同一页面。

### 设计依据

- 对齐 Codex Subagents 对独立读密集通道、写冲突、额外 token 消耗和默认单层嵌套的说明。
- 参考 Anthropic 多智能体研究系统与 Building Effective Agents 的主从编排、协调成本和“简单方案优先”原则；不硬编码第三方 token 倍数。

## 3.1.0 - 2026-07-15

### 上下文管理补强

- `PreCompact` 在自动或手动压缩前可靠标记待恢复状态；`SessionStart(compact)` 或下一次 `UserPromptSubmit` 再按 Codex 支持的输出协议注入结构化连续性账本。
- `PostCompact` 用“压缩已完成”替换过期的“即将压缩”；恢复原因消费后立即清除，网络失败的幂等性复核只注入一次。
- 宿主省略 `model` 或 `cwd` 时不再用空值擦除最近状态；v1 状态自动迁移到 v2 并保留已知待恢复原因。
- 状态新增有界事件与上下文注入计数、最近注入事件/类型/原因；未知或被篡改的原因会被丢弃，不能进入开发者上下文。
- 工具响应改为 32 KiB 流式有界扫描，并限制递归深度与集合项数，避免大输出先完整序列化或异常嵌套拖慢 Hook。
- 回归测试由 6 项扩展到 12 项，增加压缩恢复账本、原因去重、缺失元数据、状态迁移、注入计数和异常状态防护。

### 设计依据

- 对齐 Codex 官方 Hook 事件、信任、matcher、`PLUGIN_DATA` 和输出协议。
- 参考 Claude Code 的恢复刷新与最小上下文注入、GitHub Copilot 的事件审计与超时边界、OpenCode 的压缩账本字段；不复制第三方脚本或 prompt，也不迁移 Codex 当前不支持的 compaction prompt 改写。

## 3.0.0 - 2026-07-14

### 自动连续性保护

- 新增 Plugin 内置 `PreCompact`、`PostCompact`、`SessionStart`、`UserPromptSubmit` 和 `PostToolUse` Hook，对上下文压缩、会话恢复/重新连接、模型变化、工作目录变化和网络/传输失败自动触发复核。
- Hook 只在 `PLUGIN_DATA` 保存不可逆会话/目录指纹、模型、事件和恢复原因，不读取不稳定 transcript，不复制 prompt、工具原始输出、日志、凭证或客户数据。
- 网络失败后先检查操作是否已产生副作用，再决定查询、幂等重试、补偿或停止，避免因断线盲目重复写操作。
- 重写连续性 reference，把检查点从固定频率改为目标、约束、证据、写入和验证状态发生变化时按语义更新。

### 分发与验证

- Plugin 版本升级到 `3.0.0`，由 manifest 显式声明 `hooks/hooks.json`，构建产物包含 Hook 配置与标准库脚本。
- Marketplace manifest 按 Codex 官方目录约定生成到 `.agents/plugins/marketplace.json`，修复 `marketplace root does not contain a supported manifest`。
- 验证器新增 Hook 事件、相对路径、`PLUGIN_ROOT`、Windows 命令和超时边界校验。
- 新增标准库回归测试，覆盖自动压缩恢复、会话恢复、模型切换、网络失败和成功日志防误触发。
- 保留 Codex 对非托管命令 Hook 的首次信任要求；Hook 被禁用、managed-only 策略跳过或宿主不支持时退回 Skill 指令级恢复。

## 2.0.0 - 2026-07-10

### 重大重构

- 把 20 份相互重叠的 reference 收敛为 11 个按职责路由的主题文件，所有 reference 由 `SKILL.md` 直接链接并控制在 100 行以内。
- 重写 `SKILL.md` description，前置真实触发边界并明确纯知识问答、翻译和无仓库泛泛建议不触发。
- 将工作流统一为回答、诊断、审查、实施四种模式，避免只读请求被自动升级为写入。
- 把根因与调用链改为风险分级：简单问题停在完整语义单元，模块/系统风险才扩展链路。
- 全语言统一新增/修改注释使用简体中文的规则，并补齐 Java、Python、Vue/React/TypeScript、小程序、Shell/CI、SQL、配置与 agent/plugin 表面的去魔法值策略。

### 去除反作用规则

- 删除每次工具调用前强制 Guard Loop、全字段状态机和固定频率 Capsule。
- 删除构建验证前强制创建或迁移 `.codex/local-environment*.json` 的副作用。
- 删除读取到旁支问题就自动修改、强制补注释和强制抽象的范围扩张规则。
- 删除第三方宿主目录猜测和无法由 skill 自身保证的自动 hook 承诺。

### 分发与验证

- Plugin 版本升级到 `2.0.0`，移除空 `screenshots` 等无效元数据，不声明 hook、MCP 或 app。
- 构建脚本改为生成完整 local marketplace root，并只打包运行时必需的 skill 文件。
- 新增标准库验证器，检查 frontmatter、reference 直链、本地链接、不可见方向字符、SemVer、manifest 和 marketplace 路径。
- 精简 `.gitignore`，删除 Java/IDE 模板遗留规则和错误的 `.proxyaidistribution` 条目。

## 1.0.1 - 2026-06-14

- 补充使用说明、Apache-2.0 协议与多技术栈 reference。
- 建立 Maven/Java、Python、Vue/React、小程序、并发与环境发现规则。

## 1.0.0 - 2026-06-14

- 建立 `SKILL.md`、`references/00-index.md` 和分主题 reference 的初始结构。
- 支持编程任务意图识别、调用链检查、局部工程规则与最小验证。
