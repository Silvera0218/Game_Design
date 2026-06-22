---
name: estimate
description: "通过分析复杂性、依赖性、历史速度和风险因素来估计任务工作量。生成具有置信水平的结构化估计。"
---

## 第 1 阶段：了解 Task

Read 来自参数的任务描述。如果描述太模糊而无法进行有意义的估计，请在继续之前要求澄清。

Read AGENTS.md 用于项目上下文：技术堆栈、编码标准、架构模式和任何评估指南。

如果任务与记录的功能或系统相关，则来自 `design/gdd/` 的 Read 相关设计文档。

---

## 第 2 阶段：扫描受影响的代码

识别需要更改的文件和模块：

- 评估复杂性（大小、依赖项计数、圈复杂度）
- 确定与其他系统的集成点
- 检查受影响区域的现有测试覆盖范围
- Read 来自 `production/sprints/` 的过去冲刺数据，用于类似的已完成任务和历史速度

---

## 第 3 阶段：分析复杂性因素

**代码复杂度：**
- 受影响文件中的代码行
- 依赖数量和耦合程度
- 这是否触及 core/engine 代码与 leaf/feature 代码
- 是否可以遵循现有模式或是否需要新模式

**Scope:**
- 接触的系统数量
- 新代码与现有代码的修改
- 所需的新测试覆盖率
- 需要数据迁移或配置更改

**Risk:**
- 新技术或不熟悉的库
- 要求不明确或不明确
- 对未完成工作的依赖
- 跨系统集成复杂度
- 性能敏感性

---

## 第 4 阶段：生成估算

```markdown
## Task Estimate: [Task Name]
Generated: [Date]

### Task Description
[Restate the task clearly in 1-2 sentences]

### Complexity Assessment

| Factor | Assessment | Notes |
|--------|-----------|-------|
| Systems affected | [List] | [Core, gameplay, UI, etc.] |
| Files likely modified | [Count] | [Key files listed below] |
| New code vs modification | [Ratio] | |
| Integration points | [Count] | [Which systems interact] |
| Test coverage needed | [Low / Medium / High] | |
| Existing patterns available | [Yes / Partial / No] | |

**Key files likely affected:**
- `[path/to/file1]` -- [what changes here]

### Effort Estimate

| Scenario | Days | Assumption |
|----------|------|------------|
| Optimistic | [X] | Everything goes right, no surprises |
| Expected | [Y] | Normal pace, minor issues, one round of review |
| Pessimistic | [Z] | Significant unknowns surface, blocked for a day |

**Recommended budget: [Y days]**

### Confidence: [High / Medium / Low]

[Explain which factors drive the confidence level for this specific task.]

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

### Dependencies

| Dependency | Status | Impact if Delayed |
|-----------|--------|-------------------|

### Suggested Breakdown

| # | Sub-task | Estimate | Notes |
|---|----------|----------|-------|
| 1 | [Research / spike] | [X days] | |
| 2 | [Core implementation] | [X days] | |
| 3 | [Testing and validation] | [X days] | |
| | **Total** | **[Y days]** | |

### Notes and Assumptions
- [Key assumption that affects the estimate]
- [Any caveats about scope boundaries]
```

输出估算值并附有简短的摘要：建议的预算、置信水平和单一最大的风险因素。

该技能是只读的——不写入任何文件。结论：**完成** — 生成估计值。

---

## 第五阶段：后续步骤

- 如果置信度较低：建议在提交之前进行时间限制峰值 (`/prototype`)。
- 如果任务 > 10 天：建议通过 `/create-stories` 将其分成更小的故事。
- 要安排任务：运行 `/sprint-plan update` 将其添加到下一个冲刺。

### Guidelines

- 始终给出一个范围（乐观/预期/悲观），而不是单个数字
- 建议的预算应该是预期的预算，而不是乐观的预算
- 四舍五入到半天增量 - 以小时为单位进行估算意味着对于长度超过一天的任务精度不准确
- 不要默默地填充估计——明确指出风险，以便团队可以做出决定
