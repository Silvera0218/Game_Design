---
name: design-system
description: "针对单个游戏系统进行引导式逐节 GDD 创作。从现有文档中收集上下文，协作浏览每个所需部分，交叉引用依赖项，并增量写入文件。"
---

当该技能被调用时：

## 1. 解析参数并验证

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

系统名称或改造路径是**必需的**。如果丢失：

1. 检查`design/gdd/systems-index.md`是否存在。
2. 如果存在：读取它，找到状态为“未启动”或同等状态的最高优先级系统，然后使用 `AskUserQuestion`：
   - 提示：“您的设计订单中的下一个系统是 **[system-name]** ([priority] | [layer])。开始设计它吗？”
   - 选项：`[A] Yes — design [system-name]` / `[B] Pick a different system` / `[C] Stop here`
   - 如果 [A]：继续使用该系统名称。如[B]：询问设计哪个系统（纯文本）。如果[C]：退出。
3. 如果不存在系统索引，则失败并显示：
   > “用法：`/design-system <system-name>` — 例如，`/design-system movement`
   > 或者填补现有 GDD 中的空白：`/design-system retrofit design/gdd/[system-name].md`
   > 未找到系统索引。首先运行 `/map-systems` 来映射您的系统并获取设计订单。”

**检测改装模式：**
如果参数以 `retrofit` 开头或者参数是某个文件的文件路径
`design/gdd/`中已有`.md`文件，进入**改造模式**：

1. Read 现有的 GDD 文件。
2. 确定存在 8 个必需部分中的哪些（扫描部分标题）。
   所需部分：概述、玩家幻想、详细 Design/Rules、公式、
   边缘情况、依赖性、调节旋钮、验收标准。
3. 确定哪些部分仅包含占位符文本（`[To be designed]` 或
   等效项 — 空白、单行或明显不完整）。
4. 在执行任何操作之前向用户展示：
   ```
   ## Retrofit: [System Name]
   File: design/gdd/[filename].md

   Sections already written (will not be touched):
   ✓ [section name]
   ✓ [section name]

   Missing or incomplete sections (will be authored):
   ✗ [section name] — missing
   ✗ [section name] — placeholder only
   ```
5. 问：“我要填补 [N] 缺失的部分吗？我不会修改任何现有内容。”
6. 如果是：照常进行**阶段 2（收集上下文）**，但进入 **阶段 3**
   跳过创建骨架（文件已存在）并在**阶段 4** 跳过
   已经完成的部分。仅运行缺少/的部分循环
   不完整的部分。
7. **永远不要覆盖现有的部分内容。**使用 Edit 工具仅替换
   `[To be designed]` 占位符或空部分主体。

如果不在改造模式下，请将系统名称规范为 kebab-case
文件名（例如，“战斗系统”变为 `combat-system`）。

---

## 2. 收集上下文（Read 阶段）

Read 在向用户询问任何内容之前**所有相关上下文。这是技能的
相对于临时设计的主要优势是消息灵通。

### 2a：必读内容

- **游戏概念**：Read `design/gdd/game-concept.md` — 如果缺失则失败：
  > “未找到游戏概念。请先运行 `/brainstorm`。”
- **系统索引**：Read `design/gdd/systems-index.md` — 如果丢失则失败：
  > “未找到系统索引。首先运行 `/map-systems` 来映射您的系统。”
- **目标系统**：在索引中查找系统。如果未列出，请警告：
  > “[system-name] 不在系统索引中。您要添加它，还是
  > 将其设计为非索引系统？”
- **实体注册表**：Read `design/registry/entities.yaml`（如果存在）。
  提取该系统引用或相关的所有条目（grep
  `referenced_by.*[system-name]` 和 `source.*[system-name]`）。拿着这些
  在上下文中作为**已知事实** - 其他 GDD 已经拥有的值
  已成立且此 GDD 不得矛盾。
- **反射日志**：Read `docs/consistency-failures.md`（如果存在）。
  提取其域与该系统类别匹配的条目。这些是
  反复出现的冲突模式——将它们呈现在“过去的失败模式”下
  在第 2d 阶段上下文摘要中，以便用户知道错误在哪里
  在此域之前发生过。

### 2b：依赖性读取

从系统索引中识别：
- **上游依赖项**：此系统所依赖的系统。 Read 他们的 GDD，如果他们
  存在（这些包含该系统必须尊重的决策）。
- **下游依赖项**：依赖于此的系统。 Read 他们的 GDD 如果
  它们存在（这些包含系统必须满足的期望）。

对于存在的每个依赖项 GDD，提取并保存在上下文中：
- 关键接口（系统之间的数据流动）
- 引用该系统输出的公式
- 假设该系统行为的边缘情况
- 馈入该系统的调节旋钮

### 2c：可选阅读

