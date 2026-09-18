# Repository Install Snippet

先按当前宿主选择路径；同一个模型在不同宿主中的安装位置可能不同。

| 宿主 | 仓库级目录 |
| --- | --- |
| Codex | `.agents/skills/codex-noise-filter` |
| Claude Code | `.claude/skills/codex-noise-filter` |
| DeepSeek Harness | `.dsh/skills/codex-noise-filter` |
| Cursor | `.cursor/skills/codex-noise-filter` |
| Gemini CLI | `.gemini/skills/codex-noise-filter` |
| OpenCode | `.opencode/skills/codex-noise-filter` |
| Copilot | `.github/skills/codex-noise-filter` |

以 Codex 为例：

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  agents/openai.yaml
  references/
```

也可将源码目录软链到该位置。安装后新建 Codex 任务，通过 `$codex-noise-filter` 做一次显式调用，再用包含真实代码证据的请求验证隐式触发。

`AGENTS.md` 只能提供项目指导，不能代替 skill 安装。Claude 使用 `CLAUDE.md`；其他宿主使用其原生入口。完整项目入口已由构建器生成在 `projects/`，只合并到已授权项目，保留已有指令文件。

若选择器未刷新，检查工作区、同名副本与实际执行环境。桌面安装不推断为 CLI/云端安装，规则发现不推断为 hooks 已运行。详见 [分发说明](../distribution/README.md)。
