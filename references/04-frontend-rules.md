# 前端规则

本文件只处理通用前端布局、状态契约、局部对齐和前后端协同。文件归属、环境命令、验证策略、安全边界、硬编码和重复逻辑先按 `01-global-engineering-rules.md` 判断；本 skill 根据文件证据、项目配置、命令节点、报错输出、触碰范围和调用链内部判定是否继续读取技术栈 reference。命中原生 HTML/CSS/JavaScript/TypeScript、Vue 2、Vue 3、React、Vite、组件语法、包管理、运行、测试、lint/format/type check 或前端构建时，继续读取 `11-frontend-vue-react.md`；命中微信小程序、uni-app、Taro、分包、开发者工具模拟器、`project.config.json`、`app.json`、`pages.json` 或 `app.config.*` 时，继续读取 `12-miniprogram-development.md`。

## 基本原则

- 优先检查布局链路：`flex`、`grid`、`overflow`、`position`、`z-index`、容器宽高和响应式约束。
- 优先修复 CSS、组件属性和容器布局。
- 不通过修改后端接口解决前端问题。
- 保留权限、分页、搜索、加载状态、空状态和错误处理。
- 不新增依赖，除非当前任务目标已明确授权并完成影响评估。

## 布局与组件

- 使用现有设计系统、组件库、主题变量和目录结构。
- 不引入与现有 UI 风格冲突的视觉模式。
- 文本不能溢出按钮、卡片、表格、弹窗和侧边栏。
- 固定格式 UI 元素要有稳定尺寸或响应式约束，例如 `min-width`、`max-width`、`aspect-ratio`、grid track。
- 表格、列表、筛选区和详情页优先保证密度、扫描效率和重复操作效率。
- 复杂页面先确认容器链路，再改局部样式。
- 不用魔法宽高掩盖结构问题；确需兼容时说明原因。

## 状态契约与安全

先执行 `01-global-engineering-rules.md#跨技术栈安全与外部边界`，再处理前端展示和交互层保护。

- 保留鉴权、权限按钮、路由守卫、租户隔离相关逻辑。
- 保留分页、搜索条件、排序、筛选、刷新、加载、错误和空状态。
- 前端字段、类型、枚举、分页参数必须与后端契约一致。
- 不用前端硬编码掩盖后端数据问题。
- 请求失败不能静默吞掉；按现有模式展示错误或记录。
- 表单要保留校验、禁用态、提交中态和重复提交防护。

## 代码规范

- 优先复用现有组件、hooks、stores、utils、api client。
- 命名清晰，职责单一，不把业务规则散落到多个组件。
- 业务判断优先集中到已有领域层或组合函数，避免模板里堆复杂表达式。
- 不随意变更路由、接口路径、请求参数名、响应字段和权限 key。
- 注释只解释复杂业务原因、兼容边界、魔法值来源和风险，不重复 UI 行为。

## 前端自动局部对齐门禁

这是本 skill 执行中的内部自动触发规则，不依赖用户额外说“补注释”“抽魔法值”“格式化”或“检查前端”，也不受任意第三方调用、App、CLI、IDE 插件、MCP/ACP、hook、subagent、路由转发、未知 wrapper 或模型路由影响。只要新增、修改、阅读、检索、lint/format/typecheck 修复、构建失败定位、截图/diff 审查或调用链确认触碰前端文件，就必须在同一语义单元内同步执行局部对齐判断。

触发文件和对象：

- 文件：`.vue`、`.js`、`.jsx`、`.ts`、`.tsx`、`.mjs`、`.cjs`、`.html`、`.css`、`.scss`、`.less`、`.wxml`、`.wxss`、`package.json`、`tsconfig.json`、`jsconfig.json`、`vite.config.*`、`vue.config.js`、`next.config.*`、`nuxt.config.*`、`app.config.*`、`pages.json`、`project.config.json`。
- 对象：组件、页面、hook、composable、store、router、api client、service、model、schema、mapper、adapter、mock、fixture、测试、样式 token、构建和 lint 配置。
- 信号：前端控制台错误、Node 构建失败、TypeScript 报错、ESLint/Prettier/Biome/Stylelint 报错、UI 截图中的源码、接口字段不一致、模板/JSX/wxml 中业务判断、重复展示映射、裸 `any` 或无类型公开属性。

