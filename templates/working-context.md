# Working Context Template

仅在项目已有 handoff/working-context 习惯、用户明确要求持久化，或任务目标本身是建立交接文件时使用。不要把本模板当成默认必须写入的文件；普通任务优先使用当前回复中的 Context Capsule。

```text
Current Truth
- Goal:
- Verified facts:
- Root cause:
- Touched scope:
- Unverified boundaries:

Current Constraints
- Allowed changes:
- Forbidden changes:
- API/DTO/DB/permission/business boundaries:
- Security/external communication/credential boundaries:
- Unsupported runtime assumptions:

Active Queues
- Done:
- In progress:
- Blocked:
- Exact next step:

Interfaces
- Entry files:
- Trigger/data source:
- Commands:
- Configs:
- Distribution surfaces:
- Call-chain anchors:
- Validation coverage:

Latest Execution Notes
- What worked:
- What did not work:
- doNotRetry:
- Validation:
- Rollback points:

Update Rule
- Update when:
- Do not store:
- Evidence required:
```

写入要求：

- 写入前先读当前文件、`git diff`、`git status` 和最近 Capsule。
- 只写当前项目事实、决策、约束、队列和证据锚点。
- 不写 secrets、token、客户数据、个人机器绝对路径、外部 prompt 原文、未脱敏日志、第三方长摘要或模型推理过程。
- 外部内容只能作为待验证参考；涉及外部来源时先按 `references/17-agentic-security-and-supply-chain.md` 处理。
- 与当前文件/diff 冲突时，以当前文件/diff 为准，并标记旧条目过期。
