---
name: create-stories
description: "将单个史诗分解为可实施的故事文件。阅读史诗，其 GDD，管理 ADR 和控制清单。每个故事都嵌入其 GDD 要求 TR-ID、ADR 指南、验收标准、故事类型和测试证据路径。针对每个史诗运行 /create-epics。"
---

# 创建故事

故事是一个单一的可实现的行为——小到足以一次性完成
集中会议、独立且完全可追溯至 GDD 要求，
ADR 决定。故事是开发者收集的。史诗是建筑师的事
define.

**按史诗运行此技能**，而不是按层运行。首先为基础史诗运行它，
然后是 Core，依此类推——匹配依赖顺序。

**输出：** `production/epics/[epic-slug]/story-NNN-[slug].md` 文件

**上一步：** `/create-epics [system]`
**故事存在后下一步：** `/story-readiness [story-path]` 然后 `/dev-story [story-path]`

---

## 1. 解析参数

提取`--review [完整|lean|olo]` 如果存在并存储为审阅模式
覆盖本次运行。如果未提供，请阅读 `production/review-mode.txt`
（如果缺少，则默认为 `full`）。此解决模式适用于所有门生成
在此技能中 - 应用 `.codex/docs/director-gates.md` 中的检查模式
在每次门调用之前。

- `/create-stories [epic-slug]` — 例如`/create-stories combat`
- `/create-stories production/epics/combat/EPIC.md` — 也接受完整路径
- 没有争论——问：“你想把哪部史诗分成故事？”
  Glob `production/epics/*/EPIC.md` 并列出可用的史诗及其状态。

---

## 2. 加载这部史诗的所有内容

Read 完整：

- `production/epics/[epic-slug]/EPIC.md` — 史诗般的概述，管理 ADR，GDD 要求表
- 史诗的 GDD (`design/gdd/[filename].md`) — 阅读所有 8 个部分，尤其是验收标准、公式和边缘情况
- 史诗中列出的所有管理 ADR - 阅读决策、实施指南、引擎兼容性和引擎注释部分
- `docs/architecture/control-manifest.md` — 提取该史诗层的规则；请注意标题中的清单版本日期
- `docs/architecture/tr-registry.yaml` — 加载该系统的所有 TR-ID

**ADR 存在验证**：从史诗中读取控制 ADR 列表后，确认磁盘上存在每个 ADR 文件。如果找不到任何 ADR 文件，请在分解任何故事之前**立即停止**：

> “Epic 引用了 [ADR-NNNN: title]，但未找到 `docs/architecture/[adr-file].md`。
> 检查史诗的管理 ADR 列表中的文件名，或运行 `/architecture-decision`
> 创建它。在所有引用的 ADR 文件都存在之前，无法创建故事。”

在确认所有引用的 ADR 文件均存在之前，请勿继续执行步骤 3。

报告：“已加载史诗 [name]、GDD [filename]、[N] 管理 ADR（均已确认存在），控制清单 v[date]。”

---

## 3.按类型对故事进行分类

**故事类型分类** — 根据每个故事的接受标准为每个故事分配一个类型：

| 故事类型 | 当标准引用时分配... |
|---|---|
| **Logic** | 公式、数值阈值、状态转换、AI 决策、计算 |
| **Integration** | 两个或多个系统交互、信号跨越边界、save/load 往返 |
| **Visual/Feel** | 动画行为，VFX，“感觉灵敏”，计时，屏幕震动，音频同步 |
| **UI** | 菜单、HUD 元素、按钮、屏幕、对话框、工具提示 |
| **Config/Data** | 平衡调整值，仅更改数据文件 - 没有新的代码逻辑 |

混合故事：分配具有最高实施风险的类型。
该类型决定了 `/story-done` 结束故事之前需要哪些测试证据。

---

## 4. 将 GDD 分解为故事

对于每个 GDD 验收标准：

1. 需要相同核心实现的组相关标准
2. 每组=一个故事
3. 对故事进行排序：首先是基础行为，最后是边缘情况，最后是 UI

**故事大小规则：** 一个故事 = 一次重点会议（约 2-4 小时）。如果一个
一组标准需要更长的时间，分为两个故事。

