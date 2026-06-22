---
name: localize
description: "完整的本地化管道：扫描硬编码字符串、提取和管理字符串表、验证翻译、生成译者简介、运行 cultural/sensitivity 审查、管理 VO 本地化、测试 RTL/platform 要求、强制字符串冻结和报告覆盖率。"
---

# 本地化流程

本地化不仅仅是翻译——它是制作游戏的完整过程
在每种语言和地区都有母语的感觉。糟糕的本地化会破坏沉浸感，
迷惑玩家，阻碍平台认证。该技能涵盖
从字符串提取到文化审查、VO 录制的完整流程，
RTL 布局测试和本地化 QA 签核。

**Modes:**
- `scan` — 查找硬编码字符串和本地化反模式（只读）
- `extract` — 提取字符串并生成可翻译的表
- `validate` — 检查翻译的完整性、占位符和长度
- `status` — 所有区域设置的覆盖矩阵
- `brief` — 为外部团队生成译者上下文简报文档
- `cultural-review` — 标记文化敏感内容、符号、颜色、习语
- `vo-pipeline` — 管理画外音本地化：脚本、录音规范、集成
- `rtl-check` — 验证 RTL 语言布局、镜像和字体支持
- `freeze` — 强制字符串冻结；在翻译开始之前锁定源字符串
- `qa` — 在发布前运行完整本地化 QA 周期

如果没有提供子命令，则输出用法并停止。结论：**失败** — 缺少必需的子命令。

---

## 阶段 2A：扫描模式

搜索 `src/` 以获取硬编码的面向用户的字符串：

- UI 代码中的字符串文字未包装在本地化函数中（`tr()`、`Tr()`、`NSLocalizedString`、`GetText` 等）
- 应参数化的连接字符串
- 带有位置占位符的字符串（`%s`、`%d`）而不是命名占位符（`{playerName}`）
- 格式化混合区域设置敏感数据（数字、日期、货币）的字符串，而无需区域设置感知格式

搜索本地化反模式：

- Date/time 格式化不使用区域设置感知函数
- 不带区域设置识别的数字格式（`1,000` 与 `1.000`）
- 嵌入图像或纹理中的文本（`assets/` 中的标记资源文件）
- 假定从左到右文本方向的字符串（位置布局、字符串组装顺序）
- Gender/plurality 假设融入字符串逻辑（必须使用复数形式或性别标记）
- 硬编码标点符号（例如 `"You won!"` — 感叹号样式因区域设置而异）

报告所有发现的文件路径和行号。此模式是只读的 - 不写入任何文件。

---

## 阶段 2B：提取模式

- 扫描所有源文件以获取本地化字符串引用
- 与 `assets/data/strings/` 中的现有字符串表进行比较
- 为尚未键入的字符串生成新条目
- 建议遵循约定的键名称：`[category].[subcategory].[description]`
  - 示例：`ui.hud.health_label`、`dialogue.npc.merchant.greeting`、`menu.main.play_button`
- 每个新条目必须包含 `context` 字段 - 译者注释解释：
  - 它出现在哪里（哪个屏幕、哪个场景）
  - 最大字符长度
  - 任何占位符含义（`{playerName}` = 玩家选择的显示名称）
  - Gender/plurality 上下文（如果适用）

输出新字符串的差异以添加到字符串表中。

向用户呈现差异。问：“我可以将这些新条目写入 `assets/data/strings/strings-en.json` 吗？”

如果是，则仅写入差异（新条目），而不是完整替换。结论：**完成** — 提取并写入字符串。

---

## 阶段 2C：验证模式

Read `assets/data/strings/` 中的所有字符串表文件。对于每个区域设置，检查：

- **完整性** — 密钥存在于源代码 (en) 中，但没有针对该语言环境的翻译
- **占位符不匹配** — 源代码有 `{name}`，但翻译忽略了它或添加了额外内容
- **字符串长度违规** — 翻译超出源 `context` 字段中记录的字符限制
- **复数形式计数** — 语言环境需要 N 个复数形式；翻译提供的内容较少
- **孤立密钥** — 翻译存在，但 `src/` 中没有任何内容引用该密钥
- **过时的翻译** — 源字符串在翻译编写后发生了变化（重新翻译的标志）
- **编码** — 存在非 ASCII 字符并且字体图集支持它们（如果不确定则标记）

报告按区域设置和严重性分组的验证结果。此模式是只读的 - 不写入任何文件。

---

## 第 2D 阶段：状态模式

- 计算源表中可本地化字符串的总数
- 每个语言环境：计算已翻译、未翻译、陈旧（翻译后源已更改）
- 生成覆盖矩阵：

