# Surface Audit Checklist

用于 skill/plugin/AGENTS/templates/README/manifest/marketplace/rules/commands/hooks 的新增、删除、重构、分发或加载故障排查。普通代码任务不需要使用。

```text
surfaceAudit:
  canonicalSkill:
    path:
    status:
  index:
    path: references/00-index.md
    status:
  references:
    added:
    changed:
    removed:
    routingUpdated:
  templates:
    globalAgents:
    repoSnippet:
    activationCheck:
    optionalTemplates:
  docs:
    README.md:
    README.en.md:
    CHANGELOG.md:
  pluginMetadata:
    agents/openai.yaml:
    distribution/marketplace.json:
    pluginManifest:
    buildScript:
  hostSupport:
    type: nativeSkill | nativeCommand | rulesOnly | delegatedTool | manualFileBootstrap | fallbackOnly
    evidence:
  unsupportedRuntime:
    hooks:
    MCP/ACP:
    commands:
    subagents:
  conflicts:
    sameNameSkills:
    cacheCopies:
    staleDist:
  verification:
    commands:
    result:
    skipped:
    gaps:
```

检查规则：

- `SKILL.md` 保持轻量，细节放入 references。
- 新增 reference 必须在 `references/00-index.md` 有路由、关键词或任务映射。
- README、README.en、templates 和 CHANGELOG 同步新增能力或目录变化。
- 构建脚本、manifest、marketplace 不引用不存在的文件。
- hook、MCP、commands、subagent 只有在当前宿主支持且已注册时才写成运行时能力；否则只写成规则门禁。
- 保留无关脏改和未跟踪噪声，不把 surface audit 扩大成工作区清理。
