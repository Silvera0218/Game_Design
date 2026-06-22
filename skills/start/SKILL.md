---
name: start
description: "首次入职 - 询问您在哪里，然后引导您进入正确的工作流程。没有假设。"
---

# 引导式入职

该技能写入一个文件：`production/review-mode.txt`（查看阶段 3b 中设置的模式配置）。

该技能是新用户的切入点。它并不假设您有游戏创意、引擎偏好或任何先前的经验。它首先询问，然后将您引导至正确的工作流程。

---

## 第一阶段：检测项目状态

在提出任何问题之前，请默默收集背景信息，以便您可以定制指导。不要在没有提示的情况下显示这些结果——它们会告诉你建议，而不是对话的开场白。

Check:
- **发动机已配置？** Read `.codex/docs/technical-preferences.md`。如果引擎字段包含 `[TO BE CONFIGURED]`，则表示未设置引擎。
- **游戏概念存在吗？** 检查 `design/gdd/game-concept.md`。如果不存在，再检查当前项目常用结构：`GDD/00_项目总览_GDD.md` 和 `GDD/INDEX.md`。
- **源代码存在吗？** Glob 用于 `src/` 中的源文件（`*.gd`、`*.cs`、`*.cpp`、`*.h`、`*.rs`、 `*.py`、`*.js`、`*.ts`）。
- **原型存在吗？** 检查 `prototypes/` 中的子目录。
- **设计文档存在吗？** 计算 `design/gdd/` 中的 markdown 文件；如果该目录不存在，计算 `GDD/*_GDD.md` 和 `GDD/INDEX.md`。
- **生产工件？** 检查 `production/sprints/` 或 `production/milestones/` 中的文件。

将这些发现存储在内部，以验证用户的自我评估并定制建议。

---

## 第 2 阶段：询问用户在哪里

这是用户看到的第一件事。将 `AskUserQuestion` 与这些确切的选项一起使用，以便用户可以单击而不是键入：

- **提示**：“欢迎来到 Codex 游戏工作室！在我提出任何建议之前，我想了解一下您的出发点。您现在的游戏创意处于什么阶段？”
- **Options**:
  - `A) No idea yet` — 我根本没有游戏概念。我想探索并弄清楚要做什么。
  - `B) Vague idea` — 我心中有一个粗略的主题、感觉或类型（例如，“有空间的东西”或“舒适的农场游戏”），但没有具体的内容。
  - `C) Clear concept` - 我知道核心思想 - 类型、基本机制，也许是一个音调句子 - 但还没有将其形式化为文档。
  - `D) Existing work` — 我已经完成了设计文档、原型、代码或重要规划。我想组织或继续工作。

等待用户的选择。在他们做出回应之前不要继续。

---

## 第 3 阶段：基于答案的路线

#### 如果A：还不知道

用户首先需要创造性的探索。

1. 承认从零开始是完全没问题的
2. 简要解释一下 `/brainstorm` 的作用（使用专业框架引导构思 — MDA、玩家心理、动词优先设计）。提及它有两种模式：`/brainstorm open` 用于完全开放的探索，或者 `/brainstorm [hint]` 如果它们甚至有一个模糊的主题（例如“空间”、“舒适”、“恐怖”）。
3. 建议下一步运行 `/brainstorm open`，但请他们在想到某些事情时使用提示
4. 显示推荐路径：
   **概念阶段：**
   - `/brainstorm open` — 发现您的游戏概念
   - `/setup-engine` — 配置引擎（头脑风暴会推荐一个）
   - `/art-bible` — 定义视觉识别（使用视觉识别锚头脑风暴产生）
   - `/map-systems` — 将概念分解为系统
   - `/design-system` — 为每个 MVP 系统创建一个 GDD
   - `/review-all-gdds` — 跨系统一致性检查
   - `/gate-check` — 在架构工作之前验证准备情况
   **架构阶段：**
   - `/create-architecture` — 生成主架构蓝图和所需的 ADR 列表
   - `/architecture-decision (×N)` — 按照必需的 ADR 列表记录关键技术决策
   - `/create-control-manifest` — 将决策编译成可操作的规则表
   - `/architecture-review` — 验证架构覆盖范围
   **预生产阶段：**
   - `/ux-design` — 作者 UX 关键屏幕规范（主菜单、HUD、核心交互）
   - `/prototype` — 构建一次性原型来验证核心机制
   - `/playtest-report (×1+)` — 记录每个垂直切片游戏测试会话
   - `/create-epics` — 将系统映射到史诗
   - `/create-stories` — 将史诗分解为可实施的故事
   - `/sprint-plan` — 计划第一个冲刺
   **生产阶段：** → 通过 `/dev-story` 获取故事

