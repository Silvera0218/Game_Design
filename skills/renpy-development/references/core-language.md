# Ren'Py 核心语言

## 目录

- 项目与脚本
- 初始化与变量
- 角色与对白
- 标签与流程
- 选项与条件
- 音频、影片与语音
- 常见错误

## 项目与脚本

Ren'Py 会将 `game/` 下的 `.rpy` 源文件作为同一套脚本处理。文件名主要用于组织，真正的流程入口和跳转目标是 label。

常见文件：

```text
game/
  script.rpy
  characters.rpy
  story/
  images/
  audio/
  gui/
  tl/
  options.rpy
  gui.rpy
  screens.rpy
```

只编辑 `.rpy`，不要编辑编译产物 `.rpyc`。使用四空格缩进，语句块必须保持一致。

## 初始化与变量

使用 `define` 声明初始化后不应改变的对象：

```renpy
define e = Character("艾琳", color="#c8ffc8")
define config.window_title = "星光来信"
```

使用 `default` 声明会随新游戏、存档、读档和回滚变化的状态：

```renpy
default affection = 0
default visited_rooftop = False
default inventory = []
```

不要用 `define` 承载之后会修改的游戏状态。不要在初始化阶段执行依赖玩家存档或外部环境的副作用。

单行 Python：

```renpy
$ affection += 1
```

多行 Python：

```renpy
python:
    score = max(0, score)
    route_name = "good" if affection >= 5 else "normal"
```

## 角色与对白

```renpy
define narrator = Character(None)
define mc = Character("我", color="#d9e7ff")
define yuri = Character("尤莉", color="#ffd2e8")

label start:
    "没有名字前缀的旁白。"
    mc "这是角色对白。"
    yuri "文本可使用变量：[player_name]。"
```

把角色对象、颜色、回调、头像和发声配置集中定义。玩家可输入的名字使用 `default` 保存，不要用字符串拼接构造可翻译句子。

对白常用能力：

- 文本插值：`[variable]`
- 文本标签：颜色、速度、停顿、字体、链接等
- `extend`：让下一段文字延续当前说话框
- `window show` / `window hide`：控制对话窗
- `nvl` 角色：使用 NVL 模式
- `voice`：为下一句对白绑定语音

## 标签与流程

入口：

```renpy
label start:
    call prologue
    jump chapter_1
```

可复用场景使用 `call` 和 `return`：

```renpy
label prologue:
    "序章。"
    return
```

单向流程使用 `jump`：

```renpy
label chapter_1:
    jump ending
```

带参数的 label：

```renpy
label grant_affection(amount=1):
    $ affection += amount
    return
```

调用时为每个 `call` 指定稳定的 `from` 点有助于脚本重构和旧存档兼容；可让 Ren'Py 自动生成或在维护时保留现有 `from` 名称。

## 选项与条件

```renpy
menu:
    "陪她去天台" if not visited_rooftop:
        $ visited_rooftop = True
        $ affection += 1
        jump rooftop

    "先回教室":
        jump classroom
```

```renpy
if affection >= 5:
    jump good_ending
elif affection >= 2:
    jump normal_ending
else:
    jump bad_ending
```

选择条件应可预测且由存档状态决定。不要在条件表达式中执行修改状态、网络请求或文件写入。

## 音频、影片与语音

```renpy
play music "audio/theme.ogg" fadein 1.0
play sound "audio/door.opus"
queue music "audio/theme_loop.ogg"
stop music fadeout 1.0
```

将 BGM、音效、环境声和语音分配到合适的 channel。频繁切换音乐时使用淡入淡出；短音效通常不循环。

影片：

```renpy
play movie "movies/opening.webm"
$ renpy.pause(hard=True)
stop movie
```

语音：

```renpy
voice "voice/ch01/yuri_001.ogg"
yuri "你终于来了。"
```

大规模配音项目应使用一致的语音编号、缺失语音检查和 voice sustain/标签策略。

## 常见错误

- `define affection = 0` 后在剧情中修改：改为 `default`。
- label 名重复：Ren'Py 编译或 lint 会报冲突。
- `call` 到的 label 没有 `return`：流程会继续落入后续 label。
- 分支只改局部临时值但未保存到 store：读档后结果不一致。
- 在菜单条件、screen 表达式或角色回调中产生副作用。
- 使用绝对磁盘路径引用资源。
- 依赖 `.rpy` 文件排列理解流程；label 跳转才是可靠结构。

对应官方文档：`language_basics`、`label`、`dialogue`、`menus`、`python`、`conditional`、`audio`、`audio_filters`、`movie`、`voice`。