```markdown
## Localization Status
Generated: [Date]
String freeze: [Active / Not yet called / Lifted]

| Locale | Total | Translated | Missing | Stale | Coverage |
|--------|-------|-----------|---------|-------|----------|
| en (source) | [N] | [N] | 0 | 0 | 100% |
| [locale] | [N] | [N] | [N] | [N] | [X]% |

### Issues
- [N] hardcoded strings found in source code (run /localize scan)
- [N] strings exceeding character limits
- [N] placeholder mismatches
- [N] orphaned keys
- [N] strings added after freeze was called (freeze violations)
```

此模式是只读的 - 不写入任何文件。

---

## 阶段 2E：简短模式

生成译者上下文简介文档。该文件被发送至
外部翻译团队或本地化供应商以及字符串表导出。

Read:
- `design/gdd/` — 提取游戏类型、基调、设置、角色名称
- `assets/data/strings/strings-en.json` — 源字符串表
- `design/narrative/` 中任何现有的传说或叙述文档

生成`production/localization/translator-brief-[locale]-[date].md`：

```markdown
# Translator Brief — [Game Name] — [Locale]

## Game Overview
[2-3 paragraph summary of the game, genre, tone, and audience]

## Tone and Voice
- **Overall tone**: [e.g., "Darkly comic, not slapstick — think Terry Pratchett, not Looney Tunes"]
- **Player address**: [e.g., "Second person, informal. Never formal 'vous' — always 'tu' for French"]
- **Profanity policy**: [e.g., "Mild — PG-13 equivalent. Match intensity to source, do not soften or escalate"]
- **Humour**: [e.g., "Wordplay exists — if a pun cannot translate, invent an equivalent local joke; do not translate literally"]

## Character Glossary
| Name | Role | Personality | Notes |
|------|------|-------------|-------|
| [Name] | [Role] | [Personality] | [Do not translate / transliterate as X] |

## World Glossary
| Term | Meaning | Notes |
|------|---------|-------|
| [Term] | [What it means] | [Keep in English / translate as X] |

## Do Not Translate List
The following must appear verbatim in all locales:
- [Game name]
- [UI terms that match in-engine labels]
- [Brand or trademark names]

## Placeholder Reference
| Placeholder | What it represents | Example |
|-------------|-------------------|---------|
| `{playerName}` | Player's chosen display name | "Shadowblade" |
| `{count}` | Integer quantity | "3" |

## Character Limits
Tight UI fields with hard limits are marked in the string table `context` field.
Where no limit is stated, target ±30% of the English length as a guideline.

## Contact
Direct questions to: [placeholder for user/team contact]
Delivery format: JSON, same schema as strings-en.json
```

问：“我可以将此翻译摘要写给 `production/localization/translator-brief-[locale]-[date].md` 吗？”

---

## 阶段2F：文化回顾模式

通过 Task 生成 `localization-lead`。要求他们审核目标区域设置中的以下文化敏感性（阅读自 `assets/data/strings/` 和 `assets/`）：

### 要审查的内容领域

**符号和手势**
- 竖起大拇指、OK 手势、和平手势 — 含义因地区而异
- 艺术中的宗教或精神符号，UI，或音频
- 国旗、地图表示、有争议的领土

**Colours**
- 白色（某些亚洲文化中的哀悼）、绿色（某些地区的政治协会）、红色（幸运与危险）
- Alert/warning 与文化关联相冲突的颜色

**Numbers**
- 4（Japanese/Chinese 中的死亡）、13、666 — UI 中的标志使用（房间号、物品数量、价格）

**幽默和习语**
- 在其他语言环境中翻译为攻击性的习语
- Toilet/bodily 幽默在某些市场（特别是日本、德国、中东）不合适
- 围绕特定地区文化敏感话题的黑色幽默

**暴力和内容分级**
- 需要在 DE（德国）、AU（澳大利亚）、CN（中国）或 AE（阿联酋）进行分级更改的内容
- 血色、血腥程度、药物参考——如果需要，标记所有区域特定资产变体

**名称和代表**
- 在目标区域设置中具有攻击性、亵渎性或带有负面含义的角色名称
- 对民族、宗教或族裔群体的刻板印象

以表格形式呈现调查结果：

| Finding | 受影响的区域设置 | Severity | 建议采取的行动 |
|---------|--------------------|----------|--------------------|
| [Description] | [Locale] | [BLOCKING / ADVISORY / NOTE] | [Change / Flag for review / Accept] |

BLOCKING = 必须在发布该语言环境之前修复。 ADVISORY = 建议更改。注意 = 仅供参考。

问：“我可以把这份文化评论报告写到`production/localization/cultural-review-[date].md`吗？”

---

## 阶段2G：VO管道模式

