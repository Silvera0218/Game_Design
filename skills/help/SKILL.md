---
name: help
description: "分析已完成的操作和用户查询，并提供下一步操作的建议。如果用户说我下一步应该做什么或我现在做什么或者我陷入困境或我不知道该怎么做，则使用"
---

# Studio 帮助 — 接下来我该做什么？

该技能是只读的 - 它报告发现但不写入文件。

这项技能可以准确地确定您在游戏开发流程中的位置，并且
告诉你接下来会发生什么。它是**轻量级**——不是完整的审计。对于一个完整的
差距分析，使用 `/project-stage-detect`。

---

## 第 1 步：Read 目录

Read `.codex/docs/workflow-catalog.yaml`。这是所有的权威列表
阶段、步骤（按顺序）、每个步骤是必需的还是可选的，以及
指示完成的工件球。

如果该目录文件不存在，不要失败；改为使用第 2 步的工件推断规则，并在输出中说明“未找到 workflow-catalog，已按项目文件推断阶段”。

---

## 步骤 1b：查找目录中没有的技能

阅读目录后， Glob `.codex/skills/*/SKILL.md` 获取完整列表
已安装的技能。对于每个文件，从其 frontmatter 中提取 `name:` 字段。

与目录中的 `command:` 值进行比较。任何名字具有的技能
不显示为目录命令是一种**未编目技能** - 仍然可用但不可用
阶段门控工作流程的一部分。

收集这些用于第 7 步中的输出 - 将它们显示为页脚块：

```
### Also installed (not in workflow)
- `/skill-name` — [description from SKILL.md frontmatter]
- `/skill-name` — [description]
```

仅当至少存在一项未编目技能时才显示此块。限制为 10 个
根据用户当前阶段最相关（QA 生产、团队技能
production/polish等中的技能）。

---

## 第 2 步：确定当前相位

按此顺序检查：

1. **Read `production/stage.txt`** — 如果存在并且有内容，则这就是
   权威相名。将其映射到目录阶段键：
   - “概念”→ `concept`
   - “系统设计”→ `systems-design`
   - “技术设置”→ `technical-setup`
   - “预生产”→ `pre-production`
   - “生产” → `production`
   - “抛光”→ `polish`
   - “发布”→ `release`

2. **如果 stage.txt 丢失**，从工件推断阶段（最先进的比赛获胜）：
   - `src/` 有 10+ 源文件 → `production`
   - `production/stories/*.md` 存在 → `pre-production`
   - `docs/architecture/adr-*.md` 存在 → `technical-setup`
   - `design/gdd/systems-index.md` 存在 → `systems-design`
   - `GDD/INDEX.md` 存在且 `GDD/*_GDD.md` 至少有 2 个 → `systems-design`
   - `design/gdd/game-concept.md` 存在 → `concept`
   - `GDD/00_项目总览_GDD.md` 存在 → `concept`
   - 什么都没有 → `concept`（新项目）

---

## 步骤 3：Read 会话上下文

Read `production/session-state/active.md`（如果存在）。摘录：
- 最近在做什么
- 任何正在进行的任务或悬而未决的问题
- 来自 STATUS 块的当前 epic/feature/task（如果存在）

这会告诉您用户刚刚完成或坚持的内容 - 用它来个性化
输出。

---

## 步骤 4：检查当前阶段的步骤完成情况

对于当前阶段的每个步骤（来自目录）：

### 基于工件的检查

如果该步骤具有 `artifact.glob`：
- 使用 Glob 检查是否存在与模式匹配的文件
- 如果指定了 `min_count`，请验证至少有多个文件匹配
- 如果指定了 `artifact.pattern`，则使用 Grep 验证匹配文件中是否存在该模式
- **完成** = 满足工件条件
- **不完整** = 工件缺失或未找到模式

如果该步骤具有 `artifact.note`（无 glob）：
- 标记为 **手动** — 无法自动检测，将询问用户

如果该步骤没有 `artifact` 字段：
- 标记为 **未知** - 完成情况不可追踪（例如可重复的实施工作）

### 特殊情况：生产阶段 — 阅读 `sprint-status.yaml`

