# 环境发现与缓存

用于 Maven、JDK、Node、Python、包管理器、IDE 配置路径、小程序开发者工具等本机环境。目标是提供跨技术栈统一的“发现、验证、缓存”机制，避免硬编码路径或重复全盘查找。

本文件只管环境路径和工具可用性，不替代各技术栈的运行、构建、测试规则：

- Maven 构建和多模块命令见 `03-maven-backend-build.md`。
- Python 依赖、运行、测试、lint/type check 见 `10-python-development.md`。
- Vue/React 包管理、运行、构建、测试见 `11-frontend-vue-react.md`。
- 小程序原生/uni-app/Taro 的源码/产物目录、模拟器、构建和发布见 `12-miniprogram-development.md`。

## 目录

- [发现顺序](#发现顺序)
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
   - Node/前端：`package.json`、lockfile、`.nvmrc`、`.node-version`、`.tool-versions`、`.npmrc`、`.yarnrc.yml`、构建工具配置。
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

## 公共验证矩阵

只验证当前任务实际需要的工具；不要为了补全缓存而安装、扫描或验证无关技术栈。

| 场景 | 最小验证 | 记录要点 | 差异规则 |
| --- | --- | --- | --- |
| Maven/JDK | `<mavenExecutable> -version`，必要时验证 `JAVA_HOME` | `maven.executable`、`maven.localRepository`、`java.home`、版本、来源 | 构建命令和多模块 root 见 `03` |
| Node/前端 | `node --version`，项目实际包管理器 `--version` | `node.executable`、`packageManager`、lockfile、版本、来源 | 包管理、运行、测试、构建见 `11` |
| Python | `<pythonExecutable> --version`，项目实际管理器或测试工具 `--version` | `python.executable`、`manager`、项目配置文件、版本、来源 | 依赖、运行、测试、lint/type check 见 `10` |
| 小程序 | `<wechatDevtoolsCli> --help` 或项目实际 CLI/CI 可用性检查 | `framework`、`platform`、`sourceRoot`、`outputRoot`、`devtoolsCli`、来源 | 原生/uni-app/Taro 构建、模拟器、发布见 `12` |

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
  "maven": {
    "source": "project-config|ide-config|verified-local-candidate|cache",
    "executable": "/path/to/mvn",
    "localRepository": "/path/to/repository",
    "verifiedCommand": "/path/to/mvn -version",
    "verified": true
  },
  "node": {
    "source": "project-config|verified-local-candidate|cache",
    "executable": "/path/to/node",
    "packageManager": "pnpm|npm|yarn|bun",
    "lockfile": "pnpm-lock.yaml",
    "verified": true
  },
  "python": {
    "source": "project-venv|project-config|verified-local-candidate|cache",
    "executable": "/path/to/python",
    "manager": "uv|poetry|pipenv|venv|conda|system",
    "verified": true
  },
  "miniprogram": {
    "source": "project-config|verified-local-candidate|cache",
    "framework": "native-weapp|uni-app|taro|other",
    "platform": "weapp|alipay|tt|swan|qq|jd|ks|other",
    "sourceRoot": "src|.",
    "outputRoot": "dist|unpackage/dist/dev/mp-weixin",
    "devtoolsCli": "/path/to/devtools-cli",
    "verified": true
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
