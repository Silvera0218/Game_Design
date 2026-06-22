---
name: story-readiness
description: "验证故事文件是否已准备好实施。检查嵌入式 GDD 要求、ADR 参考、引擎说明、明确的验收标准，并且没有开放的设计问题。产生具有特定间隙的“就绪”/“需要工作”/“阻止”判决。当用户说“这个故事准备好了吗”、“我可以开始这个故事吗”、“故事 X 准备好实施了吗”时使用。"
---

# 故事准备

此技能验证故事文件包含开发人员所需的所有内容
开始实施——没有中间冲刺设计中断，没有猜测，
没有模糊的验收标准。在分配故事之前运行它。

**此技能是只读的。**它从不编辑故事文件。它报告了调查结果
并询问用户是否需要帮助来填补空白。

**输出：** 每个故事的判决（就绪/需要工作/已阻止），具有特定的
每个未准备好的故事的差距列表。

---

## 第0阶段：解决审核模式

在启动时解决一次审查模式（存储此运行中产生的所有门）：

1. 如果使用`--review [完整|lean|独奏]`→使用该值
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整的检查模式和模式定义，请参阅 `.codex/docs/director-gates.md`。

---

## 1. 解析参数

**范围：** `$ARGUMENTS[0]`（空白 = 通过 AskUserQuestion 询问用户）

- **具体路径**（例如，`/story-readiness production/epics/combat/story-001-basic-attack.md`）：
  验证该单个故事文件。
- **`sprint`**：从`production/sprints/`读取当前的冲刺计划（大多数
  最近的文件），提取它引用的每个故事路径，验证每个路径。
- **`all`**：glob `production/epics/**/*.md`，排除 `EPIC.md` 索引文件，
  验证找到的每个故事文件。
- **无参数**：询问用户要验证的范围。

如果未给出参数，则使用 `AskUserQuestion`：
- “你想确认什么？”
  - 选项：“特定故事文件”、“当前冲刺中的所有故事”、
    “production/epics/ 中的所有故事”、“特定史诗的故事”

在继续之前报告范围：“验证 [N] 故事文件。”

---

## 2. 加载支持上下文

在检查任何故事之前，加载一次参考文档（不是每个故事）：

- `design/gdd/systems-index.md` — 了解哪些系统已批准 GDD
- `docs/architecture/control-manifest.md` — 了解存在哪些清单规则
  （如果文件不存在，请将其标记为丢失一次；不要为每个故事重新标记）
  如果文件存在，还可以从标头块中提取 `Manifest Version:` 日期。
- `docs/architecture/tr-registry.yaml` — 按 `id` 索引所有条目。习惯于
  验证故事中的 TR-ID。如果该文件不存在，则记下一次； TR-ID
  检查将自动通过所有故事（注册表早于故事，因此缺少
  注册表意味着故事来自引入 TR 跟踪之前）。
- 所有 ADR 状态字段 - 对于整个故事中引用的每个唯一的 ADR
  检查后，读取 ADR 文件并记下其 `Status:` 字段。缓存这些以便您
  不要为每个故事重新阅读相同的 ADR。
- 当前的冲刺文件（如果范围是 `sprint`）— 识别必须具备 /
  应优先考虑升级决策

---

## 3. 故事准备清单

对于每个故事文件，评估下面的每一项。只有满足以下条件，故事才算准备就绪
项目通过或明确标记为 N/A 并注明原因。

### 设计完整性

- [ ] **参考 GDD 要求**：故事包含 `design/gdd/` 路径
  并引用或链接特定要求、接受标准或规则
  GDD — 不仅仅是 GDD 文件名。没有追踪的文档链接
  特定要求未通过。
- [ ] **要求是独立的**：故事中的接受标准
  无需打开 GDD 即可理解。开发人员不应该需要
  请阅读单独的文档以了解 DONE 的含义。
- [ ] **验收标准是可测试的**：每个标准都是一个特定的、
  可观察的条件——不是“实施X”或“系统正常工作”。
  坏例子：“实施跳跃机制。”很好的例子：“跳跃到达
  保持跳跃时 0.3 秒内最大高度为 5 个单位。”
- [ ] **没有验收标准需要判断**：标准如
  如果没有定义，“感觉响应”或“看起来不错”是不可测试的
  基准。这些必须用特定的可观察条件或
  游戏测试协议。

### 架构完整性

- [ ] **引用 ADR 或声明 N/A**：故事至少引用一个 ADR，
  OR 明确声明“ADR 不适用”并附上简短的理由。
  没有 ADR 引用且没有明确的 N/A 注释的故事无法通过此检查。
- [ ] **ADR 已接受（未建议）**：对于每个引用的 ADR，检查其
  `Status:` 字段使用第 2 节中加载的缓存 ADR 状态。
  - 如果`Status: Accepted`→通过。
  - 如果 `Status: Proposed` → **BLOCKED**：ADR 在被接受之前可能会发生变化，
    而且故事的实施指导可能是错误的。
    修复：`BLOCKED: ADR-NNNN is Proposed — wait for acceptance before implementing.`
  - 如果 ADR 文件不存在 → **BLOCKED**：引用的 ADR 丢失。
  - 如果故事有明确的“ADR 不适用”N/A 注释，则自动通过。
