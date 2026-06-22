# Changelog

本文件按真实 Git 记录维护。版本号只使用仓库已有 tag；未提交内容放入 `Unreleased`，不伪装成历史版本。

## Unreleased

- 补齐插件分发模板：新增 `scripts/build-plugin-package.sh`、`distribution/plugin/.codex-plugin/plugin.json`、`distribution/marketplace.json` 和分发说明，区分 skill 编写目录与 plugin 分发目录，避免直接把当前 skill 根目录误当插件根。
- 按 Codex Agent Skills 官方资料和 Runoob 教程查漏补缺：压缩并前置 `SKILL.md` 的核心触发描述，新增 `agents/openai.yaml` 声明 Codex App UI 元数据和隐式调用策略，并同步中英文 README 的目录结构与 description 预算说明。
- 按官方/第三方资料刷新跨宿主接入矩阵：补充 Roo Code 原生 Agent Skills、Gemini CLI `.gemini/skills`、OpenCode/MiMo Code skills、VS Code/GitHub Copilot Agent Skills、Continue rules/MCP、aider repo map/read-only context 和 Windsurf MCP/Rules 资料；同步 `SKILL.md`、`00`、`02`、`15`、README 与模板的 bootstrap 路径说明，避免把 rules/custom instructions 误判为 skill 已加载。
- 全文核验 15 个 reference：补齐 Python `StrEnum` 的 3.11+ 边界，去掉环境缓存示例中的个人机器名，并把小程序 npm 包参考链接替换为可自动校验的 npm registry API。
- 增加跨宿主 Skill 兼容矩阵：新增 `references/15-host-skill-portability.md`，按 `nativeSkill`、`nativeCommand`、`rulesOnly`、`delegatedTool`、`manualFileBootstrap`、`fallbackOnly` 统一第三方平台执行顺序、触发条件和性能预算，避免继续把平台名写成白名单。
- 强化 Codex 上下文窗口与自动 compact 处理：结合官方 thread/context window、automatic compaction、subagent 噪音隔离、`PreCompact`/`PostCompact`/`SessionStart compact` 事件和 memory 边界，补充上下文预算、压缩前后恢复协议、Context Capsule 字段和团队接入模板，避免大日志、重复搜索和旧假设污染主上下文。
- 增加第三方中转动态追加范围：平台名、agent 名、CLI/IDE/MCP/ACP 名称和技术栈名不再作为封闭白名单；从当前宿主、工具动作、cwd/workspace、文件扩展名、配置文件、命令、日志、diff、补丁、active cache path 和本机环境证据动态追加 reference、环境缓存和最小验证范围。
- 强化 Skill Bootstrap 三态验证：`nativeSkill`、`manualFileBootstrap`、`fallbackOnly` 必须和当前宿主真实 discovery/file-read 能力对应，AGENTS 导入本身不再被视为 skill 已加载；第三方只导入 AGENTS 时必须优先在 `HOST_CONFIG_DIR/skills/codex-noise-filter/` 或 AGENTS 相对目录分发完整 skill。
- 增加第三方全流程执行矩阵：任意第三方调用、模型路由、IDE/MCP、CLI wrapper、hook/subagent、CI/chatops、未知转发层进入本 skill 后，必须串联入口恢复、任务胶囊/快照、读取、调用链、局部对齐、抽象抽离、编码/中文乱码、环境缓存、验证、恢复与交付，不能只执行搜索、写入或验证其中一部分。
- 增加跨技术栈编码与中文乱码门禁：中文字符、非 ASCII 文案、`encoding`/`charset`、UTF-8/GBK、locale、终端输出、页面文案或构建资源异常时，自动确认项目编码依据、active cache path、工具链 locale 和最小验证路径。
- 强化任意第三方调用与模型路由触发口径：不再依赖列举具体 agent、App、CLI、插件或路由器名称；任意第三方调用、未知 wrapper、未来新增工具、模型/供应商切换只要携带编程任务证据，都必须按本 skill 内部触发，继续执行索引、任务胶囊、调用链、局部对齐、环境缓存和验证策略。
- 全文收敛触发语义：质量门禁、读取扩窗、规则刷新、环境缓存、构建验证和技术栈路由均改为基于任务状态、代码证据、触碰范围、调用链、风险信号和权限边界自动触发；移除“需要写出 skill 名、提醒、固定提示词或人工手动指定才执行”的表达，保留新增依赖、公共契约、交互验证、上传发布和长期 memory 等明确授权边界。
- 强化续跑、上下文恢复和 skill 规则变更后的自动刷新门禁：不依赖外部提醒，只要当前任务继承上一轮判断、存在 Context Capsule、跨窗口继续或 skill/reference 发生变更，就必须重新读取当前 `SKILL.md`、`00-index.md` 和命中的 reference；按当前任务证据、触碰范围、直接调用链和必要读取文件逐项区分协议 key、技术常量、固定业务取值、配置值、运行期字典值和局部字面量，避免漏掉应枚举的业务取值，也避免把所有常量机械改成枚举。
- 强化编码风格智能化门禁：写代码前先分类字面量、魔法值、状态/类型/来源、阈值、配置 key、路由/事件/storage key 和重复映射；优先复用既有枚举、常量、配置、字典、SDK 常量、生成类型和设计 token，并把风格预检写入任务胶囊、索引路由和各技术栈落地规则。
- 拆分过大的 reference：新增 `13-read-expansion-and-history.md` 承接读取完整性、智能扩窗和 Git 历史防回归；新增 `14-environment-cache-by-stack.md` 承接 Maven/Java、Node/前端、Python、小程序栈级环境缓存细则。`02` 和 `06` 保留旧锚点转发，避免既有链接断裂。
- 扩展 `SKILL.md` 的 `description`，补充 Java 后端、Maven 多模块、事务并发、Python、Vue/React、小程序、Plan/Goal、上下文压缩、减少 token 和调用链确认等高频编程触发词。
- 补充中英文 README 的 `为什么用 / Why Use It`、Before/After 对比和可复制触发示例。
- 新增 `examples/` 五个典型场景：Java Controller/Service、Maven 多模块、Vue/React、Python、小程序。
- 新增 `templates/` 三个团队接入模板：轻量全局 AGENTS、仓库安装片段、触发检查 prompt。
- 新增本 `CHANGELOG.md`，并按真实 `git log` 和 tag 重新整理历史记录。
- 强化跨技术栈硬编码和重复逻辑治理，明确什么时候使用枚举、常量、配置、动态字典、mapper、converter、schema、策略或 helper，并将通用判断从 Java 专属规则抽到全局规则。
- 继续抽取各技术栈公共规则到 `01-global-engineering-rules.md`，覆盖文件归属、环境命令、验证策略和安全边界；`03`、`04`、`07`、`09`、`10`、`11`、`12` 只保留技术栈落地差异。
- 收敛 `02-noise-filter-workflow.md` 和 `06-environment-discovery.md`：`02` 只保留跨技术栈执行门禁与局部对齐流程，`06` 只保留环境发现、最小验证和缓存结构，技术栈差异下沉到对应 reference。
- 强化环境缓存自动维护流程：构建、编译、测试、运行、预览或发布前校验时自动验证并复用 `.codex/local-environment.json`；缓存不满足当前命令时才查找本机候选路径，验证后写回缓存、重试原命令，并自动检查/补齐 Git root 的 `/.codex/` 忽略规则。
- 强化自动意图识别：粘贴代码、diff、报错日志、异常堆栈、构建/测试失败、命令输出、IDE 截图或“报错了/失败了/处理一下”等带上下文的模糊指令时，不依赖写出 skill 名，自动按排障、修复或验证任务进入索引流程。
- 强化读取完整性与智能扩窗：修改代码或评估强规则时，默认行数窗口只作为初始预算；按 Java、Python、Vue/React、小程序、SQL、配置、脚本和测试各自语法结构自动判断语义单元边界，扩读完整逻辑、契约区、直接调用点和相邻范式。未完成必要扩读前，不得声称未发现规则违背，也不能因未读到而跳过低风险局部优化；只有无法自动判断边界或业务语义时才说明缺口。
- 新增 Git 历史对比与回归防护：涉及既有行为语义、公共契约、历史兼容、回归风险或重构旧逻辑时，自动读取最小 git 历史证据，使用 `git log`、`git blame`、`git show`、`git diff`、`git log -S/-G` 对比提交意图、blame 区间和关键 token 演进；只围绕触碰文件、语义单元和直接调用链查历史，不使用会改工作区的 git 命令。
- 强化强规则命中后的自动升级：截图、片段、触碰范围、直接调用链或为完成任务必须读取的相关文件里已出现硬编码、重复逻辑、配置写死、分层错位、注释缺口或安全边界问题时，先判断调用链深度、涉及文件数量、契约风险和验证路径；低风险闭环时写入任务胶囊并直接按对应 reference 局部修复，不把“最小改动”或“非 Plan 模式”当作跳过理由。
- 强化全技术栈默认验证策略：Java、Python、前端、小程序等默认不做运行态、交互态或屏幕级操作验证，不自动启动浏览器、Browser/Computer Use、桌面点击、模拟器、真机或外部系统联调；默认以语法、编译、类型检查、构建或等价非交互命令通过作为验收，只有当前任务目标本身需要操作性证据且权限边界清楚时才做操作验证。
- 强化前端环境缓存：编译/构建前按目标 `package.json`、lockfile、`engines`、`packageManager`、依赖版本和 scripts 匹配 Node、包管理器与构建命令，写入 `.codex/local-environment.json`；缓存命中直接复用，构建失败疑似环境/脚本不匹配时重新发现、更新缓存并重试一次。
- 强化跨技术栈环境缓存：Java/Maven 按 `pom.xml`、`.mvn/*`、wrapper 和 Java/Maven 版本约束匹配 JDK/Maven/root/module；Python 按 `pyproject.toml`、锁文件、requirements、tox/nox 和虚拟环境匹配解释器/管理器；小程序按 `project.config.json`、`app.json`、`pages.json`、`manifest.json`、Taro/uni-app 配置和必要的 `package.json` 匹配框架/平台/构建脚本。失败疑似环境、依赖、模块、脚本或平台不匹配时自动重算缓存并重试一次，减少人工手动指定。

