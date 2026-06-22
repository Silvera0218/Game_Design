---
name: dev-story
description: "Read 一个故事文件并实现它。加载完整的上下文（故事、GDD 要求、ADR 指南、控制清单），路由到系统和引擎的正确程序员代理，实现代码和测试，并确认每个验收标准。核心实现技巧——在/story-readiness之后、/code-review和/story-done.之前运行"
---

# 开发故事

这项技能连接了规划和代码。它完整读取故事文件，组装
程序员需要的所有上下文，路由到正确的专家代理，以及
推动实施完成——包括编写测试。

**每个故事的循环：**
```
/qa-plan sprint           ← define test requirements before sprint begins
/story-readiness [path]   ← validate before starting
/dev-story [path]         ← implement it  (this skill)
/code-review [files]      ← review it
/story-done [path]        ← verify and close it
```

**所有冲刺故事完成后：** 运行 `/team-qa sprint` 来执行完整的 QA 周期，并在推进项目阶段之前获得签核判决。

**输出：**项目`src/`和`tests/`目录中的源代码+测试文件。

---

## 第一阶段：寻找故事

**如果提供了路径**：直接读取该文件。

**如果没有参数**：检查 `production/session-state/active.md` 是否处于活动状态
故事。如果找到，请确认：“[story title] 上的持续工作 - 这是正确的吗？”
如果没有找到，问：“我们正在实施哪个故事？” Glob
`production/epics/**/*.md` 并列出状态为“就绪”的故事。

---

## 第 2 阶段：加载完整上下文

**在加载任何上下文之前，验证所需的文件是否存在。** 从故事的 `ADR Governing Implementation` 字段中提取 ADR 路径，然后检查：

| File | Path | If missing |
|------|------|------------|
| TR registry | `docs/architecture/tr-registry.yaml` | **STOP** —“未找到 TR 注册表。运行 `/create-epics` 来生成它。” |
| 治理 ADR | 来自故事 ADR 字段的路径 | **停止** —“未找到 ADR 文件 [path]。运行 `/architecture-decision` 来创建它，或者更正故事的 ADR 字段中的文件名。” |
| 控制清单 | `docs/architecture/control-manifest.md` | **警告并继续** — “未找到控制清单 — 无法检查层规则。运行 `/create-control-manifest`。” |

如果 TR 注册表或管理 ADR 丢失，请在会话状态中将故事状态设置为 **BLOCKED** 并且不生成任何程序员代理。

Read 以下所有内容同时进行 - 这些是独立读取。在加载所有上下文之前不要开始实施：

### 故事档案
提取并保留：
- **故事标题、ID、图层、类型**（逻辑/集成/Visual/Feel / UI / Config/Data）
- **TR-ID** — GDD 要求标识符
- **管理 ADR** 参考
- **清单版本**嵌入故事标题中
- **验收标准** — 每个复选框项目逐字记录
- **实施说明** — 故事中的 ADR 指导部分
- **超出范围**边界
- **测试证据** — 所需的测试文件路径
- **依赖关系** — 在这个故事之前必须完成什么

### TR 注册表
Read `docs/architecture/tr-registry.yaml`。查找故事的 TR-ID。
Read 当前的 `requirement` 文本 — 这是事实的来源
GDD 现在需要。不要依赖故事文件中的任何内嵌文本（可能已过时）。

### 主控ADR
Read `docs/architecture/[adr-file].md`。摘录：
- 完整的决策部分
- 实施指南部分（这是程序员遵循的）
- 引擎兼容性部分（截止后 API、已知风险）
- ADR 依赖项部分

### 控制清单
Read `docs/architecture/control-manifest.md`。提取该故事层的规则：
- 所需图案
- 禁止的图案
- 性能护栏

检查：故事的嵌入清单版本是否与当前清单标题日期匹配？
如果它们不同，请在继续之前使用 `AskUserQuestion`：
- 提示：“故事是针对清单 v[story-date] 编写的。当前清单是 v[current-date]。可能适用新规则。您要如何继续？”
- Options:
  - `[A] Update story manifest version and implement with current rules (Recommended)`
  - `[B] Implement with old rules — I accept the risk of non-compliance`
  - `[C] Stop here — I want to review the manifest diff first`

如果是 [A]：在生成程序员之前将故事文件的 `Manifest Version:` 字段编辑为当前清单日期。然后仔细阅读清单以了解新规则。
如果 [B]：无论如何都要仔细阅读清单以了解新规则，并注意“偏差”下第 6 阶段摘要中的版本不匹配。
如果[C]：停止。不要生成任何代理。让用户检查并重新运行 `/dev-story`。

### 依赖性验证

从故事文件中提取 **依赖项** 列表后，验证每个：

