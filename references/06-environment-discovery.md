# 环境发现与缓存

用于 Maven、JDK、Node、Python、包管理器、IDE 配置路径等本机环境。目标是避免每次硬编码路径或重复全盘查找。

## 目录

- [发现顺序](#发现顺序)
- [Maven 验证](#maven-验证)
- [Node / 前端验证](#node--前端验证)
- [小程序验证](#小程序验证)
- [Python 验证](#python-验证)
- [缓存策略](#缓存策略)
- [写入边界](#写入边界)
- [与长期记忆的关系](#与长期记忆的关系)

## 发现顺序

1. 读取工作区缓存：`.codex/local-environment.json`。
2. 读取 IDE/项目配置：
   - JetBrains：`.idea/misc.xml`、`.idea/workspace.xml`、`.idea/compiler.xml`、`.idea/jarRepositories.xml`。
   - Maven 项目：`.mvn/maven.config`、`.mvn/jvm.config`、`.mvn/wrapper/maven-wrapper.properties`、`pom.xml`。
   - 前端项目：`package.json`、`pnpm-lock.yaml`、`yarn.lock`、`package-lock.json`、`bun.lockb`、`bun.lock`、`.nvmrc`、`.node-version`、`.tool-versions`、`.npmrc`、`.yarnrc.yml`、`vite.config.*`、`vue.config.js`、`next.config.*`。
   - 小程序项目：`project.config.json`、`project.private.config.json`、`app.json`、`sitemap.json`、`pages.json`、`manifest.json`、`app.config.js`、`app.config.ts`、`config/index.js`、`config/index.ts`、`miniprogram_npm/`、`unpackage/dist/`、`dist/`。
   - Python 项目：`pyproject.toml`、`requirements.txt`、`requirements-dev.txt`、`uv.lock`、`poetry.lock`、`Pipfile.lock`、`tox.ini`、`noxfile.py`、`pytest.ini`、`.python-version`、`.tool-versions`、`.venv/pyvenv.cfg`。
3. 读取 shell 环境和常见命令：
   - `JAVA_HOME`
   - `MAVEN_HOME`
   - `M2_HOME`
   - `PATH`
   - `which mvn`
   - `which node`
   - `which pnpm`
   - `which yarn`
   - `which npm`
   - `which bun`
   - `which corepack`
   - 微信开发者工具 CLI 候选路径
   - `which python`
   - `which python3`
   - `which uv`
   - `which poetry`
   - `which pytest`
4. 查找本机常见路径，只做小范围候选，不全盘扫描：
   - `/Users/lilinhan/dev/maven-*/bin/mvn`
   - `/Users/lilinhan/maven-git`
   - `/Users/lilinhan/.m2/repository`
   - `/opt/homebrew/bin/mvn`
   - `/usr/local/bin/mvn`
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

## Maven 验证

Maven 可执行文件必须通过：

```bash
<mavenExecutable> -version
```

Maven 本地仓库必须是存在的目录，且构建命令使用：

```bash
-Dmaven.repo.local=<localRepository>
```

当前已验证示例：

```json
{
  "maven": {
    "executable": "/Users/lilinhan/dev/maven-3.9.10/bin/mvn",
    "home": "/Users/lilinhan/dev/maven-3.9.10",
    "localRepository": "/Users/lilinhan/maven-git"
  }
}
```

## Node / 前端验证

前端项目先从 `package.json` 判断包管理器：

- `packageManager` 明确指定时优先使用该工具和版本。
- 存在 `pnpm-lock.yaml` 用 pnpm。
- 存在 `yarn.lock` 用 yarn。
- 存在 `package-lock.json` 用 npm。
- 存在 `bun.lock` 或 `bun.lockb` 用 bun。

Node 和包管理器至少验证：

```bash
node --version
npm --version
pnpm --version
yarn --version
bun --version
corepack --version
```

只验证项目实际使用的工具；不要为了验证而安装新包管理器。若 `corepack` 已启用且项目声明 `packageManager`，优先按项目声明执行。

前端项目缓存建议记录：

```json
{
  "node": {
    "source": "project-config",
    "executable": "/path/to/node",
    "version": "vX.Y.Z",
    "packageManager": "pnpm|npm|yarn|bun",
    "packageManagerVersion": "X.Y.Z",
    "lockfile": "pnpm-lock.yaml",
    "verified": true
  }
}
```

不把临时全局安装、未验证 Node、错误目录下的 lockfile 判断写入缓存。

## 小程序验证

小程序项目先识别项目形态和源码/输出目录：

- 原生微信小程序：`project.config.json`、`app.json`、`app.js`、`app.wxss`、`pages/**`、`components/**`、`miniprogram_npm/`。
- uni-app：`pages.json`、`manifest.json`、`App.vue`、`main.js`/`main.ts`、`uni_modules/`、`unpackage/dist/dev/mp-*` 或 `unpackage/dist/build/mp-*`。
- Taro：`config/index.js`/`config/index.ts`、`src/app.config.*`、`@tarojs/*` 依赖、`dist/`、`taro build --type weapp` 或项目脚本。

运行到微信小程序时，优先使用项目已有脚本生成目标小程序工程，再用微信开发者工具模拟器打开输出目录。不要直接修改 `dist/`、`unpackage/dist/` 这类构建产物，除非任务明确是排查构建结果。

微信开发者工具 CLI 至少验证：

```bash
<wechatDevtoolsCli> --help
```

项目若使用 `miniprogram-ci`，优先读项目已有上传/预览脚本和密钥路径配置，只能验证命令、构建和本地预览能力；不得提交或暴露上传密钥、真实 `appid` 私钥、机器人编号或 IP 白名单配置。

小程序缓存建议记录：

```json
{
  "miniprogram": {
    "source": "project-config",
    "framework": "native-weapp|uni-app|taro|other",
    "platform": "weapp|alipay|tt|swan|qq|jd|ks|other",
    "sourceRoot": "src|.",
    "outputRoot": "dist|unpackage/dist/dev/mp-weixin",
    "devtoolsCli": "/Applications/wechatwebdevtools.app/Contents/MacOS/cli",
    "verifiedCommand": "<wechatDevtoolsCli> --help",
    "verified": true
  }
}
```

不把未验证开发者工具路径、密钥文件内容、CI 上传凭证、构建产物临时路径写入长期记忆。

## Python 验证

Python 解释器必须通过：

```bash
<pythonExecutable> --version
```

如果项目已有虚拟环境、uv、poetry、pipenv、tox 或 nox，优先验证项目工具链：

```bash
uv --version
poetry --version
<pythonExecutable> -m pip --version
<pythonExecutable> -m pytest --version
```

Python 项目缓存建议记录：

```json
{
  "python": {
    "source": "project-venv",
    "executable": "<workspace>/.venv/bin/python",
    "version": "Python X.Y.Z",
    "manager": "uv|poetry|pipenv|venv|conda|system",
    "projectFile": "pyproject.toml",
    "verifiedCommand": "<workspace>/.venv/bin/python --version",
    "verified": true
  }
}
```

不把未验证解释器、全局 pip 安装结果、临时虚拟环境路径写入缓存。

## 缓存策略

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
    "source": "verified-local-candidate",
    "executable": "/path/to/mvn",
    "home": "/path/to/maven",
    "localRepository": "/path/to/repository",
    "verifiedCommand": "/path/to/mvn -version",
    "verified": true
  }
}
```

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
- 长期 memory 只记录稳定偏好，例如“优先从 IDE 配置和本地缓存发现 Maven”。
- 如果用户明确要求更新长期 memory，再按 memory 规则写入长期记忆更新请求。