#### 如果 B：模糊的想法

1. 让他们分享他们模糊的想法——即使是几句话就足够了
2. 以验证想法为起点（不要判断或重定向）
3. 推荐运行`/brainstorm [their hint]`来开发
4. 显示推荐路径：
   **概念阶段：**
   - `/brainstorm [hint]` — 将想法发展为完整的概念
   - `/setup-engine` — 配置引擎
   - `/art-bible` — 定义视觉识别（使用视觉识别锚头脑风暴产生）
   - `/map-systems` — 将概念分解为系统
   - `/design-system` — 为每个 MVP 系统创建一个 GDD
   - `/review-all-gdds` — 跨系统一致性检查
   - `/gate-check` — 在架构工作之前验证准备情况
   **架构阶段：**
   - `/create-architecture` — 生成主架构蓝图和所需的 ADR 列表
   - `/architecture-decision (×N)` — 按照必需的 ADR 列表记录关键技术决策
   - `/create-control-manifest` — 将决策编译成可操作的规则表
   - `/architecture-review` — 验证架构覆盖范围
   **预生产阶段：**
   - `/ux-design` — 作者 UX 关键屏幕规范（主菜单、HUD、核心交互）
   - `/prototype` — 构建一次性原型来验证核心机制
   - `/playtest-report (×1+)` — 记录每个垂直切片游戏测试会话
   - `/create-epics` — 将系统映射到史诗
   - `/create-stories` — 将史诗分解为可实施的故事
   - `/sprint-plan` — 计划第一个冲刺
   **生产阶段：** → 通过 `/dev-story` 获取故事

#### 如果 C：概念清晰

1. 让他们用一句话描述他们的概念——类型和核心机制。使用纯文本，而不是 AskUserQuestion （这是一个开放的响应）。
2. 确认这个概念，然后使用 `AskUserQuestion` 提供两条路径：
   - **提示**：“您想如何继续？”
   - **Options**:
     - `Formalize it first` — 运行 `/brainstorm [concept]` 将其构建为正确的游戏概念文档
     - `Jump straight in` — 现在转到 `/setup-engine`，然后手动写入 GDD
3. 显示推荐路径：
   **概念阶段：**
   - `/brainstorm` 或 `/setup-engine` —（他们从步骤 2 中选择）
   - `/art-bible` — 定义视觉识别（在头脑风暴后运行，或在概念文档存在后）
   - `/design-review` — 验证概念文档
   - `/map-systems` — 将概念分解为单独的系统
   - `/design-system` — 为每个 MVP 系统创建一个 GDD
   - `/review-all-gdds` — 跨系统一致性检查
   - `/gate-check` — 在架构工作之前验证准备情况
   **架构阶段：**
   - `/create-architecture` — 生成主架构蓝图和所需的 ADR 列表
   - `/architecture-decision (×N)` — 按照必需的 ADR 列表记录关键技术决策
   - `/create-control-manifest` — 将决策编译成可操作的规则表
   - `/architecture-review` — 验证架构覆盖范围
   **预生产阶段：**
   - `/ux-design` — 作者 UX 关键屏幕规范（主菜单、HUD、核心交互）
   - `/prototype` — 构建一次性原型来验证核心机制
   - `/playtest-report (×1+)` — 记录每个垂直切片游戏测试会话
   - `/create-epics` — 将系统映射到史诗
   - `/create-stories` — 将史诗分解为可实施的故事
   - `/sprint-plan` — 计划第一个冲刺
   **生产阶段：** → 通过 `/dev-story` 获取故事

#### 如果 D：现有工作

1. 分享您在第一阶段的发现：
   - “我可以看到你有 [X source files / Y design docs / Z prototypes]...”
   - “你的引擎是 [configured as X / not yet configured]...”