管理画外音本地化流程。根据参数确定子任务：

- `vo-pipeline scan` — 识别所有需要 VO 录制的对话台词
- `vo-pipeline script` — 生成带有导演注释的录音脚本
- `vo-pipeline validate` — 检查所有录制的 VO 文件是否存在且命名正确
- `vo-pipeline integrate` — 验证 code/assets 中是否正确引用了 VO 文件

### VO 管道：扫描

Read `assets/data/strings/` 和 `design/narrative/`。识别：
- 所有对话行（与 `dialogue.*` 匹配的按键）均带有源文本
- 已录制的行（音频文件存在于 `assets/audio/vo/` 中）
- 尚未记录的线路

输出录音清单：

```
## VO Recording Manifest — [Date]

| Key | Character | Source Line | Status |
|-----|-----------|-------------|--------|
| dialogue.npc.merchant.greeting | Merchant | "Welcome, traveller." | Recorded |
| dialogue.npc.merchant.haggle | Merchant | "That's my final offer." | Needs recording |
```

### VO 管道：脚本

为每个角色生成一个录音脚本文档，按场景分组。包括：

- 角色名称和简短的性格注释
- 完整的对话内容以及不常见专有名词的发音指南
- Emotion/direction 每行注释（`[Warm, welcoming]`、`[Annoyed, clipped]`）
- 对话中的任何回应台词（提供上下文：“玩家刚刚说了 X”）

问：“我可以将VO录音脚本写入`production/localization/vo-scripts-[locale]-[date].md`吗？”

### VO 管道：验证

Glob `assets/audio/vo/[locale]/` 适用于所有 `.wav`/`.ogg` 文件。与 VO 清单的交叉引用。报告：
- 丢失文件（脚本中的行，无音频文件）
- 额外文件（音频文件存在，没有匹配的字符串键）
- 违反命名约定

### VO 管道：集成

Grep `src/` 用于 VO 音频参考。验证 `assets/audio/vo/[locale]/` 中是否存在每个引用的路径。报告损坏的参考文献。

---

## 阶段 2H：RTL 检查模式

从右到左的语言（阿拉伯语、希伯来语、波斯语、乌尔都语）要求布局镜像超出
只是翻译文本。该模式验证了实现。

Read `.codex/docs/technical-preferences.md` 确定引擎。然后检查：

**布局镜像**
- 引擎中是否启用了 RTL 布局？ （Godot：`Control.layout_direction`、Unity：`RTL Support` 封装、Unreal：文本方向标志）
- 所有 UI 容器是否都设置为自动镜像，或者位置是否已硬编码？
- 进度条、生命值条和方向指示器是否正确镜像？

**文本渲染**
- 是否加载了支持 Arabic/Hebrew 字符集的字体？
- 阿拉伯文本是否使用正确的连字（连接脚本）呈现？
- 需要时数字是否显示为东方阿拉伯数字？

**弦乐组装**
- 是否存在假定从左到右阅读顺序的字符串连接？
- 当句子结构颠倒时，`{placeholder}` 在句子中的位置是否正确工作？

**资产审查**
- 是否有带有方向箭头或不对称设计的 UI 图标需要镜像变体？
- 是否存在需要 RTL 版本的图像文本资源？

Grep 要检查的模式：
- scene/prefab 文件中特定于引擎的 RTL 标志
- 任何 `HBoxContainer`、`LinearLayout`、`HorizontalBox` 节点 — 验证布局方向设置
- 与 `+` 附近对话或 UI 代码的字符串连接

报告调查结果。标记阻塞问题（内容不经修复就无法读取）与 ADVISORY（外观改进）。

问：“我可以将此 RTL 检查报告写给 `production/localization/rtl-check-[date].md` 吗？”

---

## 第 2I 阶段：冻结模式

字符串冻结锁定源（英语）字符串表，以便翻译可以继续进行
翻译者不会改变来源。

### 冻结通话

检查 `production/localization/freeze-status.md` 中当前的冻结状态（如果存在）。

如果已经冻结：
> “字符串冻结当前处于活动状态（称为 [date]）。自冻结以来已添加或修改了 [N] 字符串。这些都是冻结违规 - 它们需要重新翻译或批准的冻结解除。”

如果未冻结，请出示预冻结清单：

```
Pre-Freeze Checklist
[ ] All planned UI screens are implemented
[ ] All dialogue lines are final (no further narrative revisions planned)
[ ] All system strings (error messages, tutorial text) are complete
[ ] /localize scan shows zero hardcoded strings
[ ] /localize validate shows no placeholder mismatches in source (en)
[ ] Marketing strings (store description, achievements) are final
```

