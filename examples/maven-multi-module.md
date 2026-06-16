# Maven 多模块场景

## 触发 Prompt

```text
$codex-noise-filter 按 Maven 多模块 root 构建规则，找到当前模块的最小验证命令。
```

## 应读取

- `SKILL.md`
- `references/00-index.md`
- `references/03-maven-backend-build.md`
- Maven/JDK 路径未知时追加 `references/06-environment-discovery.md` 和 `references/14-environment-cache-by-stack.md`

## 期望行为

- 先定位聚合 root，而不是在任意子模块直接执行构建。
- 优先读取 `.codex/local-environment.json`、IDE 配置、项目配置和本机已验证候选。
- 找到 Maven 可执行文件和本地仓库后执行最小验证，并缓存到 `.codex/local-environment.json`。
- 多模块验证优先使用 `-pl <module> -am`。

## 禁止行为

- 不把个人机器的 Maven 路径写死进 README、示例或通用规则。
- 不混用未验证的全局 Maven、本地仓库或 JDK。
- 不用全量构建替代可定位的最小验证，除非影响范围确实需要。
