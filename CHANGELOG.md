# Changelog

## 2.0.0 - 2026-07-10

### 重大重构

- 把 20 份相互重叠的 reference 收敛为 11 个按职责路由的主题文件，所有 reference 由 `SKILL.md` 直接链接并控制在 100 行以内。
- 重写 `SKILL.md` description，前置真实触发边界并明确纯知识问答、翻译和无仓库泛泛建议不触发。
- 将工作流统一为回答、诊断、审查、实施四种模式，避免只读请求被自动升级为写入。
- 把根因与调用链改为风险分级：简单问题停在完整语义单元，模块/系统风险才扩展链路。
- 全语言统一新增/修改注释使用简体中文的规则，并补齐 Java、Python、Vue/React/TypeScript、小程序、Shell/CI、SQL、配置与 agent/plugin 表面的去魔法值策略。

### 去除反作用规则

- 删除每次工具调用前强制 Guard Loop、全字段状态机和固定频率 Capsule。
- 删除构建验证前强制创建或迁移 `.codex/local-environment*.json` 的副作用。
- 删除读取到旁支问题就自动修改、强制补注释和强制抽象的范围扩张规则。
- 删除第三方宿主目录猜测和无法由 skill 自身保证的自动 hook 承诺。

### 分发与验证

- Plugin 版本升级到 `2.0.0`，移除空 `screenshots` 等无效元数据，不声明 hook、MCP 或 app。
- 构建脚本改为生成完整 local marketplace root，并只打包运行时必需的 skill 文件。
- 新增标准库验证器，检查 frontmatter、reference 直链、本地链接、不可见方向字符、SemVer、manifest 和 marketplace 路径。
- 精简 `.gitignore`，删除 Java/IDE 模板遗留规则和错误的 `.proxyaidistribution` 条目。

## 1.0.1 - 2026-06-14

- 补充使用说明、Apache-2.0 协议与多技术栈 reference。
- 建立 Maven/Java、Python、Vue/React、小程序、并发与环境发现规则。

## 1.0.0 - 2026-06-14

- 建立 `SKILL.md`、`references/00-index.md` 和分主题 reference 的初始结构。
- 支持编程任务意图识别、调用链检查、局部工程规则与最小验证。