1. Glob `production/epics/**/*.md` 查找每个依赖故事文件。
2. Read 及其 `Status:` 字段。
3. 如果任何依赖项的状态不是 `Complete` 或 `Done`：
   - 使用 `AskUserQuestion`：
     - 提示：“故事‘[current story]’依赖于‘[dependency title]’，当前为 [status]，未完成。您要如何继续？”
     - Options:
       - `[A] Proceed anyway — I accept the dependency risk`
       - `[B] Stop — I'll complete the dependency first`
       - `[C] The dependency is done but status wasn't updated — mark it Complete and continue`
   - 如果 [B]：在会话状态中将故事状态设置为 **BLOCKED** 并停止。不要产生任何程序员代理。
   - 如果 [C]：询问“我可以将 [dependency path] 状态更新为完成吗？”在继续之前。
   - 如果 [A]：在“偏差”下的第 6 阶段摘要中注释：“以不完全依赖性实现：[dependency title] — [status]。”

如果找不到依赖项文件：警告“未找到依赖项故事：[path]。验证路径或创建故事文件。”

---

### 发动机参考
Read `.codex/docs/technical-preferences.md`：
- `Engine:` 值 — 确定要使用的程序员代理
- 命名约定（类名、文件名、signal/event 名称）
- 性能预算（帧预算、内存上限）
- 禁止的图案

---

## 第三阶段：找到合适的程序员

根据故事的**层**、**类型**和**系统名称**，确定哪个
专家通过 Task 生成。

**Config/Data 故事 — 完全跳过代理生成：**
如果故事的类型是 `Config/Data`，则不需要程序员代理或引擎专家。直接跳转到第 4 阶段（Config/Data 注）。实施是数据文件编辑——没有路由表评估，没有引擎专家。

### 主代理路由表

| 故事背景 | 主代理 |
|---|---|
| 基础层——任何类型 | `engine-programmer` |
| 任意层 — 类型：UI | `ui-programmer` |
| 任意层 — 类型：Visual/Feel | `gameplay-programmer`（实现） |
| 核心或功能——游戏机制 | `gameplay-programmer` |
| 核心或特征——人工智能行为、寻路 | `ai-programmer` |
| 核心或功能——网络、复制 | `network-programmer` |
| Config/Data — 无代码 | 无需代理（请参阅第 4 阶段配置说明） |

### 代理生成要求

对于任何命中主代理路由表的代码故事，必须真实生成对应的程序员子代理执行实现，而不是仅在编排器内部“逻辑归属”该代理。

- 如果路由结果是 `gameplay-programmer`，必须显式生成 `gameplay-programmer` 子代理，并把完整上下文包交给它。
- 如果路由结果是 `engine-programmer`、`ui-programmer`、`ai-programmer` 或 `network-programmer`，同样必须显式生成对应子代理。
- 如果当前运行环境不支持生成所需子代理，或子代理工具不可用，停止实施并向用户报告：“需要生成 [agent-name] 子代理，但当前环境不可用。是否允许主编排器代替实现？”
- 未获得用户明确许可前，编排器不得静默代替程序员子代理修改源代码或测试文件。
- `Config/Data` 故事例外：它们不生成程序员代理，按本技能的 Config/Data 流程直接处理。

### 引擎专家 - 始终作为代码故事的辅助生成

Read `.codex/docs/technical-preferences.md` 的 `Engine Specialists` 部分
获取配置的主要专家。将它们与主要特工一起生成
当故事涉及特定于引擎的 API、模式或 ADR 具有高电平时
发动机风险。

| Engine | 提供专业代理 |
|--------|----------------------------|
| Godot 4 | `godot-specialist`、`godot-gdscript-specialist`、`godot-shader-specialist` |
| Unity | `unity-specialist`、`unity-ui-specialist`、`unity-shader-specialist` |
| Unreal 发动机 | `unreal-specialist`、`ue-gas-specialist`、`ue-blueprint-specialist`、`ue-umg-specialist`、`ue-replication-specialist` |

**当引擎风险较高时**（来自 ADR 或 VERSION.md）：始终生成引擎
专家，即使是非面向引擎的故事。高风险意味着ADR记录
关于需要专家验证的切断后引擎 API 的假设。

---

## 第四阶段：实施

通过 Task 或当前环境等价的子代理生成工具，使用完整的上下文包生成所选的程序员代理。生成动作必须是可观察的：执行日志、工具调用或中间输出中应能看出具体启动了哪个代理。

向代理人提供：
1. 完整的故事文件内容
2. 当前的 GDD 要求文本（来自 TR 注册表）
3. ADR 决策 + 实施指南（逐字记录 — 不总结）
4. 该层的控制清单规则
5. 引擎命名约定和性能预算
6. ADR 引擎兼容性部分中的任何特定于引擎的注释
7. 必须创建的测试文件路径
8. 明确的指示：**实现这个故事并编写测试**

代理人应该：
- 按照 ADR 准则在 `src/` 中创建或修改文件
- 尊重控制清单中的所有必需和禁止的模式
- 保持在故事范围之外的范围内（不要触及不相关的文件）
- Write 干净、带文档注释的公共 API

### Config/Data 故事（无需代理）

对于类型：Config/Data 故事，不需要程序员代理。实施情况
正在编辑数据文件。 Read 故事的验收标准并做出指定
直接修改数据文件。请注意哪些值已更改以及它们的含义
更改 from/to.

