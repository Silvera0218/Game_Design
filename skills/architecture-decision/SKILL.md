---
name: architecture-decision
description: "创建架构决策记录 (ADR)，记录重要的技术决策、其背景、考虑的替代方案以及后果。每个主要技术选择都应该有一个 ADR。"
---

当该技能被调用时：

## 0. 解析参数——检测改造模式

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果`--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

**如果参数以 `retrofit` 开头，后跟文件路径**
(e.g., `/architecture-decision retrofit docs/architecture/adr-0001-事件系统.md`):

进入**改造模式**：

1. Read 与现有的 ADR 文件完全一致。
2. 通过扫描标题来识别存在哪些模板部分：
   - `## Status` — **如果缺失则阻塞**：`/story-readiness` 无法检查 ADR 接受情况
   - `## ADR Dependencies` — 如果缺失则为高：依赖顺序中断
   - `## Engine Compatibility` — 如果缺失则为高：截止后风险未知
   - `## GDD Requirements Addressed` — 如果缺失则为中等：可追溯性丢失
3. 呈现给用户：
   ```
   ## Retrofit: [ADR title]
   File: [path]

   Sections already present (will not be touched):
   ✓ Status: [current value, or "MISSING — will add"]
   ✓ [section]

   Missing sections to add:
   ✗ Status — BLOCKING (stories cannot validate ADR acceptance without this)
   ✗ ADR Dependencies — HIGH
   ✗ Engine Compatibility — HIGH
   ```
4. 问：“我要添加 [N] 缺失的部分吗？我不会修改任何现有内容。”
5. If yes:
   - 对于 **状态**：询问用户 —“此决定的当前状态是什么？”
     选项：“建议”、“已接受”、“已弃用”、“由 ADR-XXXX 取代”
   - 对于 **ADR 依赖关系**：询问 —“此决定是否依赖于任何其他 ADR？
     它是否启用或阻止任何其他 ADR 或史诗？”每个字段接受“无”。
   - 对于 **引擎兼容性**：阅读引擎参考文档（与下面的步骤 1 相同）
     并要求用户确认域名。然后生成带有验证数据的表。
   - 对于 **GDD 满足的要求**：询问 —“哪个 GDD 系统促使了这一决定？
     此 ADR 满足每个 GDD 中的哪些具体要求？”
   - 使用 Edit 工具将每个缺失的部分附加到 ADR 文件。
   - **切勿修改任何现有部分。** 仅附加或填充缺少的部分。
6. 添加所有缺失的部分后，更新 ADR 的 `## Date` 字段（如果不存在）。
7. 建议：“运行 `/architecture-review` 来重新验证覆盖范围，因为此 ADR
   有其状态和依赖项字段。”

如果未处于改装模式，请继续执行下面的步骤 1（正常 ADR 创作）。

**无参数守卫**：如果没有提供参数（标题为空），请先询问
运行阶段0：

> “您正在记录什么技术决策？请提供一个简短的标题
> （例如，`event-system-architecture`、`physics-engine-choice`）。”

使用用户的响应作为标题，然后继续执行步骤 1。

---

## 1. 加载引擎上下文（始终第一）

在做其他事情之前，先建立引擎环境：

1. Read `docs/engine-reference/[engine]/VERSION.md` 得到：
   - 引擎名称和版本
   - LLM知识截止日期
   - 截止后版本风险级别（低/中/高）

2. 从标题或中识别该架构决策的**领域**
   用户描述。常见领域：物理、渲染、UI、音频、导航、
   动画、网络、核心、输入、脚本。

3. Read 相应的模块引用（如果存在）：
   `docs/engine-reference/[engine]/modules/[domain].md`

4. Read `docs/engine-reference/[engine]/breaking-changes.md` — 标记任意
   法学硕士培训截止日期后相关领域的变化。

5. Read `docs/engine-reference/[engine]/deprecated-apis.md` — 标记任何 API
   在不应使用的相关域中。

6. **如果域包含，则在继续之前显示知识差距警告**
   中度或高风险：

   ```
   ⚠️  ENGINE KNOWLEDGE GAP WARNING
   Engine: [name + version]
   Domain: [domain]
   Risk Level: HIGH — This version is post-LLM-cutoff.

   Key changes verified from engine-reference docs:
   - [Change 1 relevant to this domain]
   - [Change 2]

   This ADR will be cross-referenced against the engine reference library.
   Proceed with verified information only — do NOT rely solely on training data.
   ```

   如果尚未配置引擎，则提示：“未配置引擎。
   首先运行 `/setup-engine`，或者告诉我您正在使用哪个引擎。”

---

## 2.确定下一个ADR号

扫描 `docs/architecture/` 查找现有 ADR 以查找下一个编号。

