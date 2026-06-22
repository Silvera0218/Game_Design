---
name: hotfix
description: "紧急修复工作流程，通过完整的审计跟踪绕过正常的冲刺流程。创建修补程序分支、跟踪批准并确保正确向后移植修复程序。"
---

> **仅显式调用**：此技能仅应在用户使用 `/hotfix` 显式请求时运行。不要根据上下文匹配自动调用。

## 第一阶段：评估严重性

Read bug 描述或 ID。确定严重性：

- **S1（严重）**：游戏无法玩、数据丢失、安全漏洞 — 立即修复
- **S2（主要）**：重大功能损坏，存在解决方法 - 24 小时内修复
- 如果严重性为 S3 或更低，建议使用正常的错误修复工作流程并停止。

---

## 第 2 阶段：创建修补程序记录

起草修补程序记录：

```markdown
## Hotfix: [Short Description]
Date: [Date]
Severity: [S1/S2]
Reporter: [Who found it]
Status: IN PROGRESS

### Problem
[Clear description of what is broken and the player impact]

### Root Cause
[To be filled during investigation]

### Fix
[To be filled during implementation]

### Testing
[What was tested and how]

### Approvals
- [ ] Fix reviewed by lead-programmer
- [ ] Regression test passed (qa-tester)
- [ ] Release approved (producer)

### Rollback Plan
[How to revert if the fix causes new issues]
```

问：“我可以把这个写到`production/hotfixes/hotfix-[date]-[short-name].md`吗？”

如果是，则写入文件，并根据需要创建目录。

---

## 第 3 阶段：创建修补程序分支

如果 git 已初始化，则创建修补程序分支：

```
git checkout -b hotfix/[short-name] [release-tag-or-main]
```

---

## 第四阶段：调查和实施

专注于解决问题的最小改变。请勿在修补程序旁边重构、清理或添加功能。

通过对受影响的系统运行有针对性的测试来验证修复。检查相邻系统中的回归。

更新修补程序记录，其中包含根本原因、修补程序详细信息和测试结果。

---

## 第 5 阶段：收集批准

使用 Task 工具并行请求签核：

- `subagent_type: lead-programmer` — 检查修复的正确性和副作用
- `subagent_type: qa-tester` — 在受影响的系统上运行有针对性的回归测试
- `subagent_type: producer` — 批准部署时间和沟通计划

所有三个人都必须返回 APPROVE，然后才能继续。如果有任何返回“担忧”或“拒绝”，请不要部署 - 首先提出问题并解决它。

---

## 阶段 5b：QA 重入门

批准后，在部署修补程序之前确定所需的 QA 范围。通过 Task 生成 `qa-lead`：
- 修补程序说明和受影响的系统
- 第 5 阶段的回归测试结果
- 涉及已更改文件的所有系统的列表（使用 Grep 查找调用者）

询问质量保证负责人：**完整的烟雾检查是否足够，或者此修复是否需要有针对性的团队质量保证通行证？**

执行判决：
- **烟雾检查足够** — 针对修补程序版本运行 `/smoke-check`。如果通过，则进入第 6 阶段。
- **需要目标 QA 通行证** — 仅在更改的系统范围内运行 `/team-qa [affected-system]`。如果 QA 返回“已批准”或“已批准但有条件”，则继续执行第 6 阶段。
- **需要完整的 QA** — S1 修复了触摸核心系统可能需要完整的 `/team-qa sprint`。这会延迟部署，但可以防止出现错误的补丁。

不要跳过这个门。破坏其他内容的修补程序比原始错误更糟糕。

---

## 第 6 阶段：更新错误状态并部署

更新原始错误文件（如果存在）：

```markdown
## Fix Record
**Fixed in**: hotfix/[branch-name] — [commit hash or description]
**Fixed date**: [date]
**Status**: Fixed — Pending Verification
```

在错误文件头中设置 `**Status**: Fixed — Pending Verification`。

输出部署摘要：

```
## Hotfix Ready to Deploy: [short-name]

**Severity**: [S1/S2]
**Root cause**: [one line]
**Fix**: [one line]
**QA gate**: [Smoke check PASS / Team-QA APPROVED]
**Approvals**: lead-programmer ✓ / qa-tester ✓ / producer ✓
**Rollback plan**: [from Phase 2 record]

Merge to: release branch AND development branch
Next: /bug-report verify [BUG-ID] after deploy to confirm resolution
```

### Rules
- 修补程序必须是解决问题的最小更改 - 无需清理，无需重构
- 每个修补程序在部署之前都必须记录回滚计划
- 修补程序分支合并到发布分支和开发分支
- 所有修补程序都需要在 48 小时内进行事后审查
- 如果修复非常复杂，需要超过 4 小时，请升级到 `technical-director`

---

## 第 7 阶段：部署后验证

部署后，运行 `/bug-report verify [BUG-ID]` 以确认修复解决了已部署版本中的问题。

如果已验证已修复：运行 `/bug-report close [BUG-ID]` 以正式关闭它。
如果仍然存在：修补程序失败 - 立即重新打开、评估回滚并升级。

使用 `/retrospective hotfix` 在 48 小时内安排事件后审查。
