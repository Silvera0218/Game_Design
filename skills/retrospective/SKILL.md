---
name: retrospective
description: "通过分析已完成的工作、速度、阻碍因素和模式，生成冲刺或里程碑回顾。为下一次迭代提供可行的见解。"
---

## 第一阶段：解析参数

确定这是冲刺回顾 (`sprint-N`) 还是里程碑回顾 (`milestone-name`)。

---

## 第 1b 阶段：检查现有回顾

在加载任何数据之前，glob 查找现有的回顾文件：

- 对于冲刺回顾：`production/retrospectives/retro-[sprint-slug]-*.md`
  （另请检查 `production/sprints/sprint-[N]-retrospective.md` 作为备用位置）
- 对于里程碑回顾：`production/retrospectives/retro-[milestone-name]-*.md`

如果找到匹配的文件，则向用户显示：

```
An existing retrospective was found: [filename]

[A] Update existing retrospective — load it and add/revise sections
[B] Start fresh — generate a new retrospective, archiving the old one
```

等待用户选择后再继续。如果更新，请读取现有文件并
将其内容推进到生成阶段，用新数据修改部分内容。

---

## 第 2 阶段：加载 Sprint 或里程碑数据

Read 来自适当位置的冲刺或里程碑计划：

- 冲刺计划：`production/sprints/`
- 里程碑定义：`production/milestones/`

**如果文件不存在或者为空**，则输出：

> “未找到 [sprint/milestone] 的冲刺数据。运行 `/sprint-status` 生成
> 首先冲刺数据，或手动提供冲刺详细信息。”

然后使用 `AskUserQuestion` 呈现两个选项：

- **[A] 手动提供数据** — 要求用户粘贴或描述冲刺
  任务、日期和结果；将其用作回顾的事实来源。
- **[B] 停止** — 中止技能。结论：**被阻止**——没有可用的冲刺数据。

如果用户选择 [A]，则收集数据并使用他们提供的数据继续进行第 3 阶段。
如果用户选择[B]，则到此为止。

摘录：计划的任务、估计的工作量、所有者和目标。

Read 冲刺或里程碑所涵盖期间的 git 日志，用于了解实际提交的内容和时间。

---

## 第 3 阶段：分析完成情况和趋势

通过将计划与实际可交付成果进行比较来扫描已完成和未完成的任务。检查：

- 按计划完成任务
- 任务已完成但对计划进行了修改
- 结转的任务（未完成）
- 冲刺中期添加的任务（计划外工作）
- 任务已删除或范围缩小

扫描代码库以了解 TODO/FIXME 趋势：

- 统计当前 TODO/FIXME/HACK 评论
- 与之前的冲刺计数（如果有）进行比较（检查之前的回顾）
- 注意技术债务是增加还是减少

Read 来自 `production/sprints/` 或 `production/milestones/` 的先前回顾（如果有）以检查：

- 之前的行动项目是否得到解决？
- 同样的问题是否反复出现？
- 速度趋势如何？

---

## 第 4 阶段：生成回顾

```markdown
## Retrospective: [Sprint N / Milestone Name]
Period: [Start Date] -- [End Date]
Generated: [Date]

### Metrics

| Metric | Planned | Actual | Delta |
|--------|---------|--------|-------|
| Tasks | [X] | [Y] | [+/- Z] |
| Completion Rate | -- | [Z%] | -- |
| Story Points / Effort Days | [X] | [Y] | [+/- Z] |
| Bugs Found | -- | [N] | -- |
| Bugs Fixed | -- | [N] | -- |
| Unplanned Tasks Added | -- | [N] | -- |
| Commits | -- | [N] | -- |

### Velocity Trend

| Sprint | Planned | Completed | Rate |
|--------|---------|-----------|------|
| [N-2] | [X] | [Y] | [Z%] |
| [N-1] | [X] | [Y] | [Z%] |
| [N] (current) | [X] | [Y] | [Z%] |

**Trend**: [Increasing / Stable / Decreasing]
[One sentence explaining the trend]

### What Went Well
- [Observation backed by specific data or examples]
- [Another positive observation]
- [Recognize specific contributions or decisions that paid off]

### What Went Poorly
- [Specific issue with measurable impact -- e.g., "Feature X took 5 days
  instead of estimated 2, blocking tasks Y and Z"]
- [Another issue with impact]
- [Do not assign blame -- focus on systemic causes]

### Blockers Encountered

| Blocker | Duration | Resolution | Prevention |
|---------|----------|------------|------------|
| [What blocked progress] | [How long] | [How it was resolved] | [How to prevent recurrence] |

### Estimation Accuracy

| Task | Estimated | Actual | Variance | Likely Cause |
|------|-----------|--------|----------|--------------|
| [Most overestimated task] | [X] | [Y] | [+Z] | [Why] |
| [Most underestimated task] | [X] | [Y] | [-Z] | [Why] |

**Overall estimation accuracy**: [X%] of tasks within +/- 20% of estimate

[Analysis: Are we consistently over- or under-estimating? For which types of
tasks? What adjustment should we apply?]

### Carryover Analysis

| Task | Original Sprint | Times Carried | Reason | Action |
|------|----------------|---------------|--------|--------|
| [Task that was not completed] | [Sprint N-X] | [N] | [Why] | [Complete / Descope / Redesign] |

### Technical Debt Status
- Current TODO count: [N] (previous: [N])
- Current FIXME count: [N] (previous: [N])
- Current HACK count: [N] (previous: [N])
- Trend: [Growing / Stable / Shrinking]
- [Note any areas of concern]

### Previous Action Items Follow-Up

| Action Item (from Sprint N-1) | Status | Notes |
|-------------------------------|--------|-------|
| [Previous action] | [Done / In Progress / Not Started] | [Context] |

### Action Items for Next Iteration

| # | Action | Owner | Priority | Deadline |
|---|--------|-------|----------|----------|
| 1 | [Specific, measurable action] | [Who] | [High/Med/Low] | [When] |
| 2 | [Another action] | [Who] | [Priority] | [When] |

### Process Improvements
- [Specific change to how we work, with expected benefit]
- [Another improvement -- keep it to 2-3 actionable items, not a wish list]

### Summary
[2-3 sentence overall assessment: Was this a good sprint/milestone? What is
the single most important thing to change going forward?]
```

---

## 第五阶段：保存回顾

向用户展示回顾性的和最重要的发现（完成率、速度趋势、最重要的阻碍、最重要的行动项目）。

问：“我可以把这个写到 `production/sprints/sprint-[N]-retrospective.md` 吗？” （或里程碑路径，如果适用）

如果是，则写入文件，并根据需要创建目录。结论：**完成** — 已保存回顾性。

如果没有，就停在这里。结论：**被阻止**——用户拒绝写入。

---

## 第六阶段：后续步骤

- 运行 `/sprint-plan` 将操作项和速度数据合并到下一个冲刺中。
- 如果这是里程碑式的回顾，请运行 `/gate-check` 来正式评估下一阶段的准备情况。

### Guidelines

- 诚实且具体。模糊的回顾（“沟通可以更好”）产生模糊的改进。使用数据和例子。
- 关注系统性问题，而不是个人指责。
- 将行动项目限制为 3-5 个。不仅如此，还会削弱焦点。
- 每个行动项目都必须有一个所有者和截止日期。
- 检查之前的行动项目是否完成。重复出现的未解决的项目是一种过程气味。
- 如果这是一个里程碑回顾，还要评估里程碑目标是否实现以及这对整个项目时间表意味着什么。
