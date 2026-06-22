---
name: setup-engine
description: "配置项目的游戏引擎和版本。将引擎固定在 AGENTS.md 中，检测知识差距，并在版本超出 LLM 训练数据时通过 WebSearch 填充引擎参考文档。"
---

当该技能被调用时：

## 1. 解析参数

四种模式：

- **完整规格**：`/setup-engine godot 4.6` — 提供引擎和版本
- **仅限引擎**：`/setup-engine unity` — 提供引擎，将查找版本
- **无参数**：`/setup-engine` — 完全引导模式（引擎推荐+版本）
- **刷新**：`/setup-engine refresh` — 更新参考文档（参见第 10 节）
- **升级**：`/setup-engine upgrade [old-version] [new-version]` — 迁移到新的引擎版本（参见第 11 节）

---

## 2. 引导模式（无参数）

如果未指定引擎，则运行交互式引擎选择过程：

### 检查现有的游戏概念
- Read `design/gdd/game-concept.md` 如果存在 — 提取流派、范围、平台
  目标、艺术风格、团队规模以及 `/brainstorm` 的任何引擎推荐
- 如果不存在概念，则通知用户：
  > “未找到游戏概念。首先考虑运行 `/brainstorm` 以发现什么
  > 你想要构建——它还会推荐一个引擎。或者告诉我你的情况
  > 游戏，我可以帮你挑选。”

### 如果用户想在没有概念的情况下进行选择，请按以下顺序询问：

**问题 1 — 先前的经验**（始终首先通过 `AskUserQuestion` 询问）：
- 提示：“您以前曾在这些发动机中工作过吗？”
- 选项：`Godot` / `Unity` / `Unreal Engine 5` / `Multiple — I'll explain` / `None of them`
- 如果他们选择特定的引擎→推荐该引擎。先前的经验胜过所有其他因素。与他们确认并跳过矩阵。
- 如果“无”或“多个”→ 继续回答以下问题。

**问题 2-6 — 决策矩阵输入**（仅当之前没有引擎经验时）：

**问题 2 — 目标平台**（始终通过 `AskUserQuestion` 询问这一秒 — 平台在任何其他因素之前消除或加重引擎）：
- 提示：“这款游戏的目标平台是什么？”
- 选项：`PC (Steam / Epic)` / `Mobile (iOS / Android)` / `Console` / `Web / Browser` / `Multiple platforms`
- 直接反馈到推荐中的平台规则：
  - 手机 → Unity 强烈推荐； Unreal 不太合适； Godot 适用于简单的移动设备
  - 控制台 → Unity 或 Unreal； Godot 控制台支持需要第三方发行商或大量额外工作
  - Web → Godot 干净地导出到 Web； Unity WebGL 正常运行； Unreal 的网络支持很差
  - 仅限 PC → 所有引擎均可用；其他因素决定
  - 多个 → Unity 是 PC/mobile/console 中最便携的

1. **什么样的游戏？**（2D、3D 或两者兼而有之？）
2. **主要输入法？**（keyboard/mouse、游戏手柄、触摸或混合？）
3. **团队规模和经验？**（独奏初学者、独奏经验丰富、小团队？）
4. **有任何强烈的语言偏好吗？**（GDScript、C#、C++、可视化脚本？）
5. **引擎许可预算？**（仅免费，或商业许可可以吗？）

### 产生推荐

不要使用消除引擎的简单评分矩阵。相反，通过用户的个人资料与下面的诚实权衡进行推理，然后提供具有完整上下文的 1-2 个建议。始终以用户选择结束——永远不要强行做出结论。

**引擎诚实的权衡：**

**Godot 4**
- 真正的优势：2D（同类最佳）、stylized/indie 3D、快速迭代、永久免费（MIT）、开源、最温和的学习曲线、最适合想要完全控制的独立开发者
- 真正的限制：与 Unity/Unreal 相比，3D 生态系统很薄弱（针对 3D 特定问题的教程、资产、社区答案较少）；大型开放世界 3D 非常困难，并且在 Godot 中基本上未经测试；控制台导出需要第三方发行商或大量额外工作；较小的专业就业市场
- 授权现实：真正免费，没有收入门槛。麻省理工学院许可证意味着您拥有一切。
- 最适合：任何范围的 2D 游戏； stylized/atmospheric 3D；包含 3D 世界（非开放世界）；第一个学习曲线很重要的游戏项目；无论规模如何，预算都是严格限制的项目

