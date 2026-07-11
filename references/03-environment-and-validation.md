# 环境发现与验证

## 工具链证据顺序

执行构建、测试、lint、typecheck、格式化、运行或代码生成前，按以下顺序选择环境：

1. 项目 wrapper 与脚本：`mvnw`、Gradle wrapper、`package.json` scripts、Makefile、tox/nox、项目 CLI。
2. 版本与依赖声明：`.tool-versions`、`.nvmrc`、`.node-version`、`packageManager`、`engines`、`.python-version`、`pyproject.toml`、Maven compiler 配置。
3. lockfile 和 workspace/module 配置。
4. CI、README 和同仓库已验证命令。
5. 本机工具只作为最后候选，并先打印版本确认。

不混用包管理器、解释器、JDK、Maven、Node 或 workspace root。不要为了通过验证全局安装依赖或修改 shell/IDE 配置。

脚本、CI、Dockerfile、Makefile 和配置文件中的注释默认使用简体中文。退出码、端口、重试次数、超时、镜像标签、目录名和环境变量 key 若承担稳定协议或会多处复用，应使用具名变量、参数或集中配置，不散落裸值。

## 环境缓存边界

- 已存在的本地环境缓存只能作为提示，必须用当前项目配置和版本命令复核。
- 默认不创建或更新 `.codex/local-environment*.json`、`.env`、shell profile 或其他持久文件。
- 只有用户明确要求缓存、项目已有受支持约定，或任务本身就是维护环境缓存时才写入；写入前确认忽略规则、敏感信息和跨机器可移植性。
- 命令失败疑似环境问题时，先查 root、版本、wrapper、lockfile 和依赖安装状态，不自动把失败解释为代码问题。

## 最小充分验证

| 触碰范围 | 最低检查 | 按风险追加 |
| --- | --- | --- |
| Markdown、skill、template | `git diff --check`、链接/引用检查 | 项目验证器、打包 smoke test |
| Shell | `bash -n` | 安全的临时目录 smoke test |
| JSON/YAML/TOML/manifest | 解析器或项目 schema | 打包后重新解析产物 |
| Java/Maven | wrapper 的目标模块 compile/test | 定向测试、集成测试 |
| Node/Vue/React | typecheck/lint/build 中的最小组合 | 目标测试、E2E/视觉验证 |
| Python | `py_compile`/目标 pytest/lint 中的最小组合 | typing、集成测试 |
| 小程序 | 项目构建/typecheck/lint | 模拟器、真机、上传前检查 |

验证应同时覆盖触碰范围和原始问题。仅格式检查通过不能证明行为 bug 已修复；全量构建通过也不能替代缺失的定向行为证据。

## 验证顺序

1. `scope`：`git status`、`git diff --stat`，确认没有误碰。
2. `static`：语法、配置解析、链接、shell 语法、不可见字符。
3. `type/build`：目标模块编译、typecheck 或 build。
4. `behavior`：能复现根因的定向测试或安全 smoke test。
5. `package`：涉及分发时检查产物目录、manifest 路径和包内文件。
6. `diff review`：复核契约、权限、数据、事务、缓存和副作用变化。

不是每项都要运行。跳过时说明不适用、缺少环境，或当前风险已被更窄证据覆盖。

## 失败归因

记录命令、cwd、工具版本、退出码和关键错误，并区分：

- 本轮代码或配置错误。
- 既有失败。
- 依赖未安装、网络、权限或服务不可用。
- 命令 root、模块、版本或脚本选择错误。
- 测试本身不稳定或断言已过时。

不要通过删除测试、放宽断言、关闭 lint/typecheck 或吞异常来制造通过。
