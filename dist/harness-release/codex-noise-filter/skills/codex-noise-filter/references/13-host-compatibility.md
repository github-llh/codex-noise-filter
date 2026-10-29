# 宿主适配与触发诊断

规则核心与模型无关。模型供应商负责推理与 API；宿主负责加载规则、工具、插件和 hooks。不要根据模型名称推断宿主能力。以下依据 2026-10-12 复核的官方文档；在线文档可能继续变化。

## 选择入口

| 实际宿主/表面 | 本项目入口 | 支持边界 |
| --- | --- | --- |
| Codex CLI、IDE、支持本地插件的桌面工作任务 | Codex plugin，或 `.agents/skills` + `AGENTS.md` | hooks 需安装、启用、信任且当前执行环境支持 |
| Claude Code CLI、Desktop 本地/SSH Code 会话 | Claude plugin，或 `.claude/skills` + `CLAUDE.md` | Desktop 远程会话的插件支持需另查；不能套用 Chat 的能力 |
| Claude Chat（网页/桌面）、Cowork | Claude plugin ZIP 或 Skill ZIP | 官方说明 Chat 仅使用插件 skills；hooks、subagents 在 Cowork 等支持表面执行 |
| DeepSeek 经 Codex/Claude Code | 按所用宿主选择上述包 | 官方提供 Responses/Anthropic 接入；不改本项目来绑定某个模型名 |
| DeepSeek Harness Desktop / CLI / Web | `harness` 原生 Cordis bundle，或 `.dsh/skills` 标准技能 | Desktop 独立安装与启用；使用原生技能注册和上下文快照，不复制 Codex hooks |
| Deep Code（DeepSeek 官方接入指南所列第三方工具） | Skill 包放 `.deepcode/skills` 或 `~/.agents/skills` | 文档确认 Agent Skills；不据此声明支持本项目 hooks |
| MiMo 经 Codex/Claude Code | 按宿主选择上述包 | 官方提供 Responses/Anthropic 配置；保留用户 model、thinking、effort |
| Cursor 桌面 Agent / CLI | `.cursor/skills` + `.cursor/rules/*.mdc` 项目包 | 共享 Agent Skills；云端与远程需要实际工作区内技能 |
| Gemini CLI | `.gemini/skills` + `GEMINI.md` 项目包 | 原生 activate_skill，遵守宿主激活确认 |
| OpenCode 桌面 / CLI / Web | `.opencode/skills` + `AGENTS.md` 项目包 | 使用技能发现和项目指导；本包不注册 OpenCode JS hooks |
| GitHub Copilot App / CLI / IDE Agent | `.github/skills` + `.github/copilot-instructions.md` 项目包 | 以具体产品支持的自定义指令和 skill 能力为准 |
| 其他 Agent Skills 宿主 | 标准 Skill ZIP；按宿主官方路径部署 | 没有核对 schema 时不复制 Codex/Claude hooks |
| 支持 Agent Plugins 规范的宿主 | portable plugin ZIP（根 `plugin.json`） | 仅 skills；不附加厂商私有 hooks |
| MiMo Desktop、MiMo Code、MiMo/DeepSeek 普通聊天 App | 用户主动配置项目/自定义指令，或每次粘贴聊天模板 | MiMo 桌面官方页确认 Beta macOS/Windows 与自定义模型，但未公布此插件加载契约；按实际 UI 入口配置，不保证后台触发 |

## 规则文件与 agents

- Codex 从全局及项目路径发现 `AGENTS.md`，同层先选 `AGENTS.override.md`；更深目录规则覆盖上层。遇到未触发先查有效规则、cwd 和长度限制，不自动改全局配置。
- Claude Code 读取 `CLAUDE.md`，不自动读取 `AGENTS.md`。已有共同规则时可在 `CLAUDE.md` 使用 `@AGENTS.md`，但只在实际授权的项目内配置。
- `AGENTS.md`、Claude `agents/*.md`、Skill 内 `agents/openai.yaml` 是三个不同用途：项目指导、子代理定义、Codex UI 元数据。文件名相似不代表可互换。
- 本项目不预设子代理模型、不新增自主工作代理。委派继续遵循 `12` 的单层、有界与用户授权约束。

