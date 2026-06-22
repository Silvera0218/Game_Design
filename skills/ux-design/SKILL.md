---
name: ux-design
description: "针对屏幕、流程或 HUD 进行引导式逐节 UX 规范创作。阅读游戏概念、玩家旅程和相关 GDD，以提供情境感知设计指导。使用工作室模板生成 ux-spec.md（根据 screen/flow）或 hud-design.md。"
---

当该技能被调用时：

## 1. 解析参数并确定模式

根据争论存在三种创作模式：

| Argument | Mode | 输出文件 |
|----------|------|-------------|
| `hud` | HUD 设计 | `design/ux/hud.md` |
| `patterns` | 交互模式库 | `design/ux/interaction-patterns.md` |
| 任何其他值（例如，`main-menu`、`inventory`） | UX 屏幕或流程规范 | `design/ux/[argument].md` |
| No argument | 询问用户 | （见下文） |

**如果没有提供参数**，不要失败——而是询问。使用 `AskUserQuestion`：
- “今天我们要设计什么？”
  - 选项：“特定的屏幕或流程（我会命名它）”，“游戏 HUD”，“交互模式库”，“我不确定 - 帮我弄清楚”

如果用户选择“我将命名它”或键入屏幕名称，请将其标准化为短横线大小写
文件名（例如，“主菜单”变为 `main-menu`）。

---

## 2. 收集上下文（Read 阶段）

Read **在**询问用户任何内容之前的所有相关上下文。技能的价值
来自到达通知。

### 2a：必读内容

- **游戏概念**：Read `design/gdd/game-concept.md` — 如果丢失，警告：
  > “未找到游戏概念。首先运行 `/brainstorm` 来建立游戏的概念
  > 设计UX之前的基础。”
  > 如果用户询问，仍然继续。

### 2b：玩家旅程

Read `design/player-journey.md`（如果存在）。对于每个相关部分，摘录：
- 此屏幕出现在哪个旅程阶段？
- 玩家到达此屏幕时的情绪状态如何？
- 玩家在旅程中需要什么屏幕？
- 该屏幕提供了哪些关键时刻（来自旅程地图）？

如果玩家旅程文件不存在，请记下间隙并继续：
> “在 `design/player-journey.md` 上找不到玩家旅程地图。没有它的设计
> 意味着我们将对玩家背景做出假设。考虑运行一个播放器
> 本规范起草后的旅程会议。”

### 2c：GDD UI 要求

Glob `design/gdd/*.md` 和 grep 用于 `UI Requirements` 部分。 Read 任何 GDD，其
UI 要求部分按名称或类别引用此屏幕。

这些 GDD UI 要求是本规范的**要求输入**。收集它们
作为规范必须满足的约束列表。

如果设计 HUD，请阅读所有 GDD UI 要求部分 — HUD 聚合
每个系统的要求。

### 2d：现有 UX 规格

Glob `design/ux/*.md` 并注意哪些屏幕已有规格。对于屏幕
将链接到当前屏幕或从当前屏幕链接，请阅读其 navigation/flow 部分
找到该规范必须匹配的入口点和出口点。

### 2e：交互模式库

如果`design/ux/interaction-patterns.md`存在，则读取模式目录索引
（模式名称列表及其一行描述）。请勿阅读全文
图案细节——只是目录。这告诉您哪些模式已经存在
所以你可以参考它们而不是重新发明它们。

### 2f：艺术圣经

检查 `design/art/art-bible.md`。如果找到，请阅读视觉方向
部分。 UX 布局必须符合已经做出的美学承诺。

### 2g：辅助功能要求

检查 `design/accessibility-requirements.md`。如果找到，请阅读它。规格
必须满足那里承诺的可访问性层。

### 2h：输入法（来自项目配置）

Read `.codex/docs/technical-preferences.md` 并提取 `## Input & Platform`
部分。存储这些值以便在整个技能中使用——它们驱动
交互地图并告知可访问性要求：

