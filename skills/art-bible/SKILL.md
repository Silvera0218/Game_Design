---
name: art-bible
description: "指导性的、逐节的艺术圣经创作。创建控制所有资产生产的视觉识别规范。在 /brainstorm 获得批准之后、/map-systems 或任何 GDD 创作开始之前运行。"
---

## 第 0 阶段：解析参数和上下文检查

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

Read `design/gdd/game-concept.md`。如果不存在，则失败并显示：
> “没有找到游戏概念。先运行`/brainstorm`——艺术圣经是在游戏概念获得批准后编写的。”

game-concept.md 摘录：
- 游戏名称（暂定名称）
- 核心幻想和电梯推介
- 游戏支柱（全部）
- **视觉识别锚**部分（如果存在）（来自头脑风暴第 4 阶段艺术总监的输出）
- 目标平台（如果注明）

**改造模式检测**：Glob `design/art/art-bible.md`。如果文件存在：
- Read 完整版
- 对于 9 个部分中的每一个，检查正文是否包含真实内容（多于 `[To be designed]` 占位符或类似内容）与 empty/placeholder
- 建立截面状态表：

```
Section | Status
--------|--------
1. Visual Identity Statement | [Complete / Empty / Placeholder]
2. Color Palette | ...
3. Lighting & Atmosphere | ...
4. Character Art Direction | ...
5. Environment & Level Art | ...
6. UI Visual Language | ...
7. VFX & Particle Style | ...
8. Asset Standards | ...
9. Style Prohibitions | ...
```

- 将此表呈现给用户：
  > “在 `design/art/art-bible.md` 找到现有的艺术圣经。[N] 部分已完成，[M] 需要内容。我将仅处理不完整的部分 - 现有内容不会被触及。”
- 仅适用于状态为：空或占位符的部分。不要重新创作已经完成的部分。

如果该文件不存在，则这是一个新的创作会话 - 正常进行。

Read `.codex/docs/technical-preferences.md`（如果存在）— 提取性能预算和资产标准约束引擎。

---

## 第一阶段：框架

在创作任何内容之前，介绍会话上下文并提出两个问题：

使用带有两个选项卡的 `AskUserQuestion`：
- 选项卡 **“范围”** — “今天需要编写哪些部分？”
  选项：`Full bible — all 9 sections` / `Visual identity core (sections 1–4 only)` / `Asset standards only (section 8)` / `Resume — fill in missing sections`
- 选项卡**“参考”** —“您有定义视觉方向的参考游戏、电影或艺术吗？”
  （自由文本 - 让用户输入特定标题。请勿在此处预设选项。）

如果 game-concept.md 有视觉识别锚点部分，请注意：
> “通过头脑风暴找到了一个视觉识别锚点：‘[anchor name] — [one-line rule]’。我将用它作为艺术圣经的基础。”

---

## 第 2 阶段：视觉识别基础（第 1-4 节）

这四个部分定义了核心视觉语言。 **所有其他部分都源于它们。** 在移动到下一个之前编写每个部分并将其写入文件。

### 第 1 部分：视觉识别声明

**目标**：一行视觉规则加上 2-3 个解决视觉歧义的支持原则。

如果 game-concept.md 中存在视觉锚点：呈现它并询问：
- “直接从这个锚点建造？”
- “先修改一下再扩展？”
- “用新的选择重新开始？”

**代理委托（强制）**：通过 Task 生成 `art-director`：
- 提供：游戏概念（电梯间距、核心幻想）、完整支柱组、平台目标、第一阶段框架中的任何参考 games/art、视觉锚点（如果存在）
- 要求：“为这款游戏起草一份视觉识别声明。提供：(1) 一条可以解决任何视觉决策模糊性的单行视觉规则，(2) 2-3 个支持性视觉原则，每个原则都有一个句子设计测试（‘当 X 不明确时，该原则要求选择 Y’）。将所有原则直接锚定在所述支柱中 - 每个原则必须服务于特定的支柱。”

将艺术总监的草稿呈现给用户。使用 `AskUserQuestion`：
- 选项：`[A] Lock this in` / `[B] Revise the one-liner` / `[C] Revise a supporting principle` / `[D] Describe my own direction`

Write 批准的部分立即归档。

### 第 2 部分：情绪与氛围

**目标**：按游戏状态划分的情感目标 - 足够具体，可供灯光艺术家进行工作。

对于每个主要游戏状态（例如，探索、战斗、胜利、失败、菜单 - 适应该游戏的状态），定义：
- 主要 emotion/mood 目标
- 照明特性（一天中的时间、色温、对比度）
- 大气描述符（3-5 个形容词）
- 能量水平（狂热/测量/沉思/等）

