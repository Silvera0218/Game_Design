---
name: story-done
description: "故事结束的完成度审查。读取故事文件，对照实施验证每个验收标准，检查 GDD/ADR 偏差，提示代码审查，将故事状态更新为“完成”，并显示冲刺中的下一个就绪故事。"
---

# 故事完成

这项技能关闭了设计和实现之间的循环。最后运行它
实现任何故事。它确保每个验收标准都经过验证
在故事被标记为完成之前，GDD 和 ADR 偏差是明确的
记录而不是默默地引入，代码审查是提示而不是
忘记了，故事文件反映了实际的完成状态。

**输出：**更新的故事文件（状态：完成）+出现下一个故事。

---

## 第一阶段：寻找故事

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

**如果提供了文件路径**（例如，`/story-done production/epics/core/story-damage-calculator.md`）：
直接读取该文件。

**如果没有提供参数：**

1. 检查 `production/session-state/active.md` 当前活动的故事。
2. 如果在那里找不到，请读取 `production/sprints/` 中的最新文件并
   查找标记为“正在进行”的故事。
3. 如果发现多个正在进行的故事，请使用 `AskUserQuestion`：
   - “我们要完成哪个故事？”
   - 选项：列出正在进行的故事文件名。
4. 如果找不到故事，请要求用户提供路径。

---

## 第 2 阶段：Read 故事

Read 完整的故事文件。提取并保留在上下文中：

- **故事名称和ID**
- **GDD 引用的要求 TR-ID**（例如，`TR-combat-001`）
- **清单版本**嵌入故事标题中（例如，`2026-03-10`）
- **ADR 参考文献** 参考文献
- **验收标准** — 完整列表（每个复选框项目）
- **实现文件** — “create/modify 的文件”下列出的文件
- **故事类型** — 故事标题中的 `Type:` 字段（逻辑/集成/Visual/Feel/UI/Config/Data）
- **引擎注释** — 注明的任何特定于引擎的限制
- **完成的定义** — 如果存在，故事级别的 DoD
- **估计范围与实际范围** - 如果注明了估计值

另请阅读：
- `docs/architecture/tr-registry.yaml` — 查找故事中的每个 TR-ID。
  Read 注册表项中的*当前* `requirement` 文本。这是
  GDD 要求的真实来源 - 不要使用任何要求文本
  可能会在故事中内联引用（可能已经过时）。
- 引用的 GDD 部分 - 只是验收标准和关键规则，而不是
  完整的文档。用它来交叉检查注册表文本是否仍然准确。
- 引用的 ADR(s) — 仅决策和后果部分
- `docs/architecture/control-manifest.md` header — 提取当前
  `Manifest Version:` 日期（用于第 4 阶段陈旧性检查）

---

## 第 3 阶段：验证验收标准

对于故事中的每个验收标准，尝试使用以下之一进行验证
三种方法：

### 自动验证（无需询问即可运行）

- **文件存在检查**：`Glob` 用于故事所说将创建的文件。
- **测试通过检查**：如果提到了测试文件路径，则通过 `Bash` 运行它。
- **没有硬编码值检查**：`Grep` 用于游戏代码中的数字文字
  应该位于配置文件中的路径。
- **没有硬编码字符串检查**：`Grep` 用于 `src/` 中面向玩家的字符串
  这应该在本地化文件中。
- **依赖性检查**：如果条件说“依赖于 X”，则检查 X 是否存在。

### 手动验证并确认（使用 `AskUserQuestion`）

- 关于主观品质的标准（“感觉灵敏”、“动画播放正确”）
- 关于游戏行为的标准（“玩家在……时受到伤害”、“敌人响应……”）
- 性能标准（“Xms 内完成”）——询问是否已分析或接受假设

将最多 4 个手动验证问题批量放入单个 `AskUserQuestion` 调用中：

```
question: "Does [criterion]?"
options: "Yes — passes", "No — fails", "Not tested yet"
```

### 无法验证（无阻塞标记）

- 需要完整的游戏构建来测试的标准（端到端游戏场景）
- 标记为：`DEFERRED — requires playtest session`

### 测试标准可追溯性

完成上述 pass/fail/deferred 检查后，映射每个验收
涵盖它的测试标准：

对于故事中的每个接受标准：

1. 问：是否有测试（单元、集成或确认的手动游戏测试）
   直接验证这个标准？
   - **单元测试**：检查 `tests/unit/` 的测试文件或函数名称
     匹配条件的主题（使用 `Glob` 和 `Grep`）
   - **集成测试**：类似检查`tests/integration/`
   - **手动确认**：如果通过 `AskUserQuestion` 验证标准
     上面有“是 - 通过”答案，将其视为手动测试

