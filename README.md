<div align="center">

# codex-noise-filter

**Codex 编程任务去噪与规则路由 skill**

减少无效上下文 · 强制调用链确认 · 渐进读取规则 · 新旧代码同等约束 · 主动治理魔法值

![Skill](https://img.shields.io/badge/Codex%20Skill-codex--noise--filter-2563eb)
![Routing](https://img.shields.io/badge/Routing-indexed%20references-16a34a)
![Mode](https://img.shields.io/badge/Mode-non--bypassable-f97316)
![Routing](https://img.shields.io/badge/Scope-dynamic%20tool%20%2B%20stack%20evidence-7c3aed)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)

[快速开始](#快速开始) · [为什么用](#为什么用) · [使用方式](#使用方式) · [触发示例](#触发示例) · [能力概览](#能力概览) · [结构](#结构) · [社区健康](#社区健康) · [协议](#协议) · [English](README.en.md)

</div>

## 快速开始

`codex-noise-filter` 是编程任务专用的 Codex skill。它把“先读规则、先收敛上下文、先确认调用链，再改代码”固化为默认流程，并通过 `references/00-index.md` 按需加载 Java 后端、Maven、前端、Python、小程序、并发事务和交付模板等规则。文档里出现的平台、agent、CLI、IDE、MCP/ACP 和技术栈名称都是高频示例，不是封闭清单；真实触发和追加范围由当前宿主、当前工具动作、cwd、文件、配置、命令、日志、diff、active cache path 和本机环境证据决定。

适用场景：

- 编写、修改、调试、排查、重构、迁移、解释代码。
- 粘贴报错日志、异常堆栈、构建/测试失败输出、IDE 截图、代码片段或 diff 后，希望 Codex 自动判断是在排障、修复还是验证。
- 多文件排查、跨模块调用链分析、后端构建、前端页面修复、小程序原生/uni-app/Taro 治理、Python 脚本/服务/包/测试治理。
- 任务经任意第三方调用、Claude Code、Gemini CLI、Cline、Roo Code、aider、OpenCode、Continue、Cursor/Windsurf、ACP/MCP、hooks、subagent、CI/chatops、`cc switch`、model/provider router、gateway/proxy、自定义 wrapper、未知转发层或未来新增工具转发，但载荷仍涉及代码读取、修改、构建、测试、lint、format、typecheck、调试或重构。
- 当前使用的工具或技术栈没有被 README 列出，但载荷包含 cwd、文件扩展名、配置文件、命令、日志、diff、补丁、编码/乱码信号或工具链动作；此时按未知第三方中转恢复原始任务，并动态追加最贴近的 reference、环境缓存和验证范围。
- 输入体现减少 token、压缩噪音、简洁可追溯、可复盘、少读无关文件或保留证据链的需求。

## 为什么用

很多编程任务失败不是因为不会写代码，而是因为上下文太散、调用链没闭环、规则只约束了新增代码、已有代码继续失控。`codex-noise-filter` 把这些容易遗漏的步骤固化为 skill 入口，让 Codex 在动手前先确认“读哪些规则、碰哪些文件、不碰哪些边界、怎么验证”。

| 不使用时 | 使用后 |
| --- | --- |
| 粘贴一段报错日志后还要反复说明“帮我排查/修复”。 | 从日志、堆栈、路径、命令和当前仓库自动推断为排障任务，先定位根因，再决定最小修复和验证。 |
| 容易全仓扫描，token 被日志和无关文件吃掉。 | 先读 `references/00-index.md`，只加载当前任务需要的 reference。 |
| 只改眼前代码，漏掉 Controller/Service/DTO/Entity 的调用链影响。 | 修改前确认触碰范围、调用链和不影响范围。 |
| 新增代码遵守规范，已有触碰代码继续堆业务逻辑、硬编码和重复 set/if。 | 新增和已有触碰代码同等执行局部规则对齐。 |
| 写代码时先把字符串、数字、状态和阈值写进去，事后才想起抽常量。 | 写代码前先做风格预检：字面量分类、复用既有枚举/常量/配置/字典/SDK 常量，再决定是否保留局部字面量。 |
| 明明截图、片段或调用链相关文件里已经有不可接受的硬编码、重复逻辑或分层错位，却被“最小改动”挡住。 | 自动判断调用链深度、涉及文件数量、契约风险和验证路径；低风险闭环时写入任务胶囊并直接按对应 reference 局部修复。 |
| 构建命令靠经验猜 `npm run build`、系统 `python` 或当前 shell 的 `mvn`，失败后还要人工手动指定环境。 | 按 Java/Maven、Python、Node/前端、小程序各自配置自动匹配工具链、命令和缓存；失败疑似环境不匹配时自动重算并重试一次。 |
| Plan/Goal、续跑或跨窗口后容易忘记规则。 | Plan/Goal/上下文恢复都必须走索引和 Context Capsule。 |
| 任务被任意第三方调用、agent、App、CLI、hook、MCP/ACP、subagent、CI bot、未知 wrapper 或 `cc switch`/router 转发后，容易被当成普通工具执行。 | 入口和路由层只作为证据；从 cwd、文件、命令、日志、diff 和工具动作恢复原始任务，继续内部触发索引、局部对齐和验证。 |
| 未列名平台、未列名 agent 或新技术栈容易被误判为“不在规则范围”。 | 平台和技术栈名只作为提示；从当前工具、文件、配置、命令、缓存和本机环境证据动态追加范围，未知技术栈也先执行跨技术栈公共门禁和最轻量验证。 |

## 使用方式

Codex skills 可用于 Codex App、CLI、IDE 扩展，也可作为任意第三方调用、wrapper、路由转发或模型切换后的内部规则入口。日常使用不应依赖写出 `$codex-noise-filter`；只要输入、转发载荷或上下文里有代码、日志、堆栈、命令输出、截图里的错误、路径、项目结构、续跑状态或规则失效信号，skill 就应按编程任务处理。

如果请求来自任意第三方调用、第三方 agent、桌面/网页 App、终端/TUI/CLI、IDE 插件、MCP/ACP、hook、subagent、CI/chatops/webhook、`cc switch`、model/provider router、gateway/proxy/adapter、自定义 wrapper、未知转发层或模型路由，也按同一规则处理：先恢复原始任务、cwd、文件、命令、日志、diff 和工具动作，再由 `references/00-index.md` 自动路由。第三方工具的“已修改/已验证/无需触发”、模型切换或供应商选择只能作为线索，不能替代当前工作区文件、diff、环境缓存和验证检查。若当前平台或技术栈未被列名，按 `02#第三方中转动态追加范围` 从当前证据追加本轮 reference；未知技术栈至少执行 `01` 的跨技术栈公共门禁、`06` 的当前项目/环境缓存门禁和覆盖触碰范围的最轻量非交互验证。

只导入 `templates/global-AGENTS.light.md` 不会让第三方 agent/CLI 自动发现本 skill。AGENTS 是指令链，不是 skill 注册表；第三方机器不一定安装 Codex，也不一定存在 `.codex`。支持 Agent Skills 的宿主还必须把本目录安装到可扫描位置，或在宿主配置里显式暴露 `SKILL.md` 路径。若宿主只支持导入 AGENTS 但能读文件，先取得第三方实际加载的配置文件路径，把其父目录记为 `HOST_CONFIG_DIR`，然后新建 `$HOST_CONFIG_DIR/skills/codex-noise-filter/` 并复制完整 skill 目录，至少包含 `SKILL.md`、`references/00-index.md` 和命中的 references；如果 AGENTS 是单独导入文件，也可放在 AGENTS 文件旁边的 `skills/codex-noise-filter/` 或 `codex-noise-filter/`。只有宿主既不能发现 skill、也不能读取分发文件时，才进入 `fallbackOnly` 兜底闭环。

### 仓库级使用

适合团队共享同一套工程规则。

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  references/
```

在仓库根目录或子目录启动 Codex 后，直接提出编程任务即可；如果要强制触发，提示中写：

```text
$codex-noise-filter 按这个 skill 检查并修改当前 Maven 后端问题。
```

### 个人级使用

适合把规则用于多个仓库。macOS/Linux 优先把本目录复制或软链到 `$HOME/.agents/skills/codex-noise-filter/`；Windows 优先复制到 `%USERPROFILE%\.agents\skills\codex-noise-filter\`。若当前环境使用 `CODEX_HOME` 或其他自定义 skill 目录，则同时确认宿主能扫描到对应 `SKILL.md`。更新后如果选择器里没有出现，先确认可扫描路径，再重启宿主。

### Codex App

1. 打开 Codex App 并选择项目目录，优先使用 Local 模式处理本机代码。
2. 在任务里直接描述编程目标即可；写出 `$codex-noise-filter` 只作为附加信号，不是启用前提。
3. 需要确认是否触发时，要求 Codex 先输出“命中的 skill、读取的 reference、触碰范围和验证项”。

示例：

```text
$codex-noise-filter 修复这个 Controller 的业务逻辑下沉问题，并说明读取了哪些 reference。
```

### 终端 / CLI

在项目根目录启动 Codex：

```bash
codex
```

交互式 CLI 中可使用 `/skills` 选择 `codex-noise-filter`；prompt 中写出 skill 名只作为附加信号：

```text
$codex-noise-filter 按索引读取最小规则集，检查这个 Java Service 改动。
```

长任务建议搭配 `/plan` 或 `/goal`，但 Plan/Goal 也不能绕过本 skill 的索引、调用链和局部规则对齐。

### IDE 扩展

在 VS Code、JetBrains 等 IDE 里使用时，先确保 Codex 当前工作目录是目标项目。JetBrains 项目会优先走 JetBrains MCP / IDE 工具；如果 IDE 工具不可用，才回退 Shell。可在任务开头写：

```text
$codex-noise-filter 使用 IDE 上下文定位调用链，不要全仓无意义扫描。
```

### 全局 AGENTS 轻量兜底

全局 `AGENTS.md` 不需要复制本 skill 的全部内容，只建议保留三类轻量指引：

```md
# Language Preference
默认使用简体中文回复。

# Tooling Preference
JetBrains 项目优先使用 JetBrains MCP / IDE 工具；搜索优先 rg。

# Programming Tasks
编程任务默认启用 codex-noise-filter，先读 SKILL.md 和 references/00-index.md。
```

### 触发验证

首次接入后，可用以下 prompt 验证：

```text
请说明当前任务是否触发 codex-noise-filter；如果触发，请列出将读取的 reference、触碰范围、禁止触碰范围和验证项。
```

如果没有触发，只能是任务缺少代码上下文、转发载荷没有可复原的编程证据、skill 未被当前宿主加载、同名 skill 冲突或会话尚未刷新；不能因为任务来自第三方调用、模型路由、CLI/App/插件或未知 wrapper 就判定不触发。

### 自动触发信号

以下输入不需要额外说明“请使用 skill”，应自动进入索引流程：

- Java/Maven：`Exception`、`Caused by`、`BUILD FAILURE`、`Failed to execute goal`、`Compilation failure`、`NullPointerException`。
- Python：`Traceback`、`pytest`、`AssertionError`、`ModuleNotFoundError`、`ImportError`。
- Node/Vue/React：`npm ERR`、`pnpm ERR`、`yarn error`、`TypeError`、`ReferenceError`、`vite`、`webpack`。
- 小程序：`project.config.json`、`miniprogram-ci`、`setData`、`app.json`、`pages.json`、`TARO_ENV`、`mp-weixin`。
- Agent/路由转发：任意第三方调用、未知 wrapper、未来新增 agent，以及 `Claude Code`、`Gemini CLI`、`Cline`、`Roo Code`、`aider`、`OpenCode`、`Continue`、`Cursor`、`Windsurf`、`Copilot`、`Antigravity`、`Zed`、`ACP`、`MCP`、`hook`、`subagent`、`chatops`、`webhook`、`CI bot`、`cc switch`、`cc-switch`、`ccswitch`、`model router`、`provider switch`、`gateway`、`proxy`、`adapter`。
- 模糊但有上下文的中文指令：`报错了`、`失败了`、`为什么不行`、`还是这样`、`处理一下`、`看下这个`。

## 触发示例

这些 prompt 可以直接复制使用：

```text
粘贴这段 Maven BUILD FAILURE 后，直接定位根因；如果能在当前仓库闭环，就做最小修复并重跑最小验证命令。
```

```text
这个 Python Traceback 是怎么回事？按当前项目虚拟环境和测试配置排查，能修就直接修。
```

```text
$codex-noise-filter 检查这个 Controller 是否写了业务逻辑，并把应下沉的逻辑迁到 Service 实现层。
```

```text
$codex-noise-filter 按 Maven 多模块 root 构建规则，找到当前模块的最小验证命令。
```

```text
$codex-noise-filter 修改这个 Service 时同步检查接口注释、事务边界、枚举/配置外置化和重复 if/set。
```

```text
$codex-noise-filter 处理这个 Vue/React 组件问题，先确认框架版本、组件归属、状态契约和验证命令。
```

```text
$codex-noise-filter 处理这个 Python 测试失败，先识别虚拟环境、依赖管理器、定向测试和 lint/type check。
```

```text
$codex-noise-filter 检查这个小程序页面，先识别原生/uni-app/Taro，再确认分包、依赖边界和默认构建验证方式。
```

更多场景见 [`examples/`](examples/)；团队接入模板见 [`templates/`](templates/)。

## 能力概览

| 能力 | 说明 |
| --- | --- |
| 索引路由 | 先读 `00-index.md`，按任务类型只打开必要 reference，避免主文件和上下文膨胀。 |
| 自动意图识别 | 从日志、堆栈、截图、路径、命令输出、代码片段、续跑状态和风险信号中推断排障、修复、验证或解释意图，不依赖反复写出 skill 名。 |
| 不可绕过门禁 | 新增、修改、Plan、Global/Goal、续跑、跨窗口恢复都必须确认触碰范围、调用链和局部对齐项。 |
| 智能扩窗 | 修改代码或评估强规则时，局部读取窗口只是起点；按 Java、Python、Vue/React、小程序、SQL、配置、脚本和测试各自语法自动扩读完整语义单元、契约区、直接调用点和相邻范式，避免因没读到而漏判漏修。 |
| Git 历史防回归 | 涉及旧逻辑、公共契约、历史兼容或高风险边界时，自动读取最小 git 历史证据，对比提交意图、blame 区间和关键 token 演进，避免只按当前需求改崩既有行为。 |
| 强规则自动升级 | 触碰范围、直接调用链或为完成任务必须读取的相关文件已命中硬编码、重复逻辑、配置写死、分层错位、注释契约缺口或安全边界时，自动判断是否能低风险闭环；能闭环就写入任务胶囊并直接修，不能闭环才记录风险。 |
| 编码风格智能化 | 写代码前主动识别魔法字符串、魔法数字、状态/类型/来源、阈值、时间窗、配置 key、路由/事件/storage key 和重复映射；优先复用项目既有枚举、常量、配置、字典、生成类型、SDK 常量和设计 token。 |
| 抽象抽离时机 | 看到公共接口、公共方法、公共类、helper、hook/composable、schema、mapper/converter、策略、泛型或 `any` 边界时，自动判断共同语义、变化点稳定性、依赖方向、契约风险和验证路径；前端 `any` 只允许最小桥接例外，后端公共抽象优先用清晰业务接口或受约束泛型。 |
| 跨技术栈公共治理 | 任何项目触碰代码时都先按全局规则检查文件归属、环境命令、验证策略、安全边界、硬编码、重复逻辑和注释位置，再进入对应技术栈落地。 |
| Java 后端治理 | 强制 Controller 轻薄、Service 接口注释、实体 Lombok、事务边界、枚举/配置/校验/去重复。 |
| 全栈默认验证 | Java、Python、前端、小程序等默认只做语法、编译、类型检查或构建等非交互命令验证，不自动浏览器点击、桌面操作、模拟器、真机或外部系统联调。 |
| 前端与小程序 | 覆盖通用前端、原生 JavaScript/TypeScript、Vue 2/3、React、Vite/webpack、原生小程序、uni-app、Taro、分包、构建、测试和前端局部对齐。 |
| 环境发现 | 构建、编译、测试、运行、预览或发布前校验时，按技术栈读取 `pom.xml`、`pyproject.toml`、`package.json`、小程序配置等项目事实，自动验证并复用 `.codex/local-environment.<profile>.json`；旧版 `.codex/local-environment.json` 只作为一次性迁移输入，迁移成功后不再 fallback。缓存不满足或失败疑似环境不匹配时发现本机候选、写回缓存、重试原命令，并确认项目根忽略 `/.codex/`。 |
| 动态工具/技术栈追加 | 第三方中转、未知 wrapper、未列名平台或新技术栈不再靠固定清单判定；从当前宿主、工具动作、文件/配置/命令/日志/diff、active cache path 和本机环境证据追加最小 reference、环境缓存和验证范围。 |
| 编码与中文乱码 | 中文字符、非 ASCII 文案、`encoding`、`charset`、UTF-8/GBK、locale、终端输出、页面文案或构建资源出现异常时，自动确认项目编码依据、active cache path、工具链 locale 和最小验证方式，不把乱码当成第三方展示问题跳过。 |
| 上下文管理 | 面向 Codex 模型上下文窗口和自动 compact，长任务使用 Context Capsule 保存目标、阶段、证据、已改、回滚点、窗口/压缩状态和下一步；大日志、重复搜索结果和旧假设只摘要，降低上下文污染与会话切换丢失风险。 |

## 结构

```text
SKILL.md
CHANGELOG.md
examples/
templates/
references/
  00-index.md
  01-global-engineering-rules.md
  02-noise-filter-workflow.md
  03-maven-backend-build.md
  04-frontend-rules.md
  05-delivery-templates.md
  06-environment-discovery.md
  07-java-backend-architecture.md
  08-java-style-patterns.md
  09-concurrency-async-batch.md
  10-python-development.md
  11-frontend-vue-react.md
  12-miniprogram-development.md
  13-read-expansion-and-history.md
  14-environment-cache-by-stack.md
```

`SKILL.md` 只保留触发、路由和硬约束；执行细则按索引进入对应文件，减少主文件负担。

### 效率策略

- 单个 reference 尽量保持入口化和主题化，避免一个文件堆到数百行。
- `01-global-engineering-rules.md` 只保留全局共用规则，例如文件归属、环境命令、验证策略、安全边界、硬编码、重复逻辑和注释原则。
- `02-noise-filter-workflow.md` 只保留跨技术栈执行门禁、上下文预算、调用链和局部对齐流程；智能扩窗和 Git 历史防回归下沉到 `13-read-expansion-and-history.md`，技术栈差异通过索引进入对应 reference。
- Java 后端架构规则集中到 `07-java-backend-architecture.md`，只有涉及分层、归属地、注释、调用链时才读取。
- Java 代码风格规则集中到 `08-java-style-patterns.md`，只有涉及枚举、参数校验、Lombok、Optional、函数式、去重复时才读取。
- 并发、异步和批量规则集中到 `09-concurrency-async-batch.md`，只有涉及高并发、幂等、死锁、事件、中间件、线程池、虚拟线程、用户上下文传播时才读取。
- Python 规则集中到 `10-python-development.md`，只有涉及 `.py`、Python 语法、虚拟环境、依赖、运行、测试、lint、类型检查或 Python 性能时才读取。
- Vue/React/原生 JS/TS 规则集中到 `11-frontend-vue-react.md`，只有涉及 Vue2/Vue3、React、原生 JavaScript/TypeScript、JSX/TSX、Vite/webpack、组件语法、包管理、运行、测试、lint、类型检查或前端构建时才读取。
- 小程序规则集中到 `12-miniprogram-development.md`，只要涉及原生微信小程序、uni-app、Taro、用户误写 `raro` 但上下文指向 Taro、分包、`project.config.json`、`app.json`、`pages.json`、`app.config.*`、构建、发布、测试，或当前任务目标包含模拟器/真机链路时就读取。
- Maven 构建只读 `03-maven-backend-build.md`；环境路径发现先读 `06-environment-discovery.md`，栈级缓存细节再读 `14-environment-cache-by-stack.md`。`06` 只负责发现顺序、最小验证、本地缓存结构和 `.codex/` 忽略规则维护，不承载各技术栈完整运行手册。
- 索引路由用“任务意图 + 代码证据 + 影响面 + 风险信号”交叉确认，减少误读，避免等待固定提示词，同时避免把所有规则一次性读入。
- `SKILL.md` 硬约束视为常驻规则；优化索引性能时只减少无关 reference 读取，不减少必须执行的约束。
- 常见任务先按快速决策表读取最小组合，例如 Java Controller/Service 改动默认 `02 + 07`，命中枚举、校验、Lombok、Optional、重复逻辑时再追加 `08`。
- Python 任务默认读取 `02 + 10`，执行语法检查、运行、测试、lint 或 type check 前追加 `06 + 14` 建立/复用 Python 环境缓存；跨系统或前后端调用链明确时再追加对应 reference。
- 普通布局/状态契约任务默认读取 `02 + 04`；Vue/React/原生 JS/TS 任务默认读取 `02 + 11`，执行构建、typecheck、lint 或测试前追加 `06 + 14` 建立/复用 Node 前端环境缓存；格式化或类型修复后仍要回扫同一语义单元的注释、魔法值、类型和契约缺口。
- 小程序任务默认读取 `02 + 12`；uni-app/Taro 命中 Vue/React 语法时追加 `11`，通用布局状态追加 `04`，执行构建、编译或 CI 前追加 `06 + 14` 建立/复用小程序环境缓存；只有当前任务目标包含模拟器、预览、上传、真机或发布链路且权限边界清楚时，才查开发者工具路径。
- 执行中触碰范围扩大时，按索引追加 reference；不得为了少读文件而跳过不可绕过门禁、既有代码局部对齐、分层、注释、事务、并发和业务抽象规则。

### 内置重点

- 默认简体中文回复。
- JetBrains 项目优先使用 JetBrains MCP / IDE 工具。
- 修改前确认目标文件、根因、最小方案和不影响范围。
- 修改前必须完成调用链和影响面确认。
- 读取窗口只是初始预算；修改代码或判断强规则前，必须按文件类型、框架配置和对应 reference 自动判断语义单元边界。Java、Python、Vue/React、小程序、SQL、配置、脚本和测试都按自身语法规范和抽象要求扩读完整逻辑、契约区、直接调用点和必要相邻范式，不能因为没读到就跳过局部优化；只有确实无法自动判断边界或业务语义时才说明缺口。
- 涉及行为语义、公共契约、历史兼容、回归风险或重构旧逻辑时，自动读取最小 git 历史证据：`git log`、`git blame`、`git show`、`git diff`、`git log -S/-G`。只围绕触碰文件、语义单元、关键 token 和直接调用链查历史，不全量翻仓库，不用会改工作区的 git 命令。
- 最小改动不是不处理强规则命中的理由；如果硬编码、重复逻辑、配置写死、分层错位或注释/安全边界缺口已经落在本次触碰范围、直接调用链或为完成任务必须读取的相关文件内，必须先判断低风险闭环，成立时写入任务胶囊并直接局部修复。
- 无论新增、修改、Plan、Global/Goal、自动续跑、上下文恢复、跨窗口、局部补丁还是后续修复，只要属于编程任务，都必须执行 skill 索引、触碰范围确认、调用链确认和局部规则对齐。
- 无论任务来自 Codex、任意第三方调用、第三方 agent、App、终端/CLI、IDE 扩展、MCP/ACP、hook、subagent、CI/chatops/webhook、`cc switch`、model/provider router、gateway/proxy/adapter、自定义 wrapper、未知转发层或未来新增工具，只要载荷涉及代码证据或工具链动作，都必须按当前工作区真实文件和 diff 重新触发 skill；不能用“另一个工具已处理”、模型切换或供应商路由跳过索引、任务胶囊/快照、调用链、局部对齐、抽象抽离、编码乱码、环境缓存或验证。
- Plan/计划阶段也必须走 skill 索引，计划里要列出适用 reference、触碰范围、局部对齐项和验收检查。
- Global/Goal/目标追踪模式也必须走 skill 索引，每轮恢复目标、适用 reference、触碰范围、局部对齐项、验收检查和 Context Capsule。
- 规则同时适用于新增代码和已有代码修改；凡本次触碰的方法、类、DTO、SQL、测试和调用链，都要做局部规则对齐。
- 工具链命令执行前按技术栈读取项目配置并验证 active cache path：强制写入并使用 `.codex/local-environment.<profile>.json`；若发现旧版 `.codex/local-environment.json`，只作为一次性迁移输入，迁移成功后不再 fallback。Java/Maven 看 `pom.xml`、`.mvn/*`、wrapper 和 Java/Maven 版本约束；Python 看 `pyproject.toml`、锁文件、requirements、tox/nox 和虚拟环境；前端看目标 `package.json`、lockfile、`engines`、`packageManager` 和 scripts；小程序看 `project.config.json`、`app.json`、`pages.json`、`manifest.json`、Taro/uni-app 配置和必要的 `package.json`。
- Maven 可执行文件、JDK、本地仓库、Python 解释器、Node 包管理器、小程序构建脚本和开发者工具路径不写死个人目录；缓存满足当前命令时直接使用，缓存缺失、失效或不满足项目配置时才按当前机器和项目配置发现，验证通过后写回缓存，并用新缓存路径重试原构建、编译、测试或运行命令。
- 更新 profile 环境缓存后自动检查 Git root 的 `.gitignore` 是否覆盖 `/.codex/`；未覆盖时补齐，并用 `git check-ignore -v` 验证。
- 多模块 Maven 项目默认从聚合 root 节点执行，并使用 `-pl <module> -am`。
- 文件归属、环境命令、验证策略、安全边界、硬编码、重复逻辑和注释原则跨技术栈保持一致，先按 `01-global-engineering-rules.md` 判断，再按 Java/Python/Vue/React/小程序的具体语法落地。
- 写代码前必须做编码风格智能化预检：新增或保留的字符串、数字、状态、类型、来源、协议字段、错误码、配置 key、路由/事件/storage key、阈值、时间窗和重复映射，先判断应使用枚举、常量、配置、字典、SDK 常量、生成类型、design tokens 还是局部字面量。
- Python 项目先确认 `requires-python`、`.python-version`、IDE 解释器、`.venv` 或锁文件，并写入/复用 Python 环境缓存；优先复用 uv、poetry、pipenv、venv、tox、nox 等项目已有工具链，不直接使用全局 pip 乱装依赖。
- Python 代码遵守项目已有 `pyproject.toml`、Ruff/Black/isort/mypy/pyright/pytest 配置；公共函数、复杂返回值、跨模块 DTO/配置对象补类型标注和必要 docstring。
- Python 运行优先使用项目命令、`python -m ...`、`uv run ...`、`poetry run ...`；测试优先定向运行 `python -m pytest path::test` 或项目已有 `tox/nox` 命令。
- Python 修改要做最小验证：语法/导入、定向测试、lint/format/type check 中与触碰范围相关的项；无法验证时说明原因。
- 前端项目先确认 `package.json`、lockfile、`packageManager`、Node 版本和构建工具；不要混用 npm/yarn/pnpm/bun。
- 前端编译、构建、lint、format、typecheck 或测试前必须先读取目标 `package.json` 的 `scripts`、依赖、`engines`、`packageManager`、lockfile，以及 ESLint/Prettier/EditorConfig/Biome/Stylelint/TypeScript 等语法、缩进和格式规范文件，匹配 Node 版本、包管理器与项目脚本，并写入 active cache path 的 `frontendQuality`；缓存满足当前 package、命令和规范文件集合时直接复用。编译失败且疑似环境/依赖/脚本/规范配置不匹配时，重新读取项目配置和本机环境，更新缓存后重试一次。
- Java、Python、前端、小程序等所有技术栈任务结束后，默认不做运行态、交互态或屏幕级操作验证：不启动浏览器，不使用 Browser/Computer Use，不操控电脑屏幕点击，不打开小程序模拟器或真机，不手工调用外部系统/API 页面。默认以语法检查、编译、类型检查、构建或等价非交互命令通过作为验收；只有当前任务目标本身需要浏览器、截图、页面点击、视觉回归、E2E、模拟器、真机、外部服务联调或电脑屏幕操作证据，且权限与副作用边界清楚时，才执行对应操作验证。
- Vue 项目必须先区分 Vue 2 与 Vue 3：Vue 2 默认 Options API 和 Vue Test Utils v1，Vue 3 可用 Composition API、`<script setup>`、Pinia 和 Vue Test Utils v2。
- React 项目先确认 React/React DOM 版本、框架和 TypeScript/JSX 配置；Hooks 只能在组件或自定义 Hook 顶层调用，副作用放 `useEffect`，纯派生值不额外存 state。
- Vue/React 新建组件前必须确认归属、复用价值、公开契约和测试/示例入口；组件使用优先复用项目已有组件，props/slots/children/API 边界要小而稳定。
- 小程序项目必须先识别原生、uni-app、Taro 或其他跨平台框架；不同构建方式走不同语法约束，uni-app/Taro 复用对应 Vue/React 规则，原生小程序走 `Page`、`Component`、`wxml`、`wxss`、`setData` 和官方 API 约束。
- 小程序默认优先按小程序环境缓存匹配框架、平台、源码目录、输出目录、Node 包管理器和项目已有 CLI/CI 构建或编译命令；不默认打开官方开发者工具模拟器、输出目录或真机。
- 小程序分包要在主包接近平台限制、首屏变慢、重功能局部使用、多业务域天然独立或依赖只在局部使用时主动评估；平台包体积限制以官方文档、开发者工具和 CI 当前校验为准，不凭旧经验写死。
- 小程序 npm、插件、分包、独立分包、预下载、权限、登录、支付、订阅消息、web-view 等能力必须按目标平台官方限制处理，并保留密钥、appid、上传凭证和白名单安全边界。
- 小程序验证默认以构建/编译通过为准；`miniprogram-simulate`、`miniprogram-ci`、HBuilderX/uni-app 自动化、官方模拟器或真机只在当前任务目标本身需要操作性证据且权限边界清楚时执行。
- 注释原则跨技术栈保持一致：注释放在对应技术栈最自然的契约位置，例如 Java Service 接口、Python docstring、Vue props/emits/slots 附近、React 组件/Hook/type 附近、前端导出 interface/type 和 api client 附近、SQL/配置定义处。新增、修改、阅读、检索、lint/format/typecheck 修复或截图/diff 审查时，只要暴露出明显契约缺口，都要内部触发注释检查。
- 前端和小程序的属性类型属于自动强规则：定义 props、properties、事件、插槽、页面参数、请求/响应或公开组件 API 时，支持 TypeScript、JSDoc、PropTypes、Vue props type、原生小程序 `properties.type` 或框架类型的项目必须显式定义类型；禁止用裸 `any`、`as any`、`Record<string, any>` 或泛化对象掩盖契约问题。
- 抽象抽离属于自动门禁：新增/修改/阅读/检索/lint/typecheck/截图/diff/调用链确认时，只要出现公共接口、公共方法、公共类、公共文件、helper、hook/composable、schema、mapper/converter、策略、泛型、`any` 或 `Object` 边界，必须先判断抽象时机。前端抽象允许把 `any` 隔离在第三方无类型、框架透传或迁移暂存等最小桥接层；后端公共抽象优先使用清晰业务接口、显式 helper、编译期 mapper/converter 或受约束泛型，不用 `Object`、反射或复杂泛型逃避建模。
- 硬编码治理跨技术栈保持一致：固定闭合集合优先用本栈枚举/联合类型/字典对象，技术标准值优先框架常量，环境或运维可变值走配置，运行期业务可维护值走字典/数据库/配置中心。
- 重复逻辑治理跨技术栈保持一致：字段不同但结构相同的分支、映射、校验、默认值和展示组装，先判断是否为稳定变化点，再用本栈 mapper、converter、schema、策略、hook/composable 或 helper 收敛。
- Vue/React 修改优先运行项目已有 `typecheck`、`build`、`lint` 或等价语法/编译命令；不默认用浏览器验证关键页面或点击操作。
- 前端格式和语法验证不依赖 IDE 飘红/飘黄：进入验证阶段时读取 active cache path 的 `frontendQuality`，核对 ESLint/Prettier/EditorConfig/Biome/Stylelint/TypeScript 配置是否变化，再运行项目已有 lint/format/typecheck/build 脚本；没有脚本时说明缺口，不臆造会全仓改格式的命令。
- 新建文件前必须确认 module、层级职责、包路径、同类文件位置和依赖方向，尤其注意接口、实现、实体、契约可能分属不同 module。
- 明确固定集合的状态、类型、来源、动作、阶段、结果等值优先写成业务 Enum，避免魔法字符串和数字散落。
- URL、密钥、开关、阈值、时间窗、线程池、缓存 TTL、外部系统参数等环境或运维可变值优先写入 yml/properties 或配置中心，并通过配置类注入。
- 简单入参校验优先写在 DTO/Request 的 Bean Validation 注解上，Controller 只触发校验并走统一异常处理。
- 多状态、多类型、多来源、多外部系统、重复流程、重复组装、重复字段映射或稳定扩展点必须评估业务抽象，优先沉淀到 Service 方法、领域组件、策略、枚举行为、Assembler/Converter、配置属性或项目已有扩展点。
- 避免字段不同但逻辑相同的一长串 `if`、`set`、转换或默认值代码，优先复用项目已有映射、校验、枚举策略、条件更新和 helper 能力。
- 判空逻辑可在 Java 版本和项目风格支持时使用 `Optional`、Stream、方法引用等函数式写法，但不要滥用于 DTO/Entity 字段或简单场景。
- 项目已使用 Lombok 时，不手写无意义 getter/setter；DTO/VO/Entity 按项目同类文件风格使用 Lombok，实体已有 `@Data` 范式时直接复用。
- Java 后端 Controller 保持轻薄，不写业务代码；返回数据补全、列表加工、URL/名称/状态填充、数据库/缓存/远程读取、状态流转和复杂条件必须下沉到 Service 实现、Assembler 或项目已有业务组件。
- Service 接口类和所有对外方法必须有契约注释；修改已有接口时，本次触碰的方法也要同步补齐，不等待额外提醒。
- 新增或修改返回实体、数据库实体、DTO/VO 时，类职责和关键字段注释必须同步补齐，尤其是状态、类型、来源、单位、外部映射、兼容字段和权限/脱敏含义。
- 事务默认放在 Service 实现层业务入口；需要精确控制提交/回滚、分段提交或部分失败保留时，优先复用项目事务管理器或 `TransactionTemplate` 函数式写法。
- 高并发默认考虑幂等、锁顺序、死锁规避、异步最终一致、批量分批和用户/租户/审计上下文传播。
- Service 接口和重要实现方法要有原因型注释，做到不冗余、不缺失、不杂乱。
- 前端优先修布局、组件属性和状态契约，不用硬编码掩盖后端问题。
- 编程任务规则已内化到 skill；当前 Codex home 下的全局 `AGENTS.md` 仍建议保留为轻量兜底。
- 长任务、切换窗口或上下文压缩前，使用 Context Capsule 保留目标、证据、已改、回滚和下一步。

### Maven 示例

```bash
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am test
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am -DskipTests package
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
```

### 环境发现

- 在执行构建、编译、测试、运行、预览或发布前校验时，首先定位工作区根并解析 active cache path；强制使用 `.codex/local-environment.<profile>.json`，旧版 `.codex/local-environment.json` 只作为一次性迁移输入，迁移成功后不再 fallback。
- 已有缓存能通过最小验证且满足当前命令需求时直接复用，不重复查找本机路径。
- Java/Maven 缓存按 `pom.xml`、`.mvn/*`、wrapper、Java/Maven 版本约束、聚合 root 和模块路径记录 JDK、Maven、本地仓库、`selectedCommand` 和验证命令。
- Python 缓存按 `pyproject.toml`、锁文件、requirements、tox/nox、版本文件和虚拟环境记录解释器、管理器、lockfile、`selectedCommand` 和验证命令。
- 前端项目缓存按目标 `package.json` 记录 `packageRoot`、`packageManager`、Node 版本约束、lockfile、scripts、最终构建命令和验证命令；`npx` 只作为 command runner 记录，不当作包管理器。
- 小程序缓存按 `project.config.json`、`pages.json`、`manifest.json`、Taro/uni-app 配置和必要 `package.json` 记录框架、平台、源码目录、输出目录、构建命令和必要的开发者工具验证状态。
- 缓存缺失、失效或项目配置显式变化时，再查找本机常见候选路径。
- 找到后必须执行最小验证，例如 `mvn -version` 或带项目 JDK 的 `JAVA_HOME=<jdk> mvn -version`。
- 验证通过后写入 active cache path，用新缓存路径重试原命令，并自动确认根 `.gitignore` 包含 `/.codex/`。

### Codex 上下文管理

- 主文件只负责触发和路由，细则通过 `references/00-index.md` 渐进读取。
- 长任务按“任务胶囊 -> 调用链确认 -> 最小修改 -> 轻量验证 -> Context Capsule”执行。
- 修改已有代码时，执行“触碰范围局部对齐”：不全量重构，但不能只让新增代码遵守规则。
- 代码片段、IDE 截图或调用链阅读过程中暴露出明显规则违背时，先定位真实文件和直接调用链；影响面浅、文件少、兼容性明确时，写入任务胶囊并直接按对应 reference 修复，而不是只输出后续建议。
- Global/Goal 模式每轮推进前恢复 Context Capsule，不能用“追求目标”绕过索引、调用链和局部对齐。
- 切换窗口、模型切换、上下文窗口压力升高、手动/自动 compact、`PreCompact`、`PostCompact` 或 `SessionStart compact` 前后输出或恢复 Context Capsule，避免丢失目标、证据、回滚点和下一步。
- 工具大段日志、重复搜索结果、旧推理和第三方包装层长叙述只保留关键错误、命令、路径/行号和结论，不倒回主上下文。
- 新目标中途插入时，先判断与主任务关系，不默认重置已有调用链。
- 全局 `AGENTS.md` 不需要承载全部细则，但建议保留为兜底入口。
- 长期 memory 只记录稳定偏好和跨任务规则；机器私有绝对路径、临时日志、一次性失败和未验证猜测不写入长期记忆。

## 社区健康

本项目补齐 GitHub Community Standards 识别的社区文件：

- [行为准则](CODE_OF_CONDUCT.md)：说明参与沟通和维护者处理边界。
- [贡献指南](CONTRIBUTING.md)：说明 skill 项目的修改原则、README 双语同步和 PR 检查项。
- [安全策略](SECURITY.md)：说明安全问题的私密报告方式和支持范围。
- [Issue 模板](.github/ISSUE_TEMPLATE)：区分 bug 报告和功能建议，并提醒移除敏感信息。
- [Pull request 模板](.github/PULL_REQUEST_TEMPLATE.md)：要求说明改动范围、同步项和验证结果。

## 协议

本项目使用 [Apache License 2.0](LICENSE) 开源协议。

选择 Apache-2.0 是为了在保持宽松复用的同时，明确版权、专利授权、贡献提交和免责声明边界，降低后续分发、修改和二次使用时的争议风险。若在企业或受监管场景中使用，请结合自身组织的开源合规流程复核。

英文说明见 [README.en.md](README.en.md)。
