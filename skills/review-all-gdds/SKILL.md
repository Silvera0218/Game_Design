---
name: review-all-gdds
description: "全面的跨 GDD 一致性和游戏设计审查。同时读取所有系统 GDD 并检查它们之间的矛盾、过时的引用、所有权冲突、公式不兼容和游戏设计理论违规（主导策略、经济失衡、认知超载、支柱漂移）。在写入所有 MVP GDD 之后、架构开始之前运行。"
---

# 查看所有 GDD

该技能同时读取每个系统 GDD 并执行两个互补的操作
无法根据 GDD 单独完成的审查：

1. **跨 GDD 一致性** — 矛盾、过时的引用和所有权
   文件之间的冲突
2. **游戏设计整体论**——只有当你看到所有系统时才会出现的问题
   共同：主导战略、破碎的经济、认知超载、支柱
   漂移、竞争进展循环

**这与 `/design-review` 不同**，后者审查了一个 GDD 的内部
完整性。该技能审查所有 GDD 之间的“关系”。

**何时运行：**
- 所有 MVP 级 GDD 均单独获得批准后
- 任何 GDD 在生产中期进行重大修改后
- 在 `/create-architecture` 开始之前（基于不一致的 GDD 构建的架构
  继承了这些不一致之处）

**论证模式：**

**焦点：** `$ARGUMENTS[0]`（空白 = `full`）

- **无参数/`full`**：一致性和设计理论均通过
- **`consistency`**：仅跨 GDD 一致性检查（更快）
- **`design-theory`**：仅游戏设计整体性检查
- **`since-last-review`**：自上次审核报告以来仅修改了 GDD（基于 git）

---

## 第一阶段：加载所有内容

### 阶段 1a — L0：摘要扫描（快速、低令牌）

在阅读任何完整文档之前，请使用 Grep 提取 `## Summary` 部分
来自所有 GDD 文件：

先选择 GDD 源目录：
- 如果 `design/gdd/*.md` 存在，使用 `design/gdd/` 作为标准 corpus。
- 否则，如果 `GDD/*.md` 存在，使用 `GDD/` 作为当前项目 corpus；将 `GDD/INDEX.md` 视为系统索引，将 `GDD/00_项目总览_GDD.md` 视为项目总览/概念文档。

然后用所选 corpus 运行摘要扫描：

```
Grep pattern="## Summary" glob="[selected-gdd-dir]/*.md" output_mode="content" -A 5
```

向用户显示清单：
```
Found [N] GDDs. Summaries:
  • combat.md — [summary text]
  • inventory.md — [summary text]
  ...
```

对于 `since-last-review` 模式：运行 `git log --name-only` 来识别 GDD
自上次审查报告文件编写以来已进行修改。向用户显示哪个
GDD 的范围基于在进行任何完整读取之前的摘要。仅
对于这些 GDD 以及其“关键部门”中列出的任何 GDD，请继续进入 L1。

### 第 1b 阶段 — 注册表预加载（快速基线）

在完整阅读任何 GDD 之前，请检查实体注册表：

```
Read path="design/registry/entities.yaml"
```

如果注册表存在并且有条目，则将其用作**预构建的冲突
基线**：已知实体、项目、公式和常量及其
权威值和来源 GDD。在第 2 阶段，grep GDD 查找已注册的
首先命名——这比在知道之前完整阅读所有 GDD 更快
寻找什么。

如果注册表为空或不存在：则无需注册表即可继续。报告中注明：
“实体注册表为空——一致性检查依赖于完整的 GDD 只读。
在此审核后运行 `/consistency-check` 以填充注册表。”

### 阶段 1c — L1/L2：完整文档加载

完整阅读范围内的文件：

1. `[selected-gdd-dir]/game-concept.md`；如果使用 `GDD/` corpus，则读取 `GDD/00_项目总览_GDD.md` — 游戏视觉、核心循环、MVP 定义
2. `[selected-gdd-dir]/game-pillars.md`（如果存在）——设计支柱和反支柱
3. `[selected-gdd-dir]/systems-index.md`；如果使用 `GDD/` corpus，则读取 `GDD/INDEX.md` — 权威系统列表、层、依赖项、状态
4. **所选 corpus 中的每个范围内系统 GDD** — 完整阅读（跳过概念文档和索引文档 — 这些内容已在上面阅读）

