---
name: design-review
description: "审查游戏设计文档的完整性、内部一致性、可实施性以及对项目设计标准的遵守情况。在将设计文档交给程序员之前运行此命令。"
---

## 第 0 阶段：解析参数

提取`--depth [完整|lean|独奏]` if present. Default is `full`当没有给出标志时。

**注意**：`--depth` 控制该技能的*分析深度*（产生多少专家代理）。它独立于 `production/review-mode.txt` 中的全局审核模式，该模式控制导演门的生成。这是两个不同的概念 - `--depth` 是关于*此*技能分析文档的彻底程度。

- **`full`**：完整审查 - 所有阶段 + 专家代理授权（阶段 3b）
- **`lean`**：所有阶段，无需专业代理 - 更快的单会话分析
- **`solo`**：仅限阶段 1-4，无委派，无阶段 5 下一步提示 — 从其他技能中调用时使用

---

## 第一阶段：加载文档

Read 完整的目标设计文档。 Read AGENTS.md 了解项目背景和标准。目标文档引用或暗示的Read相关设计文档（相关系统请检查`design/gdd/`）。

**依赖关系图验证：** 对于“依赖关系”部分中列出的每个系统，使用 Glob 检查其 GDD 文件是否存在于 `design/gdd/` 中。标记任何尚不存在的内容 - 这些是下游作者将点击的损坏的引用。

**Lore/narrative 对齐：** 如果 `design/gdd/game-concept.md` 或 `design/narrative/` 中的任何文件存在，则读取它。请注意此 GDD 中与既定世界规则、基调或设计支柱相矛盾的任何机械选择。在阶段 3b 中将此上下文传递给 `game-designer`。

**事前审核检查：**检查`design/gdd/reviews/[doc-name]-review-log.md`是否存在。如果是，请阅读最新的条目 - 请注意给出的裁决以及列出的阻止项目。本次会议是一次重新审查；跟踪先前的项目是否已得到解决。

---

## 第 2 阶段：完整性检查

根据设计文档标准清单进行评估：

- [ ] 有概述部分（一段摘要）
- [ ] 有玩家幻想部分（有意的感觉）
- [ ] 有详细规则部分（明确的机制）
- [ ] 有公式部分（所有数学都用变量定义）
- [ ] 有边缘案例部分（处理异常情况）
- [ ] 具有依赖项部分（列出了其他系统）
- [ ] 具有调音旋钮部分（已识别可配置值）
- [ ] 具有验收标准部分（可测试的成功条件）

---

## 第三阶段：一致性和可实施性

**内部一致性：**
- 公式生成的值是否与所描述的行为相匹配？
- 边缘情况是否与主要规则相矛盾？
- 依赖关系是双向的（其他系统是否知道这一点）？

**Implementability:**
- 这些规则是否足够精确，程序员无需猜测即可实施？
- 是否有任何“挥手”部分缺少细节？
- 是否考虑了性能影响？

**跨系统一致性：**
- 这与任何现有机制冲突吗？
- 这是否会造成与其他系统的意外交互？
- 这与游戏既定的基调和支柱一致吗？

---

## 第 3b 阶段：对抗性专家审查（仅限完整模式）

**在 `lean` 或 `solo` 模式下跳过此阶段。**

**此阶段在完整模式下是强制性的。** 不要跳过它。

**在生成任何代理之前**，打印此通知：
> “全面审查：并行生成专家代理。这通常需要 8-15 分钟。使用 `--review lean` 进行更快的单会话分析。”

### 步骤 1 — 识别 GDD 涉及的所有域

Read 和 GDD 并识别存在的每个域。 GDD 可以同时触及多个域——彻底。常见信号：

| 如果 GDD 包含... | 产生这些代理 |
|------------------------|-------------------|
| 成本、价格、掉落、奖励、经济 | `economy-designer` |
| 战斗统计、伤害、生命值、DPS | `game-designer`, `systems-designer` |
| AI 行为、寻路、瞄准 | `ai-programmer` |
| 关卡布局、产卵、波浪结构 | `level-designer` |
| 玩家进度、XP、解锁 | `economy-designer`、`game-designer` |
| UI、HUD、菜单、面向玩家的显示屏 | `ux-designer`, `ui-programmer` |
| 对话、任务、故事、传说 | `narrative-director` |
| 动画、感觉、时间、果汁 | `gameplay-programmer` |
| 多人游戏、同步、复制 | `network-programmer` |
| 音频提示、音乐触发器 | `audio-director` |
| 性能、绘制调用、内存 | `performance-analyst` |
| 特定于引擎的模式或 API | 主要发动机专家（来自 `.codex/docs/technical-preferences.md`） |
| 验收标准、测试覆盖率 | `qa-lead` |
| 数据模式、资源结构 | `systems-designer` |
| 任何游戏系统 | `game-designer`（始终） |

