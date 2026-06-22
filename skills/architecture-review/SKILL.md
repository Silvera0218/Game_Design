---
name: architecture-review
description: "根据所有 GDD 验证项目架构的完整性和一致性。构建将每个 GDD 技术要求映射到 ADR 的可追溯性矩阵，识别覆盖范围差距，检测跨 ADR 冲突，验证所有决策的引擎兼容性一致性，并生成 PASS/CONCERNS/FAIL 判决。相当于 /design-review. 的架构"
---

# 架构回顾

架构审查验证了架构决策的完整主体
涵盖所有游戏设计要求，内部一致且目标正确
该项目的固定引擎版本。它是技术设置之间的质量门
和预制作。

**论证模式：**
- **无争议/`full`**：全面审查 - 所有阶段
- **`coverage`**：仅可追溯性 — GDD 要求没有 ADR
- **`consistency`**：仅跨 ADR 冲突检测
- **`engine`**：仅引擎兼容性审核
- **`single-gdd [path]`**：查看一个特定 GDD 的架构覆盖范围
- **`rtm`**：需求可追溯性矩阵 - 扩展了标准矩阵
  包括故事文件路径和测试文件路径；输出
  `docs/architecture/requirements-traceability.md` 具有完整的
  GDD 要求 → ADR → 故事 → 测试链。在生产阶段使用时
  故事和测试是存在的。

---

## 第一阶段：加载所有内容

### 阶段 1a — L0：摘要扫描（快速、低令牌）

在阅读任何完整文档之前，请使用 Grep 提取 `## Summary` 部分
来自所有 GDD 和 ADR：

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 4
Grep pattern="## Summary" glob="docs/architecture/adr-*.md" output_mode="content" -A 3
```

对于 `single-gdd [path]` 模式：使用目标 GDD 的摘要来识别哪个
ADR 引用同一系统（Grep ADR 为系统名称），然后全读
只有那些 ADR。完全跳过不相关的 GDD 的全文阅读。

对于 `engine` 模式：仅完整读取 ADR — 引擎检查不需要 GDD。

对于 `coverage` 或 `full` 模式：继续完整阅读以下所有内容。

### 阶段 1b — L1/L2：完整文档加载

Read 所有适合该模式的输入：

### 设计文件
- `design/gdd/` 中的所有范围内 GDD — 完全读取每个文件
- `design/gdd/systems-index.md` — 权威系统列表

### 架构文档
- `docs/architecture/` 中的所有范围内 ADR — 完全读取每个文件
- `docs/architecture/architecture.md`（如果存在）

### 发动机参考
- `docs/engine-reference/[engine]/VERSION.md`
- `docs/engine-reference/[engine]/breaking-changes.md`
- `docs/engine-reference/[engine]/deprecated-apis.md`
- `docs/engine-reference/[engine]/modules/` 中的所有文件

### 项目标准
- `.codex/docs/technical-preferences.md`

报告计数：“已加载 [N] GDD、[M] ADR，引擎：[名称 + 版本]。”

**另请阅读 `docs/consistency-failures.md`**（如果存在）。提取条目
与正在审查的系统匹配的域（架构、引擎或任何 GDD 域）
被覆盖）。表面重复出现的模式作为“已知易发生冲突的区域”注释
在第 4 阶段冲突检测输出的顶部。

---

## 第 2 阶段：从每个 GDD 中提取技术要求

### 预加载 TR 注册表

在提取任何要求之前，请阅读 `docs/architecture/tr-registry.yaml`
如果存在的话。按 `id` 和标准化 `requirement` 对现有条目进行索引
文本（小写，已修剪）。这可以防止在审核过程中对 ID 进行重新编号。

对于您提取的每个需求，匹配规则为：
1. **Exact/near 与同一系统的现有注册表项匹配** →
   重用该条目的 TR-ID 不变。更新 `requirement` 文本
   仅当 GDD 措辞发生变化时才进行注册表（相同的意图，更清晰的措辞） -
   添加 `revised: [date]` 字段。
2. **不匹配** → 分配一个新 ID：下一个可用的 `TR-[system]-NNN`
   系统，从现有的最高序列+1开始。
3. **不明确**（部分匹配，意图不清楚）→询问用户：
   > “‘[new requirement text]’是否指与
   > `TR-[system]-NNN: [existing text]'`，还是一个新要求？”
   用户回答：“相同要求”（重用 ID）或“新要求”（新 ID）。

