---
name: create-control-manifest
description: "架构完成后，为程序员生成一个平面的、可操作的规则表——每个系统和每个层必须做什么，绝对不能做什么。摘自所有已接受的 ADR、技术偏好和引擎参考文档。比 ADR 更能立即采取行动（这解释了原因）。"
---

# 创建控制清单

控制清单是为程序员提供的一个扁平的、可操作的规则表。它
回答“我该怎么办？”以及“我绝对不能做什么？” ——由建筑组织
层，从所有接受的 ADR、技术偏好和引擎中提取
参考文档。 ADR 解释“为什么”，而清单则告诉您“什么”。

**输出：** `docs/architecture/control-manifest.md`

**何时运行：** `/architecture-review` 通过且 ADR 处于“已接受”状态后
状态。只要新的 ADR 被接受或现有的 ADR 被修改，就重新运行。

---

## 1. 加载所有输入

### ADRs
- Glob `docs/architecture/adr-*.md` 并读取每个文件
- 过滤为仅接受的 ADR（状态：已接受）- 跳过建议的、已弃用的、
  Superseded
- 记下每个规则来源的 ADR 编号和标题

### 技术偏好
- Read `.codex/docs/technical-preferences.md`
- 摘录：命名约定、性能预算、批准 libraries/addons、
  禁止的图案

### 发动机参考
- Read `docs/engine-reference/[engine]/VERSION.md` 发动机+版本
- Read `docs/engine-reference/[engine]/deprecated-apis.md` — 这些变成
  禁止 API 条目
- Read `docs/engine-reference/[engine]/current-best-practices.md` 如果存在

报告：“已加载 [N] 接受的 ADR，引擎：[名称 + 版本]。”

---

## 2.从每个ADR中提取规则

对于每个已接受的 ADR，提取：

### 所需模式（来自“实施指南”部分）
- 每一个“必须”、“应该”、“要求”、“总是”的陈述
- 强制规定的每种特定模式或方法

### 禁止的方法（来自“考虑的替代方案”部分）
- 每一个被明确拒绝的替代方案——*为什么*它被拒绝变成
  规则（“永远不要因为 Y 而使用 X”）
- 任何明确指出的反模式

### 性能护栏（来自“性能影响”部分）
- 预算约束：“该系统每帧最大 N 毫秒”
- 内存限制：“该系统不得超过 N MB”

### 引擎 API 约束（来自“引擎兼容性”部分）
- 截止后需要验证的 API
- 与默认 LLM 假设不同的已验证行为
- API 在固定引擎版本中表现不同的字段或方法

### 层分类
按每个规则所管理的系统的架构层对每个规则进行分类：
- **基础**：场景管理、事件架构、save/load、引擎初始化
- **核心**：核心游戏循环、主要玩家系统、physics/collision
- **功能**：二级系统、二级机制、人工智能
- **演示**：渲染、音频、UI、VFX、着色器

如果 ADR 跨越多个层，请将规则复制到每个相关层中。

---

## 3.添加全局规则

组合适用于所有层的规则：

### 来自 technical-preferences.md：
- 命名约定（类、变量、signals/events、文件、常量）
- 性能预算（目标帧率、帧预算、绘制调用限制、内存上限）

### 来自 deprecated-apis.md：
- 所有已弃用的 API → 禁止的 API 条目

### 来自 current-best-practices.md（如果有）：
- 引擎推荐的模式 → 必填项

### 来自 technical-preferences.md 禁止模式：
- 直接复制任何“禁止模式”条目

---

## 4. 写作前展示规则摘要

在编写清单之前，向用户提供摘要：

```
## Control Manifest Preview
Engine: [name + version]
ADRs covered: [list ADR numbers]
Total rules extracted:
  - Foundation layer: [N] required, [M] forbidden, [P] guardrails
  - Core layer: [N] required, [M] forbidden, [P] guardrails
  - Feature layer: ...
  - Presentation layer: ...
  - Global: [N] naming conventions, [M] forbidden APIs, [P] approved libraries
```

问：“这看起来完整吗？在编写清单之前需要添加或删除任何规则吗？”

---

## 4b.总监之门 — 技术审查

**审查模式检查** — 在生成 TD-MANIFEST 之前应用：
- `solo` → 跳过。注意：“TD-MANIFEST 已跳过 — 单人模式。”进入第 5 阶段。
- `lean` → 跳过。注意：“跳过 TD-MANIFEST — 精益模式。”进入第 5 阶段。
- `full` → 正常生成。

