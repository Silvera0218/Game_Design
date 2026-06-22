---
name: day-one-patch
description: "为游戏发布准备第一天补丁。范围、优先级、实施和 QA 门是一个重点补丁，解决在金牌大师之后但在公开发布之前或之后立即发现的已知问题。将补丁视为具有自己的 QA 门和回滚计划的迷你冲刺。"
---

# 第一天补丁

每个发布的游戏都有一个第一天补丁。在发布日之前进行规划可以防止
混乱。该技能将补丁范围限制在安全且必要的范围内，并对其进行门控
通过轻量级 QA 传递，并确保在执行任何操作之前存在回滚计划
船舶。这是一个迷你冲刺——不是修补程序，也不是完整的冲刺。

**何时运行：**
- 黄金主版本被锁定后（证书已批准或发布候选标记）
- 当存在已知错误且风险太大而无法在 Gold Master 中解决时
- 当证书反馈需要提交后进行小修改时
- 当发布前的游戏测试在发布门通过后出现必须解决的问题时

**第一天补丁范围规则：**
- 只有 P1/P2 错误可以安全快速修复
- 没有新功能——这只是修复
- 无需重构——最小可行的改变
- 任何需要超过 4 小时开发时间的修复都属于补丁 1.1，而不是第一天

**输出：** `production/releases/day-one-patch-[version].md`

---

## 第 1 阶段：加载释放上下文

Read:
- `production/stage.txt` — 确认项目处于发布阶段
- `production/gate-checks/` 中的最新文件 — 阅读释放门判决
- `production/qa/bugs/*.md` — 加载状态为“开放”或“已修复”的所有错误 — 待验证
- `production/sprints/` 最新 — 了解发货内容
- `production/security/security-audit-*.md` 最新 — 检查是否有任何打开的安全项目

如果 `production/stage.txt` 不是 `Release` 或 `Polish`：
> “第一天的补丁准备适用于发布阶段的项目。当前阶段：[stage]。在即将发布之前，此技能不适用。”

---

## 第 2 阶段：确定补丁范围

### 步骤 2a — 对未解决的错误进行分类以包含补丁

对于每个未解决的错误，评估：

| Criterion | 包括在第一天吗？ |
|-----------|-------------------|
| S1 or S2 severity | 是 - 必须包括是否可以安全修复 |
| P1 priority | Yes |
| 预计修复时间 < 4 小时 | Yes |
| 修复需要更改架构 | 否 — 遵循 1.1 |
| 修复引入了新的代码路径 | 不——风险太大 |
| 仅修复 data/config（无代码更改） | 是的——风险非常低 |
| 证书反馈要求 | 是 - 需要平台批准 |
| S3/S4 severity | 仅当简单的配置修复时；否则推迟 |

### 步骤 2b — 向用户展示补丁范围

使用 `AskUserQuestion`：
- 提示：“根据未解决的错误和证书反馈，这是建议的第一天补丁范围。这看起来正确吗？”
- 显示：包含的错误表（ID、严重性、描述、估计工作量）
- 显示：延迟错误表（ID、严重性、延迟原因）
- 选项：`[A] Approve this scope` / `[B] Adjust — I want to add or remove items` / `[C] No day-one patch needed`

如果 [C]：输出“不需要第一天补丁。继续 `/launch-checklist`。”停止。

### 步骤 2c — 检查总范围

估计工作量总和。如果总工作时间超过 1 天：
> “⚠️ 补丁范围是 [N hours] — 这超出了安全的第一天窗口。考虑将优先级较低的项目推迟到补丁 1.1。臃肿的第一天补丁带来的风险比它消除的风险还要多。”

使用 `AskUserQuestion` 确认继续或缩小范围。

---

## 第三阶段：回滚计划

在编写任何代码之前，定义回滚过程。这是没有商量余地的。

通过 Task 生成 `release-manager`。要求他们制定一份回滚计划，内容包括：
- 如何在每个目标平台上恢复到金牌大师版本
- 特定于平台的回滚约束（某些平台无法回滚证书版本）
- 谁负责触发回滚
- 如果发生回滚，需要哪些玩家沟通

提出回滚计划。问：“我可以把这个回滚计划写到`production/releases/rollback-plan-[version].md`吗？”

在编写回滚计划之前，不要继续进入第 4 阶段。

