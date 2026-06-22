---
name: playtest-report
description: "生成结构化游戏测试报告模板或将现有游戏测试注释分析为结构化格式。用它来标准化游戏测试反馈收集和分析。"
---

## 第一阶段：解析参数

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

确定模式：

- `new` → 生成空白的游戏测试报告模板
- `analyze [path]` → 阅读原始笔记并用结构化结果填写模板

---

## 阶段 2A：新模板模式

生成此模板并将其输出给用户：

```markdown
# Playtest Report

## Session Info
- **Date**: [Date]
- **Build**: [Version/Commit]
- **Duration**: [Time played]
- **Tester**: [Name/ID]
- **Platform**: [PC/Console/Mobile]
- **Input Method**: [KB+M / Gamepad / Touch]
- **Session Type**: [First time / Returning / Targeted test]

## Test Focus
[What specific features or flows were being tested]

## First Impressions (First 5 minutes)
- **Understood the goal?** [Yes/No/Partially]
- **Understood the controls?** [Yes/No/Partially]
- **Emotional response**: [Engaged/Confused/Bored/Frustrated/Excited]
- **Notes**: [Observations]

## Gameplay Flow
### What worked well
- [Observation 1]

### Pain points
- [Issue 1 -- Severity: High/Medium/Low]

### Confusion points
- [Where the player was confused and why]

### Moments of delight
- [What surprised or pleased the player]

## Bugs Encountered
| # | Description | Severity | Reproducible |
|---|-------------|----------|-------------|

## Feature-Specific Feedback
### [Feature 1]
- **Understood purpose?** [Yes/No]
- **Found engaging?** [Yes/No]
- **Suggestions**: [Tester suggestions]

## Quantitative Data (if available)
- **Deaths**: [Count and locations]
- **Time per area**: [Breakdown]
- **Items used**: [What and when]
- **Features discovered vs missed**: [List]

## Overall Assessment
- **Would play again?** [Yes/No/Maybe]
- **Difficulty**: [Too Easy / Just Right / Too Hard]
- **Pacing**: [Too Slow / Good / Too Fast]
- **Session length preference**: [Shorter / Good / Longer]

## Top 3 Priorities from this session
1. [Most important finding]
2. [Second priority]
3. [Third priority]
```

---

## 阶段 2B：分析模式

Read 所提供路径中的原始注释。与现有设计文件的交叉引用。用结构化的结果填写上面的模板。标记任何与设计意图相冲突的游戏测试观察结果。

---

## 第三阶段：动作路由

将所有发现分为四类：

- **需要进行设计更改** — 有趣的问题、玩家困惑、机制损坏、与 GDD 的预期体验相冲突的观察结果
- **平衡调整** - 数字感觉不对，难度太高或太平
- **错误报告** - 明确的可重现的实施缺陷
- **抛光项目** - 不会阻碍进展，但会产生摩擦或感觉问题供以后使用

显示分类列表，然后路由：

- **设计更改：**“在受影响的设计文档上运行 `/propagate-design-change [path]`，以在进行更改之前查找下游影响。”
- **平衡调整：**“在调整值之前运行 `/balance-check [system]` 以验证完整的平衡图。”
- **错误：**“使用 `/bug-report` 正式跟踪这些。”
- **抛光项目：**“当团队达到该阶段时，添加到 `production/` 中的抛光待办事项中。”

---

## 第 3b 阶段：创意总监玩家体验审核

**查看模式检查** — 在生成 CD-PLAYTEST 之前应用：
- `solo` → 跳过。注意：“CD-PLAYTEST 已跳过 — 单人模式。”继续进行第 4 阶段（保存报告）。
- `lean` → 跳过（不是相位门）。注意：“CD-PLAYTEST 已跳过 — 精益模式。”继续进行第 4 阶段（保存报告）。
- `full` → 正常生成。

对结果进行分类后，使用门 **CD-PLAYTEST** (`.codex/docs/director-gates.md`) 通过 Task 生成 `creative-director`。

通过：结构化报告内容、游戏支柱和核心幻想（来自`design/gdd/game-concept.md`）、正在测试的具体假设。

在保存报告之前呈现创意总监的评估。如果存在疑虑或拒绝，请在捕获结论和反馈的报告中添加 `## Creative Director Assessment` 部分。如果批准，请在报告中注明批准情况。

---

## 第四阶段：保存报告

问：“我可以将此游戏测试报告写给 `production/qa/playtests/playtest-[date]-[tester].md` 吗？”

如果是，则写入文件，并根据需要创建目录。

---

## 第五阶段：后续步骤

结论：**完成** — 生成游戏测试报告。

- 首先对最高优先级的发现类别采取行动。
- 解决设计更改后：在更新的 GDD 上重新运行 `/design-review`。
- 修复错误后：重新运行 `/bug-triage` 以更新优先级。
