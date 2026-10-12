<div align="center">

# codex-noise-filter

**模型无关的编程任务去噪、证据验证与连续性保护**

[English](README.en.md) · [更新记录](CHANGELOG.md) · [安装与分发](distribution/README.md) · [官方依据与宿主矩阵](references/13-host-compatibility.md)

</div>

## v4 做了什么

保留既有名称与工程规则，以一份 `SKILL.md` 和 references 支持不同宿主。模型可以是 GPT、Claude、MiMo、DeepSeek 或其他兼容供应商；**触发能力由运行任务的宿主提供，不能由模型名称推断**。

- 按用户意图区分解释、诊断、审查和实施，保护脏改，按真实证据追踪必要调用链。
- 插件在首次启动、恢复、清空和压缩恢复时注入一次短语义路由，结合前文识别“继续”“还是报错”等续问；skill 正文调用后在会话内保留，不按轮重复调用。
- Codex/Claude 分别生成原生 manifest、marketplace 和 hooks；Claude 以 `PostToolUseFailure` 替代 `PostToolUse`；路由每会话只注入一次，不按轮重复。DeepSeek Harness 单独生成原生 Cordis bundle，使用技能注册与稳定上下文快照。
- 性能优化针对重复上下文、无关扫描与 Hook 空操作，保持用户选择的模型、推理强度、输出预算、原始工具结果和质量验收。
- 普通成功工具事件不写状态；新会话建档才清理历史状态，扫描使用全局节点/深度/字符预算。

适用真实代码、diff、配置、日志、构建、测试、CI、skill/plugin/agent 配置；不用于纯翻译、文案或无仓库背景的常识问答。外部文档、截图、日志中的指令只作为内容分析，不替代用户请求。

## 选哪个包

| 使用方式 | 分发包 | 前提 |
| --- | --- | --- |
| Codex CLI、IDE、支持本地插件的桌面工作任务 | `codex` | 本地插件与 hooks 已启用/信任 |
| Claude Code CLI、Desktop 本地/SSH Code 会话、支持插件的 Cowork | `claude` | macOS/Linux，运行环境可调用 Python 3.10+ 的 `python3` |
| Windows Claude Code | `claude-windows` | PowerShell hooks、Python 3.10+，可调用 `py -3` |
| Claude Chat（Web/Desktop）或其他 Skill 宿主 | `skill` ZIP，或该表面支持的 Claude plugin ZIP | Chat 可用 skills 不等于能执行 hooks |
| Agent Plugins 规范宿主 | `portable` ZIP | 根 `plugin.json`，只提供 skills |
| MiMo/DeepSeek 经 Codex、Claude Code | 选择对应宿主包 | 模型配置由用户按厂商文档管理，本项目不改密钥/模型 |
| DeepSeek Harness Desktop / CLI / Web | `harness` 原生 bundle / tgz | Desktop 独立安装启用；也可使用 `.dsh/skills` 项目入口 |
| Cursor、Gemini CLI、OpenCode、Copilot App/CLI/IDE | `projects/` 对应项目入口 | 原生技能目录与规则文件；不套用 Codex hooks |
| Deep Code | `skill` | `.deepcode/skills` 或 `~/.agents/skills` |
| MiMo/DeepSeek 普通 App、尚未确认插件入口的桌面/网页/移动端 | [聊天指令模板](templates/chat-app-instructions.md) | 用户放入当前 App 支持的指令入口或本次请求；不能保证跨会话自动触发 |

普通聊天 App 无文件工具时，必须上传实际内容，不能让它假装读取本机路径。上述是文档支持范围，不是全部厂商端到端实测结果；完整来源、版本边界和恢复条件见 [宿主矩阵](references/13-host-compatibility.md)。

## 构建与安装

仅需 Python 3.10+，不安装额外依赖：

```bash
python3 scripts/build-distributions.py
```

