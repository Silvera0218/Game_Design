---
name: gate-check
description: "验证开发阶段之间推进的准备情况。生成包含特定阻止程序和所需工件的 PASS/CONCERNS/FAIL 判决。当用户说“我们准备好转向 X 了吗”、“我们可以进入生产吗”、“检查我们是否可以开始下一阶段”、“通过大门”时使用。"
---

# 阶段门验证

该技能验证项目是否已准备好进入下一个开发阶段
阶段。它检查所需的工件、质量标准和阻碍因素。

**与 `/project-stage-detect` 不同**：该技能是诊断性的（“我们在哪里？”）。
这项技能是规定性的（“我们准备好前进了吗？”并做出正式的裁决）。

## 生产阶段 (7)

该项目将经历以下阶段：

1. **概念** — 头脑风暴，游戏概念文档
2. **系统设计** — 绘制系统、编写 GDD
3. **技术设置** — 引擎配置、架构决策
4. **预生产** — 原型设计、垂直切片验证
5. **生产** — 功能开发（Epic/Feature/Task 跟踪活动）
6. **抛光** — 性能、游戏测试、错误修复
7. **发布** — 启动准备、认证

**当门通过时**，将新的阶段名称写入`production/stage.txt`
（单行，例如 `Production`）。这会立即更新状态行。

---

## 1. 解析参数

**目标阶段：** `$ARGUMENTS[0]`（空白=自动检测当前阶段，然后验证下一个转换）

还解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则阅读 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

注意：在 `solo` 模式下，将跳过导向器生成（CD-PHASE-GATE、TD-PHASE-GATE、PR-PHASE-GATE、AD-PHASE-GATE）——门检查仅变为工件存在检查。在 `lean` 模式下，所有四个控制器仍然运行（相位门是精益模式的目的）。

- **带参数**：`/gate-check production` — 验证该特定阶段的准备情况
- **无参数**：使用与以下相同的启发式自动检测当前阶段
  `/project-stage-detect`，然后**运行前与用户确认**：

使用 `AskUserQuestion`：
  - 提示：“检测到的阶段：**[current stage]**。[Current] → [Next] 转换的运行门。这是正确的吗？”
  - Options:
    - `[A] Yes — run this gate`
    - `[B] No — pick a different gate`（如果选择，则显示第二个小部件，列出所有门选项：概念→系统设计，系统设计→技术设置，技术设置→预生产，预生产→生产，生产→抛光，抛光→发布）

  当未提供参数时，请勿跳过此确认步骤。

---

## 2. 相位门定义

### 门：概念→系统设计

**所需物品：**
- [ ] `design/gdd/game-concept.md` 存在并且有内容
- [ ] 定义游戏支柱（在概念文档或 `design/gdd/game-pillars.md` 中）
- [ ] 视觉识别锚点部分存在于 `design/gdd/game-concept.md` 中（来自头脑风暴第 4 阶段艺术总监输出）

**质量检查：**
- [ ] 游戏概念已经过审核（`/design-review` 判决不需要进行重大修改）
- [ ] 描述并理解核心循环
- [ ] 目标受众已确定
- [ ] 视觉识别锚包含一行视觉规则和至少 2 个支持视觉原则

---

### 门：系统设计→技术设置

**所需物品：**
- [ ] 系统索引位于 `design/gdd/systems-index.md`，至少枚举了 MVP 系统
- [ ] 所有 MVP 层 GDD 都存在于 `design/gdd/` 中并单独通过 `/design-review`
- [ ] `design/gdd/`中存在跨GDD审查报告（来自`/review-all-gdds`）

**质量检查：**
- [ ] 所有 MVP GDD 通过单独的设计审查（8 个必需部分，无需重大修改裁决）
- [ ] `/review-all-gdds` 判决不为 FAIL（跨 GDD 一致性和设计理论检查通过）
- [ ] 由 `/review-all-gdds` 标记的所有跨 GDD 一致性问题均已解决或明确接受
- [ ] 系统依赖关系映射到系统索引中并且双向一致
- [ ] MVP 优先级已定义
- [ ] 没有标记过时的 GDD 引用（较旧的 GDD 已更新以反映后续 GDD 中做出的决策）