当当前相位为`production`时，检查`production/sprint-status.yaml`
在进行任何基于全局的故事检查之前。如果存在则直接读取：

- 带有 `status: in-progress` 的故事 → 表面为“当前活动”
- `status: ready-for-dev` 的故事 → 表面为“下一个”
- 包含 `status: done` 的故事 → 算作完整
- 故事与 `status: blocked` → 表面作为 `blocker` 字段的阻挡者

这无需降价扫描即可提供精确的每个故事状态。跳过全局
`implement` 和 `story-done` 步骤的工件检查 - YAML 是权威的。

### 特殊情况：`repeatable: true`（非生产）

对于生产之外的可重复步骤（例如“系统 GDD”），工件
检查告诉您是否*任何*工作已经完成，而不是它是否完成。
对这些进行不同的标记——显示检测到的内容，然后注意它可能正在进行。

---

## 第 5 步：找到位置并确定后续步骤

根据完成数据，确定：

1. **最后确认的完整步骤** — 最远完成的所需步骤
2. **当前阻止程序** — 第一个不完整的*必需*步骤（这就是
   用户接下来必须执行的操作）
3. **可选机会** — 可以完成的不完整的*可选*步骤
   在阻挡者之前或旁边
4. **即将执行的所需步骤** — 当前阻止程序之后所需的步骤
   （显示为“即将推出”，以便用户可以提前计划）

如果用户提供了一个参数（例如“刚刚完成设计审查”），请使用该参数
即使工件检查不明确，也可以继续执行他们指定的步骤。

---

## 第 6 步：检查正在进行的工作

如果 `active.md` 显示活动任务或史诗：
- 在顶部突出显示：“看起来您正在处理 [X]”
- 建议继续或确认是否已完成

---

## 第 7 步：呈现输出

保持**简短而直接**。这是一个快速的指导，而不是一份报告。

```
## Where You Are: [Phase Label]

**In progress:** [from active.md, if any]

### ✓ Done
- [completed step name]
- [completed step name]

### → Next up (REQUIRED)
**[Step name]** — [description]
Command: `[/command]`

### ~ Also available (OPTIONAL)
- **[Step name]** — [description] → `/command`
- **[Step name]** — [description] → `/command`

### Coming up after that
- [Next required step name] (`/command`)
- [Next required step name] (`/command`)

---
Approaching **[next phase]** gate → run `/gate-check` when ready.
```

**格式规则：**
- `✓` 确认完成
- `→` 用于当前所需的下一步（只有一个 - 第一个阻止程序）
- `~` 现已提供可选步骤
- 将内联命令显示为反引号代码
- 如果某个步骤没有命令（例如“实施故事”），请解释要做什么，而不是显示斜线命令
- 对于手动步骤，询问用户：“我无法判断 [step] 是否已完成 - 它已完成吗？”

结论：**完成**——确定了后续步骤。

---

## 第 8 步：门警告（如果关闭）

在当前阶段的步骤之后，检查用户是否可能接近大门：
- 如果当前阶段的所有必需步骤均已完成（或接近完成），
  添加：“您已接近 **[Current] → [Next]** 门。准备好后运行 `/gate-check`。”
- 如果仍有多个必需步骤，请跳过门警告 - 它还不相关。

---

## 第 9 步：升级路径

在建议之后，如果用户似乎陷入困境或困惑，请添加：

```
---
Need more detail?
- `/project-stage-detect` — full gap analysis with all missing artifacts listed
- `/gate-check` — formal readiness check for your next phase
- `/start` — re-orient from scratch
```

仅当用户的输入表明混乱时才显示此内容（例如“我不知道”、“卡住”、
“丢失”、“不确定”）。不要为了简单的“下一步是什么？”而展示它。查询。

---

## 协作协议

- **永远不要自动运行下一个技能。**推荐它，让用户调用它。
- **询问手动步骤**，而不是假设完整或不完整。
- **匹配用户的语气** - 如果他们听起来很紧张（“我完全迷失了”），那就
  令人放心并采取一项行动，而不是列出六项行动。
- **一个主要建议** — 用户离开时应该确切地知道一件事
  接下来要做的事。可选步骤和“即将进行”是次要背景。
