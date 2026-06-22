---
name: prototype
description: "快速原型制作工作流程。跳过正常标准来快速验证游戏概念或机制。生成一次性代码和结构化原型报告；如果用户要求 Unity demo，或验证依赖 Unity Play Mode、物理、镜头、输入手感、动画、VFX、Shader、Prefab 或场景搭建，请改用 /unity-demo。"
---

## 第一阶段：定义问题

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则阅读 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

Read 来自参数的概念描述。确定该原型必须回答的核心问题。如果概念模糊，请在继续之前明确说明问题——没有明确问题的原型会浪费时间。

---

## 第 2 阶段：加载项目上下文

Read `AGENTS.md` 用于项目上下文和当前技术堆栈。了解正在使用的引擎、语言和框架，以便使用兼容的工具构建原型。

如果项目可能是 Unity，检查：

- `ProjectSettings/ProjectVersion.txt`
- `Packages/manifest.json`
- `Assets/`
- `*.asmdef` 或 `*.csproj`

如果缺少 `AGENTS.md`，从目录结构和用户请求推断最小可行技术路径，但在计划中标明假设。

---

## 第三阶段：规划原型

用 3-5 个要点定义最小可行原型的样子：

- 核心问题是什么？
- 回答这个问题所需的绝对最少代码是多少？
- 什么可以跳过（错误处理、完善、架构）？

同时选择原型载体，并说明原因：

- **HTML/脚本原型**：适合 UI 流程、数值验证、规则模拟、低保真交互节奏。
- **Unity demo**：适合用户明确要求 Unity，或核心问题依赖 Unity 的 2D/3D 场景、物理、输入手感、镜头、动画、Timeline、NavMesh、粒子/VFX、Shader/材质、Prefab 组合、Inspector 调参或 Play Mode 观察。此时停止本技能的实施部分，改用 `/unity-demo`。
- **正式工程故事**：如果问题必须接入真实账号、数据库、线上协议、生产存档或大量生产系统，停止原型并建议进入设计/架构/故事流程。

在构建之前向用户展示此计划。如果范围不清楚，请寻求确认。

---

## 第四阶段：实施

问：“我可以在 `prototypes/[concept-name]/` 创建原型目录并开始实施吗？”

如果是，则创建目录。每个文件必须以以下内容开头：

```
// PROTOTYPE - NOT FOR PRODUCTION
// Question: [Core question being tested]
// Date: [Current date]
```

Unity demo 的具体文件结构、C# 规则、Editor builder 和 Play Mode 验证由 `/unity-demo` 处理。

有意放宽标准：

- 自由地对值进行硬编码
- 使用占位符资源
- 跳过错误处理
- 使用最简单有效的方法
- 复制代码而不是从生产环境导入

运行原型。观察行为。收集任何可测量的数据（帧时间、交互次数、感觉评估）。

---

## 第 5 阶段：生成原型报告

起草报告：

```markdown
## Prototype Report: [Concept Name]

### Hypothesis
[What we expected to be true -- the question we set out to answer]

### Approach
[What we built, how long it took, what shortcuts we took]

### Result
[What actually happened -- specific observations, not opinions]

### Metrics
[Any measurable data collected during testing]
- Frame time: [if relevant]
- Unity scene / Play Mode notes: [if relevant]
- Feel assessment: [subjective but specific -- "response felt sluggish at
  200ms delay" not "felt bad"]
- Player action counts: [if relevant]
- Iteration count: [how many attempts to get it working]

### Recommendation: [PROCEED / PIVOT / KILL]

[One paragraph explaining the recommendation with evidence]

### If Proceeding
[What needs to change for a production-quality implementation]
- Architecture requirements
- Performance targets
- Scope adjustments from the original design
- Estimated production effort

### If Pivoting
[What alternative direction the results suggest]

### If Killing
[Why this concept does not work and what we should do instead]

### Lessons Learned
[Discoveries that affect other systems or future work]
```

问：“我可以将此报告写给 `prototypes/[concept-name]/REPORT.md` 吗？”

如果是，则写入文件。

---

## 第六阶段：创意总监审核

**查看模式检查** — 在生成 CD-PLAYTEST 之前应用：
- `solo` → 跳过。注意：“CD-PLAYTEST 已跳过 — 单人模式。”继续进行第 7 阶段总结，以原型设计者的建议作为最终结论。
- `lean` → 跳过（不是相位门）。注意：“CD-PLAYTEST 已跳过 — 精益模式。”继续进行第 7 阶段总结，以原型设计者的建议作为最终结论。
- `full` → 正常生成。

使用门 **CD-PLAYTEST** (`.codex/docs/director-gates.md`) 通过 Task 生成 `creative-director`。

通行证：完整的REPORT.md内容、来自`design/gdd/game-concept.md`的原始设计问题、游戏支柱和核心幻想（如果存在）。

创意总监根据游戏的创意愿景和支柱评估原型结果，然后确认、修改或推翻原型师的 PROCEED / PIVOT / KILL 建议。他们的判决是最终的。如果创意总监的结论与原型师的结论不同，请更新 REPORT.md `Recommendation` 部分。

---

## 第 7 阶段：总结和后续步骤

向用户输出摘要：核心问题、结果、原型师的初始建议以及创意总监的最终决定。完整报告链接：`prototypes/[concept-name]/REPORT.md`。

如果**继续**：运行 `/design-system` 开始为此机械师生产 GDD，或运行 `/architecture-decision` 来记录实施前的关键技术决策。

如果 **PIVOT** 或 **KILL**：无需采取进一步行动 - 原型报告即为可交付成果。

结论：**完成**——原型完成。根据上述发现，建议是“继续”、“旋转”或“终止”。

### 重要限制

- 原型代码绝不能从生产源文件导入
- 生产代码绝不能从原型目录导入
- Unity demo 由 `/unity-demo` 处理；其产物必须隔离在 `Assets/Prototypes/` 或 `prototypes/`，不能混入正式场景、正式 Prefab 或生产程序集
- 如果建议继续，则必须从头开始编写生产实现 - 原型代码不会重构到生产中
- 原型总工作量应按时间限制为 1-3 天的工作量
- 如果原型范围开始扩大，停止并重新评估问题是否可以简化

---

## 建议的后续步骤

- **如果继续**：运行 `/design-system [mechanic]` 以编写生产 GDD，或运行 `/architecture-decision` 以在实施前记录关键技术决策
- **如果是PIVOT**：运行`/prototype [revised-concept]`来测试调整的方向
- **如果 KILL**：无需采取进一步行动 - 原型报告即为可交付成果
- 运行 `/playtest-report` 以正式记录原型制作期间进行的任何游戏测试会话