## 1.0.1 - 2026-06-14

Tag: `1.0.1`，commit: `0279ba8`

- `0279ba8` 补充 `codex-noise-filter` 使用说明，并同步中英文 README。
- `b7c4d79` 添加 Apache-2.0 开源协议，并在中英文 README 中说明协议边界。
- `be8c25a` 优化 README 展示风格，改为开源项目首页式顶部描述。
- `ebdde4e` 移除个人 Maven 绝对路径写法，明确先读 `.codex/local-environment.json`，未命中再发现、验证、写入缓存。
- `f55e955` 强化小程序原生、uni-app、Taro、分包、模拟器、测试与索引路由规则。

## 1.0.0 - 2026-06-14

Tag: `1.0.0`，commit: `50413f1`

### 2026-06-14

- `50413f1` 明确 React 列表 key、Vue slots、组件二次封装，以及表单、表格、弹窗、上传下载等高复用组件的状态保留要求。
- `2b9afd3` 强化 Vue/React 前端侧语法、版本识别、运行、测试、构建和索引性能策略。
- `029877d` 强化 Python 侧语法、环境、运行、测试、lint、类型检查和性能规则。

### 2026-06-12

- `98f847d` 强化索引性能，同时保留既有硬约束。
- `518a1f5` 压缩入口说明并强化索引性能，避免规则堆回 `SKILL.md`。
- `d3644fc` 明确新增、修改、Plan、Global/Goal、自动续跑、上下文恢复、跨窗口、局部补丁和后续修复都必须走索引、确认触碰范围并执行局部规则对齐。
- `3e7a088` 新增 Controller 触碰硬约束，要求迁出返回数据补全、列表加工、状态流转、跨系统取值、数据库/缓存访问等业务逻辑。

