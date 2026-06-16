# Python 场景

## 触发 Prompt

```text
$codex-noise-filter 处理这个 Python 测试失败，先识别虚拟环境、依赖管理器、定向测试和 lint/type check。
```

## 应读取

- `SKILL.md`
- `references/00-index.md`
- `references/02-noise-filter-workflow.md`
- `references/10-python-development.md`
- 环境路径未知时追加 `references/06-environment-discovery.md` 和 `references/14-environment-cache-by-stack.md`

## 期望行为

- 先检查 `pyproject.toml`、`.python-version`、`.venv`、`requirements.txt`、`uv.lock`、`poetry.lock`、`tox.ini`、`noxfile.py` 等项目证据。
- 优先复用项目已有 `uv`、`poetry`、`pipenv`、`venv`、`tox`、`nox` 流程。
- 公共函数、复杂返回值、跨模块 DTO/配置对象补类型标注和必要 docstring。
- 验证优先定向运行测试、语法/导入检查、触碰范围相关 lint/format/type check。

## 禁止行为

- 不直接使用全局 `pip` 乱装依赖。
- 不跳过项目已有 Ruff/Black/isort/mypy/pyright/pytest 配置。
- 不把临时解释器路径写进可复用文档。