- **输入法** — 例如，Keyboard/Mouse、游戏手柄、触摸、混合
- **主要输入** — 该游戏的主要输入
- **游戏手柄支持** — 全部/部分/无
- **触摸支持** — 全部/部分/无
- **目标平台** — 用于安全区和纵横比决策

如果该部分未配置 (`[TO BE CONFIGURED]`)，请询问一次：
> “输入法还没配置，这个游戏的目标是什么？”
> 选项：“仅限 Keyboard/Mouse”、“仅限游戏手柄”、“两者（PC + 主机）”、“触摸（移动）”、“以上全部”
>
> （运行 `/setup-engine` 以永久保存此信息，这样就不会再次询问您。）

存储本次会议剩余部分的答案。 **不要**按部分再次询问
或每个屏幕。

### 2i：当前背景摘要

在任何设计工作之前，向用户提供一个简短的总结：

> **设计：[Screen/Flow Name]**
> - 模式：[UX Spec / HUD Design / Pattern Library]
> - 旅程阶段：[来自 player-journey.md，或“未知 — 无旅程地图”]
> - GDD 满足此规范的要求：[计数和名称，或“未找到”]
> - 已指定相关屏幕：[列表，或“尚无”]
> - 已知可用模式：[计数，或“尚无模式库”]
> - 辅助功能层：[来自需求文档，或“尚未定义”]
> - 输入方法：[来自technical-preferences.md，或“上面询问”]

然后问：“在我们开始之前我还应该读些什么，还是我们继续？”

---

## 2b.改造模式检测

在创建骨架之前，请检查目标输出文件是否已存在。

Glob `design/ux/[filename].md`（其中 `[filename]` 是第 1 阶段的已解析输出路径）。

**如果文件存在——改造模式：**
- Read 完整文件
- 对于每个预期部分，检查正文是否具有真实内容（超过 `[To be designed]` 占位符）或者是 empty/placeholder
- 向用户呈现部分状态摘要：

> “在 `design/ux/[filename].md` 上找到现有的 UX 规范。以下是已经完成的操作：
>
> | Section | Status |
> |---------|--------|
> | 概述与背景 | [Complete / Empty / Placeholder] |
> | 玩家旅程整合 | ... |
> | 屏幕布局和信息架构 | ... |
> | 交互模型 | ... |
> | 反馈和状态沟通 | ... |
> | Accessibility | ... |
> | 边缘情况和错误状态 | ... |
> | 开放性问题 | ... |
>
> 我将仅处理 [N] 不完整的部分 - 现有内容不会被覆盖。”

- 跳过第 3 部分（骨架创建）——文件已存在
- 在第 4 阶段（节创作）中，仅处理状态为：空或占位符的节
- 使用 `Edit` 就地填充占位符，而不是创建新的骨架

**如果文件不存在 - 全新创作模式：**
照常进入第 3 阶段（创建文件骨架）。

---

## 3. 创建文件骨架

一旦用户确认，**立即**创建带有空部分的输出文件
标头。这确保增量写入有目标并且工作不会中断。

问：“我可以在 `design/ux/[filename].md` 创建骨架文件吗？”

---

### UX 规格的骨架（屏幕或流程）

```markdown
# UX Spec: [Screen/Flow Name]

> **Status**: In Design
> **Author**: [user + ux-designer]
> **Last Updated**: [today's date]
> **Journey Phase(s)**: [from context]
> **Template**: UX Spec

---

## Purpose & Player Need

[To be designed]

---

## Player Context on Arrival

[To be designed]

---

## Navigation Position

[To be designed]

---

## Entry & Exit Points

[To be designed]

---

## Layout Specification

### Information Hierarchy

[To be designed]

### Layout Zones

[To be designed]

### Component Inventory

[To be designed]

### ASCII Wireframe

[To be designed]

---

## States & Variants

[To be designed]

---

## Interaction Map

[To be designed]

---

## Events Fired

[To be designed]

---

## Transitions & Animations

[To be designed]

---

## Data Requirements

[To be designed]

---

## Accessibility

[To be designed]

---

## Localization Considerations

[To be designed]

---

## Acceptance Criteria

[To be designed]

---

## Open Questions

[To be designed]
```