对于注册表中 `status: deprecated` 的任何要求 - 跳过它。
它被有意从 GDD 中删除。

对于每个 GDD，阅读它并提取所有 **技术要求** —
架构必须保证系统能够正常工作。技术要求是任何
暗示特定架构决策的声明。

要提取的类别：

| Category | Example |
|----------|---------|
| **数据结构** | “每个实体都有健康状况、最大健康状况、状态影响” → 需要 component/data 模式 |
| **性能限制** | “碰撞检测必须以 60fps 的速度运行 200 个实体”→ 物理预算 ADR |
| **发动机能力** | “角色动画的逆运动学” → IK 系统 ADR |
| **跨系统通信** | “损坏系统同时通知UI和音频” → event/signal架构 ADR |
| **状态持久性** | “玩家进度在会话之间保持不变” → 保存系统 ADR |
| **Threading/timing** | “AI 决策发生在主线程之外”→ 并发 ADR |
| **平台要求** | “支持键盘、游戏手柄、触摸” → 输入系统 ADR |

对于每个 GDD，生成一个结构化列表：

```
GDD: [filename]
System: [system name]
Technical Requirements:
  TR-[GDD]-001: [requirement text] → Domain: [Physics/Rendering/etc]
  TR-[GDD]-002: [requirement text] → Domain: [...]
```

这成为**需求基线**——完整的集合
架构必须覆盖。

---

## 第 3 阶段：构建可追溯性矩阵

对于第 2 阶段提取的每项技术要求，搜索 ADR：

1. Read 每个 ADR 的“GDD 满足的要求”部分
2. 检查它是否明确引用了该要求或其 GDD
3. 检查 ADR 的决策文本是否隐式涵盖了要求
4. 标记覆盖状态：

| Status | Meaning |
|--------|---------|
| ✅ **覆盖** | ADR 明确满足了此要求 |
| ⚠️ **部分** | ADR 部分涵盖了这一点，或者覆盖范围不明确 |
| ❌ **差距** | 没有 ADR 满足此要求 |

构建完整矩阵：

```
## Traceability Matrix

| Requirement ID | GDD | System | Requirement | ADR Coverage | Status |
|---------------|-----|--------|-------------|--------------|--------|
| TR-combat-001 | combat.md | Combat | Hitbox detection < 1 frame | ADR-0003 | ✅ |
| TR-combat-002 | combat.md | Combat | Combo window timing | — | ❌ GAP |
| TR-inventory-001 | inventory.md | Inventory | Persistent item storage | ADR-0005 | ✅ |
```

计算总数：X 已覆盖、Y 部分、Z 间隙。

---

## 阶段 3b：故事和测试链接（仅限 RTM 模式）

*除非参数是 `rtm` 或 `full` 并且存在故事，否则请跳过此阶段。*

此阶段扩展了第 3 阶段矩阵以包括实现的故事
每个要求和验证它的测试 - 生成完整的
需求可追溯性矩阵 (RTM)。

### 步骤 3b-1 — 加载故事

Glob `production/epics/**/*.md`（不包括 EPIC.md 索引文件）。对于每个
故事文件：
- 从故事的上下文部分提取 `TR-ID`
- 提取故事文件路径、标题、状态
- 提取 `## Test Evidence` 部分 — 指定的测试文件路径

### 步骤 3b-2 — 加载测试文件

Glob `tests/unit/**/*_test.*` 和 `tests/integration/**/*_test.*`。
建立索引：系统→[test file paths]。

对于步骤 3b-1 中的每个测试文件路径，通过 Glob 确认该文件是否
确实存在。如果指定的路径不存在，请注意“MISSING”。

### 步骤 3b-3 — 构建扩展 RTM

对于第 3 阶段矩阵中的每个 TR-ID，添加：
- **故事**：引用此 TR-ID 的故事文件路径（可以是多个）
- **测试文件**：故事的测试证据部分中所述的测试文件路径
- **测试状态**：COVERED（测试文件存在）/MISSING（指定路径但未指定）
  已找到）/ NONE（未说明测试路径，故事类型可能是 Visual/Feel/UI）/
  没有故事（需求还没有故事——预生产差距）

扩展矩阵格式：