2. 生成追溯表：

```
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [criterion text] | tests/unit/test_foo.gd::test_bar | COVERED |
| AC-2: [criterion text] | Manual playtest confirmation | COVERED |
| AC-3: [criterion text] | — | UNTESTED |
```

3. 应用这些升级规则：

   - 如果 **>50% 的标准未经测试**：升级到 **阻止** — 测试
     报道不足以证实故事确实完成。判决结果
     在覆盖范围改善之前，第 6 阶段无法完成。
   - 如果**某些（≤50%）标准未经测试**：保持建议 — 不阻止
     完成，但必须出现在完成注释中。
   - 如果**涵盖所有标准**：除了包括以下内容之外，无需采取任何行动
     报告中的表格。

4. 对于任何未经测试的 ADVISORY 标准，请添加到第 7 阶段的完成注释中：
   `"Untested criteria: [AC-N list]. Recommend adding tests in a follow-up story."`

### 测试证据要求

根据第二阶段提取的故事类型，检查所需的证据：

| 故事类型 | 所需证据 | 门级 |
|---|---|---|
| **Logic** | `tests/unit/[system]/` 中的自动化单元测试 — 必须存在并通过 | BLOCKING |
| **Integration** | `tests/integration/[system]/` 或 playtest 文档中的集成测试 | BLOCKING |
| **Visual/Feel** | `production/qa/evidence/` 中的屏幕截图 + 签核 | ADVISORY |
| **UI** | `production/qa/evidence/` 中的手动演练文档或交互测试 | ADVISORY |
| **Config/Data** | `production/qa/smoke-*.md` 中的烟雾检查通过报告 | ADVISORY |

**对于逻辑故事**：首先阅读故事的**测试证据**部分以提取
确切的所需文件路径。使用 `Glob` 检查该确切路径。如果确切路径不是
找到后，还广泛搜索 `tests/unit/[system]/` （该文件可能已放置在
位置略有不同）。如果在任一位置都找不到测试文件：
- 标记为 **BLOCKING**：“逻辑故事没有单元测试文件。故事需要它
  `[exact-path-from-Test-Evidence-section]`。在标记之前创建并运行测试
  这个故事完成了。”

**对于集成故事**：阅读故事的 **测试证据** 部分以了解确切的信息
所需路径。首先使用 `Glob` 检查确切的路径，然后搜索
`tests/integration/[system]/` 广泛，然后检查 `production/session-logs/` 的
参考这个故事的游戏测试记录。
如果没有找到：标记为 **BLOCKING**（与 Logic 的规则相同）。

**对于 Visual/Feel 和 UI 故事**：文件的 glob `production/qa/evidence/`
参考这个故事。如果没有：标记为 **ADVISORY** —
“未找到手动测试证据。创建 `production/qa/evidence/[story-slug]-evidence.md`
使用测试证据模板并在最终关闭之前获得签字。”

**对于 Config/Data 故事**：检查是否有任何 `production/qa/smoke-*.md` 文件。
如果没有：标记为 **ADVISORY** —“未找到烟雾检查报告。运行 `/smoke-check`。”

**如果未设置故事类型**：标记为 **ADVISORY** —
“未声明故事类型。添加`类型：[逻辑|Integration|Visual/Feel|UI|Config/Data]`
到故事标题，以便在未来的故事中启用测试证据门。”

任何阻塞测试证据差距都会阻止第 6 阶段的完整判决。

---

## 第 4 阶段：检查偏差

将实现与设计文档进行比较。

自动运行这些检查：

1. **GDD 规则检查**：使用 `tr-registry.yaml` 中的当前要求文本
   （通过故事的 TR-ID 查找），检查实施是否反映了什么
   GDD 现在实际上需要 — 而不是故事编写时所需要的。
   `Grep` 关键函数名称、数据结构或类的实现文件
   当前 GDD 部分中提到的名称。

2. **清单版本过时性检查**：比较 `Manifest Version:` 日期
   嵌入故事标题中的 `Manifest Version:` 日期
   当前 `docs/architecture/control-manifest.md` 标头。
   - 如果它们匹配→默默地通过。
   - 如果故事的版本较旧 → 标记为“建议”：
     `建议：故事是根据清单 v[story-date] 编写的；当前舱单
     是 v[current-date]。新规则可能适用。运行 /story-readiness 进行检查。`
   - 如果 control-manifest.md 不存在 → 跳过此检查。