**Unity**
- 真正的优势：中型 3D 和移动行业标准；海量资源商店和教程生态系统； C#是一门专业语言；为独立游戏提供最佳控制台认证支持；几乎所有类型的强大社区
- 真正的局限性：2023 年的许可争议损害了信任（提出运行费后又撤回——政策变化的风险仍然存在）； C# 的初始曲线比 GDScript 更陡；对于简单项目，比 Godot 更重的编辑器
- 许可现实：收入低于 20 万美元且安装次数低于 20 万次免费 (Unity Personal/Plus)。只有当游戏真正成功时，成本才会变得高昂——大多数独立游戏从未达到这个门槛。 2023 年的争议值得了解，但当前的实际条款对于大多数独立开发者来说是合理的。
- 最适合：手机游戏；中范围 3D；针对控制台的游戏；具有C#背景的开发人员；需要大型资产存储的项目； 2-5人一组

**Unreal 发动机 5**
- 真正的优势：一流的 3D 视觉效果（Lumen、Nanite、混沌物理）； AAA 和逼真 3D 行业标准；大型开放世界支持已经成熟并经过生产测试； Blueprint 可视化脚本降低了 C++ 障碍；非常适合针对高端 PC 或游戏机的游戏
- 真正的局限性：最陡的学习曲线；最重的编辑器（编译时间慢，项目规模大）；对于 stylized/2D/small-scope 游戏来说过度杀伤； C++ 确实很难；不适合移动或网络；总收入超过 100 万美元时收取 5% 的特许权使用费
- 授权现实：5% 的版税仅适用于每部作品总收入达到 100 万美元之后。对于第一款游戏或任何未达到 100 万美元的游戏，无需任何费用。这个门槛足够高，大多数独立开发者永远不会支付。
- 最适合：AAA 品质 3D；大型开放世界游戏；逼真的视觉效果；有C++经验或愿意使用Blueprint的开发者；面向高端 PC/console 的游戏，其中视觉保真度是核心卖点

**特定类型的指导**（将其纳入建议中）：
- 2D 任何样式 → Godot 强烈首选
- 3D 风格化/大气/封闭世界 → Godot 可行，Unity 可靠替代品
- 3D开放世界（大型、无缝）→ Unity或Unreal； Godot 尚未经过生产验证
- 3D 逼真 / AAA 品质 → Unreal
- 移动优先 → Unity 强烈首选
- 控制台优先 → Unity 或 Unreal； Godot 控制台支持需要额外的工作
- 恐怖/叙事/行走模拟 → 任何引擎；与艺术风格和团队经验相匹配
- 动作角色扮演游戏 / 魂类 → Unity 或 Unreal for 3D；社区支持和资产在这里很重要
- 2D 平台游戏 → Godot
- 策略/自上而下/RTS → Godot 或 Unity 取决于 2D 与 3D

**推荐格式：**
1. 显示比较表，其中用户的特定因素为行
2. 给出诚实推理的初步建议
3. 列出最佳替代方案以及何时选择它
4. 明确指出：“这是一个起点，而不是一个结论——你可以随时迁移引擎，并且许多开发人员可以在项目之间切换。”
5. 使用 `AskUserQuestion` 确认：“这个建议感觉正确吗，或者您想探索不同的引擎吗？”
   - 选项：`[Primary engine] (Recommended)` / `[Alternative engine]` / `[Third engine]` / `Explore further` / `Type something`

**如果用户选择“进一步探索”：**
将 `AskUserQuestion` 与特定于概念的深入主题结合使用。始终根据用户的实际概念生成这些选项 - 不要使用通用选项。始终至少包括：
- 主引擎对此概念的具体限制（例如，“Godot 3D 对于 [genre] 实际上能走多远？”）
- 替代引擎对此概念的具体权衡
- 语言选择对该概念的技术挑战的影响
- 任何特定于概念的技术问题（例如，自适应音频、开放世界流媒体、多人网络代码）