## 触发与恢复

- description 提供语义发现；显式调用与项目指导补充入口。插件 `SessionStart` 在 startup/resume/clear/compact 时注入短路由；`UserPromptSubmit` 只在会话尚未注入路由或存在待恢复原因时输出。hook 注入的 `additionalContext` 会留在会话记录中，按轮重复注入会持续累积上下文，两家官方文档都提示多来源 hook 上下文会叠加。
- 路由送达不等于模型已读取规则。用真实请求、实际 skill 读取动作和宿主 hook 日志区分安装、执行、遵循三个阶段。
- `PreCompact`/`PostCompact` 只记恢复标记；在 `SessionStart`、下一条 prompt 或工具完成事件中输出合法 `additionalContext`。不向不支持上下文的事件伪造输出。
- Codex 的失败工具结果在 `PostToolUse` 检查；Claude 只注册 `PostToolUseFailure` 并读取其 `error` 字段，不注册 `PostToolUse`。Claude 仅 `SessionStart` 可能携带 `model`，会话中途的模型切换依赖指令级复核。
- Skill 正文被调用后会在会话内保留；Claude Code 压缩后只重新附带每个 skill 最近一次调用的前 5,000 token，因此关键规则放在 `SKILL.md` 顶部。模型字段缺失时无法自动检测模型切换，使用指令级复核。
- 脚本只依赖 Python 3.10+ 标准库。Codex 使用 `PLUGIN_ROOT`/`PLUGIN_DATA`，Claude 使用 `CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA`。缺失私有数据目录时无状态运行，不猜测 home 路径。
- 普通工具成功时不写状态、不扫描历史目录；会话建档才清理历史状态。事件计数只记录状态处理，不代表全部工具次数，也不证明模型遵循了上下文。
- 输入扫描预算只限制守卫自身工作量，不截断、替换模型收到的原始工具结果。范围外失败可能未被守卫识别，模型仍需按原始证据处理。

## 官方来源

- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[Skills](https://learn.chatgpt.com/docs/build-skills)、[Hooks](https://learn.chatgpt.com/docs/hooks)、[Plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Claude memory](https://code.claude.com/docs/en/memory)、[Skills](https://code.claude.com/docs/en/skills)、[Plugins](https://code.claude.com/docs/en/plugins)、[Hooks](https://code.claude.com/docs/en/hooks)、[Desktop](https://code.claude.com/docs/en/desktop)
- [Claude Chat/Cowork 插件边界](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [DeepSeek 接入 Codex](https://api-docs.deepseek.com/quick_start/agent_integrations/codex/)、[接入 Claude Code](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/)、[Deep Code skills](https://api-docs.deepseek.com/quick_start/agent_integrations/deepcode/)
- [MiMo 接入 Claude Code](https://mimo.mi.com/docs/en-US/tokenplan/integration/claudecode)、[接入 Codex](https://mimo.mi.com/docs/en-US/tokenplan/integration/codex-configuration)、[工具概览](https://mimo.mi.com/docs/en-US/tokenplan/integration/tools-overview)、[MiMo Desktop](https://mimo.mi.com/docs/en-US/tokenplan/integration/mimo-desktop)

- [Harness Skills](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/skills)、[原生 bundle 分发](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish)、[Desktop 独立 profile](https://deepseek-harness.github.io/deepseek-harness/en/reference/)、[上下文快照](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/system-prompt)
- [Cursor Skills](https://cursor.com/docs/skills)、[Rules](https://cursor.com/docs/rules)；[Gemini Skills](https://geminicli.com/docs/cli/skills/)、[GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)
- [OpenCode Skills](https://opencode.ai/docs/skills/)、[Rules](https://opencode.ai/docs/rules/)；[Copilot Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)、[项目指令](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
