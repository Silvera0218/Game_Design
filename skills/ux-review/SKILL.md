---
name: ux-review
description: "验证 UX 规范、HUD 设计或交互模式库的完整性、可访问性合规性、GDD 对齐和实施准备情况。生成具有特定差距的已批准/需要修订/需要重大修订的判决。"
---

## Overview

在 UX 设计文档进入实施流程之前对其进行验证。
充当 UX Design 和 Visual Design/Implementation 之间的质量关
`/team-ui` 管道。

**运行此技能：**
- 使用 `/ux-design` 完成 UX 规范后
- 移交给 `ui-programmer` 或 `art-director` 之前
- 在从生产前到生产的门控检查之前（需要关键屏幕
  已审查 UX 规格）
- 对 UX 规范进行重大修订后

**判决级别：**
- **已批准** — 规范完整、一致且可实施
- **需要修订**——发现具体差距；在移交之前修复，但不是完全重新设计
- **需要进行重大修改**——范围、玩家需求或
  完整性；需要大量返工

---

## 第一阶段：解析参数

- **具体文件路径**（例如，`/ux-review design/ux/inventory.md`）：验证
  那一份文件
- **`all`**：查找 `design/ux/` 中的所有文件并验证每个文件
- **`hud`**：专门验证`design/ux/hud.md`
- **`patterns`**：专门验证`design/ux/interaction-patterns.md`
- **无参数**：询问用户要验证哪个规范

对于`all`，先输出一个汇总表（文件 | verdict | 主要问题）然后
每个的完整细节。

---

## 第 2 阶段：加载交叉引用上下文

在验证任何规范之前，请加载：

1. **输入和平台配置**：Read `.codex/docs/technical-preferences.md` 和
   提取 `## Input & Platform`。这是输入的权威来源
   游戏支持的方法 - 用它来驱动输入法覆盖率检查
   阶段 3A，不是规范自己的标头。如果未配置，则返回到规范标头。
2. `design/accessibility-requirements.md` 中承诺的可访问性层
   (if it exists)
3. 交互模式库位于 `design/ux/interaction-patterns.md`（如果
   it exists)
4. 规范标题中引用的 GDD（阅读其 UI 要求部分）
5. 位于 `design/player-journey.md` 的玩家旅程地图（如果存在）
   上下文到达验证

---

## 第 3A 阶段：UX 规格验证清单

针对基于 `ux-spec.md` 的文档运行所有检查。

### 完整性（必填部分）

- [ ] 文档标题包含状态、作者、平台目标
- [ ] 目的和玩家需求——有玩家视角的需求声明（不是
  developer-perspective)
- [ ] 玩家到达时的背景 — 描述玩家的状态和之前的活动
- [ ] 导航位置 — 显示屏幕在层次结构中的位置
- [ ] 入口和出口点 - 记录所有入口源和出口目的地
- [ ] 布局规范 — 定义区域、提供组件库存表
- [ ] 状态和变体 - 至少：加载、empty/populated 和错误状态
  documented
- [ ] 交互图——涵盖所有目标输入法（查看平台目标
  in header)
- [ ] 数据要求 - 每个显示的数据元素都有一个源系统和所有者
- [ ] 触发的事件 — 每个玩家操作都有一个相应的事件或 null
  explanation
- [ ] 过渡和动画 - 至少指定 enter/exit 过渡
- [ ] 可访问性要求 - 存在屏幕级要求
- [ ] 本地化注意事项 - 文本元素的最大字符数
- [ ] 验收标准——至少 5 个具体的可测试标准

### 质量检查

**玩家需要清晰度**
- [ ] 目的是从玩家角度写的，而不是 system/developer 角度
- [ ] 玩家到达时的目标是明确的（“玩家到达时想要 ___”）
- [ ] 玩家到达时的背景是特定的（不仅仅是“他们打开了
  inventory")

**状态的完整性**
- [ ] 记录错误状态（不仅仅是快乐路径）
- [ ] 记录空状态（无数据场景）
- [ ] 如果屏幕获取异步数据，则会记录加载状态
- [ ] 任何带有计时器或自动关闭的状态都会记录持续时间

**输入法覆盖**
- [ ] 如果平台包括 PC：完全指定仅键盘导航
- [ ] 如果平台包括 console/gamepad：方向键导航和面部按钮
  映射记录
- [ ] 无需在游戏手柄上实现像鼠标一样的精准交互
- [ ] 定义焦点顺序（键盘的 Tab 顺序、游戏手柄的方向键顺序）

**数据架构**
- [ ] 没有数据元素将“UI”列为所有者（UI 不得拥有游戏状态）
- [ ] 更新频率是为所有实时数据指定的（不仅仅是“实时”——
  什么触发更新？）
- [ ] 为所有数据元素指定空处理（当数据为空时显示的内容）
  不可用？）

**Accessibility**
- [ ] `accessibility-requirements.md` 的可访问性等级已匹配或超出
- [ ] 如果是基本层：没有纯颜色信息指示器
- [ ] 如果是标准层+：记录对焦顺序，指定文本对比度
- [ ] 如果综合层+：关键状态更改的屏幕阅读器公告
- [ ] 色盲检查：任何颜色编码的元素都有非颜色替代品