使用门 **TD-MANIFEST** (`.codex/docs/director-gates.md`) 通过 Task 生成 `technical-director`。

通过：第 4 阶段的控制清单预览（每层规则计数、完整提取的规则列表）、涵盖的 ADR 列表、引擎版本以及源自 technical-preferences.md 或引擎参考文档的任何规则。

技术总监审查是否：
- 所有强制 ADR 模式均已捕获并准确表述
- 禁止的方法是完整且正确的
- 未添加缺少源 ADR 或首选项文档的规则
- 性能护栏与 ADR 约束一致

执行判决：
- **批准** → 进入第 5 阶段
- **问题** → 通过 `AskUserQuestion` 进行表面处理，并带有选项：`Revise flagged rules` / `Accept and proceed` / `Discuss further`
- **拒绝** → 不写清单；修复标记的规则并重新呈现摘要

---

## 5. Write 控制清单

问：“我可以把这个写到`docs/architecture/control-manifest.md`吗？”

Format:

```markdown
# Control Manifest

> **Engine**: [name + version]
> **Last Updated**: [date]
> **Manifest Version**: [date]
> **ADRs Covered**: [ADR-NNNN, ADR-MMMM, ...]
> **Status**: [Active — regenerate with `/create-control-manifest update` when ADRs change]

`Manifest Version` is the date this manifest was generated. Story files embed
this date when created. `/story-readiness` compares a story's embedded version
to this field to detect stories written against stale rules. Always matches
`Last Updated` — they are the same date, serving different consumers.

This manifest is a programmer's quick-reference extracted from all Accepted ADRs,
technical preferences, and engine reference docs. For the reasoning behind each
rule, see the referenced ADR.

---

## Foundation Layer Rules

*Applies to: scene management, event architecture, save/load, engine initialisation*

### Required Patterns
- **[rule]** — source: [ADR-NNNN]
- **[rule]** — source: [ADR-NNNN]

### Forbidden Approaches
- **Never [anti-pattern]** — [brief reason] — source: [ADR-NNNN]

### Performance Guardrails
- **[system]**: max [N]ms/frame — source: [ADR-NNNN]

---

## Core Layer Rules

*Applies to: core gameplay loop, main player systems, physics, collision*

### Required Patterns
...

### Forbidden Approaches
...

### Performance Guardrails
...

---

## Feature Layer Rules

*Applies to: secondary mechanics, AI systems, secondary features*

### Required Patterns
...

### Forbidden Approaches
...

---

## Presentation Layer Rules

*Applies to: rendering, audio, UI, VFX, shaders, animations*

### Required Patterns
...

### Forbidden Approaches
...

---

## Global Rules (All Layers)

### Naming Conventions
| Element | Convention | Example |
|---------|-----------|---------|
| Classes | [from technical-preferences] | [example] |
| Variables | [from technical-preferences] | [example] |
| Signals/Events | [from technical-preferences] | [example] |
| Files | [from technical-preferences] | [example] |
| Constants | [from technical-preferences] | [example] |

### Performance Budgets
| Target | Value |
|--------|-------|
| Framerate | [from technical-preferences] |
| Frame budget | [from technical-preferences] |
| Draw calls | [from technical-preferences] |
| Memory ceiling | [from technical-preferences] |

### Approved Libraries / Addons
- [library] — approved for [purpose]

### Forbidden APIs ([engine version])
These APIs are deprecated or unverified for [engine + version]:
- `[api name]` — deprecated since [version] / unverified post-cutoff
- Source: `docs/engine-reference/[engine]/deprecated-apis.md`

### Cross-Cutting Constraints
- [constraint that applies everywhere, regardless of layer]
```

---

## 6. 建议后续步骤

写完清单后：

- 如果 epics/stories 尚不存在：“运行 `/create-epics layer: foundation`，然后 `/create-stories [epic-slug]` — 程序员
  现在可以在编写故事实现注释时使用此清单。”
- 如果这是再生（清单已存在）：“已更新。推荐
  通知团队更改的规则 - 特别是任何新的禁止条目。”

---

## 协作协议

1. **静默加载** - 在呈现任何内容之前读取所有输入
2. **首先显示摘要** — 让用户在编写之前了解范围
3. **写入前询问** — 在创建或覆盖清单之前始终确认。写入时：结论：**完成** — 控制清单已写入。拒绝时：判决：**被阻止** - 用户拒绝写入。
4. **获取每条规则的来源** — 切勿添加不追踪到 ADR 的规则，
   技术偏好，或引擎参考文档
5. **无解释** — 提取 ADR 中规定的规则；不要转述
   以改变意义的方式