---

### 大门：技术设置 → 预生产

**所需物品：**
- [ ] 选择的引擎（AGENTS.md 技术堆栈不是 `[CHOOSE]`）
- [ ] 配置的技术首选项（已填充 `.codex/docs/technical-preferences.md`）
- [ ] 艺术圣经位于 `design/art/art-bible.md`，至少包含第 1-4 节（视觉识别基金会）
- [ ] `docs/architecture/` 中至少包含 3 个架构决策记录
      基础层系统（场景管理、事件架构、save/load）
- [ ] 引擎参考文档存在于 `docs/engine-reference/[engine]/` 中
- [ ] 测试框架初始化：`tests/unit/`和`tests/integration/`目录存在
- [ ] CI/CD 测试工作流程存在于 `.github/workflows/tests.yml`（或同等版本）
- [ ] 至少存在一个示例测试文件来确认框架功能正常
- [ ] 主架构文档位于 `docs/architecture/architecture.md`
- [ ] 架构可追溯性索引位于 `docs/architecture/architecture-traceability.md`
- [ ] `/architecture-review`已运行（`docs/architecture/`中存在审核报告文件）
- [ ] `design/accessibility-requirements.md` 存在并已承诺可访问性层
- [ ] `design/ux/interaction-patterns.md` 存在（模式库已初始化，即使是最小的）

**质量检查：**
- [ ] 架构决策涵盖核心系统（渲染、输入、状态管理）
- [ ] 技术偏好设置了命名约定和性能预算
- [ ] 辅助功能层已定义并记录（甚至“基本”也是可以接受的 - 未定义则不可以）
- [ ] 至少启动一个屏幕的 UX 规范（通常主菜单或核心 HUD 是在技术设置期间设计的）
- [ ] 所有 ADR 都有一个**引擎兼容性部分**，并带有引擎版本标记
- [ ] 所有 ADR 都有一个 **GDD 要求解决部分**，具有明确的 GDD 链接
- [ ] 没有 ADR 引用 `docs/engine-reference/[engine]/deprecated-apis.md` 中列出的 API
- [ ] 所有高风险引擎域（根据 VERSION.md）均已明确解决
      在架构文档中或标记为开放问题
- [ ] 架构可追溯性矩阵具有**零基础层间隙**
      （所有基金会要求在预生产之前必须覆盖 ADR）

**ADR 循环依赖性检查**：对于 `docs/architecture/` 中的所有 ADR，请阅读每个 ADR 的
“ADR 依赖项”/“取决于”部分。构建依赖图（ADR-A → ADR-B 表示
A 取决于 B）。如果检测到任何循环（例如A→B→A，或A→B→C→A）：
- 标记为 **FAIL**：“循环 ADR 依赖项：[ADR-X] → [ADR-Y] → [ADR-X]。
  当循环存在时，两者都无法达到“已接受”状态。删除一条“取决于”边
  打破循环。”

**引擎验证**（首先阅读 `docs/engine-reference/[engine]/VERSION.md`）：
- [ ] 涉及截止后引擎 API 的 ADR 被标记为知识风险：HIGH/MEDIUM
- [ ] `/architecture-review` 引擎审核显示没有弃用的 API 用法
- [ ] 所有 ADR 都同意相同的引擎版本（没有过时的版本引用）

---

### 大门：预生产→生产

**所需物品：**
- [ ] `prototypes/` 中至少有 1 个原型以及自述文件
- [ ] 第一个冲刺计划存在于 `production/sprints/` 中
- [ ] 艺术圣经完整（全部 9 个部分），AD-ART-BIBLE 签核判决记录在 `design/art/art-bible.md` 中
- [ ] 叙述文档中引用的关键角色存在角色视觉配置文件
- [ ] 系统索引中的所有 MVP 层 GDD 均已完成
- [ ] 主架构文档位于 `docs/architecture/architecture.md`
- [ ] `docs/architecture/` 中至少存在 3 个涵盖基础层决策的 ADR
- [ ] 控制清单存在于 `docs/architecture/control-manifest.md`
      （由 `/create-control-manifest` 根据已接受的 ADR 生成）
