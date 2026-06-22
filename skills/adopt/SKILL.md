---
name: adopt
description: "Brownfield onboarding — 审核现有项目工件的模板格式合规性（而不仅仅是存在），按影响对差距进行分类，并生成编号的迁移计划。加入正在进行的项目或从旧模板版本升级时运行此命令。与 /project-stage-detect（检查存在的内容）不同 - 它检查存在的内容是否真正适用于模板的技能。"
---

# 采用 — 棕地模板采用

此技能审核现有项目的工件的**格式合规性**
模板的技能管道，然后生成优先级迁移计划。

**这不是 `/project-stage-detect`。**
`/project-stage-detect` 回答：*存在什么？*
`/adopt` 回答：*现有的内容实际上可以与模板的技能配合使用吗？*

一个项目可以有 GDD、ADR 和故事——以及每一项格式敏感的技能
如果这些工件位于其中，仍然会默默地失败或产生错误的结果
内部格式错误。

**输出：** `docs/adoption-plan-[date].md` — 持久的、可检查的迁移计划。

**论证模式：**

**审核模式：** `$ARGUMENTS[0]`（空白 = `full`）

- **无参数/`full`**：完整审核 - 所有工件类型
- **`gdds`**：仅符合 GDD 格式
- **`adrs`**：仅符合 ADR 格式
- **`stories`**：仅符合故事格式
- **`infra`**：仅限基础设施工件差距（注册表、清单、冲刺状态、stage.txt）

---

## 第一阶段：检测项目状态

在读取之前发出一行：`"Scanning project artifacts..."` — 这确认了
技能在静默阅读阶段运行。

然后在展示其他内容之前默读。

### 存在性检查
- `production/stage.txt` — 如果存在，请阅读它（权威阶段）
- `design/gdd/game-concept.md` — 概念存在吗？
- `design/gdd/systems-index.md` — 系统索引存在吗？
- 计数 GDD 文件：`design/gdd/*.md`（不包括 game-concept.md 和 systems-index.md）
- 计数 ADR 文件：`docs/architecture/adr-*.md`
- 统计故事文件：`production/epics/**/*.md`（不包括EPIC.md）
- `.codex/docs/technical-preferences.md` — 引擎已配置？
- `docs/engine-reference/` — 引擎参考文档存在吗？
- Glob `docs/adoption-plan-*.md` — 记下最近的先前计划的文件名（如果存在）

### 推断阶段（如果没有 stage.txt）
使用与 `/project-stage-detect` 相同的启发式：
- `src/` 中的 10 多个源文件 → 生产
- `production/epics/` 中的故事 → 预制作
- ADR 存在 → 技术设置
- systems-index.md 存在 → 系统设计
- game-concept.md 存在 → 概念
- 什么都没有→新鲜（不是棕地项目——建议`/start`）

如果项目看起来很新（根本没有工件），请使用 `AskUserQuestion`：
- “这看起来像是一个新项目 - 没有发现任何现有工件。`/adopt` 用于
需要迁移工作的项目。你想做什么？”
  - “运行 `/start` — 开始引导首次入门”
  - “我的文物位于非标准位置 - 帮我找到它们”
  - "Cancel"

然后停止——无论用户选择哪个选项，都不要继续进行审核
（每个选项都会导致不同的技能或手动调查）。

报告：“检测到的阶段：[phase]。已找到：[N] GDD、[M] ADR、[P] 故事。”

---

## 第二阶段：格式审核

对于范围内的每个工件类型（基于参数模式），不仅要检查
该文件存在，但它包含模板所需的内部结构。

### 2a：GDD格式审核

对于找到的每个 GDD 文件，通过扫描标题检查 8 个必需部分：

| 必填部分 | 要寻找的标题模式 |
|---|---|
| Overview | `## Overview` |
| 玩家幻想 | `## Player Fantasy` |
| 详细规则/设计 | `## Detailed` 或 `## Core Rules` 或 `## Detailed Design` |
| Formulas | `## Formulas` 或 `## Formula` |
| 边缘情况 | `## Edge Cases` |
| Dependencies | `## Dependencies` 或 `## Depends` |
| 调音旋钮 | `## Tuning` |
| 验收标准 | `## Acceptance` |

对于每个 GDD，记录：
- 存在哪些部分
- 哪些部分缺失
- 当前部分中是否包含任何内容或仅包含占位符文本
  （`[To be designed]` 或同等产品）

另请检查：每个 GDD 的标头块中是否有 `**Status**:` 字段？
有效值：`In Design`、`Designed`、`In Review`、`Approved`、`Needs Revision`。

### 2b：ADR 格式审核

