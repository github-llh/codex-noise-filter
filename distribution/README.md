# 分发与安装

本目录保存 Codex 源 manifest/hooks。`SKILL.md`、`references/` 与守卫只有一份源码；构建器生成独立宿主包。当前版本 `4.1.0`。

## 构建产物

```bash
python3 scripts/build-distributions.py
```

在 Windows 终端使用 `py -3` 代替 `python3`。输出：

```text
dist/release-4.1.0/
  codex/.agents/plugins/marketplace.json
  codex/plugins/codex-noise-filter/
  claude/.claude-plugin/marketplace.json
  claude/plugins/codex-noise-filter/
  claude-windows/.claude-plugin/marketplace.json
  claude-windows/plugins/codex-noise-filter/
  harness/codex-noise-filter/（package.json、cordis.patch.yml、index.js、metadata.json、icon.svg、locale/、skills/）
  portable/codex-noise-filter/plugin.json
  skill/codex-noise-filter/SKILL.md
  codex-noise-filter-codex.zip
  codex-noise-filter-claude.zip
  codex-noise-filter-claude-windows.zip
  codex-noise-filter-harness.zip
  dsh-codex-noise-filter-4.1.0.tgz
  projects/{cursor,gemini,opencode,copilot,harness}/
  codex-noise-filter-portable.zip
  codex-noise-filter-skill.zip
  chat-app-instructions.md
```

各 ZIP 不包含 marketplace，直接包含宿主插件根文件；Skill ZIP 使用 `codex-noise-filter/SKILL.md` 顶层目录。README、测试、examples、templates 不进入运行时 Skill。聊天模板单独交付，不在运行时默认加载。

`--target codex|claude|claude-windows|harness|portable|skill` 可只构建单个目录；只有 `all`（默认）同时生成 ZIP。使用 `--output <新的目录>` 指定目标，非空/源码/祖先/指向源码的软链目录会被拒绝，不删除已有用户文件。旧入口 `scripts/build-plugin-package.sh` 仍生成 Codex `dist/marketplace`，同样要求输出为空。

## Codex

从本仓库根目录执行安装（这些命令会改变本机插件配置，仅在准备好安装时运行）：

```bash
codex plugin marketplace add ./dist/release-4.1.0/codex
codex plugin add codex-noise-filter@codex-noise-filter-local
codex plugin list
```

随后新建任务，在 `/hooks` 或宿主 hooks 设置中完成启用与信任，确认 `SessionStart` 包含 startup/resume/clear/compact。桌面、IDE 与 CLI 必须使用实际执行任务的机器、账户和配置目录，不能把本机安装推断为云端安装。

显式调用：`$codex-noise-filter 查明并修复这个构建错误`。

## Claude Code、Desktop Code 与 Cowork

macOS/Linux 的 Code 会话可通过 CLI 安装：

```bash
claude plugin marketplace add ./dist/release-4.1.0/claude
claude plugin install codex-noise-filter@codex-noise-filter-local
```

Windows 选择 `./dist/release-4.1.0/claude-windows`，其 hooks 明确使用 PowerShell 和 `py -3`；POSIX 包使用 `python3`。要求实际 hook 执行环境中已有 Python 3.10+。不自动安装 Python、设置模型或放宽权限。

支持文件上传插件的 Claude 表面可导入 `codex-noise-filter-claude.zip`；运行在 Linux VM 的 Cowork 使用 POSIX 包，即使桌面宿主是 Windows。以执行环境而非 UI 操作系统选择包。Chat 表面只使用插件 skills，hooks/subagents 需支持的 Cowork/Code 表面，不能据上传成功推断 hooks 可用。

显式调用插件技能：`/codex-noise-filter:codex-noise-filter`。独立安装的 Skill 使用 `/codex-noise-filter`。Claude manifest 不包含 Codex UI 字段或 `commandWindows`，默认 `hooks/hooks.json` 只注册一次。

## DeepSeek Harness 桌面端与 CLI

`harness/codex-noise-filter` 是独立 Cordis bundle（npm 包名 `dsh-codex-noise-filter`），按 Harness 插件契约组织：