- [ ] `production/epics/` 中定义的史诗至少具有基础和核心
      存在层史诗（使用 `/create-epics layer: foundation` 和
      `/create-epics layer: core` 创建它们，然后 `/create-stories [epic-slug]`
      对于每个史诗）
- [ ] 垂直切片构建存在并且可以播放（不仅仅是范围定义的）
- [ ] Vertical Slice 已经过至少 3 个会话的游戏测试（内部正常）
- [ ] Vertical Slice 游戏测试报告位于 `production/playtests/` 或同等版本
- [ ] UX 关键屏幕的规格：主菜单、核心游戏 HUD（位于 `design/ux/`）、暂停菜单
- [ ] HUD 设计文档存在于 `design/ux/hud.md`（如果游戏中有 HUD）
- [ ] 所有按键屏幕 UX 规格均已通过 `/ux-review`（判决已批准或接受需要修订）

**质量检查：**
- [ ] **核心循环乐趣得到验证** - 游戏测试数据证实中央机制是令人愉快的，而不仅仅是功能性的。明确检查 Vertical Slice 游戏测试报告。
- [ ] UX 规格涵盖 MVP 层 GDD 中的所有 UI 要求部分
- [ ] 交互模式库记录了关键屏幕中使用的模式
- [ ] `design/accessibility-requirements.md` 的辅助功能层已在所有关键屏幕 UX 规范中得到解决
- [ ] Sprint 计划引用 `production/epics/` 中的真实故事文件路径
      （不仅仅是 GDD — 故事必须嵌入 GDD 请求 ID + ADR 参考）
- [ ] **垂直切片是完整的**，而不仅仅是范围——构建演示了端到端的完整核心循环。至少有一个完整的[开始→挑战→解决]循环有效。
- [ ] 架构文档在基础层或核心层中没有未解决的开放问题
- [ ] 所有 ADR 均具有标有引擎版本的引擎兼容性部分
- [ ] 所有 ADR 都有 ADR 依赖项部分（即使所有字段均为“无”）
- [ ] 手动验证确认 GDD + 架构 + 史诗是一致的
      （如果最近没有完成，请运行 `/review-all-gdds` 和 `/architecture-review`）
- [ ] **核心幻想已交付** - 至少一位游戏测试者独立描述了与核心系统 GDD 的玩家幻想部分相匹配的体验（无需提示）。

**垂直切片验证**（如果任何一项为“否”，则失败）：
- [ ] 人类在没有开发人员指导的情况下完成了核心循环
- [ ] 游戏会在游戏开始的前 2 分钟内传达要做什么
- [ ] Vertical Slice 构建中不存在严重的“有趣阻碍”错误
- [ ] 与核心机制互动感觉很好（这是一个主观检查——询问用户）

> **注意**：如果任何垂直切片验证项为 FAIL，则判定自动为 FAIL
> 不考虑其他检查。在没有经过验证的垂直切片的情况下前进是导致以下问题的第一大原因：
> 游戏开发中的生产失败（根据来自 155 个项目的 GDC 事后分析数据）。

---

### 门：生产→抛光

**所需物品：**
- [ ] `src/` 将活动代码组织成子系统
- [ ] GDD 的所有核心机制均已实现（交叉引用 `design/gdd/` 与 `src/`）
- [ ] 主要游戏路径是端到端可玩的
- [ ] 测试文件存在于 `tests/unit/` 和 `tests/integration/` 中，涵盖逻辑和集成故事
- [ ] 此冲刺中的所有逻辑故事在 `tests/unit/` 中都有相应的单元测试文件
- [ ] 烟雾检查已运行，结果为“通过”或“通过但有警告”判定 — 报告存在于 `production/qa/` 中
- [ ] QA 计划存在于 `production/qa/`（由 `/qa-plan` 生成）中，涵盖此冲刺或最终生产冲刺
- [ ] QA 签核报告存在于 `production/qa/`（由 `/team-qa` 生成）中，判决已批准或已条件批准
- [ ] `production/playtests/` 中记录了至少 3 个不同的游戏测试会话
- [ ] 游戏测试报告涵盖：新玩家体验、游戏中期系统和难度曲线
- [ ] 游戏概念中的有趣假设已得到明确验证或修改