### Visual/Feel 故事

生成 `gameplay-programmer` 以实现 code/animation 调用。请注意
Visual/Feel 验收标准无法自动验证 - “感觉合适吗？”
通过手动确认，检查发生在 `/story-done` 中。

---

## 第 5 阶段：Write 测试

对于**逻辑**和**集成**故事，测试必须作为
这个实施——不推迟到以后。

提醒程序员代理：

> “需要此故事的测试文件：`[path from Test Evidence section]`。
> 如果没有它，故事就无法通过 `/story-done` 关闭。 Write 测试
> 与实施同时进行，而不是在实施之后。”

测试要求（来自coding-standards.md）：
- 文件名: `[system]_[feature]_test.[ext]`
- 函数名称：`test_[scenario]_[expected_outcome]`
- 每个验收标准必须至少有一个测试函数覆盖它
- 无随机种子、无时间相关断言、无外部 I/O
- 从 GDD 公式部分测试公式范围

对于 **Visual/Feel** 和 **UI** 故事：无自动化测试。提醒代理人
在实施摘要中注明需要哪些手动证据：
“`production/qa/evidence/[slug]-evidence.md` 需要证据文档。”

对于 **Config/Data** 故事：没有测试文件。烟雾检查将作为证据。

---

## 第六阶段：收集和总结

程序员代理完成后，收集：

- 创建或修改的文件（带路径）
- 创建的测试文件（写入的测试函数的路径和数量）
- 任何偏离故事范围边界的偏差（标记这些）
- 代理出现的任何问题或障碍
- 专家标记的任何特定于发动机的风险

给出一个简洁的实施摘要：

```
## Implementation Complete: [Story Title]

**Files changed**:
- `src/[path]` — created / modified ([brief description])
- `tests/[path]` — test file ([N] test functions)

**Acceptance criteria covered**:
- [x] [criterion] — implemented in [file:function]
- [x] [criterion] — covered by test [test_name]
- [ ] [criterion] — DEFERRED: requires playtest (Visual/Feel)

**Deviations from scope**: [None] or [list files touched outside story boundary]
**Engine risks flagged**: [None] or [specialist finding]
**Blockers**: [None] or [describe]

Ready for: `/code-review [file1] [file2]` then `/story-done [story-path]`
```

---

## 第 7 阶段：更新会话状态

默默追加到`production/session-state/active.md`：

```
## Session Extract — /dev-story [date]
- Story: [story-path] — [story title]
- Files changed: [comma-separated list]
- Test written: [path, or "None — Visual/Feel/Config story"]
- Blockers: [None, or description]
- Next: /code-review [files] then /story-done [story-path]
```

如果 `active.md` 不存在，则创建它。确认：“会话状态已更新。”

---

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
- 清单版本不匹配→向用户显示差异，询问是否继续使用旧规则或先更新故事

## 协作协议

- **文件写入被委托** - 所有源代码、测试文件和证据文档均由通过 Task 或当前环境等价子代理工具生成的子代理编写。每个子代理强制执行“我可以写入 [path] 吗？”单独协议。该编排器不直接写入文件。
- **路由必须落地为子代理** - 当故事命中 `gameplay-programmer`、`engine-programmer`、`ui-programmer`、`ai-programmer` 或 `network-programmer` 路由时，必须真实启动对应子代理。仅在总结中声称“按某代理规则实现”不算满足本技能要求。
- **无法生成子代理时停止** - 如果当前环境无法启动路由要求的子代理，先报告阻塞并请求用户决策。除非用户明确同意主编排器代替实现，否则不得继续修改代码或测试。
- **在实现之前加载** - 在加载所有上下文之前不要开始编码
  （故事、TR-ID、ADR、清单、引擎首选项）。不完整的上下文生成代码
  偏离设计。
- **ADR 是法律** — 实施必须遵循 ADR 的实施
  指导方针。如果指南与看起来“更好”的内容相冲突，请在
  总结而不是默默偏离。
- **留在范围内** — 超出范围的部分是一份合同。如果实施
这个故事需要接触一个超出范围的文件，停止并显示它：
  “实现 [criterion] 需要修改 [file]，这超出了范围。
  我应该继续还是创建一个单独的故事？”
- **对于 Logic/Integration，测试不是可选的** — 不标记实现
  在不存在测试文件的情况下完成
- **Visual/Feel 标准被推迟，而不是跳过** - 将它们标记为 DEFERRED
  在摘要中；它们将在 `/story-done` 中手动验证
- **在做出重大结构性决策之前先询问**——如果故事需要
  ADR 未涵盖的架构模式，请在实现之前将其表面化：
  “ADR 没有指定如何处理 [case]。我的计划是 [X]。继续吗？”

---

## 建议的后续步骤

- 在结束故事之前运行 `/code-review [file1] [file2]` 以检查实施情况
- 运行 `/story-done [story-path]` 以验证验收标准并将故事标记为完成
- 所有冲刺故事完成后：在推进项目阶段之前，运行 `/team-qa sprint` 完成整个 QA 周期
