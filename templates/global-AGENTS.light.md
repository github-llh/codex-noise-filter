# Language Preference

默认使用简体中文回复。

规则：

1. 分析、解释、计划、变更说明、验证结果、根因分析和下一步建议使用简体中文。
2. 代码、命令、配置项、环境变量、文件名、类名、方法名、日志和异常信息保持原文。
3. 除非当前任务目标明确需要英文，否则不要使用英文回复。

---

# Tooling Preference

对于 JetBrains 项目：

1. 代码读取、定位、修改、诊断任务优先调用 JetBrains MCP / IDE 工具。
2. JetBrains MCP 不可用、超时或返回错误时，再使用 Shell。
3. 优先分析最小范围，不做无意义全仓扫描。

非 JetBrains 项目可使用本地文件工具；搜索优先 `rg` 或 `rg --files`。

---

# Programming Tasks

编程相关任务默认启用 `codex-noise-filter` skill。

触发范围：

- 编写、修改、调试、排查、重构、迁移、解释代码。
- 粘贴代码片段、diff、报错日志、异常堆栈、构建/测试失败、命令输出、IDE 截图、路径、文件名、类名、方法名、配置文件或项目结构。
- 只说“报错了”“失败了”“为什么不行”“处理一下”“看下这个”“还是这样”“按计划执行”等模糊指令，但上下文能从日志、截图、路径、当前仓库或上一轮任务推断为编程排查或修复。
- 多文件排查、跨模块调用链分析、构建、测试、前后端代码规范。
- 任务经任意第三方调用、App、终端/CLI、IDE 插件、MCP/ACP、hook、subagent、CI/chatops、`cc switch`、模型/供应商路由、未知 wrapper 或未来新增工具转发，只要载荷涉及代码证据或工具链动作，仍按编程任务触发。
- 平台名、agent 名和技术栈名只是示例；若当前宿主、当前工具、cwd、文件、配置、命令、日志、diff、补丁、active cache path 或本机环境证据指向未列名平台/技术栈，也要按编程任务触发，并由当前证据内部追加对应范围。
- 输入体现减少 token、压缩噪音、简洁可追溯、可复盘、少读无关文件或保留证据链的需求。

全局安装与跨平台路径：

- 第三方 agent/CLI 不一定安装 Codex，也不一定存在 `.codex` 目录；不能把 `.codex` 当成唯一入口。
- AGENTS 可能安装在任意用户级目录、第三方配置目录或当前项目内；先以第三方工具实际加载的配置文件所在目录作为 `HOST_CONFIG_DIR`，以宿主实际导入的 AGENTS 文件所在目录作为 `AGENTS_DIR`。如果配置文件是 `/path/to/vendor/config/agent.md`，则 `HOST_CONFIG_DIR=/path/to/vendor/config`。
- 若第三方要求在自己的配置目录下放扩展能力，最高优先级是在该配置目录中新建 `skills/codex-noise-filter/` 并放入完整 skill：`$HOST_CONFIG_DIR/skills/codex-noise-filter/SKILL.md`、`$HOST_CONFIG_DIR/skills/codex-noise-filter/references/00-index.md`；也兼容 `$HOST_CONFIG_DIR/codex-noise-filter/SKILL.md`。Windows 使用同等反斜杠路径。
- 若随 AGENTS 一起分发 skill，继续检查相对路径：`$AGENTS_DIR/skills/codex-noise-filter/SKILL.md`、`$AGENTS_DIR/codex-noise-filter/SKILL.md`、`$AGENTS_DIR/.agents/skills/codex-noise-filter/SKILL.md`。
- 若设置了 `CODEX_HOME`，兼容检查 `$CODEX_HOME/AGENTS.override.md`、`$CODEX_HOME/AGENTS.md` 和 `$CODEX_HOME/skills/codex-noise-filter/SKILL.md`；Windows 对应 `%CODEX_HOME%\AGENTS.override.md`、`%CODEX_HOME%\AGENTS.md` 和 `%CODEX_HOME%\skills\codex-noise-filter\SKILL.md`。
- macOS/Linux 用户级兼容路径包括 `$HOME/.agents/skills/codex-noise-filter/SKILL.md` 和 `$HOME/.codex/skills/codex-noise-filter/SKILL.md`；Windows 包括 `%USERPROFILE%\.agents\skills\codex-noise-filter\SKILL.md` 和 `%USERPROFILE%\.codex\skills\codex-noise-filter\SKILL.md`。
- 不能把某台机器的绝对路径写死给其他用户；每次在第三方 agent/CLI 中导入 AGENTS 后，先按当前系统、当前用户和环境变量解析真实路径，再判断是否能加载 skill。

