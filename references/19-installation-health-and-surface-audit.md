# 19 安装健康、分发表面与故障排查

本文件处理 skill、rules、commands、hooks、templates、plugin、manifest、marketplace、AGENTS 片段和跨宿主安装的健康检查。目标是让能力能被真实宿主加载，并且不会因为分发表面漂移导致“说过的规则又失效”。

## 触发信号

出现任一信号时追加本文件：

- 用户要求安装、分发、迁移、同步、更新、强化、重构、删除/新增目录、生成 plugin、marketplace、manifest、README、AGENTS snippet、全局配置或第三方 agent 接入。
- 出现 skill 不生效、规则没加载、换窗口丢失、第三方 agent 不识别、hook 不触发、commands 找不到、MCP 不可用、插件缓存缺文件、模板过期。
- 任务涉及 `.codex`、`.agents`、`skills/`、`rules/`、`commands/`、`hooks/`、`agents/openai.yaml`、`.codex-plugin/plugin.json`、`distribution/marketplace.json`、`dist/`、`templates/`。
- 需要判断某个平台是否支持 native skills、slash command、rules-only、hook、MCP、ACP、subagent 或 fallback。
- 需要删除/新增目录或重排 skill 文档结构。

## 表面角色边界

按角色分层，不按文件名迷信：

| 表面 | 角色 | 约束 |
| --- | --- | --- |
| `SKILL.md` | 轻量启动器 | 只放触发、索引、总门禁和执行节奏 |
| `references/00-index.md` | 路由器 | 维护快速决策、关键词和最小加载组合 |
| `references/*.md` | 细则 | 承载技术栈、流程、安全、验证、连续性等执行规则 |
| `templates/` | 安装/检查片段 | 可复制但不能写死个人路径或承诺宿主不支持的能力 |
| `agents/openai.yaml` | Codex App UI 元数据 | 不承载执行规则 |
| `distribution/` | 发布元数据 | 不直接等同于可加载 skill 根目录 |
| `dist/` | 构建产物 | 可重建，不作为源规则编辑入口 |
| `rules/commands/hooks` | 兼容表面 | 只有宿主支持时才具备运行时效果；否则只是说明或 shim |

如果外部体系把 commands 当 canonical，而当前体系把 `skills/` 当 canonical，迁移时以当前体系为准：commands/rules/hooks 只补兼容说明，不把旧运行时整套搬入。

## 加载健康检查

接入或排障时按顺序确认：

1. `nativeSkill`：当前宿主是否列出了 `codex-noise-filter`。列出才可声称原生加载。
2. `manualFileBootstrap`：若没有 discovery 但可读文件，是否按 `HOST_CONFIG_DIR`、`AGENTS_DIR`、项目 `.agents/skills`、用户级 `.agents`、`CODEX_HOME`、兼容 `.codex` 找到首个 `SKILL.md`。
3. `rulesOnly`：若只能读取 AGENTS/rules，是否已明确“不是 skill 自动加载”，并把 `references/00-index.md` 的路径探测写清。
4. `fallbackOnly`：若既无 discovery 也不能读文件，是否进入最小兜底矩阵，且明确记录原因。
5. `conflictCheck`：是否存在多个同名 skill、旧版本、插件缓存副本、项目级覆盖用户级、AGENTS 片段和真实安装目录不一致。
6. `reloadCheck`：宿主是否需要重启、刷新插件、重新打开窗口、重新加载 MCP 或清理缓存。
7. `evidenceCheck`：是否用当前宿主的可见列表、文件路径、版本、git diff/status 或打包产物证明，而不是凭记忆。

## 分发一致性检查

修改 skill 结构后至少检查：

