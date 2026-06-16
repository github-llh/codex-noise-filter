# Vue / React 前端开发规则

本文件按需读取。只有任务涉及 Vue、React、Vite、前端包管理、运行、测试、组件语法、状态管理、路由、lint/format/type check 或构建时打开。文件归属、环境命令、验证策略、安全边界、硬编码、重复逻辑和注释的跨技术栈判断先按 `01-global-engineering-rules.md` 执行；通用布局、状态契约和前后端协同仍见 `04-frontend-rules.md`；不可绕过门禁和既有代码局部对齐仍见 `02-noise-filter-workflow.md`；Node/包管理器环境发现见 `06-environment-discovery.md`。

参考来源：Vue 3 官方文档、Vue 2 官方文档、React 官方文档、Vite、Vue Test Utils、Testing Library、Vitest 官方文档。

## 目录

- [触发与读取](#触发与读取)
- [项目识别](#项目识别)
- [组件创建规则](#组件创建规则)
- [组件使用规则](#组件使用规则)
- [Vue 2 规则](#vue-2-规则)
- [Vue 3 规则](#vue-3-规则)
- [React 规则](#react-规则)
- [组件注释位置](#组件注释位置)
- [状态、路由与接口](#状态路由与接口)
- [枚举、常量与配置](#枚举常量与配置)
- [环境与依赖](#环境与依赖)
- [运行与构建](#运行与构建)
- [测试与验证](#测试与验证)
- [Lint、格式化与类型检查](#lint格式化与类型检查)
- [性能、可访问性与安全](#性能可访问性与安全)
- [参考资料](#参考资料)

## 触发与读取

- 看到 `package.json`、`.vue`、`.jsx`、`.tsx`、`vite.config.*`、`vue.config.js`、`next.config.*`、`vitest.config.*`、`jest.config.*`、`playwright.config.*`、`cypress.config.*`、`eslint.config.*` 时按本文件路由。
- 默认组合：`02` + `11`。只涉及通用布局/表单/状态契约时可用 `02` + `04`；执行编译、构建、typecheck、lint 或测试前必须加 `06` 读取/复用 Node 前端环境缓存；涉及接口契约或后端数据问题再按索引追加后端 reference。
- 不为 Vue/React 任务一次性读取 Java、Python、Maven reference；触碰范围扩大时再追加。

## 项目识别

- 先读 `package.json` 的 `scripts`、`dependencies`、`devDependencies`、`engines`、`packageManager`，再看 lockfile 和配置文件。
- 版本判断：
  - Vue 2：`vue` 主版本为 2、`vue-template-compiler`、`@vue/cli-service`、Vue Router 3、Vuex 3、`@vue/test-utils` v1。
  - Vue 3：`vue` 主版本为 3、`@vitejs/plugin-vue`、`@vue/compiler-sfc`、Vue Router 4、Pinia、`@vue/test-utils` v2。
  - React：`react`、`react-dom` 主版本决定可用 API；Next、Remix、CRA、Vite、Rsbuild 等框架先按项目配置识别。
- 不按文件后缀猜版本；Vue 2 和 Vue 3 都可能使用 `.vue`，React 也可能混用 `.js/.jsx/.ts/.tsx`。
- 修改前确认 TypeScript、JSX、SFC、CSS Modules、Sass/Less、Tailwind、组件库、状态库、路由库和测试框架。

## 组件创建规则

先执行 `01-global-engineering-rules.md#跨技术栈文件归属与依赖边界`，再按 Vue/React 组件类型确认目录和公开契约。

- 新建组件前先确认归属：业务域、页面私有组件、通用基础组件、表单组件、表格/列表组件、弹窗/抽屉组件、布局组件、图表/可视化组件或第三方封装组件。
- 只有满足以下任一条件时才新建组件：跨页面/跨模块复用、单组件过大且职责混杂、需要隔离复杂交互、需要稳定公开 props/slots/children 契约、需要独立测试或 Story/示例。
- 不为两三行模板或一次性静态片段过度拆组件；可读性更强时保留在父组件中。
- 组件名必须表达业务或 UI 角色，避免 `CommonComponent`、`BaseItem`、`TempModal` 这类泛名。Vue SFC 和 React 组件文件按项目约定使用 PascalCase 或既有命名范式。
- 目录位置跟随项目结构：页面私有组件放页面目录下的 `components/`，跨业务复用放业务域共享目录，真正通用基础组件才放全局 `components/common`、`shared` 或设计系统目录。
- 组件公开 API 要小而稳定：props/emit/slots/children/ref 暴露必要能力，不把父组件内部数据结构整体透传。
- 展示组件只负责渲染和轻交互；容器组件负责取数、权限、路由、状态协调；业务规则和接口调用优先下沉到 store、service、api client、composable、hook 或 mapper。
- 表单、表格、弹窗、上传、下载、权限按钮等高复用组件必须保留 loading、disabled、error、empty、permission、重复提交防护和可访问性状态。
- 新建组件时同步考虑测试或示例入口：项目已有 Storybook、Histoire、demo、unit test 或 playground 时，按既有规则补最小覆盖。

## 组件使用规则

- 使用组件前先查同业务域、设计系统、组件库和历史页面是否已有同类组件；优先复用，不重复造轮子。
- Vue 组件通信优先 props down / events up；跨层级共享使用项目已有 provide/inject、store 或 composable，不用事件总线继续扩大隐式耦合。
- Vue 插槽用于可变内容区域；默认插槽、具名插槽、作用域插槽要有清晰命名和数据边界，不用插槽传递大块业务状态。
- React 组合优先使用 props、children、render prop、context 或自定义 Hook；共享状态按 React 官方建议提升到最近公共父组件，或复用项目已有 store。
- React props 使用 camelCase；布尔 prop 为 true 时按项目 lint 规则可省略值。避免随意 `{...props}` 透传，除非是明确封装原生元素或第三方组件，并已过滤无关字段。
- 列表渲染必须使用稳定业务 key，不用数组 index 作为默认 key，除非列表完全静态且不会重排、插入、删除。
- 组件使用不能绕过权限、路由守卫、表单校验、错误处理、loading、空状态和重复提交防护。
- 不在模板或 JSX 中堆复杂业务表达式；超过一行且含业务含义的判断，抽到 computed、method、composable、hook、selector 或 mapper。
- 组件库二次封装要保留原组件关键能力：禁用态、错误态、尺寸、插槽/children、事件、aria、class/style 扩展和测试选择器。

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

## 组件注释位置

- 注释遵循通用原则：解释业务原因、边界、兼容性、风险和非显然契约，不重复模板/JSX 正在做什么。
- Vue SFC：组件用途和业务边界写在 `<script>` 中组件定义、`defineOptions`、props/emits 类型附近；复杂 slot 契约写在 slot 对应定义附近；模板注释只保留非显然布局、兼容 hack 或权限边界；样式注释只说明设计 token、覆盖第三方样式或浏览器兼容原因。
- Vue 2 Options API：复杂 `props`、`computed`、`watch`、生命周期副作用和兼容逻辑写在对应 option 附近；不要在 template 顶部堆整段业务说明。
- Vue 3 Composition API：复杂 composable 调用、watch 副作用、跨组件 provide/inject、异步请求和类型化 props/emits 在 `<script setup>` 对应语句附近说明。
- React：组件用途写在组件导出或函数定义上方；复杂 props 契约写在 props type/interface 字段附近；复杂 Hook、副作用、memoization、ref、context 边界写在对应 hook 附近；JSX 内只保留非显然分支、可访问性或兼容注释。
- 测试文件注释解释场景、夹具来源和回归原因；不要注释每一步点击和断言。
- 如果注释必须跨文件解释，优先把契约沉淀到类型、props、emits、slot、hook、composable、README/Story 示例或测试用例中，不用散落的长注释替代清晰 API。

## 状态、路由与接口

- API 请求集中到项目已有 api client/service，不在组件里散写 base URL、token、header、错误处理和重复映射。
- 保留权限、路由守卫、鉴权刷新、租户/组织上下文、埋点、分页、筛选、排序、缓存和错误处理。
- 表单状态、校验、提交中、重复提交防护和错误提示必须按项目已有组件库/表单库处理。
- 固定状态、类型、来源、动作、阶段、结果等闭合集合优先集中为 enum/常量/字典映射；不要在模板和 JSX 中散写魔法字符串。
- 跨多个页面复用的展示组装、字段映射、字典翻译、权限过滤、下载/上传流程，应抽到 composable、hook、store、service 或 mapper。

## 枚举、常量与配置

Vue/React 任务也必须执行 `01-global-engineering-rules.md#跨技术栈硬编码治理`。模板、JSX、store、api client、hook/composable、测试和 mock 中都不能散写同一类魔法字符串或数字。

优先选择：

- TypeScript 项目：固定闭合集合优先使用项目既有风格的 `enum`、字符串联合类型、`as const` 对象或 `Record` 映射；需要运行期遍历、展示、反查时优先 `as const` 对象 + 类型推导或集中字典对象。
- JavaScript 项目：使用冻结常量对象、集中 `constants`/`dict`/`enum` 模块或项目已有字典体系；不要在组件内散写 `"wecom"`、`"markdown"`、`1`、`2`。
- 接口契约值：状态、类型、平台、消息格式、权限 code、路由 name、feature flag key、错误码等放到 api/contract、model、store 或领域 constants，不放在页面模板里。
- 技术标准值：HTTP method、header、content type、storage key、事件名、route name、query key 优先复用项目 api client、router、query key factory 或 SDK 常量。
- 环境变量：base URL、开关、第三方 key、构建模式走 Vite/webpack/框架环境变量规则；客户端 bundle 不得暴露 secret。

处理要求：

- 如果后端已经有枚举或字典接口，前端不要自行创造不兼容 code；优先复用生成类型、OpenAPI 类型、字典接口或项目已有 mapper。
- 展示文案和 code 分离：不要用中文展示文案当业务判断值；i18n 项目把文案放翻译资源。
- 常量抽取不能制造跨业务域依赖；页面私有值可在页面局部集中，跨页面复用才上升到共享模块。
- 测试和 mock 使用同一套 contract 常量，避免测试里写旧 code 导致误判。

## 环境与依赖

先执行 `01-global-engineering-rules.md#跨技术栈环境与命令`，再按 `14-environment-cache-by-stack.md#node前端环境缓存` 读取或更新前端环境缓存。

- 包管理器优先级来自项目文件：`packageManager`、`pnpm-lock.yaml`、`yarn.lock`、`package-lock.json`、`bun.lockb`、`bun.lock`、`.npmrc`、`.yarnrc.yml`、`.nvmrc`、`.node-version`、Volta 配置。
- 优先使用项目已有包管理器和锁文件；不要混用 npm/yarn/pnpm/bun 导致 lockfile 变更。
- 前端命令必须先定位目标 `package.json`，读取 `scripts`、`dependencies`、`devDependencies`、`engines`、`packageManager` 和 lockfile；monorepo 中优先使用触碰文件最近的 package，再结合 workspace root 判断 filter/workspace 命令。
- 选择 Node 版本时必须参考 `engines.node`、`.nvmrc`、`.node-version`、Volta 和构建工具版本要求；本机默认 Node 不匹配时，继续查找已安装候选并更新 `.codex/local-environment.json`。
- `npm`、`pnpm`、`yarn`、`bun` 是包管理器；`npx`、`pnpm dlx`、`yarn dlx` 是命令 runner，必须记录但不能误判为包管理器。
- `.codex/local-environment.json` 已记录同一 `packageJson`、lockfile、Node 约束、包管理器和 selected command 且验证仍通过时，直接复用，不重复查找。
- 不新增 UI 库、状态库、请求库、测试库、lint/format 工具，除非项目已有范式或用户明确批准。
- 环境变量按构建工具规则处理：Vite 客户端变量必须使用项目约定前缀，通常是 `VITE_`；不要把密钥暴露到客户端 bundle。
- 不提交 `.env.local`、真实 token、生产地址、构建产物、缓存目录。

## 运行与构建

先执行 `01-global-engineering-rules.md#跨技术栈环境与命令` 和 `14-environment-cache-by-stack.md#node前端环境缓存`，再选择 Vue/React 项目脚本。

- 先读 `package.json` scripts，优先使用项目已有 `dev`、`serve`、`start`、`build`、`preview`、`lint`、`typecheck`、`test` 命令。
- 默认验收优先选 `build`；没有 `build` 时按项目 scripts 选择 `typecheck`、`compile`、`lint` 或框架等价命令。不要凭经验直接写 `npm run build`，必须使用缓存里匹配的包管理器和脚本。
- Vite 项目通常使用 `npm/pnpm/yarn/bun run dev`、`build`、`preview`；Vue CLI 项目通常使用 `serve`、`build`。
- 多 package/workspace 项目先确认 workspace root 和目标 package，使用项目已有 filter/workspace 命令，不在错误目录安装或运行。
- 默认不启动 dev server 做浏览器点击验证；只有用户明确要求浏览器、截图、页面点击、视觉回归、端到端交互或电脑屏幕操作时，才检查端口、启动当前项目命令并给出实际 URL。
- 构建失败先看 TypeScript、lint、环境变量、别名解析、CSS 预处理器、Node 版本、包管理器版本、lockfile、workspace/filter 和 scripts 选择。若疑似环境或命令不匹配，必须重新执行 Node 前端环境缓存流程，更新 `.codex/local-environment.json` 后用同一目标脚本重试一次。

## 测试与验证

先执行 `01-global-engineering-rules.md#跨技术栈验证策略`，再选择前端定向验证。

- 优先使用项目已有测试框架：Vitest、Jest、Vue Test Utils、Vue Testing Library、React Testing Library、Cypress、Playwright。
- 单测优先定向运行触碰文件或测试名；必要时再跑完整套件。
- Vue 2 用 Vue Test Utils v1；Vue 3 用 Vue Test Utils v2 或 Vue Testing Library。
- React 组件测试优先验证用户可见行为和交互，不依赖组件内部实现细节。
- 修改布局或交互时，默认仍以命令侧验证为准：优先 `build`、`typecheck`、`lint` 或等价语法/编译命令；编译/构建通过即可作为默认验收。
- 不默认执行浏览器点击、页面截图、Playwright/Cypress E2E、Computer Use 或桌面屏幕操作；只有用户明确指定浏览器/点击/截图/视觉/E2E/电脑屏幕验证时才执行。
- 修改请求或缓存时，覆盖成功、失败、空数据、权限不足、重复提交和刷新场景。
- E2E 只覆盖关键业务流，不用 E2E 代替所有组件单测。

## Lint、格式化与类型检查

- 优先运行项目已有命令：`lint`、`lint:fix`、`typecheck`、`test`、`test:unit`、`test:e2e`、`build`。
- TypeScript 项目必须关注类型错误，不用 `any`、`as unknown as`、`// @ts-ignore` 掩盖契约问题；必须使用时说明原因并缩小作用域。
- ESLint/Prettier/Stylelint 配置按项目执行；不要因为局部修改触发全仓格式化。
- 只修触碰范围和直接调用链的 lint/type 问题；历史全仓问题记录边界，不扩大重构。

## 性能、可访问性与安全

先执行 `01-global-engineering-rules.md#跨技术栈安全与外部边界`，再处理浏览器端性能、可访问性和安全细节。

- 大列表优先分页、虚拟滚动或懒加载；不要把全量数据渲染进 DOM。
- 图片、图表、富文本、编辑器、地图、代码高亮等重组件优先懒加载和按需加载。
- Vue `computed` / React memoization 只用于真实派生值或性能热点；不要用 watcher/effect 堆同步状态。
- 交互元素必须保留语义、键盘可达、焦点管理、aria/label、错误提示和 loading 状态。
- `v-html`、`dangerouslySetInnerHTML`、动态 URL、文件下载、iframe、第三方脚本必须确认可信来源和转义/白名单策略。
- 不把鉴权、权限、租户隔离、数据脱敏只放在前端；前端只做展示和交互保护，后端仍是最终边界。

## 参考资料

- Vue 3 Guide: https://vuejs.org/guide/introduction.html
- Vue Components Basics: https://vuejs.org/guide/essentials/component-basics
- Vue Style Guide: https://vuejs.org/style-guide/
- Vue 3 Composition API FAQ: https://vuejs.org/guide/extras/composition-api-faq
- Vue 2 Guide: https://v2.vuejs.org/v2/guide/
- Vue School Slots Guide: https://vueschool.io/articles/vuejs-tutorials/the-complete-guide-to-vue-slots/
- React Learn: https://react.dev/learn
- React Passing Props: https://react.dev/learn/passing-props-to-a-component
- React Sharing State: https://react.dev/learn/sharing-state-between-components
- React Hooks: https://react.dev/reference/react/hooks
- Airbnb React/JSX Style Guide: https://javascript.airbnb.tech/react/
- Vite Guide: https://vite.dev/guide/
- Vite Env and Modes: https://vite.dev/guide/env-and-mode
- Vue Test Utils v2: https://test-utils.vuejs.org/guide/
- Vue Test Utils v1: https://v1.test-utils.vuejs.org/
- Vitest: https://vitest.dev/guide/
- React Testing Library: https://testing-library.com/docs/react-testing-library/intro/
- Vue Testing Library: https://testing-library.com/docs/vue-testing-library/intro/