用户可以选择多个主题。在返回引擎确认问题之前，深入回答每个选定的主题。

---

## 3. 查找当前版本

选择引擎后：

- 如果提供了版本，请使用它
- 如果未提供版本，请使用 WebSearch 查找最新的稳定版本：
  - 搜索：`"[engine] latest stable version [current year]"`
  - 与用户确认：“最新稳定的[engine]是[version]，用这个吗？”

---

## 4.更新AGENTS.md技术堆栈

### 语言选择（仅限 Godot）

如果选择 Godot，请在显示建议的技术堆栈之前询问用户使用哪种语言：

> “Godot 支持两种主要语言：
>
>   **A) GDScript** — Python 类似，Godot 原生，最快迭代。最适合来自 Python 或 Lua 的初学者、独立开发者和团队。
>   **B) C#** — .NET 8+，Unity 开发人员熟悉，更强大的 IDE 工具（Rider / Visual Studio），在繁重的逻辑上略有性能优势。
>   **C) 两者** — GDScript 用于 gameplay/UI 脚本，C# 用于性能关键型系统。高级设置 - 需要 .NET SDK 以及 Godot。
>
> 这个项目主要使用哪一个？”

记录选择。它确定 AGENTS.md 模板、命名约定、专家路由以及为整个项目的代码文件生成哪个代理。

---

Read `AGENTS.md` 并向用户展示建议的技术堆栈更改。
问：“我可以将这些引擎设置写入 `AGENTS.md` 吗？”

在进行任何编辑之前等待确认。

更新技术堆栈部分，将 `[CHOOSE]` 占位符替换为实际值：

**对于 Godot** — 使用与上面选择的语言匹配的模板。有关所有三种变体（GDScript、C#、两者），请参阅本技能底部的**附录 A**。

**对于 Unity：**
```markdown
- **Engine**: Unity [version]
- **Language**: C#
- **Build System**: Unity Build Pipeline
- **Asset Pipeline**: Unity Asset Import Pipeline + Addressables
```

**对于 Unreal：**
```markdown
- **Engine**: Unreal Engine [version]
- **Language**: C++ (primary), Blueprint (gameplay prototyping)
- **Build System**: Unreal Build Tool (UBT)
- **Asset Pipeline**: Unreal Content Pipeline
```

---

## 5. 填写技术偏好

更新 AGENTS.md 后，创建或更新 `.codex/docs/technical-preferences.md`
适合引擎的默认值。 Read 先现有模板，然后填写：

### 引擎和语言部分
- 根据步骤 4 中选择的引擎进行填充

### 命名约定（引擎默认值）

**对于 Godot** — 请参阅 **附录 A** 了解 GDScript、C# 和两种变体。