对于找到的每个 ADR 文件，检查以下关键部分：

| Section | 缺失影响 |
|---|---|
| `## Status` | **阻止** — `/story-readiness` ADR 状态检查默默地通过了一切 |
| `## ADR Dependencies` | 高 — `/architecture-review` 中的依赖性排序中断 |
| `## Engine Compatibility` | 高 — 截止后 API 风险未知 |
| `## GDD Requirements Addressed` | 中 — 可追溯性矩阵失去覆盖范围 |
| `## Performance Implications` | 低——不是管道关键的 |

对于每个 ADR，记录：存在哪些部分、缺少哪些部分、当前状态值
如果状态部分存在。

### 2c：systems-index.md 格式审核

如果 `design/gdd/systems-index.md` 存在：

1. **附加状态值** — Grep 对于包含以下内容的任何状态单元格
   括号：`"Needs Revision ("`、`"In Progress ("` 等
   这些破坏了 `/gate-check`、`/create-stories` 中的精确字符串匹配，
   和 `/architecture-review`。 **封锁。**

2. **有效状态值** — 检查“状态”列值仅来自：
   `Not Started`、`In Progress`、`In Review`、`Designed`、`Approved`、`Needs Revision`
   标记任何无法识别的值。

3. **列结构** — 检查表至少包含：系统名称、
层、优先级、状态列。缺少列会降低技能功能。

### 2d：故事格式审核

对于找到的每个故事文件：

- **`Manifest Version:` 字段** — 出现在故事标题中吗？ （低 — 如果不存在则自动通过）
- **TR-ID 参考** — 故事是否包含 `TR-[a-z]+-[0-9]+` 模式？ （中 — 无陈旧性跟踪）
- **ADR 参考** — 故事是否至少参考了一个 ADR？ （检查 `ADR-` 模式）
- **状态字段** — 存在且可读？
- **接受标准** — 故事是否有复选框列表 (`- [ ]`)？

### 2e：基础设施审计

| Artifact | Path | 缺失影响 |
|---|---|---|
| TR registry | `docs/architecture/tr-registry.yaml` | 高 — 没有稳定的需求 ID |
| 控制清单 | `docs/architecture/control-manifest.md` | 高 — 故事没有图层规则 |
| 清单版本标记 | 在清单标头中：`Manifest Version:` | MEDIUM — 盲目检查陈旧性 |
| 冲刺状态 | `production/sprint-status.yaml` | 中 — `/sprint-status` 回落至降价 |
| 舞台文件 | `production/stage.txt` | MEDIUM — 相位自动检测不可靠 |
| 发动机参考 | `docs/engine-reference/[engine]/VERSION.md` | 高 — ADR 发动机盲检查 |
| 架构溯源 | `docs/architecture/architecture-traceability.md` | MEDIUM — 无持久矩阵 |

### 2f：技术偏好审核

Read `.codex/docs/technical-preferences.md`。检查每个字段中的 `[TO BE CONFIGURED]`：
- 引擎、语言、渲染、物理 → 如果未配置则为高（ADR 技能失败）
- 命名约定 → MEDIUM
- 绩效预算 → 中
- 禁止的模式，允许的库 → 低（按设计从空开始）

---

## 第三阶段：对差距进行分类和优先排序

将所有审计中发现的每个差距分为四个严重级别：

**阻塞** — 将导致模板技能*立即*默默地产生错误的结果。
示例：ADR 缺少状态字段、系统索引括号状态值、
当 ADR 存在时，引擎未配置。

**高** — 将导致生成的故事缺少安全检查，或者
基础设施引导将会失败。
示例：ADR 缺少引擎兼容性、GDD 缺少验收标准
（无法从中生成故事），tr-registry.yaml 缺失。

**中** — 降低质量和管道跟踪，但不会破坏功能。
示例：GDD 缺少调谐旋钮或公式部分、故事缺少 TR-ID、
sprint-status.yaml 缺失。

**低** — 追溯性改进是可有可无的，但并不紧急。
示例：故事缺少清单版本标记，GDD 缺少开放问题部分。

计算每层的总数。如果 BLOCKING 为零并且 HIGH 间隙为零：报告该项目
与模板兼容，仅保留建议性改进。

---

## 第 4 阶段：制定迁移计划

制定一个编号、有序的行动计划。订购规则：
1. 首先阻塞间隙（必须在任何管道技能可靠运行之前修复）
2. 接下来是高差距，GDD/ADR 内容之前的基础设施（引导需要正确的格式）
3. 中等间隙排序：GDD 间隙之前 ADR 故事间隙之前的间隙（故事取决于 GDD 和 ADR）
4. 低差距最后