- **游戏支柱**：Read `design/gdd/game-pillars.md`（如果存在）
- **现有GDD**：Read `design/gdd/[system-name].md`如果存在（恢复，不要
  从头开始）
- **相关 GDD**：Glob `design/gdd/*.md` 并阅读任何主题相关的内容
  （例如，如果设计一个与另一个范围重叠的系统，请阅读相关的 GDD
  即使它不是正式的依赖项）

### 2d：当前背景摘要

在开始设计工作之前，向用户提供一个简短的总结：

> **设计：[System Name]**
> - 优先级：[from index] |图层：[from index]
> - 取决于：[列表，注意哪些具有 GDD 与哪些未设计]
> - 取决于：[列表，注意哪些具有 GDD 与哪些未设计]
> - 需要尊重的现有决定：[key constraints from dependency GDDs]
> - 支柱对齐：[该系统主要服务于哪个支柱]
> - **已知的跨系统事实（来自注册表）：**
> - [entity_name]：[attribute]=[value]，[attribute]=[value]（归[source GDD]所有）
>   - [item_name]：[attribute]=[value]，[attribute]=[value]（归[source GDD]所有）
>   - [formula_name]：变量=[list]，输出=[最小–最大]（由[source GDD]拥有）
>   - [constant_name]：[value] [unit]（归[source GDD]所有）
>   *（这些值已锁定 - 如果此 GDD 需要不同的值，表面
>   写之前的冲突。不要默默地使用不同的号码。）*
>
> 如果没有相关的注册表项：省略“已知的跨系统事实”部分。

如果任何上游依赖项未设计，则发出警告：
> “[dependency] 还没有 GDD。我们需要做出以下假设：
> 它的界面。首先考虑设计它，或者我们可以定义预期的
> 签订合同并将其标记为临时的。”

### 2e：技术可行性预检查

在要求用户开始设计之前，加载引擎上下文并显示任何内容
影响设计的约束或知识差距。

**步骤 1 — 确定该系统的引擎域：**
将系统的类别（来自 systems-index.md）映射到引擎域：

| 系统类别 | 引擎域 |
|----------------|--------------|
| 战斗、物理、碰撞 | Physics |
| 渲染、视觉效果、着色器 | Rendering |
| UI、HUD、菜单 | UI |
| 音频、声音、音乐 | Audio |
| 人工智能、寻路、行为树 | 导航/脚本 |
| 动画、IK、绑定 | Animation |
| 网络、多人、同步 | Networking |
| 输入、控件、键绑定 | Input |
| Save/load，持久性，数据 | Core |
| 对话、任务、叙事 | Scripting |

**步骤 2 — Read 引擎上下文（如果可用）：**
- Read `.codex/docs/technical-preferences.md` 识别引擎和版本
- 如果配置了引擎，请阅读 `docs/engine-reference/[engine]/VERSION.md`
- Read `docs/engine-reference/[engine]/modules/[domain].md` 如果存在
- Read `docs/engine-reference/[engine]/breaking-changes.md` 用于域相关条目
- Glob `docs/architecture/adr-*.md` 并读取域匹配的任何 ADR
  （检查引擎兼容性表的“域”字段）

**第 3 步 — 提交可行性简介：**

如果存在引擎参考文档，请在开始设计之前提供：

```
## Technical Feasibility Brief: [System Name]
Engine: [name + version]
Domain: [domain]

### Known Engine Capabilities (verified for [version])
- [capability relevant to this system]
- [capability 2]

### Engine Constraints That Will Shape This Design
- [constraint from engine-reference or existing ADR]

### Knowledge Gaps (verify before committing to these)
- [post-cutoff feature this design might rely on — mark HIGH/MEDIUM risk]

### Existing ADRs That Constrain This System
- ADR-XXXX: [decision summary] — means [implication for this GDD]
  (or "None yet")
```

如果不存在引擎参考文档（引擎尚未配置），则显示简短的注释：
> “尚未配置引擎 - 跳过技术可行性检查。运行
> 如果您还没有转向架构，请先阅读 `/setup-engine`。”

**第 4 步 — 继续前询问：**

使用 `AskUserQuestion`：
- “在我们开始之前需要添加任何限制，还是我们应该按照这些记录继续进行？”
  - 选项：“继续处理这些注释”、“首先添加约束”、“我需要检查引擎文档 - 在此暂停”

---

使用 `AskUserQuestion`：
- “准备好开始设计 [system-name] 了吗？”
  - 选项：“是的，我们开始吧”、“首先向我展示更多上下文”、“首先设计依赖项”

---

## 3. 创建文件骨架

一旦用户确认，**立即**创建带有空部分的 GDD 文件
标头。这确保增量写入有目标。

使用 `.codex/docs/templates/game-design-document.md` 中的模板结构：

