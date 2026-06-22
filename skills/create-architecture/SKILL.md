---
name: create-architecture
description: "指导性地、逐节地创作游戏的主架构文档。在编写任何代码之前，读取所有 GDD、系统索引、现有 ADR 和引擎参考库，以生成完整的架构蓝图。引擎版本感知：标记知识差距并根据固定的引擎版本验证决策。"
---

# 创建架构

这项技能产生了 `docs/architecture/architecture.md`——主架构
将所有批准的 GDD 转化为具体技术蓝图的文件。
它位于设计和实现之间，并且必须在冲刺计划开始之前存在。

**与 `/architecture-decision` 不同**：ADR 记录各个点的决策。
这项技能创建了整个系统蓝图，为 ADR 提供了背景。

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果`--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

**论证模式：**
- **无参数/`full`**：完整的指导演练 - 所有部分，从头到尾
- **`layers`**：仅关注系统层图
- **`data-flow`**：仅关注模块之间的数据流
- **`api-boundaries`**：仅关注 API 边界定义
- **`adr-audit`**：仅审核现有 ADR 的引擎兼容性差距

---

## 阶段 0：加载所有上下文

首先，按以下顺序加载完整的项目上下文：

### 0a。引擎上下文（关键）

Read完整的引擎参考库：

1. `docs/engine-reference/[engine]/VERSION.md`
   → 摘录：引擎名称、版本、LLM 截止、截止后风险级别
2. `docs/engine-reference/[engine]/breaking-changes.md`
   → 摘录：所有高风险和中风险变更
3. `docs/engine-reference/[engine]/deprecated-apis.md`
   → 摘录：要避免的 API
4. `docs/engine-reference/[engine]/current-best-practices.md`
   → 摘录：与训练数据不同的截止后最佳实践
5. `docs/engine-reference/[engine]/modules/` 中的所有文件
   → 提取：每个域的当前 API 模式

如果没有配置引擎，则停止并提示：
> “未配置引擎。先运行`/setup-engine`。架构无法
> 在不知道您的目标引擎和版本的情况下编写的。”

### 0b。设计背景+技术需求提取

Read 所有批准的设计文件并从每个文件中提取技术要求：

1. `design/gdd/game-concept.md` — 游戏支柱、类型、核心循环
2. `design/gdd/systems-index.md` — 所有系统、依赖项、优先级
3. `.codex/docs/technical-preferences.md` — 命名约定、性能预算、
   允许的库，禁止的模式
4. **`design/gdd/` 中的每个 GDD** — 对于每个 GDD，提取技术要求：
   - 游戏规则隐含的数据结构
   - 明示或暗示的性能限制
   - 系统所需的引擎功能
   - 跨系统通信模式（什么与什么对话、如何对话）
   - 必须持续存在的状态（save/load 含义）
   - 线程或时序要求

建立 **技术要求基线** - 所有提取的简单列表
所有 GDD 的要求，编号为 `TR-[gdd-slug]-[NNN]`。这是
架构必须涵盖的完整集合。将其呈现为：

```
## Technical Requirements Baseline
Extracted from [N] GDDs | [X] total requirements

| Req ID | GDD | System | Requirement | Domain |
|--------|-----|--------|-------------|--------|
| TR-combat-001 | combat.md | Combat | Hitbox detection per-frame | Physics |
| TR-combat-002 | combat.md | Combat | Combo state machine | Core |
| TR-inventory-001 | inventory.md | Inventory | Item persistence | Save/Load |
```

该基线会影响到每个后续阶段。不应有 GDD 要求
到本次会议结束时，还没有做出支持它的架构决策。

### 0c。现有架构决策

Read `docs/architecture/` 中的所有文件了解已经决定的内容。
列出找到的所有 ADR 及其域。

### 0d。生成知识差距清单

在继续之前，显示结构化摘要：

```
## Engine Knowledge Gap Inventory
Engine: [name + version]
LLM Training Covers: up to approximately [version]
Post-Cutoff Versions: [list]

### HIGH RISK Domains (must verify against engine reference before deciding)
- [Domain]: [Key changes]

### MEDIUM RISK Domains (verify key APIs)
- [Domain]: [Key changes]

### LOW RISK Domains (in training data, likely reliable)
- [Domain]: [no significant post-cutoff changes]

