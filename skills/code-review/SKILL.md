---
name: code-review
description: "对指定文件或文件集执行体系结构和质量代码审查。检查编码标准合规性、架构模式遵守情况、SOLID 原则、可测试性和性能问题。"
---

## 第 1 阶段：加载目标文件

Read 完整的目标文件。 Read AGENTS.md 用于项目编码标准。

---

## 第 2 阶段：确定发动机专家

Read `.codex/docs/technical-preferences.md`，`## Engine Specialists` 部分。注意：

- **主要**专家（用于架构和广泛的引擎问题）
- **Language/Code 专家**（在审查项目的主要语言文件时使用）
- **着色器专家**（在检查着色器文件时使用）
- **UI 专家**（在审查 UI 代码时使用）

如果该部分显示为 `[TO BE CONFIGURED]`，则表示没有固定任何引擎 - 跳过引擎专家步骤。

---

## 第 3 阶段：ADR 合规性检查

在故事文件、提交消息和标题注释中搜索 ADR 引用。查找类似 `ADR-NNN` 或 `docs/architecture/ADR-` 的模式。

如果未找到 ADR 引用，请注意：“未找到 ADR 引用 — 跳过 ADR 合规性检查。”

对于每个引用的 ADR：读取文件，提取 **Decision** 和 **Consequences** 部分，然后对任何偏差进行分类：

- **架构违规**（阻止）：使用 ADR 中明确拒绝的模式
- **ADR DRIFT**（警告）：在不使用禁止模式的情况下明显偏离所选方法
- **轻微偏差**（信息）：与 ADR 指南略有差异，不会影响整体架构

---

## 第四阶段：标准合规

确定系统类别（引擎、游戏玩法、AI、网络、UI、工具）并评估：

- [ ] 公共方法和类有文档注释
- [ ] 每个方法的圈复杂度低于 10
- [ ] 没有方法超过 40 行（不包括数据声明）
- [ ] 注入依赖项（游戏状态没有静态单例）
- [ ] 从数据文件加载的配置值
- [ ] 系统公开接口（不是具体的类依赖项）

---

## 第 5 阶段：架构和 SOLID

**Architecture:**
- [ ] 正确的依赖方向（引擎 <- 游戏玩法，而不是反向）
- [ ] 模块之间没有循环依赖关系
- [ ] 适当的层分离（UI 不拥有游戏状态）
- [ ] Events/signals 用于跨系统通信
- [ ] 与代码库中既定的模式一致

**SOLID:**
- [ ] 单一职责：每个类都有一个改变的理由
- [ ] Open/Closed：无需修改即可扩展
- [ ] 里氏替换：可替换基本类型的子类型
- [ ] 接口隔离：无胖接口
- [ ] 依赖倒置：依赖于抽象，而不是具体

---

## 第 6 阶段：特定于游戏的问题

- [ ] 帧速率独立性（增量时间使用）
- [ ] 热路径中没有分配（更新循环）
- [ ] 正确的 null/empty 状态处理
- [ ] 需要时的线程安全
- [ ] 资源清理（无泄漏）

---

## 第 7 阶段：专家评审（并行）

通过 Task 同时生成所有适用的专家 - 不要等待一个专家才开始下一个。

### 发动机专家

如果配置了引擎，请确定哪个专家适用于每个文件并并行生成：

- 主要语言文件（`.gd`、`.cs`、`.cpp`）→ Language/Code 专家
- 着色器文件（`.gdshader`、`.hlsl`、着色器图）→ 着色器专家
- UI screen/widget 代码 → UI 专家
- 交叉或不清楚 → 主要专家

还为任何文件接触引擎架构（场景结构、节点层次结构、生命周期挂钩）生成**主要专家**。

### QA 可测试性审查

对于逻辑和集成故事，还通过 Task 与引擎专家并行生成 `qa-tester`。通过：
- 正在审查实施文件
- 故事的 `## QA Test Cases` 部分（来自 qa-lead 的预先编写的测试规范）
- 故事的`## Acceptance Criteria`

请质量保证测试人员评估：
- [ ] 所有测试挂钩和接口是否都公开（未隐藏在 private/internal 访问后面）？
- [ ] 故事 `## QA Test Cases` 部分中的 QA 测试用例是否映射到可测试的代码路径？
- [ ] 实施时是否存在无法测试的验收标准（例如，硬编码值、无注入缝）？
- [ ] 该实现是否引入了现有 QA 测试用例未涵盖的任何新边缘情况？
- [ ] 是否有任何明显的副作用应该进行测试但没有进行？

对于 Visual/Feel 和 UI 故事：qa-tester 检查 `## QA Test Cases` 中的手动验证步骤是否可以通过所编写的实现来实现 - 例如，“手动检查器需要达到的状态是否实际上可以达到？”

在产生输出之前收集所有专家的发现。

---

## 第 8 阶段：输出审核

```
## Code Review: [File/System Name]

### Engine Specialist Findings: [N/A — no engine configured / CLEAN / ISSUES FOUND]
[Findings from engine specialist(s), or "No engine configured." if skipped]

### Testability: [N/A — Visual/Feel or Config story / TESTABLE / GAPS / BLOCKING]
[qa-tester findings: test hooks, coverage gaps, untestable paths, new edge cases]
[If BLOCKING: implementation must expose [X] before tests in ## QA Test Cases can run]

### ADR Compliance: [NO ADRS FOUND / COMPLIANT / DRIFT / VIOLATION]
[List each ADR checked, result, and any deviations with severity]

### Standards Compliance: [X/6 passing]
[List failures with line references]

### Architecture: [CLEAN / MINOR ISSUES / VIOLATIONS FOUND]
[List specific architectural concerns]

### SOLID: [COMPLIANT / ISSUES FOUND]
[List specific violations]

### Game-Specific Concerns
[List game development specific issues]

### Positive Observations
[What is done well -- always include this section]

### Required Changes
[Must-fix items before approval — ARCHITECTURAL VIOLATIONs always appear here]

### Suggestions
[Nice-to-have improvements]

### Verdict: [APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED]
```

该技能是只读的——不写入任何文件。

---

## 第 9 阶段：后续步骤

- 如果判决被批准：运行 `/story-done [story-path]` 来结束故事。
- 如果结论是需要更改：修复问题并重新运行 `/code-review`。
- 如果发现架构违规：运行 `/architecture-decision` 记录正确的方法。
