# 环境发现与缓存

用于 Maven、JDK、Node、Python、包管理器、IDE 配置路径、小程序开发者工具等本机环境。目标是提供跨技术栈统一的“发现、验证、缓存”机制，避免硬编码路径或重复全盘查找。

本文件只管环境路径和工具可用性，不替代各技术栈的运行、构建、测试规则：

- Maven 构建和多模块命令见 `03-maven-backend-build.md`。
- Python 依赖、运行、测试、lint/type check 见 `10-python-development.md`。
- Vue/React 包管理、运行、构建、测试见 `11-frontend-vue-react.md`。
- 小程序原生/uni-app/Taro 的源码/产物目录、模拟器、构建和发布见 `12-miniprogram-development.md`。

## 目录

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

## 发现顺序

1. 读取工作区缓存：`.codex/local-environment.json`。
2. 读取 IDE/项目配置，按当前项目实际命中的技术栈选择，不一次性读取所有配置：
   - IDE：`.idea/misc.xml`、`.idea/workspace.xml`、`.idea/compiler.xml`、`.idea/jarRepositories.xml`。
   - Java/Maven：`.mvn/maven.config`、`.mvn/jvm.config`、`.mvn/wrapper/maven-wrapper.properties`、`pom.xml`。
   - Node/前端：目标 package 的 `package.json`、lockfile、`engines`、`packageManager`、`scripts`、`.nvmrc`、`.node-version`、`.tool-versions`、Volta 配置、`.npmrc`、`.yarnrc.yml`、构建工具配置。
   - 小程序：`project.config.json`、`project.private.config.json`、`app.json`、`pages.json`、`manifest.json`、`app.config.*`、`config/index.*`。
   - Python：`pyproject.toml`、`requirements*.txt`、`uv.lock`、`poetry.lock`、`Pipfile.lock`、`tox.ini`、`noxfile.py`、`pytest.ini`、`.python-version`、`.tool-versions`、`.venv/pyvenv.cfg`。
3. 读取 shell 环境和常见命令，只查当前任务需要的候选：`JAVA_HOME`、`MAVEN_HOME`、`M2_HOME`、`PATH`、`which mvn/node/npm/pnpm/yarn/bun/corepack/python/python3/uv/poetry/pytest`、微信开发者工具 CLI 候选路径。
4. 查找本机常见路径，只做小范围候选，不全盘扫描：
   - 用户明确提供过的 Maven 路径和本地仓库路径。
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
6. 验证通过后写入 `.codex/local-environment.json`，下次优先复用。

## 自动环境缓存维护

只要任务需要使用 Maven/JDK/Node/Python/小程序开发者工具等本机工具链执行构建、编译、测试、运行、预览、打包、发布前校验或代码生成，就自动前置执行本流程；不需要等用户显式提出维护 `.codex/local-environment.json`。

触发场景：

- 即将执行 `mvn`、`java`、`node`、`npm`、`pnpm`、`yarn`、`bun`、`python`、`pytest`、`uv`、`poetry`、`tox`、`nox`、微信开发者工具 CLI、`miniprogram-ci`、Taro/uni-app 构建命令等。
- 构建、编译、测试、运行命令失败，且失败原因可能是工具路径、版本、`JAVA_HOME`、本地 Maven 仓库、包管理器、虚拟环境、开发者工具路径或工作目录不匹配。
- 任务目标直接涉及强化、补齐或更新 `.codex/local-environment.json`。

执行步骤：

1. 定位工作区根：
   - 优先使用当前任务路径所在的 Git root：`git rev-parse --show-toplevel`。
   - 如果不是 Git 仓库，使用用户给定路径向上查找项目根标志，例如 `pom.xml`、`package.json`、`pyproject.toml`、`project.config.json`。