对于每个差距，生成一个计划条目：
- 清晰的问题陈述（一句话，没有行话）
- 如果技能可以处理它，则修复它的确切命令
- 如果需要直接编辑则手动步骤
- 时间估计（粗略：5 分钟/30 分钟/1 次）
- 用于跟踪的复选框 `- [ ]`

**特殊情况 - 系统索引括号状态值：**
如果存在，这始终是第一项。显示需要更改的确切值
以及确切的替换文本。在编写计划之前立即提出解决这个问题。

**特殊情况 - ADR 缺少状态字段：**
对于每个受影响的 ADR，修复方法为：
`/architecture-decision retrofit docs/architecture/adr-[NNNN]-[中文标题].md`
将每个 ADR 列为单独的可检查项目。

**特殊情况 - GDD 缺少部分：**
对于每个受影响的 GDD，列出缺失的部分以及修复方法：
`/design-system retrofit design/gdd/[filename].md`

**基础设施引导排序** — 始终按以下顺序出现：
1. 首先修复 ADR 格式（注册表取决于读取 ADR 状态字段）
2. 运行 `/architecture-review` → 引导程序 `tr-registry.yaml`
3. 运行 `/create-control-manifest` → 创建带有版本标记的清单
4. 运行 `/sprint-plan update` → 创建 `sprint-status.yaml`
5. 运行`/gate-check [phase]` → 权威写入`stage.txt`

**现有故事** — 明确说明：
> “现有的故事继续适用于所有模板技能 - 所有新格式
> 当字段不存在时检查自动通过。他们不会从 TR-ID 中受益
> 过时跟踪或清单版本检查，直到重新生成。这个
> 是故意的：不要重新生成已经在进行中的故事。”

---

## 第 5 阶段：呈现总结并询问 Write

在写作之前先给出一个简短的总结：

```
## Adoption Audit Summary
Phase detected: [phase]
Engine: [configured / NOT CONFIGURED]
GDDs audited: [N] ([X] fully compliant, [Y] with gaps)
ADRs audited: [N] ([X] fully compliant, [Y] with gaps)
Stories audited: [N]

Gap counts:
  BLOCKING: [N] — template skills will malfunction without these fixes
  HIGH:     [N] — unsafe to run /create-stories or /story-readiness
  MEDIUM:   [N] — quality degradation
  LOW:      [N] — optional improvements

Estimated remediation: [X blocking items × ~Y min each = roughly Z hours]
```

