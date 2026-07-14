# Skill 与 Plugin 分发

本文件只描述 Codex 已验证的分发表面；第三方宿主必须以其官方文档和当前可见能力为准。

## Skill 结构

Skill 的运行时入口是 `SKILL.md`，可选目录为 `references/`、`scripts/`、`assets/` 和 `agents/openai.yaml`。

- `name` 与 `description` 是隐式选择的关键元数据。description 要前置主要用途、边界清晰且简短。
- `SKILL.md` 保留核心流程和 reference 入口；技术栈细节放 reference，避免重复。
- `agents/openai.yaml` 用于 UI、调用策略和工具依赖，不承载大段执行规则。
- Codex 会从 repo、user、admin 和 system 位置发现 skill；repo 级路径位于从 CWD 到 repo root 的 `.agents/skills`。
- 同名 skill 不会自动合并；排障时检查重复安装和当前会话是否需要重启。

## AGENTS.md 边界

`AGENTS.md` 是持久项目指导，不是 skill 注册表。保持简短，只放每次都适用的构建命令、约定和 review 期望；工作流细节留在 skill。更靠近 CWD 的项目指导具有更高局部优先级。

## Plugin 结构

稳定分发使用：

```text
plugin-root/
  .codex-plugin/plugin.json
  hooks/
    hooks.json
    continuity_guard.py
  skills/codex-noise-filter/
    SKILL.md
    agents/openai.yaml
    references/
```

- manifest 的 `name` 使用稳定 kebab-case，`version` 使用严格 SemVer，`skills` 与 `hooks` 使用以 `./` 开头的相对路径。
- 不声明不存在的 app、MCP、hook 或 assets。只有真实文件存在、权限边界清楚并通过验证时才加入 manifest。
- marketplace 的 `source.path` 相对 marketplace root、以 `./` 开头且不越界；每项包含 installation、authentication 和 category。
- 构建产物必须可重建，不作为源规则编辑入口。

## Hooks 与机械强制

Skill 指令只能指导 agent，不能证明 hook 会运行。需要生命周期强制时：

1. 使用 Codex 当前支持的 `PreCompact`、`PostCompact`、`SessionStart`、`UserPromptSubmit` 和 `PostToolUse` 事件。
2. Plugin Hook 通过 `$PLUGIN_ROOT` 定位只读脚本，通过 `$PLUGIN_DATA` 保存最小私有状态；不写项目目录、全局配置或长期 memory。
3. 审查 matcher、退出行为、超时、多 hook 并发语义、敏感信息边界和故障降级。
4. 非托管 Hook 首次启用或内容变化后必须由宿主完成信任审查；被禁用或跳过时退回 Skill 指令级流程。
5. 没有实际注册和运行证据时，不写“自动阻止”或“所有表面必执行”。

本项目 v3 只内置连续性 Hook，不声明 MCP 或 app，也不扩大文件、网络或外部系统权限。

## 发布检查

1. 校验 `SKILL.md` frontmatter、reference 链接和 `agents/openai.yaml`。
2. 校验 plugin manifest、SemVer、相对路径和 marketplace schema。
3. 在临时输出目录运行构建脚本，确认包内没有 README、CHANGELOG、`.DS_Store`、源码仓库辅助文件或个人路径。
4. 对构建产物再次运行验证器，并比较 source/reference 文件清单。
5. 本地安装或更新后，新建任务验证隐式和显式触发；仅修改源码不等于已刷新安装副本。

## 官方资料

- [Build skills](https://developers.openai.com/codex/build-skills)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md)
- [Hooks](https://developers.openai.com/codex/hooks)