---

### HUD 设计骨架

```markdown
# HUD Design

> **Status**: In Design
> **Author**: [user + ux-designer]
> **Last Updated**: [today's date]
> **Template**: HUD Design

---

## HUD Philosophy

[To be designed]

---

## Information Architecture

### Full Information Inventory

[To be designed]

### Categorization

[To be designed]

---

## Layout Zones

[To be designed]

---

## HUD Elements

[To be designed]

---

## Dynamic Behaviors

[To be designed]

---

## Platform & Input Variants

[To be designed]

---

## Accessibility

[To be designed]

---

## Open Questions

[To be designed]
```

---

### 交互模式库骨架

```markdown
# Interaction Pattern Library

> **Status**: In Design
> **Author**: [user + ux-designer]
> **Last Updated**: [today's date]
> **Template**: Interaction Pattern Library

---

## Overview

[To be designed]

---

## Pattern Catalog

[To be designed]

---

## Patterns

[Individual pattern entries added here as they are defined]

---

## Gaps & Patterns Needed

[To be designed]

---

## Open Questions

[To be designed]
```

---

编写骨架后，更新 `production/session-state/active.md`：
- Task：设计 [screen/flow name] UX 规格
- 当前部分：开始（已创建骨架）
- 文件：design/ux/[filename].md

---

## 4. 逐节创作

按顺序浏览每个部分。对于**每个部分**，请遵循以下循环：

```
Context  ->  Questions  ->  Options  ->  Decision  ->  Draft  ->  Approval  ->  Write
```

1. **上下文**：说明本节需要包含的内容并显示任何相关内容
   来自第二阶段收集的上下文的约束。
2. **问题**：询问起草本节需要什么。使用`AskUserQuestion`
对于有限的选择，对话文本用于开放式探索。
3. **选项**：如果存在设计选择，则使用 pros/cons. 提供 2-4 种方法
   在对话中解释推理，然后使用 `AskUserQuestion` 捕获决策。
4. **决策**：用户选择一种方法或提供自定义方向。
5. **草稿**：Write 对话中的部分内容供审核。临时旗帜
   明确的假设。
6. **批准**：“这是否捕获了它？在将其写入文件之前有任何更改吗？”
7. **Write**：使用 `Edit` 替换 `[To be designed]` 占位符
   内容。确认写入。

编写完每个部分后，更新 `production/session-state/active.md`。

---

### 部分指南：UX 规格模式

#### A 部分：目的和玩家需求

本节是基础。所有其他决定都源于此。

**要问的问题**：
- “这个屏幕的玩家目标是什么？玩家想在这里做什么？”
- “如果这个屏幕不存在或者很难使用，会出现什么问题？”
- “完成这句话：‘玩家到达此屏幕时想要 ___。’ ”

交叉引用第二阶段收集的玩家旅程背景。既定目的
必须与旅程阶段和情绪状态保持一致。

---

#### B 部分：玩家到达时的情况

**要问的问题**：
- “玩家在游戏中什么时候第一次遇到这个屏幕？”
- “他们在到达这个屏幕之前刚刚在做什么？”
- “设计应该呈现什么样的情绪状态？（平静、紧张、好奇、时间压力）”
- “玩家是自愿来到这个界面的，还是游戏派到这里的？”

如果玩家旅程文档存在，则建议将此映射到旅程阶段。

---

#### B2 部分：导航位置

该屏幕位于游戏导航层次结构中的哪个位置？这是一张单段方向图，而不是完整的流程图。

**要问的问题**：
- “这个屏幕是从主菜单、暂停、游戏内还是另一个屏幕访问的？”
- “它是顶级目的地（始终可到达）还是依赖于上下文的目的地（仅在某些状态下可访问）？”
- “玩家可以从游戏中的多个位置到达此屏幕吗？”