```markdown
# [System Name]

> **Status**: In Design
> **Author**: [user + agents]
> **Last Updated**: [today's date]
> **Implements Pillar**: [from context]

## Overview

[To be designed]

## Player Fantasy

[To be designed]

## Detailed Design

### Core Rules

[To be designed]

### States and Transitions

[To be designed]

### Interactions with Other Systems

[To be designed]

## Formulas

[To be designed]

## Edge Cases

[To be designed]

## Dependencies

[To be designed]

## Tuning Knobs

[To be designed]

## Visual/Audio Requirements

[To be designed]

## UI Requirements

[To be designed]

## Acceptance Criteria

[To be designed]

## Open Questions

[To be designed]
```

问：“我可以在 `design/gdd/[system-name].md` 创建骨架文件吗？”

写入后，更新`production/session-state/active.md`：
- 使用 Glob 检查文件是否存在。
- 如果它**不存在**：使用**Write**工具创建它。切勿在可能不存在的文件上尝试 Edit。
- 如果**已经存在**：使用**Edit**工具更新相关字段。

文件内容：
- Task：设计 [system-name] GDD
- 当前部分：开始（已创建骨架）
- 文件：design/gdd/[system-name].md

---

## 4. 分段设计

按顺序浏览每个部分。对于**每个部分**，请遵循以下循环：

### 节循环

```
Context  ->  Questions  ->  Options  ->  Decision  ->  Draft  ->  Approval  ->  Write
```

1. **上下文**：说明本节需要包含的内容，并显示任何相关内容
   来自约束它的依赖 GDD 的决策。

2. **问题**：提出针对本节的澄清问题。使用
   `AskUserQuestion` 用于受限问题，用于开放式对话文本
   exploration.

3. **选项**：该部分涉及设计选择（不仅仅是文档），
   使用 pros/cons. 呈现 2-4 种方法 解释对话文本中的推理，
   然后使用 `AskUserQuestion` 捕获决策。

4. **决策**：用户选择一种方法或提供自定义方向。

5. **草稿**：Write 对话文本中的部分内容供审阅。标记任何
   关于未设计的依赖关系的临时假设。

6. **批准**：草稿后立即 - 在同一响应中 - 使用
   `AskUserQuestion`。 **切勿使用纯文本。切勿跳过此步骤。**
   - 提示：“批准 [Section Name] 部分吗？”
   - 选项：`[A] Approve — write it to file` / `[B] Make changes — describe what to fix` / `[C] Start over`

   **草稿和批准小部件必须一起出现在一个响应中。
   如果草稿在没有小部件的情况下出现，用户将看到空白提示
   没有前进的道路——这是违反协议的行为。**

7. **Write**：使用Edit工具将占位符替换为批准的内容。
   **关键**：始终在 `old_string` 中包含该部分标题，以确保
   唯一性 - 永远不要单独匹配 `[To be designed]`，因为多个部分使用
   相同的占位符和 Edit 工具需要唯一的匹配。使用这个模式：
   ```
   old_string: "## [Section Name]\n\n[To be designed]"
   new_string: "## [Section Name]\n\n[approved content]"
   ```
   确认写入。

8. **注册表冲突检查**（仅限 C 和 D 部分 - 详细设计和公式）：
   写入后，扫描该部分内容以查找实体名称、项目名称、公式
出现在注册表中的名称和数字常量。对于每场比赛：
   - 将刚刚写入的值与注册表项进行比较。
   - 如果它们不同：**在开始下一个冲突之前立即提出冲突**
     部分。不要继续沉默。
     > “注册表冲突：[name] 在 [source GDD] 中注册为 [registry_value]。
     > 本节刚刚写了[new_value]。哪个是正确的？”
   - 如果是新的（不在注册表中）：将其标记为注册表注册的候选者
     （将在第五阶段处理）。

编写每个部分后，用以下内容更新 `production/session-state/active.md`
完成的部分名称。使用 Glob 检查文件是否存在 — 使用 Write 创建
如果不存在，则 Edit 更新它（如果存在）。

### 特定部分的指导

每个部分都有独特的设计考虑，并可能受益于专业代理：

---

### A 部分：概述

**目标**：陌生人可以阅读和理解的一段。

**在构建小部件之前推导推荐选项**：Read 来自系统索引的系统类别和层（已在第 2 阶段的上下文中），然后确定每个选项卡的推荐选项：
- **“框架”选项卡**：Foundation/Infrastructure 层 → 建议使用 `[A]`。面向玩家的类别（战斗、UI、对话、角色、动画、视觉效果、音频）→推荐 `[C] Both`。
- **ADR 参考选项卡**：Glob `docs/architecture/adr-*.md` 和 grep 查找任何 ADR 的 GDD 要求部分中的系统名称。如果找到匹配的 ADR → 建议使用 `[A] Yes — cite the ADR`。如果没有找到 → 建议 `[B] No`。
- **幻想选项卡**：Foundation/Infrastructure 层 → 推荐 `[B] No`。所有其他类别 → 推荐 `[A] Yes`。