2. **子案例 D1 — 早期阶段**（引擎未配置或仅存在游戏概念）：
   - 如果未配置引擎，首先推荐 `/setup-engine`
   - 然后 `/project-stage-detect` 为缺口库存

   **子案例 D2 — GDD、ADR 或故事已存在：**
   - 解释一下：“拥有文件与模板能够使用它们的技能不同。GDD 可能会缺少必需的部分。`/adopt` 会专门检查这一点。”
   - Recommend:
     1. `/project-stage-detect` — 了解哪个阶段以及完全缺少什么
     2. `/adopt` — 审核现有工件是否采用正确的内部格式

3. 显示 D2 的推荐路径：
   - `/project-stage-detect` — 相位检测 + 存在间隙
   - `/adopt` — 格式合规性审核 + 迁移计划
   - `/setup-engine` — 如果未配置引擎
   - `/design-system retrofit [path]` — 填充缺失的 GDD 部分
   - `/architecture-decision retrofit [path]` — 添加缺失的 ADR 部分
   - `/architecture-review` — 引导 TR 要求注册表
   - `/gate-check` — 验证下一阶段的准备情况

---

## 第 3b 阶段：设置审核模式

检查 `production/review-mode.txt` 是否已存在。

**如果存在**：Read 它并显示当前模式 — “审阅模式设置为 `[current]`。” — 然后进入第 4 阶段。不要再问。

**如果不存在**：使用`AskUserQuestion`：

- **提示**：“一种设置选择：在完成工作流程时您希望进行多少设计审查？”
- **Options**:
  - `Full` — 主管专家在每个关键工作流程步骤进行审查。最适合团队、学习工作流程或当您需要对每个决定进行全面反馈时。
  - `Lean (recommended)` — 仅在相门转换时使用导向器 (/gate-check)。跳过每项技能的评论。适合单独开发者和小团队的平衡方法。
  - `Solo` — 根本没有导演评论。最大速度。最适合游戏即兴创作、原型制作，或者如果评论感觉过于繁琐。

Write 用户选择后立即改为 `production/review-mode.txt`
选择 — 没有单独的“我可以写吗？”需要，因为写入是直接的
选择的结果：
- `Full` → 写入 `full`
- `Lean (recommended)` → 写入 `lean`
- `Solo` → 写入 `solo`

如果 `production/` 目录不存在，则创建该目录。

---

## 第 4 阶段：继续之前确认

呈现推荐路径后，使用 `AskUserQuestion` 询问用户想要首先执行哪一步。永远不要自动运行下一个技能。

- **提示**：“您想从 [recommended first step] 开始吗？”
- **Options**:
  - `Yes, let's start with [recommended first step]`
  - `I'd like to do something else first`

---

## 第五阶段：交接

当用户确认下一步时，用一条短线进行响应：“键入 `[skill command]` 开始。”没有别的了。不要重新解释技能或添加鼓励。 `/start` 技能的工作已完成。

结论：**完成**——以用户为导向并移交给下一步。

---

## 边缘情况

- **用户选择 D 但项目是空的**：轻轻重定向 — “看起来该项目是一个新模板，还没有任何工件。路径 A 或 B 会更适合吗？”
- **用户选择 A 但项目有代码**：提及您发现的内容 - “我注意到 `src/` 中已经有代码。您是否打算选择 D（现有工作）？”
- **用户正在返回（引擎已配置，概念存在）**：完全跳过入门 - “看起来您已经设置完毕！您的引擎是 [X]，您在 `design/gdd/game-concept.md` 上有一个游戏概念。审阅模式：`[read from production/review-mode.txt, or 'lean (default)' if missing]`。想从您上次停下的地方继续吗？尝试 `/sprint-plan` 或告诉我您想要什么继续工作。”
- **用户不适合任何选项**：让他们用自己的话描述自己的情况并适应。

---

## 协作协议

1. **先询问**——永远不要假设用户的状态或意图
2. **提出选项** — 给出明确的路径，而不是强制要求
3. **用户决定**——他们选择方向
4. **不自动执行** — 推荐下一个技能，不要在没有询问的情况下运行它
5. **适应** — 如果用户的情况不适合模板，请倾听并调整
