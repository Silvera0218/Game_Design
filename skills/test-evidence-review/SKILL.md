---
name: test-evidence-review
description: "测试文件和手动证据文件的质量审查。超越存在性检查——评估断言覆盖率、边缘情况处理、命名约定和证据完整性。每个故事生成 ADEQUATE/INCOMPLETE/MISSING 判决。在 QA 签核之前或​​按需运行。"
---

# 测试证据审查

`/smoke-check` 验证测试文件**存在**并且**通过**。这个技能
更进一步——它审查这些测试和证据文件的**质量**。
存在并通过的测试文件可能仍会留下未发现的关键行为。
现有的手动证据文档可能缺乏结束所需的签字。

**输出：** 摘要报告（对话中）+可选 `production/qa/evidence-review-[date].md`

**何时运行：**
- QA 移交签核之前（`/team-qa` 第 5 阶段）
- 关于任何测试质量有问题的故事
- 作为逻辑和集成故事质量审核里程碑审核的一部分

---

## 1. 解析参数

**Modes:**
- `/test-evidence-review [story-path]` — 审查单个故事的证据
- `/test-evidence-review sprint` — 查看当前冲刺中的所有故事
- `/test-evidence-review [system-name]` — 查看 epic/system 中的所有故事
- 没有争论 - 询问哪个范围：“单个故事”，“当前冲刺”，“一个系统”

---

## 2. 在范围内加载故事

基于论证：

**单个故事**：Read 直接故事文件。摘录：故事类型，测试
证据部分、故事片段、系统名称。

**Sprint**：Read `production/sprints/` 中最近修改的文件。
从冲刺计划中提取故事文件路径列表。 Read 每个故事文件。

**系统**：Glob `production/epics/[system-name]/story-*.md`。 Read 每个。

对于每个故事，收集：
- `Type:` 字段（逻辑/集成/Visual/Feel / UI / Config/Data）
- `## Test Evidence` 部分 — 指定的预期测试文件路径或证据文档
- 故事片段（来自文件名）
- 系统名称（来自目录路径）
- 验收标准列表（所有复选框项目）

---

## 3. 找到证据文件

对于每个故事，找到证据：

**逻辑故事**：Glob `tests/unit/[system]/[story-slug]_test.*`
  - 如果没有找到，还可以尝试：Grep in `tests/unit/[system]/` for files
    包含故事片段

**集成故事**：Glob `tests/integration/[system]/[story-slug]_test.*`
  - 另请检查 `production/session-logs/` 中提及故事的游戏测试记录

**Visual/Feel 和 UI 故事**：Glob `production/qa/evidence/[story-slug]-evidence.*`

**Config/Data 故事**：Glob `production/qa/smoke-*.md`（任何烟雾检查报告）

记下每个故事找到的内容（路径）或未找到的内容（差距）。

---

## 4.审查自动化测试质量（逻辑/集成）

对于找到的每个测试文件，读取它并评估：

### 断言覆盖率

计算不同断言的数量（包含断言、期望、
检查、验证或特定于引擎的断言模式）。低断言计数是
质量信号 - 每个测试函数仅做出 1 个断言的测试可能
不涵盖预期行为的范围。

Thresholds:
- **每个测试函数有 3 个以上断言** → 正常
- **每个测试函数 1-2 个断言** → 注意可能很薄
- **0 个断言**（测试存在但没有断言）→ 标记为 BLOCKING —
  测试空洞地通过并且什么也没证明

### 边缘情况覆盖

对于故事中包含数字、阈值的每个接受标准，
或“当 X 发生时”条件：检查测试函数名称或
测试机构引用该特定案例。

Heuristics:
- Grep 测试文件“zero”、“max”、“null”、“empty”、“min”、“invalid”、
  “boundary”、“edge” — 任何一个的存在都是一个积极的信号
- 如果故事有一个具有特定范围的公式部分：检查是否
  以 minimum/maximum 值进行测试练习

### 命名质量

测试函数名称应描述：场景+预期结果。
图案：`test_[scenario]_[expected_outcome]`

将通用命名的函数（`test_1`、`test_run`、`testBasic`）标记为
**命名问题** - 它们使故障更难以诊断。

### 配方可追溯性

对于 GDD 具有公式部分的逻辑故事：检查测试是否正确
文件至少包含一个测试，其名称或注释引用了公式
名称或公式值。练习公式而不提及的测试
当公式改变时，它的名字就更难维护。

---

