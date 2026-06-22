---
name: bug-report
description: "根据描述创建结构化错误报告，或分析代码以识别潜在错误。确保每个错误报告都有完整的重现步骤、严重性评估和上下文。"
---

## 第一阶段：解析参数

从参数确定模式：

- 无关键字 → **描述模式**：根据提供的描述生成结构化错误报告
- `analyze [path]` → **分析模式**：读取目标文件并识别潜在的错误
- `verify [BUG-ID]` → **验证模式**：确认报告的修复确实解决了错误
- `close [BUG-ID]` → **关闭模式**：将已验证的错误标记为已关闭并带有解决记录

如果未提供参数，请在继续之前询问用户错误描述。

---

## 阶段 2A：描述模式

1. **解析描述**以获取关键信息：什么问题、何时、如何重现以及预期的行为是什么。

2. **使用 Grep/Glob 搜索代码库**相关文件以添加上下文（受影响的系统，可能的文件）。

3. **起草错误报告**：

```markdown
# Bug Report

## Summary
**Title**: [Concise, descriptive title]
**ID**: BUG-[NNNN]
**Severity**: [S1-Critical / S2-Major / S3-Minor / S4-Trivial]
**Priority**: [P1-Immediate / P2-Next Sprint / P3-Backlog / P4-Wishlist]
**Status**: Open
**Reported**: [Date]
**Reporter**: [Name]

## Classification
- **Category**: [Gameplay / UI / Audio / Visual / Performance / Crash / Network]
- **System**: [Which game system is affected]
- **Frequency**: [Always / Often (>50%) / Sometimes (10-50%) / Rare (<10%)]
- **Regression**: [Yes/No/Unknown -- was this working before?]

## Environment
- **Build**: [Version or commit hash]
- **Platform**: [OS, hardware if relevant]
- **Scene/Level**: [Where in the game]
- **Game State**: [Relevant state -- inventory, quest progress, etc.]

## Reproduction Steps
**Preconditions**: [Required state before starting]

1. [Exact step 1]
2. [Exact step 2]
3. [Exact step 3]

**Expected Result**: [What should happen]
**Actual Result**: [What actually happens]

## Technical Context
- **Likely affected files**: [List of files based on codebase search]
- **Related systems**: [What other systems might be involved]
- **Possible root cause**: [If identifiable from the description]

## Evidence
- **Logs**: [Relevant log output if available]
- **Visual**: [Description of visual evidence]

## Related Issues
- [Links to related bugs or design documents]

## Notes
[Any additional context or observations]
```

---

## 阶段 2B：分析模式

1. **Read 参数中指定的目标文件**。

2. **识别潜在的错误**：空引用、相差一错误、竞争条件、未处理的边缘情况、资源泄漏、不正确的状态转换。

3. **对于每个潜在的错误**，使用上面的模板生成错误报告，并填写可能的触发场景和建议的修复。

---

## 阶段 2C：验证模式

Read `production/qa/bugs/[BUG-ID].md`。提取重现步骤和预期结果。

1. **重新运行重现步骤** — 使用 Grep/Glob 检查根本原因代码路径是否仍然存在，如所述。如果修复程序删除或更改了它，请记下更改。
2. **运行相关测试** — 如果 bug 的系统在 `tests/` 中有测试文件，则通过 Bash 运行它并报告 pass/fail.
3. **检查回归** — grep 代码库以查找导致错误的模式的任何新出现。

产生验证结论：

- **已验证已修复** - 复制步骤不再产生错误；相关测试通过
- **仍然存在** — 错误按照描述重现；修复并没有解决问题
- **无法验证** — 自动检查没有结论；需要手动游戏测试

问：“我可以更新 `production/qa/bugs/[BUG-ID].md` 以设置状态：已验证已修复/仍然存在/无法验证吗？”

如果仍然存在：重新打开错误，将状态设置回打开，并建议重新运行 `/hotfix [BUG-ID]`。

---

## 第 2D 阶段：关闭模式

Read `production/qa/bugs/[BUG-ID].md`。关闭前确认状态为 `Verified Fixed`。如果状态为其他任何内容，请停止：“必须先验证修复错误 [ID]，然后才能关闭。首先运行 `/bug-report verify [BUG-ID]`。”

将关闭记录附加到错误文件中：

```markdown
## Closure Record
**Closed**: [date]
**Resolution**: Fixed — [one-line description of what was changed]
**Fix commit / PR**: [if known]
**Verified by**: qa-tester
**Closed by**: [user]
**Regression test**: [test file path, or "Manual verification"]
**Status**: Closed
```

将顶级 `**Status**: Open` 字段更新为 `**Status**: Closed`。

问：“我可以更新 `production/qa/bugs/[BUG-ID].md` 以将其标记为已关闭吗？”

关闭后，检查 `production/qa/bug-triage-*.md` — 如果该错误出现在打开的分类报告中，请注意：“分类报告中引用了错误 [ID]。运行 `/bug-triage` 以刷新打开的错误计数。”

---

## 第三阶段：保存报告

向用户呈现已完成的错误报告。

问：“我可以把这个写到`production/qa/bugs/BUG-[NNNN].md`吗？”

如果是，则写入文件，并根据需要创建目录。结论：**完成** — 已提交错误报告。

如果没有，就停在这里。结论：**被阻止**——用户拒绝写入。

---

## 第四阶段：后续步骤

保存后，根据模式建议：

**归档后（Description/Analyze模式）：**
- 运行 `/bug-triage` 以与现有的未解决错误一起确定优先级
- 如果是 S1 或 S2：运行 `/hotfix [BUG-ID]` 进行紧急修复工作流程

**修复错误后（开发人员确认已修复）：**
- 运行 `/bug-report verify [BUG-ID]` — 在关闭之前确认修复确实有效
- 切勿在未经验证的情况下将错误标记为已关闭 - 未验证的修复仍处于打开状态

**验证返回后已验证已修复：**
- 运行 `/bug-report close [BUG-ID]` — 写入关闭记录并更新状态
- 运行 `/bug-triage` 刷新未解决的错误计数并将其从活动列表中删除