### Systems from GDD that touch HIGH/MEDIUM risk domains:
- [GDD system name] → [domain] → [risk level]
```

询问：“此清单标识了高风险引擎域中的 [N] 系统。我可以吗？
继续构建带有这些警告标记的架构吗？”

---

## 第一阶段：系统层映射

将 `systems-index.md` 中的每个系统映射到架构层。标准
游戏架构层为：

```
┌─────────────────────────────────────────────┐
│  PRESENTATION LAYER                         │  ← UI, HUD, menus, VFX, audio
├─────────────────────────────────────────────┤
│  FEATURE LAYER                              │  ← gameplay systems, AI, quests
├─────────────────────────────────────────────┤
│  CORE LAYER                                 │  ← physics, input, combat, movement
├─────────────────────────────────────────────┤
│  FOUNDATION LAYER                           │  ← engine integration, save/load,
│                                             │    scene management, event bus
├─────────────────────────────────────────────┤
│  PLATFORM LAYER                             │  ← OS, hardware, engine API surface
└─────────────────────────────────────────────┘
```

对于每个 GDD 系统，询问：
- 它属于哪一层？
- 它的模块边界是什么？
- 它独家拥有什么？ （数据、状态、行为）

提出建议的层分配并在继续之前请求批准
下一节。 Write 将批准的图层图立即添加到骨架文件中。

**引擎意识检查**：对于分配给核心和基础的每个系统
层，如果涉及高风险或中风险引擎域，则进行标记。显示相关
内嵌引擎参考摘录。

---

## 第 2 阶段：模块所有权图

对于阶段 1 中定义的每个模块，定义所有权：

- **拥有**：该模块单独负责哪些数据和状态
- **暴露**：其他模块可以读取或调用什么
- **消耗**：从其他模块读取的内容
- **使用的引擎 API**：此模块使用哪个特定引擎 classes/nodes/signals
  直接调用（注明版本和风险级别）

格式化为每层表格，然后格式化为 ASCII 依赖关系图。

**引擎意识检查**：对于列出的每个引擎 API，根据
相关模块参考文档。如果 API 是截止后的，则将其标记为：

```
⚠️  [ClassName.method()] — Godot 4.6 (post-cutoff, HIGH risk)
    Verified against: docs/engine-reference/godot/modules/[domain].md
    Behaviour confirmed: [yes / NEEDS VERIFICATION]
```

在编写之前获得用户对所有权图的批准。

---

## 第三阶段：数据流

定义在关键游戏场景期间数据如何在模块之间移动。至少覆盖：

1. **帧更新路径**：输入→核心系统→状态→渲染
2. **Event/signal 路径**：系统如何在没有紧密耦合的情况下进行通信
3. **Save/load路径**：序列化什么状态，哪个模块拥有序列化
4. **初始化顺序**：哪些模块必须先于其他模块启动

如果有帮助，请使用 ASCII 序列图。对于每个数据流：
- 命名正在传输的数据
- 识别生产者和消费者
- 说明这是同步调用、signal/event 还是共享状态
- 标记任何跨越线程边界的数据流

在编写之前获得每个场景的用户批准。

---

## 第 4 阶段：API 边界

定义模块之间的公共合约。对于每个边界：

- 模块向系统其余部分公开的接口是什么？
- 入口点是什么（functions/signals/properties）？
- 调用者必须遵守哪些不变量？
- 模块必须向调用者保证什么？

Write 伪代码或项目的实际语言（来自技术偏好）。
这些成为程序员实施的合同。

**引擎感知检查**：如果任何接口使用特定于引擎的类型（例如
`Node`、`Resource`、Godot 中的 `Signal`)，标记版本并验证类型
存在且未更改目标引擎版本中的签名。

---

## 第 5 阶段：ADR 审核 + 可追溯性检查

根据内置架构审查阶段 0c 中的所有现有 ADR
第 1-4 阶段以及第 0b 阶段的技术要求基线。

### ADR 质量检查

对于每个 ADR：
- [ ] 它有引擎兼容性部分吗？
- [ ] 是否记录了引擎版本？
- [ ] 截止后 API 是否被标记？
- [ ] 它是否有“GDD 已解决的要求”部分？
- [ ] 它与本次会议中做出的 layer/ownership 决定是否冲突？
- [ ] 它对于固定引擎版本仍然有效吗？

| ADR | 发动机兼容性 | Version | GDD 联动 | Conflicts | Valid |
|-----|--------------|---------|-------------|-----------|-------|
| ADR-0001：[title] | ✅/❌ | ✅/❌ | ✅/❌ | None/[conflict] | ✅/⚠️ |

### 可追溯性覆盖范围检查

将技术要求基线中的每项要求映射到现有 ADR。
对于每个要求，检查是否有任何 ADR 的“GDD 已解决的要求”部分
或决策文本涵盖它：

| Req ID | Requirement | ADR 覆盖范围 | Status |
|--------|-------------|--------------|--------|
| TR-combat-001 | 每帧的 Hitbox 检测 | ADR-0003 | ✅ |
| TR-combat-002 | 组合状态机 | — | ❌ 差距 |

计数：X 已覆盖，Y 是间隙。对于每个间隙，它都会成为**必需的新 ADR**。

### 所需的新 ADR

列出本次架构会议（阶段 1-4）期间所做的所有决策
尚未有相应的 ADR，以及所有未涵盖的技术要求。
逐层分组——基础优先：

**基础层（必须在任何编码之前创建）：**
- `/architecture-decision [title]` → 涵盖：TR-[id]、TR-[id]

**核心层：**
- `/architecture-decision [title]` → 盖：TR-[id]

---

## 第 6 阶段：缺少 ADR 列表

基于完整的架构，生成应该存在的 ADR 的完整列表
但还没有。按优先级分组：

**在编码开始之前必须具备（基础和核心决策）：**
- [例如《场景管理和场景加载策略》]
- [例如“事件总线与直接信号架构”]

**相关系统搭建前应具备：**
- [例如“库存序列化格式”]

**可以推迟实施：**
- [例如“水的特定着色器技术”]

---

## 第 7 阶段：Write 主架构文档

一旦所有部分都获得批准，请将完整的文件写入
`docs/architecture/architecture.md`.

问：“我可以将主架构文档写入`docs/architecture/architecture.md`吗？”

文档结构：

```markdown
# [Game Name] — Master Architecture

