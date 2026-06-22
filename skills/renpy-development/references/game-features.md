# 常用视觉小说功能

## 目录

- NVL 与多角色对白
- 气泡、头像与输入
- 历史、画廊、音乐室与回放
- 拖放、精灵与手势
- 成就
- 启动画面和模式

## NVL 与多角色对白

NVL 模式适合在屏幕中保留多段文本：

```renpy
define n = Character(None, kind=nvl)
define yuri_nvl = Character("尤莉", kind=nvl)

label diary:
    n "九月十二日。"
    yuri_nvl "今天的风很温柔。"
    nvl clear
```

需要 ADV/NVL 混用时明确切换窗口和清屏行为。多角色同时对白应使用官方多角色机制，避免用图像拼出不可访问的文字。

## 气泡、头像与输入

- 气泡式对白：适合漫画化演出，需要处理锚点、角色位置和屏幕边缘。
- side image：根据当前说话角色或属性自动显示头像。
- 文本输入：使用 `renpy.input()` 或 `input` screen，处理长度、默认值和文本标签。

```renpy
$ player_name = renpy.input("你的名字？", length=16).strip()
if not player_name:
    $ player_name = "旅人"
```

玩家输入进入对白时防止恶意或意外文本标签被解释。

## 历史、画廊、音乐室与回放

默认历史 screen 依赖引擎记录的对话历史。自定义时保留：

- 说话者。
- 文本。
- 语音重播。
- 可访问性。
- 长文本和多语言布局。

画廊和音乐室通常由持久化解锁条件驱动。回放使用 Replay 机制，避免污染正常剧情状态。

设计解锁：

```renpy
default persistent.cg_rooftop = False
```

在首次达成时设置，再由画廊按钮读取。回放结束必须安全返回回放上下文。

## 拖放、精灵与手势

- Drag and Drop：拼图、道具摆放、地图节点。定义拖拽组、吸附、边界和 drop 回调。
- SpriteManager：大量简单精灵的高效管理。
- Gesture：触摸平台手势输入。

这些功能需要实际设备测试。为拖拽和手势提供键盘、按钮或其他替代输入，避免把关键流程锁死在单一操作。

## 成就

使用 Ren'Py Achievement API 定义、授予、同步和清除成就。平台成就服务可能需要额外集成。

原则：

- 成就 ID 发布后保持稳定。
- 授予操作应幂等。
- 本地和平台状态需要同步策略。
- 不把成就显示文本当作内部 ID。

## 启动画面和模式

- `splashscreen`：Logo、警告、片头。
- presplash：引擎启动前的静态等待画面。
- mode：描述当前交互模式，影响窗口和 UI 行为。
- lifecycle：进入菜单、剧情、回放、加载等阶段的行为。

启动流程应支持跳过或依法显示必要警告，并避免过长不可跳过动画。

对应官方文档：`nvl_mode`、`multiple`、`bubble`、`side_image`、`input`、`history`、`rooms`、`drag_drop`、`sprites`、`gesture`、`achievement`、`splashscreen_presplash`、`modes`、`keymap`。