**GDD 对齐**
- [ ] 本规范中解决了标头中引用的每个 GDD UI 要求
- [ ] 如果没有相应的 GDD，则没有 UI 元素会显示或修改游戏状态
  requirement
- [ ] 否 GDD UI 此规范中缺少要求（交叉检查引用的
  GDD 部分）

**模式库一致性**
- [ ] 所有交互组件都引用模式库（或者注意它们是
  新模式）
- [ ] 如果模式行为已存在于
  模式库
- [ ] 本规范中发明的任何新模式都会被标记为添加到
  模式库

**Localization**
- [ ] 所有文本较多的元素都会出现字符限制警告
- [ ] 任何布局关键的文本都已标记为 40% 扩展空间

**验收标准质量**
- [ ] 对于没有看过设计文档的 QA 测试人员来说，标准足够具体
- [ ] 存在性能标准（屏幕在 Xms 内打开）
- [ ] 存在分辨率标准
- [ ] 没有标准需要阅读另一篇文档来评估

---

## 阶段 3B：HUD 验证清单

针对基于 `hud-design.md` 的文档运行所有检查。

### Completeness

- [ ] HUD 哲学定义
- [ ] 信息架构表涵盖 GDD 中具有 UI 要求的所有系统
- [ ] 为所有目标平台定义了安全区域边距的布局区域
- [ ] 每个 HUD 元素都有完整的规格（区域、可见性触发器、数据
  来源、优先级）
- [ ] HUD 游戏上下文状态至少涵盖：探索、战斗、
  dialogue/cutscene，已暂停
- [ ] 定义视觉预算（最大同时元素、最大屏幕百分比）
- [ ] 平台适配覆盖所有目标平台
- [ ] 为玩家可调节的元素提供调音旋钮

### 质量检查

- [ ] 如果没有可见性规则，则没有 HUD 元素覆盖中心游戏区域
  hide it
- [ ] 任何 GDD 中存在的每个信息项要么在 HUD 中，要么在 HUD 中
  明确分类为“hidden/demand”
- [ ] 所有颜色编码的 HUD 元素都有色盲变体
- [ ] 反馈和通知部分中的 HUD 元素有 queue/priority
  行为定义
- [ ] 视觉预算合规性：同步元素总数在预算范围内

### GDD 对齐

- [ ] `design/gdd/systems-index.md` 和 UI 类别中的所有系统都具有
  HUD 中的表示（或合理缺席）

---

## 阶段 3C：模式库验证清单

- [ ] 模式目录索引是最新的（与文档中的实际模式匹配）
- [ ] 指定了所有标准控制模式：按钮变体、切换、
  滑块、下拉菜单、列表、网格、模态、对话框、吐司、工具提示、进度条、
  输入字段、标签栏、滚动条
- [ ] 存在当前 UX 规格所需的所有游戏特定模式
- [ ] 每个模式都有：何时使用、何时不使用、完整的状态规范、
  可访问性规范、实施说明
- [ ] 动画标准表呈现
- [ ] 存在声音标准表
- [ ] 模式之间没有冲突的行为（例如，“返回”行为一致
  跨越所有导航模式）

---

## 第四阶段：输出判决

```markdown
## UX Review: [Document Name]
**Date**: [date]
**Reviewer**: ux-review skill
**Document**: [file path]
**Platform Target**: [from header]
**Accessibility Tier**: [from header or accessibility-requirements.md]

### Completeness: [X/Y sections present]
- [x] Purpose & Player Need
- [ ] States & Variants — MISSING: error state not documented

### Quality Issues: [N found]
1. **[Issue title]** [BLOCKING / ADVISORY]
   - What's wrong: [specific description]
   - Where: [section name]
   - Fix: [specific action to take]

### GDD Alignment: [ALIGNED / GAPS FOUND]
- GDD [name] UI Requirements — [X/Y requirements covered]
- Missing: [list any uncovered GDD requirements]

### Accessibility: [COMPLIANT / GAPS / NON-COMPLIANT]
- Target tier: [tier]
- [list specific accessibility findings]

### Pattern Library: [CONSISTENT / INCONSISTENCIES FOUND]
- [findings]

### Verdict: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
**Blocking issues**: [N] — must be resolved before implementation
**Advisory issues**: [N] — recommended but not blocking

[For APPROVED]: This spec is ready for handoff to `/team-ui` Phase 2
(Visual Design).

[For NEEDS REVISION]: Address the [N] blocking issues above, then re-run
`/ux-review`.

[For MAJOR REVISION NEEDED]: The spec has fundamental gaps in [areas].
Recommend returning to `/ux-design` to rework [sections].
```

---

## 第五阶段：协作协议

该技能是只读的——它从不编辑或写入文件。它仅报告调查结果。

作出判决后：
- 对于**批准**：建议运行 `/team-ui` 开始实施协调
- 对于**需要修订**：提供帮助修复特定差距（“您希望我
  帮助起草缺失的错误状态？”）——但不自动修复；等待用户
  instruction
- 对于 **需要重大修订**：建议返回 `/ux-design`
  需要返工的特定部分

切勿阻止用户继续操作 - 该结论是建议性的。记录风险，
呈现调查结果，让用户决定是否继续进行，尽管存在顾虑。一个用户
选择继续进行需求修订规范的人承担记录的风险。