3. **ADR 约束检查**：Read 引用的 ADR 的决策部分。检查
   对于来自 `docs/architecture/control-manifest.md` 的禁止模式（如果它
   存在）。 `Grep` 用于 ADR 中明确禁止的模式。

4. **硬编码值检查**：`Grep` 数字文字的实现文件
   游戏逻辑中的内容应该位于数据文件中。

5. **范围检查**：实施是否涉及故事所述之外的文件
   范围？ （“至 create/modify 的文件”中未列出的文件）

对于发现的每个偏差，进行分类：

- **阻塞** — 实现与 GDD 或 ADR 相矛盾（必须在之前修复）
  标记完成）
- **建议** - 实现与规范略有偏差，但在功能上是可行的
  等效（文档，用户决定）
- **超出范围** - 超出故事所述范围的其他文件被触及
  边界（意识标志——可能有效或范围蔓延）

---

## 阶段 4b：QA 覆盖门

**审查模式检查** — 在生成 QL-TEST-COVERAGE 之前应用：
- `solo` → 跳过。注意：“已跳过 QL-TEST-COVERAGE — 独奏模式。”进入第 5 阶段。
- `lean` → 跳过（不是相位门）。注意：“已跳过 QL-TEST-COVERAGE — 精益模式。”进入第 5 阶段。
- `full` → 正常生成。

完成阶段 4 中的偏差检查后，使用门 **QL-TEST-COVERAGE** (`.codex/docs/director-gates.md`) 通过 Task 生成 `qa-lead`。

Pass:
- 故事文件路径和故事类型
- 测试在第 3 阶段找到的文件路径（确切路径，或“未找到”）
- 故事的 `## QA Test Cases` 部分（故事创建中预先编写的测试规范）
- 故事的 `## Acceptance Criteria` 列表

质量保证负责人会审查测试是否真正涵盖了指定的内容，而不仅仅是文件是否存在。

执行判决：
- **足够** → 进入第 5 阶段
- **差距** → 标记为 **ADVISORY**：“QA 领导确定了覆盖范围差距：[list]。故事可以完成，但应在后续故事中解决差距。”
- **不充分**→标记为**阻止**：“QA 领先：关键逻辑未经测试。在覆盖范围改善之前，判决无法完成。具体差距：[list]。”

对于 Config/Data 故事，请跳过此阶段（无需进行代码测试）。

---

## 第 5 阶段：首席程序员代码审查门

**审查模式检查** — 在生成 LP-CODE-REVIEW 之前应用：
- `solo` → 跳过。注意：“LP-CODE-REVIEW 已跳过 — Solo 模式。”继续进行第 6 阶段（完成报告）。
- `lean` → 跳过（不是相位门）。注意：“LP-CODE-REVIEW 已跳过 — 精益模式。”继续进行第 6 阶段（完成报告）。
- `full` → 正常生成。

使用门 **LP-CODE-REVIEW** (`.codex/docs/director-gates.md`) 通过 Task 生成 `lead-programmer`。

通过：实现文件路径、故事文件路径、相关GDD部分，管理ADR。

将判决结果呈现给用户。如果有疑虑，请通过 `AskUserQuestion` 提出：
- 选项：`Revise flagged issues` / `Accept and proceed` / `Discuss further`
如果拒绝，请在问题解决之前不要继续进行第 6 阶段的裁决。

如果故事还没有实现文件（编码完成之前正在运行判决），请跳过此阶段并注意：“LP-CODE-REVIEW 已跳过 - 未找到实现文件。实现完成后运行。”

---

## 第六阶段：提交完成报告

在更新任何文件之前，请提供完整的报告：

```markdown
## Story Done: [Story Name]
**Story**: [file path]
**Date**: [today]

### Acceptance Criteria: [X/Y passing]
- [x] [Criterion 1] — auto-verified (test passes)
- [x] [Criterion 2] — confirmed
- [ ] [Criterion 3] — FAILS: [reason]
- [?] [Criterion 4] — DEFERRED: requires playtest

### Test-Criterion Traceability
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [text] | [test file::test name] | COVERED |
| AC-2: [text] | Manual confirmation | COVERED |
| AC-3: [text] | — | UNTESTED |

### Test Evidence
**Story Type**: [Logic | Integration | Visual/Feel | UI | Config/Data | Not declared]
**Required evidence**: [unit test file | integration test or playtest | screenshot + sign-off | walkthrough doc | smoke check pass]
**Evidence found**: [YES — `[path]` | NO — BLOCKING | NO — ADVISORY]

### Deviations
[NONE] OR:
- BLOCKING: [description] — [GDD/ADR reference]
- ADVISORY: [description] — user accepted / flagged for tech debt

### Scope
[All changes within stated scope] OR:
- Extra files touched: [list] — [note whether valid or scope creep]

### Verdict: COMPLETE / COMPLETE WITH NOTES / BLOCKED
```