将 `(Recommended)` 附加到每个选项卡中相应的选项文本。

**框架问题（起草前询问）**：将 `AskUserQuestion` 与多选项卡小部件一起使用：
- “框架”选项卡 —“概述应如何构建该系统？”选项：`[A] As a data/infrastructure layer (technical framing)` / `[B] Through its player-facing effect (design framing)` / `[C] Both — describe the data layer and its player impact`
- 选项卡“ADR ref”—“概述是否应该引用此系统的现有 ADR？”选项：`[A] Yes — cite the ADR for implementation details` / `[B] No — keep the GDD at pure design level`
- 选项卡“幻想”——“这个系统有值得一说的玩家幻想吗？”选项：`[A] Yes — players feel it directly` / `[B] No — pure infrastructure, players feel what it enables`

使用用户的答案来制定草稿。不要自己回答这些问题和自动起草。

**要问的问题**：
- 用一句话来形容这个系统是什么？
- 玩家如何与其互动？ （active/passive/automatic）
- 为什么这个系统存在——如果没有它，游戏会失去什么？

**交叉引用**：检查描述是否与系统索引的方式一致
描述它。标志差异。

**设计与实现边界**：概述问题必须停留在行为上
级别——系统*做什么*，而不是*它是如何构建的*。如果实施有问题
在概述期间出现（例如，“这应该使用自动加载单例还是信号
总线？”），将它们标记为“→ 成为 ADR”并继续。实现模式属于
在 `/architecture-decision` 中，而不是 GDD 中。 GDD 描述了行为； ADR
描述了用于实现它的技术方法。

---

### B 部分：玩家幻想

**目标**：情感目标——玩家应该“感受”什么。

**在构建小部件之前导出推荐选项**：Read 来自第 2 阶段上下文的系统类别和层：
- 面向玩家的类别（战斗、UI、对话、角色、动画、音频、Level/World）→推荐`[A] Direct`
- Foundation/Infrastructure 层 → `[B] Indirect` 推荐
- 混合类别（Camera/input、经济、具有可见玩家效果的 AI）→ 推荐 `[C] Both`

将 `(Recommended)` 附加到适当的选项文本。

**框架问题（起草前询问）**：使用 `AskUserQuestion`：
- 提示：“这个系统是玩家直接接触的系统，还是他们间接体验的基础设施？”
- 选项：`[A] Direct — player actively uses or feels this system` / `[B] Indirect — player experiences the effects, not the system` / `[C] Both — has a direct interaction layer and infrastructure beneath it`

使用答案来适当地构建玩家幻想部分。不要假设答案。

**要问的问题**：
- 这服务于什么情感或权力幻想？
- 有哪些参考游戏可以体现这种感觉？具体是什么创造了它？
- 这是一个“你喜欢参与的系统”还是“你没有注意到的基础设施”？

**交叉参考**：必须与游戏支柱保持一致。如果系统服务于一个支柱，
引用相关的支柱文本。

**代理委托（强制）**：在给出框架答案之后但在起草之前，
通过 Task 生成 `creative-director`：
- 提供：系统名称、框架答案（direct/indirect/both）、游戏支柱、用户提到的任何参考游戏、游戏概念摘要
- 问：“为这个系统塑造玩家幻想。它应该服务于什么样的情感或权力幻想？我们应该锚定玩家的哪个时刻？什么基调和语言适合游戏既定的感觉？具体一点——给我 2-3 个候选框架。”
- 收集创意总监的框架并将其与草稿一起呈现给用户。

**在未先咨询 `creative-director` 的情况下，请勿起草 B 部分。** 框架
答案告诉我们这是什么类型的幻想；创意总监塑造*它是如何的
描述*——语气、语言、要锚定的特定玩家时刻。

---

### C 部分：详细设计（核心规则、状态、交互）

**目标**：程序员可以毫无疑问地实现的明确规范。

这通常是最大的部分。将其分为几个小节：

1. **核心规则**：基本机制。使用编号规则进行顺序
   流程、属性项目符号。
2. **状态和转换**：如果系统有状态，则映射每个状态和
   每个有效的转换。使用桌子。
3. **与其他系统的交互**：对于每个依赖项（上游和下游），
   指定什么数据流入、什么流出以及谁拥有该接口。

**要问的问题**：
- 逐步引导我完成该系统的典型使用
- 玩家面临的决策点是什么？
- 玩家不能做什么？ （限制与能力同样重要）