```
## Requirements Traceability Matrix (RTM)

| TR-ID | GDD | Requirement | ADR | Story | Test File | Test Status |
|-------|-----|-------------|-----|-------|-----------|-------------|
| TR-combat-001 | combat.md | Hitbox < 1 frame | ADR-0003 | story-001-hitbox.md | tests/unit/combat/hitbox_test.gd | COVERED |
| TR-combat-002 | combat.md | Combo window | — | story-002-combo.md | — | NONE (Visual/Feel) |
| TR-inventory-001 | inventory.md | Persistent storage | ADR-0005 | — | — | NO STORY |
```

RTM 覆盖范围摘要：
- 涵盖：[N] — ADR 的要求 + 故事 + 通过测试
- 缺少测试：[N] — 故事存在，但未找到测试文件
- 无故事：[N] — ADR 的要求，但还没有故事
- NO ADR：[N] — 无架构覆盖的要求（来自第 3 阶段的差距）
- 完整链条（已覆盖）：[N/total] ([%])

---

## 第4阶段：跨ADR冲突检测

将每个 ADR 与其他每个 ADR 进行比较以检测矛盾。冲突
存在于：

- **数据所有权冲突**：两个 ADR 声称对同一数据拥有独占所有权
- **集成合同冲突**：ADR-A 假设系统 X 具有接口 Y，但是
  ADR-B 用不同的接口定义系统 X
- **性能预算冲突**：ADR-A 向物理分配 N ms，ADR-B 分配
  对 AI 来说有 N 毫秒，它们合计超过了总帧预算
- **依赖循环**：ADR-A 表示系统 X 在 Y 之前初始化； ADR-B 表示 Y
  在 X 之前初始化
- **架构模式冲突**：ADR-A 使用事件驱动通信来实现
  子系统； ADR-B 使用对同一子系统的直接函数调用
- **状态管理冲突**：两个 ADR 定义了对同一游戏状态的权限
  （例如，战斗 ADR 和角色 ADR 都声称拥有生命值）

对于发现的每个冲突：

```
## Conflict: [ADR-NNNN] vs [ADR-MMMM]
Type: [Data ownership / Integration / Performance / Dependency / Pattern / State]
ADR-NNNN claims: [...]
ADR-MMMM claims: [...]
Impact: [What breaks if both are implemented as written]
Resolution options:
  1. [Option A]
  2. [Option B]
```

### ADR 依赖性排序

冲突检测后，分析所有 ADR 的依赖关系图：

1. **从每个 ADR 的“ADR 依赖项”部分收集所有 `Depends On` 字段**
2. **拓扑排序**：确定正确的执行顺序——没有的ADR
   依赖项先出现（基础），依赖于这些项的 ADR 接下来出现，等等。
3. **标记未解决的依赖关系**：如果 ADR-A 的“取决于”字段引用 ADR
   仍然是 `Proposed` 或不存在，标记它：
   ```
   ⚠️  ADR-0005 depends on ADR-0002 — but ADR-0002 is still Proposed.
       ADR-0005 cannot be safely implemented until ADR-0002 is Accepted.
   ```
4. **循环检测**：如果ADR-A依赖于ADR-B且ADR-B依赖于ADR-A（直接
   或传递地），将其标记为 `DEPENDENCY CYCLE`：
   ```
   🔴 DEPENDENCY CYCLE: ADR-0003 → ADR-0006 → ADR-0003
      This cycle must be broken before either can be implemented.
   ```
5. **输出建议的实施顺序**：
   ```
   ### Recommended ADR Implementation Order (topologically sorted)
   Foundation (no dependencies):
     1. ADR-0001: [title]
     2. ADR-0003: [title]
   Depends on Foundation:
     3. ADR-0002: [title] (requires ADR-0001)
     4. ADR-0005: [title] (requires ADR-0003)
   Feature layer:
     5. ADR-0004: [title] (requires ADR-0002, ADR-0005)
   ```

---

## 第 5 阶段：发动机兼容性交叉检查

在所有 ADR 中，检查引擎的一致性：

### 版本一致性
- 所有提到引擎版本的 ADR 是否都同意同一版本？
- 如果任何 ADR 是为较旧的引擎版本编写的，请将其标记为可能过时

