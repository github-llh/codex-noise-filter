# Maven 多模块场景

## Prompt

```text
$codex-noise-filter 处理这个 Maven 编译失败，只构建必要模块，并区分环境问题和代码问题。
```

## 路由

- `references/02-execution-workflow.md`
- `references/03-environment-and-validation.md`
- `references/04-java-backend.md`

## 期望

- 确认聚合 root、wrapper、JDK/Maven 约束和目标 module。
- 使用 `-pl <module> -am` 或项目等价方式收窄验证。
- 不全局安装 Maven/JDK，不把依赖或 profile 问题误修成代码问题。