显示为：“此屏幕位于：[root] → [parent] → [this screen]”以及任何备用入口路径。

---

#### B3 部分：入口和出口点

绘制玩家到达和离开此屏幕的所有方式。

**要问的问题**：
- “玩家可以通过哪些方式到达此屏幕？” （列出每个触发器：按钮按下、游戏事件、从另一个屏幕重定向等）
- “玩家可以做什么来退出？退出时会发生什么？” （后退按钮、确认操作、超时、游戏事件）
- “是否有任何单向出口——玩家无法在不重新开始的情况下返回此屏幕？”

呈现为两个表：

| 条目来源 | Trigger | 播放器携带此上下文 |
|---|---|---|
| [screen/event] | [how] | [state/data they arrive with] |

| 退出目的地 | Trigger | Notes |
|---|---|---|
| [screen/event] | [how] | [any irreversible state changes] |

---

#### C 部分：布局规范

这是最大且互动性最强的部分。分几个小节来完成它：

**第 1 小节 — 信息层次结构**（在任何布局之前建立此结构）：
- 要求用户列出该屏幕必须传达的每一条信息。
- 然后要求他们对这些项目进行排名：“对于玩家来说，最重要的事情是什么？
  需要先看吗？第二是什么？有什么是可以发现而不是立即可见的？”
- 在移动到区域之前呈现结果层次结构以供批准。

**第 2 小节 — 布局区域**：
- 根据信息层次结构，提出粗略的屏幕区域（标题、内容
  区域、操作栏、侧边栏等）。
- 提供 2-3 个区域安排以及每个区域的理由。参考平台和
  从游戏概念收集的输入上下文。
- 问：“这些是否符合您的心理形象，或者我们应该进行定制安排吗？”

**第 3 节 — 组件库存**：
- 对于每个区域，列出其包含的 UI 组件。对于每个组件，请注意：
  - 组件类型（按钮、列表、卡片、统计显示、输入字段等）
  - 显示的内容
  - 是否是互动的
  - 如果它使用库中的现有模式（按模式名称引用）
  - 如果它引入了新模式（稍后添加到库中的标志）

**第 4 节 — ASCII 线框**：
- 提供基于区域布局和组件列表生成 ASCII 线框。
- 使用 `AskUserQuestion`：“想要 ASCII 线框作为此规范的一部分吗？”
  - 选项：“是，包括一个”，“否，我将附加一个单独的文件”
- 如果是，请先在对话中制作线框图。之前询问反馈
  将其写入文件。

---

#### D 部分：状态和变体

引导用户超越快乐路径进行思考。

**要问的问题**（一次完成这些问题）：
- “当玩家第一次看到这个屏幕时，它看起来是什么样子？
  还没有数据吗？ （空状态）”
- “当出现问题时会发生什么——错误、失败的操作、缺失
  资源？ （错误状态）”
- “此屏幕上是否有加载等待？如果有，它会显示什么？（加载状态）”
- “是否有任何玩家进度状态会改变此屏幕显示的内容？对于
  例如，锁定内容、高级内容或教程模式叠加？”
- “此屏幕在任何受支持的平台上的行为是否有所不同？（平台变体）”

将收集的状态呈现为表格以供批准：

| 状态/变体 | Trigger | 有什么变化 |
|-----------------|---------|--------------|
| Default | 正常负载 | — |
| Empty | 无可用数据 | [content area description] |
| [etc.] | [trigger] | [changes] |

---

#### E 部分：交互图

对于布局规范中标识的每个交互组件，定义：
- 操作（点击、单击、按下、按住、滚动、拖动）
- 触发它的平台输入（鼠标单击、游戏手柄 A、键盘 Enter）
- 即时反馈（视觉、音频、触觉）
- 结果（导航目标、状态变化、数据写入）

使用阶段 2h 中从 `technical-preferences.md` 加载的输入法 — do
不再询问用户。预先说明：“映射交互：
[Input Methods from tech-prefs]。涵盖 [Gamepad Support] 游戏手柄支持。”