### 截止后 API 一致性
- 从所有 ADR 中收集所有“截止后使用的 API”字段
- 对于每个模块，根据相关模块参考文档进行验证
- 检查是否有两个 ADR 对相同的截止后 API 做出矛盾的假设

### 已弃用 API 检查
- Grep `deprecated-apis.md` 中列出的 API 名称的所有 ADR
- 标记任何引用已弃用的 API 的 ADR

### 缺少引擎兼容性部分
- 列出完全缺少引擎兼容性部分的所有 ADR
- 这些都是盲点——他们的引擎假设是未知的

输出格式：
```
### Engine Audit Results
Engine: [name + version]
ADRs with Engine Compatibility section: X / Y total

Deprecated API References:
  - ADR-0002: uses [deprecated API] — deprecated since [version]

Stale Version References:
  - ADR-0001: written for [older version] — current project version is [version]

Post-Cutoff API Conflicts:
  - ADR-0004 and ADR-0007 both use [API] with incompatible assumptions
```

---

### 发动机专家咨询

完成上述引擎审核后，通过 Task 生成**主要引擎专家**以获得领域专家的第二意见：
- Read `.codex/docs/technical-preferences.md` `Engine Specialists` 部分获得初级专家
- 如果未配置引擎，请跳过此咨询
- 生成 `subagent_type: [primary specialist]`：包含特定于引擎的决策或 `Post-Cutoff APIs Used` 字段的所有 ADR、引擎参考文档和第 5 阶段审核结果。要求他们：
  1. 确认或质疑每项审计结果 - 专家可能知道参考文档中未捕获的发动机细微差别
  2. 识别 ADR 中审计可能遗漏的特定于引擎的反模式（例如，使用错误的 Godot 节点类型、Unity 组件耦合、Unreal 子系统滥用）
  3. 标记对引擎行为做出与实际固定版本不同的假设的 ADR

将 `### Engine Specialist Findings` 下的其他发现纳入第 5 阶段输出中。这些都会影响最终的裁决——专家确定的问题与审计确定的问题具有相同的权重。

---

## 阶段 5b：设计修订标志（架构 → GDD 反馈）

对于第 5 阶段发现的每个 **高风险引擎**，检查是否有任何 GDD 做出了
假设已验证的发动机实际情况与此相矛盾。

具体情况要检查：

1. **截止后 API 行为与训练数据假设不同**：如果 ADR
   记录与默认 LLM 假设不同的经过验证的 API 行为，
   检查引用相关系统的所有 GDD。寻找书面的设计规则
   围绕旧的（假设的）行为。

2. **ADR 中的已知引擎限制**：如果 ADR 记录了已知的引擎限制
   （例如“Jolt 忽略 HingeJoint3D 阻尼”、“D3D12 现在是默认后端”），检查
   GDD 围绕受影响的功能设计机制。

3. **已弃用的 API 冲突**：如果第 5 阶段标记了 ADR 中使用的已弃用的 API，
   检查是否有任何 GDD 包含假定已弃用的 API 行为的机制。

对于发现的每个冲突，将其记录在 GDD 修订标志表中：

```
### GDD Revision Flags (Architecture → Design Feedback)
These GDD assumptions conflict with verified engine behaviour or accepted ADRs.
The GDD should be revised before its system enters implementation.

| GDD | Assumption | Reality (from ADR/engine-reference) | Action |
|-----|-----------|--------------------------------------|--------|
| combat.md | "Use HingeJoint3D damp for weapon recoil" | Jolt ignores damp — ADR-0003 | Revise GDD |
```

如果未找到修订标志，请写入：“无 GDD 修订标志 — 所有 GDD 假设
与经过验证的发动机行为一致。”

问：“我是否应该在系统索引中标记这些 GDD 以供修订？”
- 如果是：将相关系统的状态字段更新为“需要修订”
  并在相邻的 Notes/Description 列中添加一个简短的内联注释来解释冲突。
  写作前请求批准。
  （不要使用诸如“需要修订（架构反馈）”之类的括号——其他技能
  匹配确切的字符串“Needs Revision”，括号会破坏该匹配。）

---

## 第 6 阶段：架构文档覆盖范围

如果 `docs/architecture/architecture.md` 存在，则根据 GDD 对其进行验证：

- `systems-index.md` 中的每个系统都出现在架构层中吗？
- 数据流部分是否涵盖了GDD中定义的所有跨系统通信？
- API 边界是否支持 GDD 的所有集成要求？
- 架构文档中是否有系统没有对应的GDD
  （孤儿建筑）？

