# Contributing

Thanks for helping improve `codex-noise-filter`. This project is a Codex skill, so changes should keep the entrypoint small, route detailed rules through references, and preserve Chinese/English documentation consistency.

## Before You Start

- Open an issue first for behavior changes, new rule categories, large rewrites, or changes that may affect skill activation.
- Small typo fixes, broken links, and template updates can go directly to a pull request.
- Keep changes scoped. Do not rewrite unrelated references or examples while fixing one rule.
- Do not add secrets, private paths, production URLs, tokens, customer data, or proprietary logs.

## Project Shape

- `SKILL.md` is the lightweight trigger and routing entrypoint.
- `references/00-index.md` owns routing decisions.
- Detailed rules live under `references/`.
- `README.md` and `README.en.md` should stay aligned when user-facing behavior, installation, capabilities, or community links change.
- `examples/` and `templates/` should remain focused on copyable usage patterns.

## Change Guidelines

1. Identify the exact rule, template, or document being changed.
2. Read `SKILL.md`, `references/00-index.md`, and the smallest relevant reference file before editing.
3. Keep trigger boundaries explicit. Do not broaden activation based on vague domain terms alone.
4. Preserve progressive disclosure: keep the main skill file lean and move details into the most relevant reference.
5. Update both README files when the change affects public usage or project metadata.
6. Add or update examples only when they clarify a real workflow.
7. Prefer concise, auditable wording over broad policy language.

## Pull Request Checklist

Before opening a pull request, confirm:

- The change has a clear purpose and narrow scope.
- `SKILL.md` remains lightweight unless the change is truly entrypoint-level.
- `references/00-index.md` is updated when routing changes.
- Chinese and English README files are synchronized when public behavior changes.
- New or changed templates do not include real credentials, private hostnames, or personal machine paths.
- You ran the lightest relevant validation, such as Markdown review, link review, or repository-specific checks.

## 中文说明

贡献时请保持改动可审计、范围收敛、可回滚。涉及触发条件、索引路由、README 展示、模板内容或安全边界时，需要同步检查中英文文档和相关 reference。不要提交真实密钥、生产地址、私有日志或个人机器路径。