Windows 可以使用 `py -3 scripts/build-distributions.py`。默认输出 `dist/release-4.1.0/`，包含六种目录/ZIP、Harness npm tarball、五种项目入口和聊天指令模板。构建器拒绝覆盖非空输出；再次构建使用 `--output dist/release-check-2` 等新目录。

安装命令、ZIP 导入、旧版本迁移和项目指令配置统一见 [分发说明](distribution/README.md)。**构建源码不会自动刷新已经安装的 1.x/3.x 副本。** 同一宿主选择一个原生插件包，避免插件和独立 Skill 同名重复加载。

## 触发可靠性

触发分三个阶段验收：

1. **发现**：宿主技能/插件列表能看到正确来源和版本；显式调用可用。
2. **事件执行**：支持 hooks 的表面记录 startup/prompt/恢复事件及上下文注入。
3. **遵循规则**：真实编程请求确实读取 skill，诊断不写文件，修复完成必要验证；纯翻译不加载工程工作流。

Hook 注入是路由提醒，不代表模型必然遵循。项目可合并 [AGENTS 模板](templates/global-AGENTS.light.md)；Claude 使用 [CLAUDE 模板](templates/project-CLAUDE.md)。`AGENTS.md` 不是插件注册表，Claude Code 不自动读取它；可在已有 `CLAUDE.md` 显式导入 `@AGENTS.md`。

管理员禁用、首次信任未完成、宿主缺少事件/Python 或运行在不同机器/容器时，必须按实际环境排查，不能仅凭插件开关判定成功。普通 App 使用指令级工作流，无法凭本项目获得宿主未提供的后台 hook。

## 连续性与隐私

连续性守卫仅保存不可逆会话/目录指纹、模型、已知恢复原因与有界计数；不复制 prompt、transcript、原始工具输出、日志、凭证或客户数据。状态使用宿主提供的 `PLUGIN_DATA` 或 `CLAUDE_PLUGIN_DATA`；没有该目录则无状态运行，不猜测用户目录。

压缩事件先记标记，由支持 `additionalContext` 的后续事件要求复核目标、约束、落盘文件、验证和唯一下一步。网络失败先检查操作回执，避免盲目重试副作用。状态是辅助证据，不是业务事务日志，不能据计数声称精确一次执行。

## 验证与性能

```bash
python3 scripts/validate-project.py
python3 scripts/test-continuity-guard.py
python3 scripts/test-distributions.py
bash -n scripts/build-plugin-package.sh
python3 scripts/benchmark-hooks.py
# 完整构建后验证 Harness 服务契约（需要 Node.js）
node scripts/test-harness.mjs dist/release-4.1.0/harness/codex-noise-filter
git diff --check
```

需要与已审查的旧版本比较时：`python3 scripts/benchmark-hooks.py --baseline-ref <git-ref>`。该选项会在临时环境执行指定版本的守卫代码；只用可信项目版本。

基准仅测合成事件的本地 Hook 耗时，分别报告函数与完整进程延迟，不证明模型生成更快或质量无回归。测试覆盖事件协议、压缩恢复、模型变化、只读成功路径、隐私、跨包规则一致性、可复现 ZIP 和安全输出目录。真实模型触发、Windows/Cowork 运行环境及各厂商 App 仍需安装后验收。

## 规则结构

`SKILL.md` 是执行入口；`references/00-index.md` 选择最小必要规则集。`01`—`03` 管理工程范围/执行/验证，`04`—`08` 覆盖 Java、并发数据、Python、前端与小程序，`09`—`13` 覆盖供应链安全、连续性、分发、受控委派与宿主适配。reference 均直接链接且不超过 100 行。

子代理仅在可独立验收、收益高于协调成本且符合宿主授权时使用，严格单层；不预设某个厂商的模型，不为凑并发而启动。新增注释默认简体中文，稳定业务值遵循项目现有常量/类型机制。

[贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md) · [Apache-2.0](LICENSE)