在要求写作之前，先展示一下**间隙预览**：
- 将每个阻塞间隙列为描述实际问题的单行项目符号
  (e.g. `systems-index.md: 3 rows have parenthetical status values`,
  `adr-0002.md: missing ## Status section`）。没有计数——显示实际物品。
- 仅将高/中/低显示为计数（例如 `HIGH: 4, MEDIUM: 2, LOW: 1`）。

这为用户提供了足够的上下文来在提交写入文件之前判断范围。

如果在第 1 阶段检测到先前的采用计划，请添加注释：
> “之前的计划存在于 `docs/adoption-plan-[prior-date].md`。新计划将
> 反映当前的项目状态——它与之前的运行没有差异。”

使用 `AskUserQuestion`：
- “准备好编写迁移计划了吗？”
  - “是的——写 `docs/adoption-plan-[date].md`”
  - “先给我看完整的计划预览（先别写）”
  - “取消 — 我将手动处理迁移”

如果用户选择“显示完整计划预览”，则将完整计划输出为
围栏降价块。然后用相同的三个选项再次询问。

---

## 第 6 阶段：Write 采用计划

如果获得批准，请使用以下结构编写 `docs/adoption-plan-[date].md`：

```markdown
# Adoption Plan

> **Generated**: [date]
> **Project phase**: [phase]
> **Engine**: [name + version, or "Not configured"]
> **Template version**: v1.0+

Work through these steps in order. Check off each item as you complete it.
Re-run `/adopt` anytime to check remaining gaps.

---

## Step 1: Fix Blocking Gaps

[One sub-section per blocking gap with problem, fix command, time estimate, checkbox]

---

## Step 2: Fix High-Priority Gaps

[One sub-section per high gap]

---

## Step 3: Bootstrap Infrastructure

### 3a. Register existing requirements (creates tr-registry.yaml)
Run `/architecture-review` — even if ADRs already exist, this run bootstraps
the TR registry from your existing GDDs and ADRs.
**Time**: 1 session (review can be long for large codebases)
- [ ] tr-registry.yaml created

### 3b. Create control manifest
Run `/create-control-manifest`
**Time**: 30 min
- [ ] docs/architecture/control-manifest.md created

### 3c. Create sprint tracking file
Run `/sprint-plan update`
**Time**: 5 min (if sprint plan already exists as markdown)
- [ ] production/sprint-status.yaml created

### 3d. Set authoritative project stage
Run `/gate-check [current-phase]`
**Time**: 5 min
- [ ] production/stage.txt written

---

## Step 4: Medium-Priority Gaps

[One sub-section per medium gap]

---

## Step 5: Optional Improvements

[One sub-section per low gap]

---

## What to Expect from Existing Stories

Existing stories continue to work with all template skills. New format checks
(TR-ID validation, manifest version staleness) auto-pass when the fields are
absent — so nothing breaks. They won't benefit from staleness tracking until
regenerated. Do not regenerate stories that are in progress or done.

---

## Re-run

Run `/adopt` again after completing Step 3 to verify all blocking and high gaps
are resolved. The new run will reflect the current state of the project.
```

---

## 阶段 6b：设置审核模式

编写采用计划后（或者如果用户取消编写），检查是否
`production/review-mode.txt` 存在。

**如果存在**：Read 并记下当前模式 — “审阅模式已设置为 `[current]`。” — 跳过提示。

**如果不存在**：使用`AskUserQuestion`：

- **提示**：“还有一个设置步骤：在完成工作流程时您希望进行多少设计审查？”
- **Options**:
  - `Full` — 主管专家在每个关键工作流程步骤进行审查。最适合团队、学习工作流程或当您需要对每个决定进行全面反馈时。
  - `Lean (recommended)` — 仅在相门转换时的导向器 (/gate-check)。跳过每项技能的评论。适合单独开发者和小团队。
  - `Solo` — 根本没有导演评论。最大速度。最适合游戏即兴创作、原型制作，或者如果评论感觉很麻烦的话。

选择后立即选择 Write 到 `production/review-mode.txt` — 没有单独的“我可以写吗？”需要：
- `Full`→写入`full`
- `Lean (recommended)`→写入`lean`
- `Solo` → 写入 `solo`

如果 `production/` 目录不存在，则创建该目录。

---

## 第 7 阶段：提供第一个行动

写完计划后，不要就此止步。选择单个最高优先级的差距
并提出使用 `AskUserQuestion` 立即处理。选择第一个
适用的分支：

**如果systems-index.md中有括号状态值：**
使用 `AskUserQuestion`：
- “最紧急的修复是 `systems-index.md` — [N] 行具有括号状态
  破坏 /gate-check 的值（例如 `Needs Revision (see notes)`），
  现在是 /create-stories 和 /architecture-review。我可以就地修复这些问题。”
  - “立即修复 - 编辑 systems-index.md”
  - “我自己解决”
  - “完成了——把计划留给我”

**如果 ADR 缺少 `## Status`（并且没有括号问题）：**
使用 `AskUserQuestion`：
- “最紧急的修复是将 `## Status` 添加到 [N] ADR：[list filenames]。
  如果没有它，/story-readiness 会默默地通过所有 ADR 检查。开始于
  [first affected filename]？”
  - “是的 — 立即改装 [first affected filename]”
  - “一一改造所有 [N] ADR”
  - “我会亲自处理 ADR”

**如果 GDD 缺少验收标准（并且没有上述阻塞问题）：**
使用 `AskUserQuestion`：
- “最紧迫的差距是 [N] GDD 中缺少验收标准：
  [list filenames]。没有它们，/create-stories 就无法生成故事。
  从 [highest-priority GDD filename] 开始？”
  - “是的 - 立即将验收标准添加到 [GDD filename]”
  - “一一完成所有[N] GDD”
  - “我会亲自处理 GDD”

**如果不存在阻塞或高间隙：**
使用 `AskUserQuestion`：
- “没有阻塞间隙——这个项目是模板兼容的。接下来做什么？”
  - “引导我完成中等优先级的改进”
  - “运行 /project-stage-detect 进行更广泛的健康检查”
  - “完成——我将按照自己的节奏完成计划”

---

## 协作协议

1. **Read 默默** — 在展示任何内容之前完成完整的审核
2. **首先显示摘要** - 让用户在要求写入之前查看范围
3. **写作前询问** — 在创建采用计划文件之前始终确认
4. **提供，不要强迫**——该计划是建议性的；用户决定修复什么以及何时修复
5. **一次一项行动** - 交付计划后，提供一个具体的下一步，
   不是同时做六件事的清单
6. **永远不要重新生成现有的工件**——只填补现有的空白；
   不要重写 GDD、ADR 或已有内容的故事