**对于 Unity (C#)：**
- 类：PascalCase（例如 `PlayerController`）
- 公共 fields/properties：PascalCase（例如 `MoveSpeed`）
- 私有字段：_camelCase（例如，`_moveSpeed`）
- 方法：PascalCase（例如 `TakeDamage()`）
- 文件：PascalCase 匹配类（例如 `PlayerController.cs`）
- 常量：PascalCase 或 UPPER_SNAKE_CASE

**对于 Unreal (C++)：**
- 类：前缀 PascalCase（`A` 表示 Actor，`U` 表示 UObject，`F` 表示结构）
- 变量：PascalCase（例如 `MoveSpeed`）
- 函数：PascalCase（例如，`TakeDamage()`）
- 布尔值：`b` 前缀（例如，`bIsAlive`）
- 文件：不带前缀的匹配类（例如，`PlayerController.h`）

### 输入与平台部分

使用第 2 部分中收集的答案（或提取的答案）填充 `## Input & Platform`
从游戏概念来看）。使用此映射导出值：

| 平台目标 | 游戏手柄支持 | 触摸支持 |
|-----------------|-----------------|---------------|
| PC only | 部分（推荐） | None |
| Console | Full | None |
| Mobile | None | Full |
| PC + Console | Full | None |
| PC + Mobile | Partial | Full |
| Web | Partial | Partial |

对于 **主要输入**，使用游戏类型的主要输入：
- Action/RPG/platformer 瞄准控制台 → 游戏手柄
- Strategy/point-and-click/RTS → Keyboard/Mouse
- 手机游戏 → 触摸
- 跨平台→询问用户

呈现导出的值并要求用户在书写前确认或调整。

填充部分示例：
```markdown
## Input & Platform
- **Target Platforms**: PC, Console
- **Input Methods**: Keyboard/Mouse, Gamepad
- **Primary Input**: Gamepad
- **Gamepad Support**: Full
- **Touch Support**: None
- **Platform Notes**: All UI must support d-pad navigation. No hover-only interactions.
```

### 剩余部分
- **性能预算**：使用 `AskUserQuestion`：
  - 提示：“我应该现在设置默认性能预算，还是留到以后再设置？”
  - 选项：`[A] Set defaults now (60fps, 16.6ms frame budget, engine-appropriate draw call limit)` / `[B] Leave as [TO BE CONFIGURED] — I'll set these when I know my target hardware`
  - 如果 [A]：使用建议的默认值填充。如果 [B]：保留为占位符。
- **测试**：建议适合引擎的框架（Godot 的 GUT、Unity 的 NUnit 等）——在添加之前询问。
- **禁止的模式**：保留为占位符 — 不要预先填充。
- **允许的库**：保留为占位符 - 不要预先填充项目当前不需要的依赖项。仅当正在积极集成时才在此处添加库，而不是推测性的。

> **Guardrail**：切勿向允许的库添加推测依赖项。例如，除非在此会话中主动开始 Steam 集成，否则请勿添加 GodotSteam。启动后集成应在工作开始时添加到允许的库中，而不是在引擎设置期间。

### 发动机专家路由

还要使用所选引擎的正确路由填充 `technical-preferences.md` 中的 `## Engine Specialists` 部分：

**对于 Godot** — 请参阅 **附录 A** 了解与所选语言匹配的路由表。

**对于 Unity：**
```markdown
## Engine Specialists
- **Primary**: unity-specialist
- **Language/Code Specialist**: unity-specialist (C# review — primary covers it)
- **Shader Specialist**: unity-shader-specialist (Shader Graph, HLSL, URP/HDRP materials)
- **UI Specialist**: unity-ui-specialist (UI Toolkit UXML/USS, UGUI Canvas, runtime UI)
- **Additional Specialists**: unity-dots-specialist (ECS, Jobs system, Burst compiler), unity-addressables-specialist (asset loading, memory management, content catalogs)
- **Routing Notes**: Invoke primary for architecture and general C# code review. Invoke DOTS specialist for any ECS/Jobs/Burst code. Invoke shader specialist for rendering and visual effects. Invoke UI specialist for all interface implementation. Invoke Addressables specialist for asset management systems.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.cs files) | unity-specialist |
| Shader / material files (.shader, .shadergraph, .mat) | unity-shader-specialist |
| UI / screen files (.uxml, .uss, Canvas prefabs) | unity-ui-specialist |
| Scene / prefab / level files (.unity, .prefab) | unity-specialist |
| Native extension / plugin files (.dll, native plugins) | unity-specialist |
| General architecture review | unity-specialist |
```

**对于 Unreal：**
```markdown
## Engine Specialists
- **Primary**: unreal-specialist
- **Language/Code Specialist**: ue-blueprint-specialist (Blueprint graphs) or unreal-specialist (C++)
- **Shader Specialist**: unreal-specialist (no dedicated shader specialist — primary covers materials)
- **UI Specialist**: ue-umg-specialist (UMG widgets, CommonUI, input routing, widget styling)
- **Additional Specialists**: ue-gas-specialist (Gameplay Ability System, attributes, gameplay effects), ue-replication-specialist (property replication, RPCs, client prediction, netcode)
- **Routing Notes**: Invoke primary for C++ architecture and broad engine decisions. Invoke Blueprint specialist for Blueprint graph architecture and BP/C++ boundary design. Invoke GAS specialist for all ability and attribute code. Invoke replication specialist for any multiplayer or networked systems. Invoke UMG specialist for all UI implementation.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.cpp, .h files) | unreal-specialist |
| Shader / material files (.usf, .ush, Material assets) | unreal-specialist |
| UI / screen files (.umg, UMG Widget Blueprints) | ue-umg-specialist |
| Scene / prefab / level files (.umap, .uasset) | unreal-specialist |
| Native extension / plugin files (Plugin .uplugin, modules) | unreal-specialist |
| Blueprint graphs (.uasset BP classes) | ue-blueprint-specialist |
| General architecture review | unreal-specialist |
```

### 协作步骤
向用户呈现填写的首选项。对于 Godot，请包含所选语言并记下完整命名约定和路由表所在的位置：
> “以下是 [engine] ([language if Godot]) 的默认技术首选项。命名约定和专业路由位于本技能的附录 A 中 - 我将应用 [GDScript/C#/Both] 变体。想要自定义其中任何一个，还是应该保存默认值？”

对于所有其他引擎，直接提供默认值，而不参考附录。

在写入文件之前等待批准。

---

## 6. 确定知识差距

检查引擎版本是否可能超出法学硕士的训练数据。

**已知的大致覆盖范围**（随着型号的变化更新）：
- LLM 知识截止日期：**2025 年 5 月**
- Godot：训练数据可能覆盖~4.3
- Unity：训练数据可能覆盖 ~2023.x / 早期 6000.x
- Unreal：训练数据可能覆盖 ~5.3/早期 5.4

将用户选择的版本与这些基线进行比较：

- **在训练数据中** → `LOW RISK` — 参考文档可选，但推荐
- **靠近边缘** → `MEDIUM RISK` — 推荐参考文档
- **超越训练数据** → `HIGH RISK` — 需要参考文档

告知用户他们属于哪个类别以及原因。

---

## 7. 填充引擎参考文档

### 如果在训练数据内（低风险）：

创建最小的 `docs/engine-reference/<engine>/VERSION.md`：

```markdown
# [Engine] — Version Reference

| Field | Value |
|-------|-------|
| **Engine Version** | [version] |
| **Project Pinned** | [today's date] |
| **LLM Knowledge Cutoff** | May 2025 |
| **Risk Level** | LOW — version is within LLM training data |

## Note

This engine version is within the LLM's training data. Engine reference
docs are optional but can be added later if agents suggest incorrect APIs.

Run `/setup-engine refresh` to populate full reference docs at any time.
```

不要创建 breaking-changes.md、deprecated-apis.md 等 - 他们会
以最小的价值添加上下文成本。

### 如果超出训练数据（中风险或高风险）：

通过搜索网络创建完整的参考文档集：

1. **搜索官方migration/upgrade指南**：
   - `"[engine] [old version] to [new version] migration guide"`
   - `"[engine] [version] breaking changes"`
   - `"[engine] [version] changelog"`
   - `"[engine] [version] deprecated API"`

2. **从官方文档中获取并提取**：
   - 从训练截止到当前每个版本之间的重大变化
   - 已弃用的 API 及其替代品
   - 新功能和最佳实践

问：“我可以在 `docs/engine-reference/<engine>/` 下创建引擎参考文档吗？”

在写入任何文件之前等待确认。

3. **创建完整的参考目录**：
   ```
   docs/engine-reference/<engine>/
   ├── VERSION.md              # Version pin + knowledge gap analysis
   ├── breaking-changes.md     # Version-by-version breaking changes
   ├── deprecated-apis.md      # "Don't use X → Use Y" tables
   ├── current-best-practices.md  # New practices since training cutoff
   └── modules/                # Per-subsystem references (create as needed)
   ```

4. **使用网络搜索中的真实数据填充每个文件**，如下
   现有参考文档中建立的格式。每个文件必须有
   “最后验证：[date]”标头。

5. **对于模块文件**：仅为重要的子系统创建模块
   发生了变化。不要创建空的或最小的模块文件。

---

## 8.更新AGENTS.md导入

问：“我可以更新 `AGENTS.md` 中的 `@` 导入以指向新引擎参考吗？”

等待确认，然后更新“引擎版本参考”下的 `@` 导入以指向
正确的发动机：

```markdown
## Engine Version Reference

@docs/engine-reference/<engine>/VERSION.md
```

如果先前的导入指向不同的引擎（例如，从
Godot 至 Unity），更新它。

---

## 9. 更新代理说明

问：“我可以在引擎专家代理文件中添加版本感知部分吗？”在进行任何编辑之前。

对于所选引擎的专业代理，请验证他们是否拥有
“版本意识”部分。如果没有，请按照以下模式添加一个
现有Godot专业代理商。

该部分应指示代理人：
1. Read `docs/engine-reference/<engine>/VERSION.md`
2. 在建议代码之前检查已弃用的 API
3. 检查相关版本转换的重大更改
4. 使用WebSearch验证不确定的API

---

## 10. 刷新子命令

如果作为 `/setup-engine refresh` 调用：

1. Read 现有`docs/engine-reference/<engine>/VERSION.md` 获取
   当前引擎和版本
2. 使用 WebSearch 检查：
   - 自上次验证以来新引擎发布
   - 更新了迁移指南
   - 新弃用的 API
3. 用新发现更新所有参考文档
4. 更新所有修改文件的“上次验证”日期
5. 报告发生的变化

---

## 11. 升级子命令

如果作为 `/setup-engine upgrade [old-version] [new-version]` 调用：

### 步骤 1 — Read 当前版本状态

Read `docs/engine-reference/<engine>/VERSION.md` 确认当前固定
版本、风险级别以及已记录的任何迁移说明 URL。如果
`old-version` 未作为参数提供，请使用此中的固定版本
file.

### 第 2 步 — 获取迁移指南

使用 WebSearch 和 WebFetch 查找官方迁移指南
`old-version` 和 `new-version`：

- 搜索：`"[engine] [old-version] to [new-version] migration guide"`
- 搜索：`"[engine] [new-version] breaking changes changelog"`
- 如果已经记录了，请从 VERSION.md 获取迁移指南 URL，
  或使用通过搜索找到的 URL。

提取：重命名 API、删除 API、更改默认值、行为更改以及
任何“必须迁移”的项目。

### 第 3 步 — 升级前审核

扫描 `src/` 查找使用已知已弃用或更改的 API 的代码
目标版本：

- 使用 Grep 搜索从迁移中提取的已弃用的 API 名称
  指南（例如旧函数名称、删除的节点类型、更改的属性名称）
- 列出每个匹配的文件，以及找到的特定 API 参考

将审核结果以表格形式呈现：

```
Pre-Upgrade Audit: [engine] [old-version] → [new-version]
==========================================================

Files requiring changes:
  File                                        | Deprecated API Found       | Effort
  ------------------------------------------- | -------------------------- | ------
  client/Assets/Scripts/Game/PlayerMovement.cs | old_api_name               | Low
  client/Assets/Scripts/UI/HUD.cs             | removed_node_type          | Medium

Breaking changes to watch for:
  - [change description from migration guide]
  - [change description from migration guide]

Recommended migration order (dependency-sorted):
  1. [system/layer with fewest dependencies first]
  2. [next system]
  ...
```

如果在 `src/` 中未找到已弃用的 API，则报告：“没有已弃用的 API 用法
在 src/ 中找到 — 升级可能风险较低。”

### 第 4 步 — 更新前确认

在进行任何更改之前询问用户：

> “升级前审核已完成。使用已弃用的 API 发现 [N] 文件。
> 是否继续将 VERSION.md 升级到 [new-version]？
> （这将更新固定版本并添加迁移注释 - 它不会
> 更改任何源文件。源迁移是手动或通过故事完成的。）”

在继续之前等待明确的确认。

### 第 5 步 — 更新 VERSION.md

确认后：

1. 更新`docs/engine-reference/<engine>/VERSION.md`：
   - `Engine Version` → `[new-version]`
   - `Project Pinned` → 今天的日期
   - `Last Docs Verified` → 今天的日期
   - 重新评估并更新 `Risk Level` 和 `Post-Cutoff Version Timeline`
     表如果新版本超出了 LLM 知识截止点
   - 添加 `## Migration Notes — [old-version] → [new-version]` 部分
     包含：迁移指南 URL、关键重大更改、已弃用的 API
     在这个项目中发现，并从审核中推荐迁移顺序

2. 如果引擎中存在 `breaking-changes.md` 或 `deprecated-apis.md`
   参考目录，将新版本的更改附加到这些文件中。

### 第 6 步 — 升级后提醒

更新VERSION.md后，输出：

```
VERSION.md updated: [engine] [old-version] → [new-version]

Next steps:
1. Migrate deprecated API usages in the [N] files listed above
2. Run /setup-engine refresh after upgrading the actual engine binary to
   verify no new deprecations were missed
3. Run /architecture-review — the engine upgrade may invalidate ADRs that
   reference specific APIs or engine capabilities
4. If any ADRs are invalidated, run /propagate-design-change to update
   downstream stories
```

---

## 12. 输出总结

设置完成后，输出：

```
Engine Setup Complete
=====================
Engine:          [name] [version]
Language:        [GDScript | C# | GDScript + C# | C# | C++ + Blueprint]
Knowledge Risk:  [LOW/MEDIUM/HIGH]
Reference Docs:  [created/skipped]
AGENTS.md:       [updated]
Tech Prefs:      [created/updated]
Agent Config:    [verified]

Next Steps:
1. Review docs/engine-reference/<engine>/VERSION.md
2. [If from /brainstorm] Run /map-systems to decompose your concept into individual systems
3. [If from /brainstorm] Run /design-system to author per-system GDDs (guided, section-by-section)
4. [If from /brainstorm] Run /prototype [core-mechanic] to test the core loop
5. [If fresh start] Run /brainstorm to discover your game concept
6. Create your first milestone: /sprint-plan new
```

---

结论：**完成** — 引擎已配置并已填充参考文档。

## Guardrails

- 永远不要猜测引擎版本 - 始终通过网络搜索或用户确认进行验证
- 切勿在没有询问的情况下覆盖现有参考文档 - 追加或更新
- 如果不同引擎的参考文档已存在，请在更换前询问
- 在进行 AGENTS.md 编辑之前，始终向用户显示您将要更改的内容
- 如果 WebSearch 返回不明确的结果，请向用户显示并让他们决定
- 当用户选择**GDScript**时：准确复制附录A1中的GDScript AGENTS.md模板。切勿将“C++ via GDExtension”添加到语言字段。 GDScript 项目可能使用 GDExtension，但它不是主要项目语言。路由表中的 `godot-gdextension-specialist` 可在需要本机扩展时使用 - 它不会使 C++ 成为项目语言。

---

## 附录 A — Godot 语言配置

用于语言相关配置的所有 Godot 特定变体。参考第 4 节和第 5 节 — 仅当选择 Godot 引擎时才相关。使用与第 4 节中选择的语言相匹配的小节。

---

### A1。 AGENTS.md 技术堆栈模板

**GDScript:**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript
- **Build System**: SCons (engine), Godot Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

> **Guardrail**：使用此 GDScript 模板时，请将语言字段准确写入“`GDScript`” - 无需添加。不要附加“C++ via GDExtension”或任何其他语言。下面的 C# 模板包含 GDExtension，因为 C# 项目通常包装本机代码； GDScript 项目没有。

**C#:**
```markdown
- **Engine**: Godot [version]
- **Language**: C# (.NET 8+, primary), C++ via GDExtension (native plugins only)
- **Build System**: .NET SDK + Godot Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

**两者 — GDScript + C#：**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript (gameplay/UI scripting), C# (performance-critical systems), C++ via GDExtension (native only)
- **Build System**: .NET SDK + Godot Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

---

### A2。命名约定

**GDScript:**
- 类：PascalCase（例如 `PlayerController`）
- Variables/functions：snake_case（例如，`move_speed`）
- 信号：snake_case 过去时（例如，`health_changed`）
- 文件：snake_case 匹配类（例如，`player_controller.gd`）
- 场景：PascalCase 匹配根节点（例如，`PlayerController.tscn`）
- 常量：UPPER_SNAKE_CASE（例如，`MAX_HEALTH`）

**C#:**
- 类：PascalCase (`PlayerController`) — 也必须是 `partial`
- 公共properties/fields：PascalCase（`MoveSpeed`，`JumpVelocity`）
- 私有字段：`_camelCase`（`_currentHealth`、`_isGrounded`）
- 方法：PascalCase（`TakeDamage()`、`GetCurrentHealth()`）
- 信号代表：PascalCase + `EventHandler` 后缀（`HealthChangedEventHandler`）
- 文件：PascalCase 匹配类 (`PlayerController.cs`)
- 场景：PascalCase匹配根节点（`PlayerController.tscn`）
- 常量：PascalCase（`MaxHealth`、`DefaultMoveSpeed`）

**两者 — GDScript + C#：**
对 `.gd` 文件使用 GDScript 约定，对 `.cs` 文件使用 C# 约定。混合语言文件不存在——边界是每个文件。当对新系统应使用哪种语言有疑问时，请询问用户并将决定记录在 `technical-preferences.md` 中。

---

### A3。发动机专家路由

**GDScript:**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **Language/Code Specialist**: godot-gdscript-specialist (all .gd files)
- **Shader Specialist**: godot-shader-specialist (.gdshader files, VisualShader resources)
- **UI Specialist**: godot-specialist (no dedicated UI specialist — primary covers all UI)
- **Additional Specialists**: godot-gdextension-specialist (GDExtension / native C++ bindings only)
- **Routing Notes**: Invoke primary for architecture decisions, ADR validation, and cross-cutting code review. Invoke GDScript specialist for code quality, signal architecture, static typing enforcement, and GDScript idioms. Invoke shader specialist for material design and shader code. Invoke GDExtension specialist only when native extensions are involved.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.gd files) | godot-gdscript-specialist |
| Shader / material files (.gdshader, VisualShader) | godot-shader-specialist |
| UI / screen files (Control nodes, CanvasLayer) | godot-specialist |
| Scene / prefab / level files (.tscn, .tres) | godot-specialist |
| Native extension / plugin files (.gdextension, C++) | godot-gdextension-specialist |
| General architecture review | godot-specialist |
```

**C#:**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **Language/Code Specialist**: godot-csharp-specialist (all .cs files)
- **Shader Specialist**: godot-shader-specialist (.gdshader files, VisualShader resources)
- **UI Specialist**: godot-specialist (no dedicated UI specialist — primary covers all UI)
- **Additional Specialists**: godot-gdextension-specialist (GDExtension / native C++ bindings only)
- **Routing Notes**: Invoke primary for architecture decisions, ADR validation, and cross-cutting code review. Invoke C# specialist for code quality, [Signal] delegate patterns, [Export] attributes, .csproj management, and C#-specific Godot idioms. Invoke shader specialist for material design and shader code. Invoke GDExtension specialist only when native C++ plugins are involved.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.cs files) | godot-csharp-specialist |
| Shader / material files (.gdshader, VisualShader) | godot-shader-specialist |
| UI / screen files (Control nodes, CanvasLayer) | godot-specialist |
| Scene / prefab / level files (.tscn, .tres) | godot-specialist |
| Project config (.csproj, NuGet) | godot-csharp-specialist |
| Native extension / plugin files (.gdextension, C++) | godot-gdextension-specialist |
| General architecture review | godot-specialist |
```

**两者 — GDScript + C#：**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **GDScript Specialist**: godot-gdscript-specialist (.gd files — gameplay/UI scripts)
- **C# Specialist**: godot-csharp-specialist (.cs files — performance-critical systems)
- **Shader Specialist**: godot-shader-specialist (.gdshader files, VisualShader resources)
- **UI Specialist**: godot-specialist (no dedicated UI specialist — primary covers all UI)
- **Additional Specialists**: godot-gdextension-specialist (GDExtension / native C++ bindings only)
- **Routing Notes**: Invoke primary for cross-language architecture decisions and which systems belong in which language. Invoke GDScript specialist for .gd files. Invoke C# specialist for .cs files and .csproj management. Prefer signals over direct cross-language method calls at the boundary.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.gd files) | godot-gdscript-specialist |
| Game code (.cs files) | godot-csharp-specialist |
| Cross-language boundary decisions | godot-specialist |
| Shader / material files (.gdshader, VisualShader) | godot-shader-specialist |
| UI / screen files (Control nodes, CanvasLayer) | godot-specialist |
| Scene / prefab / level files (.tscn, .tres) | godot-specialist |
| Project config (.csproj, NuGet) | godot-csharp-specialist |
| Native extension / plugin files (.gdextension, C++) | godot-gdextension-specialist |
| General architecture review | godot-specialist |
```