**判决定义：**
- **完成**：所有标准均通过，无阻塞偏差
- **附注完整**：所有标准均通过，建议偏差已记录
- **被阻止**：必须首先解决失败的标准或阻止偏差

如果判决为 **BLOCKED**：请勿继续进行第 7 阶段。列出必须执行的操作
固定。主动提出帮助修复阻塞项目。

---

## 第 7 阶段：更新故事状态

写作前询问：“我可以更新故事文件以将其标记为完成并记录吗
完成笔记？”

如果是，请编辑故事文件：

1. 更新状态字段：`Status: Complete`
2. 在底部添加 `## Completion Notes` 部分：

```markdown
## Completion Notes
**Completed**: [date]
**Criteria**: [X/Y passing] ([any deferred items listed])
**Deviations**: [None] or [list of advisory deviations]
**Test Evidence**: [Logic: test file at path | Visual/Feel: evidence doc at path | None required (Config/Data)]
**Code Review**: [Pending / Complete / Skipped]
```

3. 如果存在建议偏差，请询问：“我应该将这些作为技术债务记录在案吗？
   `docs/tech-debt-register.md`？”

4. **更新`production/sprint-status.yaml`**（如果存在）：
   - 查找与该故事的文件路径或 ID 匹配的条目
   - 设置 `status: done` 和 `completed: [today's date]`
   - 更新顶级 `updated` 字段
   - 这是静默更新 - 无需额外批准（已在上述步骤中批准）

### 会话状态更新

更新故事文件后，静默追加到
`production/session-state/active.md`:

## 会话摘录 — /story-done [date]
    - 判决：[COMPLETE / COMPLETE WITH NOTES / BLOCKED]
    - 故事：[story file path] — [story title]
    - 记录的技术债务：[N 项，或“无”]
    - 下一个推荐：[下一个准备好的故事标题和路径，或“未识别”]

如果`active.md`不存在，则以此块为初始内容创建它。
在对话中确认：“会话状态已更新。”

---

## 第 8 阶段：揭示下一个故事

完成后，帮助开发者保持动力：

1. Read `production/sprints/` 的当前冲刺计划。
2. 查找以下故事：
   - 状态：准备好或未开始
   - 没有被其他不完整的故事阻挡
   - 属于必须拥有或应该拥有的级别

Present:

```
### Next Up
The following stories are ready to pick up:
1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `/story-readiness [path]` to confirm a story is implementation-ready
before starting.
```

如果此冲刺中不再有必须有的故事（所有故事都已完成或已阻止）：

```
### Sprint Close-Out Sequence

All Must Have stories are complete. QA sign-off is required before advancing.
Run these in order:

1. `/smoke-check sprint` — verify the critical path still works end-to-end
2. `/team-qa sprint` — full QA cycle: test case execution, bug triage, sign-off report
3. `/gate-check` — advance to the next phase once QA approves

Do not run `/gate-check` until `/team-qa` returns APPROVED or APPROVED WITH CONDITIONS.
```

如果有“应该有”的故事仍未开始，请将它们与结束序列一起显示，以便用户可以选择：立即结束冲刺，或先拉入更多工作。

如果没有更多故事准备就绪，但必备故事仍在进行中（未完成）：
“没有更多故事可以开始 - [N] 必须有故事仍在进行中。在冲刺结束之前继续实施这些故事。”

---

## 协作协议

- **未经用户批准，切勿将故事标记为完整** - 第 7 阶段需要
  在编辑任何文件之前明确“是”。
- **永远不要自动修复失败的标准** - 报告它们并询问该怎么做。
- **偏差是事实，而不是判断**——中立地呈现它们；用户
  决定它们是否可以接受。
- **BLOCKED 判决是建议性的** — 用户可以覆盖并标记为完成
  无论如何；如果这样做，请明确记录风险。
- 使用 `AskUserQuestion` 作为代码审查提示和批处理手册
  标准确认。

---

## 建议的后续步骤

- 在开始实施之前运行 `/story-readiness [next-story-path]` 以验证下一个故事
- 如果所有必备故事均已完成：运行 `/smoke-check sprint` → `/team-qa sprint` → `/gate-check`
- 如果记录了技术债务：通过 `/tech-debt` 进行跟踪以保持寄存器最新
