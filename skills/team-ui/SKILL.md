---
name: team-ui
description: "通过完整的 UX 管道协调 UI 团队：从 UX 规范创作到视觉设计、实施、审查和完善。与 /ux-design、/ux-review 和 studio UX 模板集成。"
---
调用此技能时，通过结构化管道协调 UI 团队。

**决策点：** 在每个阶段转换时，使用 `AskUserQuestion` 来呈现
用户将子代理的建议作为可选择的选项。 Write 代理的
在对话中进行全面分析，然后用简洁的标签捕捉决策。
用户必须批准才能进入下一阶段。

## 团队构成
- **ux-designer** — 用户流程、线框、可访问性、输入处理
- **ui-programmer** — UI 框架、屏幕、小部件、数据绑定、实现
- **艺术总监** — 视觉风格、布局精美、与艺术圣经的一致性
- **引擎 UI 专家** — 根据特定于引擎的最佳实践验证 UI 实施模式（阅读 `.codex/docs/technical-preferences.md` 引擎专家 → UI 专家）
- **可访问性专家** - 在第 4 阶段审核可访问性合规性

**此管道使用的模板：**
- `ux-spec.md` — 标准 screen/flow UX 规格
- `hud-design.md` — HUD 特定 UX 规范
- `interaction-pattern-library.md` — 可重用的交互模式
- `accessibility-requirements.md` — 承诺的可访问性级别和要求

## 如何委派

使用 Task 工具将每个团队成员生成为子代理：
- `subagent_type: ux-designer` — 用户流程、线框、可访问性、输入处理
- `subagent_type: ui-programmer` — UI 框架、屏幕、小部件、数据绑定
- `subagent_type: art-director` — 视觉风格、布局优化、艺术圣经一致性
- `subagent_type: [UI engine specialist]` — 引擎特定的 UI 模式验证（例如，unity-ui-specialist、ue-umg-specialist、godot-specialist）
- `subagent_type: accessibility-specialist` — 辅助功能合规性审核

始终在每个代理的提示中提供完整的上下文（功能要求、现有 UI 模式、平台目标）。在管道允许的情况下并行启动独立代理（例如，第 4 阶段审核代理可以同时运行）。

## Pipeline

### 第 1a 阶段：背景收集

在设计任何东西之前，请阅读并综合：
- `design/gdd/game-concept.md` — 平台目标和目标受众
- `design/player-journey.md` — 玩家到达此屏幕时的状态和上下文
- 所有与此功能相关的 GDD UI 要求部分
- `design/ux/interaction-patterns.md` — 要重用的现有模式（而不是重新发明）
- `design/accessibility-requirements.md` — 承诺的可访问性层（例如，基本、增强、完整）

**如果 `design/ux/interaction-patterns.md` 不存在**，立即显示间隙：
> “interaction-patterns.md 不存在 — 没有可重用的现有模式。”

然后使用 `AskUserQuestion` 和选项：
- (a) 先运行`/ux-design patterns`建立花样库，然后继续
- (b) 在没有模式库的情况下继续 - ui-programmer 会将创建的所有模式视为新模式，并在完成时将每个模式添加到新的 `design/ux/interaction-patterns.md`

请勿仅根据功能名称或 GDD 发明或假设模式。如果用户选择 (b)，则在第 3 阶段明确指示 ui-programmer 将所有模式视为新模式，并在实现完成后将它们记录在 `design/ux/interaction-patterns.md` 中。请注意最终摘要报告中的模式库状态（创建/缺失/更新）。

为用户体验设计师总结背景：玩家在做什么、他们需要什么、应用什么约束以及哪些现有模式是相关的。

### 阶段 1b：UX 规范创作

调用 `/ux-design [feature name]` 技能或直接委托给 ux-designer 以按照 `ux-spec.md` 模板生成 `design/ux/[feature-name].md`。

如果设计 HUD，请使用 `hud-design.md` 模板而不是 `ux-spec.md`。

> **特殊情况说明：**
> - 特别是对于 HUD 设计，请使用 `argument: hud` 调用 `/ux-design`（例如，`/ux-design hud`）。
> - 对于交互模式库，在项目启动时运行一次 `/ux-design patterns`，并在后续阶段引入新模式时更新它。

输出：`design/ux/[feature-name].md`，已填充所有必需的规格部分。

### 第 1c 阶段：UX 审查

规范完成后，调用 `/ux-review design/ux/[feature-name].md`。

**关**：在判决获得批准之前不要进入第 2 阶段。如果结论是需要修订，用户体验设计师必须解决标记的问题并重新运行审核。用户可以明确接受需要修改的风险并继续，但这必须是一个有意识的决定——在询问是否继续之前通过 `AskUserQuestion` 提出具体问题。

### 第二阶段：视觉设计

委托给**艺术总监**：
- 查看完整的 UX 规范（流程、线框、交互模式、辅助功能注释）——而不仅仅是线框图像
- 应用艺术圣经中的视觉处理：颜色、排版、间距、动画风格
- 检查视觉设计是否保持可访问性合规性：验证颜色对比度，并确认颜色永远不是状态的唯一指示符（形状、文本或图标必须强化它）
- 指定艺术管道所需的所有资产要求：指定尺寸的图标、背景纹理、字体、装饰元素 - 具有精确的尺寸和格式要求
- 确保与现有实施的 UI 屏幕的一致性
- 输出：带有风格注释和资产清单的视觉设计规范