**质量检查：**
- [ ] 测试正在通过（通过 Bash 运行测试套件）
- [ ] 任何错误跟踪器中都没有 critical/blocker 错误或已知问题
- [ ] 核心循环按设计播放（与 GDD 验收标准相比）
- [ ] 性能在预算之内（检查 technical-preferences.md 目标）
- [ ] 游戏测试结果已被审查并解决了关键的有趣问题（不仅仅是记录）
- [ ] 没有发现“混乱循环”——游戏中没有超过 50% 的游戏测试者在不知道原因的情况下陷入困境的情况
- [ ] 难度曲线与难度曲线设计文档相匹配（如果 `design/difficulty-curve.md` 中存在）
- [ ] 所有实现的屏幕都有相应的 UX 规格（没有“代码内设计”屏幕）
- [ ] 交互模式库是最新的，包含实现中使用的所有模式
- [ ] 根据 `design/accessibility-requirements.md` 中的承诺层验证可访问性合规性

---

### 门：抛光→发布

**所需物品：**
- [ ] 里程碑计划中的所有功能均已实施
- [ ] 内容完整（设计文档中引用的所有级别、资产、对话均存在）
- [ ] 本地化字符串被外部化（`src/` 中没有硬编码的面向玩家的文本）
- [ ] QA 测试计划存在（`production/qa/` 中的 `/qa-plan` 输出）
- [ ] QA 签核报告存在（`/team-qa` 输出 — 已批准或已批准但有条件）
- [ ] 所有必须具备的故事测试证据均已提供（Logic/Integration：测试文件通过；Visual/Feel/UI：`production/qa/evidence/` 中的签核文档）
- [ ] 候选版本构建上的烟雾检查顺利通过（通过判定）
- [ ] 之前的冲刺没有测试回归（测试套件完全通过）
- [ ] 余额数据已审核（`/balance-check` 运行）
- [ ] 已完成发布清单（`/release-checklist` 或 `/launch-checklist` 运行）
- [ ] 存储准备好的元数据（如果适用）
- [ ] 起草变更日志/补丁说明

**质量检查：**
- [ ] 完整的 QA 通行证由 `qa-lead` 签署
- [ ] 所有测试均通过
- [ ] 所有目标平台均达到性能目标
- [ ] 没有已知的严重、高或中等严重性错误
- [ ] 涵盖辅助功能基础知识（重新映射、文本缩放（如果适用））
- [ ] 所有目标语言的本地化验证
- [ ] 满足法律要求（EULA、隐私政策、年龄分级（如果适用））
- [ ] 干净地构建编译和打包

---

## 3. 运行门检查

**在运行工件检查之前**，请阅读 `docs/consistency-failures.md`（如果存在）。
提取其域与目标阶段匹配的条目（例如，如果检查
系统设计 → 技术设置，拉取经济、战斗或任何 GDD 领域的条目；
如果检查技术设置 → 预生产，请提取架构、引擎中的条目。
将这些作为上下文——目标域中反复出现的冲突模式
加强对这些具体检查的审查。

对于目标门中的每个项目：

### 文物检查
- 使用 `Glob` 和 `Read` 验证文件是否存在并具有有意义的内容
- 不要只检查存在性 - 验证文件是否具有真实内容（而不仅仅是模板标头）
- 对于代码检查，验证目录结构和文件计数

