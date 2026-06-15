# Python 开发规则

本文件按需读取。只有任务涉及 Python 语法、脚本、服务、包管理、虚拟环境、依赖、运行、测试、lint/format、类型检查或 Python 性能时打开。通用不可绕过门禁、调用链和既有代码局部对齐仍按 `02-noise-filter-workflow.md` 执行；环境路径发现见 `06-environment-discovery.md`。

参考来源：Python 官方文档、PEP 8、PEP 257、Python Packaging User Guide、pytest、Ruff、uv 官方文档。

## 目录

- [触发与读取](#触发与读取)
- [版本与语法](#版本与语法)
- [代码规范](#代码规范)
- [枚举、常量与配置](#枚举常量与配置)
- [项目结构与归属](#项目结构与归属)
- [环境与依赖](#环境与依赖)
- [运行与命令](#运行与命令)
- [测试与验证](#测试与验证)
- [Lint、格式化与类型检查](#lint格式化与类型检查)
- [性能与健壮性](#性能与健壮性)
- [安全与配置](#安全与配置)
- [参考资料](#参考资料)

## 触发与读取

- 看到 `.py`、`pyproject.toml`、`requirements.txt`、`setup.py`、`tox.ini`、`noxfile.py`、`Pipfile`、`poetry.lock`、`uv.lock`、`pytest.ini`、`ruff.toml`、`mypy.ini` 时优先读本文件。
- 默认组合：`02` + `10`。只有涉及环境路径发现时加 `06`，涉及前后端/Java 调用链时再按索引追加。
- 不为 Python 任务一次性读取 Java、Maven、前端 reference；触碰范围扩大时再追加。

## 版本与语法

- 修改前先确认 Python 版本来源：`pyproject.toml` 的 `requires-python`、`.python-version`、`.tool-versions`、`runtime.txt`、Dockerfile、CI 配置、IDE 解释器、`.venv/pyvenv.cfg`。
- 不使用超过目标版本的语法：`match/case`、`type` 语句、`list[str]`、`Self`、`ExceptionGroup`、`tomllib`、`pathlib.Path.walk` 等都要先确认版本。
- 新代码优先使用清晰的现代 Python：`pathlib`、上下文管理器、生成器表达式、`dataclass`、`Enum`、`typing`、`collections.abc`、`logging`。
- 避免可变默认参数、裸 `except`、吞异常、全局隐式状态、运行时乱改 `sys.path`、通配符 import、在库代码中直接 `print`。
- 脚本入口使用 `if __name__ == "__main__":`，可复用逻辑放函数，避免 import 时产生副作用。
- 公共函数、复杂返回值、跨模块 DTO/配置对象必须补类型标注；类型标注服务静态检查和 IDE，不假设运行时自动校验。

## 代码规范

- 优先遵守项目已有配置：`pyproject.toml`、`ruff.toml`、`.ruff.toml`、`setup.cfg`、`tox.ini`、`mypy.ini`、`.editorconfig`。
- 若项目已有 Ruff/Black/isort/mypy/pyright/pytest/tox/nox/uv/poetry，不新增同类工具，优先复用现有命令和配置。
- import 分组按标准库、第三方、本项目分组；不要为了通过 lint 把 import 放到函数里，除非是性能、循环依赖或可选依赖的明确需要。
- 注释说明“为什么”和边界，不重复代码行为；模块、公共类、公共函数、复杂算法、兼容逻辑、外部协议、数据清洗规则写必要 docstring。
- 函数保持小而清晰。超过一个稳定业务概念、多个副作用、多个外部资源或多段重复分支时，拆成私有函数、策略、数据类、配置对象或领域组件。
- 固定状态、类型、来源、动作、阶段、结果等闭合集合优先 `Enum` 或 `StrEnum`；环境变化值、密钥、URL、阈值、超时、重试次数放配置，不散落在代码里。

## 枚举、常量与配置

Python 任务也必须执行 `01-global-engineering-rules.md#跨技术栈硬编码治理`。不要因为是脚本或测试就把平台编码、状态值、外部协议、content type、路径、超时和阈值散写在多个函数里。

优先选择：

- 固定闭合集合：Python 3.11+ 优先 `enum.StrEnum`；较低版本用 `Enum` + `str` mixin，或项目已有枚举/常量范式。
- 类型收窄的少量固定字符串：可用 `typing.Literal` 或 `Final` 常量，但跨模块、跨接口或需要反查/展示时仍优先 `Enum`。
- 技术标准值：优先标准库、框架或 SDK 常量；没有时放到模块级 `Final` 常量或协议常量模块。
- 配置可变值：URL、token、secret、超时、重试、批量大小、阈值、路径等走环境变量、配置文件、settings 对象或项目已有配置系统。
- 动态业务分类：走数据库、配置中心、规则系统或数据字典，不写成 `Enum`。

写法要求：

- 常量名使用大写下划线，并尽量靠近所属模块；跨模块复用时放到现有 `constants.py`、`enums.py`、`settings.py` 或领域包内。
- `Enum` 成员值要保持外部协议兼容；不要随意修改已持久化或已对外返回的字符串。
- 业务代码比较枚举时优先比较枚举对象或 `.value` 的明确边界，不在多处散写同一个字符串。
- 测试里的重复角色、状态、平台、错误码和 fixture key 也要集中，避免测试与生产协议漂移。

## 项目结构与归属

- 新建文件前确认包结构、运行入口、测试目录、导入方向和发布方式，不把脚本随意丢在 root。
- 应用代码优先放项目既有包目录，例如 `src/<package>/` 或现有 application/service/domain/infrastructure 分层。
- 测试放现有 `tests/`、`test/` 或同包测试目录；不要把测试夹在生产包里，除非项目已有该约定。
- CLI、任务脚本、迁移脚本、一次性工具分别放到项目已有 `cli/`、`scripts/`、`tasks/`、`migrations/` 等位置。
- 包内资源读取优先用 `importlib.resources`，不要依赖当前工作目录拼相对路径。

## 环境与依赖

- 环境发现顺序：项目缓存、IDE/项目配置、锁文件/配置文件、`.venv`、shell 环境、`which python/python3/uv/poetry/pytest`，最后才查本机候选。
- 优先复用项目已有工具链：
  - `uv.lock` 或 `uv.toml`：优先 `uv sync`、`uv run ...`。
  - `poetry.lock`：优先 `poetry install`、`poetry run ...`。
  - `Pipfile.lock`：优先 `pipenv install`、`pipenv run ...`。
  - `requirements*.txt`：优先 `.venv` + `python -m pip install -r ...`。
  - 只有标准库或简单脚本：可用 `python -m venv .venv`，但不自动改全局解释器。
- 依赖声明优先在 `pyproject.toml`、锁文件或项目已有依赖文件中维护；不要只在本机环境 `pip install` 后不记录。
- 开发依赖和测试依赖放 dependency groups、optional dependencies、requirements-dev 或项目已有 dev 依赖分组，不混入运行依赖。
- 不提交 `.venv`、缓存、构建产物、真实密钥、token、生产地址。

## 运行与命令

- 优先使用项目文档、Makefile、justfile、tox、nox、CI、`pyproject.toml` scripts 或现有 README 中的命令。
- 运行模块优先 `python -m package.module` 或工具链包装命令，例如 `uv run python -m ...`、`poetry run python -m ...`。
- 安装或运行工具优先 `python -m pip`、`python -m pytest`、`python -m ruff`，避免解释器和命令来自不同环境。
- 脚本要支持可重复运行：参数显式、路径可配置、日志清晰、失败返回非零退出码，不依赖当前目录的隐式状态。
- 涉及文件、网络、数据库、队列、外部 API 时，超时、重试、批量大小和连接配置必须可配置。

## 测试与验证

- 优先识别项目测试框架：pytest、unittest、tox、nox、coverage、hypothesis、pytest-asyncio、pytest-django、pytest-cov。
- pytest 项目优先运行最小目标：`python -m pytest path/to/test_file.py::test_name`；需要全量时再跑目录或完整套件。
- unittest 项目优先 `python -m unittest` 或项目已有命令。
- 测试命名和发现规则跟随项目配置；pytest 常见为 `tests/`、`test_*.py`、`*_test.py`。
- 单元测试覆盖纯函数、边界值、异常路径、空值、类型转换、配置缺失、外部失败；集成测试覆盖数据库、文件、网络、队列等边界。
- mock 要打在被测代码实际查找对象的位置；不要过度 mock 导致测试只验证 mock 自己。
- 异步代码使用项目已有 async 测试插件和事件循环策略；不要在已有事件循环里乱用 `asyncio.run`。
- 涉及 bug 修复时，优先补一个能复现问题的定向测试；若不能补测试，说明原因并执行最小可复现命令。

## Lint、格式化与类型检查

- 优先运行项目已有命令，例如 `ruff check`、`ruff format --check`、`black --check`、`isort --check-only`、`mypy`、`pyright`、`tox -e lint`。
- Ruff 项目优先复用 Ruff 配置，不再叠加手写风格修复；只在触碰范围内修 lint，不做全仓风格重排。
- 类型检查只对触碰范围和直接调用链做最小补强；不要为了消除一个错误大面积重写模型、协议或 API。
- 不滥用 `Any`、`cast`、`# type: ignore`。必须使用时写明原因，并尽量指定错误码或缩小作用域。

## 性能与健壮性

- 先用简单清晰实现；只有在数据量、调用频率、延迟或内存压力明确时做性能优化。
- 大文件、流式数据、批量 IO 优先迭代器、生成器、分批处理和上下文管理器，不一次性读入全部内容。
- 热路径避免重复正则编译、重复网络/DB 调用、循环内重复初始化客户端、无界并发和隐式全局缓存。
- 并发选择基于任务类型：IO 密集优先 async 或线程池；CPU 密集评估进程池、向量化、底层库或任务拆分。
- 并发任务必须限制并发数、超时、取消、异常聚合和资源释放；用户、租户、trace、审计上下文显式传入，不依赖线程局部隐式继承。
- 外部调用必须有超时、重试边界、幂等键或去重策略；不要无限重试。

## 安全与配置

- 不把密钥、token、账号、生产 URL 写死在代码、测试或样例里。
- 配置读取优先项目已有配置系统；简单脚本可用环境变量、`.env.example` 或明确参数，但不提交真实 `.env`。
- 文件路径、压缩包、上传文件、命令参数、SQL、模板渲染、反序列化和 `eval/exec` 相关逻辑必须做输入边界检查。
- 生产代码禁止直接拼 shell 命令；必须调用外部命令时使用列表参数、超时、错误码检查和最小权限。

## 参考资料

- Python PEP 8: https://peps.python.org/pep-0008/
- Python PEP 257: https://peps.python.org/pep-0257/
- Python `venv`: https://docs.python.org/3/library/venv.html
- Python `typing`: https://docs.python.org/3/library/typing.html
- Python Packaging `pyproject.toml`: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- Python Packaging dependency groups: https://packaging.python.org/en/latest/specifications/dependency-groups/
- pytest good practices: https://docs.pytest.org/en/stable/explanation/goodpractices.html
- Ruff docs: https://docs.astral.sh/ruff/
- uv docs: https://docs.astral.sh/uv/