## Document Status
- Version: [N]
- Last Updated: [date]
- Engine: [name + version]
- GDDs Covered: [list]
- ADRs Referenced: [list]

## Engine Knowledge Gap Summary
[Condensed from Phase 0d inventory — HIGH/MEDIUM risk domains and their implications]

## System Layer Map
[From Phase 1]

## Module Ownership
[From Phase 2]

## Data Flow
[From Phase 3]

## API Boundaries
[From Phase 4]

## ADR Audit
[From Phase 5]

## Required ADRs
[From Phase 6]

## Architecture Principles
[3-5 key principles that govern all technical decisions for this project,
derived from the game concept, GDDs, and technical preferences]

## Open Questions
[Decisions deferred — must be resolved before the relevant layer is built]
```

---

## 第 7b 阶段：技术总监签字 + 首席程序员可行性审查

编写主架构文档后，在移交之前执行明确的签核。

**第 1 步 — 技术总监自我审查**（此技能以技术总监身份运行）：

应用门 **TD-ARCHITECTURE** (`.codex/docs/director-gates.md`) 作为自我审查。根据已完成的文档检查该门定义中的所有四个标准。

**审查模式检查** — 在生成 LP 可行性之前应用：
- `solo` → 跳过。注意：“LP-FEASIBILITY 已跳过 — 独奏模式。”进入第 8 阶段交接。
- `lean` → 跳过（不是相位门）。注意：“LP-FEASIBILITY 已跳过 — 精益模式。”进入第 8 阶段交接。
- `full` → 正常生成。

**步骤 2 — 使用门 LP 可行性 (`.codex/docs/director-gates.md`) 通过 Task 生成 `lead-programmer`：**

通过：架构文档路径、技术需求基线摘要、ADR列表。

**第 3 步 — 向用户呈现两项评估：**

并排显示技术总监的评估和首席程序员的结论。

使用 `AskUserQuestion` —“技术总监和首席程序员已经审查了架构。您想如何继续？”
选项：`Accept — proceed to handoff` / `Revise flagged items first` / `Discuss specific concerns`

**第 4 步 — 在架构文档中记录签核：**

更新文档状态部分：
```
- Technical Director Sign-Off: [date] — APPROVED / APPROVED WITH CONDITIONS
- Lead Programmer Feasibility: FEASIBLE / CONCERNS ACCEPTED / REVISED
```

问：“我可以更新 `docs/architecture/architecture.md` 中的文档状态部分并进行签核吗？”

---

## 第 8 阶段：交接

编写文档后，提供清晰的交接：

1. **接下来运行这些 ADR**（从第 6 阶段开始，优先）：列出前 3 个
2. **门检查**：“主架构文档已完成。运行`/gate-check
   预生产`，所有必需的 ADR 也都已编写完毕。”
3. **更新会话状态**：Write `production/session-state/active.md` 的摘要

---

## 协作协议

该技能在每个阶段都遵循协作设计原则：

1. **静默加载上下文** - 不叙述文件读取
2. **当前发现** — 显示知识差距清单和层建议
3. **决定前先询问** - 为每个架构选择提供选项
4. **写作前获得批准** - 每个阶段部分仅在之后编写
   用户批准内容
5. **增量写作**——立即编写每个批准的部分；不
   积累一切并写在最后。这可以避免会话崩溃。

在没有用户输入的情况下，切勿做出具有约束力的架构决策。如果用户是
不确定，请在要求他们做出决定之前向 pros/cons 提供 2-4 个选项。

---

## 建议的后续步骤

- 为阶段 6 中列出的每个必需的 ADR 运行 `/architecture-decision [title]` — 首先是基础层 ADR
- 写入所需的 ADR 以生成层规则清单后，运行 `/create-control-manifest`
- 当所有必需的 ADR 都已写入并且架构已签核时，运行 `/gate-check pre-production`