**代理委托（强制）**：在起草 C 部分之前，通过 Task 并行生成专家代理：
- 在路由表中查找系统类别（本技能第6节）
- 产生为此类别列出的主要代理和支持代理
- 提供每个代理：系统名称、游戏概念摘要、支柱集、依赖项 GDD 摘录、正在处理的具体部分
- 在起草之前收集他们的发现
- 通过 `AskUserQuestion` 向用户表明代理之间的任何分歧
- 仅在收到专家意见后草稿

**在未先咨询相应专家的情况下，请勿起草 C 部分。** `systems-designer` 审查规则和机制将发现主会议无法发现的设计差距。

**交叉引用**：对于列出的每个交互，验证其与
依赖项 GDD 指定。如果依赖项定义了一个值或公式并且这
系统期望有不同的东西，标记冲突。

---

### D 部分：公式

**目标**：每个数学公式，定义变量，指定范围，
并指出了边缘情况。

**完成指导 - 始终以以下精确结构开始每个公式：**

```
The [formula_name] formula is defined as:

`[formula_name] = [expression]`

**Variables:**
| Variable | Symbol | Type | Range | Description |
|----------|--------|------|-------|-------------|
| [name] | [sym] | float/int | [min–max] | [what it represents] |

**Output Range:** [min] to [max] under normal play; [behaviour at extremes]
**Example:** [worked example with real numbers]
```

不要写 `[Formula TBD]` 或在没有变量的情况下用散文描述公式
表。没有定义变量的公式无法在没有猜测的情况下实现。

**要问的问题**：
- 该系统执行哪些核心计算？
- 缩放应该是线性的、对数的还是阶梯式的？
- early/mid/late 游戏的输出范围应该是多少？

**代理委托（强制）**：在提出任何公式或余额值之前，通过 Task 并行生成专家代理：
- **始终生成 `systems-designer`**：提供 C 部分的核心规则、用户的调整目标、平衡依赖 GDD 的上下文。要求他们提出带有变量表和输出范围的公式。
- **对于 economy/cost 系统，还会生成 `economy-designer`**：提供放置成本、升级成本意图和进度目标。要求他们验证成本曲线和比率。
- 通过 `AskUserQuestion` 将专家的建议提交给用户审核
- 用户决定；主会话写入文件
- **未经专家输入，请勿发明公式值或天平数字。** 没有天平设计专业知识的用户无法评估原始数字 - 他们需要专家的推理。

**交叉引用**：如果依赖项 GDD 定义了一个公式，其输出输入到
这个系统，明确引用它。不要重新发明——连接。

---

### E 部分：边缘情况

**目标**：明确处理异常情况，这样它们就不会成为错误。

**完成指导 - 将每个边缘情况格式化为：**
- **如果 [condition]**：[exact outcome]。 [rationale if non-obvious]

示例（根据游戏领域调整术语）：
- **如果 [protective condition] 处于活动状态时 [resource] 达到 0**：保持最小值直到条件结束，然后应用结果。
- **如果两个 [triggers/events] 同时触发**：在 [defined priority order] 中解析；关系使用 [defined tiebreak rule]。

不要写出诸如“适当处理”之类的模糊条目——每个条目必须准确命名
条件和准确的分辨率。没有解决方案的边缘情况是开放的
设计问题，而不是规范。

**要问的问题**：
- 为零时会发生什么？最多？值超出范围？
- 当两个规则同时适用时会发生什么？
- 如果玩家发现意外的互动，会发生什么？ （识别退化策略）

**代理委托（强制）**：在最终确定边缘情况之前通过 Task 生成 `systems-designer`。提供：完成的 C 部分和 D 部分，并要求他们从主会议可能错过的公式和规则空间中识别边缘情况。对于叙事系统，还会生成 `narrative-director`。展示他们的发现并询问用户要包含哪些内容。

**交叉引用**：根据依赖性 GDD 检查边缘情况。如果有依赖关系
定义该系统可能违反的下限、上限或解决规则，对其进行标记。

---

### F 部分：依赖关系

**目标**：绘制每个系统连接的方向和性质。

本节部分是在上下文收集阶段预先填充的。呈现
从系统索引已知的依赖关系并询问：
- 我缺少依赖项吗？
- 对于每个依赖项，具体的数据接口是什么？
- 哪些依赖项是硬依赖项（没有它系统就无法运行）与软依赖项
  （由它增强但没有它也能工作）？

**交叉引用**：此部分必须双向一致。如果这个系统
列出“取决于 Combat”，那么 Combat GDD 应列出“取决于 [this
系统]”。标记任何单向依赖性以进行更正。

---

### G 部分：调音旋钮

**目标**：每个设计师可调节的值，具有安全范围和极端行为。

**要问的问题**：
- 设计者应该能够在不更改代码的情况下调整哪些值？
- 对于每个旋钮，如果设置得太高会损坏什么？太低了？
- 哪些旋钮相互作用？ （改变 A 会使 B 变得不相关）