---

## 第 4 阶段：实施修复

对于批准范围内的每个错误，产生一个集中的实现循环：

1. 通过 Task 生成 `lead-programmer`：
   - 错误报告（确切的重现步骤和根本原因（如果已知））
   - 约束：仅最小可行修复，不进行清理
   - 受影响的文件（来自错误报告技术上下文部分）

2. 首席程序员实施并运行有针对性的测试。

3. 通过 Task 生成 `qa-tester` 来验证：修复后错误是否会重现？

对于 config/data-only 修复：直接进行更改（无需程序员代理）。确认更改的值并重新运行任何相关的烟雾测试。

---

## 第 5 阶段：补丁 QA 门

这是一个轻量级的 QA 通行证 — 不是完整的 `/team-qa`。该补丁已在发布阶段获得 QA 批准；我们只是重新验证更改的区域。

通过 Task 生成 `qa-lead`：
- 所有已更改文件的列表
- 已修复的错误列表（包含第 4 阶段的验证状态）
- 受影响系统的烟雾检查范围

询问 qa-lead 以确定：**有针对性的烟雾检查是否足够，或者是否有任何修复涉及需要更广泛回归的系统？**

运行所需的 QA 范围：
- **有针对性的烟雾检查** — 运行 `/smoke-check [affected-systems]`
- **更广泛的回归** — 在 `tests/unit/` 和 `tests/integration/` 中针对受影响的系统运行有针对性的测试

QA 判定必须为“通过”或“通过但有警告”，然后才能继续。如果失败：将失败的修复范围排除在第一天补丁之外并推迟到 1.1。

---

## 阶段6：生成补丁记录

```markdown
# Day-One Patch: [Game Name] v[version]

**Date prepared**: [date]
**Target release**: [launch date or "day of launch"]
**Base build**: [gold master tag or commit]
**Patch build**: [patch tag or commit]

---

## Patch Notes (Internal)

### Bugs Fixed
| BUG-ID | Severity | Description | Fix summary |
|--------|----------|-------------|-------------|
| BUG-NNN | S[1-4] | [description] | [one-line fix] |

### Deferred to 1.1
| BUG-ID | Severity | Description | Reason deferred |
|--------|----------|-------------|-----------------|
| BUG-NNN | S[1-4] | [description] | [reason] |

---

## QA Sign-Off

**QA scope**: [Targeted smoke / Broader regression]
**Verdict**: [PASS / PASS WITH WARNINGS]
**QA lead**: qa-lead agent
**Date**: [date]
**Warnings (if any)**: [list or "None"]

---

## Rollback Plan

See: `production/releases/rollback-plan-[version].md`

**Trigger condition**: If [N] or more S1 bugs are reported within [X] hours of launch, execute rollback.
**Rollback owner**: [user / producer]

---

## Approvals Required Before Deploy

- [ ] lead-programmer: all fixes reviewed
- [ ] qa-lead: QA gate PASS confirmed
- [ ] producer: deployment timing approved
- [ ] release-manager: platform submission confirmed

---

## Player-Facing Patch Notes

[Draft for community-manager to review before publishing]

[list player-facing changes in plain language]
```

问：“我可以将这个补丁记录写入`production/releases/day-one-patch-[version].md`吗？”

---

## 第 7 阶段：后续步骤

补丁记录写入后：

1. 运行 `/patch-notes` 生成面向玩家的补丁说明版本
2. 补丁生效后，针对每个已修复的错误运行 `/bug-report verify [BUG-ID]`
3. 针对每个经过验证的修复运行 `/bug-report close [BUG-ID]`
4. 使用 `/retrospective launch` 在启动后 48-72 小时安排启动后审核

**如果补丁后任何 S1 错误仍然存在：**
> “⚠️ S1 错误仍然存在并且没有修补。这些都是可接受的风险。将它们记录在回滚计划触发条件中 - 如果它们大规模发生，回滚可能比后续补丁更可取。”

---

## 协作协议

- **范围纪律就是一切**——抵制范围蔓延；每次添加都会增加风险
- **始终先回滚计划** — 没有回滚计划的补丁是不负责任的
- **延迟不会被遗忘** - 每个延迟的错误都会自动获得 1.1 票证
- **玩家通信是补丁的一部分** - `/patch-notes` 是必需的输出，不是可选的
