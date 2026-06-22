---
name: milestone-review
description: "生成全面的里程碑进度审查，包括功能完整性、质量指标、风险评估和 go/no-go 建议。在里程碑检查点或评估里程碑截止日期的准备情况时使用。"
---

## 第 0 阶段：解析参数

提取里程碑名称（`current` 或特定名称）并解析审核模式（一次，存储此运行中生成的所有门）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

---

## 第 1 阶段：加载里程碑数据

Read `production/milestones/` 的里程碑定义。如果参数为 `current`，则使用最近修改的里程碑文件。

Read 来自 `production/sprints/` 的此里程碑内冲刺的所有冲刺报告。

---

## 第 2 阶段：扫描代码库健康状况

- 扫描指示未完成工作的 `TODO`、`FIXME`、`HACK` 标记
- 检查风险登记册 `production/risk-register/`

---

## 第 3 阶段：生成里程碑审核

```markdown
# Milestone Review: [Milestone Name]

## Overview
- **Target Date**: [Date]
- **Current Date**: [Today]
- **Days Remaining**: [N]
- **Sprints Completed**: [X/Y]

## Feature Completeness

### Fully Complete
| Feature | Acceptance Criteria | Test Status |
|---------|-------------------|-------------|

### Partially Complete
| Feature | % Done | Remaining Work | Risk to Milestone |
|---------|--------|---------------|------------------|

### Not Started
| Feature | Priority | Can Cut? | Impact of Cutting |
|---------|----------|----------|------------------|

## Quality Metrics
- **Open S1 Bugs**: [N] -- [List]
- **Open S2 Bugs**: [N]
- **Open S3 Bugs**: [N]
- **Test Coverage**: [X%]
- **Performance**: [Within budget? Details]

## Code Health
- **TODO count**: [N across codebase]
- **FIXME count**: [N]
- **HACK count**: [N]
- **Technical debt items**: [List critical ones]

## Risk Assessment
| Risk | Status | Impact if Realized | Mitigation Status |
|------|--------|-------------------|------------------|

## Velocity Analysis
- **Planned vs Completed** (across all sprints): [X/Y tasks = Z%]
- **Trend**: [Improving / Stable / Declining]
- **Adjusted estimate for remaining work**: [Days needed at current velocity]

## Scope Recommendations
### Protect (Must ship with milestone)
- [Feature and why]

### At Risk (May need to cut or simplify)
- [Feature and risk]

### Cut Candidates (Can defer without compromising milestone)
- [Feature and impact of cutting]

## Go/No-Go Assessment

**Recommendation**: [GO / CONDITIONAL GO / NO-GO]

**Conditions** (if conditional):
- [Condition 1 that must be met]
- [Condition 2 that must be met]

**Rationale**: [Explanation of the recommendation]

## Action Items
| # | Action | Owner | Deadline |
|---|--------|-------|----------|
```

---

## 第 3b 阶段：生产者风险评估

**审查模式检查** — 在生成 PR-MILESTONE 之前应用：
- `solo` → 跳过。注意：“PR-MILESTONE 已跳过 — 单人模式。”呈现 Go/No-Go 部分，无需制作人裁决。
- `lean` → 跳过（不是相位门）。注意：“PR-MILESTONE 已跳过 — 精益模式。”呈现 Go/No-Go 部分，无需制作人裁决。
- `full` → 正常生成。

在生成 Go/No-Go 建议之前，使用门 **PR-MILESTONE** (`.codex/docs/director-gates.md`) 通过 Task 生成 `producer`。

通过：里程碑名称和目标日期、当前完成百分比、阻塞故事计数、冲刺报告中的速度数据（如果有）、候选者列表。

在 Go/No-Go 部分中内嵌制作人的评估。制作人的裁决（正常/有风险/偏离轨道）告知整体建议 - 在没有明确用户确认的情况下，不要针对偏离轨道的制作人裁决发出 GO。

---

## 第四阶段：保存评论

向用户呈现评论。

问：“我可以把这个写到 `production/milestones/[milestone-name]-review.md` 吗？”

如果是，则写入文件，并根据需要创建目录。结论：**完成** — 里程碑审核已保存。

如果没有，就停在这里。结论：**被阻止**——用户拒绝写入。

---

## 第五阶段：后续步骤

- 如果此里程碑标志着开发阶段边界，请运行 `/gate-check` 以获得正式的阶段门裁决。
- 运行 `/sprint-plan` 以根据上述范围建议调整下一个冲刺。