---

## 第七阶段：输出评审报告

```
## Architecture Review Report
Date: [date]
Engine: [name + version]
GDDs Reviewed: [N]
ADRs Reviewed: [M]

---

### Traceability Summary
Total requirements: [N]
✅ Covered: [X]
⚠️ Partial: [Y]
❌ Gaps: [Z]

### Coverage Gaps (no ADR exists)
For each gap:
  ❌ TR-[id]: [GDD] → [system] → [requirement]
     Suggested ADR: "/architecture-decision [suggested title]"
     Domain: [Physics/Rendering/etc]
     Engine Risk: [LOW/MEDIUM/HIGH]

### Cross-ADR Conflicts
[List all conflicts from Phase 4]

### ADR Dependency Order
[Topologically sorted implementation order from Phase 4 — dependency ordering section]
[Unresolved dependencies and cycles if any]

### GDD Revision Flags
[GDD assumptions that conflict with verified engine behaviour — from Phase 5b]
[Or: "None — all GDD assumptions consistent with verified engine behaviour"]

### Engine Compatibility Issues
[List all engine issues from Phase 5]

### Architecture Document Coverage
[List missing systems and orphaned architecture from Phase 6]

---

### Verdict: [PASS / CONCERNS / FAIL]

PASS: All requirements covered, no conflicts, engine consistent
CONCERNS: Some gaps or partial coverage, but no blocking conflicts
FAIL: Critical gaps (Foundation/Core layer requirements uncovered),
      or blocking cross-ADR conflicts detected

### Blocking Issues (must resolve before PASS)
[List items that must be resolved — FAIL verdict only]

### Required ADRs
[Prioritised list of ADRs to create, most foundational first]
```

---

## 第 8 阶段：Write 和更新追溯索引

使用 `AskUserQuestion` 进行写入批准：
- “复习完毕，你想写什么？”
  - [A] Write 所有三个文件（审核报告+溯源索引+TR注册表）
  - [B] Write 仅审查报告 — `docs/architecture/architecture-review-[date].md`
  - [C] 不要写任何东西 - 我需要先检查一下结果

### RTM 输出（仅限 RTM 模式）

对于 `rtm` 模式，另外询问：“我可以写完整的需求可追溯性吗？
矩阵到 `docs/architecture/requirements-traceability.md`？”

RTM 文件格式：

```markdown
# Requirements Traceability Matrix (RTM)

> Last Updated: [date]
> Mode: /architecture-review rtm
> Coverage: [N]% full chain complete (GDD → ADR → Story → Test)

## How to read this matrix

| Column | Meaning |
|--------|---------|
| TR-ID | Stable requirement ID from tr-registry.yaml |
| GDD | Source design document |
| ADR | Architectural decision governing implementation |
| Story | Story file that implements this requirement |
| Test File | Automated test file path |
| Test Status | COVERED / MISSING / NONE / NO STORY |

## Full Traceability Matrix

| TR-ID | GDD | Requirement | ADR | Story | Test File | Status |
|-------|-----|-------------|-----|-------|-----------|--------|
[Full matrix rows from Phase 3b]

## Coverage Summary

| Status | Count | % |
|--------|-------|---|
| COVERED — full chain complete | [N] | [%] |
| MISSING test — story exists, no test | [N] | [%] |
| NO STORY — ADR exists, not yet implemented | [N] | [%] |
| NO ADR — architectural gap | [N] | [%] |
| **Total requirements** | **[N]** | **100%** |

## Uncovered Requirements (Priority Fix List)

Requirements where the full chain is broken, prioritised by layer:

### Foundation layer gaps
[list with suggested action per gap]

### Core layer gaps
[list]

### Feature / Presentation layer gaps
[list — lower priority]

## History

| Date | Full Chain % | Notes |
|------|-------------|-------|
| [date] | [%] | Initial RTM |
```

### TR 注册表更新

另请询问：“我可以根据新要求更新 `docs/architecture/tr-registry.yaml`
这篇评论的 ID？”

If yes:
- **附加**在此审核之前注册表中未包含的任何新 TR-ID
- **更新** `requirement` 文本和 `revised` 其 GDD 的任何条目的日期
  措辞已更改（ID 保持不变）