报告：“已加载 [N] 系统 GDD，覆盖 [M] 系统。支柱：[list]。反支柱：[list]。”

如果存在的系统 GDD 少于 2 个，则停止：
> “跨 GDD 审核需要至少 2 个系统 GDD。首先需要 Write 更多 GDD，
> 然后重新运行 `/review-all-gdds`。”

---

### 并行执行

第 2 阶段（一致性）和第 3 阶段（设计理论）是独立的——他们读
相同的 GDD 输入，但生成单独的报告。生成并行 Task
代理同时进行，而不是等待第 2 阶段完成
开始第 3 阶段。在编写合并报告之前收集两个结果。

---

## 第 2 阶段：跨 GDD 一致性

仔细研究每一对和每一组 GDD，找出矛盾和差距。

### 2a：双向依赖

对于每个 GDD 的依赖项部分，检查每个列出的依赖项是否
reciprocal:
- 如果 GDD-A 列出“依赖于 GDD-B”，请检查 GDD-B 是否将 GDD-A 列为依赖项
- 如果 GDD-A 列出“由 GDD-C 依赖”，请检查 GDD-C 是否将 GDD-A 列为依赖项
- 将任何单向依赖性标记为一致性问题

```
⚠️  Dependency Asymmetry
[system-a].md lists: Depends On → [system-b].md
[system-b].md does NOT list [system-a].md as a dependent
→ One of these documents has a stale dependency section
```

### 2b：规则矛盾

对于任何 GDD 中定义的每个游戏规则、机制或约束，检查是否
任何其他 GDD 为相同情况定义了矛盾的规则：

扫描类别：
- **Floor/ceiling 规则**：是否有任何 GDD 定义输出的最小值？还有其他人说不同的系统可以绕过该楼层吗？这些是矛盾的。
- **资源所有权**：如果两个 GDD 都定义共享资源如何累积或消耗，它们是否同意？
- **状态转换**：如果 GDD-A 描述了角色死亡时会发生什么，
  GDD-B 对同一事件的描述是否一致？
- **时序**：如果 GDD-A 说“X 发生在同一帧上”，GDD-B 是否假设
  它是异步发生的吗？
- **堆叠规则**：如果 GDD-A 表示状态效果堆叠，GDD-B 是否假设
  他们不？

```
🔴 Rule Contradiction
[system-a].md: "Minimum [output] after reduction is [floor_value]"
[system-b].md: "[mechanic] bypasses [system-a]'s rules and can reduce [output] to 0"
→ These rules directly contradict. Which GDD is authoritative?
```

### 2c：过时的参考文献

对于每个跨文档参考（GDD-A 提到了一个机制、值或
系统名称（来自 GDD-B），验证引用的元素是否仍然存在于 GDD-B 中
具有相同的名称和行为：

- 如果 GDD-A 说“战斗系统的组合乘数馈入得分”，请检查
  战斗 GDD 实际上定义了一个输出得分的组合乘数
- 如果 GDD-A 引用“[system].md 中定义的进度曲线”，请检查
  [system].md 实际上具有该曲线，而不是不同的级数模型
- 如果 GDD-A 是在 GDD-B 之前编写的，并且假设 GDD-B 之后的机制
  设计不同，将 GDD-A 标记为包含过时的引用

```
⚠️  Stale Reference
inventory.md (written first): "Item weight uses the encumbrance formula
  from movement.md"
movement.md (written later): Defines no encumbrance formula — uses a flat
  carry limit instead
→ inventory.md references a formula that doesn't exist
```

### 2d：数据和调音旋钮所有权冲突

两个 GDD 不应同时声称拥有相同的数据或调谐旋钮。扫描全部
调整所有 GDD 中的旋钮部分并标记重复项：

```
⚠️  Ownership Conflict
[system-a].md Tuning Knobs: "[multiplier_name] — controls [output] scaling"
[system-b].md Tuning Knobs: "[multiplier_name] — scales [output] with [factor]"
→ Two GDDs define multipliers on the same output. Which owns the final value?
  This will produce either a double-application bug or a design conflict.
```

### 2e：配方兼容性

对于公式相连的 GDD（一个的输出提供另一个的输入），
检查上游公式的输出范围是否在预期范围内
下游公式的输入范围：