**始终生成 `game-designer` 和 `systems-designer` 作为基线最小值。** 每个 GDD 都会触及其域。

### 第 2 步 — 并行产生所有相关专家

**关键：此技能中的 Task 会生成一个 SUBAGENT — 一个单独的独立 Codex 会话
有自己的上下文窗口。这不是任务跟踪。不要模拟专家
内部观点。不要自己通过域视图进行推理。你必须发出
实际的 Task 调用。模拟审核不是专家审核。**

同时发出所有 Task 调用。不要一次生成一个。

**对抗性地提示每位专家：**
> “这是 [system] 的 GDD 以及迄今为止主要审查的结构发现。
> 你的工作不是验证这个设计——你的工作是发现问题。
> 挑战您的领域专业知识的设计选择。怎么了，
> 未指定、可能导致问题或完全缺失？
> 要具体并具有批判性。欢迎对主要审查提出不同意见。”

**每种代理类型的附加说明：**

- **`game-designer`**：将您的评论锚定在本 GDD 的 B 部分中所述的玩家幻想上。这个设计真的能实现那种幻想吗？玩家会感受到预期的体验吗？标记任何有助于实施但破坏所表达的感觉的规则。

- **`systems-designer`**：对于 GDD 中的每个公式，插入边界值（最小和最大合理输入）。报告是否有任何输出退化——负值、除以零、无穷大或极端情况下的无意义结果。

- **`qa-lead`**：检查每项验收标准。标记任何不可独立测试的内容——诸如“感觉平衡”、“工作正常”、“表现良好”之类的短语不是 AC。针对未通过此测试的任何内容提出具体重写建议。

### 第 3 步 — 高级主管审核

所有专家响应后，生成 `creative-director` 作为 **高级审阅者**：
- 提供：GDD、所有专家调查结果、他们之间的任何分歧
- 问：“综合这些发现。最重要的问题是什么？你同意专家的观点吗？你对这个设计的总体结论是什么？”
- 创意总监的综合结果成为第四阶段的**最终裁决**。

### 第四步——表面分歧

如果专家之间或与创意总监意见不一致，不要默默地选择一种观点。在第 4 阶段明确提出分歧，以便用户可以做出裁决。

标记每个发现的来源：`[game-designer]`、`[economy-designer]`、`[creative-director]` 等。

---

## 第 4 阶段：输出审核

```
## Design Review: [Document Title]
Specialists consulted: [list agents spawned]
Re-review: [Yes — prior verdict was X on YYYY-MM-DD / No — first review]

### Completeness: [X/8 sections present]
[List missing sections]

### Dependency Graph
[List each declared dependency and whether its GDD file exists on disk]
- ✓ enemy-definition-data.md — exists
- ✗ loot-system.md — NOT FOUND (file does not exist yet)

### Required Before Implementation
[Numbered list — blocking issues only. Each item tagged with source agent.]

### Recommended Revisions
[Numbered list — important but not blocking. Source-tagged.]

### Specialist Disagreements
[Any cases where agents disagreed with each other or with the main review.
Present both sides — do not silently resolve.]

### Nice-to-Have
[Minor improvements, low priority.]

### Senior Verdict [creative-director]
[Creative director's synthesis and overall assessment.]

### Scope Signal
Estimate implementation scope based on: dependency count, formula count,
systems touched, and whether new ADRs are required.
- **S** — single system, no formulas, no new ADRs, <3 dependencies
- **M** — moderate complexity, 1-2 formulas, 3-6 dependencies
- **L** — multi-system integration, 3+ formulas, may require new ADR
- **XL** — cross-cutting concern, 5+ dependencies, multiple new ADRs likely
Label clearly: "Rough scope signal: M (producer should verify before sprint planning)"

### Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
```

