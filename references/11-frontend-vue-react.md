# Vue / React 前端开发规则

本文件按需读取。只有任务涉及 Vue、React、Vite、前端包管理、运行、测试、组件语法、状态管理、路由、lint/format/type check 或构建时打开。通用布局、状态契约、安全和前后端协同仍见 `04-frontend-rules.md`；不可绕过门禁和既有代码局部对齐仍见 `02-noise-filter-workflow.md`；Node/包管理器环境发现见 `06-environment-discovery.md`。

参考来源：Vue 3 官方文档、Vue 2 官方文档、React 官方文档、Vite、Vue Test Utils、Testing Library、Vitest 官方文档。

## 目录

- [触发与读取](#触发与读取)
- [项目识别](#项目识别)
- [Vue 2 规则](#vue-2-规则)
- [Vue 3 规则](#vue-3-规则)
- [React 规则](#react-规则)
- [状态、路由与接口](#状态路由与接口)
- [环境与依赖](#环境与依赖)
- [运行与构建](#运行与构建)
- [测试与验证](#测试与验证)
- [Lint、格式化与类型检查](#lint格式化与类型检查)
- [性能、可访问性与安全](#性能可访问性与安全)
- [参考资料](#参考资料)

## 触发与读取

- 看到 `package.json`、`.vue`、`.jsx`、`.tsx`、`vite.config.*`、`vue.config.js`、`next.config.*`、`vitest.config.*`、`jest.config.*`、`playwright.config.*`、`cypress.config.*`、`eslint.config.*` 时按本文件路由。
- 默认组合：`02` + `11`。只涉及通用布局/表单/状态契约时可用 `02` + `04`；涉及环境路径再加 `06`；涉及接口契约或后端数据问题再按索引追加后端 reference。
- 不为 Vue/React 任务一次性读取 Java、Python、Maven reference；触碰范围扩大时再追加。

## 项目识别

- 先读 `package.json` 的 `scripts`、`dependencies`、`devDependencies`、`engines`、`packageManager`，再看 lockfile 和配置文件。
- 版本判断：
  - Vue 2：`vue` 主版本为 2、`vue-template-compiler`、`@vue/cli-service`、Vue Router 3、Vuex 3、`@vue/test-utils` v1。
  - Vue 3：`vue` 主版本为 3、`@vitejs/plugin-vue`、`@vue/compiler-sfc`、Vue Router 4、Pinia、`@vue/test-utils` v2。
  - React：`react`、`react-dom` 主版本决定可用 API；Next、Remix、CRA、Vite、Rsbuild 等框架先按项目配置识别。
- 不按文件后缀猜版本；Vue 2 和 Vue 3 都可能使用 `.vue`，React 也可能混用 `.js/.jsx/.ts/.tsx`。
- 修改前确认 TypeScript、JSX、SFC、CSS Modules、Sass/Less、Tailwind、组件库、状态库、路由库和测试框架。

## Vue 2 规则

- 默认使用 Options API：`data()`、`computed`、`methods`、`watch`、生命周期钩子和 `this` 上下文。
- 组件 `data` 必须是函数，避免组件实例共享状态。
- 不使用 Vue 3 专属语法：`createApp`、`<script setup>`、`defineProps`、`defineEmits`、`defineExpose`、`Teleport`、`Suspense`、多根节点、Vue Router 4 API、Pinia 默认范式，除非项目明确装了兼容插件并已有同类写法。
- Vue 2 响应式存在对象新增属性和部分数组变更限制；新增响应式字段时优先初始化完整数据结构，或复用项目已有 `Vue.set`/`this.$set` 风格。
- 组合式写法只有在项目明确使用 `@vue/composition-api` 且已有范式时才继续使用。
- 过滤器、事件总线、mixins 等历史写法只在项目已有且触碰范围内需要兼容时保留；新增复杂复用逻辑优先抽到 util、service、store 或组件组合，不继续扩大隐式耦合。
- Vue 2 测试优先 `@vue/test-utils` v1；不要用 Vue Test Utils v2 API。

## Vue 3 规则

- 优先跟随项目现有风格：`<script setup>` + Composition API、普通 `setup()`，或 Options API；不要在同一组件里无理由混杂。
- 使用 Composition API 时，`ref`、`reactive`、`computed`、`watch`、`watchEffect`、生命周期函数要保持依赖清晰；模板自动解包不代表脚本里可以省略 `.value`。
- `props` 和 `emits` 必须声明清楚；TypeScript 项目优先类型化 `defineProps`、`defineEmits`，避免父子组件靠隐式字段通信。
- 复杂业务逻辑、请求逻辑、复用状态不要堆在 SFC 顶层；抽到 composable、store、api client、service 或领域 util。
- `watch` 用于副作用，`computed` 用于派生值；不要用 watcher 维护可以由 computed 表达的状态。
- Vue 3 状态管理优先复用项目已有 Pinia/Vuex；Pinia 项目不要新增 Vuex 范式，Vuex 项目不要无批准迁移 Pinia。
- Vue 3 测试优先 `@vue/test-utils` v2、Vue Testing Library 或项目已有 Vitest/Jest 配置。

## React 规则

- 函数组件和 Hooks 为默认优先；类组件只在项目已有或兼容旧代码时维护。
- Hooks 必须在组件或自定义 Hook 顶层调用，不在条件、循环、回调或嵌套函数中调用。
- `useEffect` 用于外部同步和副作用，不把纯派生计算塞进 effect；能在 render 期间计算的值不要额外存 state。
- `useMemo`、`useCallback` 只用于明确的性能或引用稳定性需求，不为“看起来高级”到处包。
- 复杂状态优先 `useReducer`、状态机、store 或领域 Hook；不要把多段业务流程散落在多个 `useState` 和 effect 里。
- 组件 props、事件、children、ref、context 边界要类型化；TypeScript 项目避免无意义 `any` 和过宽 `React.FC` 约束。
- React 版本相关 API 必须先确认版本；不要在 React 17/18 项目中直接使用只在更高版本或特定框架中可用的 API。
- Next/Remix 等框架项目要区分客户端组件、服务端组件、loader/action、路由约定和构建边界，不把纯客户端写法硬塞进服务端文件。

## 状态、路由与接口

- API 请求集中到项目已有 api client/service，不在组件里散写 base URL、token、header、错误处理和重复映射。
- 保留权限、路由守卫、鉴权刷新、租户/组织上下文、埋点、分页、筛选、排序、缓存和错误处理。
- 表单状态、校验、提交中、重复提交防护和错误提示必须按项目已有组件库/表单库处理。
- 固定状态、类型、来源、动作、阶段、结果等闭合集合优先集中为 enum/常量/字典映射；不要在模板和 JSX 中散写魔法字符串。
- 跨多个页面复用的展示组装、字段映射、字典翻译、权限过滤、下载/上传流程，应抽到 composable、hook、store、service 或 mapper。

## 环境与依赖

- 包管理器优先级来自项目文件：`packageManager`、`pnpm-lock.yaml`、`yarn.lock`、`package-lock.json`、`bun.lockb`、`bun.lock`、`.npmrc`、`.yarnrc.yml`、`.nvmrc`、`.node-version`、Volta 配置。
- 优先使用项目已有包管理器和锁文件；不要混用 npm/yarn/pnpm/bun 导致 lockfile 变更。
- 不新增 UI 库、状态库、请求库、测试库、lint/format 工具，除非项目已有范式或用户明确批准。
- 环境变量按构建工具规则处理：Vite 客户端变量必须使用项目约定前缀，通常是 `VITE_`；不要把密钥暴露到客户端 bundle。
- 不提交 `.env.local`、真实 token、生产地址、构建产物、缓存目录。

## 运行与构建

- 先读 `package.json` scripts，优先使用项目已有 `dev`、`serve`、`start`、`build`、`preview`、`lint`、`typecheck`、`test` 命令。
- Vite 项目通常使用 `npm/pnpm/yarn/bun run dev`、`build`、`preview`；Vue CLI 项目通常使用 `serve`、`build`。
- 多 package/workspace 项目先确认 workspace root 和目标 package，使用项目已有 filter/workspace 命令，不在错误目录安装或运行。
- 启动 dev server 前检查端口和已有进程；需要浏览器验证时使用当前项目命令启动，并给出实际 URL。
- 构建失败先看 TypeScript、lint、环境变量、别名解析、CSS 预处理器、Node 版本、包管理器版本和 lockfile。

## 测试与验证

- 优先使用项目已有测试框架：Vitest、Jest、Vue Test Utils、Vue Testing Library、React Testing Library、Cypress、Playwright。
- 单测优先定向运行触碰文件或测试名；必要时再跑完整套件。
- Vue 2 用 Vue Test Utils v1；Vue 3 用 Vue Test Utils v2 或 Vue Testing Library。
- React 组件测试优先验证用户可见行为和交互，不依赖组件内部实现细节。
- 修改布局或交互时，至少验证关键页面的加载、空状态、错误状态、提交中状态和移动/桌面宽度。
- 修改请求或缓存时，覆盖成功、失败、空数据、权限不足、重复提交和刷新场景。
- E2E 只覆盖关键业务流，不用 E2E 代替所有组件单测。

## Lint、格式化与类型检查

- 优先运行项目已有命令：`lint`、`lint:fix`、`typecheck`、`test`、`test:unit`、`test:e2e`、`build`。
- TypeScript 项目必须关注类型错误，不用 `any`、`as unknown as`、`// @ts-ignore` 掩盖契约问题；必须使用时说明原因并缩小作用域。
- ESLint/Prettier/Stylelint 配置按项目执行；不要因为局部修改触发全仓格式化。
- 只修触碰范围和直接调用链的 lint/type 问题；历史全仓问题记录边界，不扩大重构。

## 性能、可访问性与安全

- 大列表优先分页、虚拟滚动或懒加载；不要把全量数据渲染进 DOM。
- 图片、图表、富文本、编辑器、地图、代码高亮等重组件优先懒加载和按需加载。
- Vue `computed` / React memoization 只用于真实派生值或性能热点；不要用 watcher/effect 堆同步状态。
- 交互元素必须保留语义、键盘可达、焦点管理、aria/label、错误提示和 loading 状态。
- `v-html`、`dangerouslySetInnerHTML`、动态 URL、文件下载、iframe、第三方脚本必须确认可信来源和转义/白名单策略。
- 不把鉴权、权限、租户隔离、数据脱敏只放在前端；前端只做展示和交互保护，后端仍是最终边界。

## 参考资料

- Vue 3 Guide: https://vuejs.org/guide/introduction.html
- Vue 3 Composition API FAQ: https://vuejs.org/guide/extras/composition-api-faq
- Vue 2 Guide: https://v2.vuejs.org/v2/guide/
- React Learn: https://react.dev/learn
- React Hooks: https://react.dev/reference/react/hooks
- Vite Guide: https://vite.dev/guide/
- Vite Env and Modes: https://vite.dev/guide/env-and-mode
- Vue Test Utils v2: https://test-utils.vuejs.org/guide/
- Vue Test Utils v1: https://v1.test-utils.vuejs.org/
- Vitest: https://vitest.dev/guide/
- React Testing Library: https://testing-library.com/docs/react-testing-library/intro/
- Vue Testing Library: https://testing-library.com/docs/vue-testing-library/intro/