ADR 文件命名必须使用 `docs/architecture/adr-[NNNN]-[中文标题].md`：
- `[NNNN]` 为四位递增编号。
- `[中文标题]` 从 ADR 标题生成，使用中文语义标题。
- 不要为新 ADR 使用英文 slug，除非用户明确要求。
- 历史英文文件名可以保留；重命名已有 ADR 必须先获得用户明确批准。

---

## 3. 收集背景信息

Read 相关代码、现有 ADR 以及 `design/gdd/` 中的相关 GDD。

### 3a：架构注册表检查（阻塞门）

Read `docs/registry/architecture.yaml`。提取与此 ADR 相关的条目
域和决策（按系统名称、域关键字或所触及的状态进行 grep）。

**在协作设计之前**向用户展示任何相关立场
开始，作为锁定约束：

```
## Existing Architectural Stances (must not contradict)

State Ownership:
  player_health → owned by health-system (ADR-0001)
  Interface: HealthComponent.current_health (read-only float)
  → If this ADR reads or writes player health, it must use this interface.

Interface Contracts:
  damage_delivery → signal pattern (ADR-0003)
  Signal: damage_dealt(amount, target, is_crit)
  → If this ADR delivers or receives damage events, it must use this signal.

Forbidden Patterns:
  ✗ autoload_singleton_coupling (ADR-0001)
  ✗ direct_cross_system_state_write (ADR-0000)
  → The proposed approach must not use these patterns.
```

如果用户提出的决定与任何已登记的立场相矛盾，则表面
立即发生冲突：

> “⚠️冲突：这个ADR提出了[X]，但是ADR-[NNNN]确定了[Y]是
> 为此目的所接受的模式。不解决此遗嘱就继续进行
> 产生矛盾的 ADR 和不一致的故事。
> 选项：(1) 与现有立场一致，(2) 用以下内容取代 ADR-[NNNN]
> 显式替换，(3) 解释为什么本例是例外。”

在解决任何冲突之前，不要继续执行步骤 4（协作设计）
或明确接受为有意的例外。

---

## 4. 协同指导决策

在提出任何问题之前，先从上下文中得出该技能的最佳猜测
收集（读取 GDD、加载引擎参考、扫描现有 ADR）。然后呈现
使用 `AskUserQuestion` 的 **confirm/adjust** 提示 — 不是开放式问题。

**首先推导假设：**
- **问题**：从标题 + GDD 上下文推断需要做出什么决定
- **替代方案**：根据引擎参考+ GDD 要求提出 2-3 个具体选项
- **依赖关系**：扫描现有 ADR 以查找上游依赖关系；如果不清楚则假设无
- **GDD 链接**：提取与标题直接相关的 GDD 系统
- **状态**：新 ADR 始终为 `Proposed` — 切勿询问用户状态是什么

**假设范围选项卡**：假设仅涵盖：问题框架、替代方法、上游依赖性、GDD 链接和状态。模式设计问题（例如，“生成计时应该如何工作？”、“数据应该是内联的还是外部的？”）不是假设 - 它们是属于确认假设后的单独步骤的设计决策。不要在假设 AskUserQuestion 小部件中包含架构设计问题。

**确认假设后**，如果 ADR 涉及架构或数据设计选择，请在起草之前使用单独的多选项卡 `AskUserQuestion` 独立询问每个设计问题。

**用 `AskUserQuestion` 提出假设：**

```
Here's what I'm assuming before drafting:

Problem: [one-sentence problem statement derived from context]
Alternatives I'll consider:
  A) [option derived from engine reference]
  B) [option derived from GDD requirements]
  C) [option from common patterns]
GDD systems driving this: [list derived from context]
Dependencies: [upstream ADRs if any, otherwise "None"]
Status: Proposed

[A] Proceed — draft with these assumptions
[B] Change the alternatives list
[C] Adjust the GDD linkage
[D] Add a performance budget constraint
[E] Something else needs changing first
```

在用户确认假设或提供更正之前，不要生成 ADR。

**发动机专家和 TD 审查返回后**（步骤 5.5/5.6），如果未解决
决定仍然存在，将每一项作为单独的 `AskUserQuestion` 以及建议的
选项作为选择加上自由文本转义：

```
Decision: [specific unresolved point]
[A] [option from specialist review]
[B] [alternative option]
[C] Different approach — I'll describe it
```

**ADR 依赖项** — 从现有 ADR 派生，然后确认：
- 此决定是否取决于任何其他尚未接受的 ADR？
- 它是否解锁或解锁任何其他 ADR 或史诗？
- 它会阻止任何特定史诗的开始吗？

将答案记录在 **ADR 依赖项** 部分。 Write 如果没有适用的约束，则每个字段为“无”。

---

## 5.生成ADR