```text
harness/codex-noise-filter/
  package.json        dsh.bundle.patch、private、type=module、main/exports、icon、files
  cordis.patch.yml    insert 条目 codex-noise-filter -> dsh-codex-noise-filter
  index.js            ESM 入口：apply(ctx) 注册技能与短路由，返回清理函数
  metadata.json       入口读取的技能描述与激活语
  icon.svg            原创图标（Plugin Manager 与设置页展示）
  locale/en.json      meta.title / meta.description（英文）
  locale/zh.json      meta.title / meta.description（中文）
  skills/codex-noise-filter/  同一份 SKILL.md 与 references
```

没有 npm 依赖、安装脚本、模型覆盖或 Python hook。它向 `ctx.skills` 注册技能，向 `ctx.systemPrompt.context` 注册短路由；Harness 按快照变化与压缩恢复机制交付上下文，技能正文保持按需读取。`files` 与 `exports` 覆盖全部运行时文件，Plugin Manager 从 `locale` 与 `icon` 读取展示元数据。

CLI/Web 在准备安装时执行，例如已有 `web` profile：

```bash
dsh plugin --profile web add ./dist/release-4.1.0/dsh-codex-noise-filter-4.1.0.tgz
dsh --profile web --dump-config
```

`dsh plugin` 把参数原样转发给 profile 目录里的 pnpm，因此 CLI 可用相对路径；Plugin Manager 页面或 agent 工具安装时只接受绝对路径（`file:`/`link:` 同样按绝对路径解析）。安装默认启用该组合包；`--dump-config` 应出现 `codex-noise-filter` 条目。未声明 `engines.dsh` 时按 DSH peer 范围做兼容检查，不兼容会要求精确版本豁免，不要顺手放宽。卸载用 `dsh plugin --profile web remove dsh-codex-noise-filter`。内置 `web` 模板启用 HMR，安装与启停通常即时生效；其他模板重启后生效，结果里的 `restart-required` 必须如实转告。

Desktop 使用应用自带 Plugin Manager 添加本地 bundle 目录或 tarball 并确认启用，标题、描述与图标来自 bundle 的 `locale` 与 `icon.svg`。若该版本 UI 不接受本地路径，使用下面的项目 Skill 入口，不手写或修改 Desktop 保留的 profile。桌面 executable packages、plugin activation 与 CLI 分开管理，`dsh plugin --profile web` 成功不证明 Desktop 已安装。使用当前 Desktop 实际绑定的 Harness 版本验证，预览期 API 可能演进。

不安装 Cordis bundle 也可将 `projects/harness/.dsh/skills/codex-noise-filter` 放入目标仓库的 `.dsh/skills/`。在 Desktop 选择该工作区，新会话技能列表应出现同名技能；核对实际 `skill` 工具调用和资源读取。该路径使用宿主自带发现/压缩后目录刷新，不注册本项目短路由或外部 hooks。插件和项目技能二选一，避免同名来源覆盖。

Native bundle 依赖宿主已启用 `skills`、`systemPrompt` 服务及模型可见的 skill 消费工具；Minimal 或自定义隐藏技能的 preset 必须以实际能力为准。本地服务契约测试不代替真实桌面安装验收。

## Cursor、Gemini CLI、OpenCode、GitHub Copilot

`projects/` 内提供可合并到目标仓库的目录，构建时不会写入其他项目：

| 宿主 | 技能目录 | 持久项目入口 |
| --- | --- | --- |
| Cursor 桌面 Agent/CLI | `.cursor/skills/codex-noise-filter` | `.cursor/rules/codex-noise-filter.mdc`（始终加载短语义路由） |
| Gemini CLI | `.gemini/skills/codex-noise-filter` | `GEMINI.md` |
| OpenCode 桌面/CLI/Web | `.opencode/skills/codex-noise-filter` | `AGENTS.md` |
| GitHub Copilot App/CLI/IDE Agent | `.github/skills/codex-noise-filter` | `.github/copilot-instructions.md` |