使用 `AskUserQuestion`：
- 提示：“以上各项都确认了吗？调用string freeze会锁定源表。”
- 选项：`[A] Yes — call string freeze now` / `[B] No — I still have strings to add`

如果 [A]: Write `production/localization/freeze-status.md`:

```markdown
# String Freeze Status

**Status**: ACTIVE
**Called**: [date]
**Called by**: [user]
**Total strings at freeze**: [N]

## Post-Freeze Changes
[Any strings added or modified after freeze are listed here automatically by /localize extract]
```

### 冻结电梯

如果参数包含 `lift`：将 `freeze-status.md` 状态更新为 `LIFTED`，记录原因和日期。警告：“解除冻结需要重新翻译所有修改过的字符串。请通知翻译团队。”

### 冻结检查（自动集成到提取物中）

当 `extract` 模式找到新的或修改的字符串并且 `freeze-status.md` 显示 Status: ACTIVE — 将新密钥附加到 `## Post-Freeze Changes` 并发出警告：
> “⚠️ 字符串冻结已激活。[N] new/modified 字符串已添加。这些都是冻结违规。请在继续之前通知您的本地化供应商。”

---

## 阶段 2J：QA 模式

本地化 QA 是在翻译交付后运行的专用通道，但
在任何语言环境发布之前。这与 `/validate`（检查完整性）不同
——这是一个基于结构化游戏的质量检查。

通过 Task 生成 `localization-lead`：
- QA 的目标区域设置
- 游戏中所有screens/flows的列表（从`design/gdd/`或`/content-audit`输出）
- 当前 `/localize validate` 报告
- 文化审查报告（如果有）

要求本地化主管制作一份 QA 计划，内容包括：

1. **功能性字符串检查** — 每个字符串都在游戏中显示，没有截断、占位符错误或编码损坏
2. **UI 溢出检查** — 翻译后的字符串超出 UI 范围（即使在字符限制内，某些语言也会扩展）
3. **上下文准确性** — 游戏中检查 10% 字符串的样本，以确保翻译准确性和自然措辞
4. **文化审查项目** — 验证文化审查中的所有阻止项目均已解决
5. ** VO 同步检查** — 如果 VO 存在，请验证翻译后口型同步或字幕时序是否可接受
6. **平台证书要求** — 检查特定于平台的本地化要求（年龄评级文本、法律声明、ESRB/PEGI/CERO 文本）

根据语言环境输出 QA 判决：

```
## Localization QA Verdict — [Locale]

**Status**: PASS / PASS WITH CONDITIONS / FAIL
**Reviewed by**: localization-lead
**Date**: [date]

### Findings
| ID | Area | Description | Severity | Status |
|----|------|-------------|----------|--------|
| LOC-001 | UI Overflow | "Settings" button text overflows on [Screen] | BLOCKING | Open |
| LOC-002 | Translation | [Key] translation is literal — sounds unnatural | ADVISORY | Open |

### Conditions (if PASS WITH CONDITIONS)
- [Condition 1 — must resolve before ship]

### Sign-Off
[ ] All BLOCKING findings resolved
[ ] Producer approves shipping [Locale]
```

问：“我可以将这份本地化 QA 报告写给 `production/localization/loc-qa-[locale]-[date].md` 吗？”

**门集成**：波兰 → 发布门需要对每个要运送的区域设置通过或通过条件判定。 FAIL 仅阻止该区域设置的释放 - 如果 QA 通过，其他区域设置仍可能继续进行。

---

## 第三阶段：规则和后续步骤

### Rules
- 英语 (en) 始终是源语言环境
- 每个字符串表条目必须包含一个 `context` 字段，其中包含译者注释、字符限制和占位符含义
- 切勿直接修改翻译文件 - 生成差异以供审核
- 必须为每个 UI 元素定义字符限制并在验证模式下强制执行
- 在将字符串发送给翻译器之前必须调用字符串冻结 - 切勿翻译移动目标
- RTL 支持必须从一开始就设计好 — 改造 RTL 布局的成本很高
- 任何商业销售游戏的地区都需要进行文化审查
- 旁白脚本必须包含导演注释——原始对话台词产生平淡的录音

### 推荐工作流程

```
/localize scan            → find hardcoded strings
/localize extract         → build string table
/localize freeze          → lock source before sending to translators
/localize brief           → generate translator briefing document
[Send to translators]
/localize validate        → check returned translations
/localize cultural-review → flag culturally sensitive content
/localize rtl-check       → if shipping Arabic / Hebrew / Persian
/localize vo-pipeline     → if shipping dubbed VO
/localize qa              → full localization QA pass
```

`qa` 返回所有发货区域设置的 PASS 后，在运行 `/gate-check release` 时包括 QA 报告路径。
