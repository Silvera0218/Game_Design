---
name: scope-check
description: "通过将当前范围与原始计划进行比较来分析功能或冲刺的范围蠕变。标记添加、量化膨胀并建议削减。当用户说“任何范围蔓延”、“范围审查”、“我们是否留在范围内”时使用。"
---

# 范围检查

该技能是只读的 - 它报告发现但不写入文件。

将原始计划范围与当前状态进行比较，以进行检测、量化和分类
范围蔓延。

**参数：** `$ARGUMENTS[0]` — 功能名称、冲刺编号或里程碑名称。

---

## 第一阶段：找到最初的计划

找到给定参数的基线范围文档：

- **功能名称** → 读取 `design/gdd/[feature].md` 或 `design/` 中的匹配文件
- **Sprint 编号**（例如，`sprint-3`）→ 阅读 `production/sprints/sprint-03.md` 或类似内容
- **里程碑** → 阅读 `production/milestones/[name].md`

如果未找到该文档，则报告丢失的文件并停止。如果没有，请勿继续
比较的基线。

---

## 第 2 阶段：Read 当前状态

检查实际已实施或正在进行的内容：

- 扫描代码库中与 feature/sprint 相关的文件
- Read 与此工作相关的提交的 git 日志 (`git log --oneline --since=[start-date]`)
- 检查指示未完成范围添加的 TODO/FIXME 注释
- 如果该功能处于冲刺中期，请检查活动的冲刺计划

---

## 第 3 阶段：比较原始范围与当前范围

生成比较报告：

```markdown
## Scope Check: [Feature/Sprint Name]
Generated: [Date]

### Original Scope
[List of items from the original plan]

### Current Scope
[List of items currently implemented or in progress]

### Scope Additions (not in original plan)
| Addition | Source | When | Justified? | Effort |
|----------|--------|------|------------|--------|
| [item] | [commit/person] | [date] | [Yes/No/Unclear] | [S/M/L] |

### Scope Removals (in original but dropped)
| Removed Item | Reason | Impact |
|-------------|--------|--------|
| [item] | [why removed] | [what's affected] |

### Bloat Score
- Original items: [N]
- Current items: [N]
- Items added: [N] (+[X]%)
- Items removed: [N]
- Net scope change: [+/-N] ([X]%)

### Risk Assessment
- **Schedule Risk**: [Low/Medium/High] — [explanation]
- **Quality Risk**: [Low/Medium/High] — [explanation]
- **Integration Risk**: [Low/Medium/High] — [explanation]

### Recommendations
1. **Cut**: [Items that should be removed to stay on schedule]
2. **Defer**: [Items that can move to a future sprint/version]
3. **Keep**: [Additions that are genuinely necessary]
4. **Flag**: [Items that need a decision from producer/creative-director]
```

---

## 第四阶段：判决

根据净范围变化分配规范判决：

| 净变化 | Verdict | Meaning |
|-----------|---------|---------|
| ≤10% | **PASS** | 步入正轨——在可接受的差异范围内 |
| 10–25% | **CONCERNS** | 轻微蠕变——可通过有针对性的削减来控制 |
| 25–50% | **FAIL** | 重大蠕变——必须缩短或正式延长时间表 |
| >50% | **FAIL** | 失控——停止、重新计划、上报给生产者 |

显着输出判决结果：

```
**Scope Verdict: [PASS / CONCERNS / FAIL]**
Net change: [+X%] — [On Track / Minor Creep / Significant Creep / Out of Control]
```

---

## 第五阶段：后续步骤

提交报告后，提出具体的后续行动：

- **通过** → 无需采取任何行动。建议在下一个里程碑之前重新运行。
- **关注** → 提出确定具有最佳切割比例的 2-3 个添加项。参考 `/sprint-plan update` 正式重新调整范围。
- **失败** → 建议升级给生产者。参考 `/sprint-plan update` 进行重新规划，或参考 `/estimate` 重新设定时间线基线。

始终以以下内容结尾：
> “进行切割后再次运行 `/scope-check [name]` 以验证判决是否有所改善。”

---

### Rules

- 范围蔓延是指没有相应削减或时间线延长的增加
- 并非所有添加都是不好的——有些是被发现的需求。但必须承认并解释它们
- 在建议削减时，优先考虑保留核心玩家体验而不是锦上添花
- 始终量化范围变化——“感觉更大”是不可行的，“+35% 的项目”才是可行的