一次完成一个组件，而不是一次要求所有组件。
对于导航操作（转到另一个屏幕），验证目标匹配
现有的 UX 规范或将其记为规范依赖项。

---

#### E2 部分：触发的事件

对于交互地图中的每个玩家操作，记录游戏或分析系统应触发的相应事件，或者如果没有适用的情况，则明确注明“无事件”。

**要问的问题**：
- “对于每个动作，游戏是否应该触发分析事件、触发游戏状态更改，还是两者兼而有之？”
- “是否有任何行为不应该引发事件——这是一个故意的选择吗？”

以表格形式与交互图一起呈现：

| 玩家行动 | 事件触发 | 有效负载/数据 |
|---|---|---|
| [action] | [EventName] 或无 | [data passed with event] |

标记任何修改持久游戏状态的操作（保存数据、进度、经济）——这些需要架构团队的明确关注。

---

#### E3 部分：过渡和动画

指定屏幕如何进入和退出，以及如何响应状态变化。

**要问的问题**：
- “这个屏幕是如何出现的？（淡入、从右侧滑动、即时弹出、从按钮缩放）”
- “它如何消失？（淡出、滑回、剪切）”
- “是否有任何屏幕内状态转换需要动画？（加载微调器、成功状态、错误闪烁）”
- “是否有任何动画可能会导致晕动病 - 游戏是否有缩减动作选项？”

最低要求：
- 屏幕进入过渡
- 屏幕退出过渡
- 如果屏幕有多种状态，则至少有一个状态更改动画

---

#### F 部分：数据要求

交叉引用第 2 阶段收集的 GDD UI 要求部分。

对于屏幕显示的每条信息，询问：
- “这些数据从哪里来？哪个系统拥有它？”
- “这个屏幕需要写回数据吗，还是只读的？”
- “这些数据是否具有时间敏感性或实时性？（生命条、冷却计时器）”

标记 UI 需要作为架构拥有或管理游戏状态的任何情况
关心。 UX 规格定义了 UI 的需求；他们不规定数据如何
已交付。这是一个架构决策。

将数据要求以表格形式呈现：

| Data | 源系统 | Read / Write | Notes |
|------|--------------|--------------|-------|
| [item] | [system] | Read | — |
| [item] | [system] | Write | [concern if any] |

---

#### G 部分：无障碍

交叉引用 `design/accessibility-requirements.md`（如果存在）。

浏览此屏幕的用户体验设计师代理的标准清单：
- 通过所有交互元素的仅键盘导航路径
- 游戏手柄导航顺序（如果适用）
- 文本对比度和最小可读字体大小
- 与颜色无关的通信（仅通过颜色无法传达信息）
- 任何非文本元素的屏幕阅读器注意事项
- 任何需要缩减动作替代方案的动作或动画

使用 `AskUserQuestion` 来显示有关可访问性层的任何未解决的问题：
- “这个项目是否致力于无障碍层？”
  - 选项：“是的，阅读需求文档”，“还没有 - 让我们将其标记为问题”，“暂时跳过可访问性部分”

---

#### H 部分：本地化注意事项

翻译文本时影响此屏幕行为方式的文档约束。

**要问的问题**：
- “此屏幕上的哪些文本元素最长？适合该布局的最大字符数是多少？”
- “是否有任何元素的文本长度对布局至关重要 - 例如，按钮标签必须保留在一行上？”
- “是否有任何显示数字、日期或货币的元素需要特定于区域设置的格式？”

注意：旨在标记 40% 文本扩展（常见于从英语到德语或法语的翻译中）会破坏布局的任何元素。对于本地化工程师来说，将这些标记为“高优先级”。

---

#### 第一部分：验收标准

Write 至少 5 个特定的、可测试的标准，QA 测试人员无需阅读任何其他设计文档即可验证这些标准。这些成为 `/story-done` 的 pass/fail 条件。

**格式**：使用复选框。每个标准都必须可由人类测试人员验证：