对于每个故事，确定：
- **GDD 要求**：这满足哪个验收标准（ia）？
- **TR-ID**：在 `tr-registry.yaml` 中查找。使用稳定的 ID。如果不匹配，则使用 `TR-[system]-???` 并发出警告。
- **管理 ADR**：哪个 ADR 管理如何实现这一点？
  - `Status: Accepted` → 正常嵌入
  - `Status: Proposed` → 设置故事 `Status: Blocked`，并附注：“已封锁：建议 ADR-NNNN — 运行 `/architecture-decision` 来推进它”
- **故事类型**：来自第 3 步分类
- **引擎风险**：来自 ADR 的知识风险字段

---

## 4b. QA 主要故事准备门

**查看模式检查** — 在生成 QL-STORY-READY 之前应用：
- `solo` → 跳过。注意：“已跳过 QL-STORY-READY — 单人模式。”继续执行步骤 5（呈现故事以供审核）。
- `lean` → 跳过（不是相位门）。注意：“已跳过 QL-STORY-READY — 精益模式。”继续执行步骤 5（呈现故事以供审核）。
- `full` → 正常生成。

分解所有故事后（完成第 4 步），但在提交它们进行写入批准之前，使用门 **QL-STORY-READY** (`.codex/docs/director-gates.md`) 通过 Task 生成 `qa-lead`。

通过：包含接受标准、故事类型和 TR-ID 的完整故事列表；史诗的GDD验收标准可供参考。

呈现 QA 领导的评估。对于标记为差距或不充分的每个故事，请在继续之前修改验收标准 - 具有无法测试标准的故事无法正确实施。一旦所有故事都达到足够水平，就继续。

**充分之后**：对于每个逻辑和集成故事，请质量保证负责人制定具体的测试用例规范 - 每个验收标准一个 - 采用以下格式：

```
Test: [criterion text]
  Given: [precondition]
  When: [action]
  Then: [expected result / assertion]
  Edge cases: [boundary values or failure states to test]
```

对于 Visual/Feel 和 UI 故事，请改为生成手动验证步骤：
```
Manual check: [criterion text]
  Setup: [how to reach the state]
  Verify: [what to look for]
  Pass condition: [unambiguous pass description]
```

这些测试用例规范直接嵌入到每个故事的 `## QA Test Cases` 部分中。开发人员针对这些情况实施。程序员不会从头开始编写测试 - QA 已经定义了“完成”的样子。

---

## 5. 呈现故事供回顾

在编写任何文件之前，请提供完整的故事列表：

```
## Stories for Epic: [name]

Story 001: [title] — Logic — ADR-NNNN
  Covers: TR-[system]-001 ([1-line summary of requirement])
  Test required: tests/unit/[system]/[slug]_test.[ext]

Story 002: [title] — Integration — ADR-MMMM
  Covers: TR-[system]-002, TR-[system]-003
  Test required: tests/integration/[system]/[slug]_test.[ext]

Story 003: [title] — Visual/Feel — ADR-NNNN
  Covers: TR-[system]-004
  Evidence required: production/qa/evidence/[slug]-evidence.md

[N stories total: N Logic, N Integration, N Visual/Feel, N UI, N Config/Data]
```

使用 `AskUserQuestion`：
- 提示：“我可以将这些 [N] 故事写入 `production/epics/[epic-slug]/` 吗？”
- 选项：`[A] Yes — write all [N] stories` / `[B] Not yet — I want to review or adjust first`

---

## 6. Write 故事文件

对于每个故事，请写入 `production/epics/[epic-slug]/story-[NNN]-[slug].md`：

