---
name: team-qa
description: "协调 QA 团队完成整个测试周期。协调 qa-lead（策略 + 测试计划）和 qa-tester（测试用例编写 + bug 报告），为冲刺或功能生成完整的 QA 包。涵盖：测试计划生成、测试用例编写、烟雾检查门、手动 QA 执行和签核报告。"
---

调用此技能时，通过结构化测试周期协调 QA 团队。

**决策点：** 在每个阶段转换时，使用 `AskUserQuestion` 来呈现
用户将子代理的建议作为可选择的选项。 Write 代理的
在对话中进行全面分析，然后用简洁的标签捕捉决策。
用户必须批准才能进入下一阶段。

## 团队构成

- **qa-lead** — QA 策略、测试计划生成、故事分类、签核报告
- **qa-tester** — 测试用例编写、错误报告编写、手册 QA 文档

## 如何委派

使用 Task 工具将每个团队成员生成为子代理：
- `subagent_type: qa-lead` — 策略、规划、分类、签署
- `subagent_type: qa-tester` — 测试用例编写和错误报告编写

始终在每个代理的提示中提供完整的上下文（故事文件路径、QA 计划路径、范围约束）。尽可能并行启动独立的质量保证测试人员任务（例如，可以同时搭建第 5 阶段的多个故事）。

## Pipeline

### 第一阶段：加载上下文

在做任何其他事情之前，先收集完整的范围：

1. 从参数中检测当前的冲刺或功能范围：
   - 如果参数是 sprint 标识符（例如 `sprint-03`）：读取 `production/sprints/[sprint]/` 中的所有故事文件
   - 如果参数是 `feature: [system-name]`：为该系统标记的 glob 故事文件
   - 如果没有参数：读取 `production/session-state/active.md` 和 `production/sprint-status.yaml`（如果存在）以推断活动冲刺

2. Read `production/stage.txt` 确认当前项目阶段。

3. 统计找到的故事并向用户报告：
   > “QA 周期从 [sprint/feature] 开始。找到 [N] 故事。当前阶段：[stage]。准备好开始 QA 策略了吗？”

### 第 2 阶段：QA 策略（qa 主导）

通过 Task 生成 `qa-lead`，以审查所有范围内的故事并生成 QA 策略。

提示质量保证人员：
- Read 每个故事文件
- 按类型对每个故事进行分类：**逻辑** / **集成** / **Visual/Feel** / **UI** / **Config/Data**
- 确定哪些故事需要自动测试证据与手动测试 QA
- 标记任何缺少验收标准或缺少测试证据的故事，这些故事会阻止 QA
- 估计手动 QA 工作量（所需的测试会话数）
- 检查 `tests/smoke/` 的烟雾测试场景；对于每个，评估是否可以在当前版本的情况下进行验证。生成烟雾检查结论：**通过** / **通过但带有警告 [list]** / **失败 [list of failures]**
- 生成策略汇总表和烟雾检查结果：

  | Story | Type | 需要自动化 | 需要手册 | 拦截器？ |
  |-------|------|--------------------|-----------------|----------|

  **烟雾检查**：[PASS / PASS WITH WARNINGS / FAIL] — [details if not PASS]

如果烟雾检查结果为 **FAIL**，则 qa 领导必须突出列出失败。 QA 在烟雾检查失败的情况下无法继续通过策略阶段。

向用户展示 qa-lead 的完整策略，然后使用 `AskUserQuestion`：

```
question: "QA Strategy Review"
options:
  - "Looks good — proceed to test plan"
  - "Adjust story types before proceeding"
  - "Skip blocked stories and proceed with the rest"
  - "Smoke check failed — fix issues and re-run /team-qa"
  - "Cancel — resolve blockers first"
```

如果冒烟检查**失败**：不要继续进行第 3 阶段。找出故障并停止。用户必须修复它们并重新运行 `/team-qa`。
如果烟雾检查**通过但有警告**：记下签核报告的警告并继续。
如果存在阻碍：明确列出它们。用户可以选择跳过被阻止的故事或取消循环。

### 第 3 阶段：测试计划生成

使用第二阶段的策略，生成结构化测试计划文档。

测试计划应涵盖：
- **范围**：sprint/feature 名称、故事数、日期
- **故事分类表**：来自第二阶段策略
- **自动化测试要求**：哪些故事需要测试文件，`tests/` 中的预期路径
- **手动 QA 范围**：哪些故事需要手动演练以及需要验证哪些内容
- **超出范围**：本周期明确未测试的内容以及原因
- **进入标准**：在 QA 开始之前必须满足什么条件（烟雾检查通过，构建稳定）
- **退出标准**：完整的 QA 周期的构成是什么（所有案例通过或失败，并提交错误）

问：“我可以将QA计划写入`production/qa/qa-plan-[sprint]-[date].md`吗？”

Write 仅在获得批准后。

### 第 4 阶段：测试用例编写 (qa-tester)

> **烟雾检查**作为第 2 阶段（QA 策略）的一部分执行。如果烟雾检查在第 2 阶段返回“失败”，则循环将在此处停止。仅当第 2 阶段烟雾检查通过或通过但有警告时才运行此阶段。

