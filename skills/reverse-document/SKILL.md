---
name: reverse-document
description: "从现有实施生成设计或架构文档。从 code/prototypes 向后工作以创建缺失的规划文档。"
# Read 仅限诊断技能 — 无需专业代理委派
---

# 反向文档

该技能分析现有的实现（代码、原型、系统）并生成
适当的设计或架构文档。在以下情况下使用此功能：
- 您在没有先编写设计文档的情况下构建了一个功能
- 您继承了一个没有文档的代码库
- 您制作了一个机械师原型并需要将其形式化
- 您需要记录现有代码背后的“原因”

---

## Workflow

## 第一阶段：解析参数

**格式**：`/reverse-document <type> <path>`

**类型选项**：
- `design` → 生成游戏设计文档（GDD部分）
- `architecture` → 生成架构决策记录 (ADR)
- `concept` → 从原型生成概念文档

**路径**：要分析的目录或文件
- `client/Assets/Scripts/Gameplay/Combat/` → 所有与战斗相关的代码
- `server/service/combat/` → 服务端战斗逻辑
- `client/Assets/Scripts/Core/EventSystem.cs` → 特定文件
- `client/Prototypes/StealthMech/` → 原型目录

**Examples**:
```bash
/reverse-document design client/Assets/Scripts/Gameplay/MagicSystem
/reverse-document architecture client/Assets/Scripts/Core/EntityComponent
/reverse-document design server/service/CombatSystem
/reverse-document concept client/Prototypes/VehicleCombat
```

## 第 2 阶段：分析实施情况

**Read 并了解 code/prototype**：

**对于设计文档 (GDD)：**
- 识别机制、规则、公式
- 提取游戏价值（伤害、冷却时间、范围）
- 查找状态机、能力系统、进程
- 检测代码中处理的边缘情况
- 映射依赖关系（哪些系统交互？）

**对于架构文档 (ADR)：**
- 识别模式（ECS、单例、观察者等）
- 了解技术决策（线程、序列化等）
- 映射依赖关系和耦合
- 评估性能特征
- 寻找限制和权衡

**对于概念文档（原型分析）：**
- 确定核心机制
- 提取新兴的游戏模式
- 记下哪些有效，哪些无效
- 寻找技术可行性见解
- 记录玩家的幻想/感受

## 第三阶段：提出澄清问题

**不要**只描述代码。 **询问**关于意图：

**设计问题**：
- “我看到一个 [resource] 系统在 [activity] 期间耗尽。这是为了：
  - 节奏（防止垃圾邮件）？
  - 资源管理（战略深度）？
  - 还是别的什么？”
- “[mechanic] 似乎很重要。这是核心支柱，还是支持功能？”
- “[Value] 与 [factor] 呈指数级扩展。有意设计，还是需要重新平衡？”

**架构问题**：
- “您正在使用服务定位器模式。选择此模式是为了：
  - 可测试性（模拟依赖项）？
  - 解耦（减少硬引用）？
  - 还是从现有代码继承？”
- “我看到手动内存管理而不是智能指针。性能要求，还是遗留问题？”

**概念问题**：
- “原型机强调隐身而非战斗。这是预期的支柱吗？”
- “玩家似乎利用抓钩来提高速度。功能还是错误？”

## 第四阶段：目前的发现

在起草之前，展示你的发现：

```
I've analyzed [path]/. Here's what I found:

MECHANICS IMPLEMENTED:
- [mechanic-a] with [property] (e.g. timing windows, cooldowns)
- [mechanic-b] (e.g. interaction between two states)
- [resource] system (depletes on [action], regens on [condition])
- [state] system (builds up, triggers [effect])

FORMULAS DISCOVERED:
- [Output] = [formula using discovered variables]
- [Secondary output] = [formula]

UNCLEAR INTENT AREAS:
1. [Resource] system — pacing or resource management?
2. [Mechanic] — core pillar or supporting feature?
3. [Value] scaling — intentional design or needs tuning?

Before I draft the design doc, could you clarify these points?
```

在起草之前等待用户澄清意图。

## 阶段 5：使用模板起草文档

根据类型，使用适当的模板：

| Type | Template | 输出路径 |
|------|----------|-------------|
| `design` | `templates/design-doc-from-implementation.md` | `design/gdd/[system-name].md` |
| `architecture` | `templates/architecture-doc-from-code.md` | `docs/architecture/[decision-name].md` |
| `concept` | `templates/concept-doc-from-prototype.md` | `prototypes/[name]/CONCEPT.md` 或 `design/concepts/[name].md` |

