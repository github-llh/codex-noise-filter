# Vue、React 与 TypeScript

## 项目识别

- 从 `package.json`、lockfile、`tsconfig`、Vite/webpack/Next/Nuxt 配置和源码语法确认框架版本、包管理器和 workspace。
- 使用项目已有组件库、design tokens、状态管理、路由和 API client；不要混入另一代框架范式。
- 构建产物、生成类型和 vendor 文件默认不编辑，修复回到源码或生成配置。

## 组件与契约

- 组件保持单一职责。页面编排、业务状态、数据请求和通用展示能力分层清楚。
- Vue 明确 props、emits、slots；React 明确 props、children、回调和 ref 边界。公开组件契约使用可读类型，不用 `any` 透传业务数据。
- 复用项目已有组件和 composable/hook；仅当共同语义稳定且状态所有权清楚时抽离。
- 列表 key 使用稳定业务标识；不要用随机值或会变化的 index 掩盖重渲染问题。

## 状态、请求与路由

- 明确状态所有者，派生值使用 computed/selector，不复制多份可变状态。
- 副作用声明真实依赖并处理取消、竞态、重复提交、loading、空态和错误态。
- API 请求/响应、分页、筛选、排序和错误结构使用项目类型；页面已有控件不代表后端参数已接通，必须核对传递链。
- 路由守卫、权限、认证和 401 处理保持集中，不在页面局部绕过。

## 常量、展示与安全

- 业务状态使用联合类型、`as const` 对象、枚举或后端生成类型；展示文案与业务 code 分离。
- URL、token、超时和环境开关使用项目配置；不要把示例地址或截图值复制为真实配置。
- route name、event name、storage key、请求 header、轮询间隔、分页大小、z-index 层级和断点值按项目模式集中到类型化常量、配置或 design token；颜色、间距、字号和圆角优先复用现有 token，不在组件内重复裸值。
- 动态 HTML、URL、文件上传下载和外部消息需校验；避免 `v-html`、`dangerouslySetInnerHTML` 等未净化输入。
- 样式复用 design tokens，避免无依据的全局覆盖和高特异性补丁。

新增或修改的组件说明、JSDoc/TSDoc、props/emits/slots/children 契约、hook/composable 副作用说明以及 template/JSX/style 注释使用简体中文；组件名、属性名、API 字段和第三方术语保持原文。注释只保留业务原因、可访问性、兼容和非显然状态边界。

## 验证

1. 使用项目声明的 Node 和包管理器。
2. 优先 typecheck、lint 和目标测试；UI 产物变化再运行 build。
3. 交互、视觉、E2E、浏览器或 Computer Use 只在任务明确需要运行态证据时执行。
4. 构建失败先区分 Node/包管理器/依赖审批与代码错误。