**代理委托**：如果公式复杂，委托给`systems-designer`
从公式变量导出调谐旋钮。

**交叉引用**：如果依赖项 GDD 列出了影响该系统的调谐旋钮，
在这里参考它们。不要创建重复的旋钮——指出事实的来源。

---

### H 部分：验收标准

**目标**：证明系统按设计工作的可测试条件。

**完成指导 - 将每个标准格式化为“Given-When-Then”：**
- **给定** [initial state]，**何时** [action or trigger]，**那么** [measurable outcome]

示例（根据游戏领域调整术语）：
- **给出** [initial state]，**何时** [player action or system trigger]，**那么** [specific measurable outcome]。
- **给出** [a constraint is active]，**何时** [player attempts an action]，**那么** [feedback shown and action result]。

至少包括：C 部分中的每条核心规则一项标准，以及每个公式一项
来自 D 部分。不要写“系统按设计运行”——每个标准都必须
可由 QA 测试仪独立验证，无需读取 GDD。

**代理委托（强制）**：在最终确定验收标准之前，通过 Task 生成 `qa-lead`。提供：完成的 GDD C、D、E 部分，并要求他们验证标准是否可独立测试并涵盖所有核心规则和公式。向用户展示任何差距或无法测试的标准。

**要问的问题**：
- 证明此方法有效的最少测试集是什么？
- 该系统可以获得多少性能预算？ （帧时间、内存）
- QA 测试仪首先会检查什么？

**交叉引用**：包括验证跨系统交互工作的标准，
不仅仅是这个孤立的系统。

---

### 可选部分：Visual/Audio、UI 要求、开放问题

这些部分包含在模板中。 Visual/Audio 对于视觉系统类别来说是**必需** — 不是可选的。在询问之前确定要求级别：

**对于这些系统类别，Visual/Audio 是必需的（强制 — 请勿跳过）：**
- 战斗、伤害、健康
- UI 系统（HUD，菜单）
- 动画、角色动作
- 视觉效果、粒子、着色器
- 角色系统
- 对话、任务、传说
- Level/world 系统

对于所需的系统：**在起草本节之前通过 Task 生成 `art-director`**。提供：系统名称、游戏概念、游戏支柱、艺术圣经第 1-4 部分（如果存在）。要求他们指定：(1) VFX 和该系统事件的视觉反馈要求，(2) 任何动画或视觉风格限制，(3) 哪些艺术圣经原则最直接适用于该系统。展示他们的成果；对于视觉系统，请勿将此部分保留为 `[To be designed]`。

对于**所有其他系统类别**（Foundation/Infrastructure、经济型、AI/pathfinding、Camera/input），请在必填部分后提供可选部分：

使用 `AskUserQuestion`：
- “8 个必需的部分已完成。您是否还想定义 Visual/Audio
  要求、UI 要求或捕获未决问题？”
  - 选项：“是的，全部三个”，“只需提出问题”，“跳过 - 我稍后会添加这些”

对于 **Visual/Audio**（非必需系统）：如果需要详细信息，请与 `art-director` 和 `audio-director` 协调。通常，在 GDD 阶段，一条简短的注释就足够了。

> **资产规格标志**：在Visual/Audio部分写入真实内容后，输出此通知：
> “📌 **资产规格** — 定义了 Visual/Audio 要求。艺术圣经获得批准后，运行 `/asset-spec system:[system-name]` 以生成本部分中的每个资产的视觉描述、尺寸和生成提示。”

对于 **UI 要求**：与 `ux-designer` 协调以实现复杂的 UI 系统。
写完这一部分后，检查它是否包含真实内容（而不仅仅是
`[To be designed]` 或注释该系统没有 UI）。如果真的有
UI要求，立即输出该标志：

> **📌 UX 标志 — [System Name]**：此系统具有 UI 要求。第四阶段
> （预生产），运行 `/ux-design` 为每个屏幕创建 UX 规范或
> HUD 该系统在**编写史诗之前**贡献的元素。故事
> 引用 UI 应引用 `design/ux/[screen].md`，而不是直接引用 GDD。
>
> 如果您更新该系统，请在该系统的系统索引中注意这一点。

对于**开放性问题**：捕获设计过程中出现的任何未出现的问题
完全解决。每个问题都应该有一个所有者和目标解决日期。

---

## 5. 设计后验证

写完所有部分后：

### 5a：自检

Read 从文件返回完整的 GDD（不是从对话内存 — 该文件是
真理的来源）。验证：
- 所有 8 个必填部分都有真实内容（不是占位符）
- 公式引用定义的变量
- 边缘情况有解决方案
- 依赖项与接口一起列出
- 验收标准是可测试的

