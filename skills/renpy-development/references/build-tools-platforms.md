# 工具、测试、构建与平台

## 目录

- 启动器与开发工具
- Lint 与自动化测试
- 桌面发行
- Android、iOS 与 Web
- 更新器、下载器与内购
- 安全和故障处理

## 启动器与开发工具

启动器用于创建、选择、运行、编辑、检查、翻译和构建项目。常用开发能力：

- Developer Menu。
- 控制台。
- Image Location Picker。
- Interactive Director。
- 重新加载脚本。
- 样式检查器和 screen 分析。
- 截图。

开发功能不得进入面向玩家的正式流程。发布前确认开发者模式、控制台和调试 UI 配置符合发行要求。

## Lint 与自动化测试

每次结构性变更后运行 Lint。Lint 能发现：

- 未定义或冲突的 label/image。
- 无法到达或异常的流程。
- 资源和声明问题。
- 部分 screen、translation 和 build 问题。

Lint 不能替代游玩测试。

Ren'Py 8.5.x 文档增加了 Automated Testing/Testcases。若目标版本支持：

- 为启动、分支、screen 交互和关键回归路径编写自动化测试。
- 测试必须使用目标 SDK 执行。
- 保留手动验证：视觉演出、音频、设备输入、存读档和平台打包。

命令行以目标 SDK 自带 launcher/renpy 可执行文件为准。执行前查看该版本 `cli` 和 `testcases` 文档，不凭记忆假设参数。

## 桌面发行

在 `options.rpy` 中维护：

- `config.name`
- `config.version`
- `build.name`
- 可执行文件、图标、存档目录、窗口和显示配置
- build classify / archive 规则

构建前：

1. 升级决策已完成并阅读 incompatible changes。
2. Lint 通过。
3. 从全新用户目录测试新游戏。
4. 使用旧存档测试升级。
5. 删除不应发布的源素材、设计文档、密钥和测试文件。
6. 检查许可证、第三方组件和字体授权。
7. 对 Windows、macOS、Linux 的目标包分别启动验证。

## Android、iOS 与 Web

### Android

需要 Android 工具链、包名、版本号、图标、签名和权限配置。验证：

- 触摸与返回键。
- 刘海和安全区。
- 暂停/恢复。
- 存储和权限。
- 包体、下载和设备性能。
- 正式签名与升级安装。

### iOS

需要 macOS/Xcode、Bundle ID、签名证书和 provisioning。验证触摸、安全区、生命周期、音频会话和商店要求。

### Web

Web 构建受到浏览器存储、自动播放、下载大小、线程、文件和网络限制。验证：

- 首次加载和缓存。
- 移动浏览器内存。
- 音频必须经用户交互启动的情况。
- 存档持久性和清理浏览器数据后的行为。
- HTTPS 和跨域限制。

ChromeOS、树莓派等目标应查看对应版本文档并在真机测试。

## 更新器、下载器与内购

- Updater：发布稳定的更新元数据、签名/HTTPS 和回滚方案。
- Mobile Downloader：将大资源与基础包拆分，处理离线、重试、校验和空间不足。
- IAP：商品 ID、恢复购买、失败和取消路径必须测试；不要自行存储支付敏感信息。

所有网络与商店功能都需要失败路径和版本兼容策略。

## 安全和故障处理

- 不打包 API 密钥、签名私钥或后台管理员凭据。
- 不信任玩家输入、下载内容和外部文件。
- 网络使用 HTTPS，限制解析内容和写入位置。
- 分发前检查第三方 Python 库的许可与平台兼容性。

故障顺序：

1. 读取 `traceback.txt`。
2. 读取 `log.txt` 和 lint 输出。
3. 确认错误发生的 SDK 版本和平台。
4. 缩小到最小 label/screen/asset。
5. 检查最近修改、缩进、命名和资源路径。
6. 清理项目 `game/cache/` 或重新编译仅作为诊断步骤，不把清缓存当根因修复。
7. 检查 `display_problems`、`problems`、环境变量和目标平台文档。

对应官方文档：`launcher`、`developer_tools`、`director`、`cli`、`build`、`android`、`ios`、`web`、`chromeos`、`raspi`、`iap`、`updater`、`downloader`、`security`、`problems`、`environment_variables`、`template_projects`。Ren'Py 8.5.x 另见 `testcases` 和 `display_problems`。