对于需要手动 QA 的每个故事（Visual/Feel、UI、无需自动化测试的集成）：

通过 Task 为每个故事生成 `qa-tester`（如果可能，并行运行），提供：
- 故事文件路径
- QA 计划中该故事的相关部分
- 正在测试的系统的 GDD 验收标准（如果有）
- 编写涵盖所有验收标准的详细测试用例的说明

每个测试用例集应包括：
- **先决条件**：测试开始前所需的游戏状态
- **步骤**：编号、明确的操作
- **预期结果**：应该发生什么
- **实际结果**：字段留空供测试人员填写
- **Pass/Fail**：字段留空

在执行之前将测试用例呈现给用户进行审查。按故事分组。

每个故事组使用 `AskUserQuestion`（一次批处理 3-4 个）：

```
question: "Test cases ready for [Story Group]. Review before manual QA begins?"
options:
  - "Approved — begin manual QA for these stories"
  - "Revise test cases for [story name]"
  - "Skip manual QA for [story name] — not ready"
```

### 第 6 阶段：手动 QA 执行

浏览经批准的手册 QA 列表中的每个故事。

将故事分成 3-4 组，并为每个组使用 `AskUserQuestion`：

```
question: "Manual QA — [Story Title]\n[brief description of what to test]"
options:
  - "PASS — all acceptance criteria verified"
  - "PASS WITH NOTES — minor issues found (describe after)"
  - "FAIL — criteria not met (describe after)"
  - "BLOCKED — cannot test yet (reason)"
```

每次 FAIL 结果后：使用 `AskUserQuestion` 收集失败描述，然后通过 Task 生成 `qa-tester`，在 `production/qa/bugs/` 中编写正式的错误报告。

错误报告命名：`BUG-[NNN]-[short-slug].md`（从目录中的现有错误增量 NNN）。

收集完所有结果后，总结一下：
- 故事通过：[count]
- 故事通过并附有注释：[count]
- 故事失败：[count] — 提交的错误：[IDs]
- 故事被阻止：[count]

### 第 7 阶段：QA 签署报告

通过 Task 生成 `qa-lead`，以使用阶段 4-6 的所有结果生成签核报告。

签核报告格式：

```markdown
## QA Sign-Off Report: [Sprint/Feature]
**Date**: [date]
**QA Lead sign-off**: [pending]

### Test Coverage Summary
| Story | Type | Auto Test | Manual QA | Result |
|-------|------|-----------|-----------|--------|
| [title] | Logic | PASS | — | PASS |
| [title] | Visual | — | PASS | PASS |

### Bugs Found
| ID | Story | Severity | Status |
|----|-------|----------|--------|
| BUG-001 | [story] | S2 | Open |

### Verdict: APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED

**Conditions** (if any): [list what must be fixed before the build advances]

### Next Step
[guidance based on verdict]
```

判决规则：
- **批准**：所有故事均通过或通过注释；没有打开 S1/S2 错误
- **有条件批准**：S3/S4 错误已打开，或已记录问题通过；没有 S1/S2 错误
- **未批准**：任何 S1/S2 错误已打开；或故事在没有记录的解决方法的情况下失败

通过判决进行下一步指导：
- 已批准：“构建已为下一阶段做好准备。运行 `/gate-check` 来验证进度。”
- 有条件批准：“在前进之前解决条件。S3/S4 错误可能会推迟修复。”
- 未批准：“解决 S1/S2 错误并重新运行 `/team-qa` 或目标手册 QA，然后再继续。”

问：“我可以将这份 QA 签核报告写给 `production/qa/qa-signoff-[sprint]-[date].md` 吗？”

Write 仅在获得批准后。

## 错误恢复协议

如果任何生成的代理（通过 Task）返回 BLOCKED、错误或无法完成：

1. **立即浮出水面**：在继续依赖阶段之前向用户报告“[AgentName]：BLOCKED — [reason]”
2. **评估依赖关系**：检查后续阶段是否需要被阻止的代理的输出。如果是，则在没有用户输入的情况下不要继续越过该依赖点。
3. **通过 AskUserQuestion 提供选项**，可选择：
   - 跳过此代理并注意最终报告中的差距
   - 以更窄的范围重试
   - 停在这里并首先解决阻止程序
4. **始终生成部分报告** — 输出已完成的内容。切勿因为一名代理阻塞而放弃工作。

常见的拦截器：
- 输入文件丢失（未找到故事，GDD 不存在）→ 重定向到创建它的技能
- ADR 状态为建议 → 不实施；首先运行 `/architecture-decision`
- 范围太大 → 通过 `/create-stories` 分成两个故事
- ADR 和故事之间的指令冲突 → 冲突浮出水面，不要猜测

## Output

摘要涵盖：范围内的故事、烟雾检查结果、手动 QA 结果、提交的错误（包含 ID 和严重性）以及最终批准/有条件批准/未批准判决。

结论：**完成** — QA 周期完成。
结论： **阻塞** — 烟雾检查失败或关键阻塞程序阻止循环完成；产生了部分报告。