- [ ] **TR-ID 有效且处于活动状态**：如果故事包含 `TR-[system]-NNN`
  参考，在第 2 节加载的 TR 注册表中查找它。
  - 如果 ID 存在且 `status: active` → 通过。
  - 如果 ID 存在且 `status: deprecated` 或 `status: superseded-by: ...` →
    需要工作：该要求已被删除或替换。
    修复：更新故事以引用当前的需求 ID 或删除（如果不再适用）。
  - 如果注册表中不存在该 ID → 需要处理：ID 未注册
    （故事可能早于注册表，或者注册表需要 `/architecture-review` 运行）。
  - 如果故事没有 TR-ID 引用或注册表不存在，则自动通过。
- [ ] **清单版本是最新的**：如果故事有 `Manifest Version:` 日期
  在其标头中并且 `docs/architecture/control-manifest.md` 存在：
  - 如果故事版本与当前清单 `Manifest Version:` 匹配 → 通过。
  - 如果故事版本早于当前清单 → 需要工作：新规则可能
    申请。修复：查看更改的清单规则，更新故事（如果有）forbidden/required
    条目发生更改，然后将故事的 `Manifest Version:` 更新为当前。
  - 如果故事没有 `Manifest Version:` 字段或清单，则自动通过
不存在。
- [ ] **存在引擎注释**：对于任何后截止引擎 API 这个故事
  可能会触及，实施说明或验证要求是
  包括在内。如果故事显然没有触及引擎 API（例如，它是一个
  纯 data/config 更改），“N/A — 不涉及引擎 API”是可以接受的。
- [ ] **注意控制清单规则**：来自控制的相关层规则
  引用清单，或声明“N/A — 清单尚未创建”。
  如果 `docs/architecture/control-manifest.md` 没有，则此项自动通过
  尚存在（不要惩罚在创建清单之前编写的故事）。

### 范围清晰

- [ ] **估计目前**：故事包括大小估计（小时、
  分，或 T 恤尺寸）。没有估计的故事是无法策划的。
- [ ] **规定范围内/范围外边界**：故事说明了什么
  它不包括，无论是在明确的超出范围部分还是在
  使边界变得明确的语言。如果没有这个，范围就会蔓延
  在实施过程中是有可能的。
- [ ] **列出的故事依赖关系**：如果此故事依赖于其他故事
  首先完成后，会列出这些故事 ID。如果没有依赖关系，
  “无”被明确说明（不仅仅是省略）。

### 开放性问题

- [ ] **没有未解决的设计问题**：故事不包含文字
  标记为“UNRESOLVED”、“TBD”、“TODO”、“?”或等效标记
  任何验收标准、实施说明或规则声明。
- [ ] **依赖故事不在 DRAFT 中**：对于列为
  依赖项，检查文件是否存在且不具有 DRAFT 状态。一个
  依赖于草稿或缺失故事的故事被阻止，而不仅仅是
  需要工作。

### 资产参考检查

- [ ] **存在引用的资产**：扫描故事文本以获取资产路径模式
  （包含 `assets/` 的路径，或文件扩展名 `.png`、`.jpg`、`.svg`、
  `.wav`、`.ogg`、`.mp3`、`.glb`、`.gltf`、`.tres`、`.tscn`、`.res`）。
  - 对于找到的每个资产路径：使用 Glob 检查文件是否存在。
  - 如果任何引用的资产不存在：**需要工作** - 记下缺失的资产
    路径。 （该故事引用了尚未创建的资产。
    删除引用、创建占位符或将其标记为
    对资产创建故事的明确依赖。）
  - 如果所有引用的资产都存在：请注意“引用的资产已验证：
    找到 [count]。”
  - 如果故事中没有引用资产路径：请注意“没有资产引用
    在故事中发现——跳过资产检查。”该项目自动通过。
  - 这是仅存在性检查。不验证文件格式或内容。

### 完成的定义

- [ ] **至少 3 个可测试的验收标准**：建议少于 3 个
  这个故事要么很小（应该是一个故事吗？），要么不具体。
- [ ] **如果适用，注明绩效预算**：如果这个故事涉及到任何
  游戏循环、渲染或物理的一部分、性能预算或
  存在“预计不会影响性能 - [reason]”的注释。
- [ ] **声明的故事类型**：故事的标题中包含 `Type:` 字段
  识别测试类别（逻辑/集成/Visual/Feel / UI / Config/Data）。
  如果没有这个，测试证据要求就无法在故事结束时得到执行。
  修复：添加`类型：[逻辑|Integration|Visual/Feel|UI|Config/Data]` 添加到故事标题。
- [ ] **测试证据要求明确**：如果设置了Story Type，则故事
  包括 `## Test Evidence` 部分，说明证据的存储位置
  （Logic/Integration 的测试文件路径，或 Visual/Feel/UI 的证据文档路径）。
  修复：添加 `## Test Evidence` 以及故事类型的预期证据位置。

