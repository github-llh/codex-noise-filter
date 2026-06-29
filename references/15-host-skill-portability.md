# 第三方宿主 Skill 兼容与执行顺序

本文件用于处理 Codex 之外的 agent、CLI、IDE、App、workflow、rules、hooks、subagent、MCP/ACP、模型路由和未知 wrapper。目标不是维护平台白名单，而是把不同宿主归一为能力类型，再按同一套触发、加载、执行和验证顺序推进。

## 官方资料归纳

已核对的官方资料显示，宿主能力大致分为五类：

资料来源：

- OpenAI Codex Agent Skills：`https://developers.openai.com/codex/skills`
- Claude Code Skills：`https://code.claude.com/docs/en/skills`
- OpenCode Skills：`https://opencode.ai/docs/skills/`
- Roo Code Skills / Custom Instructions：`https://docs.roocode.com/features/skills`、`https://docs.roocode.com/features/custom-instructions`
- MiMo Code Skills / Rules：`https://mimo.xiaomi.com/mimocode/skills`、`https://mimo.xiaomi.com/mimocode/rules`
- Gemini CLI Agent Skills / Commands：`https://geminicli.com/docs/cli/skills/`、`https://geminicli.com/docs/reference/commands/`
- VS Code Agent Skills：`https://code.visualstudio.com/docs/agent-customization/agent-skills`
- Cursor Rules：`https://cursor.com/docs/rules`
- Cline Rules：`https://docs.cline.bot/customization/cline-rules`
- Continue Rules / MCP：`https://docs.continue.dev/customize/deep-dives/rules`、`https://docs.continue.dev/customize/deep-dives/mcp`
- GitHub Copilot custom instructions：`https://docs.github.com/copilot/how-tos/configure-custom-instructions/add-repository-instructions`
- Windsurf/Cascade Rules / MCP / Workflows：`https://docs.windsurf.com/llms-full.txt`
- aider repo map / read-only context：`https://aider.chat/docs/repomap.html`、`https://aider.chat/docs/faq.html`
- AGENTS.md spec：`https://agents.md/`

