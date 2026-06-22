---
name: asset-spec
description: "从 GDD、关卡文档或角色配置文件生成每个资产的视觉规范和 AI 生成提示。生成结构化规格文件并更新主资产清单。在艺术圣经和 GDD/level 设计获得批准后运行，然后开始生产。"
---

如果不提供参数，请检查 `design/assets/asset-manifest.md` 是否存在：
- 如果存在：读取它，找到任何资产处于“需要”状态但尚未写入规范文件的第一个上下文 (system/level/character)，然后使用 `AskUserQuestion`：
  - 提示：“下一个未指定的上下文是 **[target]**。为其生成资产规范吗？”
  - 选项：`[A] Yes — spec [target]` / `[B] Pick a different target` / `[C] Stop here`
- 如果没有清单：失败并显示：
  > “用法：`/asset-spec system:<name>` — 例如，`/asset-spec system:tower-defense`
  > 或：`/asset-spec level:iron-gate-fortress` / `/asset-spec character:frost-warden`
  > 追求你的艺术圣经和 GDD 获得批准。”

---

## 第 0 阶段：解析参数

Extract:
- **目标类型**：`system`、`level` 或 `character`
- **目标名称**：冒号后的名称（标准化为短横线大小写）
- **查看模式**：`--review [完整|lean|独奏]`如果存在

**模式行为：**
- `full`（默认）：并行生成 `art-director` 和 `technical-artist`
- `lean`：仅生成 `art-director` — 更快，跳过技术约束传递
- `solo`：没有代理生成 - 主会话仅根据艺术圣经规则编写规范。用于简单的资产类别或当速度比深度更重要时。

---

## 第一阶段：收集背景信息

Read **在**向用户询问任何内容之前的所有源材料。

### 必读内容：
- **艺术圣经**：Read `design/art/art-bible.md` — 如果丢失则失败：
  > “未找到艺术圣经。首先运行 `/art-bible` - 资产规格以艺术圣经的视觉规则和资产标准为基础。”
  摘录：视觉识别声明、颜色系统（语义颜色）、形状语言、资产标准（第 8 节 — 尺寸、格式、多计数预算、纹理分辨率层）。

- **技术偏好**：Read `.codex/docs/technical-preferences.md` — 提取性能预算和命名约定。

### 源文档读取（按目标类型）：
- **系统**：Read `design/gdd/[target-name].md`。提取 **Visual/Audio 要求** 部分。如果它不存在或读取为 `[To be designed]`：
  > “`design/gdd/[target-name].md` 的 Visual/Audio 部分是空的。要么运行 `/design-system [target-name]` 来完成 GDD，要么手动描述视觉需求。”
  使用`AskUserQuestion`：`[A] Describe needs manually` / `[B] Stop — complete the GDD first`
- **级别**：Read `design/levels/[target-name].md`。从步骤 4 中提取美术要求、资产列表、VFX 需求以及美术总监的制作概念规格。
- **字符**：Read `design/narrative/characters/[target-name].md` 或搜索 `design/narrative/` 以获取字符配置文件。提取视觉描述、角色和任何指定的区别特征。

### 可选读物：
- **现有清单**：Read `design/assets/asset-manifest.md`（如果存在）- 提取此目标已指定的资产以避免重复。
- **相关规范**：Glob `design/assets/specs/*.md` — 扫描可共享的资产（例如，为一个系统指定的通用 UI 元素也可能适用于此处）。

### 当前上下文摘要：
> **资产规格：[Target Type] — [Target Name]**
> - 源文档：[path] — [N] 已识别的资产类型
> - 艺术圣经：找到——资产标准第 8 节
> - 该目标的现有规格：[N already specced / none]
> - 在其他规范中找到的共享资产：[列表或“无”]

---

## 第二阶段：资产识别

从源文档中提取提到的每种资产类型 - 明确的和隐含的。

**对于系统**：查找 VFX 事件、精灵引用、UI 元素、音频触发器、粒子效果、图标需求以及任何“视觉反馈”语言。

**对于关卡**：寻找独特的环境道具、大气 VFX、照明设置、环境音频、skybox/background 以及任何特定于区域的材料。

**对于角色**：寻找精灵表（空闲、行走、攻击、死亡）、附加到能力的 portrait/avatar、VFX、UI 表示（图标、生命条皮肤）。