```
- [ ] Screen opens within [X]ms from [trigger]
- [ ] [Element] displays correctly at [minimum] and [maximum] values
- [ ] [Navigation action] correctly routes to [destination screen]
- [ ] Error state appears when [condition] and shows [specific message or icon]
- [ ] Keyboard/gamepad navigation reaches all interactive elements in logical order
- [ ] [Accessibility requirement] is met — e.g., "all interactive elements have focus indicators"
```

**最低要求**：
- 1 性能标准（load/open次）
- 1 条导航标准（至少验证一条进入或退出路径）
- 1 error/empty 状态标准
- 1 个可访问性标准（每个承诺层）
- 1 个特定于此屏幕核心用途的标准

要求用户确认：“这些标准是否涵盖了为您的 QA 流程实际‘完成’此屏幕的内容？”

---

### 部分指南：HUD 设计模式

HUD 设计遵循与 UX 规格模式不同的顺序。从哲学开始；
在信息架构完成之前不要触及布局。

#### A 部分：HUD 理念

要求用户描述游戏与屏幕信息的关系
1-2 sentences.

提供框架示例以帮助：
- “几乎无 HUD — 氛围需要无障碍的沉浸感（例如，《空洞骑士》、《看火人》）”
- “最小但存在——只有关键信息可见，其他一切都是上下文相关的（例如，黑暗之魂）”
- “信息密集——所有与决策相关的数据始终可见（例如，暗黑破坏神 IV、星际争霸 II）”
- “自适应 - HUD 密度响应战斗状态、探索模式、菜单（例如，战神）”

这一理念成为每个后续 HUD 决策的设计约束。
如果提议的要素与既定的理念相冲突，请将冲突浮出水面。

---

#### B 部分：信息架构

在进行任何布局工作之前完成此操作。不要跳过它。

**第 1 步 — 完整信息清单**：
从第 2 阶段收集的 GDD UI 要求部分中提取所有信息。
展示完整列表：“这些都是您的游戏系统所说需要的东西
与屏幕上的玩家进行交流。”

**步骤 2 — 分类**：
对于每个项目，要求用户对其进行分类：

| Category | Description |
|----------|-------------|
| **必须显示** | 始终可见，玩家需要它来做出核心决策 |
| **Contextual** | 仅在相关时可见（在战斗中、接近可交互等） |
| **On Demand** | 玩家必须主动请求（切换、按住按钮） |
| **Hidden** | 通过 world/audio 进行通信，从不在屏幕上显示文本 |

使用 `AskUserQuestion` 以 3-4 为一组逐步执行项目，而不是一次执行所有项目。
这是 HUD 中最重要的设计决策 — 不要着急。

**冲突检查**：如果信息哲学（A 部分）说“几乎没有 HUD”
但必须展示的列表越来越长，明确地指出冲突：
> “当前必须显示列表中有 [N] 项目。这可能与 HUD 无冲突
> 哲学。选项：减少“必须展示”列表、修改理念或定义
> 一种混合方法，其中 HUD 在探索中不存在，但在战斗中出现。”

---

#### C 部分：布局区域

只有在信息架构获得批准后，才能设计布局区域。

基本布局：
- 哪些项目是必须展示的（它们驱动永久区域的决策）
- 玩家在游戏过程中注意力自然流向的地方（动作游戏的中心屏幕，
  策略游戏的角落）
- 平台和纵横比目标

提供 2-3 个区域安排。包括基于 HUD 理念的基本原理和
B 部分的分类。

---

#### D 部分：HUD 元素

对于布局中的每个元素，指定：
- 元素名称和类别（必须显示/上下文/按需）
- 显示内容
- 视觉形式（条形图、数字、图标、计数器、地图）
- 更新行为（实时、事件驱动、玩家查询）
- 上下文触发器（如果不总是可见）
- 动画行为（低电平时是否脉冲？淡入？猛烈进入？）

逐个元素地工作。如果有相关模式，请参考交互模式库
用于状态显示、资源栏或冷却指示器。

---

