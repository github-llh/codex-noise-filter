# Python 开发

## 环境与结构

- 从 `pyproject.toml`、lockfile、`.python-version`、tox/nox 和 CI 判断 Python 版本、包管理器和命令。
- 优先项目虚拟环境与 `uv`/Poetry/pip-tools 等既有流程；不直接向全局 Python 安装依赖。
- 源码、测试、脚本、迁移和生成产物按现有 package 布局放置；避免通过修改 `sys.path` 掩盖包结构问题。

## 类型与模型

- 公共函数、复杂返回值、配置、DTO 和跨模块边界使用明确类型。
- 动态输入优先 `TypedDict`、dataclass、Pydantic/项目 schema、Protocol 或 `unknown` 等价的运行期校验方式；避免大范围 `Any`。
- 有限字符串集合按项目版本和风格使用 `Enum`、`StrEnum` 或 `Literal`，保持序列化值兼容。
- 状态、事件名、环境变量 key、路径片段、时间格式、超时、重试和批次大小使用有领域含义的模块常量、Enum 或类型化配置；不要为短小局部值制造无意义常量。
- 默认参数不要使用可变对象；资源使用 context manager，异常链使用 `raise ... from ...` 保留原因。

新增或修改的模块、类、公共函数 docstring 和复杂逻辑注释使用简体中文；标识符、库名、异常类型、CLI 参数和外部协议保持原文。docstring 说明输入输出、异常、副作用和兼容边界，不重复函数名可表达的内容。

## IO、异步与安全

- 文本 IO 显式指定项目要求的 `encoding`；路径使用 `pathlib` 并校验输入边界。
- 异步代码避免在 event loop 中执行阻塞 IO；并发数、超时、取消和清理要可控。
- 不使用 `eval/exec`、不安全反序列化或未限制的 shell 参数；subprocess 优先参数数组且检查退出码。
- 密钥和环境差异来自受控配置，不进入源码、fixture 或日志。

## 测试与质量

- 优先目标 pytest、现有 fixture 和最小复现场景；不要通过删除断言或扩大 mock 范围制造通过。
- 按项目配置运行 Ruff/Flake8、Black、isort、mypy/pyright 中实际存在的工具。
- 修改 CLI、文件、网络或数据库逻辑时覆盖退出码、异常、空输入、编码、超时和资源清理。
- 解释器或依赖问题与代码问题分开报告。