先审阅再合并生成入口，已有同名指令文件必须保留并合并，不能直接覆盖。规则引导原生 skill 工具和完整文件读取，不关闭 Gemini 的激活确认或任何宿主权限。它们使用规则/技能级连续性流程，不注册这些宿主专有 hooks。远程、云端或手机控制任务须把项目技能提供给真正执行任务的环境，仅有本机目录并不代表已同步。

## 独立 Skill 与 portable plugin

解压 Skill ZIP 后，按宿主放置 `codex-noise-filter` 目录：

| 宿主 | 项目级 | 用户级 |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Deep Code | `.deepcode/skills/` | `~/.agents/skills/` |
| DeepSeek Harness | `.dsh/skills/` 或 `.agents/skills/` | `<dshHome>/skills/` 或 `<agentsHome>/skills/` |

有 Skills 上传入口的 App 可上传 Skill ZIP。其他宿主必须查官方发现路径，不猜测。portable plugin ZIP 使用 Agent Plugins 标准根 `plugin.json`，仅在支持该规范的表面导入，不带厂商私有 hooks。

MiMo、DeepSeek 经 Codex/Claude Code 接入时仍使用该宿主包，模型 API 配置参考 [官方链接](../references/13-host-compatibility.md)，本项目不写 API Key、Base URL、模型名、thinking、effort 或 token 预算。

没有已确认扩展入口的普通 App 使用 [聊天模板](../templates/chat-app-instructions.md)，由用户放入其官方支持的项目/自定义指令或本次请求。模板不提供后台事件，也不保证所有 App 的跨会话继承。

## 旧版本迁移

截图中的 `1.0.1`、既有 `3.x` 或同名全局 Skill 都不会因源码升级自动刷新。先查看宿主当前安装来源、版本和同名副本，再用其插件更新/替换入口载入 `4.1.0`；CLI marketplace 更新以当前 `codex plugin marketplace --help` / `claude plugin --help` 为准，不手改插件缓存。

已配置同名 marketplace 时优先更新原来源，不重复执行 add 注册另一份。首次内容更新后可能需要宿主重新信任 hooks；开始新会话核验。不要同时装 Claude POSIX 与 Windows 两包，或同时保留同名独立 Skill 与插件副本。

## 验证证据

```bash
python3 scripts/validate-project.py
python3 scripts/test-continuity-guard.py
python3 scripts/test-distributions.py
python3 scripts/validate-project.py --marketplace-root dist/release-4.1.0/codex
python3 scripts/validate-project.py --claude-plugin dist/release-4.1.0/claude/plugins/codex-noise-filter
python3 scripts/validate-project.py --portable-plugin dist/release-4.1.0/portable/codex-noise-filter
python3 scripts/validate-project.py --harness-bundle dist/release-4.1.0/harness/codex-noise-filter
claude plugin validate --strict dist/release-4.1.0/claude/plugins/codex-noise-filter
node scripts/test-harness.mjs dist/release-4.1.0/harness/codex-noise-filter dist/release-4.1.0/dsh-codex-noise-filter-4.1.0.tgz
node scripts/test-harness-e2e.mjs dist/release-4.1.0/harness/codex-noise-filter
```

`test-harness-e2e.mjs` 从本机 Desktop 安装的 `app.asar` 提取真实 cordis Loader 与 `skills`/`systemPrompt` 服务，按 patch 条目导入 bundle 并验证注册、加载、装配与释放；安装路径不同用 `--asar <path>` 指定，未安装 Desktop 时跳过即可。

安装验收用 [触发检查请求](../templates/activation-check.prompt.md)，同时查宿主 hook 日志和实际 skill 读取动作。状态在宿主提供的 `PLUGIN_DATA/continuity` 或 `CLAUDE_PLUGIN_DATA/continuity` 中，`last_context_kind` 区分 activation/recovery。成功工具不写状态，计数不是所有工具次数，更不是模型质量评分。

本地测试证明包结构、脚本行为与内容一致性；不会替代各厂商真实账号、模型、桌面、移动端、远程或 VM 环境的触发验收。