#### E、F、G 部分：动态行为、平台变体、可访问性

它们遵循与 UX 规范等效项相同的结构。请参阅 UX 规格部分
D (States/Variants)、E（交互）和 G（辅助功能）的指南。

特别针对 HUD，强调：
- 动态行为：是什么导致 HUD 在游戏过程中改变密度？
- 平台变体：mobile/console 是否需要不同的元件尺寸或位置？

---

### 部分指导：交互模式库模式

模式库创作是附加的、目录驱动的，而不是线性的。

#### 第一阶段：对现有模式进行分类

Glob `design/ux/*.md`（不包括`interaction-patterns.md`）并读取组件
每个规格的库存和交互图部分。提取每一个交互
使用的模式。

显示提取的列表：“根据现有的 UX 规范，这些模式已经
游戏中使用：”
- [Pattern name]：用于[screen]、[screen]
- [etc.]

问：“是否存在您知道存在但尚未出现在现有规范中的模式？列出任何模式
现在还有更多。”

---

#### 第 2 阶段：形式化每个模式

对于每个模式（现有的或新的），记录：

```markdown
### [Pattern Name]

**Category**: Navigation / Input / Feedback / Data Display / Modal / Overlay / [other]
**Used In**: [list of screens]

**Description**: [One paragraph explaining what this pattern is and when to use it]

**Specification**:
- [Component behavior]
- [Input mapping]
- [Visual/audio feedback]
- [Accessibility requirements for this pattern]

**When to Use**: [Conditions where this pattern is appropriate]
**When NOT to Use**: [Conditions where another pattern is more appropriate]

**Reference**: [Screenshot path or ASCII example, if available]
```

分组研究模式。提议：“我应该根据什么起草第一批？
我已经在现有的规范中找到了，还是你想一一定义？”

---

#### 第三阶段：找出差距

对已知模式进行编目后，询问：
- “是否有计划中的屏幕或交互还需要模式？
  在这个图书馆里？”
- “现有规范中是否存在与每个规范不一致的模式？
  其他的应该合并吗？”

在“差距”部分记录差距以供后续跟进。

---

## 5. 交叉引用检查

在将规范标记为可供审核之前，请运行以下检查：

**1. GDD 要求覆盖率**：是否每个 GDD UI 引用的要求
该屏幕在该规范中有相应的元素吗？提出任何差距。

**2.模式库对齐**：本规范中是否使用了所有交互模式
按名称引用？如果在此规范会议期间发明了新模式，请标记
将其添加到模式库中：
> “该规范使用 [pattern name]，但它尚未出现在模式库中。
> 想要立即添加它，还是将其标记为空白？”

**3.导航一致性**：本规范中的 entry/exit 点是否与
导航地图有相关规格吗？标志不匹配。

**4.可访问性覆盖**：规范是否涉及可访问性层
致力于`design/accessibility-requirements.md`？如果没有，请标记未解决的问题。

**5.空状态**：是否每个数据相关元素都定义了空状态？
标记任何不这样做的。

出示检查结果：
> **交叉引用检查：[Screen Name]**
> - GDD 要求：[N of M covered / all covered]
> - 添加到库的新模式：[列表或“无”]
> - 导航不匹配：[列表或“无”]
> - 可访问性差距：[列出或“无”]
> - 缺少空状态：[列表或“无”]

---

## 6. Handoff

当所有部分都获得批准并编写后：

### 6a：更新会话状态

将 `production/session-state/active.md` 更新为：
- Task：[screen-name] UX 规格
- 状态：已完成（或正在审核中）
- 文件：design/ux/[filename].md
- 部分：全部书面
- 下一篇：[suggestion]

### 6b：建议下一步

在提出选项之前，请明确说明：

> “该规范在进入之前应通过 `/ux-review` 进行验证
> 实施管道。预生产门需要所有关键屏幕规格
> 作出复核裁决。”