**系统设计 → 技术设置门 — 交叉 GDD 审查检查**：
使用 `Glob('design/gdd/gdd-cross-review-*.md')` 查找 `/review-all-gdds` 报告。
如果没有文件匹配，则将“跨 GDD 审核报告存在”工件标记为 **FAIL** 并
突出显示：“在 `design/gdd/` 中找不到 `/review-all-gdds` 报告。运行
`/review-all-gdds`，然后再进入技术设置。”
如果找到文件，则读取该文件并检查判定行：“失败”判定意味着
跨 GDD 一致性检查失败，必须在继续之前解决。

### 质量检查
- 对于测试检查：如果配置了测试运行程序，则通过 `Bash` 运行测试套件
- 对于设计审查检查：`Read` GDD 并检查 8 个必需部分
- 对于性能检查：`Read` technical-preferences.md 并与任何
  `tests/performance/` 或最近的 `/perf-profile` 输出中的分析数据
- 对于本地化检查：`Grep` 用于 `src/` 中的硬编码字符串

### 交叉引用检查
- 将 `design/gdd/` 文档与 `src/` 实现进行比较
- 检查架构文档中引用的每个系统是否都有相应的代码
- 验证冲刺计划是否引用实际工作项目

---

## 4. 协作评估

对于无法自动验证的项目，**询问用户**：

- “我无法自动验证核心循环是否运行良好。它经过了游戏测试吗？”
- “没有找到游戏测试报告。是否进行过非正式测试？”
- “性能分析数据不可用。您想运行 `/perf-profile` 吗？”

**永远不要假设无法验证的项目通过。**将它们标记为“需要手动检查”。

---

## 4b.董事小组评估

在生成最终判决之前，使用 `.codex/docs/director-gates.md` 中的并行门协议通过 Task 将所有四个控制器生成为**并行子代理**。同时发出所有四个 Task 调用 - 不要等待一个调用才开始下一个调用。

**并行生成：**

1. **`creative-director`** — 门 **CD-相-门** (`.codex/docs/director-gates.md`)
2. **`technical-director`** — 门 **TD 相门** (`.codex/docs/director-gates.md`)
3. **`producer`** — 门 **PR-PHASE-GATE** (`.codex/docs/director-gates.md`)
4. **`art-director`** — 门 **AD-PHASE-GATE** (`.codex/docs/director-gates.md`)

传递给每个：目标阶段名称、存在的工件列表以及该门定义中列出的上下文字段。

**收集所有四份回复，然后呈现董事小组摘要：**

```
## Director Panel Assessment

Creative Director:  [READY / CONCERNS / NOT READY]
  [feedback]

Technical Director: [READY / CONCERNS / NOT READY]
  [feedback]

Producer:           [READY / CONCERNS / NOT READY]
  [feedback]

Art Director:       [READY / CONCERNS / NOT READY]
  [feedback]
```

**适用判决：**
- 任何董事返回“未就绪”→ 判决最低为“失败”（用户可以通过明确确认来覆盖）
- 任何董事都会返回担忧 → 判决是最低限度的担忧
- 所有四个 READY → 有资格获得 PASS（仍需接受第 3 节中的工件和质量检查）

---

## 5. 输出判决结果

```
## Gate Check: [Current Phase] → [Target Phase]

**Date**: [date]
**Checked by**: gate-check skill

### Required Artifacts: [X/Y present]
- [x] design/gdd/game-concept.md — exists, 2.4KB
- [ ] docs/architecture/ — MISSING (no ADRs found)
- [x] production/sprints/ — exists, 1 sprint plan

### Quality Checks: [X/Y passing]
- [x] GDD has 8/8 required sections
- [ ] Tests — FAILED (3 failures in tests/unit/)
- [?] Core loop playtested — MANUAL CHECK NEEDED

### Blockers
1. **No Architecture Decision Records** — Run `/architecture-decision` to create one
   covering core system architecture before entering production.
2. **3 test failures** — Fix failing tests in tests/unit/ before advancing.

### Recommendations
- [Priority actions to resolve blockers]
- [Optional improvements that aren't blocking]

### Verdict: [PASS / CONCERNS / FAIL]
- **PASS**: All required artifacts present, all quality checks passing
- **CONCERNS**: Minor gaps exist but can be addressed during the next phase
- **FAIL**: Critical blockers must be resolved before advancing
```