遵循这种格式：

```markdown
# ADR-[NNNN]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Date
[Date of decision]

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | [e.g. Godot 4.6] |
| **Domain** | [Physics / Rendering / UI / Audio / Navigation / Animation / Networking / Core / Input] |
| **Knowledge Risk** | [LOW / MEDIUM / HIGH — from VERSION.md] |
| **References Consulted** | [List engine-reference docs read, e.g. `docs/engine-reference/godot/modules/physics.md`] |
| **Post-Cutoff APIs Used** | [Any APIs from post-LLM-cutoff versions this decision depends on, or "None"] |
| **Verification Required** | [Specific behaviours to test before shipping, or "None"] |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | [ADR-NNNN (must be Accepted before this can be implemented), or "None"] |
| **Enables** | [ADR-NNNN (this ADR unlocks that decision), or "None"] |
| **Blocks** | [Epic/Story name — cannot start until this ADR is Accepted, or "None"] |
| **Ordering Note** | [Any sequencing constraint that isn't captured above] |

## Context

### Problem Statement
[What problem are we solving? Why does this decision need to be made now?]

### Constraints
- [Technical constraints]
- [Timeline constraints]
- [Resource constraints]
- [Compatibility requirements]

### Requirements
- [Must support X]
- [Must perform within Y budget]
- [Must integrate with Z]

## Decision

[The specific technical decision made, described in enough detail for someone
to implement it.]

### Architecture Diagram
[ASCII diagram or description of the system architecture this creates]

### Key Interfaces
[API contracts or interface definitions this decision creates]

## Alternatives Considered

### Alternative 1: [Name]
- **Description**: [How this would work]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Rejection Reason**: [Why this was not chosen]

### Alternative 2: [Name]
- **Description**: [How this would work]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Rejection Reason**: [Why this was not chosen]

## Consequences

### Positive
- [Good outcomes of this decision]

### Negative
- [Trade-offs and costs accepted]

### Risks
- [Things that could go wrong]
- [Mitigation for each risk]

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| [system-name].md | [specific rule, formula, or performance constraint from that GDD] | [how this decision satisfies it] |

## Performance Implications
- **CPU**: [Expected impact]
- **Memory**: [Expected impact]
- **Load Time**: [Expected impact]
- **Network**: [Expected impact, if applicable]

## Migration Plan
[If this changes existing code, how do we get from here to there?]

## Validation Criteria
[How will we know this decision was correct? What metrics or tests?]

## Related Decisions
- [Links to related ADRs]
- [Links to related design documents]
```

5.5. **引擎专家验证** - 在保存之前，通过 Task 生成**主要引擎专家**以验证起草的 ADR：
   - Read `.codex/docs/technical-preferences.md` `Engine Specialists` 部分获得初级专家
   - 如果没有配置引擎（`[TO BE CONFIGURED]`），则跳过此步骤
   - 生成 `subagent_type: [primary specialist]`，其中包含：ADR 的引擎兼容性部分、决策部分、关键接口和引擎参考文档路径。要求他们：
     1. 确认所提出的方法对于固定引擎版本是惯用的
     2. 标记训练截止后已弃用或更改的任何 API 或模式
     3. 识别当前 ADR 草案中未涵盖的特定于引擎的风险或陷阱
   - 如果专家发现**阻塞问题**（错误的 API、已弃用的方法、引擎版本不兼容）：相应地修改决策和引擎兼容性部分，然后在继续之前与用户确认更改
   - 如果专家仅发现**小注释**：将它们合并到 ADR 的风险小节中

**查看模式检查** — 在生成 TD-ADR 之前应用：
- `solo` → 跳过。注意：“TD-ADR 已跳过 — 单人模式。”继续执行步骤 5.7（GDD 同步检查）。
- `lean` → 跳过（不是相位门）。注意：“TD-ADR 已跳过 — 精益模式。”继续执行步骤 5.7（GDD 同步检查）。
- `full` → 正常生成。

5.6. **技术总监战略审查** — 经过引擎专家验证后，使用门 **TD-ADR** (`.codex/docs/director-gates.md`) 通过 Task 生成 `technical-director`：
   - 传递：ADR 文件路径（或草稿内容）、引擎版本、域、同一域中的任何现有 ADR
   - TD 验证架构一致性（此决定与整个系统一致吗？）——与引擎专家的 API 级别检查不同
   - 如果担心或拒绝：在继续之前相应地修改“决定”或“替代方案”部分

5.7. **GDD 同步检查** — 在提交写入批准之前，扫描所有 GDD
有关命名不一致的问题，请参阅“GDD 已解决的要求”部分
与 ADR 的关键接口和决策部分（重命名信号、API 方法、
或数据类型）。如果发现任何内容，请将其作为**显着的警告块**显示出来
紧接在写入批准之前 - 不作为脚注：