然后使用 `AskUserQuestion`：
- “现在运行 `/ux-review [filename]`，还是先做点别的事情？”
  - Options:
    - “立即运行 `/ux-review` — 验证此规范”
    - “首先设计另一个屏幕，然后一起审查所有规格”
    - “使用此规范中的新模式更新交互模式库”
    - “本次会议就停在这里”

如果用户选择“首先设计另一个屏幕”，请添加注释：“提醒：运行
在运行 `/gate-check pre-production` 之前，先了解所有已完成的规格上的 `/ux-review`。”

### 6c：交联相关规范

如果其他 UX 规格链接到此屏幕或从此屏幕链接，请注意应引用哪些规格
这个规格。不要在没有询问的情况下编辑这些文件——只需命名它们即可。

---

## 7. 恢复和继续

如果会话中断（压缩、崩溃、新会话）：

1. Read `production/session-state/active.md` — 记录当前屏幕
   以及哪些部分已完成。
2. Read `design/ux/[filename].md` — 具有真实内容的部分已完成；
   带有 `[To be designed]` 的部分仍然需要工作。
3. 从下一个未完成的部分继续——无需重新讨论已完成的部分。

这就是为什么增量写作很重要：每个批准的部分都可以在任何情况下幸存下来
disruption.

---

## 8. 专业代理路由

该技能使用`ux-designer`作为主要代理（在frontmatter中设置）。对于
可能需要具体的子主题、额外的背景或协调：

| Topic | 与 协调 |
|-------|----------------|
| 视觉美感、色彩、布局感觉 | `art-director` — UX 规范定义区域；艺术定义了他们的外表 |
| 实施可行性（引擎限制） | `ui-programmer` — 在最终确定组件库存之前 |
| 游戏数据要求 | `game-designer` — 当数据所有权不清楚时 |
| Narrative/lore 在 UI 中可见 | `narrative-director` — 用于风味文本、物品名称、知识面板 |
| 无障碍层决策 | 由本次会议处理 — 由 ux-designer 所有 |

通过 Task 工具委托给另一个代理时：
- 提供：屏幕名称、游戏概念概要、需要专家输入的具体问题
- 代理将分析结果返回到此会话
- 此会话向用户呈现代理的输出
- 用户决定；该会话写入文件
- 代理不直接写入文件 - 此会话拥有所有文件写入

---

## 协作协议

该技能的每一步都遵循协作设计原则：

1. **问题 -> 选项 -> 决定 -> 草案 -> 批准** 每个部分
2. **AskUserQuestion** 在每个决策点（解释 -> 捕获模式）：
   - 第 2 阶段：“准备好开始，还是需要更多背景信息？”
   - 第三阶段：“我可以创建骨架吗？”
   - 第 4 阶段（每个部分）：设计问题、方法选项、草案批准
   - 阶段 5：“运行交叉引用检查？接下来做什么？”
3. **“我可以写信给 [filepath] 吗？”** 在骨架之前和每个部分写之前
4. **增量写入**：每个部分在批准后立即写入归档
5. **会话状态更新**：在每个部分写入之后

**审美尊重**：当布局或视觉选择取决于个人品味时，
提出选项并询问。不要选择布局，因为它是“标准”的 - 始终
确认。用户是创意总监。

**冲突表面**：当 GDD 要求和可用屏幕空间时
冲突，揭示冲突并提出解决方案。绝不默默滴
一个要求。切勿在没有标记的情况下默默地扩展布局。

**永远不要**自动生成完整的规范并将其呈现为既成事实。
**切勿**在未经用户批准的情况下编写部分。
**绝不**与现有已批准的 UX 规范相矛盾而不标记冲突。
**始终**显示决策的来源（GDD 要求、玩家旅程、用户选择）。

结论：**完成** — UX 规范逐节编写和批准。

---

## 建议的后续步骤

- 在进入实施管道之前运行 `/ux-review [filename]` 以验证此规范
- 运行 `/ux-design [next-screen]` 以继续设计剩余的屏幕或流程
- 所有关键屏幕均已批准 UX 规格后，运行 `/gate-check pre-production`
