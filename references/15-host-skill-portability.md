# 第三方宿主 Skill 兼容与执行顺序

本文件用于处理 Codex 之外的 agent、CLI、IDE、App、workflow、rules、hooks、subagent、MCP/ACP、模型路由和未知 wrapper。目标不是维护平台白名单，而是把不同宿主归一为能力类型，再按同一套触发、加载、执行和验证顺序推进。

## 官方资料归纳

已核对的官方资料显示，宿主能力大致分为五类：

资料来源：

- OpenAI Codex Agent Skills：`https://developers.openai.com/codex/skills`
- Claude Code Skills：`https://code.claude.com/docs/en/skills`
- OpenCode Skills：`https://opencode.ai/docs/skills/`
- MiMo Code Skills / Rules：`https://mimo.xiaomi.com/mimocode/skills`、`https://mimo.xiaomi.com/mimocode/rules`
- Gemini CLI Agent Skills / Commands：`https://geminicli.com/docs/cli/skills/`、`https://geminicli.com/docs/reference/commands/`
- VS Code Agent Skills：`https://code.visualstudio.com/docs/agent-customization/agent-skills`
- Cline Rules：`https://docs.cline.bot/customization/cline-rules`
- GitHub Copilot custom instructions：`https://docs.github.com/copilot/how-tos/configure-custom-instructions/add-repository-instructions`
- Windsurf/Cascade Workflows：`https://docs.devin.ai/workflows`
- AGENTS.md spec：`https://agents.md/`

| 能力类型 | 代表宿主或机制 | 当前可确认行为 | 本 skill 的处理方式 |
| --- | --- | --- | --- |
| 原生 Agent Skills | Codex、Claude Code、Gemini CLI、OpenCode、MiMo Code、VS Code/GitHub Copilot Agent Skills | 通过 `SKILL.md`、`name`、`description`、可用 skill 列表、`skill` tool 或 `activate_skill` 按需加载完整内容 | 标记 `nativeSkill`，先加载 `SKILL.md`，再读 `references/00-index.md` |
| Slash command / workflow | Claude Code `/skill-name`、Gemini CLI custom commands、Windsurf/Cascade Workflows、MiMo Code commands | 命令或 workflow 是显式调用入口，可能不等同于完整 Agent Skills discovery | 标记 `nativeCommand`；若可读文件，继续执行 Skill Bootstrap；不可读时转 `fallbackOnly` |
| 持久规则 / instruction 文件 | `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、Cline Rules、Cursor Rules、Windsurf Rules、Copilot custom instructions | 多数是持续注入或按路径匹配的提示规则，不代表完整 skill 已加载 | 标记 `rulesOnly`；只作为触发与 bootstrap 指令，不能声称已加载 skill |
| Agent / subagent / hook / MCP / ACP | 子代理、hook、MCP tool、IDE 工具、CI/chatops、模型路由、provider switch | 常用于工具执行、隔离上下文或生命周期注入，输出可能是摘要或工具结果 | 标记 `delegatedTool`；只把输出当证据，必须回到当前文件、diff、环境和验证 |
| 无 discovery 且不可读文件 | 受限第三方、只传入一段结果或无法访问分发目录的 wrapper | 只能得到 AGENTS 兜底或转发载荷，无法读取完整 skill | 标记 `fallbackOnly`；执行第三方兜底闭环，不伪装成 skill 已加载 |

平台名只用于识别能力类型。若新平台支持 `SKILL.md`、`skills/`、skill tool、slash command、rules、workflow、subagent 或 MCP 中任一机制，按能力类型处理；若资料不足，按当前宿主暴露的文件、命令、工具和载荷证据处理。

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
   - `manualFileBootstrap` / `rulesOnly`：按宿主配置目录、AGENTS 目录、项目级 `.agents/skills`、兼容 `.claude/.codex/.opencode/.mimocode`、用户级 `.agents`、`CODEX_HOME` 的顺序查找首个存在的 `SKILL.md`，读取成功后立即停止查找。
   - `fallbackOnly`：不再查找平台清单，直接执行第三方兜底闭环。
6. **内部状态机**：建立 `activated/loadState/hostCapability/references/dynamicScope/capsule/scope/callChain/localAlignment/environment/validation`，后续工具调用、写入、验证和最终回复前都自检。
7. **动态追加范围**：根据触碰文件、最近配置、命令、错误、diff、active cache path 和本机环境追加 `01`、`02`、`06`、`14` 和命中的技术栈 reference。
8. **最小执行与验证**：只做当前触碰范围的最小闭环；第三方“已验证/已修改”必须用当前 root、diff、active cache path、命令和触碰范围复核。

## 触发条件

以下任一条件成立即触发本 skill 或兜底闭环：

- 显式调用：`$codex-noise-filter`、`/codex-noise-filter`、`skill({ name: "codex-noise-filter" })` 或同等宿主选择器。
- 隐式匹配：宿主可用 skill 列表中的 `description` 与编程任务、代码证据、构建/测试、调用链、环境缓存、验证或上下文恢复匹配。
- Rules/AGENTS 触发：规则文件声明编程任务默认启用本 skill，且当前载荷包含代码、路径、命令、日志、diff、项目结构、工具链动作或上下文恢复信号。
- Command/workflow 触发：custom command、workflow、prompt file 或 task runner 的内容要求读取、修改、验证代码，或要求调用本 skill。
- 转发载荷触发：来自第三方 agent、subagent、MCP/ACP、hook、CI/chatops、model router、provider switch、gateway/proxy/adapter 的载荷带有 cwd、文件、命令、日志、diff、patch、构建/测试/lint/typecheck 输出、截图错误或工具动作。
- 恢复触发：上下文压缩、窗口切换、模型切换、自动续跑、工具超时、网络断开、上一轮 Capsule、规则争议或当前工作区 skill/reference 变化。

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

若验收失败，先定位失败类别：未发现 skill、description 不匹配、同名 skill 冲突、权限 deny/hidden、rules 只注入未读取文件、工作目录错误、配置路径错误、缓存旧版本、宿主需要 reload/restart。不要通过扩大平台白名单解决。