执行入口：

1. 先执行 Skill Bootstrap：AGENTS 只是指令文件，不等同于 skill 自动加载器；若当前宿主支持 Codex/Agent Skills，先确认可用 skill 列表中存在 `codex-noise-filter`，不存在时不要声称已加载 skill。
2. 若宿主未自动暴露该 skill，但允许读取文件，按顺序查找并读取首个存在的 `SKILL.md`：第三方配置目录 `skills/codex-noise-filter/`、随 AGENTS 分发的相对路径、`<repo>/.agents/skills/codex-noise-filter/SKILL.md`、用户级 `.agents` 路径、`CODEX_HOME` 路径、兼容 `.codex` 路径；读取成功后把状态记为 `manualFileBootstrap`，继续读取同目录 `references/00-index.md`。
3. 只有在宿主既不支持 skill 发现、也不能读取上述文件时，才把状态记为 `fallbackOnly`，执行下方“第三方兜底闭环”；兜底不是自动加载成功。
4. 再按 `references/00-index.md` 渐进读取对应规则文件。
5. 第三方调用、模型切换、CLI/App/插件/路由器变化不能降低内部触发级别；仍执行任务胶囊/快照、调用链、局部对齐、抽象抽离、编码/中文乱码检查、环境缓存和验证策略。
6. 内部追加范围不按固定平台或技术栈清单裁剪；先从当前宿主、当前工具动作、cwd/workspace、文件扩展名、配置文件、命令、日志、diff、active cache path 和本机环境证据判断本轮需要的 reference、环境缓存和最小验证项。
7. 修改前确认目标文件、问题根因、最小修改方案、调用链、影响面和不影响范围。
8. Maven、JDK、Node、Python 等环境路径先读项目缓存和 IDE/项目配置；拿不到时再查找本机候选路径，验证通过后缓存。未列名工具链也要先确认项目根、命令来源、active cache path 和最轻量验证边界。
9. 遇到中文字符乱码、`encoding`、`charset`、UTF-8/GBK、locale、终端输出或页面文案异常时，先确认项目编码依据和最小验证方式，不把它当成第三方展示问题跳过。
10. 长任务、切换窗口或上下文压缩前，输出 Context Capsule。
11. 一旦进入编程任务，后续每次工具调用、写入、验证和最终回复前都必须自检内部状态：已读规则、任务胶囊/快照、触碰范围、调用链、局部对齐、抽象抽离、环境缓存和验证；缺项时先补齐，不能只总结最后一个工具结果。

第三方兜底闭环：

如果当前宿主、第三方 agent 或模型路由不能发现、读取或执行 `codex-noise-filter` 的 `SKILL.md` 和 references，也不能跳过工作流；必须直接执行以下最小矩阵，并明确记录 `fallbackOnly` 原因：

1. 入口恢复：恢复原始意图、cwd、项目根、目标文件、命令、日志、diff 和工具动作。
2. 任务胶囊/快照：复杂任务开始、读取 3 个文件、执行 2 次工具调用、耗时工具调用前、每次写入前、阶段完成后都输出或刷新 Capsule。
3. 读取与调用链：读取当前文件、必要配置、直接调用方/被调方、影响面和回滚点。
4. 局部对齐：检查并闭环注释契约、魔法值/硬编码、重复逻辑、抽象抽离时机、类型/any 边界、安全边界和旧代码一致性。
5. 动态范围：从当前宿主、当前工具、文件/配置/命令/日志/diff 和 active cache path 判断本轮技术栈与 reference；未列名平台或未列名语言仍执行公共门禁和最小验证。
6. 环境缓存：构建、编译、lint、format、typecheck、测试、运行前先解析 `.codex/local-environment.<profile>.json`；旧版 `.codex/local-environment.json` 只作为一次性迁移输入。
7. 验证：修改后执行覆盖触碰范围的最轻量非交互验证；无法运行必须说明原因。
8. 恢复交付：网络断开、工具超时、上下文压缩或模型切换后，先读当前文件、`git diff`、`git status` 和最近 Capsule，从断点继续。

防模型/第三方重置：

- 如果执行流像被模型重置、只剩最后一次工具结果或第三方只给出“已替换/Build 完成”，不得直接交付。
- 先重建状态：已读规则、任务胶囊、当前文件、`git diff`、触碰范围、调用链、局部对齐、环境缓存、验证结果。
- 缺少任一必需状态时，先补读、补胶囊、补验证或说明无法补齐原因。