```
⚠️ GDD SYNC REQUIRED
[gdd-filename].md uses names this ADR has renamed:
  [old_name] → [new_name_from_adr]
  [old_name_2] → [new_name_2_from_adr]
The GDD must be updated before or alongside writing this ADR to prevent
developers reading the GDD from implementing the wrong interface.
```

如果没有不一致：默默地跳过此块。

5. **Write 批准** — 使用 `AskUserQuestion`：

如果发现 GDD 同步问题：
- “ADR 草案已完成。您想如何继续？”
  - [A] Write ADR + 在同一遍中更新 GDD
  - 仅 [B] Write ADR — 我将手动更新 GDD
  - [C] 还没有 — 我需要进一步审查

如果没有 GDD 同步问题：
- “ADR草稿已完成，我可以写一下吗？”
  - [A] Write ADR 至 `docs/architecture/adr-[NNNN]-[中文标题].md`
  - [B] 还没有 — 我需要进一步审查

如果任何写入选项为“是”，则写入文件，并根据需要创建目录。
对于带有 GDD 更新的选项 [A]：同时更新 GDD 文件以使用新名称。

6. **更新架构注册表**

扫描书面 ADR 以获取应注册的新架构立场：
- 声明其声称拥有
- 它定义的接口契约（信号签名、方法 API）
- 它声称的绩效预算
- API 它明确做出的选择
- 它禁止的模式（后果 → 否定或明确的“不要使用 X”）

目前候选人：
```
Registry candidates from this ADR:
  NEW state ownership:      player_stamina → stamina-system
  NEW interface contract:   stamina_depleted signal
  NEW performance budget:   stamina-system: 0.5ms/frame
  NEW forbidden pattern:    polling stamina each frame (use signal instead)
  EXISTING (referenced_by update only): player_health → already registered ✅
```

**注册表附加逻辑**：写入 `docs/registry/architecture.yaml` 时，不要假设部分为空。该文件可能已经包含在此会话中写入的先前 ADR 的条目。在每次 Edit 调用之前：
1. Read `docs/registry/architecture.yaml` 的当前状态
2. 找到正确的部分（state_ownership、interfaces、forbidden_patterns、api_decisions）
3. 将新条目追加到该部分中最后一个现有条目之后 - 不要尝试替换可能不再存在的 `[]` 占位符
4. 如果该部分已有条目，则使用最后一个条目的结束内容作为 `old_string` 锚点，并在其后附加新条目

**阻止 — 未经用户明确批准，请勿写入 `docs/registry/architecture.yaml`。**

使用 `AskUserQuestion` 询问：
- “我可以用这些 [N] 新立场来更新 `docs/registry/architecture.yaml` 吗？”
  - 选项：“是 - 更新注册表”、“还没有 - 我想查看候选人”、“跳过注册表更新”

仅当用户选择“是”时才继续。如果是：追加新条目。切勿修改现有条目——如果立场是
更改后，将旧条目设置为 `status: superseded_by: ADR-[NNNN]` 并添加新条目。

---

## 6. 结束后续步骤

写入 ADR 后（并且可以选择更新注册表），以 `AskUserQuestion` 关闭。

在生成小部件之前：
1. Read `docs/registry/architecture.yaml` — 检查是否有任何优先级 ADR 仍未写入（查找 technical-preferences.md 或 systems-index.md 中标记的 ADR 作为先决条件）
2. 检查所有必备 ADR 是否现已写入。如果是，请添加“开始编写 GDD”选项。
3. 将所有剩余的优先 ADR 作为单独的选项列出，而不仅仅是接下来的一两个。

小部件格式：
```
ADR-[NNNN] written and registry updated. What would you like to do next?
[1] Write [next-priority-adr-name] — [brief description from prerequisites list]
[2] Write [another-priority-adr] — [brief description]  (include ALL remaining ones)
[N] Start writing GDDs — run `/design-system [first-undesigned-system]` (only show if all prerequisite ADRs are written)
[N+1] Stop here for this session
```

如果没有剩余的优先级 ADR 且没有未设计的 GDD 系统，则仅提供“在此停止”并建议在新会话中运行 `/architecture-review`。

**始终在结束输出中包含此固定通知（请勿省略）：**

> 要根据您的 GDD 验证 ADR 覆盖范围，请打开 **新的 Codex 会话**
> 并运行 `/architecture-review`。
>
> **切勿在与 `/architecture-decision` 相同的会话中运行 `/architecture-review`。**
> 审查机构必须独立于创作背景，以给出公正的意见
> 评估。在这里运行它会使审核无效。

将 `Status: Blocked` 等待此 ADR 的所有故事更新为 `Status: Ready`。
