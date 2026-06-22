# 图像、文本与演出

## 目录

- 图像命名与显示
- 位置、变换与 ATL
- 转场
- 文本与可视组件
- 层叠式图像
- 高级演出
- 性能与可读性

## 图像命名与显示

Ren'Py 可根据 `game/images/` 中的文件名自动定义图像。文件名去掉扩展名并转为小写后成为图像名；目录名不参与自动名称。

```text
images/bg classroom day.webp  -> bg classroom day
images/yuri casual smile.png  -> yuri casual smile
```

基本语句：

```renpy
scene bg classroom day
show yuri casual smile at center
hide yuri
```

- 图像名第一部分是 tag，同 tag 的新图像会替换旧图像。
- `scene` 清理场景层并显示新图像。
- `show` 显示或替换图像。
- `hide` 按 tag 隐藏。
- 用 `onlayer`、`behind`、`zorder` 处理多层和遮挡，但保持层级方案简单。

显式定义：

```renpy
image logo = "gui/logo.webp"
image yuri silhouette = Solid("#111")
```

## 位置、变换与 ATL

简单位置：

```renpy
show yuri smile at left
show akira normal at right
```

自定义 transform：

```renpy
transform portrait_left:
    xalign 0.18
    yalign 1.0

transform enter_from_left:
    xalign -0.3
    ease 0.35 xalign 0.18
```

ATL 可表达时间、插值、并行、循环、事件和条件。常用语句包括：

- `linear`、`ease`、`pause`
- `parallel`
- `repeat`
- `choice`
- `on show`、`on hide`、`on replace`
- `function`

避免让 ATL 修改叙事状态；它应主要负责视觉表现。需要确定性的剧情事件时放回脚本流程。

## 转场

```renpy
scene bg street night
with fade

show yuri worried
with dissolve
```

常用内置转场包括 `dissolve`、`fade`、`pixellate`、`move` 和图像式转场。多个 `scene/show/hide` 后的一个 `with` 会一次性呈现累计变化。

不要滥用长转场。跳过模式、自动播放和频繁表情切换下，应保持节奏可接受。

## 文本与可视组件

文本支持插值、样式、文本标签、超链接、慢速文本、Ruby/竖排等能力。玩家输入必须谨慎处理文本标签；需要时使用安全替换或禁用标签解释。

常见 displayable：

- `Text`、`Image`、`Solid`
- `Frame`、`Transform`
- `Composite`、`LiveComposite`
- `ConditionSwitch`、`ShowingSwitch`
- `DynamicDisplayable`
- `Movie`

优先使用标准 displayable 和 screen language 组合 UI。只有标准机制无法表达时才创建自定义 displayable。

## 层叠式图像

`layeredimage` 适合把身体、服装、表情、配件拆成组合层：

```renpy
layeredimage yuri:
    always:
        "yuri_body"

    group outfit:
        attribute casual default
        attribute uniform

    group face:
        attribute neutral default
        attribute smile
        attribute angry
```

调用：

```renpy
show yuri casual smile
```

设计要点：

- 每组设置明确默认值。
- 属性名保持稳定，避免同名语义冲突。
- 控制服装与表情组合数量，避免无意义的资源爆炸。
- 用条件属性表达真正依赖状态的层，不要把剧情逻辑藏进美术组合。

## 高级演出

- `3dstage`：透视、深度、摄像机和 3D 变换。
- `matrixcolor`：亮度、色相、饱和度、对比度和颜色矩阵。
- `textshaders` / shader parts：文本与渲染着色器。
- `Live2D`：模型、动作、表情与口型，需要匹配平台和 SDK 支持。
- `Movie`：视频背景、过场、透明视频，需验证编码和平台兼容性。

这些能力均可能受 Ren'Py 版本、渲染器和目标平台影响。实现前核对目标版本文档并在实际设备测试。

## 性能与可读性

- 使用适合目标分辨率的纹理，不要无条件加载超大原图。
- 对大量组合立绘关注预测、缓存和显存。
- 避免每帧创建新 displayable、字符串或复杂 Python 对象。
- 确保角色轮廓、明暗、对话框与背景有足够对比度。
- 动效需兼容减少动态效果的用户需求；重要信息不能只靠动画传达。

对应官方文档：`displaying_images`、`text`、`displayables`、`transforms`、`transform_properties`、`transitions`、`matrixcolor`、`layeredimage`、`3dstage`、`live2d`、`textshaders`。
