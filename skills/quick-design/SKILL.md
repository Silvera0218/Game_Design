---
name: quick-design
description: "针对微小变化的轻量级设计规范——调音调整、细微机械结构、平衡调整。当系统 GDD 已存在或更改太小而无法保证时，跳过完整的 GDD 创作。生成直接嵌入到故事文件中的快速设计规范。"
---

# 快速设计

这是不需要完整 GDD 的更改的**轻量级设计路径**。
通过 `/design-system` 进行完整的 GDD 创作是重量级路径。使用这个技能
对于大约 4 小时的实施工作 - 调整调整，
细微的行为调整、对现有系统的少量添加或独立
功能太小，无法保证完整的文档。

**输出：** `design/quick-specs/[name]-[date].md`

**何时运行：** 任何时候更改对于 `/design-system` 来说太小但又太小
在没有书面理由的情况下实施是有意义的。

---

## 1. 对变更进行分类

首先，阅读论证并确定此更改属于哪一类：

- **调整** — 更改现有系统中的数字或平衡值，无需
  行为改变（最短路径）。示例：“将跳跃高度从 5 增加到
  减少到6个单位”，“减少敌人巡逻速度10%”。
- **调整**——对现有系统进行一个小的行为改变，不引入任何
  新的状态、分支或系统。示例：“使冲刺在第 1 帧上无敌”，
  “允许组合取消进入滚动”。
- **添加** — 在现有系统中添加一个小机制，可能会引入
  1-2 个新状态或交互。示例：“向方块添加一个格挡窗口
  机械师”，“在基本攻击中添加冲锋变体”。
- **新的小型系统** - 一个独立的功能，足够小，没有
  现有 GDD，正在进行大约一周的实施工作。
  示例：“成就弹出系统”、“简单day/night可视化循环”。

如果更改不适合这些类别 - 它会引入一个新系统
显着的跨系统依赖性，需要超过一周的时间
实施，或从根本上改变现有系统的核心规则——停止
并重定向到 `/design-system`。

将分类呈现给用户并确认其正确性
进行中。如果没有争议，请要求用户描述更改。

---

## 2. 上下文扫描

在起草任何内容之前，请阅读相关上下文：

- 搜索 `design/gdd/` 以查找与此更改最相关的 GDD。 Read 的
  此更改将影响的部分。
- 检查`design/gdd/systems-index.md`是否存在。如果是的话，请阅读它
了解该系统在依赖图中的位置以及它的层级
  属于.如果不存在，请注意“未找到系统索引 - 跳过
  依赖层检查。”并继续。
- 检查 `design/quick-specs/` 是否有任何涉及此的先前快速规格
  系统——避免与它们相矛盾。
- 如果这是调整更改，还请检查 `assets/data/` 的数据文件
  持有相关值。

报告发现的内容：“在 [path] 找到 GDD。相关部分：[section name]。
没有发现相互冲突的快速规格。” （或记下发现的任何冲突。）

---

## 3. 起草快速设计规范

对变更类别使用适当的规范格式。

### 对于调整更改

生成单个表：

```markdown
# Quick Design Spec: [Title]

**Type**: Tuning
**System**: [System name]
**GDD Reference**: `design/gdd/[filename].md` — Tuning Knobs section
**Date**: [today]

## Change

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| [param]   | [old]     | [new]     | [why]     |

## Tuning Knob Mapping

Maps to GDD Tuning Knob: [knob name and its documented range].
New value is [within / at the edge of / outside] the documented range.
[If outside: explain why the range should be extended.]

## Acceptance Criteria

- [ ] [Parameter] reads [new value] from `assets/data/[file]`
- [ ] Behavior difference is observable in [specific context]
- [ ] No regression in [related behavior]
```

### 对于调整和添加更改

