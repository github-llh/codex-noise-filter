# 技术栈环境缓存

本文件按需读取。只有任务准备执行构建、编译、测试、运行、预览、发布前校验、代码生成，或工具链失败疑似环境/版本/依赖/脚本/模块/平台不匹配时打开。统一发现、验证、跨系统缓存文件命名、active cache path 和 `.codex/` 忽略规则见 `06-environment-discovery.md`。

## 目录

- [Maven/Java 环境缓存](#mavenjava-环境缓存)
- [Node/前端环境缓存](#node前端环境缓存)
- [Python 环境缓存](#python-环境缓存)
- [小程序环境缓存](#小程序环境缓存)

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
   - 优先复用 active cache path 中同一 `mavenRoot`、`modulePath`、Java 版本约束和 Maven/wrapper 仍匹配的缓存。
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
- 若发现更匹配的 JDK、Maven、wrapper、localRepository 或模块参数，更新 active cache path 后，用同一目标命令重试一次。
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
   - `dependencies`、`devDependencies`：识别 Vue 2/3、React、Vite、Next、Nuxt、Vue CLI、Taro、uni-app、TypeScript、ESLint、Prettier、Stylelint、Biome、oxlint 等工具链版本。
   - `engines.node`、`engines.npm`、`packageManager`、Volta 配置：作为 Node 和包管理器版本约束。
3. 读取语法、缩进和格式规范文件：
   - ESLint flat config：`eslint.config.js`、`eslint.config.mjs`、`eslint.config.cjs`、`eslint.config.ts`、`eslint.config.mts`、`eslint.config.cts`。
   - ESLint legacy config：`.eslintrc`、`.eslintrc.js`、`.eslintrc.cjs`、`.eslintrc.yaml`、`.eslintrc.yml`、`.eslintrc.json`，以及 `package.json` 中的 `eslintConfig`。
   - Prettier：`package.json` 中的 `prettier`，`.prettierrc`、`.prettierrc.json`、`.prettierrc.yml`、`.prettierrc.yaml`、`.prettierrc.json5`、`.prettierrc.js`、`.prettierrc.cjs`、`.prettierrc.mjs`、`.prettierrc.ts`、`.prettierrc.cts`、`.prettierrc.mts`、`prettier.config.js`、`prettier.config.cjs`、`prettier.config.mjs`、`prettier.config.ts`、`prettier.config.cts`、`prettier.config.mts`，以及 `.prettierignore`。
   - EditorConfig：从目标文件或目标 package 目录向上查找 `.editorconfig`，直到项目根或命中 `root = true`；缓存每个命中的文件路径。
   - 其他前端规范：`biome.json`、`biome.jsonc`、`.stylelintrc`、`.stylelintrc.json`、`.stylelintrc.yaml`、`.stylelintrc.yml`、`.stylelintrc.js`、`.stylelintrc.cjs`、`stylelint.config.js`、`stylelint.config.cjs`、`oxlint.json`、`.oxlintrc.json`、`tsconfig.json`、`tsconfig.*.json`、`jsconfig.json`。
   - 只读取目标 package、workspace root 和触碰文件向上路径内的规范文件；不全仓扫描无关 package，也不把 IDE inspection profile 当作项目规范来源。
4. 读取锁文件和包管理器配置：
   - `pnpm-lock.yaml` -> 默认 `pnpm`。
   - `yarn.lock`、`.yarnrc.yml` -> 默认 `yarn`，注意 Yarn classic 与 berry。
   - `package-lock.json`、`npm-shrinkwrap.json` -> 默认 `npm`。
   - `bun.lockb`、`bun.lock` -> 默认 `bun`。
   - 没有 lockfile 时再按 `packageManager`、项目 README/CI、scripts 中的命令前缀判断。
5. 选择命令：
   - 优先使用 `package.json` 里已存在的 scripts，例如 `<pm> run build`、`<pm> run typecheck`、`<pm> run lint`。
   - 若存在 ESLint/Prettier/Biome/Stylelint/TypeScript 规范文件或依赖，优先匹配已有 `lint`、`lint:fix`、`format`、`format:check`、`prettier`、`stylelint`、`typecheck`、`check`、`biome`、`oxlint` 脚本；没有脚本时只记录可用工具和缺口，不臆造会改动大量文件的命令。
   - 如果 scripts 明确使用 `npx`、`pnpm dlx`、`yarn dlx` 或框架 CLI，记录为 `commandRunner`，但不要把 `npx` 误判为包管理器。
   - workspace 子包优先使用项目既有 filter/workspace 命令；没有项目范式时，在目标 package 目录执行该 package 的 script。
6. 匹配本机环境：
   - 优先复用 active cache path 中同一 `packageJson`、lockfile、Node 约束和包管理器仍匹配的缓存。
   - 缓存中记录的 ESLint/Prettier/EditorConfig/Biome/Stylelint/TypeScript 规范文件不存在、路径集合变化、mtime/size/hash 变化，或 `package.json` 中 scripts/dependencies/devDependencies/packageManager 变化时，必须重新读取规范文件并更新缓存。
   - 缓存缺失或不匹配时，查找本机 Node、corepack、npm、pnpm、yarn、bun 候选，并验证版本。
   - Node 版本不满足 `engines.node`、`.nvmrc`、`.node-version`、Volta 或构建工具最低要求时，继续查找本机候选；找不到则说明缺口，不用不匹配版本盲跑。
7. 写入缓存：
   - 写入目标 package 的 `packageJson`、`packageRoot`、`workspaceRoot`、Node 版本约束、实际 Node 路径和版本、包管理器名称/路径/版本、lockfile、选定 scripts、最终命令，以及 `frontendQuality`。
   - `frontendQuality` 至少记录：`eslint`、`prettier`、`editorconfig`、`biome`、`stylelint`、`typescript`、`javascript`/`ecma` 相关配置文件路径，来源字段来自 `packageJson` 还是文件，文件 `mtime`/`size` 或可用 hash，匹配的验证脚本名，是否存在 format check 脚本。
   - 旧缓存若只有字符串形式的 `node.packageManager`，在下一次前端命令前按当前 schema 重写为对象，补齐 `name`、`executable`、`version`、`declared` 和 `commandRunner`；如果来自旧版 `.codex/local-environment.json`，必须先强制迁移替换到当前 profile 文件，之后不再读取旧版文件。
   - 只写项目声明和已验证结果，不写安装日志、token、registry 凭据或临时失败详情。

前端命令失败后的重算：

- 如果构建/编译/typecheck/lint 失败信息涉及 Node 版本、包管理器版本、lockfile、依赖解析、`engines`、`corepack`、workspace/filter、找不到脚本、找不到 CLI、ESM/CJS 兼容或框架版本不匹配，必须重新读取目标 `package.json`、依赖版本、lockfile 和本机候选环境。
- 若发现更匹配的 Node 或包管理器，更新 active cache path 后，用同一目标脚本重试一次。
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
   - 优先复用 active cache path 中同一 `packageRoot`、配置文件、锁文件、Python 版本约束和管理器仍匹配的缓存。
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
- 若发现更匹配的解释器、虚拟环境或管理器，更新 active cache path 后，用同一目标命令重试一次。
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
   - 优先复用 active cache path 中同一 `sourceRoot`、`outputRoot`、framework、platform、packageJson 和构建脚本仍匹配的缓存。
   - 只在当前任务目标本身包含模拟器、预览、上传、真机或 CI 上传链路，且权限边界清楚时，才查找并验证微信开发者工具 CLI、`miniprogram-ci` 上传配置或平台账号依赖。
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
- 若发现更匹配的包管理器、构建脚本、平台、源码目录、输出目录或开发者工具 CLI，更新 active cache path 后，用同一目标命令重试一次。
- 若重试仍失败，停止连续盲改，区分环境不匹配、依赖未安装、项目历史失败、平台账号/密钥缺口和本次代码问题。
