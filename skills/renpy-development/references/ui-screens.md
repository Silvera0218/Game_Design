# GUI、Screen Language 与样式

## 目录

- 修改层级
- Screen 基础
- Actions、Values 与函数
- 样式
- 特殊 screen
- Screen 与 Python
- 性能和输入

## 修改层级

优先级从低风险到高风险：

1. 修改 `gui.rpy` 中的颜色、尺寸、字体、间距和图片变量。
2. 替换 `game/gui/` 中的对应资源。
3. 在 `screens.rpy` 中小范围调整现有 screen。
4. 新建独立 screen 和 style。
5. 只有整体交互模型确实不同，才重写模板 GUI。

不要为改一个按钮而整体替换 `screens.rpy`。

## Screen 基础

```renpy
screen affection_panel(target):
    tag overlay
    zorder 100

    frame:
        xalign 0.98
        yalign 0.03

        vbox:
            text "[target.name]"
            bar value target.affection range 10
```

常用结构：

- 布局：`fixed`、`hbox`、`vbox`、`grid`、`side`
- 容器：`frame`、`window`、`viewport`
- 内容：`text`、`image`、`add`
- 控件：`button`、`textbutton`、`imagebutton`、`bar`、`input`
- 组合：`use`、`transclude`
- 条件与循环：`if`、`for`
- 状态：screen 内 `default`

screen 参数应清晰，避免隐式依赖大量全局状态。

## Actions、Values 与函数

按钮优先使用 Action：

```renpy
textbutton "返回" action Return()
textbutton "设置" action ShowMenu("preferences")
textbutton "路线图" action Show("route_map")
textbutton "静音" action Preference("music mute", "toggle")
```

常见 Action：

- `Jump`、`Call`
- `Show`、`Hide`、`ToggleScreen`
- `ShowMenu`、`Return`
- `SetVariable`、`ToggleVariable`
- `SetField`、`ToggleField`
- `Function`
- `FileSave`、`FileLoad`、`FileDelete`
- `Preference`
- `OpenURL`

常见 Value：

- `VariableValue`
- `FieldValue`
- `DictValue`
- `Preference`
- `AnimatedValue`

使用 `Function` 时保证函数快速、可预测，并明确是否修改可回滚状态。不要在 screen 每次求值时直接调用有副作用的表达式。

## 样式

```renpy
style route_button is button:
    xminimum 320
    padding (24, 14)

style route_button_text is button_text:
    color "#ffffff"
    hover_color "#ffd2e8"
```

样式支持继承、前缀状态和 displayable 特性。常见状态前缀：

- `idle_`
- `hover_`
- `selected_`
- `insensitive_`
- `activate_`

把共享外观放入 style；把具体内容和行为留在 screen。先利用模板样式体系，再新增命名样式。

## 特殊 Screen

修改前必须理解其契约。常见特殊 screen：

- `say`、`choice`、`input`
- `main_menu`、`navigation`
- `game_menu`
- `save`、`load`、`file_slots`
- `preferences`
- `history`
- `confirm`
- `notify`
- `skip_indicator`
- `nvl`

特殊 screen 的参数、返回值、tag 和调用方式可能由引擎或模板约定。保留所需参数和行为。

## Screen 与 Python

- screen 局部状态使用 `default`。
- 计算型数据可通过参数、属性或轻量函数提供。
- `show screen` 用于非阻塞显示。
- `call screen` 等待 `Return()` 的结果。
- 需要复用布局时使用 `use`。
- screen 会被反复预测和求值；参数表达式和显示表达式不要有副作用。

## 性能和输入

- 避免在 screen 内创建大列表、排序大数据集或反复读取文件。
- 使用稳定的 displayable 和可预测的数据。
- 大列表使用 viewport/vpgrid，并验证滚轮、触摸和控制器。
- 为键盘与手柄定义 focus 顺序和可见状态。
- 按钮点击区域应适合触摸；重要按钮远离设备安全区。
- 文本需容纳翻译扩展，避免依赖固定像素宽度。
- 对复杂 screen 使用 Ren'Py 的 screen language 分析和性能工具。

对应官方文档：`gui`、`gui_advanced`、`screens`、`screen_actions`、`screen_special`、`screen_optimization`、`screen_python`、`style`、`style_properties`、`config`、`preferences`、`store_variables`、`mouse`。