该技能是只读的——在第 4 阶段不会写入任何文件。

---

## 第五阶段：后续步骤

使用 `AskUserQuestion` 进行所有关闭交互。绝不是纯文本。

**第一个小部件 - 接下来做什么：**

如果已批准（第一次通过，无需修改），则直接进入系统索引小部件、审查日志小部件，然后是最终关闭小部件。不要显示单独的“做什么”小部件 - 最终的关闭小部件涵盖后续步骤。

如果需要修订或需要重大修订，选项：
- `[A] Revise the GDD now — address blocking items together`
- `[B] Stop here — revise in a separate session`
- `[C] Accept as-is and move on (only if all items are advisory)`

**如果用户选择 [A] — 立即修改：**

解决所有阻塞项目，仅在无法仅通过 GDD 和现有文档解决问题时才要求设计决策。在进行任何编辑之前，将所有设计决策问题分组到一个多选项卡 `AskUserQuestion` 中 - 不要单独中断每个阻止程序的中间修订。

所有修订完成后，显示汇总表（阻止程序→已应用修复）并使用 `AskUserQuestion` 作为**修订后关闭小部件**：

- 提示：“修订完成 — [N] 阻止程序已解决。接下来做什么？”
- 注意当前上下文使用情况：如果上下文高于 ~50%，请添加：“（建议：重新审核前 /clear — 此会话已使用 X% 上下文。完整的重新审核运行 5 个代理，需要干净的上下文。）”
- Options:
  - `[A] Re-review in a new session — run /design-review [doc-path] after /clear`
  - `[B] Accept revisions and mark Approved — update systems index, skip re-review`
  - `[C] Move to next system — /design-system [next-system] (#N in design order)`
  - `[D] Stop here`

切勿以纯文本结束修订流程。始终关闭此小部件。

**第二个小部件 - 系统索引更新（始终单独显示）：**

使用第二个 `AskUserQuestion`：
- 提示：“我可以更新`design/gdd/systems-index.md`，将[system]标记为[In Review / Approved]吗？”
- 选项：`[A] Yes — update it` / `[B] No — leave it as-is`

**第三个小部件 - 审查日志（始终提供）：**

使用第三个 `AskUserQuestion`：
- 提示：“我可以将此审核摘要附加到 `design/gdd/reviews/[doc-name]-review-log.md` 吗？这会创建修订历史记录，以便将来的重新审核可以跟踪更改的内容。”
- 选项：`[A] Yes — append to review log` / `[B] No — skip`

如果是，请附加以下格式的条目：
```
## Review — [YYYY-MM-DD] — Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
Scope signal: [S/M/L/XL]
Specialists: [list]
Blocking items: [count] | Recommended: [count]
Summary: [2-3 sentence summary of key findings from creative-director verdict]
Prior verdict resolved: [Yes / No / First review]
```

---

**最终关闭小部件 - 始终在所有文件写入完成后显示：**

一旦系统索引和审查日志小部件得到答复，请检查项目状态并显示最终的 `AskUserQuestion`：

在构建选项之前，请阅读：
- `design/gdd/systems-index.md` — 查找任何状态为：正在审查或需要修订的系统（除了刚刚审查的系统）
- 统计 `design/gdd/` 中的 `.md` 文件（不包括 game-concept.md、systems-index.md），以确定 `/review-all-gdds` 是否值得提供（≥2 GDD）
- 查找设计订单中状态为“未启动”的下一个系统

动态构建选项列表 - 只包含真正的下一个选项：
- `[_] Run /design-review [other-gdd-path] — [system name] is still [In Review / NEEDS REVISION]`（如果另一个 GDD 需要审核，则包括在内）
- `[_] Run /consistency-check — verify this GDD's values don't conflict with existing GDDs`（如果存在 ≥1 个其他 GDD，则始终包含）
- `[_] Run /review-all-gdds — holistic design-theory review across all designed systems`（如果存在 ≥2 个 GDD，则包括在内）
- `[_] Run /design-system [next-system] — next in design order`（始终包含，命名实际系统）
- `[_] Stop here`

仅将字母 A、B、C...分配给包含的选项。将最先进的管道选项标记为 `(recommended)`。

文件写入后切勿以纯文本结束技能。始终关闭此小部件。