---

## 4. 判决分配

为每个故事指定三个判决之一：

**就绪** — 所有清单项目均通过或具有明确的 N/A 理由。
故事可以立即分配。

**需要工作** — 一个或多个清单项目失败，但所有依赖关系故事
存在且不是 DRAFT。故事可以在分配之前确定。

**已阻止** — 一个或多个依赖关系故事丢失或处于草稿状态，
或者关键设计问题（在标准或规则中标记为“未解决”）
没有主人。在解决阻碍之前，无法分配故事。注意：
被阻止的故事也可能有需要工作的项目 - 列出两者。

---

## 5. 输出格式

### 单故事输出

```
## Story Readiness: [story title]
File: [path]
Verdict: [READY / NEEDS WORK / BLOCKED]

### Passing Checks (N/[total])
[list passing items briefly]

### Gaps
- [Checklist item]: [exact description of what is missing or wrong]
  Fix: [specific text needed to resolve this gap]

### Blockers (if BLOCKED)
- [What is blocking]: [story ID or design question that must resolve first]
```

### 多故事聚合输出

```
## Story Readiness Summary — [scope] — [date]

Ready:      [N] stories
Needs Work: [N] stories
Blocked:    [N] stories

### Ready Stories
- [story title] ([path])

### Needs Work
- [story title]: [primary gap — one line]
- [story title]: [primary gap — one line]

### Blocked Stories
- [story title]: Blocked by [story ID / design question]

---
[Full detail for each non-ready story follows, using the single-story format]
```

### 冲刺升级

如果范围是 `sprint` 并且任何必备故事都需要工作或被阻止，
在输出顶部添加一个显着的警告：

```
WARNING: [N] Must Have stories are not implementation-ready.
[List them with their primary gap or blocker.]
Resolve these before the sprint begins or replan with `/sprint-plan update`.
```

---

## 6. 协作协议

该技能是只读的。它从不建议编辑或要求写入文件。

报告调查结果后，提供：

“您需要帮助填补这些故事中的空白吗？我可以
起草缺失的部分供您批准。”

如果用户对特定故事表示同意，则仅起草缺失的部分
在谈话中。请勿使用 Write 或 Edit 工具 — 用户（或
`/create-stories`) 处理写入。

**重定向规则：**
- 如果故事文件根本不存在：“该故事文件完全丢失。
  运行 `/create-epics [layer]`，然后运行 `/create-stories [epic-slug]`，以从 GDD 和 ADR 生成故事。”
- 如果一个故事没有 GDD 参考并且作品看起来很小：“这个故事有
没有 GDD 参考。如果变化很小（不到 4 小时），请运行
  `/quick-design [description]` 创建快速设计规范，然后参考
  故事中的那个规格。”
- 如果故事的范围超出了其原始规模：“这个故事出现了
  范围有所扩大。考虑将其拆分或升级给生产者
  在实施开始之前。”

---

## 7. 下一个故事的交接

完成单层就绪检查后（不是 `all` 或 `sprint` 范围）：

1. Read `production/sprints/`（最新）的当前冲刺文件。
2. 查找以下故事：
   - 状态：准备好或未开始
   - 不是刚刚查到的故事
   - 不被不完整的依赖关系阻塞
   - 属于必须拥有或应该拥有的级别

如果找到的话，最多显示 3 个：

```
### Other Ready Stories in This Sprint

1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `/story-readiness [path]` to validate before starting.
```

如果不存在冲刺文件或未找到其他准备好的故事，请直接跳过此部分。

---

## 第 8 阶段：导演之门 — 故事准备情况审核

在生成 QL-STORY-READY 之前应用第 0 阶段解决的审阅模式：

- `solo` → 跳过。注意：“已跳过 QL-STORY-READY — 单人模式。”继续关闭。
- `lean` → 跳过。注意：“已跳过 QL-STORY-READY — 精益模式。”继续关闭。
- `full` → 正常生成。

使用门 **QL-STORY-READY** (`.codex/docs/director-gates.md`) 通过 Task 生成 `qa-lead`。

传递以下上下文：
- 故事标题
- 验收标准列表（故事验收标准部分的所有项目）
- 依赖关系状态（列出的所有依赖关系及其当前状态：存在/草案/缺失）
- 第 4 阶段的总体结论（就绪/需要工作/已阻止）

按照`director-gates.md`中的标准规则处理判决：
- **足够**→故事已清除。继续关闭。
- **间隙 [list]** → 通过 `AskUserQuestion` 向用户显示特定间隙：
  选项：`Update story with suggested gaps` / `Accept and proceed anyway` / `Discuss further`。
- **不充分** → 明确具体差距；询问用户是否更新故事或继续。

---

## 建议的后续步骤

- 故事准备就绪后，运行 `/dev-story [story-path]` 以开始实施
- 运行 `/story-readiness sprint` 以立即检查当前冲刺中的所有故事
- 如果故事文件完全丢失，请运行 `/create-stories [epic-slug]`