| 能力类型 | 代表宿主或机制 | 当前可确认行为 | 本 skill 的处理方式 |
| --- | --- | --- | --- |
| 原生 Agent Skills | Codex、Claude Code、Gemini CLI、OpenCode、MiMo Code、Roo Code、VS Code/GitHub Copilot Agent Skills | 通过 `SKILL.md`、`name`、`description`、可用 skill 列表、`skill` tool、`activate_skill`、自动目录扫描或等价机制按需加载完整内容 | 标记 `nativeSkill`，先加载 `SKILL.md`，再读 `references/00-index.md` |
| Slash command / workflow | Claude Code `/skill-name`、Gemini CLI custom commands、Roo Code slash commands、Windsurf/Cascade Workflows、MiMo Code commands | 命令或 workflow 是显式调用入口，可能不等同于完整 Agent Skills discovery | 标记 `nativeCommand`；若可读文件，继续执行 Skill Bootstrap；不可读时转 `fallbackOnly` |
| 持久规则 / instruction 文件 | `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、Cline Rules、Cursor Rules、Windsurf Rules、Roo Code custom instructions、Continue Rules、Copilot custom instructions、aider `/read` 或 `.aider.conf.yml` 读取的规则文件 | 多数是持续注入或按路径匹配的提示规则，不代表完整 skill 已加载 | 标记 `rulesOnly`；只作为触发与 bootstrap 指令，不能声称已加载 skill |
| Agent / subagent / hook / MCP / ACP | 子代理、hook、MCP tool、IDE 工具、CI/chatops、模型路由、provider switch | 常用于工具执行、隔离上下文或生命周期注入，输出可能是摘要或工具结果 | 标记 `delegatedTool`；只把输出当证据，必须回到当前文件、diff、环境和验证 |
| 无 discovery 且不可读文件 | 受限第三方、只传入一段结果或无法访问分发目录的 wrapper | 只能得到 AGENTS 兜底或转发载荷，无法读取完整 skill | 标记 `fallbackOnly`；执行第三方兜底闭环，不伪装成 skill 已加载 |

平台名只用于识别能力类型。若新平台支持 `SKILL.md`、`skills/`、skill tool、slash command、rules、workflow、subagent 或 MCP 中任一机制，按能力类型处理；若资料不足，按当前宿主暴露的文件、命令、工具和载荷证据处理。

## 运行时现实边界

跨宿主迁移时，先区分“规则已注入”和“运行时会自动执行”：

- `rulesOnly` 只能证明规则文本被宿主看到，不能证明 `SKILL.md`、references、hook、MCP 或 command 已加载。
- `hook` 是否能阻止命令、修改参数或注入提醒，取决于当前宿主是否支持生命周期 hook、是否已注册、matcher 是否命中和权限是否允许；没有这些证据时，只能写成规则门禁，不能承诺自动拦截。
- Codex、第三方 IDE、CLI、App 和网页宿主的 hook parity 不一致；不能把某个宿主的 hook 行为迁移成所有宿主的保证。
- MCP/ACP、subagent、CI、chatops 和路由器输出只算证据或工具结果；必须回到当前文件、diff、环境缓存和验证命令复核。
- commands/workflows 可以作为入口或 shim，但本 skill 的 canonical source 仍是 `SKILL.md` + `references/00-index.md` + 命中的 references。
- 外部仓库、插件、hook 脚本、rules、skills、commands、MCP 配置和 prompt file 都按 `17-agentic-security-and-supply-chain.md` 做供应链边界；不要直接复制外部运行时实现。
- 安装、分发、manifest、marketplace、README/templates 或加载故障按 `19-installation-health-and-surface-audit.md` 做 surface audit；不要用平台名替代实际加载证据。

## 常见宿主目录提示

这些路径只用于安装建议和手动 bootstrap 的候选，不是触发白名单；宿主官方文档或用户配置给出更具体路径时，以当前宿主事实为准。

| 宿主 | 原生 skill 或规则候选 |
| --- | --- |
| Codex | `<repo>/.agents/skills/<name>/SKILL.md`、`$HOME/.agents/skills/<name>/SKILL.md`、`CODEX_HOME` 下的 Codex skill 目录 |
| Claude Code | `<repo>/.claude/skills/<name>/SKILL.md`、`$HOME/.claude/skills/<name>/SKILL.md`、`.claude/commands/*.md` |
| Gemini CLI | `<repo>/.agents/skills/<name>/SKILL.md`、`<repo>/.gemini/skills/<name>/SKILL.md`、`$HOME/.agents/skills/<name>/SKILL.md`、`$HOME/.gemini/skills/<name>/SKILL.md`、`GEMINI.md` |
| OpenCode / MiMo Code | `.agents/skills/<name>/SKILL.md`、宿主自身配置目录下的 `skills/<name>/SKILL.md`、`AGENTS.md` 或宿主 rules |
| Roo Code | `<repo>/.roo/skills/<name>/SKILL.md`、`<repo>/.agents/skills/<name>/SKILL.md`、`$HOME/.roo/skills/<name>/SKILL.md`、`$HOME/.agents/skills/<name>/SKILL.md`，以及 `.roo/skills-{mode}/` / `.agents/skills-{mode}/` |
| Cline / Cursor / Windsurf / Continue / Copilot / aider | 多数先作为 `rulesOnly` 或 `delegatedTool` 处理；若宿主另行支持 Agent Skills 或可读分发目录，再转 `manualFileBootstrap` 或 `nativeSkill` |

## 跨宿主执行顺序

所有宿主都按以下顺序推进，不能按平台名跳步：

1. **入口恢复**：记录当前宿主、cwd/workspace、Git root、用户原始意图、转发载荷、目标文件、命令、日志、diff、工具动作、模型/供应商和路由层。
2. **任务触发判定**：先看任务证据，不看平台名称。命中代码读取、修改、构建、测试、lint、format、typecheck、调试、重构、配置、路径、报错、diff、编码/乱码或验证链路，即按编程任务触发。
3. **宿主能力探测**：先用宿主已暴露的可用 skill 列表、`skill` tool 描述、slash command、workflow 列表、rules 面板、配置文件或 AGENTS 注入状态；不要为了“全平台兼容”深扫整机。
4. **加载状态判定**：
   - `nativeSkill`：可用 skill 列表或 skill tool 中能看到 `codex-noise-filter`，并已读取本轮 `SKILL.md`。
   - `nativeCommand`：当前通过 `/skill-name`、custom command 或 workflow 显式进入，但宿主未证明完整 Agent Skills 已加载。
   - `manualFileBootstrap`：宿主没有 native skill discovery，或只有 rules/commands/workflow，但允许读取分发目录中的 `SKILL.md`。
   - `rulesOnly`：只注入 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.clinerules`、`.cursor/rules`、`.windsurf` 或 Copilot instructions，尚未读取完整 skill。
   - `fallbackOnly`：既不能发现 skill，也不能读取 `SKILL.md` 和 references。
5. **最小加载**：
   - `nativeSkill`：读取 `SKILL.md` -> `references/00-index.md` -> 仅打开命中的 reference。
   - `nativeCommand`：先读取命令/workflow 当前内容；若可读文件，再按 Skill Bootstrap 读取 `SKILL.md` 和 `00-index.md`。
   - `manualFileBootstrap` / `rulesOnly`：按宿主配置目录、AGENTS 目录、项目级 `.agents/skills`、宿主原生目录、用户级 `.agents`、`CODEX_HOME` 和兼容 `.codex` 的顺序查找首个存在的 `SKILL.md`，读取成功后立即停止查找。
   - `fallbackOnly`：不再查找平台清单，直接执行第三方兜底闭环。
6. **内部状态机**：建立 `activated/loadState/hostCapability/references/dynamicScope/capsule/scope/callChain/localAlignment/environment/securityBoundary/surfaceHealth/qualityGate/validation`，后续工具调用、写入、验证和最终回复前都自检。
7. **动态追加范围**：根据触碰文件、最近配置、命令、错误、diff、active cache path、本机环境、外部内容、供应链表面和分发状态追加 `01`、`02`、`06`、`14`、`17`、`18`、`19` 和命中的技术栈 reference。
8. **最小执行与验证**：只做当前触碰范围的最小闭环；第三方“已验证/已修改”必须用当前 root、diff、active cache path、命令和触碰范围复核，并按 `18` 记录验证矩阵。

## 触发条件

以下任一条件成立即触发本 skill 或兜底闭环：

- 显式调用：`$codex-noise-filter`、`/codex-noise-filter`、`skill({ name: "codex-noise-filter" })` 或同等宿主选择器。
- 隐式匹配：宿主可用 skill 列表中的 `description` 与编程任务、代码证据、构建/测试、调用链、环境缓存、验证或上下文恢复匹配。
- Rules/AGENTS 触发：规则文件声明编程任务默认启用本 skill，且当前载荷包含代码、路径、命令、日志、diff、项目结构、工具链动作或上下文恢复信号。
- Command/workflow 触发：custom command、workflow、prompt file 或 task runner 的内容要求读取、修改、验证代码，或要求调用本 skill。
- 转发载荷触发：来自第三方 agent、subagent、MCP/ACP、hook、CI/chatops、model router、provider switch、gateway/proxy/adapter 的载荷带有 cwd、文件、命令、日志、diff、patch、构建/测试/lint/typecheck 输出、截图错误或工具动作。
- 恢复触发：上下文压缩、窗口切换、模型切换、自动续跑、工具超时、网络断开、上一轮 Capsule、规则争议或当前工作区 skill/reference 变化。
- 安全与供应链触发：外部仓库、网页、issue/PR、PDF、邮件、模型输出、MCP/ACP、hook、rules、skills、commands、plugin manifest、凭证、权限、外发、hidden unicode、base64 或 prompt/tool/memory poisoning 风险。
- 安装健康触发：skill 不生效、hook 不触发、commands 找不到、rulesOnly/manualFileBootstrap/fallbackOnly、README/templates/AGENTS/manifest/marketplace 同步、插件缓存或分发产物引用漂移。

不触发：纯生活对话、无代码上下文的一般知识问答、无法从当前仓库/转发载荷/历史任务恢复编程目标的空泛指令。

## 性能强化

性能优化不能降低触发准确度；只能减少无关读取和无效输出。

- **先读能力描述，不读全量文件**：优先使用宿主的 skill 列表、tool description、command/workflow 元数据、rules 面板或配置路径；只有命中本 skill 后才读完整 `SKILL.md`。
- **路径探测有上限**：手动 bootstrap 只检查当前宿主配置目录、AGENTS 目录、当前工作区、用户级兼容目录和 `CODEX_HOME`。命中首个有效 `SKILL.md` 后停止；除非宿主官方支持递归 discovery，不手写全盘递归扫描。
- **索引优先**：完整 `SKILL.md` 后只读 `references/00-index.md`，默认追加 1 个主 reference；需要构建/运行时再加 `06` + `14`，需要恢复/交付时再加 `05`。
- **证据优先于平台名**：不因为平台名出现在清单里就打开平台专属规则；只有载荷证据决定技术栈、工具链和验证范围。
- **状态缓存写入 Capsule**：同一任务内记录 `hostCapability`、`loadState`、已读 `SKILL.md` 路径、已读 reference 和未读边界；恢复后先复用并用当前文件/diff 校验。
- **大输出只摘要**：日志、搜索结果、子代理报告、CI 输出和第三方包装层长叙述只保留命令、关键错误、路径/行号、退出码、结论和下一步。
- **subagent 用于读多写少**：探索、日志归因、测试输出汇总可交给 subagent；写多、跨文件修改、公共契约和验证结论必须回到主上下文复核。
- **避免模板复制膨胀**：AGENTS、rules、workflow 和 README 只放 bootstrap 和兜底矩阵；完整细则保留在本 skill 的 references 中。

## 接入验收矩阵

团队给第三方宿主接入本 skill 后，用以下最小矩阵验收：

| 场景 | 预期状态 |
| --- | --- |
| 原生 Agent Skills 宿主能看到 `codex-noise-filter` | `nativeSkill`，读取 `SKILL.md` 和 `00-index.md` |
| 只导入 AGENTS 但能读文件 | `manualFileBootstrap`，读取首个存在的 `SKILL.md` 和同目录 `00-index.md` |
| 只有 rules/custom instructions | `rulesOnly` 触发，随后尝试 manual bootstrap；失败才 `fallbackOnly` |
| custom command/workflow 调用 | `nativeCommand`，按命令内容恢复任务，再尝试读取完整 skill |
| subagent/hook/MCP/CI 转发结果 | `delegatedTool`，输出只作证据，必须复核当前文件、diff、环境和验证 |
| 无文件读取能力 | `fallbackOnly`，执行第三方兜底闭环，并明确不是自动加载成功 |
| hook/rules/commands 声称可执行规则 | 先证明宿主支持、已注册、matcher 命中和当前任务可见；否则只作为 `rulesOnly` 或 `nativeCommand` 入口 |
| skill/plugin 分发或加载故障 | 按 `19` 检查 canonical skill、索引、模板、manifest、marketplace、缓存副本、reload/restart 需求 |
| 外部体系迁移 | 按 `17` 做供应链边界，只迁移可验证制度能力，不搬运不受当前宿主支持的 runtime |

若验收失败，先定位失败类别：未发现 skill、description 不匹配、同名 skill 冲突、权限 deny/hidden、rules 只注入未读取文件、工作目录错误、配置路径错误、缓存旧版本、宿主需要 reload/restart。不要通过扩大平台白名单解决。
