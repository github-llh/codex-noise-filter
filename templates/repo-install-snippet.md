# Repository Install Snippet

把完整 skill 目录放到仓库级发现路径：

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  agents/openai.yaml
  references/
```

也可将源码目录软链到该位置。安装后新建 Codex 任务，通过 `$codex-noise-filter` 做一次显式调用，再用包含真实代码证据的请求验证隐式触发。

`AGENTS.md` 只能提供项目指导，不能代替 skill 安装。若选择器未刷新，检查同名副本并重启 Codex。