- `SKILL.md` 是否仍保持轻量，没有复制完整 reference 清单。
- `references/00-index.md` 是否包含新增 reference 的路由、关键词和组合。
- README/README.en 是否同步能力概览和目录结构。
- templates 是否同步 bootstrap、activation check 和 repo install snippet。
- 若新增或强化自动触发、范围追加、状态机、防断流规则，是否同步 `20-automatic-guard-loop.md`、`02` 状态机、`05` Capsule、README 和 AGENTS 模板。
- `agents/openai.yaml` 是否只保留 UI 元数据，不塞执行规则。
- `scripts/build-plugin-package.sh` 是否仍能定位源文件和必要目录。
- `distribution/marketplace.json` 是否指向正确构建产物、版本和显示名。
- 新增文件是否会进入构建产物；删除文件是否没有被 README、模板、manifest 或脚本引用。
- 是否保留无关脏改和未跟踪噪声，不把安装健康检查变成清理工作区。

## 故障排查矩阵

| 症状 | 常见原因 | 处理 |
| --- | --- | --- |
| 用户说 skill 没生效 | 宿主只读了 AGENTS，没有 native skill discovery | 标记 `rulesOnly` 或 `manualFileBootstrap`，按路径探测读取 `SKILL.md`/`00-index.md` |
| 换窗口后又犯旧错 | Capsule/working context 未刷新，或新窗口只恢复了摘要 | 按 `16` 恢复 `currentTruth/decisions/doNotRetry/nextStep`，再查当前 diff/status |
| 第三方 agent 找不到 `.codex` | 该宿主没有 Codex 目录约定 | 以 `HOST_CONFIG_DIR` 为准，优先 `$HOST_CONFIG_DIR/skills/codex-noise-filter/` |
| hook 不触发 | 宿主无 hook parity、matcher 不匹配、未注册、权限/路径错误 | 不承诺自动阻止；改成规则门禁或宿主支持的 hook，并记录验证证据 |
| commands 可用但 skill 不加载 | commands 是兼容 shim，不是 canonical skill | 保持 `skills/` 为 canonical，把 commands 指向 skill 或保留为轻量入口 |
| 插件缓存缺文件 | 构建脚本未包含新增 reference/template，或 manifest 引用漂移 | 更新构建脚本/manifest 后重新打包并检查产物 |
| context 变大且慢 | 外层入口膨胀、一次性读完 references、模板重复规则 | 收缩 `SKILL.md`，让 `00-index.md` 渐进路由 |
| memory 带错规则 | 旧记忆未按当前文件复核，或外部内容污染长期记忆 | 以当前文件和 diff 为准，按 `17`/`16` 标记旧记忆失效 |
| 环境命令找不到 | 未读项目缓存、版本管理器或 IDE 配置 | 按 `06`/`14` 解析 active cache path 和工具链来源 |

## Surface Audit 清单

做大改、分发或跨宿主接入前，输出或内部维护：

```text
surfaceAudit:
  canonicalSkill: <path/status>
  index: <path/status>
  references: <新增/删除/变更>
  guardLoop: <20 路由/模板/README 同步状态>
  templates: <同步状态>
  pluginMetadata: <agents/openai.yaml/distribution/manifest>
  hostSupport: <nativeSkill|manualFileBootstrap|rulesOnly|fallbackOnly>
  unsupportedRuntime: <hooks/MCP/subagents/etc>
  conflicts: <同名副本/旧版本/缓存>
  verification: <命令/结果>
```

## 删除和新增目录规则

- 可以删除过时目录或文件，但必须先确认没有被 `SKILL.md`、`00-index.md`、README、templates、scripts、manifest、marketplace、安装片段引用。
- 删除兼容表面前确认目标宿主是否仍依赖它；无法确认时优先标记 deprecated，不直接删除。
- 新增目录必须有清晰角色；不要把 runtime、source、dist、memory、template 混在同一目录。
- 不把个人机器绝对路径写进可分发文件；示例路径使用变量或相对占位。
- 构建产物可重建时，不把 `dist/` 当源事实；以源码目录和脚本为准。

## 交付要求

命中本文件后，最终回复至少说明：

- 本轮调整了哪些分发表面。
- 哪些宿主能力是原生支持，哪些只是 rules/manual bootstrap/fallback。
- 做了哪些安装健康或引用一致性检查。
- 是否留下无关脏改、缓存副本或需要用户手动刷新宿主。