---

## 5a.验证链

在第五阶段起草裁决后，在最终确定之前对其提出质疑。

**第 1 步 — 生成 5 个挑战问题**，旨在反驳判决：

对于 **PASS** 草稿：
- “我通过实际读取文件来验证哪些质量检查，而不是推断它们通过了？”
- “是否有未经用户确认而标记为“通过”的需要手动检查的项目？”
- “我是否确认所有列出的工件都有真实内容，而不仅仅是空标题？”
- “我认为是次要的任何阻碍因素实际上会阻止该阶段的成功吗？”
- “我对哪一项检查最没有信心，为什么？”

对于 **担忧** 草案：
- “考虑到该项目的当前状态，任何列出的问题是否都会被提升为阻碍因素？”
- “这个问题可以在下一阶段得到解决，还是会随着时间的推移而变得复杂？”
- “我是否将任何失败条件软化为担忧以避免做出更严厉的判决？”
- “是否有一些我没有检查过的文物可能会揭示其他阻碍因素？”
- “即使每一个问题都很小，所有问题加在一起是否会造成阻塞问题？”

对于**失败**草稿：
- “我是否准确地区分了硬性阻碍和强烈建议？”
- “有哪些 PASS 项目是我太宽容的吗？”
- “我是否遗漏了用户应该了解的任何其他阻止程序？”
- “我能否提供一条通向 PASS 的最小路径——必须改变的具体 3 件事？”
- “失败情况是否可以解决，或者是否表明存在更深层次的设计问题？”

**第 2 步 — 独立回答每个问题**。
不要引用草稿判决文本——重新检查特定文件或询问用户。

**第 3 步 — 根据需要进行修改：**
- 如果任何答案显示错过了阻止程序→升级判决（通过→关注或关注→失败）
- 如果任何答案揭示了夸大的阻碍因素 → 仅在引用具体证据时降级
- 如果答案一致 → 确认判决不变

**第 4 步 — 注意最终报告输出中的验证**：
`Chain-of-Verification: [N] questions checked — verdict [unchanged | revised from X to Y]`

---

## 6. PASS 更新阶段

当判决为 **PASS** 并且用户确认他们想要晋级时：

1. Write 为 `production/stage.txt` 的新阶段名称（单行，无尾随换行符）
2. 这会立即更新所有未来会话的状态行

示例：如果通过“预生产→生产”大门：
```bash
echo -n "Production" > production/stage.txt
```

**写作前务必询问**：“门已通过。我可以将 `production/stage.txt` 更新为“生产”吗？”

---

## 7. 关闭下一步小部件

做出判决并完成任何 stage.txt 更新后，使用 `AskUserQuestion` 以结构化的下一步提示结束。

**针对刚刚运行的门定制选项：**

对于**系统设计通过**：
```
Gate passed. What would you like to do next?
[A] Run /create-architecture — produce your master architecture blueprint and ADR work plan (recommended next step)
[B] Design more GDDs first — return here when all MVP systems are complete
[C] Stop here for this session
```

> **系统设计通过注意事项**：`/create-architecture` 是写入任何 ADR 之前所需的下一步。它生成主架构文档和要编写的 ADR 的优先级列表。在没有此步骤的情况下运行 `/architecture-decision` 意味着在没有蓝图的情况下编写 ADR - 跳过它需要您自担风险。

对于**技术设置通过**：
```
Gate passed. What would you like to do next?
[A] Start Pre-Production — begin prototyping the Vertical Slice
[B] Write more ADRs first — run /architecture-decision [next-system]
[C] Stop here for this session
```

对于所有其他门，提供该阶段的两个最合乎逻辑的后续步骤以及“在此停止”。

---

## 八、后续行动

根据判决，建议具体的后续步骤：