将资产分为几类：
- **精灵/2D 艺术** — 角色精灵、UI 图标、图块表
- **VFX / 粒子** — 命中效果、环境粒子、屏幕效果
- **环境** — 道具、图块、背景、天空盒
- **UI** — HUD 元素、菜单艺术、字体（如果自定义）
- **音频** — SFX、音乐曲目、环境循环 *（注意：音频规格仅是描述 — 无生成提示）*
- **3D 资源** — 网格、材质（如果每个引擎适用）

向用户呈现完整的识别列表。使用 `AskUserQuestion`：
- 提示：“我在 [N] 类别中为 **[target]** 识别了 [N] 资产。指定前先检查：”
- 首先在对话文本中显示分组列表
- 选项：`[A] Proceed — spec all of these` / `[B] Remove some assets` / `[C] Add assets I didn't catch` / `[D] Adjust categories`

在用户未确认资产列表的情况下，请勿继续进入第 3 阶段。

---

## 第 3 阶段：规格生成

基于审查模式产生专业代理。 **同时发出所有 Task 调用 - 不要等待一个调用才开始下一个调用。**

### 完整模式——并行生成：

**`art-director`** 通过 Task：
- 提供：第二阶段的完整资产列表、艺术圣经视觉识别声明、色彩系统、形状语言、源文档的视觉要求以及艺术圣经第 9 节中提到的任何参考 games/art
- 要求：“对于此列表中的每个资产，生成：(1) 一个基于艺术圣经的形状语言和颜色系统的 2-3 句话视觉描述 - 足够具体，以便两个不同的艺术家能够产生一致的结果；(2) 准备与 AI 图像工具一起使用的生成提示（Midjourney/Stable 扩散风格 - 包括风格关键字、构图、调色板锚点、负面提示）；(3) 哪些艺术圣经规则直接管理该资产（按部分引用）。音频资产，描述声音特征而不是生成提示。”

**`technical-artist`** 通过 Task：
- 提供：完整资产清单、艺术圣经资产标准（第8节）、technical-preferences.md性能预算、引擎名称和版本
- 询问：“对于此列表中的每个资源，请指定：(1) 精确尺寸或多边形计数（匹配艺术圣经资源标准层 - 不要发明新尺寸）；(2) 文件格式和导出设置；(3) 命名约定（来自 technical-preferences.md）；(4) 该资源类型必须遵守的任何特定于引擎的约束；(5) LOD 要求（如果适用）。标记艺术圣经首选标准与引擎约束冲突的任何资源类型。”

### 精益模式——仅产生艺术总监（跳过技术艺术家）。

### 单人模式——跳过两者。仅从艺术圣经规则中得出规格，并注意技术限制未经验证。

**在第 4 阶段之前收集这两个响应。** 如果艺术总监和技术艺术家之间存在任何冲突（例如，艺术总监指定 4K 纹理，但技术艺术家标记引擎预算需要 512 像素），请明确提出 - 不要默默解决。

---

## 第四阶段：编译和审查

将代理输出合并到每个资产的草案规范中。使用以下格式在对话文本中呈现所有规格：

```
## ASSET-[NNN] — [Asset Name]

| Field | Value |
|-------|-------|
| Category | [Sprite / VFX / Environment / UI / Audio / 3D] |
| Dimensions | [e.g. 256×256px, 4-frame sprite sheet] |
| Format | [PNG / SVG / WAV / etc.] |
| Naming | [e.g. vfx_frost_hit_01.png] |
| Polycount | [if 3D — e.g. <800 tris] |
| Texture Res | [e.g. 512px — matches Art Bible §8 Tier 2] |

**Visual Description:**
[2–3 sentences. Specific enough for two artists to produce consistent results.]

**Art Bible Anchors:**
- §3 Shape Language: [relevant rule applied]
- §4 Color System: [color role — e.g. "uses Threat Blue per semantic color rules"]

**Generation Prompt:**
[Ready-to-use prompt. Include: style keywords, composition notes, color palette anchors, lighting direction, negative prompts.]

**Status:** Needed
```

提供所有规格后，使用 `AskUserQuestion`：
- 提示：“**[target]** — [N] 资产的资产规格。审核完成吗？”
- 选项：`[A] Approve all — write to file` / `[B] Revise a specific asset` / `[C] Regenerate with different direction`