```markdown
# Story [NNN]: [title]

> **Epic**: [epic name]
> **Status**: Ready
> **Layer**: [Foundation / Core / Feature / Presentation]
> **Type**: [Logic | Integration | Visual/Feel | UI | Config/Data]
> **Manifest Version**: [date from control-manifest.md header]

## Context

**GDD**: `design/gdd/[filename].md`
**Requirement**: `TR-[system]-NNN`
*(Requirement text lives in `docs/architecture/tr-registry.yaml` — read fresh at review time)*

**ADR Governing Implementation**: [ADR-NNNN: title]
**ADR Decision Summary**: [1-2 sentence summary of what the ADR decided]

**Engine**: [name + version] | **Risk**: [LOW / MEDIUM / HIGH]
**Engine Notes**: [from ADR Engine Compatibility section — post-cutoff APIs, verification required]

**Control Manifest Rules (this layer)**:
- Required: [relevant required pattern]
- Forbidden: [relevant forbidden pattern]
- Guardrail: [relevant performance guardrail]

---

## Acceptance Criteria

*From GDD `design/gdd/[filename].md`, scoped to this story:*

- [ ] [criterion 1 — directly from GDD]
- [ ] [criterion 2]
- [ ] [performance criterion if applicable]

---

## Implementation Notes

*Derived from ADR-NNNN Implementation Guidelines:*

[Specific, actionable guidance from the ADR. Do not paraphrase in ways that
change meaning. This is what the programmer reads instead of the ADR.]

---

## Out of Scope

*Handled by neighbouring stories — do not implement here:*

- [Story NNN+1]: [what it handles]

---

## QA Test Cases

*Written by qa-lead at story creation. The developer implements against these — do not invent new test cases during implementation.*

**[For Logic / Integration stories — automated test specs]:**

- **AC-1**: [criterion text]
  - Given: [precondition]
  - When: [action]
  - Then: [assertion]
  - Edge cases: [boundary values / failure states]

**[For Visual/Feel / UI stories — manual verification steps]:**

- **AC-1**: [criterion text]
  - Setup: [how to reach the state]
  - Verify: [what to look for]
  - Pass condition: [unambiguous pass description]

---

## Test Evidence

**Story Type**: [type]
**Required evidence**:
- Logic: `tests/unit/[system]/[story-slug]_test.[ext]` — must exist and pass
- Integration: `tests/integration/[system]/[story-slug]_test.[ext]` OR playtest doc
- Visual/Feel: `production/qa/evidence/[story-slug]-evidence.md` + sign-off
- UI: `production/qa/evidence/[story-slug]-evidence.md` or interaction test
- Config/Data: smoke check pass (`production/qa/smoke-*.md`)

**Status**: [ ] Not yet created

---

## Dependencies

- Depends on: [Story NNN-1 must be DONE, or "None"]
- Unlocks: [Story NNN+1, or "None"]
```

### 同时更新 `production/epics/[epic-slug]/EPIC.md`

将“故事：尚未创建”行替换为填充的表：

```markdown
## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [title] | Logic | Ready | ADR-NNNN |
| 002 | [title] | Integration | Ready | ADR-MMMM |
```

---

## 7. 写完之后

使用 `AskUserQuestion` 关闭上下文感知的后续步骤：

Check:
- `production/epics/` 中还有其他没有故事的史诗吗？列出它们。
- 这是最后的史诗了吗？如果是这样，请包含 `/sprint-plan` 作为选项。

Widget:
- 提示：“[N] 故事写入 `production/epics/[epic-slug]/`。接下来做什么？”
- 选项（包括所有适用的选项）：
  - `[A] Start implementing — run /story-readiness [first-story-path]`（推荐）
  - `[B] Create stories for [next-epic-slug] — run /create-stories [slug]`（仅当其他史诗还没有故事时）
  - `[C] Plan the sprint — run /sprint-plan`（仅当所有史诗都有故事时）
  - `[D] Stop here for this session`

输出中的注释：“按顺序完成故事 - 每个故事的 `Depends on:` 字段告诉您在开始之前必须完成哪些操作。”

---

## 协作协议

1. **呈现前 Read** — 在显示故事列表之前以静默方式加载所有输入
2. **询问一次** — 在一份摘要中呈现史诗的所有故事，而不是一次一个
3. **对被阻止的故事发出警告** — 在写入之前用“提议的 ADR”标记任何故事
4. **写作前询问** — 在编写文件之前获得完整故事集的批准
5. **无发明** — 验收标准来自 GDD，实施说明来自 ADR，规则来自舱单
6. **永远不要开始实施** - 此技能停止在故事文件级别

写信后（或拒绝）：

- **结论：完整** — [N] 故事写入 `production/epics/[epic-slug]/`。运行 `/story-readiness` → `/dev-story` 开始实施。
- **判决：被阻止** - 用户拒绝。没有写故事文件。
