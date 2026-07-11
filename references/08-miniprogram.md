# 小程序、uni-app 与 Taro

## 识别宿主

- 原生小程序：`project.config.json`、`app.json`、WXML/WXSS、`Page`/`Component`。
- uni-app：`pages.json`、`manifest.json`、`App.vue`、`uni_modules`、条件编译。
- Taro：`@tarojs`、`app.config.*`、`page.config.*`、`config/index.*`。
- 同仓库可能同时存在源码、HBuilderX/CLI 宿主和平台产物；先确认真实启动链，不把宿主插件故障误判为业务源码错误。

## 源码与产物

- 不长期编辑 `unpackage/dist`、`miniprogram_npm` 或其他生成产物。
- 页面、组件、分包、静态资源和平台配置遵循现有目录与生成链。
- 条件编译只包围真实平台差异，避免同一业务规则在多个平台分支复制。

## 页面与数据

- `properties`/props、事件、slot、页面参数和接口数据使用平台支持的明确类型与默认值。
- 原生 `setData` 控制频率和 payload，避免大对象、深路径高频更新和不存在字段。
- loading、空态、错误态、重复点击、取消和页面卸载后的异步回调都要有边界。
- 平台 API、授权、登录、支付、订阅消息、文件和隐私能力不得绕过宿主权限与用户同意。
- 页面路径、事件名、storage key、平台 code、超时、重试、分页大小、分包名和条件编译相关业务值使用集中常量、类型或配置；展示文案不作为业务判断 code。

新增或修改的 Page/Component、properties、生命周期、条件编译、WXML/template 和 WXSS/style 注释使用简体中文；平台 API、配置字段和外部协议保持原文。注释说明平台差异、权限、分包、性能和兼容原因，不复述模板结构。

## 分包与体积

- 以当前平台配置和构建输出判断主包、分包、独立分包和预下载，不依赖记忆中的固定体积上限。
- 公共依赖放置要平衡复用与主包体积；避免把页面私有大资源推入公共层。

## 环境与验证

- 先确认 HBuilderX、CLI、Node、平台开发者工具和插件链哪个是真实入口。
- 使用项目脚本进行 typecheck/lint/build；宿主插件报错先核对插件安装、alias、环境变量和版本链。
- 模拟器、真机、上传和发布只在任务明确要求且账号/副作用边界清楚时执行。
- 无法运行宿主时说明静态验证覆盖和仍需人工确认的平台行为。