2. 读取 `<workspace>/.codex/local-environment.json`：
   - 文件存在且 JSON 可解析时，逐项验证已记录的 `executable`、`home`、`localRepository`、`devtoolsCli` 等路径。
   - 已验证且仍可用的值直接复用，不重复查找本机候选。
   - 已有缓存满足当前命令所需工具链时，直接用缓存中的路径重新组装命令并执行原构建/编译/测试/运行任务。
   - 路径缺失、命令失败、项目配置变化或工具版本明显不匹配时，标记该项失效并重新发现；不要继续用失效路径盲跑。
3. 读取项目配置并选择最贴近项目的环境：
   - Maven/Java 项目必须先按 [Maven/Java 环境缓存](#mavenjava-环境缓存) 读取 `pom.xml`、`.mvn/*`、wrapper、Java/Maven 版本约束和模块结构，选择匹配度最高的 JDK、Maven 和构建 root。
   - Node/前端项目必须先按 [Node/前端环境缓存](#node前端环境缓存) 读取目标 `package.json`、lockfile、`engines`、`packageManager` 和 `scripts`，选择匹配度最高的 Node、包管理器和脚本命令。
   - Python 项目必须先按 [Python 环境缓存](#python-环境缓存) 读取 `pyproject.toml`、锁文件、requirements、tox/nox、版本文件和虚拟环境配置，选择匹配度最高的 Python、管理器和命令入口。
   - 小程序项目必须先按 [小程序环境缓存](#小程序环境缓存) 读取平台配置、框架配置、输出目录和必要的 `package.json`，选择匹配度最高的小程序框架、目标平台、源码目录、构建脚本和 Node 包管理器。
   - 只读取当前任务命中的技术栈配置，不为了补全缓存扫描无关技术栈。
4. 查找本机候选：
   - 只在缓存或项目配置无法提供可用路径时执行。
   - 只查当前任务需要的候选路径，不全盘扫描。
5. 执行最小验证：
   - Maven/JDK、Node、Python、小程序开发者工具按 [公共验证矩阵](#公共验证矩阵) 验证。
   - Maven 后端若项目声明 Java 8，但默认 `mvn -version` 使用更高 JDK，应优先尝试带 `JAVA_HOME=<project-jdk>` 的验证命令，并把项目目标 Java 版本和验证 JDK 分开记录。
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
   - 在 Git root 检查 `.gitignore` 是否已经忽略 `.codex/`：优先用 `git check-ignore -v .codex/local-environment.json .codex/` 验证。
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

Java 编译、Maven 构建、测试、代码生成或后端模块验证前，必须先以目标模块和聚合 root 为单位解析环境，不只看当前 shell 的 `mvn`。

读取顺序：

1. 定位目标 `pom.xml` 和聚合 root：
   - 优先使用本次触碰 Java/Kotlin/资源/测试文件向上最近的 `pom.xml`。
   - 向上读取父级 `pom.xml`，确认 `packaging=pom`、`modules`、`parent.relativePath` 和目标模块是否在聚合链路内。
   - 多层 Maven 项目记录 `mavenRoot`、目标 `modulePath`、`groupId`、`artifactId`，构建命令默认从聚合 root 执行。
2. 读取 Java 和 Maven 约束：
   - `pom.xml` 的 `properties`：`java.version`、`maven.compiler.release`、`maven.compiler.source`、`maven.compiler.target`、`project.build.sourceEncoding`。
   - `maven-compiler-plugin`、`maven-surefire-plugin`、`maven-failsafe-plugin`、`toolchains-maven-plugin` 等关键插件配置。
   - `.mvn/maven.config`、`.mvn/jvm.config`、`.mvn/wrapper/maven-wrapper.properties`、`mvnw`、`mvnw.cmd`。
   - IDE 配置只作为补充，不覆盖项目 `pom.xml`、wrapper 和 `.mvn/*` 的明确约束。
3. 匹配本机环境：
   - 优先复用 `.codex/local-environment.json` 中同一 `mavenRoot`、`modulePath`、Java 版本约束和 Maven/wrapper 仍匹配的缓存。
   - 项目存在并要求 Maven Wrapper 时优先验证 `./mvnw -version`；否则验证缓存或本机 Maven 候选。
   - JDK 必须满足 `release/source/target/java.version` 或 toolchain 约束；若默认 `mvn -version` 使用的 JDK 不匹配，继续查找 `JAVA_HOME`、IDE JDK 或本机 JDK 候选。
4. 选择命令：
   - 构建命令只从项目结构和任务目标推导：`compile`、`package -DskipTests`、`test` 或定向 `-Dtest=...`。
   - 多模块项目优先使用 `-pl <modulePath> -am`；路径不可用时再用 `-pl :<artifactId> -am`。
   - 不因为当前目录在子模块内就直接跑子模块 Maven，除非聚合链路无法确认。
5. 写入缓存：
   - 写入 `mavenRoot`、`modulePath`、`artifactId`、Java 版本约束、实际 JDK home/version、Maven/wrapper 路径、localRepository、`.mvn` 配置摘要、选定命令和验证命令。
   - Java 目标版本和 Maven 实际运行 JDK 要分开记录，避免把“能运行 Maven 的 JDK”误当成“项目目标 JDK”。

Maven/Java 命令失败后的重算：

- 如果失败信息涉及 JDK 版本、`release/source/target`、`JAVA_HOME`、Maven 版本、wrapper、本地仓库、插件版本、依赖解析、模块路径、`-pl` 选择、toolchain 或 surefire/failsafe 选择，必须重新读取 `pom.xml`、`.mvn/*`、wrapper、IDE 配置和本机候选环境。
- 若发现更匹配的 JDK、Maven、wrapper、localRepository 或模块参数，更新 `.codex/local-environment.json` 后，用同一目标命令重试一次。
- 若重试仍失败，停止连续盲改，区分环境不匹配、依赖未拉取、项目历史失败、测试选择错误和本次代码问题。

## Node/前端环境缓存

前端编译、构建、typecheck、lint 或测试前，必须先以目标 package 为单位解析环境，不只看仓库根。

读取顺序：

1. 定位目标 `package.json`：
   - 优先使用本次触碰文件向上最近的 `package.json`。
   - monorepo/workspace 项目再读取 workspace root 的 `package.json`、`pnpm-workspace.yaml`、`yarn workspaces`、`npm workspaces` 或项目既有 filter 方式。
   - 不因为根目录有 `package.json` 就忽略子包的 `package.json`。
2. 读取目标 `package.json` 字段：
   - `scripts`：优先选择与当前任务匹配的 `build`、`typecheck`、`lint`、`test`、`compile`、框架自定义脚本；不要臆造不存在的脚本。
   - `dependencies`、`devDependencies`：识别 Vue 2/3、React、Vite、Next、Nuxt、Vue CLI、Taro、uni-app、TypeScript、ESLint 等工具链版本。
   - `engines.node`、`engines.npm`、`packageManager`、Volta 配置：作为 Node 和包管理器版本约束。
3. 读取锁文件和包管理器配置：
   - `pnpm-lock.yaml` -> 默认 `pnpm`。
   - `yarn.lock`、`.yarnrc.yml` -> 默认 `yarn`，注意 Yarn classic 与 berry。
   - `package-lock.json`、`npm-shrinkwrap.json` -> 默认 `npm`。
   - `bun.lockb`、`bun.lock` -> 默认 `bun`。
   - 没有 lockfile 时再按 `packageManager`、项目 README/CI、scripts 中的命令前缀判断。
4. 选择命令：
   - 优先使用 `package.json` 里已存在的 scripts，例如 `<pm> run build`、`<pm> run typecheck`、`<pm> run lint`。
   - 如果 scripts 明确使用 `npx`、`pnpm dlx`、`yarn dlx` 或框架 CLI，记录为 `commandRunner`，但不要把 `npx` 误判为包管理器。
   - workspace 子包优先使用项目既有 filter/workspace 命令；没有项目范式时，在目标 package 目录执行该 package 的 script。
5. 匹配本机环境：
   - 优先复用 `.codex/local-environment.json` 中同一 `packageJson`、lockfile、Node 约束和包管理器仍匹配的缓存。
   - 缓存缺失或不匹配时，查找本机 Node、corepack、npm、pnpm、yarn、bun 候选，并验证版本。
   - Node 版本不满足 `engines.node`、`.nvmrc`、`.node-version`、Volta 或构建工具最低要求时，继续查找本机候选；找不到则说明缺口，不用不匹配版本盲跑。
6. 写入缓存：
   - 写入目标 package 的 `packageJson`、`packageRoot`、`workspaceRoot`、Node 版本约束、实际 Node 路径和版本、包管理器名称/路径/版本、lockfile、选定 scripts 和最终命令。
   - 旧缓存若只有字符串形式的 `node.packageManager`，在下一次前端命令前按当前 schema 重写为对象，补齐 `name`、`executable`、`version`、`declared` 和 `commandRunner`。
   - 只写项目声明和已验证结果，不写安装日志、token、registry 凭据或临时失败详情。

前端命令失败后的重算：

- 如果构建/编译/typecheck/lint 失败信息涉及 Node 版本、包管理器版本、lockfile、依赖解析、`engines`、`corepack`、workspace/filter、找不到脚本、找不到 CLI、ESM/CJS 兼容或框架版本不匹配，必须重新读取目标 `package.json`、依赖版本、lockfile 和本机候选环境。
- 若发现更匹配的 Node 或包管理器，更新 `.codex/local-environment.json` 后，用同一目标脚本重试一次。
- 若重试仍失败，停止连续盲改，区分环境不匹配、依赖未安装、项目历史失败和本次代码问题。

## Python 环境缓存

Python 语法检查、导入检查、lint、type check、测试或脚本运行前，必须先以目标 Python 项目为单位解析环境，不只使用系统 `python`。

读取顺序：

1. 定位项目根和目标配置：
   - 优先使用本次触碰 `.py`、测试或配置文件向上最近的 `pyproject.toml`、`setup.py`、`setup.cfg`、`requirements*.txt`、`Pipfile` 或 `tox.ini`。
   - 若仓库包含多个 Python 包，按触碰文件最近配置确定 `packageRoot`，再读取仓库根的共享配置、Makefile、justfile 或 CI 命令范式。
2. 读取 Python 版本和依赖约束：
   - `pyproject.toml` 的 `requires-python`、`project.dependencies`、`dependency-groups`、`tool.poetry.dependencies.python`、`tool.uv`、`tool.ruff`、`tool.pytest`、`tool.mypy`、`tool.pyright`。
   - `uv.lock`、`poetry.lock`、`Pipfile.lock`、`requirements*.txt`、`constraints*.txt`、`tox.ini`、`noxfile.py`、`pytest.ini`。
   - `.python-version`、`.tool-versions`、`runtime.txt`、`.venv/pyvenv.cfg`、Dockerfile 或 CI 中的 Python 版本。
3. 匹配本机环境：
   - 优先复用 `.codex/local-environment.json` 中同一 `packageRoot`、配置文件、锁文件、Python 版本约束和管理器仍匹配的缓存。
   - 根据项目证据选择管理器：`uv.lock` 优先 `uv`，`poetry.lock` 优先 `poetry`，`Pipfile.lock` 优先 `pipenv`，已有 `.venv` 优先项目虚拟环境，只有简单脚本才考虑系统 Python。
   - Python 版本不满足 `requires-python`、`.python-version`、`.tool-versions` 或锁文件约束时，继续查找项目虚拟环境、pyenv/asdf/系统候选；找不到则说明缺口，不用不匹配解释器盲跑。
4. 选择命令：
   - 优先使用项目已有 Makefile、justfile、tox、nox、CI、`pyproject.toml` tool 配置或 README 命令。
   - 没有项目命令时按管理器包装：`uv run ...`、`poetry run ...`、`pipenv run ...`、`<venv>/bin/python -m ...`。
   - 语法检查可选 `python -m py_compile` 或 `compileall`；lint/type check/test 只在项目已有工具或任务需要时执行。
5. 写入缓存：
   - 写入 `packageRoot`、配置文件、Python 版本约束、解释器路径/version、管理器名称/path/version、虚拟环境路径、lockfile、选定命令和验证命令。
   - 只写项目声明和已验证结果，不写 pip 安装日志、私有 index token、`.env` 内容或临时失败详情。

Python 命令失败后的重算：

- 如果失败信息涉及 Python 版本、虚拟环境、依赖解析、lockfile、管理器、模块导入、工具命令不存在、tox/nox env、ABI/wheel 或 `Requires-Python`，必须重新读取 Python 配置、锁文件、虚拟环境和本机候选环境。
- 若发现更匹配的解释器、虚拟环境或管理器，更新 `.codex/local-environment.json` 后，用同一目标命令重试一次。
- 若重试仍失败，停止连续盲改，区分环境不匹配、依赖未安装、项目历史失败和本次代码问题。

## 小程序环境缓存

小程序编译、构建、CI、预览、上传或发布前校验前，必须先识别项目形态、目标平台和构建入口；默认不启动模拟器、真机或开发者工具 UI。

读取顺序：

1. 定位小程序项目和框架：
   - 原生小程序读取 `project.config.json`、`project.private.config.json`、`app.json`、`sitemap.json`、`miniprogramRoot`、`miniprogram_npm`。
   - uni-app 读取 `pages.json`、`manifest.json`、`App.vue`、`uni.scss`、`uni_modules`、`vite.config.*` 或 `vue.config.*`。
   - Taro 读取 `package.json`、`app.config.*`、`page.config.*`、`config/index.*`、`project.config.json`、`TARO_ENV` 相关脚本。
   - 多端项目必须记录目标平台：`weapp`、`mp-weixin`、`alipay`、`tt`、`swan`、`qq`、`jd`、`ks` 等。
2. 读取 Node 和构建约束：
   - 有 `package.json` 的小程序项目必须同时按 [Node/前端环境缓存](#node前端环境缓存) 读取 lockfile、包管理器、`scripts`、`engines` 和框架依赖版本。
   - 原生项目若只有微信开发者工具配置，没有 Node 构建脚本，则只缓存小程序 root、平台配置和必要的开发者工具 CLI 需求，不强行查 Node。
3. 匹配本机环境：
   - 优先复用 `.codex/local-environment.json` 中同一 `sourceRoot`、`outputRoot`、framework、platform、packageJson 和构建脚本仍匹配的缓存。
   - 只在用户明确要求模拟器、预览、上传、真机或 CI 上传链路时，才查找并验证微信开发者工具 CLI、`miniprogram-ci` 上传配置或平台账号依赖。
   - 不把未验证的开发者工具路径、上传私钥、appid 密钥或平台账号状态写入缓存。
4. 选择命令：
   - 原生小程序优先使用项目已有 npm/CI 构建脚本或静态编译脚本；没有脚本时默认只做配置和语法层检查，不打开开发者工具。
   - uni-app 优先使用 `build:mp-weixin`、`build:custom` 或项目既有平台脚本。
   - Taro 优先使用 `build:weapp`、`build:<platform>` 或项目既有 `taro build --type ...` 脚本。
   - 构建命令必须来自项目 scripts、框架配置或现有 CI，不凭经验替换包管理器、平台或输出目录。
5. 写入缓存：
   - 写入 `framework`、`platform`、`projectConfig`、`sourceRoot`、`outputRoot`、`packageRoot`、`packageJson`、Node/包管理器引用、构建脚本、`devtoolsCli` 验证状态和选定命令。
   - 开发者工具路径只有验证通过且当前任务确实需要时才写入；上传密钥、私钥、token、白名单和平台账号状态永不写入。

小程序命令失败后的重算：

- 如果失败信息涉及框架版本、目标平台、包管理器、lockfile、`miniprogramRoot`、`sourceRoot`、`outputRoot`、`project.config.json`、`pages.json`、`manifest.json`、条件编译、Taro/uni-app 脚本、开发者工具 CLI 或 `miniprogram-ci`，必须重新读取小程序配置、Node 配置和本机候选环境。
- 若发现更匹配的包管理器、构建脚本、平台、源码目录、输出目录或开发者工具 CLI，更新 `.codex/local-environment.json` 后，用同一目标命令重试一次。
- 若重试仍失败，停止连续盲改，区分环境不匹配、依赖未安装、项目历史失败、平台账号/密钥缺口和本次代码问题。

## 公共验证矩阵

只验证当前任务实际需要的工具；不要为了补全缓存而安装、扫描或验证无关技术栈。

| 场景 | 最小验证 | 记录要点 | 差异规则 |
| --- | --- | --- | --- |
| Maven/JDK | `<mavenExecutable> -version`，必要时验证 `JAVA_HOME` 和 `java -version` | `mavenRoot`、`modulePath`、`maven.executable`、`maven.localRepository`、`java.home/version/versionRequirement`、来源 | 先按本文件 Maven/Java 环境缓存匹配，再按 `03` 执行构建 |
| Node/前端 | `node --version`，项目实际包管理器 `--version`，必要时验证 `corepack --version` | `node.executable`、`node.version`、`packageManager.name/executable/version`、`packageJson`、`packageRoot`、lockfile、scripts、selectedCommand、来源 | 先按本文件 Node/前端环境缓存匹配，再按 `11` 执行构建 |
| Python | `<pythonExecutable> --version`，项目实际管理器或测试工具 `--version` | `python.executable/version/versionRequirement`、`manager`、`packageRoot`、项目配置文件、lockfile、来源 | 先按本文件 Python 环境缓存匹配，再按 `10` 执行命令 |
| 小程序 | 项目实际构建 CLI `--version`、构建脚本 dry check，只有明确需要时验证 `<wechatDevtoolsCli> --help` | `framework`、`platform`、`projectConfig`、`sourceRoot`、`outputRoot`、`buildCommand`、`devtoolsCli`、来源 | 先按本文件小程序环境缓存匹配，再按 `12` 执行构建/CI |

公共约束：

- 工具路径、版本、来源和验证命令必须对应同一个工作区。
- 只把验证通过的候选写入缓存。
- 不把临时全局安装、错误目录下的 lockfile 判断、未验证解释器、未验证开发者工具路径写入缓存。
- 不把密钥文件内容、CI 上传凭证、真实 appid 私钥、机器人编号、生产白名单写入缓存或长期记忆。

## 缓存结构

缓存文件路径：

```text
.codex/local-environment.json
```

推荐结构：

```json
{
  "version": 1,
  "updatedAt": "YYYY-MM-DDTHH:mm:ssZ",
  "scope": "workspace",
  "workspaceRoot": "/path/to/workspace",
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
    "verified": true
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
    "verified": true
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
- `.codex/local-environment.json` 是本地状态文件，不提交到仓库。

## 写入边界

- 允许写入当前工作区的 `.codex/local-environment.json`。
- 不自动修改用户全局 shell 配置、IDE 配置、Maven settings 或系统环境变量。
- 不把临时失败日志写入缓存。
- 不把未验证路径写入缓存。

## 与长期记忆的关系

- 本地缓存记录“这个工作区当前可用的环境路径”。
- 长期 memory 只记录稳定偏好，例如“优先从 IDE 配置和本地缓存发现 Maven”；不记录某台机器的 Maven、JDK、Node、Python 绝对路径。
- 如果用户明确要求更新长期 memory，再按 memory 规则写入长期记忆更新请求。
