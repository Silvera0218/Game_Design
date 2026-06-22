# Ren'Py 项目组织与质量门

## 推荐结构

```text
game/
  script.rpy
  options.rpy
  gui.rpy
  screens.rpy
  characters.rpy
  state.rpy
  story/
    prologue.rpy
    chapter_01.rpy
    endings.rpy
  ui/
    route_map.rpy
    gallery.rpy
  systems/
    achievements.rpy
    migrations.rpy
  images/
  audio/
  voice/
  movies/
  gui/
  tl/
```

小项目无需为结构而拆分；当职责开始混杂时再拆。

## 命名

- label：`chapter_01_start`、`route_yuri_rooftop`
- screen：`route_map`、`affection_panel`
- transform：`portrait_left`、`shake_small`
- style：`route_button`、`route_button_text`
- state：`yuri_affection`、`visited_rooftop`
- persistent：`persistent.cg_rooftop`

避免过短、冲突、含义随剧情变化的命名。

## 代码审查清单

- `define` 和 `default` 使用正确。
- 没有重复 label、screen、transform、image。
- `call` 路径最终 `return`。
- 菜单条件无副作用。
- screen 求值无副作用。
- 没有绝对路径或秘密。
- 新状态有默认值和旧存档策略。
- persistent 有迁移和隐私边界。
- 图片、音频、字体和视频存在且可打包。
- 玩家文本可翻译。
- 控件可用鼠标、键盘和目标设备操作。

## 最小功能验收

```text
主菜单
  → 开始游戏
  → 对白和立绘
  → 选项
  → 状态变化
  → 分支反馈
  → 保存
  → 读档
  → 回滚
  → 结局
  → 返回主菜单
```

## 发布门

`PASS` 需要：

- Lint 无阻断问题。
- 目标路径可完整游玩。
- 存读档和回滚正常。
- 旧存档策略已验证或明确不支持。
- 缺失资源检查通过。
- 目标语言 UI 无明显溢出。
- 目标构建可以启动。
- 无密钥、私有文件或未授权资产进入包。

`CONCERNS`：

- 尚未在真机/目标商店环境测试。
- 视觉、音频或本地化只能人工确认。
- 版本升级后旧存档样本不足。

`BLOCKED`：

- 缺少目标 SDK、签名、商店账户、平台工具链或关键素材。

`FAIL`：

- 语法、lint、运行、流程、存档或构建已知失败。