### 5a-bis：创意总监支柱回顾

**查看模式检查** — 在生成 CD-GDD-ALIGN 之前应用：
- `solo` → 跳过。注意：“已跳过 CD-GDD-ALIGN — 单人模式。”继续步骤 5b。
- `lean` → 跳过（不是相位门）。注意：“已跳过 CD-GDD-ALIGN — 精益模式。”继续步骤 5b。
- `full` → 正常生成。

在最终确定 GDD 之前，使用门 **CD-GDD-ALIGN** (`.codex/docs/director-gates.md`) 通过 Task 生成 `creative-director`。

通行证：完成的GDD文件路径、游戏支柱（来自`design/gdd/game-concept.md`或`design/gdd/game-pillars.md`）、MDA美学目标。

根据 `director-gates.md` 中的标准规则处理判决。解决后，将结论记录在 GDD Status 标头中：
`> **Creative Director Review (CD-GDD-ALIGN)**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]`

---

### 5b：更新实体注册表

扫描完整的 GDD 以获取应注册的跨系统事实：
- 具有统计数据或掉落的命名实体（敌人、NPC、头目）
- 具有值、权重或类别的命名项目
- 具有定义变量和输出范围的命名公式
- 在多个地方按值引用的命名常量

对于每个候选者，检查它是否已存在于 `design/registry/entities.yaml` 中：
```
Grep pattern="  - name: [candidate_name]" path="design/registry/entities.yaml"
```

提出一个总结：
```
Registry candidates from this GDD:
  NEW (not yet registered):
    - [entity_name] [entity]: [attribute]=[value], [attribute]=[value]
    - [item_name] [item]: [attribute]=[value], [attribute]=[value]
    - [formula_name] [formula]: variables=[list], output=[min–max]
  ALREADY REGISTERED (referenced_by will be updated):
    - [constant_name] [constant]: value=[N] ← matches registry ✅
```

询问：“我可以用这些 [N] 新条目更新 `design/registry/entities.yaml`
并更新现有条目的 `referenced_by`？”

如果是：追加新条目并更新 `referenced_by` 数组。绝不修改
现有的 `value` / 属性字段，而不首先将其作为冲突显示出来。

### 5c：提供设计审核

呈现完成摘要：

> **GDD 完整：[System Name]**
> - 写入的部分：[list]
> - 临时假设：[list any assumptions about undesigned dependencies]
> - 发现跨系统冲突：[列表或“无”]

> **要验证此 GDD，请打开一个新的 Codex 会话并运行：**
> `/design-review design/gdd/[system-name].md`
>
> **切勿在与 `/design-system` 相同的会话中运行 `/design-review`。**
> 代理必须独立于创作上下文。在这里运行它会继承
> 完整的设计历史，使得独立批评变得不可能。

**切勿提供内联运行 `/design-review`。** 始终将用户引导至新窗口。

### 5d：更新系统索引

GDD 完成后（并可选择进行审核）：

- Read 系统索引
- 更新目标系统的行：
  - 如果设计评审已运行且结论已批准：状态→“已批准”
  - 如果运行了设计审查并且结论是需要修订：状态→“审查中”
  - 如果跳过设计审核：状态→“已设计”（待审核）
  - 如果用户选择“我先自己审阅”：状态→“已设计”
  - 设计文档：链接至 `design/gdd/[system-name].md`
- 更新进度跟踪器计数

问：“我可以更新 `design/gdd/systems-index.md` 处的系统索引吗？”

### 5d：更新会话状态

将 `production/session-state/active.md` 更新为：
- Task: [system-name] GDD
- 状态：已完成（如果运行了设计审核，则处于审核中）
- 文件：design/gdd/[system-name].md
- 部分：全部 8 个书面部分
- 下一篇：[suggest next system from design order]

### 5e：建议后续步骤

使用 `AskUserQuestion`：
- “接下来怎么办？”
  - Options:
    - “运行 `/consistency-check` — 验证此 GDD 的值不会与现有 GDD 冲突（建议在设计下一个系统之前使用）”
    - “设计下一个系统 ([next-in-order])” — 如果仍有未设计的系统
    - “修复审查结果”——如果设计审查标记了问题
    - “本次会议就停在这里”
    - “运行 `/gate-check`” — 如果设计了足够多的 MVP 系统

---

## 6. 专业代理路由

该技能委托给专业代理以获取领域专业知识。主要会议
协调整体流程；代理提供专家内容。

