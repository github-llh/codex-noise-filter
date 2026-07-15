# 自动连续性保护

## 目标与边界

在上下文自动/手动压缩、会话恢复或重新连接、模型切换、工作目录变化、网络/传输失败后，自动恢复任务的证据链，不要求用户重复已经提供的信息。

- Skill 指令负责语义检查点和恢复顺序；Plugin 内置 Hook 负责感知 Codex 已公开的生命周期事件。
- 单纯切换可见窗口不会改变同一任务上下文；窗口关闭、重新连接或重新进入任务由 `SessionStart(resume)` 覆盖。
- Codex 没有公开独立的“网络断开”或“模型切换”Hook。网络工具失败由 `PostToolUse` 识别；模型变化由相邻事件的 `model` 字段比较。
- Hook 被禁用、未信任、被 managed-only 策略跳过或当前表面不支持时，仍执行本文件的指令级恢复，不宣称机械保证。

## 语义检查点

只在以下语义变化后更新短检查点：

- 用户新增或修改目标、约束、验收条件或禁止路径。
- 根因假设、公共契约、调用链边界或实现方案被证据确认。
- 文件真实写入、验证状态变化，或即将运行长时间/高输出/可能中断的工具。
- 同一命令或假设连续失败，需要写入 `doNotRetry`。

```text
目标:
约束与已确认事实:
已改文件:
验证状态:
doNotRetry:
唯一下一步:
```

检查点只存在于当前任务上下文；Plugin Hook 的持久状态只记录会话/目录指纹、模型、事件计数、上下文注入计数和恢复原因，不复制 prompt、日志、工具输出、凭证、客户数据或本机路径。未知或被篡改的恢复原因不得进入开发者上下文。

## 压缩与恢复契约

持续任务的压缩摘要应保留以下结构，但 Hook 不读取不稳定 transcript：

1. 最新用户目标、验收条件和不可违反约束。
2. 已确认事实、根因假设、关键决策及证据来源。
3. 已改文件、真实落盘状态和仍在运行的工具。
4. 已运行验证、结果、未覆盖边界和外部操作幂等性状态。
5. `doNotRetry` 与唯一下一步。

没有证据的字段标记为未确认；不把静态项目规则、完整日志、旧时间戳或大段历史重复塞入摘要。当前 Codex 的 `PreCompact`/`PostCompact` 输出协议不接受 `additionalContext`，因此 Hook 只在压缩前落下待恢复标记，再由 `SessionStart(compact)` 或下一次 `UserPromptSubmit` 注入上述账本复核，不照搬其他宿主的压缩 prompt 改写能力。

## 自动触发矩阵

| 触发 | 自动动作 |
| --- | --- |
| `PreCompact(manual|auto)` | 静默标记压缩待恢复，不返回宿主不支持的上下文字段 |
| `PostCompact(manual|auto)` | 用“压缩已完成”替换过期的“即将压缩”，等待恢复注入 |
| `SessionStart(compact|resume)` | 注入恢复要求并清除已消费标记 |
| `UserPromptSubmit` | 比较当前模型/目录指纹；发现变化或待恢复标记时注入恢复要求 |
| `PostToolUse(Bash|MCP)` | 同时具有失败状态和网络/传输特征时立即注入一次幂等性复核 |

Hook 不读取不稳定的 transcript 格式，也不阻止用户 prompt、压缩或工具结果；网络失败后只要求先查副作用，不盲目重试。宿主省略 `model` 或 `cwd` 时保留最近一次已知值，不用空值覆盖。

## 恢复顺序

1. 重读最新用户目标和高优先级指令，恢复目标、约束与验收条件。
2. 查看 `git status`、`git diff`、目标文件、运行中工具和外部操作回执，确认哪些动作真实落盘。
3. 用当前证据复核旧检查点、压缩摘要和上一模型结论；冲突时以当前工作区和最新指令为准。
4. 对网络/传输失败先判断远端或本地操作是否可能已成功，再决定查询、幂等重试、补偿或停止。
5. 重建已改文件、验证状态、`doNotRetry` 和唯一下一步，从断点继续，不从零全仓扫描。

每个原因消费后立即清除；已即时注入的网络失败不在下一条 prompt 重复。私有状态保留 `event_counts`、`context_injection_count`、最近注入事件/类型/原因，作为不包含用户内容的运行证据。

## 防复发与交付

- 同一命令或假设连续失败两次后停止原路径，记录替代证据入口。
- 证据不足时明确标记未验证，不用旧摘要、memory 或模型自述补事实。
- 最终回复不展示完整内部账本，只交付结果、验证、仍未覆盖的外部边界。
- 未经用户明确要求不把连续性状态写入长期 memory 或项目源码。

## 设计依据

- [Codex Hooks](https://developers.openai.com/codex/hooks)：事件、信任、matcher、`PLUGIN_DATA` 与输出协议。
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks)：恢复时刷新易过期上下文、快速 SessionStart 与最小 `additionalContext`。
- [GitHub Copilot Hooks](https://docs.github.com/en/copilot/concepts/agents/hooks)：事件审计、超时与跨平台命令边界。
- [OpenCode Plugins](https://opencode.ai/docs/plugins/)：借鉴其压缩账本字段，但不迁移 Codex 当前不支持的 compaction prompt 改写。