### 第三阶段：实施

在实施开始之前，生成 **引擎 UI 专家**（来自 `.codex/docs/technical-preferences.md` 引擎专家 → UI 专家）以查看 UX 规范和视觉设计规范，以获取特定于引擎的实施指南：
- 该屏幕应使用哪种引擎 UI 框架？ （例如，UI Toolkit 与 Unity 中的 UGUI、Godot 中的控制节点与 CanvasLayer、UMG 与 Unreal 中的 CommonUI）
- 对于建议的布局或交互模式有任何特定于引擎的问题吗？
- 推荐 widget/node 发动机结构？
- 输出：引擎 UI 实施说明，在开始之前交给 ui 程序员

如果没有配置引擎，请跳过此步骤。

委托给 **ui 程序员**：
- 按照 UX 规范和视觉设计规范实施 UI
- **使用 `design/ux/interaction-patterns.md` 中的模式** — 不要重新发明已指定的模式。如果一个模式几乎适合但需要修改，请记下偏差并将其标记为用户体验设计师审查。
- **UI 从不拥有或修改游戏状态** — 仅显示；为所有玩家操作发出事件
- 所有文本均通过本地化系统 - 没有面向玩家的硬编码字符串
- 支持两种输入法（keyboard/mouse 和游戏手柄）
- 在 `design/accessibility-requirements.md` 中按承诺层实现辅助功能
- 将数据绑定连接到游戏状态
- **如果在实现过程中创建了任何新的交互模式**（即模式库中尚未存在的内容），请在标记实现完成之前将其添加到 `design/ux/interaction-patterns.md`
- 输出：已实现的 UI 功能

### 第 4 阶段：审查（并行）

并行委托：
- **ux-designer**：验证实现是否匹配线框和交互规范。测试仅键盘和仅游戏手柄的导航。检查辅助功能是否正常运行。
- **艺术总监**：验证与艺术圣经的视觉一致性。检查支持的最小和最大分辨率。
- **可访问性专家**：根据 `design/accessibility-requirements.md` 中记录的承诺可访问性层验证合规性。将任何违规行为标记为阻止者。

所有三个审核流程都必须在进入第 5 阶段之前进行报告。

### 第五阶段：抛光

- 处理所有评论反馈
- 验证动画是否可跳过并尊重玩家的运动减少偏好
- 通过音频事件系统确认 UI 声音触发（无直接音频呼叫）
- 在所有支持的分辨率和宽高比下进行测试
- **验证 `design/ux/interaction-patterns.md` 是最新的** — 如果在此功能的实现过程中引入了任何新模式，请确认它们已添加到库中
- **确认所有 HUD 元素均遵循 `design/ux/hud.md` 中定义的视觉预算**（元素计数、屏幕区域分配、最大不透明度值）

## 快速参考 - 何时使用哪种技能

- `/ux-design` — 从头开始为屏幕、流程或 HUD 创建新的 UX 规范
- `/ux-review` — 在实施之前验证完整的 UX 规范
- `/team-ui [feature]` — 从概念到完善的完整流程（内部调用 `/ux-design` 和 `/ux-review`）
- `/quick-design` — UI 的小更改，不需要全新的 UX 规范

## 错误恢复协议

如果任何生成的代理（通过 Task）返回 BLOCKED、错误或无法完成：

1. **立即浮出水面**：在继续依赖阶段之前向用户报告“[AgentName]：BLOCKED — [reason]”
2. **评估依赖关系**：检查后续阶段是否需要被阻止的代理的输出。如果是，则在没有用户输入的情况下不要继续越过该依赖点。
3. **通过 AskUserQuestion 提供选项**，可选择：
   - 跳过此代理并注意最终报告中的差距
   - 以更窄的范围重试
   - 停在这里并首先解决阻止程序
4. **始终生成部分报告** — 输出已完成的内容。切勿因为一名代理阻塞而放弃工作。

常见的拦截器：
- 输入文件丢失（未找到故事，GDD 不存在）→ 重定向到创建它的技能
- ADR 状态为建议 → 不实施；首先运行 `/architecture-decision`
- 范围太大 → 通过 `/create-stories` 分成两个故事
- ADR 和故事之间的指令冲突 → 冲突浮出水面，不要猜测

## 文件 Write 协议

所有文件写入（UX 规范、交互模式库更新、实施文件）
委托给子代理和子技能（`/ux-design`、`ui-programmer`）。每个强制执行
“我可以写信给 [path] 吗？”协议。该编排器不直接写入文件。

## Output

摘要报告涵盖：UX 规范状态、UX 审查结论、视觉设计状态、实施状态、辅助功能合规性、输入法支持、交互模式库更新状态以及任何未解决的问题。

结论：**完成** — UI 功能通过完整管道交付（UX 规范 → 视觉 → 实施 → 审查 → 完善）。
结论：**封锁**——管道停止；在停止之前，先将阻断剂及其相暴露出来。

## 下一步

- 如果尚未获得批准，请在最终规格上运行 `/ux-review`。
- 在结束故事之前，在 UI 实现上运行 `/code-review`。
- 如果需要视觉或音频润色通道，请运行 `/team-polish`。