## 5.审查手册证据质量（Visual/Feel / UI）

对于找到的每份证据文件，阅读并评估：

### 标准联动

证据文件应引用故事中的每项验收标准。
检查：证据文档是否包含每个标准（或明确的措辞）？
缺少标准意味着标准从未得到验证。

### 签核完整性

检查三个签核行（或等效字段）：
- 开发人员签核
- 设计师/艺术主管签字（适用于 Visual/Feel）
- QA 领导签核

如果有任何缺失或空白：标记为不完整 - 故事无法完整
在没有所有必需的签字的情况下关闭。

### 截图/工件完整性

对于Visual/Feel故事：检查是否引用了截图文件路径
在证据文件中。如果被引用，Glob 用于确认它们存在。

对于 UI 故事：检查演练序列（逐步交互
日志）存在。

### 日期覆盖范围

证据文件应该有日期。如果日期早于故事的日期
最后一次重大变更（启发式：与冲刺开始日期进行比较
计划），标记为“可能过时”——证据可能无法涵盖最终结果
implementation.

---

## 6. 构建审核报告

对于每个故事，指定一个结论：

| Verdict | Meaning |
|---------|---------|
| **ADEQUATE** | Test/evidence 存在，通过质量检查，涵盖所有标准 |
| **INCOMPLETE** | Test/evidence 存在，但存在质量差距（断言薄弱，缺少签核） |
| **MISSING** | 没有找到需要它的故事类型的测试或证据 |

总体 sprint/system 判决是目前最糟糕的故事判决。

```markdown
## Test Evidence Review

> **Date**: [date]
> **Scope**: [single story path | Sprint [N] | [system name]]
> **Stories reviewed**: [N]
> **Overall verdict**: ADEQUATE / INCOMPLETE / MISSING

---

### Story-by-Story Results

#### [Story Title] — [Type] — [ADEQUATE/INCOMPLETE/MISSING]

**Test/evidence path**: `[path]` (found) / (not found)

**Automated test quality** *(Logic/Integration only)*:
- Assertion coverage: [N per function on average] — [adequate / thin / none]
- Edge cases: [covered / partial / not found]
- Naming: [consistent / [N] generic names flagged]
- Formula traceability: [yes / no — formula names not referenced in tests]

**Manual evidence quality** *(Visual/Feel/UI only)*:
- Criterion linkage: [N/M criteria referenced]
- Sign-offs: [Developer ✓ | Designer ✗ | QA Lead ✗]
- Artefacts: [screenshots present / missing / N/A]
- Freshness: [dated [date] — current / potentially stale]

**Issues**:
- BLOCKING: [description] *(prevents story-done)*
- ADVISORY: [description] *(should fix before release)*

---

### Summary

| Story | Type | Verdict | Issues |
|-------|------|---------|--------|
| [title] | Logic | ADEQUATE | None |
| [title] | Integration | INCOMPLETE | Thin assertions (avg 1.2/function) |
| [title] | Visual/Feel | INCOMPLETE | QA lead sign-off missing |
| [title] | Logic | MISSING | No test file found |

**BLOCKING items** (must resolve before story can be closed): [N]
**ADVISORY items** (should address before release): [N]
```

---

## 7. Write 输出（可选）

在对话中展示报告。

问：“我可以将此测试证据审查写给
`production/qa/evidence-review-[date].md`？”

这是可选的——该报告独立有用。 Write 仅当用户
想要一个持久的记录。

报告后：

- 对于 BLOCKING 项目：“必须先解决这些问题，然后 `/story-done` 才能标记
  故事完成。您现在想对他们中的任何一个讲话吗？”
- 对于薄断言：“考虑运行 `/test-helpers [system]` 来查看
  常见情况的脚手架断言模式。”
- 对于缺少签核：“需要 [role] 进行手动签核。分享
  `[evidence-path]` 与他们一起完成签核。”

结论：**完成**——证据审查已完成。如果发现阻塞项目，请使用关注。

---

## 协作协议

- **报告质量问题，而不是修复它们** - 该技能读取和评估；
  它不会修改测试文件或证据文件
- **足够意味着足以运输，但不完美** - 避免挑剔
  功能齐全且全面的测试足以给人信心
- **BLOCKING 与 ADVISORY 的区别很重要** — 仅在以下情况下标记 BLOCKING：
  这一差距留下了一个真正未经验证的故事标准
- **写作前询问**——报告文件是可选的；写作前务必确认
