<div align="center">

# codex-noise-filter

**证据驱动的 Codex 编程工作流 skill**

少读无关内容 · 保护脏工作区 · 自动恢复连续性 · 真实验证

[English](README.en.md) · [更新记录](CHANGELOG.md) · [分发说明](distribution/README.md)

</div>

## v3 定位

`codex-noise-filter` 用于真实代码库里的解释、诊断、审查和实施任务。它先判断用户授权的任务模式，再从代码、diff、路径、配置、日志和失败命令中收敛证据，最后用与触碰范围匹配的验证闭环。v3 新增 Plugin 内置连续性 Hook，在上下文压缩、会话恢复/重新连接、模型变化和网络/传输失败后自动要求复核目标与落盘状态。

v3 保留 v2 已清理的噪音与副作用边界：

- 不再要求每次工具调用都运行 Guard Loop。
- 不再按固定文件数或工具次数输出 Context Capsule。
- 不再在验证前强制创建 `.codex/local-environment*.json`。
- 不再因阅读到旁支代码味道就自动扩大修改范围。
- 不猜测第三方宿主目录；自动能力只建立在已打包、已验证且被宿主启用的 Hook 上。
- 调用链改为按风险追踪：简单错误停在完整语义单元，高风险变更才扩展到系统边界。

仍然保留根因假设、必要调用链、Git 脏改保护、外部内容安全、失败换路和最小充分验证。连续性状态只写插件专属 `PLUGIN_DATA`，不复制 prompt、transcript、工具原始输出、日志、凭证、客户数据或工作区路径。

所有技术栈统一要求：新增或修改的注释、docstring、Javadoc、JSDoc/TSDoc 和模板说明默认使用简体中文；状态、类型、协议 key、阈值、超时、路由、事件、样式 token 等魔法值按项目既有方式收敛到枚举、常量、类型、配置、字典或 design token。

## 触发边界

适用：

- 代码读取、调试、修复、重构、迁移和代码审查。
- diff、路径、异常堆栈、构建/测试/lint/typecheck/CI 输出。
- Java/Maven、Python、Vue/React/TypeScript、小程序/uni-app/Taro。
- skill、plugin、AGENTS、hook、MCP、manifest、marketplace 和 agentic 供应链审计。
- 上下文压缩、会话恢复/重新连接、模型切换、工作目录变化和网络/传输失败后的任务恢复。

不适用：纯知识问答、没有仓库上下文的泛泛建议、翻译和普通文案改写。

## 工作流

1. 读取 `SKILL.md` 和 `references/00-index.md`。
2. 判定回答、诊断、审查或实施模式。
3. 检查 Git root、目标模块、分支和脏工作区。
4. 从原始症状或目标行为定位完整语义单元，按风险补必要调用链。
5. 只修改授权范围和目标所需直接依赖。
6. 运行静态检查、目标构建/测试和 diff review 中的最小充分组合。
7. 连续性事件触发后自动从最新指令、工作区、落盘文件和工具状态重建唯一下一步。
8. 用中文交付结果、关键变更、验证与未覆盖边界。

## 安装

### 仓库级

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  agents/openai.yaml
  references/
```

可以复制本仓库，或把本仓库软链到上述目录。

### 用户级

将完整 skill 目录放到 `$HOME/.agents/skills/codex-noise-filter/`。Codex 也支持系统和管理员级 skill 位置；同名 skill 不会自动合并，出现重复时要确认当前加载来源。

显式调用：

```text
$codex-noise-filter 找到这个构建失败的根因并修复，保护现有脏改并运行最小充分验证。
```

隐式调用依赖 `SKILL.md` 的 `description`。更新后若未出现，重启 Codex 并检查同名副本。

直接安装 Skill 只能获得指令级恢复；要让生命周期事件自动触发，使用下方 Plugin 分发包。Plugin 的非托管命令 Hook 按 Codex 官方安全模型在首次启用或内容变化后需要信任审查；完成一次信任后，压缩、恢复、模型变化和受支持工具的网络失败不需要用户再次提醒。管理员禁用 Hook、启用 managed-only 策略或宿主不支持对应事件时会退回指令级流程。

## Reference 结构

| 文件 | 职责 |
| --- | --- |
| `00-index.md` | 最小规则集路由 |
| `01-engineering-baseline.md` | 范围、授权、读取与工程质量 |
| `02-execution-workflow.md` | 回答/诊断/审查/实施流程 |
| `03-environment-and-validation.md` | 工具链发现、验证与失败归因 |
| `04` 至 `08` | Java、并发数据、Python、前端、小程序 |
| `09-agentic-security.md` | 外部内容与可执行供应链安全 |
| `10-continuity.md` | 压缩、中断、模型变化与网络失败后的自动连续性保护 |
| `11-skill-and-plugin-distribution.md` | Codex skill/plugin 分发 |

所有 reference 都由 `SKILL.md` 直接链接，并控制在 100 行以内，避免深层引用和默认上下文膨胀。

## Plugin 分发

运行：

```bash
scripts/build-plugin-package.sh
```

默认生成可直接作为 local marketplace root 使用的目录：

```text
dist/marketplace/
  marketplace.json
  plugins/codex-noise-filter/
    .codex-plugin/plugin.json
    hooks/
      hooks.json
      continuity_guard.py
    LICENSE
    skills/codex-noise-filter/
```

运行时 Plugin 额外包含连续性 Hook；其中 Skill 包只包含 `SKILL.md`、`agents/` 和 `references/`。README、CHANGELOG、examples、templates、测试和仓库维护文件不会进入运行时包。

## 验证

```bash
python3 scripts/validate-project.py
python3 scripts/test-continuity-guard.py
bash -n scripts/build-plugin-package.sh
scripts/build-plugin-package.sh
python3 scripts/validate-project.py --plugin dist/marketplace/plugins/codex-noise-filter
python3 scripts/validate-project.py --marketplace-root dist/marketplace
git diff --check
```

验证器和 Hook 测试只使用 Python 标准库，检查 frontmatter、命名、description 长度、reference 直链、本地 Markdown 链接、方向控制字符、SemVer、manifest、Hook 事件/路径/超时和 marketplace 路径。

## 官方依据

- [Build skills](https://developers.openai.com/codex/build-skills)：渐进披露、description 触发、skill 发现位置和 `agents/openai.yaml`。
- [Build plugins](https://developers.openai.com/codex/plugins/build)：`.codex-plugin/plugin.json`、`skills/`、SemVer 和 marketplace。
- [AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md)：项目指令链、优先级和大小边界。
- [Hooks](https://developers.openai.com/codex/hooks)：生命周期事件、配置位置和运行时限制。

## 协议

[Apache License 2.0](LICENSE)
