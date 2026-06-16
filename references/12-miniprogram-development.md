# 小程序开发规则

本文件按需读取。只有任务涉及微信小程序、其他平台小程序、原生小程序、uni-app、Taro、`project.config.json`、`app.json`、`pages.json`、`app.config.*`、分包、开发者工具模拟器、`miniprogram-ci`、`miniprogram-simulate`、小程序构建产物或小程序测试时打开。文件归属、环境命令、验证策略、安全边界、硬编码、重复逻辑和注释的跨技术栈判断先按 `01-global-engineering-rules.md` 执行；通用前端布局、状态契约和前后端协同见 `04-frontend-rules.md`；Vue/React 语法复用 `11-frontend-vue-react.md`；Node 和开发者工具路径发现见 `06-environment-discovery.md`；不可绕过门禁仍见 `02-noise-filter-workflow.md`。

参考来源：微信小程序官方文档、微信开发者工具与 `miniprogram-ci`/`miniprogram-simulate`、uni-app 官方文档、Taro 官方文档、项目实际脚本和配置。

## 目录

- [触发与读取](#触发与读取)
- [项目形态识别](#项目形态识别)
- [语法与框架选择](#语法与框架选择)
- [文件归属与依赖边界](#文件归属与依赖边界)
- [分包与包体积](#分包与包体积)
- [组件、页面与注释](#组件页面与注释)
- [常量、枚举与配置](#常量枚举与配置)
- [环境与运行](#环境与运行)
- [构建与发布](#构建与发布)
- [测试与验证](#测试与验证)
- [性能、限制与安全](#性能限制与安全)
- [参考资料](#参考资料)

## 触发与读取

- 命中 `app.json`、`app.js`、`app.wxss`、`sitemap.json`、`project.config.json`、`project.private.config.json`、`miniprogramRoot`、`miniprogram_npm`、`wxml`、`wxss`、`wxs`、`wx:`、`setData`、`Component`、`Page`、`Behavior`、`subPackages`、`preloadRule` 时按原生小程序处理。
- 命中 `pages.json`、`manifest.json`、`App.vue`、`uni.scss`、`uni_modules`、`#ifdef MP`、`#ifdef MP-WEIXIN`、`mp-weixin`、`unpackage/dist` 时按 uni-app 处理。
- 命中 `@tarojs/*`、`taro`、`Taro.`、`app.config.js`、`app.config.ts`、`page.config.*`、`config/index.*`、`TARO_ENV`、`dev:weapp`、`build:weapp` 时按 Taro 处理。
- 默认组合：小程序任务读 `02` + `12`。涉及 Vue/React 语法时加 `11`；涉及通用布局、表单、状态契约时加 `04`；执行构建、编译、CI 或发布前校验前加 `06` 并按 `小程序环境缓存` 复用/更新项目配置和 Node 包管理器。只有用户明确要求模拟器、预览、上传或真机验证时，才查开发者工具路径。
- 不因为小程序是前端就一次性读取所有前端、Java、Python reference；触碰接口契约、后端数据或构建链路时再按索引追加。

## 项目形态识别

先读根配置和 `package.json`，不要只看文件后缀猜框架。

- 原生微信小程序：根目录或 `miniprogramRoot` 下有 `app.json`、`app.js`、`app.wxss`、页面 `*.wxml/*.wxss/*.js/*.json`，配置来自 `project.config.json`。
- uni-app：有 `pages.json`、`manifest.json`、`App.vue`、`main.js`/`main.ts`，输出到 `unpackage/dist/dev/mp-*` 或 `unpackage/dist/build/mp-*`，平台语法常见 `#ifdef MP-WEIXIN`。
- Taro：有 `@tarojs/*` 依赖、`src/app.config.*`、`config/index.*`，通过 `taro build --type weapp` 或项目脚本输出到 `dist`。
- 其他跨平台框架或低代码生成：先确认框架文档、生成目录和源码目录；只改源码目录，除非任务明确要求分析生成结果。
- 多端项目必须确认目标平台：`weapp`、`alipay`、`tt`、`swan`、`qq`、`jd`、`ks` 等平台 API 和配置能力不完全一致，不能把微信专属能力默认扩散到所有端。

## 语法与框架选择

- 原生小程序使用官方语法：`Page`、`Component`、`Behavior`、`properties`、`data`、`methods`、`lifetimes`、`pageLifetimes`、`observers`、`wxml`、`wxss`、`wxs` 和 `wx.*` API；不要写浏览器 DOM、`window`、`document`、`localStorage` 或 Node 内置模块。
- 原生小程序更新视图优先精确 `setData` 路径，不把大对象、长列表或临时计算结果整块反复写入 data。
- uni-app 语法先区分 Vue 2 与 Vue 3，并复用 `11-frontend-vue-react.md` 对应规则；平台差异用官方条件编译，不把微信端 API 直接写成所有端通用逻辑。
- Taro 语法先区分 React、Vue 2、Vue 3，再复用 `11-frontend-vue-react.md`；小程序能力通过 Taro API、配置文件和平台条件处理，不直接混用 H5 DOM 习惯。
- 框架项目不绕过框架：uni-app 不直接长期维护生成后的 `mp-weixin` 代码；Taro 不直接把构建产物当源码改；原生项目不引入框架语法片段。

## 文件归属与依赖边界

先执行 `01-global-engineering-rules.md#跨技术栈文件归属与依赖边界`，再按小程序项目形态确认主包、分包、源码目录和生成目录。

- 新建页面前先确认是否属于主包、已有分包、独立分包或跨端共享模块；页面配置、路由配置和实际目录必须一致。
- 新建组件前先查当前分包、业务域组件、全局组件、第三方组件库和框架组件库；只在复用价值、职责隔离或公开契约清晰时新建。
- 主包只放启动必需页面、TabBar 页面、全局配置和真正跨分包公共能力；不把单个业务分包私有依赖放到主包。
- 分包私有组件、图片、工具函数优先放在分包内；跨分包共享依赖需要评估是否进入主包、公共分包、异步分包或框架 split chunk。
- npm 依赖必须确认小程序可用性、包体积、构建方式和 tree shaking 效果。原生微信小程序使用 npm 后必须走开发者工具或 CI 的 npm 构建产物，不手写 `miniprogram_npm`。
- 生成目录、平台目录和源码目录要分清：`dist/`、`unpackage/dist/`、`miniprogram_npm/` 通常是产物；源文件在 `src/`、页面目录、`components/`、`uni_modules/` 或框架约定目录。

## 分包与包体积

分包不是最后才补救，也不要过早把所有页面拆散。出现以下情况必须评估分包：

- 主包接近平台限制、首次启动变慢、TabBar 外页面持续增加。
- 地图、图表、富文本、编辑器、相机、AR、视频、报表、客服、支付后流程等重功能只在局部使用。
- 多业务域天然独立，用户路径明确，且首次访问可接受加载分包。
- 某依赖只在单个业务域使用，放主包会拖慢启动。

分包规则：

- 先查目标平台最新官方限制，不凭记忆写死包体积数字；以开发者工具、CI 上传和官方文档的当前校验为准。
- TabBar 页面、启动页、登录态恢复、全局错误页和跨分包公共启动能力保留在主包。
- 普通分包用于业务域拆分；独立分包用于不依赖主包即可启动的场景；预下载用于明确高概率后续访问的分包，不把所有分包都预下载。
- 分包间避免直接互相引用私有文件。确需共享时抽到主包公共模块、公共分包、框架支持的 shared chunk，或通过服务端/API/缓存传递数据。
- uni-app 分包优先在 `pages.json` 配置，注意目标平台和 App 端是否需要 `manifest.json` 配合。
- Taro 分包优先在 `app.config.*` 配置；混合原生小程序时确认 `subPackages` 指向 Taro 编译后的页面，并评估 `splitChunks`、`addChunkPages` 等依赖拆分策略。

## 组件、页面与注释

- 页面只承载路由参数解析、页面生命周期、用户交互入口和视图状态；复杂业务编排、请求组装、字典翻译、权限判断和重复字段映射抽到 service、store、model、hook/composable、utils 或框架推荐位置。
- 原生组件的 `properties`、`observers`、`lifetimes`、`relations`、`externalClasses`、`options` 是契约位置；复杂字段、兼容逻辑和副作用在这些定义附近注释。
- uni-app 组件注释遵循 Vue 规则；Taro React 组件注释遵循 React 规则；Taro Vue 组件注释遵循 Vue 规则。
- `wxml`、Vue template、JSX 中只保留非显然权限、slot、兼容、可访问性和布局边界注释，不逐行解释绑定和事件。
- 稳定状态、来源、动作、平台、业务类型和页面模式优先集中为 enum/常量映射，不在页面模板和事件处理里散写魔法字符串。

## 常量、枚举与配置

小程序任务也必须执行 `01-global-engineering-rules.md#跨技术栈硬编码治理`。原生、uni-app、Taro 的写法不同，但判断标准一致：固定闭合集合集中，环境可变值配置化，运行期可维护值走字典/后台配置。

按项目形态落地：

- 原生小程序：稳定状态、平台、页面模式、消息格式、storage key、事件名、接口错误码放到 `constants`、`enums`、`model` 或业务域 util，不在 `Page`、`Component`、`wxml` 中散写。
- uni-app：复用 Vue/TypeScript 规则；平台差异值结合 `pages.json`、`manifest.json`、条件编译和集中常量，不把微信端 code 当全端通用值。
- Taro：复用 React/Vue/TypeScript 规则；路由、页面配置、平台能力、消息格式、请求 header、storage key 集中在 config、constants、service 或 model 层。
- 平台和环境配置：`appid`、baseUrl、上传域名、白名单、机器人 webhook、订阅消息模板、支付参数、CI 上传密钥等不得写死在页面逻辑里；按官方配置、环境变量、项目配置或服务端下发处理。
- 动态业务字典：渠道、分类、模板、租户策略等如果可后台维护，不写死到小程序包里。

注意：

- 主包和分包私有常量要分清；分包私有值不要为了复用一点点就上升到主包公共模块。
- 模板中不要用裸字符串做业务判断；先在脚本层转成语义化状态或字典映射，再渲染。
- 测试、mock 和小程序 CI 脚本也要复用同一批常量，避免发布时和运行时代码不一致。

## 环境与运行

先执行 `01-global-engineering-rules.md#跨技术栈环境与命令`，再按 `14-environment-cache-by-stack.md#小程序环境缓存` 读取/复用 `.codex/local-environment.json`、小程序项目配置、框架平台、源码目录、输出目录、构建脚本和必要的 Node 包管理器。

- 首先读取项目脚本和配置：`package.json`、lockfile、`project.config.json`、`project.private.config.json`、`pages.json`、`manifest.json`、`config/index.*`。
- 有 `package.json` 的小程序项目必须同时按 `14-environment-cache-by-stack.md#node前端环境缓存` 读取 Node 版本、包管理器、lockfile、`scripts` 和框架依赖版本；缓存命中同一 framework、platform、sourceRoot、outputRoot、packageJson 和构建脚本时直接复用。
- 原生微信小程序：默认优先执行项目已有构建、编译或 CI 脚本；不默认用微信开发者工具模拟器打开工程。
- uni-app：CLI 项目默认优先使用项目已有 `build:mp-weixin` 或 `build:custom` 脚本；不默认运行到 HBuilderX/小程序模拟器。
- Taro：默认优先使用项目已有 `build:weapp` 或 `taro build --type weapp`；构建后不默认用微信开发者工具打开输出目录。
- 首次运行需要开发者工具路径时，按 `14-environment-cache-by-stack.md#小程序环境缓存` 从缓存、IDE/项目配置、本机候选路径发现并验证；不要把未验证路径写成长期规则。
- 不混用 npm/yarn/pnpm/bun；锁文件和 `packageManager` 按 `11-frontend-vue-react.md` 执行。

## 构建与发布

- 构建命令必须来自项目 scripts 或框架配置，不凭经验替换包管理器或输出目录。
- 构建/编译/CI 失败且疑似框架版本、目标平台、包管理器、lockfile、`miniprogramRoot`、`sourceRoot`、`outputRoot`、条件编译、Taro/uni-app 脚本、开发者工具 CLI 或 `miniprogram-ci` 不匹配时，必须重跑 `14-environment-cache-by-stack.md#小程序环境缓存`，更新缓存后用同一目标命令重试一次。
- 原生小程序发布、预览或上传属于操作性验证/发布链路，只有用户明确要求时才执行；默认只确认构建配置、`appid`、`miniprogramRoot`、`setting`、npm 构建产物和忽略规则。
- uni-app 发布到微信小程序通常生成 `unpackage/dist/build/mp-weixin`；自动上传依赖 HBuilderX/CI 插件、上传密钥、`appid` 和 IP 白名单，密钥不得提交。
- Taro 小程序 CI 可复用项目已有 `@tarojs/plugin-mini-ci` 或 `miniprogram-ci` 脚本；不要自行新增上传能力，除非用户明确要求。
- 发布脚本不得在日志或 README 中暴露私钥、机器人编号、生产 `appid` 密钥、上传 token、平台后台截图和白名单信息。

## 测试与验证

先执行 `01-global-engineering-rules.md#跨技术栈验证策略`，再选择小程序框架和目标平台的验证方式。

- 原生组件单测只在用户明确要求、任务本身是测试修复或需要复现 bug 时运行；可复用项目已有 Jest + `miniprogram-simulate`，但它不等价于完整小程序集成测试。
- 原生小程序默认验收优先使用项目已有 CLI/CI 脚本完成编译或构建；不默认预览、上传、打开模拟器或真机验证。
- uni-app 默认验收优先使用项目已有 CLI 构建或编译脚本；HBuilderX 自动化测试、页面级自动化、开发者工具关键路径只在用户明确要求时执行。
- Taro 测试优先使用项目已有 Jest/Vitest/Testing Library/框架测试；默认补 `build:weapp` 这类构建验证，不默认开发者工具模拟器预览。
- 修改分包、路由、启动页、TabBar、登录态、授权、支付、分享、定位、文件上传下载时，默认先做构建/编译验证；模拟器关键路径、真机验证、预览上传只有用户明确要求时才执行。
- 用户明确要求官方模拟器、真机、预览、上传或 CI 操作但无法运行时，说明缺少的开发者工具路径、登录态、密钥、权限或平台账号，不用假验证替代。

## 性能、限制与安全

先执行 `01-global-engineering-rules.md#跨技术栈安全与外部边界`，再处理小程序平台限制和审核边界。

- 优先控制主包体积、首屏资源、同步初始化、全局依赖和首次 `setData` 数据量。
- 大图、视频、富文本、地图、图表、编辑器、模型文件等资源优先 CDN、懒加载、分包或按需加载；不要把重资源塞进主包。
- 避免频繁 `setData`、大对象 `setData`、长列表全量渲染、无分页请求、无节流搜索和生命周期重复请求。
- 小程序运行环境不是浏览器：不要依赖 DOM、BOM、cookie、浏览器存储、跨域代理、动态执行脚本或未支持的 Node API。
- 权限、登录、手机号、定位、相册、摄像头、蓝牙、支付、订阅消息、隐私弹窗等能力必须按平台官方流程处理；前端只做交互保护，服务端仍需校验。
- 外部链接、web-view、插件、第三方 SDK、动态 URL、文件下载和富文本必须确认白名单、可信来源、转义和平台审核要求。
- 平台限制、包体积上限、基础库能力和审核规则会变化；涉及这些点时优先查官方文档、开发者工具校验和项目配置，不把旧经验写死进业务代码。

## 参考资料

- 微信小程序分包加载: https://developers.weixin.qq.com/miniprogram/dev/framework/subpackages.html
- 微信小程序 npm 支持: https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html
- 微信开发者工具 CI / miniprogram-ci: https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html
- miniprogram-ci npm: https://www.npmjs.com/package/miniprogram-ci
- miniprogram-simulate npm: https://www.npmjs.com/package/miniprogram-simulate
- miniprogram-simulate GitHub: https://github.com/wechat-miniprogram/miniprogram-simulate
- uni-app pages.json: https://uniapp.dcloud.net.cn/collocation/pages.html
- uni-app manifest.json: https://uniapp.dcloud.net.cn/collocation/manifest.html
- uni-app 快速上手与小程序模拟器: https://uniapp.dcloud.net.cn/quickstart
- uni-app CLI: https://uniapp.dcloud.net.cn/worktile/CLI.html
- uni-app 自动化测试: https://uniapp.dcloud.net.cn/worktile/auto/quick-start.html
- Taro 全局配置: https://docs.taro.zone/docs/app-config
- Taro 编译配置: https://docs.taro.zone/docs/config
- Taro CLI: https://docs.taro.zone/docs/cli
- Taro 微信小程序独立分包: https://docs.taro.zone/docs/independent-subpackage
- Taro 原生项目使用 Taro: https://docs.taro.zone/docs/taro-in-miniapp
- Taro 小程序持续集成: https://docs.taro.zone/docs/plugin-mini-ci
