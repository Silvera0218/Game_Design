# 高级 Python、扩展与渲染

## 目录

- 何时扩展
- 等效语句与 API
- Creator-Defined Displayable
- Creator-Defined Statement
- 文本标签与角色回调
- 模型、矩阵和着色器
- 网络、截图与 `_ren.py`
- 风险检查

## 何时扩展

优先顺序：

1. Ren'Py 脚本语句。
2. screen language、Action、Value、style。
3. Transform/ATL 和标准 displayable。
4. 普通 Python 函数和数据类。
5. Creator-Defined Displayable/Statement、渲染模型或 `_ren.py`。

越靠后，与引擎生命周期、预测、回滚、保存和平台的耦合越高。

## 等效语句与 API

许多 Ren'Py 语句有 Python 等效函数，例如显示图像、跳转、调用 screen、播放音频等。只有在动态行为确实需要时使用等效 API；普通剧情优先保留可读的 Ren'Py 语句。

API 调用必须确认：

- 是否允许在初始化、互动或 screen 求值阶段调用。
- 是否参与预测。
- 是否改变可回滚状态。
- 是否在所有目标平台可用。

## Creator-Defined Displayable

CDD 用于标准 displayable 无法表达的自定义绘制或交互。实现通常涉及 render、event、per_interact、visit 等协议。

要求：

- render 必须快速且避免不必要分配。
- 正确报告尺寸和子 displayable。
- 事件返回值和 redraw 调度符合引擎协议。
- 自定义状态可保存、可回滚，或明确排除。
- 适配缩放、触摸和不同渲染器。

能用 screen + Transform 完成的组件不要升级为 CDD。

## Creator-Defined Statement

CDS 用于为项目或库增加新的脚本语法。需要定义解析、执行、预测、lint、翻译和可能的下一语句行为。

发布库时：

- 语法保持稳定。
- 给出明确错误信息。
- 支持 lint 和预测。
- 不与内置语句或其他库冲突。
- 测试旧版本和目标版本兼容范围。

## 文本标签与角色回调

自定义文本标签用于特殊排版和内联 displayable。必须处理：

- 参数解析和错误。
- 嵌套文本。
- 慢速文本和跳过。
- self-voicing/替代文本。
- 翻译。

角色回调可用于口型、音效、日志或演出事件。回调会在对白生命周期的多个阶段触发，应快速、幂等，并避免不可逆副作用。

## 模型、矩阵和着色器

- `Color` / `Matrix` / `MatrixColor`：颜色与几何变换。
- Model-based renderer：网格、纹理、uniform 和渲染操作。
- Shader parts：组合引擎着色器片段。
- Text shaders：文本级视觉效果。

高级渲染必须：

- 锁定目标 Ren'Py 版本。
- 验证 GL2/ANGLE/平台渲染差异。
- 提供低性能或不支持平台的降级方案。
- 记录 uniform、纹理、坐标空间和混合模式。

## 网络、截图与 `_ren.py`

- `fetch`：HTTPS/HTTP 请求；处理超时、离线、证书、响应大小和数据验证。
- screenshot：保存或获取截图；遵循可写目录和平台权限。
- `_ren.py`：让 Python 模块集成 Ren'Py；适合库开发，不是普通剧情脚本的默认选择。

Web 平台网络受浏览器 CORS 和沙箱约束。不要把秘密放进客户端，也不要信任服务器返回数据。

## 风险检查

- 是否破坏预测或 screen 重求值？
- 是否破坏保存、加载或回滚？
- 是否持有无法序列化的对象？
- 是否每帧分配或执行昂贵 Python？
- 是否有跨平台 API？
- 是否与翻译、自发声和跳过兼容？
- 是否需要 lint、自动测试和版本门控？

对应官方文档：`statement_equivalents`、`other`、`cdd`、`cds`、`custom_text_tags`、`character_callbacks`、`color_class`、`matrix`、`matrixcolor`、`model`、`shader_parts`、`textshaders`、`fetch`、`screenshot`、`ren_py`。