| 系统类别 | 主要代理 | 支持代理 |
|----------------|---------------|---------------------|
| **Foundation/Infrastructure**（事件总线、save/load、场景管理、服务定位器） | `systems-designer` | `gameplay-programmer`（可行性）、`engine-programmer`（引擎集成） |
| 战斗、伤害、健康 | `game-designer` | `systems-designer`（公式）、`ai-programmer`（敌方AI）、`art-director`（命中反馈视觉方向、VFX意图） |
| 经济、战利品、制作 | `economy-designer` | `systems-designer`（曲线）、`game-designer`（循环） |
| 进度、XP、技能 | `game-designer` | `systems-designer`（曲线）、`economy-designer`（水槽） |
| 对话、任务、传说 | `game-designer` | `narrative-director`（故事）、`writer`（内容）、`art-director`（角色视觉配置文件、电影色调） |
| UI 系统（HUD，菜单） | `game-designer` | `ux-designer`（流程）、`ui-programmer`（可行性）、`art-director`（视觉风格方向）、`technical-artist`（render/shader 约束） |
| 音频系统 | `game-designer` | `audio-director`（方向），`sound-designer`（规格） |
| 人工智能、寻路、行为 | `game-designer` | `ai-programmer`（实现）、`systems-designer`（评分） |
| Level/world 系统 | `game-designer` | `level-designer`（空间）、`world-builder`（传说） |
| 摄像头、输入、控件 | `game-designer` | `ux-designer`（手感）、`gameplay-programmer`（可行性） |
| 动画、角色动作 | `game-designer` | `art-director`（动画风格、姿势语言）、`technical-artist`（rig/blend约束）、`gameplay-programmer`（感觉） |
| 视觉效果、粒子、着色器 | `game-designer` | `art-director`（VFX视觉方向）、`technical-artist`（性能预算、着色器复杂性）、`systems-designer`（trigger/state集成） |
| 角色系统（统计数据、原型） | `game-designer` | `art-director`（字符视觉原型）、`narrative-director`（字符弧对齐）、`systems-designer`（统计公式） |

**通过 Task 工具委托时**：
- 提供：系统名称、游戏概念概要、依赖GDD摘录、具体
  正在研究的部分，以及哪些问题需要专家的意见
- 代理将 analysis/proposals 返回到主会话
- 主会话通过 `AskUserQuestion` 将代理的输出呈现给用户
- 用户决定；主会话写入文件
- 代理不直接写入文件 - 主会话拥有所有文件写入

---

## 7. 恢复和继续

如果会话中断（压缩、崩溃、新会话）：

1. Read `production/session-state/active.md` — 它记录当前系统并
   哪些部分已完成
2. Read `design/gdd/[system-name].md` — 具有真实内容的部分已完成；
   带有 `[To be designed]` 的部分仍然需要工作
3. 从下一个未完成的部分继续——无需重新讨论已完成的部分

这就是为什么增量写作很重要：每个批准的部分都可以在任何情况下幸存下来
disruption.

---

## 协作协议

该技能的每一步都遵循协作设计原则：

1. **问题 -> 选项 -> 决定 -> 草案 -> 批准** 每个部分
2. **AskUserQuestion** 在每个决策点（解释 -> 捕获模式）：
   - 第 2 阶段：“准备好开始，还是需要更多背景信息？”
   - 第三阶段：“我可以创建骨架吗？”
   - 第 4 阶段（每个部分）：设计问题、方法选项、草案批准
   - 阶段 5：“运行设计评审？更新系统索引？下一步是什么？”
3. **“我可以写信给 [filepath] 吗？”** 在骨架之前和每个部分写之前
4. **增量写入**：每个部分在批准后立即写入归档
5. **会话状态更新**：在每个部分写入之后
6. **交叉引用**：每个部分都会检查现有 GDD 是否存在冲突
7. **专家路由**：复杂的部分获得专家代理的输入，呈现给
   用户做出决定——从不默写

**永远不要**自动生成完整的 GDD 并将其呈现为既成事实。
**切勿**在未经用户批准的情况下编写部分。
**切勿**与现有已批准的 GDD 相矛盾而不标记冲突。
**始终**显示决策的来源（依赖 GDD、支柱、用户选择）。

## 上下文窗口感知

这是一个长期运行的技能。写完每个部分后，检查状态行是否
显示 70% 或以上的上下文。如果是这样，请将此通知附加到响应中：

> **上下文已接近极限 (≥70%)。** 您的进度已保存 - 全部已批准
> 部分写入 `design/gdd/[system-name].md`。当你准备好继续时，
> 打开一个新的 Codex 会话并运行 `/design-system [system-name]` — 它将
> 检测哪些部分已完成并从下一个部分继续。

---

## 建议的后续步骤

- 在**新会话**中运行 `/design-review design/gdd/[system-name].md` 以独立验证已完成的 GDD
- 运行 `/consistency-check` 以验证此 GDD 的值不与其他 GDD 冲突
- 运行 `/map-systems next` 以移至下一个最高优先级的未设计系统
- 当所有 MVP GDD 均已编写和审核后运行 `/gate-check pre-production`
