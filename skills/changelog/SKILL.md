---
name: changelog
description: "从 git 提交、冲刺数据和设计文档自动生成变更日志。生成内部版本和面向玩家的版本。"
---

## 第一阶段：解析参数

Read 目标版本或冲刺编号的参数。如果给出了版本，请使用相应的 git 标签。如果给出了冲刺编号，请使用冲刺日期范围。

验证存储库是否已初始化：运行 `git rev-parse --is-inside-work-tree` 以确认 git 可用。如果不是 git 存储库，请通知用户并正常中止。

---

## 第 2 阶段：收集变更数据

Read 自上次标记或发布以来的 git 日志：

```
git log --oneline [last-tag]..HEAD
```

如果不存在标签，请读取完整日志或合理的近期范围（最近 100 次提交）。

Read 来自 `production/sprints/` 的相关期间的冲刺报告，以了解计划的工作和变更背后的背景。

Read 完成了 `design/gdd/` 在此期间实施的任何新功能的设计文档。

---

## 第 3 阶段：对变更进行分类

将每个更改分类为以下类别之一：

- **新功能**：全新的游戏系统、模式或内容
- **改进**：现有功能的增强、UX 改进、性能提升
- **错误修复**：纠正损坏的行为
- **平衡变化**：调整游戏价值、难度、经济
- **已知问题**：团队已意识到但尚未解决的问题
- **杂项**：不符合上述类别的更改，或提交的消息过于模糊而无法自信地分类

对于每个提交，检查消息是否包含任务 ID 或故事引用
（例如 `[STORY-123]`、`TR-`、`#NNN` 或类似名称）。计算缺少任何任务引用的提交
并将此计数包含在第 4 阶段指标部分中，如下所示：`Commits without task reference: [N]`。

---

## 第 4 阶段：生成内部变更日志

```markdown
# Internal Changelog: [Version]
Date: [Date]
Sprint(s): [Sprint numbers covered]
Commits: [Count] ([first-hash]..[last-hash])

## New Features
- [Feature Name] -- [Technical description, affected systems]
  - Commits: [hash1], [hash2]
  - Owner: [who implemented it]
  - Design doc: [link if applicable]

## Improvements
- [Improvement] -- [What changed technically and why]
  - Commits: [hashes]
  - Owner: [who]

## Bug Fixes
- [BUG-ID] [Description of bug and root cause]
  - Fix: [What was changed]
  - Commits: [hashes]
  - Owner: [who]

## Balance Changes
- [What was tuned] -- [Old value -> New value] -- [Design intent]
  - Owner: [who]

## Technical Debt / Refactoring
- [What was cleaned up and why]
  - Commits: [hashes]

## Miscellaneous
- [Change that didn't fit other categories, or vague commit message]
  - Commits: [hashes]

## Known Issues
- [Issue description] -- [Severity] -- [ETA for fix if known]

## Metrics
- Total commits: [N]
- Files changed: [N]
- Lines added: [N]
- Lines removed: [N]
- Commits without task reference: [N]
```

---

## 第 5 阶段：生成面向玩家的变更日志

```markdown
# What is New in [Version]

## New Features
- **[Feature Name]**: [Player-friendly description of what they can now do
  and why it is exciting. Focus on the experience, not the implementation.]

## Improvements
- **[What improved]**: [How this makes the game better for the player.
  Be specific but avoid jargon.]

## Bug Fixes
- Fixed an issue where [describe what the player experienced, not what was
  wrong in the code]
- Fixed [player-visible symptom]

## Balance Changes
- [What changed in player-understandable terms and the design intent.
  Example: "Healing potions now restore 50 HP (up from 30) -- we felt
  players needed more recovery options in late-game encounters."]

## Known Issues
- We are aware of [issue description in player terms] and are working on a
  fix. [Workaround if one exists.]

---
Thank you for playing! Your feedback helps us make the game better.
Report issues at [link].
```

---

## 阶段 6：输出

将两个变更日志输出给用户。内部变更日志是主要工作文档。面向玩家的变更日志在审核后已准备好供社区发布。

---

## 第 7 阶段：报价文件 Write

呈现变更日志后，询问用户：

> “我可以将此变更日志写入 `docs/CHANGELOG.md` 吗？
> [A] 是，附加此条目（如果文件已存在，则建议添加）
> [B] 是，完全覆盖该文件
> [C] 否 — 我将手动复制它”

- 询问前检查`docs/CHANGELOG.md`是否存在。如果是这样，则默认
  建议**[A] 附加**。
- 如果用户选择 [A]：将新的内部变更日志条目附加到顶部
  现有文件（最新条目在前）。
- 如果用户选择 [B]：用新的更改日志覆盖该文件。
- 如果用户选择[C]：此处停止，不写入。

成功写入后：结论：**更改日志写入** — 更改日志已保存到 `docs/CHANGELOG.md`。
如果用户拒绝：结论：**完成** - 生成变更日志。

---

## 第 7 阶段：后续步骤

- 使用 `/patch-notes [version]` 生成样式化的保存版本以供公开发布。
- 在外部发布变更日志之前使用 `/release-checklist`。

### Guidelines

- 切勿在面向玩家的变更日志中公开内部代码引用、文件路径或开发人员名称
- 将相关更改分组在一起，而不是列出单独的提交
- 如果提交消息不清楚，请检查关联文件和冲刺数据以了解上下文
- 平衡变化应始终包括设计推理，而不仅仅是数字
- 已知问题应该是诚实的——玩家欣赏透明度
- 如果 git 历史记录很混乱（合并提交、恢复、修复提交），请清理叙述而不是逐字列出每个提交