**结构草案**：
- 捕获**存在的东西**（机制、模式、实现）
- 文档**为什么存在**（与用户澄清意图）
- 确定**缺少什么**（未处理的边缘情况、设计中的差距）
- 标记**后续工作**（平衡调整、缺失功能）

## 第 6 阶段：展示草稿并请求批准

**协作协议**：
```
I've drafted the [system-name] design doc based on your code and clarifications.

[Show key sections: Overview, Mechanics, Formulas, Design Intent]

ADDITIONS I MADE:
- Documented [mechanic] as "[intent]" per your clarification
- Added edge cases not in code (e.g., what if [resource] hits 0 mid-[action]?)
- Flagged balance concern: [scaling type] scaling at [boundary condition]

SECTIONS MARKED AS INCOMPLETE:
- "[System] interaction with [other-system]" (not fully implemented yet)
- "[Variant or feature]" (only [subset] implemented so far)

May I write this to design/gdd/[system-name].md?
```

等待批准。用户可以在编写之前请求更改。

## 第 7 阶段：带有元数据的 Write 文档

批准后，用特殊标记写入文件：

```markdown
---
status: reverse-documented
source: [path/]
date: [today]
verified-by: [User name]
---

# [System Name] Design

> **Note**: This document was reverse-engineered from the existing implementation.
> It captures current behavior and clarified design intent. Some sections may be
> incomplete where implementation is partial or intent was unclear.

[Rest of document...]
```

## 第 8 阶段：标记后续工作

写完后，建议后续步骤：

```
✅ Written to design/gdd/combat-system.md

FOLLOW-UP RECOMMENDED:
1. Run /balance-check on combat formulas (exponential scaling concern)
2. Create ADR for stamina system architecture decision
3. Implement missing edge cases:
   - Stamina depletion mid-combo behavior
   - Stagger state during dodge
4. Extend design doc when weapon variety is implemented

Would you like me to tackle any of these now?
```

---

## 模板选择逻辑

| If analyzing... | 使用模板... | Because... |
|----------------|-----------------|------------|
| `client/Assets/Scripts/Gameplay/*` | design-doc-from-implementation.md | 游戏机制 → GDD |
| `server/service/*` | design-doc-from-implementation.md | 服务端逻辑 → GDD |
| `client/Assets/Scripts/Core/*`, `client/Assets/Scripts/AI/*` | architecture-doc-from-code.md | 核心系统 → ADR |
| `client/Prototypes/*` | concept-doc-from-prototype.md | 实验→概念文档 |
| `client/Assets/Scripts/Network/*`, `server/service/network/*` | architecture-doc-from-code.md | 技术系统 → ADR |
| `client/Assets/Scripts/UI/*` | design-doc-from-implementation.md | UI/UX → 设计规范 |

---

## 示例会话：反向记录系统

```
User: /reverse-document design client/Assets/Scripts/Gameplay/[system]

Agent: I'll analyze your [system] implementation to create a design doc.
       [Reads code, discovers mechanics, formulas]

Agent: I've analyzed client/Assets/Scripts/Gameplay/[system]/. Here's what I found:
       [Shows mechanics, formulas, unclear areas]

       Before drafting, could you clarify:
       1. [Resource] system intent?
       2. Is [mechanic] a core pillar?
       3. [Value] scaling — intentional or needs tuning?

User: 1. [Resource] is for pacing, prevent [unwanted behavior]
      2. [Mechanic] is core — I want [design intent]
      3. Yeah, exponential is too much, should be linear

Agent: Perfect, that clarifies the vision. Let me draft the design doc.
       [Shows draft with clarified intent]

       May I write this to design/gdd/[system-name].md?

User: Yes, write it.

Agent: ✅ Written to design/gdd/[system-name].md
       ✅ Marked as [REVERSE-DOCUMENTED]
       ✅ Flagged [value] scaling for rebalancing

       Next steps:
       - Update [formula] to [corrected scaling]
       - Run /balance-check to validate [curve]
       - Document [mechanic] as core pillar in game-pillars.md
```

---

## 协作协议

该技能遵循协作设计原则：

1. **先分析**：Read代码，了解实现
2. **问题意图**：询问“为什么”，而不仅仅是“什么”
3. **当前发现**：展示发现，突出显示不清楚的区域
4. **用户澄清**：将意图与事故分开
5. **文档草案**：根据现实+意图创建文档
6. **显示草稿**：显示关键部分，解释添加内容
7. **获得批准**：“我可以写信给 [filepath] 吗？”批准后：判决：**完成** — 生成文档。拒绝时：判决：**被阻止** - 用户拒绝写入。
8. **标记跟进**：建议相关工作，不自动执行

**永远不要假设意图。在记录“为什么”之前始终询问。**
