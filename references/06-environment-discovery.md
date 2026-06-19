# 环境发现与缓存

用于 Maven、JDK、Node、Python、包管理器、IDE 配置路径、小程序开发者工具等本机环境。目标是提供跨技术栈统一的“发现、验证、缓存”机制，避免硬编码路径或重复全盘查找。

本文件只管环境路径、工具可用性和会影响工具链输出的基础 locale/encoding 证据，不替代各技术栈的运行、构建、测试规则：

- Maven 构建和多模块命令见 `03-maven-backend-build.md`。
- Python 依赖、运行、测试、lint/type check 见 `10-python-development.md`。
- Vue/React 包管理、运行、构建、测试见 `11-frontend-vue-react.md`。
- 小程序原生/uni-app/Taro 的源码/产物目录、模拟器、构建和发布见 `12-miniprogram-development.md`。

## 目录

- [当前项目范围门禁](#当前项目范围门禁)
- [当前工具与技术栈动态追加门禁](#当前工具与技术栈动态追加门禁)
- [跨系统缓存文件命名](#跨系统缓存文件命名)
- [构建测试前环境缓存门禁](#构建测试前环境缓存门禁)
- [发现顺序](#发现顺序)
- [自动环境缓存维护](#自动环境缓存维护)
- [Maven/Java 环境缓存](#mavenjava-环境缓存)
- [Node/前端环境缓存](#node前端环境缓存)
- [Python 环境缓存](#python-环境缓存)
- [小程序环境缓存](#小程序环境缓存)
- [公共验证矩阵](#公共验证矩阵)
- [缓存结构](#缓存结构)
- [缓存策略](#缓存策略)
- [写入边界](#写入边界)
- [与长期记忆的关系](#与长期记忆的关系)

## 当前项目范围门禁

当任务边界证据指向“当前项目、当前工作区、只修改当前项目、不跨项目、不要同步到全局、不要改其他目录”时，当前工作区本地环境缓存不只是工具链路径缓存，也作为项目范围证据自动触发。边界证据可以来自用户输入、当前 `cwd`、workspace root、任务胶囊禁止项、触碰文件路径、Git root、worktree 状态或恢复上下文；即使本轮只改文档、配置或 skill 规则且不准备执行 Maven/Node/Python/小程序命令，也必须做轻量核对。该门禁由本 skill 在确认任务边界时内部触发，外部显式提醒不参与触发级别判断。

触发后先做轻量核对：

1. 定位当前任务工作区根，优先用 `git rev-parse --show-toplevel`，失败时用当前路径和项目根标志。
2. 按 [跨系统缓存文件命名](#跨系统缓存文件命名) 解析当前用户、当前机器、当前工作区的 active cache path；强制使用 `.codex/local-environment.<profile>.json`。若只发现旧版 `.codex/local-environment.json`，必须先迁移替换为 profile 缓存，不能继续把旧版当 fallback。
3. 核对 `workspaceRoot`、`scope`、工具链缓存项和当前工作区是否一致；缓存缺少 `workspaceRoot` 时不能据此扩大范围，只能记录“缓存缺少范围字段，本轮按当前 Git root 保守处理”。
4. 用 `git check-ignore -v .codex/ .codex/local-environment*.json` 核对 `.codex/` 和所有环境缓存 profile 是否被当前项目根 `.gitignore` 覆盖；未覆盖时按“自动环境缓存维护”补根忽略规则。
5. 若本轮不执行构建、测试、运行、预览、代码生成或工具链命令，不查找本机候选、不验证版本、不更新工具路径，只在任务胶囊记录“已核对缓存存在性和项目范围，本轮不使用工具链路径”。
6. 若后续准备执行工具链命令，再进入“自动环境缓存维护”和对应 `14` 技术栈缓存规则，验证并按需更新缓存。

不得出现的行为：

- 不能因为当前项目有 `.codex/local-environment.json` 就同步或修改其他目录下的 skill 副本。
- 不能把全局 `~/.codex/skills/...` 的缓存或路径当成当前项目范围证据。
- 不能为了补齐缓存 schema 查找无关技术栈或写入未验证路径。
- 不能在用户已限定当前项目时，只用当前 cwd 口头说明范围而不核对本项目 active cache path 和忽略规则。

## 当前工具与技术栈动态追加门禁

本节用于第三方工具、中转层、模型路由、IDE/MCP、CLI wrapper、hook/subagent、CI/chatops 或未知宿主把编程任务转入当前上下文时的环境判断。环境缓存不能被限定为某个固定平台、固定技术栈或某台机器路径；必须由当前使用的工具、当前命令和当前触碰文件动态决定。

触发信号：

- 当前任务准备执行或复核构建、编译、测试、lint、format、typecheck、运行、预览、打包、发布前校验或代码生成。
- 第三方输出里出现命令、工具名、工作目录、模块路径、版本、环境变量、lockfile、虚拟环境、开发者工具、IDE 运行配置或 CI job。
- 任务来自未知宿主或中转层，但载荷包含文件扩展名、配置文件、错误日志、diff、补丁或工具动作。
- 现有缓存、命令输出或页面/日志出现中文乱码、`encoding`、`charset`、locale、跨平台文件名或终端输出异常。

处理顺序：

1. 先确定当前任务的项目根和触碰范围，不能把全局 skill 目录、用户级 `.codex` 或第三方配置目录当成业务项目根。
2. 从当前证据识别实际工具链：命令名、脚本名、文件扩展名、最近配置文件、lockfile、错误类型、IDE 配置和 active cache path。产品名或 agent 名只作为线索，不参与工具链优先级。
3. 只读取命中的技术栈配置：Java/Maven、Node/前端、小程序、Python 或其他最贴近的项目配置。未命中某技术栈时，不为补齐缓存去扫描、验证或写入该技术栈字段。
4. 若未知技术栈没有专属 reference，仍使用本文件的 active cache path、`.codex/` 忽略规则、locale/encoding 证据和 `01` 的跨技术栈验证策略；命令选择来自项目脚本、README、CI 或第三方载荷，不能凭个人习惯臆造。
5. 第三方已经执行过命令时，只有能证明 root/workspace、命令、工具版本、active cache path、触碰范围覆盖和当前 diff 匹配，才可作为验证证据；否则补做最轻量非交互验证或说明无法验证。

写入缓存时必须记录当前证据来源：

- `toolContext.host`：当前宿主或中转层；未知时写 `unknownHost`。
- `toolContext.action`：build/test/lint/typecheck/format/run/codegen 等动作。
- `toolContext.evidence`：触发本次工具链判断的命令、文件、配置、日志或 diff。
- `toolContext.references`：本轮实际追加的技术栈 reference；未追加其他技术栈的原因。

禁止行为：

- 不能把当前 shell 可用的 `mvn/node/python` 当作项目工具链事实。
- 不能把某个第三方 agent 的默认工作目录当作项目根。
- 不能把未列名工具或未列名技术栈视为“不需要缓存/验证”；至少要完成项目根、命令来源、active cache path 和最轻量验证边界。
- 不能为了第三方兼容写入个人绝对路径、token、密钥、上传凭证或供应商特有的不可迁移路径。

## 跨系统缓存文件命名

本节是内部自动门禁。任何创建、读取、迁移或更新本地环境缓存的流程，都必须先解析跨 Windows/macOS/Linux 兼容的缓存文件名；不能只用单一固定文件名，也不能只用 hostname 区分不同用户和机器。

文件布局：

- 缓存目录固定为 `<project-root>/.codex/`，目录本身必须被 Git root 的 `.gitignore` 忽略。
- 新写入优先使用 profile 文件：`<project-root>/.codex/local-environment.<profile>.json`。
- 旧版文件 `<project-root>/.codex/local-environment.json` 只允许作为一次性迁移输入；新规则下不再作为 fallback，也不再为旧工具保留兼容写入。
- 若旧版文件存在，读取其中可解析且仍适用于当前工作区的字段，立即生成或更新 active profile 文件，并把 `identity.migratedFrom` 记录为 `.codex/local-environment.json`。迁移成功后优先删除旧版文件；删除失败时记录原因，但后续命令选择仍只能使用 profile 文件。

`<profile>` 生成规则：

1. 采集 `os`、`arch`、当前用户名、当前主机名或计算机名。
2. 主机名只能作为可读标签，不能作为唯一 ID：用户可改名，局域网和组织内可能重复，macOS 局域网重名时还可能自动追加数字。
3. 生成或复用 `profileId`：优先复用当前 profile 文件里的 `identity.profileId`；没有时生成随机 UUID，并在文件内容中保存完整 UUID。
4. 文件名使用短 id：`local-environment.<os>-<arch>-<safe-user>-<safe-host>-<id8>.json`，其中 `<id8>` 是 `profileId` 的前 8 到 12 个十六进制字符。若检测到同名文件但 `identity` 不匹配，追加新的随机短 id，不能覆盖。
5. `safe-user` 和 `safe-host` 只用于可读性，必须按跨系统规则清洗后再入文件名。

跨系统文件名清洗规则：

- 统一转小写；优先保留 ASCII 字母、数字、点、短横线和下划线。
- 空白、中文、emoji、路径分隔符和 Windows 禁用字符 `< > : " / \ | ? *` 统一替换为 `-`，连续 `-` 折叠为一个。
- 去掉首尾空格、点和短横线；空值用 `unknown`。
- 不生成 Windows 保留设备名：`con`、`prn`、`aux`、`nul`、`com1` 到 `com9`、`lpt1` 到 `lpt9`；命中时加前缀 `x-`。
- 不依赖大小写区分文件；`Alice-Mac` 和 `alice-mac` 视为同一个 slug。
- 单段 slug 控制在 32 字符以内，完整文件名控制在 120 字符以内，避免 Windows 路径长度和同步工具兼容问题。

缓存内容必须包含：

- `schemaVersion`：当前缓存 schema 版本。
- `workspaceRoot`：当前项目根的绝对路径。
- `cacheFile`：当前 active cache path。
- `identity`：`profileId`、`os`、`arch`、`username`、`hostname`、`safeUser`、`safeHost`、`createdAt`、`updatedAt`。
- 各技术栈已验证的工具链字段。不得写入 token、密钥、registry 凭据、上传凭证或个人隐私备注。

## 构建测试前环境缓存门禁

本节是自动门禁，属于流程内置前置步骤。只要本 skill 的执行流程进入构建、编译、测试、lint、typecheck、运行、预览、打包、发布前校验或代码生成节点，就必须先从当前任务项目根解析并处理 active cache path。

执行顺序：

1. 定位项目根：优先 `git rev-parse --show-toplevel`；非 Git 项目按当前触碰文件向上查找 `pom.xml`、`package.json`、`pyproject.toml`、`project.config.json` 等根标志。
2. 解析缓存路径：按 [跨系统缓存文件命名](#跨系统缓存文件命名) 得到 active cache path；不得使用父目录、其他仓库或全局 skill 目录的缓存。
3. 缓存存在：
   - JSON 可解析且包含当前命令所需工具链时，优先直接使用缓存中的 `executable`、`home`、`localRepository`、`packageManager.executable`、`python.executable`、`devtoolsCli` 等路径组装命令。
   - 缓存缺少 `workspaceRoot` 时，不阻断使用；按当前项目根保守补充判断，并在下次需要更新缓存时写入 `workspaceRoot`。
   - 只有缓存路径不存在、JSON 无法解析、项目配置明确变化、缓存不满足当前命令或命令失败疑似环境问题时，才进入重新发现。
4. 编码与 locale 核对：
   - 若当前任务、工具输出或待执行命令涉及中文字符、非 ASCII 文案、乱码、`encoding`、`charset`、`UTF-8`/`GBK`、终端输出、资源编译、日志或跨平台文件名，必须同时读取 `01#跨技术栈编码与中文乱码门禁`。
   - active cache path 中已有 locale、source encoding、前端 `frontendQuality`、Python 解释器或 Maven source encoding 记录时，先核对是否仍匹配当前项目配置；缺失时只补当前命令需要且可验证的字段。
   - 不为了处理乱码直接全局改 shell 配置、IDE 全局编码或系统 locale；只能记录当前项目命令需要的环境变量、项目配置和验证命令。
5. 缓存不存在：
   - 创建 `<project-root>/.codex/` 目录。
   - 按当前命令命中的技术栈读取项目配置，再按 `14-environment-cache-by-stack.md` 查找本机候选、执行最小验证。
   - 验证通过后创建 active cache path，只写当前命令需要且已验证的字段，不为补齐 schema 写空值或猜测值。
6. 执行命令：使用缓存路径或新验证路径执行原目标命令；不要回退到未验证全局命令。
7. 命令失败：
   - 如果错误可能来自工具路径、版本、依赖、锁文件、脚本、模块路径、workspace/filter、虚拟环境、框架平台、本地仓库或开发者工具路径不匹配，必须重新读取项目配置和本机候选环境。
   - 如果错误或输出可能来自字符集、locale、资源编码、终端编码、文件名编码、HTTP charset 或前端页面 charset 不匹配，必须执行 `01#跨技术栈编码与中文乱码门禁`，并按当前技术栈重新核对编码配置后重试一次原命令。
   - 找到更匹配环境后更新 active cache path，并用同一目标命令重试一次。
   - 重试仍失败时，停止连续重试，区分环境问题、依赖缺失、项目历史失败和本次改动问题。
8. 忽略规则：创建或更新缓存后，必须确认项目根 `.gitignore` 覆盖 `/.codex/`，没有则补齐并用 `git check-ignore -v .codex/ .codex/local-environment*.json` 验证。

禁止行为：

- 不允许先跑构建/测试失败后才想起检查缓存。
- 不允许因为当前 shell 有 `mvn/node/python` 就跳过项目根缓存。
- 不允许把缓存缺失转交给用户手动指定路径；应先自动发现、验证并创建。
- 不允许在缓存可用时重复全盘查找环境。

## 发现顺序

1. 读取工作区缓存：先按 [跨系统缓存文件命名](#跨系统缓存文件命名) 解析 active cache path，再读取 profile 文件；旧版 `.codex/local-environment.json` 存在时先强制迁移替换，不作为 fallback。
2. 读取 IDE/项目配置，按当前项目、当前工具动作和实际命中的技术栈选择，不一次性读取所有配置：
   - IDE：`.idea/misc.xml`、`.idea/workspace.xml`、`.idea/compiler.xml`、`.idea/jarRepositories.xml`。
   - Java/Maven：`.mvn/maven.config`、`.mvn/jvm.config`、`.mvn/wrapper/maven-wrapper.properties`、`pom.xml`。
   - Node/前端：目标 package 的 `package.json`、lockfile、`engines`、`packageManager`、`scripts`、`.nvmrc`、`.node-version`、`.tool-versions`、Volta 配置、`.npmrc`、`.yarnrc.yml`、构建工具配置。
   - 小程序：`project.config.json`、`project.private.config.json`、`app.json`、`pages.json`、`manifest.json`、`app.config.*`、`config/index.*`。
   - Python：`pyproject.toml`、`requirements*.txt`、`uv.lock`、`poetry.lock`、`Pipfile.lock`、`tox.ini`、`noxfile.py`、`pytest.ini`、`.python-version`、`.tool-versions`、`.venv/pyvenv.cfg`。
3. 读取 shell 环境和常见命令，只查当前任务需要的候选：`JAVA_HOME`、`MAVEN_HOME`、`M2_HOME`、`PATH`、`which mvn/node/npm/pnpm/yarn/bun/corepack/python/python3/uv/poetry/pytest`、微信开发者工具 CLI 候选路径。
4. 查找本机常见路径，只做小范围候选，不全盘扫描：
   - 当前任务上下文中已提供且可验证的 Maven 路径和本地仓库路径。
   - `~/dev/maven-*/bin/mvn`
   - `~/.sdkman/candidates/maven/*/bin/mvn`
   - `~/.m2/repository`
   - `/opt/homebrew/bin/mvn`
   - `/usr/local/bin/mvn`
   - `mvn`
   - `/Library/Java/JavaVirtualMachines/*/Contents/Home`
   - `<workspace>/.venv/bin/python`
   - `/opt/homebrew/bin/python3`
   - `/usr/local/bin/python3`
   - `/opt/homebrew/bin/uv`
   - `/usr/local/bin/uv`
   - `/opt/homebrew/bin/node`
   - `/usr/local/bin/node`
   - `/opt/homebrew/bin/pnpm`
   - `/usr/local/bin/pnpm`
   - `/Applications/wechatwebdevtools.app/Contents/MacOS/cli`
   - `/Applications/微信开发者工具.app/Contents/MacOS/cli`
5. 找到候选后执行最小验证。
6. 验证通过后写入 active cache path，下次优先复用。

## 自动环境缓存维护

只要任务需要使用 Maven/JDK/Node/Python/小程序开发者工具等本机工具链执行构建、编译、测试、lint、typecheck、运行、预览、打包、发布前校验或代码生成，就自动前置执行本流程；不需要额外提出维护本地环境缓存。具体执行顺序先按 [构建测试前环境缓存门禁](#构建测试前环境缓存门禁) 处理项目根缓存，再进入当前技术栈发现。

触发场景：

- 即将执行 `mvn`、`java`、`node`、`npm`、`pnpm`、`yarn`、`bun`、`python`、`pytest`、`uv`、`poetry`、`tox`、`nox`、微信开发者工具 CLI、`miniprogram-ci`、Taro/uni-app 构建命令，以及 lint、typecheck、compile、codegen 等项目脚本。
- 构建、编译、测试、运行命令失败，且失败原因可能是工具路径、版本、`JAVA_HOME`、本地 Maven 仓库、包管理器、虚拟环境、开发者工具路径或工作目录不匹配。
- 构建、编译、测试、运行、lint、format、typecheck 或日志输出出现中文乱码、字符集异常、`encoding`/`charset`/locale 错误、文件名编码问题或资源过滤乱码。
- 任务目标直接涉及强化、补齐或更新 `.codex/local-environment.json`、profile 环境缓存、主机名/用户名区分、跨 Windows/macOS 文件名兼容或 `.codex/` 忽略规则；其中旧版 `.codex/local-environment.json` 必须自动迁移替换为 profile 缓存。

执行步骤：

1. 定位工作区根：
   - 优先使用当前任务路径所在的 Git root：`git rev-parse --show-toplevel`。
   - 如果不是 Git 仓库，使用当前工作目录或任务上下文中的路径向上查找项目根标志，例如 `pom.xml`、`package.json`、`pyproject.toml`、`project.config.json`。
2. 按 [跨系统缓存文件命名](#跨系统缓存文件命名) 解析 active cache path：
   - 文件存在且 JSON 可解析时，逐项验证已记录的 `executable`、`home`、`localRepository`、`devtoolsCli` 等路径。
   - 已验证且仍可用的值直接复用，不重复查找本机候选。
   - 已有缓存满足当前命令所需工具链时，直接用缓存中的路径重新组装命令并执行原构建/编译/测试/运行任务。
   - 路径缺失、命令失败、项目配置变化或工具版本明显不匹配时，标记该项失效并重新发现；不要继续用失效路径盲跑。
3. 读取项目配置并选择最贴近项目的环境：
   - Maven/Java 项目必须先按 `14-environment-cache-by-stack.md#mavenjava-环境缓存` 读取 `pom.xml`、`.mvn/*`、wrapper、Java/Maven 版本约束和模块结构，选择匹配度最高的 JDK、Maven 和构建 root。
   - Node/前端项目必须先按 `14-environment-cache-by-stack.md#node前端环境缓存` 读取目标 `package.json`、lockfile、`engines`、`packageManager`、`scripts`，以及 ESLint/Prettier/EditorConfig/Biome/Stylelint/TypeScript 等语法、缩进和格式规范文件，选择匹配度最高的 Node、包管理器和脚本命令。
   - Python 项目必须先按 `14-environment-cache-by-stack.md#python-环境缓存` 读取 `pyproject.toml`、锁文件、requirements、tox/nox、版本文件和虚拟环境配置，选择匹配度最高的 Python、管理器和命令入口。
   - 小程序项目必须先按 `14-environment-cache-by-stack.md#小程序环境缓存` 读取平台配置、框架配置、输出目录和必要的 `package.json`，选择匹配度最高的小程序框架、目标平台、源码目录、构建脚本和 Node 包管理器。
   - 只读取当前任务命中的技术栈配置，不为了补全缓存扫描无关技术栈。
4. 查找本机候选：
   - 只在缓存或项目配置无法提供可用路径时执行。
   - 只查当前任务需要的候选路径，不全盘扫描。
5. 执行最小验证：
   - Maven/JDK、Node、Python、小程序开发者工具按 [公共验证矩阵](#公共验证矩阵) 验证。
   - Maven 后端若项目声明 Java 8，但默认 `mvn -version` 使用更高 JDK，应优先尝试带 `JAVA_HOME=<project-jdk>` 的验证命令，并把项目目标 Java 版本和验证 JDK 分开记录。
   - 命中编码/乱码风险时，同时记录本次命令使用的 locale、source encoding、前端规范文件、Python 文件 IO 编码或小程序/页面 charset 依据；只记录可验证证据，不写未验证猜测。
6. 写回缓存：
   - 只写验证通过的字段。
   - 更新 `updatedAt`、`workspaceRoot`，能确认 Maven 聚合 root 时写入 `mavenRoot`。
   - 不写入密钥、token、上传凭证、生产白名单、临时失败日志或未验证猜测。
7. 重试原任务命令：
   - 缓存更新后，使用新缓存路径重新执行原本要跑的构建、编译、测试、运行或预览命令。
   - Maven 命令必须使用缓存中的 `maven.executable` 和 `maven.localRepository`；项目需要特定 JDK 时带上已验证的 `JAVA_HOME`。
   - Node/Python/小程序命令必须使用项目声明的包管理器、解释器、虚拟环境或开发者工具路径，不回退到未验证全局命令。
   - 若重试仍失败，先区分环境问题、项目历史失败、依赖缺失和本次改动问题，不继续无限重试。
8. 自动检查忽略文件：
   - 在 Git root 检查 `.gitignore` 是否已经忽略 `.codex/`：优先用 `git check-ignore -v .codex/ .codex/local-environment*.json` 验证。
   - 若未忽略，读取根 `.gitignore`；存在则追加 `/.codex/`，不存在则新建根 `.gitignore` 并写入 `/.codex/`。
   - 不修改子目录 `.gitignore` 来替代根忽略规则，除非项目本身不是 Git 仓库且用户只给了子项目目录。
   - 写入后再次用 `git check-ignore -v` 验证。

完成后必须汇报：

- 复用了哪些缓存项。
- 新发现并验证了哪些路径。
- 更新了哪些缓存字段。
- 是否已使用缓存路径执行或重试原构建、编译、测试、运行命令。
- `.codex/` 是否已被根忽略文件覆盖，是否新增或修改了 `.gitignore`。
- 哪些路径或工具未找到、未验证或因项目配置不需要而未处理。

## Maven/Java 环境缓存

旧锚点保留。详细规则下沉到 `14-environment-cache-by-stack.md#mavenjava-环境缓存`。

## Node/前端环境缓存

旧锚点保留。详细规则下沉到 `14-environment-cache-by-stack.md#node前端环境缓存`。

## Python 环境缓存

旧锚点保留。详细规则下沉到 `14-environment-cache-by-stack.md#python-环境缓存`。

## 小程序环境缓存

旧锚点保留。详细规则下沉到 `14-environment-cache-by-stack.md#小程序环境缓存`。

## 公共验证矩阵

只验证当前任务实际需要的工具；不要为了补全缓存而安装、扫描或验证无关技术栈。

| 场景 | 最小验证 | 记录要点 | 差异规则 |
| --- | --- | --- | --- |
| Maven/JDK | `<mavenExecutable> -version`，必要时验证 `JAVA_HOME` 和 `java -version` | `mavenRoot`、`modulePath`、`maven.executable`、`maven.localRepository`、`java.home/version/versionRequirement`、来源 | 先按 `14` 的 Maven/Java 环境缓存匹配，再按 `03` 执行构建 |
| Node/前端 | `node --version`，项目实际包管理器 `--version`，必要时验证 `corepack --version` | `node.executable`、`node.version`、`packageManager.name/executable/version`、`packageJson`、`packageRoot`、lockfile、scripts、selectedCommand、`frontendQuality` 规范文件集合、来源 | 先按 `14` 的 Node/前端环境缓存匹配，再按 `11` 执行构建、lint、format 或 typecheck |
| Python | `<pythonExecutable> --version`，项目实际管理器或测试工具 `--version` | `python.executable/version/versionRequirement`、`manager`、`packageRoot`、项目配置文件、lockfile、来源 | 先按 `14` 的 Python 环境缓存匹配，再按 `10` 执行命令 |
| 小程序 | 项目实际构建 CLI `--version`、构建脚本 dry check，只有明确需要时验证 `<wechatDevtoolsCli> --help` | `framework`、`platform`、`projectConfig`、`sourceRoot`、`outputRoot`、`buildCommand`、`devtoolsCli`、来源 | 先按 `14` 的小程序环境缓存匹配，再按 `12` 执行构建/CI |

公共约束：

- 工具路径、版本、来源和验证命令必须对应同一个工作区。
- 只把验证通过的候选写入缓存。
- 不把临时全局安装、错误目录下的 lockfile 判断、未验证解释器、未验证开发者工具路径写入缓存。
- 不把密钥文件内容、CI 上传凭证、真实 appid 私钥、机器人编号、生产白名单写入缓存或长期记忆。

## 缓存结构

缓存文件路径：

```text
.codex/local-environment.<os>-<arch>-<safe-user>-<safe-host>-<id8>.json
```

旧版 `.codex/local-environment.json` 不再作为 fallback。发现旧版时必须先迁移替换到 profile 文件，具体命名规则见 [跨系统缓存文件命名](#跨系统缓存文件命名)。

推荐结构：

```json
{
  "schemaVersion": 2,
  "updatedAt": "YYYY-MM-DDTHH:mm:ssZ",
  "scope": "workspace",
  "workspaceRoot": "/path/to/workspace",
  "cacheFile": "/path/to/workspace/.codex/local-environment.darwin-arm64-safe-user-safe-host-a1b2c3d4.json",
  "identity": {
    "profileId": "a1b2c3d4-1111-2222-3333-444455556666",
    "os": "darwin|windows|linux",
    "arch": "arm64|x64",
    "username": "raw-user-name",
    "hostname": "raw-host-name",
    "safeUser": "raw-user-name",
    "safeHost": "raw-host-name",
    "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
    "updatedAt": "YYYY-MM-DDTHH:mm:ssZ"
  },
  "mavenRoot": "/path/to/workspace/module-root",
  "modulePath": "server/service-a",
  "maven": {
    "source": "project-config|ide-config|verified-local-candidate|cache",
    "executable": "/path/to/mvn",
    "wrapper": "/path/to/workspace/mvnw",
    "localRepository": "/path/to/repository",
    "mavenConfig": ".mvn/maven.config",
    "artifactId": "service-a",
    "selectedCommand": "/path/to/mvn -Dmaven.repo.local=/path/to/repository -pl server/service-a -am compile",
    "verifiedCommand": "/path/to/mvn -version",
    "verified": true,
    "sourceEncoding": "UTF-8"
  },
  "java": {
    "source": "pom|ide-config|verified-local-candidate|cache",
    "home": "/path/to/jdk",
    "executable": "/path/to/jdk/bin/java",
    "version": "17.0.10",
    "versionRequirement": "17",
    "compilerRelease": "17",
    "verifiedCommand": "JAVA_HOME=/path/to/jdk /path/to/mvn -version",
    "verified": true
  },
  "node": {
    "source": "project-config|verified-local-candidate|cache",
    "packageRoot": "/path/to/workspace/frontend-app",
    "packageJson": "/path/to/workspace/frontend-app/package.json",
    "executable": "/path/to/node",
    "version": "20.11.1",
    "versionRequirement": ">=18 <21",
    "packageManager": {
      "name": "pnpm|npm|yarn|bun",
      "executable": "/path/to/pnpm",
      "version": "9.0.0",
      "declared": "pnpm@9.0.0",
      "commandRunner": "npm|npx|pnpm|pnpm dlx|yarn|yarn dlx|bun"
    },
    "lockfile": "pnpm-lock.yaml",
    "scripts": {
      "build": "vite build",
      "typecheck": "vue-tsc --noEmit",
      "lint": "eslint ."
    },
    "selectedCommand": "pnpm run build",
    "verifiedCommand": "node --version && pnpm --version",
    "verified": true,
    "locale": {
      "LANG": "zh_CN.UTF-8",
      "LC_ALL": ""
    }
  },
  "python": {
    "source": "project-venv|project-config|verified-local-candidate|cache",
    "packageRoot": "/path/to/workspace/python-app",
    "configFile": "/path/to/workspace/python-app/pyproject.toml",
    "executable": "/path/to/python",
    "version": "3.11.8",
    "versionRequirement": ">=3.10,<3.13",
    "manager": {
      "name": "uv|poetry|pipenv|venv|conda|system",
      "executable": "/path/to/uv",
      "version": "0.5.0"
    },
    "venv": "/path/to/workspace/python-app/.venv",
    "lockfile": "uv.lock",
    "selectedCommand": "uv run python -m pytest tests/test_example.py",
    "verifiedCommand": "/path/to/python --version && /path/to/uv --version",
    "verified": true
  },
  "miniprogram": {
    "source": "project-config|verified-local-candidate|cache",
    "framework": "native-weapp|uni-app|taro|other",
    "platform": "weapp|alipay|tt|swan|qq|jd|ks|other",
    "projectConfig": "/path/to/workspace/project.config.json",
    "packageRoot": "/path/to/workspace/miniprogram",
    "packageJson": "/path/to/workspace/miniprogram/package.json",
    "sourceRoot": "src|.",
    "outputRoot": "dist|unpackage/dist/dev/mp-weixin",
    "buildCommand": "pnpm run build:weapp",
    "devtoolsCli": "/path/to/devtools-cli",
    "verifiedCommand": "pnpm --version",
    "verified": true
  },
  "git": {
    "ignoreFile": "/path/to/workspace/.gitignore",
    "codexIgnored": true,
    "ignorePattern": "/.codex/"
  }
}
```

只写当前工作区已验证且当前任务需要的字段，不为了补齐 schema 写入空值、猜测值或其他技术栈字段。

## 缓存策略

缓存规则：

- 首次发现才查找本机候选路径。
- 已有缓存且验证仍通过时，直接使用缓存。
- 项目配置显式指定路径时，项目配置优先于旧缓存。
- 缓存失效时，说明原因并重新发现。
- `.codex/local-environment.<profile>.json` 是当前唯一有效的本地环境缓存文件；旧版 `.codex/local-environment.json` 迁移成功后不再保留或使用。环境缓存不提交到仓库。
- hostname 不是唯一 ID，只能作为可读标签；真实区分依赖 `profileId`、`os`、`arch`、用户名、hostname 和 workspaceRoot 共同判断。

## 写入边界

- 允许写入当前工作区的 `.codex/local-environment.<profile>.json`；旧版 `.codex/local-environment.json` 只在强制迁移替换时读取，迁移后不再读取或写入旧版格式。
- 不自动修改用户全局 shell 配置、IDE 配置、Maven settings 或系统环境变量。
- 不把临时失败日志写入缓存。
- 不把未验证路径写入缓存。

## 与长期记忆的关系

- 本地缓存记录“这个工作区当前可用的环境路径”。
- 长期 memory 只记录稳定偏好，例如“优先从 IDE 配置和本地缓存发现 Maven”；不记录某台机器的 Maven、JDK、Node、Python 绝对路径。
- 只有存在明确的长期 memory 更新授权时，才按 memory 规则写入长期记忆更新请求。