- **没有艺术圣经？** → `/art-bible` 创建视觉识别规范
- **艺术圣经存在，但没有资产规格？** → `/asset-spec system:[name]` 用于生成每个资产的视觉规格和来自批准的 GDD 的生成提示
- **没有游戏概念？** → `/brainstorm` 创建一个
- **没有系统索引？** → `/map-systems` 将概念分解为系统
- **缺少设计文档？** → `/reverse-document` 或委托给 `game-designer`
- **需要小的设计更改？** → `/quick-design` 在约 4 小时内进行更改（绕过完整的 GDD 管道）
- **没有 UX 规格？** → `/ux-design [screen name]` 用于创作规格，或 `/team-ui [feature]` 用于完整管道
- **UX 规格尚未审核？** → `/ux-review [file]` 或 `/ux-review all` 进行验证
- **没有辅助功能要求文档？** → 使用 `AskUserQuestion` 提供立即创建它：
  - 提示：“该门需要`design/accessibility-requirements.md`。我要从模板中创建它吗？”
  - 选项：`Create it now — I'll choose an accessibility tier`、`I'll create it myself`、`Skip for now`
  - 如果“立即创建”：使用第二个 `AskUserQuestion` 来请求层：
    - 提示：“哪个无障碍层适合这个项目？”
    - 选项：`Basic — remapping + subtitles only (lowest effort)`、`Standard — Basic + colorblind modes + scalable UI`、`Comprehensive — Standard + motor accessibility + full settings menu`、`Exemplary — Comprehensive + external audit + full customization`
  - 然后使用 `.codex/docs/templates/accessibility-requirements.md` 中的模板写入 `design/accessibility-requirements.md`，填写所选层。确认：“我可以写`design/accessibility-requirements.md`吗？”
- **没有交互模式库？** → `/ux-design patterns` 进行初始化
- **GDD 未经交叉审查？** → `/review-all-gdds`（在所有 MVP GDD 单独批准后运行）
- **跨 GDD 一致性问题？** → 修复标记的 GDD，然后重新运行 `/review-all-gdds`
- **没有测试框架？** → `/test-setup` 为您的引擎搭建框架
- **当前冲刺没有 QA 计划？** → `/qa-plan sprint` 在实施开始之前生成一个计划
- **缺少 ADR？** → `/architecture-decision` 用于个人决定
- **没有主架构文档？** → `/create-architecture` 获取完整蓝图
- **ADR 缺少引擎兼容性部分？** → 重新运行 `/architecture-decision`
  或手动将引擎兼容性部分添加到现有 ADR
- **缺少控制清单？** → `/create-control-manifest`（需要接受的 ADR）
- **缺少史诗？** → `/create-epics layer: foundation` 然后 `/create-epics layer: core` （需要控制清单）
- **史诗缺少故事？** → `/create-stories [epic-slug]`（在创建每个史诗后运行）
- **故事尚未准备好实施？** → `/story-readiness` 在开发人员选择故事之前对其进行验证
- **测试失败？** → 委托给 `lead-programmer` 或 `qa-tester`
- **没有游戏测试数据？** → `/playtest-report`
- **少于 3 次游戏测试？** → 在前进之前运行更多游戏测试。使用 `/playtest-report` 构建结果。
- **没有难度曲线文档？** → 考虑在打磨之前在 `design/difficulty-curve.md` 创建一个
- **没有玩家旅程文档？** → 使用玩家旅程模板创建 `design/player-journey.md`
- **需要快速冲刺检查？** → `/sprint-status` 当前冲刺进度快照
- **性能未知？** → `/perf-profile`
- **未本地化？** → `/localize`
- **准备好发布了吗？** → `/launch-checklist`

---

## 协作协议

该技能遵循协作设计原则：

1. **首先扫描**：检查所有工件和质量门
2. **询问未知事物**：不要对无法验证的事情假设通过
3. **当前发现**：显示完整的清单及状态
4. **用户决定**：结论是建议——用户做出最终决定
5. **获得批准**：“我可以将此门检查报告写给 production/gate-checks/ 吗？”

**永远不要**阻止用户前进——该结论是建议性的。记录风险
并让用户决定是否继续，尽管有顾虑。