- 如果 [system-a].md 输出 [min]–[max] 之间的值，且 [system-b].md 为
  设计用于接收 [min2]–[max2] 之间的值，这种不匹配是故意的吗？
- 如果一个经济体 GDD 期望在 X 范围内获取资源，并且
  级数 GDD 在范围 Y 生成它，经济将是微不足道的或
  无法访问——这是故意的吗？

将不兼容性标记为问题（需要设计判断，不一定是错误的）：

```
⚠️  Formula Range Mismatch
[system-a].md: Max [output] = [value_a] (at max [condition])
[system-b].md: Base [input] = [value_b], max [input] = [value_c]
→ Late-[stage] [scenario] can resolve in a single [event].
  Is this intentional? If not, either [system-a]'s ceiling or [system-b]'s ceiling needs adjustment.
```

### 2f：验收标准交叉检查

扫描所有 GDD 的验收标准部分是否存在矛盾：

- GDD-A 标准：“玩家不会因单次命中而死亡”
- GDD-B 标准：“Boss 攻击造成玩家最大生命值的 150%”
这些验收标准不能同时通过。

---

## 第三阶段：游戏设计整体论

从游戏设计理论和玩家的角度一起回顾所有 GDD
心理学。这些是个别 GDD 评论无法发现的问题，因为
他们需要立即查看所有系统。

### 3a：循环循环竞赛

一款游戏应该有一个主导的进展循环，让玩家觉得“
游戏的“点”，并提供支持循环。当多个
系统作为主要进展驱动因素平等竞争，但玩家并不知道
游戏是关于什么的。

扫描所有 GDD 中的系统：
- 奖励玩家的主要资源（XP、等级、声望、解锁）
- 将自己定义为“核心”或“主”循环
- 与执行相同操作的其他系统具有可比的深度和时间投入

```
⚠️  Competing Progression Loops
combat.md: Awards XP, unlocks abilities, is described as "the core loop"
crafting.md: Awards XP, unlocks recipes, is described as "the primary activity"
exploration.md: Awards XP, unlocks map areas, described as "the main driver"
→ Three systems all claim to be the primary progression loop and all award
  the same primary currency. Players will optimise one and ignore the others.
  Consider: one primary loop with the others as support systems.
```

### 3b：玩家注意力预算

计算期间有多少系统同时需要活跃玩家的关注
一个典型的会话。每个主动管理的系统都需要关注：

- 活跃 = 玩家必须在游戏过程中定期对此系统做出决定
- 被动=系统自动运行，玩家看到结果但不管理它

超过 3-4 个同时活动的系统会对大多数人造成认知超载
玩家。如果并发活动系统超过 4 个，则显示计数和标志：

```
⚠️  Cognitive Load Risk
Simultaneously active systems during [core loop moment]:
  1. [system-a].md — [decision type] (active)
  2. [system-b].md — [resource management] (active)
  3. [system-c].md — [tracking] (active)
  4. [system-d].md — [item/action use] (active)
  5. [system-e].md — [cooldown/timer management] (active)
  6. [system-f].md — [coordination decisions] (active)
→ 6 simultaneously active systems during the core loop.
  Research suggests 3-4 is the comfortable limit for most players.
  Consider: which of these can be made passive or simplified?
```

### 3c：优势策略检测

占优策略使其他策略变得无关紧要——玩家发现它，
只使用它，就会发现游戏的其余部分很无聊。寻找：

- **资源垄断**：一种策略可显着产生资源
  比其他所有人都快
- **无风险力量**：高回报和低风险的策略
  （如果存在高风险策略，则需要相应更高的奖励）
- **无需权衡**：在所有方面都优于所有其他选项的选项
- **明显的最佳路径**：如果任何进展选择“明显正确”，
  其他的都不是真正的选择

```
⚠️  Potential Dominant Strategy
combat.md: Ranged attacks deal 80% of melee damage with no risk
combat.md: Melee attacks deal 100% damage but require close range
→ Unless melee has a significant compensating advantage (AOE, stagger,
  resource regeneration), ranged is dominant — higher safety, only 20% less
  damage. Consider what melee offers that ranged cannot.
```

### 3d：经济循环分析

识别所有 GDD 中的所有资源（金币、XP、制作材料、耐力、
健康、法力等）。对于每种资源，映射其**来源**（玩家如何获得
它）和**下沉**（玩家如何花费它）。