自动检查项：

1. 注释契约：导出类型、组件 props/emits/slots/children、hook/composable 返回值、api request/response、路由 meta、权限字段、外部协议字段和配置项，必须按项目已有 JSDoc、类型声明、Story、测试或 README 风格补最小必要说明。
2. 魔法值和常量：状态、类型、来源、平台、权限 code、路由 name、事件名、storage key、query key、content type、错误码、阈值、展示映射、mock code 和 fixture key，必须先查现有 constants、model、dict、i18n、router、api contract、生成类型或 SDK 常量；能低风险闭环时同步集中。
3. 类型边界：TypeScript 项目不得把业务 props、请求响应、页面参数、事件回调和公开组件 API 写成裸 `any`、`Object`、`Function` 或过宽 `Record<string, any>`；JavaScript 项目也要复用 PropTypes、Vue `type`/`validator`、JSDoc 或运行期校验范式。
4. 抽象边界：重复条件、重复展示映射、重复字段转换、重复默认值、重复请求适配和跨页面复用逻辑，先判断是否进入 hook/composable、selector、mapper、adapter、store、service 或局部 helper；页面私有且一次性语义清楚时可以只局部集中。
5. 格式化与验证：格式错误先按项目 ESLint/Prettier/EditorConfig/Biome/Stylelint/TypeScript 配置修触碰范围；修完后仍必须回扫同一组件、函数、类型或配置块的注释、魔法值、类型和契约缺口，不能只让 formatter 通过。
6. 编码与中文乱码：组件文案、i18n、模板、HTML `charset`、响应头、构建输出、CSS content、mock/fixture 或终端日志出现中文字符、乱码、`encoding`/`charset` 信号时，必须追加 `01#跨技术栈编码与中文乱码门禁`，并在验证前核对 active cache path 的前端规范文件和 charset/locale 依据。

补齐和修改边界：

- 低风险闭环：问题落在当前组件/页面/函数/类型/config 或已闭环调用链内，兼容路由、接口字段、权限 key、序列化值、展示文案和测试 fixture 时，直接按 `11` 或 `12` 同步补齐。
- 不直接修改：缺少业务语义、会改变 API/路由/权限/接口 code、需要新增依赖、跨多个业务域迁移、可能影响后端契约或生成代码来源不明时，只记录风险和所需证据。
- 不扩大范围：只处理触碰范围、已闭环调用链和为完成任务必须读取的相关文件；全仓历史风格问题不借机重构。

## 前端验证

先执行 `01-global-engineering-rules.md#跨技术栈验证策略`，再按项目栈选择最小充分验证。

按项目栈选择最小充分验证：

```bash
npm run lint
npm run typecheck
npm run test
npm run build
pnpm lint
pnpm typecheck
pnpm test
pnpm build
yarn lint
yarn typecheck
yarn test
yarn build
```

验证前先读 `package.json` scripts，使用项目已有命令。若修改布局或交互，默认仍以命令侧验证为准；浏览器页面检查、桌面/移动宽度检查和点击操作只在当前任务目标需要交互/视觉证据且权限边界清楚时执行。

默认不做操作验证：

- 前端技术栈任务完成后，默认不启动浏览器、不使用 Browser/Computer Use、不操控电脑屏幕点击验证。
- 默认验收优先使用项目已有 `build`、`typecheck`、`lint` 或等价语法/编译命令；编译/构建通过即可交付。
- 只有当前任务目标本身是浏览器、截图、页面点击、视觉回归、端到端交互或电脑屏幕操作验证，且权限与副作用边界清楚时，才启动 dev server、打开页面或进行点击验证。
- 如果当前任务不需要浏览器验证，即使修改了布局或交互，也只说明“未做浏览器点击验证，已按命令侧验证通过/未能运行原因”。

## 前后端协同

- 先确认问题属于前端展示、接口契约、后端数据还是解析链路。
- 字段不一致时优先查 API DTO 与调用链，不直接前端兜底硬编码。
- 契约必须变更时优先兼容旧逻辑，并列出影响范围。
