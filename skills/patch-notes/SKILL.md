---
name: patch-notes
description: "从 git 历史记录、冲刺数据和内部变更日志生成面向玩家的补丁说明。将开发者语言转化为清晰、引人入胜的玩家交流。"
---

## 第一阶段：解析参数

- `version`：为其生成注释的发行版本（例如，`1.2.0`）
- `--style`：输出样式 - `brief`（要点）、`detailed`（带上下文）、`full`（带开发人员评论）。默认值：`detailed`。

如果未提供版本，请在继续之前询问用户。

---

## 第 2 阶段：收集变更数据

- Read `production/releases/[version]/changelog.md` 处的内部变更日志（如果存在）
- 另请检查 `docs/CHANGELOG.md` 的相关版本条目
- 在先前版本标签和当前 tag/HEAD 之间运行 `git log` 作为后备
- Read `production/sprints/` 中的冲刺回顾以了解背景
- Read `design/balance/` 中的任何余额更改文档
- Read 来自 QA 的错误修复记录（如果有）

**如果没有可用的变更日志数据**（`production/releases/[version]/changelog.md`
此版本的 `docs/CHANGELOG.md` 条目也不存在，并且 git 日志为空或不可用）：

> “未找到 [version] 的变更日志数据。首先运行 `/changelog [version]` 以生成
> 内部变更日志，然后重新运行 `/patch-notes [version]`。”

结论：**已阻止** — 在此停止而不生成注释。

---

## 阶段 2b：检测音调指南和模板

**语气指导检测** - 在起草笔记之前，检查写作风格指导：

1. 检查 `.codex/docs/technical-preferences.md` 是否有任何“音调”、“声音”或“风格”
   字段或部分。
2. 检查 `docs/PATCH-NOTES-STYLE.md` 是否存在。
3. 检查 `design/community/tone-guide.md` 是否存在。
4. 如果任何源包含 tone/voice/style 指令，请提取它们并应用
   它们适应所生成笔记的语言和框架。
5. 如果在任何地方都找不到音调指导，则默认为：
   玩家友好的非技术性语言；热情但不夸张；
关注玩家的体验，而不是开发者改变的内容。

**模板检测** — 检查补丁说明模板是否存在：

1. Glob 适用于 `docs/patch-notes-template.md` 和 `.codex/docs/templates/patch-notes-template.md`。
2. 如果在任一位置找到，则读取它并将其用作阶段 4 的输出结构
   而不是内置的样式模板（简要/详细/完整）。填写
   带有分类数据的模板部分。
3. 如果未找到，请使用第 4 阶段中定义的内置样式模板。

---

## 第三阶段：分类和翻译

将所有更改分类为面向玩家的类别：

- **新内容**：新功能、地图、角色、物品、模式
- **游戏玩法变化**：平衡调整、机制变化、进度变化
- **生活质量**：UI 改进、便利功能、可访问性
- **错误修复**：按系统分组（战斗、UI、网络等）
- **性能**：玩家可能会注意到的优化改进
- **已知问题**：未解决问题的透明度

将开发者语言翻译为玩家语言：

- “重构伤害计算管道”→“提高命中检测精度”
- “修复了库存管理器中的空引用”→“修复了打开库存时的崩溃”
- “减少战斗循环中的GC分配”→“提高战斗性能”
- 删除不影响玩家的纯粹内部更改
- 保留平衡变化的特定数字（伤害：50 → 45）

---

## 第 4 阶段：生成补丁说明

### 简洁风格
```markdown
# Patch [Version] — [Title]

**New**
- [Feature 1]
- [Feature 2]

**Changes**
- [Balance/mechanic change with before → after values]

**Fixes**
- [Bug fix 1]
- [Bug fix 2]

**Known Issues**
- [Issue 1]
```

### 详细款式
```markdown
# Patch [Version] — [Title]
*[Date]*

## Highlights
[1-2 sentence summary of the most exciting changes]

## New Content
### [Feature Name]
[2-3 sentences describing the feature and why players should be excited]

## Gameplay Changes
### Balance
| Change | Before | After | Reason |
| ---- | ---- | ---- | ---- |
| [Item/ability] | [old value] | [new value] | [brief rationale] |

### Mechanics
- **[Change]**: [explanation of what changed and why]

## Quality of Life
- [Improvement with context]

## Bug Fixes
### Combat
- Fixed [description of what players experienced]

### UI
- Fixed [description]

### Networking
- Fixed [description]

## Performance
- [Improvement players will notice]

## Known Issues
- [Issue and workaround if available]
```

### 完整风格
包括详细信息中的所有内容，以及：
```markdown
## Developer Commentary
### [Topic]
> [Developer insight into a major change — why it was made, what was considered,
> what the team learned. Written in first-person team voice.]
```

---

## 第 5 阶段：审查输出

检查生成的注释：

- 没有内部术语（用玩家友好的语言替换技术术语）
- 没有提及内部系统、票据或冲刺编号
- 余额更改包括 before/after 值
- 错误修复描述的是玩家体验，而不是技术原因
- 语气与游戏的声音相匹配（根据游戏风格调整形式）

---

## 第 6 阶段：保存补丁说明

向用户展示已完成的补丁说明以及：按类别划分的更改计数，以及排除的任何内部更改（以供审核）。

问：“我可以将这些补丁说明写入 `docs/patch-notes/[version].md` 吗？”

如果是，则将文件写入`docs/patch-notes/[version].md`，创建目录
如果需要的话。同时写入 `production/releases/[version]/patch-notes.md` 作为
内部存档副本。

---

## 第 7 阶段：后续步骤

结论：**完成**——生成并保存补丁说明。

- 在发布之前运行 `/release-checklist` 以验证是否满足所有其他发布门槛。
- 在公开发布之前，与社区经理共享补丁说明草稿，以进行语气审查。