标记危险的经济状况：

| Condition | Sign | Risk |
|-----------|------|------|
| **无限源，无汇** | 资源无限积累 | 后期游戏变得非常简单 |
| **接收器，无源** | 资源消耗为零 | 系统变得不可用 |
| **源>>汇** | 盈余不断积累 | 资源变得毫无意义 |
| **接收器 >> 源** | 持续稀缺 | 挫折与把关 |
| **正反馈循环** | 更多资源→更容易赚更多 | 逃跑的领袖，滚雪球 |
| **No catch-up** | 落后加速赤字 | 不可恢复的状态 |

```
🔴 Economic Imbalance: Unbounded Positive Feedback
gold economy:
  Sources: monster drops (scales with player power), merchant selling (unlimited)
  Sinks: equipment purchase (one-time), ability upgrades (finite count)
→ After equipment and abilities are purchased, gold has no sink.
  Infinite surplus. Gold becomes meaningless mid-game.
  Add ongoing gold sinks (upkeep, consumables, cosmetics, gambling).
```

### 3e：难度曲线一致性

当多个系统随着玩家的进步而扩展时，它们必须缩小规模
兼容的方向和兼容的速率。缩放曲线不匹配
造成意想不到的难度峰值或琐碎化。

对于每个随时间扩展的系统，提取：
- 规模是什么（敌人生命值、玩家伤害、资源成本、区域大小）
- 如何扩展（线性、指数、阶梯）
- 当它扩展时（级别、时间、区域）

比较所有缩放曲线。标志不匹配：

```
⚠️  Difficulty Curve Mismatch
combat.md: Enemy health scales exponentially with area (×2 per area)
progression.md: Player damage scales linearly with level (+10% per level)
→ By area 5, enemies have 32× base health; player deals ~1.5× base damage.
  The gap widens indefinitely. Late areas will become inaccessibly difficult
  unless the curves are reconciled.
```

### 3f：支柱对齐

每个系统都应该明确至少服务于一个设计支柱。一个系统
没有支柱的是“设计范围蔓延”——它存在于游戏中，但不在游戏中
服务于游戏想要达到的目标。

对于每个 GDD 系统，根据设计支柱检查其玩家幻想部分。
标记其所陈述的幻想未映射到任何支柱的任何系统：

```
⚠️  Pillar Drift
fishing-system.md: Player Fantasy — "peaceful, meditative activity"
Pillars: "Brutal Combat", "Tense Survival", "Emergent Stories"
→ The fishing system serves none of the three pillars. Either add a pillar
  that covers it, redesign it to serve an existing pillar, or cut it.
```

还要检查反支柱 - 标记任何执行反支柱功能的系统
明确表示游戏不会这样做：

```
🔴 Anti-Pillar Violation
Anti-Pillar: "We will NOT have linear story progression — player defines their path"
main-quest.md: Defines a 12-chapter linear story with mandatory sequence
→ This system directly violates the defined anti-pillar.
```

### 3g：玩家幻想一致性

玩家对所有系统的幻想应该是兼容的——他们应该
强化玩家在游戏中的一致身份。冲突
玩家的幻想会造成身份混乱。

```
⚠️  Player Fantasy Conflict
combat.md: "You are a ruthless, precise warrior — every kill is earned"
dialogue.md: "You are a charismatic diplomat — violence is always avoidable"
exploration.md: "You are a reckless adventurer — diving in without a plan"
→ Three systems present incompatible identities. Players will feel the game
  doesn't know what it wants them to be. Consider: do these fantasies serve
  the same core identity from different angles, or do they genuinely conflict?
```

---

## 第 4 阶段：跨系统场景演练

从玩家的角度浏览游戏以发现仅存在的问题
出现在多个系统之间的交互边界——事物静态
对个别 GDD 的分析无法浮出水面。

### 4a：确定关键的多系统时刻

扫描所有 GDD 并识别 3-5 个最重要的玩家面临时刻
多个系统同时启动。特别寻找：

- **战斗+经济重叠**：杀死掉落资源、支出的敌人
  战斗中的资源，death/respawn与经济状态交互
- **进度+难度重叠**：升级触发战斗中，能力
  解锁不断变化的战斗力，在进度里程碑上扩展难度