如果 [B]：询问要更改哪些资产以及哪些内容。内联修改并重新呈现。不要为较小的文本修改而重新生成代理 - 仅当视觉方向本身需要更改时才重新生成。

如[C]：询问向什么方向改变。使用更新后的简介重新生成相关代理。

---

## 第 5 阶段：Write 规格文件

批准后，询问：“我可以将规范写入`design/assets/specs/[target-name]-assets.md`吗？”

Write 文件包含：

```markdown
# Asset Specs — [Target Type]: [Target Name]

> **Source**: [path to source GDD/level/character doc]
> **Art Bible**: design/art/art-bible.md
> **Generated**: [date]
> **Status**: [N] assets specced / [N] approved / [N] in production / [N] done

[all asset specs in ASSET-NNN format]
```

然后更新`design/assets/asset-manifest.md`。如果不存在，则创建它：

```markdown
# Asset Manifest

> Last updated: [date]

## Progress Summary

| Total | Needed | In Progress | Done | Approved |
|-------|--------|-------------|------|----------|
| [N] | [N] | [N] | [N] | [N] |

## Assets by Context

### [Target Type]: [Target Name]
| Asset ID | Name | Category | Status | Spec File |
|----------|------|----------|--------|-----------|
| ASSET-001 | [name] | [category] | Needed | design/assets/specs/[target]-assets.md |
```

如果清单已存在，请附加新的上下文块并更新进度摘要计数。

问：“我可以更新 `design/assets/asset-manifest.md` 吗？”

---

## 第六阶段：关闭

使用 `AskUserQuestion`：
- 提示：“**[target]** 的资产规格已完成。下一步是什么？”
- Options:
  - `[A] Spec another system — /asset-spec system:[next-system]`
  - `[B] Spec a level — /asset-spec level:[level-name]`
  - `[C] Spec a character — /asset-spec character:[character-name]`
  - `[D] Run /asset-audit — validate delivered assets against specs`
  - `[E] Stop here`

---

## 资产 ID 分配

资产 ID 在整个项目中按顺序分配，而不是按上下文分配。 Read 分配 ID 之前的清单以查找当前最高编号：

```
Grep pattern="ASSET-" path="design/assets/asset-manifest.md"
```

从 `ASSET-[highest + 1]` 开始新资产。这确保了 ID 在整个项目中稳定且唯一。

如果尚不存在清单，则从 `ASSET-001` 开始。

---

## 共享资产协议

在指定资产之前，请检查另一个上下文的规范中是否已存在等效项：

- 常见的 UI 元素（生命条、分数显示）通常在系统之间共享
- 通用环境道具可能会出现在多个级别
- 角色 VFX（击中火花、死亡效果）可以重复使用带有颜色变体的基本规格

如果找到匹配项：引用现有资产 ID，而不是创建重复项。请注意清单的引用者列中的共享用法。

> “ASSET-012（通用 Hit Spark）已指定用于战斗系统。重用于塔防 - 将塔防添加到引用者中。”

---

## 错误恢复协议

如果任何生成的代理返回 BLOCKED 或无法完成：

1. 立即浮出水面：“[AgentName]：被阻止 — [reason]”
2. 在 `lean` 模式下或如果 `technical-artist` 阻止：仅继续进行艺术总监输出 - 请注意，技术约束未经过验证
3. 在 `solo` 模式下或如果 `art-director` 阻止：从艺术圣经规则中导出描述 - 标记为“未咨询艺术总监 - 在制作前根据艺术圣经进行验证”
4. 始终生成部分规范——永远不要因为一个代理被阻止而放弃工作

---

## 协作协议

每个阶段如下：**识别→确认→生成→审核→批准→Write**

- 在未先与用户确认资产列表的情况下，切勿指定资产
- 始终将规格与艺术圣经挂钩——与艺术圣经相矛盾的规格是错误的
- 公开所有代理人的分歧——不要默默地选择一个
- Write 仅在明确批准后的规范文件
- 编写规范后立即更新清单

---

## 建议的后续步骤

- 运行 `/asset-spec [next-context]` 以继续指定剩余的系统、级别或字符
- 运行 `/asset-audit` 以根据书面规格验证交付的资产并识别差距或不匹配