- 对于满足 GDD 要求的任何注册表项，**标记** `status: deprecated`
  不再存在（在标记为已弃用之前与用户确认）
- **绝不**重新编号或删除现有条目
- 更新顶部的 `last_updated` 和 `version` 字段

这确保了所有未来的故事文件都可以引用持续存在的稳定 TR-ID
贯穿后续的每一次架构审查。

### 反射日志更新

撰写审核报告后，附加在第 4 阶段发现的任何🔴冲突条目
至 `docs/consistency-failures.md`（如果文件存在）：

```markdown
### [YYYY-MM-DD] — /architecture-review — 🔴 CONFLICT
**Domain**: Architecture / [specific domain e.g. State Ownership, Performance]
**Documents involved**: [ADR-NNNN] vs [ADR-MMMM]
**What happened**: [specific conflict — what each ADR claims]
**Resolution**: [how it was or should be resolved]
**Pattern**: [generalised lesson for future ADR authors in this domain]
```

仅附加冲突条目 - 不记录 GAP 条目（预计会丢失 ADR）
在架构完成之前）。仅当文件丢失时才创建
当它已经存在时追加。

### 会话状态更新

写入所有批准的文件后，默默附加到
`production/session-state/active.md`:

    ## 会话摘录 — /architecture-review [date]
    - 判决：[PASS / CONCERNS / FAIL]
    - 要求：[N] 总计 — [X] 已覆盖、[Y] 部分、[Z] 间隙
    - 注册的新 TR-ID：[N，或“无”]
    - GDD 修订标志：[逗号分隔的 GDD 名称，或“无”]
    - 主要 ADR 差距：[报告中的前 3 个差距标题，或“无”]
    - 报告：docs/architecture/architecture-review-[date].md

如果`active.md`不存在，则以此块为初始内容创建它。
在对话中确认：“会话状态已更新。”

追溯索引格式：

```markdown
# Architecture Traceability Index
Last Updated: [date]
Engine: [name + version]

## Coverage Summary
- Total requirements: [N]
- Covered: [X] ([%])
- Partial: [Y]
- Gaps: [Z]

## Full Matrix
[Complete traceability matrix from Phase 3]

## Known Gaps
[All ❌ items with suggested ADRs]

## Superseded Requirements
[Requirements whose GDD was changed after the ADR was written]
```

---

## 第 9 阶段：交接

完成审查并编写批准的文件后，提交：

1. **立即采取行动**：列出要创建的前 3 个 ADR（首先是影响最大的差距，
   基础层在特征层之前）
2. **门指导**：“当所有阻塞问题都解决后，运行`/gate-check
   预生产`推进”
3. **重新运行触发器**：“在写入每个新的 ADR 后重新运行 `/architecture-review`
   验证覆盖范围是否有所改善”

然后用 `AskUserQuestion` 关闭：
- “架构审查完成。接下来你想做什么？”
  - [A] Write 缺少 ADR — 打开一个新会话并运行 `/architecture-decision [system]`
  - [B] 运行 `/gate-check pre-production` — 如果所有阻塞间隙均已解决
  - [C] 本次会议在此停止

---

## 错误恢复协议

如果任何生成的代理返回 BLOCKED、错误或无法完成：

1. **立即浮出水面**：在继续之前报告“[AgentName]：被阻止 — [reason]”
2. **评估依赖关系**：如果后续阶段需要被阻止的代理的输出，则在没有用户输入的情况下不要继续经过该阶段
3. **通过 AskUserQuestion 提供选项**，共有三种选择：
   - 跳过此代理并注意最终报告中的差距
   - 以更窄的范围重试（更少的 GDD、单一系统焦点）
   - 停在这里并首先解决阻止程序
4. **始终生成部分报告** — 输出已完成的所有内容，这样工作就不会丢失

---

## 协作协议

1. **Read 默默** - 不要叙述每个读取的文件
2. **显示矩阵** — 在询问之前提供完整的可追溯性矩阵
   任何东西；让用户看到状态
3. **不要猜测** — 如果需求不明确，请询问：“[X] 是技术性的吗？
   要求还是设计偏好？”
4. **写入前询问** — 在写入报告文件之前务必确认
5. **非阻塞** — 判决是建议性的；用户决定是否继续
   尽管存在担忧甚至失败的结果