### 2026-06-10

- `29e5729` 强化配置写入 yml/properties、配置中心和配置类注入的判断规则。
- `cf0cc76` 强化 Plan 阶段门禁和 Global/Goal 模式兼容，计划必须列出适用 reference 和验收项。
- `43832a9` 新增既有代码修改一致性规则，要求触碰范围内的旧代码同步局部对齐。
- `8a9abca` 补强事务管理器、函数式事务和部分回滚规则。
- `96287a8` 强化事务、并发、幂等、异步、批量处理和索引性能，并新增并发异步批量 reference。
- `5dc2152` 完成整体索引性能优化，拆分 Java 后端架构和 Java 风格规则。
- `bef6eea` 强化 Java 判空与函数式风格规则。
- `ac2dd0e` 强化避免硬编码、重复赋值和重复判断的 Java 后端规则。

### 2026-06-09

- `a056370` 将过长 reference 拆分并强化索引命中效率。
- `edb9f3d` 强化 Lombok 使用标准。
- `d7f0a23` 强化简单校验迁移到 DTO/Request Bean Validation 的规则。
- `6da35f9` 强化稳定状态值和常量枚举化、新建文件归属地、Java 后端分层和注释约束。
- `a3a33a5` 引入更智能的 Maven 环境策略，不把 Maven 路径作为唯一硬编码规则，并新增环境发现 reference。
- `2385f7e` 将编程规则内化进 skill，建立 `SKILL.md` + `references/00-index.md` + 主题 reference 的索引结构，并补充中英文 README。
- `5952ac0` 初始化 skill 基础文件。
- `8930d84` 初始化 README。