- **叙事+游戏重叠**：对话选择locking/unlocking机制，
  故事节拍中断资源循环、任务完成触发系统
  状态变化
- **3+ 系统链**：触发系统 A 的任何玩家操作，系统 A 会馈送
  进入系统 B，从而触发系统 C（这些是风险最高的交互路径）

在继续之前，用一行描述列出每个已识别的场景。

### 4b：演练每个场景

对于每个场景，明确地逐步执行序列：

1. **触发器** — 哪些玩家操作或游戏事件会启动此操作？
2. **激活顺序** — 哪些系统激活，按什么顺序？
3. **数据流** — 每个系统输出什么，输出是否有效
   链中下一个系统的输入？
4. **玩家体验**——玩家在每一步看到、听到或感觉到什么？
5. **故障模式** — 是否存在以下任何一种？
   - **竞争条件**：两个系统尝试同时修改同一状态
   - **反馈循环**：系统A放大系统B，系统B再放大系统A
     没有盖子或阻尼器
   - **中断的状态转换**：系统假定之前的状态
系统可能已经改变（例如，战斗后“玩家还活着”的假设）
     可能导致死亡的步骤）
   - **矛盾的消息**：玩家收到来自两个人的相互矛盾的反馈
     系统对同一事件做出反应（例如，“成功”声音+“失败”UI）
   - **复合难度峰值**：两个系统同时扩展
     进展点，乘以预期的难度增加
   - **奖励冲突**：两个系统都对同一触发器做出反应
     奖励合计超过预期价值（双倍）
   - **未定义的行为**：GDD 没有指定此组合中会发生什么
     状态（两个系统的规则都没有涵盖它）

```
Example walkthrough:
Scenario: Player kills elite enemy at level-up threshold during active quest

Trigger: Player lands killing blow on elite enemy
→ combat.md: awards kill XP (100 pts)
→ progression.md: XP total crosses level threshold → triggers level-up
  Output: new level, stat increases, ability unlock popup
→ quest.md: kill-count criterion met → triggers quest completion event
  Output: quest reward XP (500 pts), completion fanfare
→ progression.md (again): quest XP added → triggers SECOND level-up in same frame
  ⚠️  Data flow issue: quest.md awards XP without checking if a level-up
  is already in progress. progression.md has no guard against concurrent
  level-up events. Undefined behavior: does the player level up once or twice?
  Does the ability popup fire twice? Does the second level use the updated or
  pre-update stat baseline?
```

### 4c：标记场景问题

对于演练过程中发现的每个问题，请对其严重程度进行分类：

- **BLOCKER**：未定义的行为、破坏的状态转换或矛盾
  玩家消息传递——在这种情况下体验被破坏或不连贯
- **警告**：复合峰值、无上限反馈循环、奖励冲突 —
  这种体验有效，但会产生意想不到的结果
- **信息**：轻微的排序模糊或消息重叠 - 值得注意，但
  不太可能造成玩家可见的问题

将所有发现添加到 **“跨系统场景问题”** 下的输出报告中。
每项发现都必须引用：场景名称、涉及的具体系统、
问题发生的步骤以及故障模式的性质。

---

## 第五阶段：输出评审报告

```
## Cross-GDD Review Report
Date: [date]
GDDs Reviewed: [N]
Systems Covered: [list]

---

### Consistency Issues

#### Blocking (must resolve before architecture begins)
🔴 [Issue title]
[What GDDs are involved, what the contradiction is, what needs to change]

#### Warnings (should resolve, but won't block)
⚠️  [Issue title]
[What GDDs are involved, what the concern is]

---

### Game Design Issues

#### Blocking
🔴 [Issue title]
[What the problem is, which GDDs are involved, design recommendation]

#### Warnings
⚠️  [Issue title]
[What the concern is, which GDDs are affected, recommendation]

---

### Cross-System Scenario Issues

Scenarios walked: [N]
[List scenario names]

#### Blockers
🔴 [Scenario name] — [Systems involved]
[Step where failure occurs, nature of the failure mode, what must be resolved]

#### Warnings
⚠️  [Scenario name] — [Systems involved]
[What the unintended outcome is, recommendation]

#### Info
ℹ️  [Scenario name] — [Systems involved]
[Minor ordering ambiguity or note]

---

### GDDs Flagged for Revision

| GDD | Reason | Type | Priority |
|-----|--------|------|----------|
| [system-a].md | Rule contradiction with [system-b].md | Consistency | Blocking |
| [system-c].md | Stale reference to nonexistent mechanic | Consistency | Blocking |
| [system-d].md | No pillar alignment | Design Theory | Warning |

---

### Verdict: [PASS / CONCERNS / FAIL]

PASS: No blocking issues. Warnings present but don't prevent architecture.
CONCERNS: Warnings present that should be resolved but are not blocking.
FAIL: One or more blocking issues must be resolved before architecture begins.

### If FAIL — required actions before re-running:
[Specific list of what must change in which GDD]
```