**代理委托**：通过 Task 生成 `art-director` 以及视觉识别声明和支柱集。要求：“为该游戏中的每个主要游戏状态定义情绪和氛围目标。要具体——‘黑暗和不祥’是不够的。说出确切的情绪目标、照明角色（warm/cool、high/low 对比度、一天中的时间方向）以及至少一个承载情绪的视觉元素。每种游戏状态必须在视觉上与其他状态不同。”

Write 批准的部分立即归档。

### 第三节：形状语言

**目标**：使游戏世界在视觉上连贯且可区分的几何词汇。

Cover:
- 人物轮廓哲学（缩略图大小的可读性如何？区分每个原型的特征？）
- 环境几何体（angular/curved/organic/geometric - 哪个占主导地位，为什么？）
- UI形状语法（UI是否符合世界审美，或者它是一种独特的HUD语言？）
- 英雄形状与辅助形状（什么吸引眼球，什么后退？）

**代理委托**：通过 Task 生成 `art-director`，并带有视觉识别声明和情绪目标。询问：“定义该游戏的形状语言。将每个形状原则与视觉识别声明和特定游戏支柱联系起来。解释这些形状选择在情感上向玩家传达的信息。”

Write 批准的部分立即归档。

### 第 4 节：颜色系统

**目标**：一个完整的、可生产的调色板系统，满足审美和沟通的需求。

Cover:
- 主要调色板（5-7 种颜色和角色 - 不仅仅是十六进制代码，还有每种颜色在这个世界上的含义）
- 语义颜色的使用（红色传达什么信息？金色？蓝色？白色？建立颜色词汇）
- 每个生物群落或每个区域的色温规则（如果游戏有不同的区域）
- UI 调色板（可能与世界调色板不同 - 明确定义差异）
- 色盲安全：哪些语义颜色需要shape/icon/sound备份

**代理委托**：通过 Task 生成 `art-director`，并带有视觉识别声明和情绪目标。提问：“为这个游戏设计颜色系统。必须解释每个语义颜色分配 - 为什么这个颜色在这个世界上意味着 danger/safety/reward？确定哪些颜色对可能会让色盲玩家失败，并指定需要哪些备用提示。”

Write 批准的部分立即归档。

---

## 第 3 阶段：制作指南（第 5-8 节）

这些部分将视觉识别转化为具体的生产规则。它们应该足够具体，以便外包团队可以在没有额外简报的情况下遵循它们。

### 第五节：角色设计方向

**代理委托**：通过 Task 生成 `art-director`，其中包含第 1-4 部分。询问：“定义该游戏的角色设计方向。涵盖：玩家角色的视觉原型（如果有）、每种角色类型的区分特征规则（玩家如何一眼就能区分出 enemies/NPCs/allies？）、expression/pose 风格目标（stiff/expressive/realistic/exaggerated）以及 LOD 理念（在游戏摄像机距离下保留了多少细节？）。”

Write 已批准的要归档的部分。

### 第 6 节：环境设计语言

**代理委托**：通过 Task 生成 `art-director`，其中包含第 1-4 部分。提问：“定义这款游戏的环境设计语言。涵盖：建筑风格及其与世界 culture/history 的关系、纹理哲学（绘画、PBR 与风格化 — 为什么选择这款游戏？）、道具密度规则（sparse/dense — 是什么推动了每个区域类型的选择？）以及环境讲故事指南（哪些视觉细节应该在没有文字的情况下讲述故事？）。”

Write 已批准的部分要归档。

### 第 7 节：UI/HUD 视觉方向

**代理委托**：并行生成：
- **`art-director`**：UI 的视觉风格 — 叙事与屏幕空间 HUD、版式方向（字体个性、粗细、尺寸层次）、图标风格 (flat/outlined/illustrated/photorealistic)、UI 元素的动画感觉
- **`ux-designer`**：UX 对齐检查 - 视觉方向是否支持该游戏所需的交互模式？标记艺术指导和 readability/accessibility 需求之间的任何冲突。

收集两者。如果它们发生冲突（例如，艺术总监想要精心设计的剧情 UI，但用户体验设计师标记这会降低战斗的可读性），请明确地用两个位置来表达冲突。不要默默解决 - 使用 `AskUserQuestion` 让用户决定。

Write 已批准的要归档的部分。

### 第八节：资产标准

**代理委托**：并行生成：
- **`art-director`**：文件格式首选项、命名约定方向、纹理分辨率层、LOD 级别期望、导出设置原理
- **`technical-artist`**：特定于引擎的硬约束 - 每个资产类别的多边形计数预算、纹理内存限制、材质槽计数、导入器约束、`.codex/docs/technical-preferences.md` 中性能预算中的任何内容

如果任何艺术偏好与技术限制相冲突（例如，艺术总监想要 4K 纹理，但性能预算需要移动 2K），请明确解决冲突 - 记下理想标准和受限标准，并解释权衡。资产标准的模糊性是产生生产成本的根源。

