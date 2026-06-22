---
name: sprint-status
description: "快速冲刺状态检查。读取当前的冲刺计划，扫描故事文件的状态，并生成包含燃尽评估和新出现风险的简明进度快照。在冲刺期间随时跑步，以便快速了解情况。当用户询问“冲刺进展如何”、“冲刺更新”、“显示冲刺进度”时使用。"
---

# 冲刺状态

这是快速态势感知检查，而不是冲刺审查。它读取
当前的冲刺计划和故事文件，扫描状态标记，并生成
30 行以内的简洁快照。对于详细的冲刺管理，请使用
`/sprint-plan update` 或 `/milestone-review`。

**此技能是只读的。**它从不提出更改，从不要求写入
文件，并最多提出一项具体建议。

---

## 1. 找到冲刺

**参数：** `$ARGUMENTS[0]`（空白=使用当前冲刺）

- 如果给出参数（例如，`/sprint-status 3`），则搜索
  `production/sprints/` 用于匹配 `sprint-03.md`、`sprint-3.md`、
  或类似的。报告找到了哪个文件。
- 如果没有给出参数，则在以下位置查找最近修改的文件
  `production/sprints/` 并将其视为当前冲刺。
- 如果 `production/sprints/` 不存在或者为空，则报告：“No sprint
  找到的文件。使用 `/sprint-plan new` 开始冲刺。”然后停下来。

Read 完整的冲刺文件。摘录：
- Sprint 编号和目标
- 开始日期和结束日期
- 所有故事或任务条目及其优先级（必须有/应该有/
  很高兴拥有）、所有者和估计

---

## 2. 计算剩余天数

使用今天的日期和冲刺文件中的冲刺结束日期，计算：
- 冲刺总天数（结束减去开始）
- 已过天数
- 剩余天数
- 消耗时间百分比

如果冲刺文件不包含明确的日期，请注意“冲刺日期不包括
发现——燃尽评估被跳过。”

---

## 3. 扫描故事状态

**首先：检查 `production/sprint-status.yaml`。**

如果存在，请直接阅读——它是权威的事实来源。
从 `status` 字段中提取每个故事的状态。无需降价扫描。
使用其 `sprint`、`goal`、`start`、`end` 字段，而不是重新解析冲刺计划。

**如果 `sprint-status.yaml` 不存在**（旧版冲刺或首次设置），
回退到 Markdown 扫描：

1. 如果条目引用故事文件路径，请检查该文件是否存在。
   Read 文件并扫描状态标记：完成、完成、进行中、
   已阻止，未启动（不区分大小写）。
2. 如果该条目没有文件路径（冲刺计划中的内联任务），则扫描
   冲刺计划本身用于该条目旁边的状态标记。
3. 如果未找到状态标记，则分类为“未启动”。
4. 如果引用文件但不存在，则分类为“丢失”并记下它。

使用后备时，请在输出底部添加注释：
“⚠ 未找到 `sprint-status.yaml` — 从降价推断的状态。运行 `/sprint-plan update` 生成一个。”

可选（仅快速检查 - 不进行深度扫描）：grep `src/`
与要检查的故事系统 slug 匹配的目录或文件名
实施证据。这只是一个提示，并不是确定的状态。

### 陈旧故事检测

收集所有故事的状态后，检查每个正在进行的故事是否过时：

- 对于每个有引用文件的故事，阅读该文件并查找
  Frontmatter 或 header 中的 `Last Updated:` 字段（例如，`Last Updated: 2026-04-01`
  或 `updated: 2026-04-01`）。接受任何合理的日期字段名称：`Last Updated`，
  `Updated`、`last-updated`、`updated_at`。
- 使用今天的日期计算自该日期以来的天数。
- 如果日期超过 2 天前，请将故事标记为 **STALE**。
- 如果故事文件中未找到日期字段，请注意“无时间戳 - 无法检查陈旧性”。
- 如果故事没有引用文件（内联任务），请注意“内联任务 - 无法检查陈旧性”。