```markdown
# Quick Design Spec: [Title]

**Type**: [Tweak / Addition]
**System**: [System name]
**GDD Reference**: `design/gdd/[filename].md`
**Date**: [today]

## Change Summary

[1-2 sentences describing what changes and why.]

## Motivation

[Why is this change needed? What player experience problem does it solve?
Reference the relevant MDA aesthetic or player feedback if applicable.]

## Design Delta

Current GDD says (quoting `design/gdd/[filename].md`, [section]):

> [exact quote of the relevant rule or description]

This spec changes that to:

[New rule or description, written with the same precision as a GDD Detailed
Rules section. A programmer should be able to implement from this text alone.]

## New Rules / Values

[Full unambiguous statement of the replacement content. If this introduces
new states, list them. If it introduces new parameters, define their ranges.]

## Affected Systems

| System | Impact | Action Required |
|--------|--------|-----------------|
| [system] | [how it is affected] | [update GDD / update data file / no action] |

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] No regression: [the original behavior this must not break]

## GDD Update Required?

[Yes / No]
[If yes: which file, which section, and what the update should say.]
```

### 对于新的小型系统更改

使用修剪后的 GDD 结构。仅包含直接的部分
必要 — 跳过玩家幻想、完整公式和边缘情况，除非
系统特别需要它们。

```markdown
# Quick Design Spec: [Title]

**Type**: New Small System
**Scope**: [1-2 sentence description of what this system does and doesn't do]
**Date**: [today]
**Estimated Implementation**: [hours]

## Overview

[One paragraph a new team member could understand. What does this system do,
when does it activate, and what does it produce?]

## Core Rules

[Unambiguous rules for the system. Use numbered lists for sequential behavior
and bullet lists for conditions. Be precise enough that a programmer can
implement without asking questions.]

## Tuning Knobs

| Knob | Default | Range | Category | Rationale |
|------|---------|-------|----------|-----------|
| [name] | [value] | [min–max] | [feel/curve/gate] | [why this default] |

All values must live in `assets/data/[appropriate-file].json`, not hardcoded.

## Acceptance Criteria

- [ ] [Functional criterion: does the right thing]
- [ ] [Functional criterion: handles the edge case]
- [ ] [Experiential criterion: feels right — what a playtest validates]
- [ ] [Regression criterion: does not break adjacent system]

## Systems Index

This system is not currently in `design/gdd/systems-index.md`.
[If it should be added: suggest which layer and priority tier.]
[If it is too small to track: state "This system is below systems-index
tracking threshold — quick spec is sufficient."]
```

---

## 四、审批和备案

将草稿完整地呈现给用户。然后问：

“我可以将这份快速设计规范写给
`design/quick-specs/[kebab-case-title]-[YYYY-MM-DD].md`？”

在文件名中使用今天的日期。标题应该是烤肉串描述
更改的信息（例如，`jump-height-tuning-2026-03-10`，
`parry-window-addition-2026-03-10`).

如果有，则创建`design/quick-specs/`目录，如果不存在，则
写入文件。

如果需要 GDD 更新（在规范中标记），请在
编写快速规范：

“此规范修改了 [System Name] 中的规则。我可以更新吗
`design/gdd/[filename].md` — 特别是 [section name] 部分？”

在询问之前显示将要更改的确切文本（旧的与新的）。不
未经明确批准进行 GDD 编辑。

---

## 5. Handoff

写入文件后，输出：

```
Quick Design Spec written to: design/quick-specs/[filename].md
Type: [Tuning / Tweak / Addition / New Small System]
System: [system name]
GDD update: [Required — pending approval / Applied / Not required]

Next step: This spec is ready for `/story-readiness` validation before
implementation. Reference this spec in the story's GDD Reference field.
```

### 管道注释

结论：**完成**——快速编写设计规范并准备实施。

快速设计规格 **绕过** `/design-review` 和 `/review-all-gdds`
设计。它们适用于小型、低风险、范围广泛的变更，其中成本
完整的审核流程超出了变更本身的风险。

如果满足以下任一条件，则重定向到完整管道：
- 该更改添加了属于系统索引的新系统
- 该变化显着改变了跨系统行为或系统的
  与其他系统签订合同
- 这一变化引入了新的面向玩家的机制，影响
  游戏的MDA美学平衡
- 实施可能会超过一周的工作时间

在这些情况下：“这种变化已经超出了快速规范的范围。我建议
使用 `/design-system` 为此编写完整的 GDD。”

---

## 建议的后续步骤

- 在实施开始之前运行 `/story-readiness [story-path]` 以验证故事 - 在故事的 GDD 参考字段中引用此规范
- 一旦故事通过准备检查，就运行 `/dev-story [story-path]` 来实施
- 如果更改大于预期，请运行 `/design-system [system-name]` 来编写完整的 GDD