Write 已批准的要归档的部分。

---

## 第 4 阶段：参考方向（第 9 节）

**目标**：精心策划的参考集，具体说明每个来源应采取的内容和应避免的内容。

**代理委托**：通过 Task 生成 `art-director`，并完成第 1-8 部分。询问：“为这个游戏编制一个参考方向。提供 3-5 个参考源（游戏、电影、艺术风格或特定艺术家）。对于每个参考源：命名它，准确指定从中绘制什么视觉元素（不是‘一般美学’——特定的技术、颜色选择或构图规则），并指定要明确避免或偏离的内容（以防止‘试图复制 X’的解读）。参考应该是附加的 - 任何两个参考都不应指向完全相同的方向。”

Write 已批准的部分要归档。

---

## 第五阶段：艺术总监签字

**查看模式检查** — 在生成 AD-ART-BIBLE 之前应用：
- `solo` → 跳过。注意：“跳过 AD-ART-BIBLE — 单人模式。”进入第 6 阶段。
- `lean` → 跳过（不是相位门）。注意：“跳过 AD-ART-BIBLE — 精益模式。”进入第 6 阶段。
- `full` → 正常生成。

所有部分完成后（或阶段 1 的范围集完成），使用门 **AD-ART-BIBLE** (`.codex/docs/director-gates.md`) 通过 Task 生成 `creative-director`。

通行证：艺术圣经文件路径、游戏支柱、视觉识别锚点。

根据 `director-gates.md` 中的标准规则处理判决。将结论记录在艺术圣经的状态标题中：
`> **Art Director Sign-Off (AD-ART-BIBLE)**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]`

---

## 第六阶段：关闭

在介绍后续步骤之前，请检查项目状态：
- `design/gdd/systems-index.md` 是否存在？ → 地图系统已完成，跳过该选项
- `.codex/docs/technical-preferences.md` 是否包含已配置的引擎（不是 `[TO BE CONFIGURED]`）？ → setup-engine 已完成，跳过该选项
- `design/gdd/` 是否包含任何 `*.md` 文件？ → 设计系统已运行，跳过该选项
- `design/gdd/gdd-cross-review-*.md` 是否存在？ → 审核所有 gdds 已完成
- GDD 是否存在（请查看上文）？ → 包括 /consistency-check 选项

使用 `AskUserQuestion` 进行后续步骤。仅包含根据上面的状态检查真正是下一个的选项：

**选项池 - 仅包括尚未完成的情况：**
- `[_] Run /map-systems — decompose the concept into systems before writing GDDs`（如果systems-index.md存在则跳过）
- `[_] Run /setup-engine — configure the engine (asset standards may need revisiting after engine is set)`（如果已配置引擎则跳过）
- `[_] Run /design-system — start the first GDD`（如果存在任何 GDD，则跳过）
- `[_] Run /review-all-gdds — cross-GDD consistency check (required before Technical Setup gate)`（如果 gdd-cross-review-*.md 存在则跳过）
- `[_] Run /asset-spec — generate per-asset visual specs and AI generation prompts from approved GDDs`（包括 GDD 是否存在）
- `[_] Run /consistency-check — scan existing GDDs against the art bible for visual direction conflicts`（包括 GDD 是否存在）
- `[_] Run /create-architecture — author the master architecture document (next Technical Setup step)`
- `[_] Stop here`

仅将字母 A、B、C...分配给实际包含的选项。将最合乎逻辑的管道推进选项标记为 `(recommended)`。

> **始终包含** `/create-architecture` 和“停在这里”作为选项 - 一旦艺术圣经完成，这些始终是有效的后续步骤。

---

## 协作协议

每个部分如下：**问题 → 选项 → 决定 → 草案（来自艺术总监代理）→ 批准 → Write 归档**

- 在没有首先产生相关代理的情况下，切勿起草部分
- Write 每个部分在批准后立即归档 - 不要批量
- 向用户展示所有代理的分歧——永远不要默默地解决艺术总监和技术美工之间的冲突
- 艺术圣经是一份约束文件：它限制未来的决策以换取视觉连贯性。每个部分都应该让人感觉它有效地缩小了解决方案空间。

---

## 建议的后续步骤

艺术圣经获批后：
- 在编写 GDD 之前，运行 `/map-systems` 将概念分解为游戏系统
- 如果尚未配置引擎，请运行 `/setup-engine`（选择引擎后可能需要重新审视资产标准）
- 运行 `/design-system [first-system]` 以开始创作每系统 GDD
- 一旦 GDD 存在，就运行 `/consistency-check`，以根据艺术圣经的视觉规则验证它们
- 运行 `/create-architecture` 生成主架构文档