STALE 故事包含在输出表中并收集到“需要注意”中
部分（请参阅第 5 阶段输出格式）。

**过时的故事升级**：如果任何正在进行的故事被标记为过时，则燃尽判决
升级到至少**处于风险** - 即使完成百分比在正常范围内
在“轨道”窗口上。记录此升级原因：“存在风险 — [N] 故事，但没有进展
[N] days."

---

## 4.燃尽评估

Calculate:
- 任务完成（完成或完成）
- 正在进行的任务（IN PROGRESS）
- 任务被阻止（BLOCKED）
- 任务未开始（NOT STARTED 或 MISSING）
- 完成百分比：（完成/总计）* 100

通过比较完成百分比与消耗时间百分比来评估燃尽：

- **按计划**：完成百分比在消耗时间 % 的 10 个点内或提前
- **有风险**：完成百分比比消耗时间百分比落后 10-25 个百分点
- **落后**：完成百分比比消耗时间百分比落后 25 分以上

如果日期不可用，请跳过燃尽评估并报告“按计划/
面临风险/落后：未知——未找到冲刺日期。”

---

## 5. Output

将总输出保持在 30 行或更少。使用这种格式：

```markdown
## Sprint [N] Status — [Today's Date]
**Sprint Goal**: [from sprint plan]
**Days Remaining**: [N] of [total] ([% time consumed])

### Progress: [complete/total] tasks ([%])

| Story / Task         | Priority   | Status      | Owner   | Blocker        |
|----------------------|------------|-------------|---------|----------------|
| [title]              | Must Have  | DONE        | [owner] |                |
| [title]              | Must Have  | IN PROGRESS | [owner] |                |
| [title]              | Must Have  | BLOCKED     | [owner] | [brief reason] |
| [title]              | Should Have| NOT STARTED | [owner] |                |

### Attention Needed
| Story / Task         | Status      | Last Updated   | Days Stale | Note           |
|----------------------|-------------|----------------|------------|----------------|
| [title]              | IN PROGRESS | [date or N/A]  | [N days]   | [STALE / no timestamp — cannot check staleness / inline task — cannot check staleness] |

*(Omit this section entirely if no IN PROGRESS stories are stale or have timestamp concerns.)*

### Burndown: [On Track / At Risk / Behind]
[1-2 sentences. If behind: which Must Haves are at risk. If on track: confirm
and note any Should Haves the team could pull.]

### Must-Haves at Risk
[List any Must Have stories that are BLOCKED or NOT STARTED with less than
40% of sprint time remaining. If none, write "None."]

### Emerging Risks
[Any risks visible from the story scan: missing files, cascading blockers,
stories with no owner. If none, write "None identified."]

### Recommendation
[One concrete action, or "Sprint is on track — no action needed."]
```

---

## 6. 快速升级规则

在输出之前应用这些规则，并将标志放置在顶部
触发时输出（状态表上方）：

**关键标志** — 如果必须有的故事被阻止或未开始并且
还剩下不到 40% 的冲刺时间：

```
SPRINT AT RISK: [N] Must Have stories are not complete with [X]% of sprint
time remaining. Recommend replanning with `/sprint-plan update`.
```

**完成标志** — 如果所有必备故事均已完成：

```
All Must Haves complete. Team can pull from Should Have backlog.
```

**缺少故事标志** — 如果任何引用的故事文件不存在：

```
NOTE: [N] story files referenced in the sprint plan are missing.
Run `/story-readiness sprint` to validate story file coverage.
```

---

## 协作协议

该技能是只读的。它报告从磁盘上的文件中观察到的事实。

- 它不会更新冲刺计划
- 它不会改变故事状态
- 它不建议范围削减（即 `/sprint-plan update`）
- 每次运行最多提出一个建议

有关特定故事的更多详细信息，用户可以直接阅读故事文件
或运行 `/story-readiness [path]`。

对于冲刺重新计划，请使用 `/sprint-plan update`。
对于冲刺结束回顾，请使用 `/milestone-review`。