---

## 第 6 阶段：Write 报告并标记 GDD

使用 `AskUserQuestion` 获取写入权限：
- 提示：“我可以将此评论写到 `design/gdd/gdd-cross-review-[date].md` 吗？”
- 选项：`[A] Yes — write the report` / `[B] No — skip`

如果任何 GDD 被标记为修订，请使用第二个 `AskUserQuestion`：
- 提示：“我应该更新系统索引以将这些 GDD 标记为需要修订吗？([list of flagged GDDs])”
- 选项：`[A] Yes — update systems index` / `[B] No — leave as-is`
- 如果是：将 systems-index.md 中每个标记的 GDD 的状态字段更新为“需要修订”。
  （请勿在状态值后添加括号 — 其他技能与“需要修订”相匹配
  因为精确的字符串和括号会破坏匹配。）

### 会话状态更新

写完报告后（如果获得批准，则更新系统索引），默默地
附加到 `production/session-state/active.md`：

    ## 会话摘录 — /review-all-gdds [date]
    - 判决：[PASS / CONCERNS / FAIL]
    - 已审核的 GDD：[N]
    - 标记为修订：[逗号分隔列表，或“无”]
    - 阻塞问题：[N — 简短的一行描述，或“无”]
    - 接下来推荐：【第七阶段交接动作，浓缩为一行】
    - 报告：design/gdd/gdd-cross-review-[date].md

如果`active.md`不存在，则以此块为初始内容创建它。
在对话中确认：“会话状态已更新。”

---

## 第 7 阶段：交接

所有文件写入完成后，使用 `AskUserQuestion` 关闭小部件。

在构建选项之前，检查项目状态：
- 是否有任何警告级别的项目是简单编辑（标有“30 秒编辑”、“简短添加”或类似标记）？ → 提供内联快速修复选项
- “标记为修订”表中是否有任何 GDD？ → 为每个提供 /design-review 选项
- Read systems-index.md 适用于状态为：未启动的下一个系统 → 提供 /design-system 选项
- 判决是通过还是令人担忧？ → 提供 /gate-check 或 /create-architecture

动态构建选项列表 - 仅包含适用的选项：

**期权池：**
- `[_] Apply quick fix: [W-XX description] in [gdd-name].md — [effort estimate]`（每个简单编辑警告一个选项；仅适用于警告级别，不适用于阻止）
- `[_] Run /design-review [flagged-gdd-path] — address flagged warnings`（每个标记的 GDD 一个，如果有）
- `[_] Run /design-system [next-system] — next in design order`（始终包含，命名实际系统）
- `[_] Run /create-architecture — begin architecture (verdict is PASS/CONCERNS)`（如果判决不失败则包括）
- `[_] Run /gate-check — validate Systems Design phase gate`（如果判定为“通过”则包括）
- `[_] Stop here`

仅将字母 A、B、C...分配给包含的选项。将最先进的管道选项标记为 `(recommended)`。

永远不要用纯文本结束技能。始终关闭此小部件。

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

1. **Read 静默** — 在呈现任何内容之前加载所有 GDD
2. **展示一切** — 呈现完整的一致性和设计理论分析
   在要求采取任何行动之前
3. **区分阻止和咨询** - 并非每个问题都需要阻止
   建筑；明确做什么
4. **不要做出设计决策** - 标记矛盾和选项，但永远不要
   单方面决定哪个GDD是“正确的”
5. **撰写前询问** — 在撰写报告或更新报告之前确认
   系统索引
6. **具体** — 每个问题都必须引用确切的 GDD、部分和文本
   涉及；没有含糊的警告
