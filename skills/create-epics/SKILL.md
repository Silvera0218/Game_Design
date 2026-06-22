---
name: create-epics
description: "将批准的 GDD + 架构转化为史诗 - 每个架构模块一个史诗。定义范围、管理 ADR、引擎风险和未追踪的要求。不会分解故事 - 创建每个史诗后运行 /create-stories [epic-slug]。"
---

# 创造史诗

史诗是映射到一个架构模块的命名的、有界的作品体。
它定义了**需要构建什么**以及**谁在架构上拥有它**。它
不规定实施步骤——这是故事的工作。

**当您在开发过程中接近该层时，**每层运行一次此技能**。
在核心接近完成之前，不要创建功能层史诗 - 设计
将会改变。

**输出：** `production/epics/[epic-slug]/EPIC.md` + `production/epics/index.md`

**每部史诗之后的下一步：** `/create-stories [epic-slug]`

**何时运行：** `/create-control-manifest` 和 `/architecture-review` 通过后。

---

## 1. 解析参数

解决审查模式（一次，存储本次运行的所有门生成）：
1. 如果 `--review [完整|lean|独奏]`已通过→使用
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认为 `lean`

有关完整检查模式，请参阅 `.codex/docs/director-gates.md`。

**Modes:**
- `/create-epics all` — 按层顺序处理所有系统
- `/create-epics layer: foundation` — 仅基础层
- `/create-epics layer: core` — 仅核心层
- `/create-epics layer: feature` — 仅要素层
- `/create-epics layer: presentation` — 仅表示层
- `/create-epics [system-name]` — 一个特定系统
- 没有争论——问：“你想为哪个层或系统创建史诗？”

---

## 2. 负载输入

### 步骤 2a — 摘要扫描（快速）

在完整阅读任何内容之前，Grep 的所有 GDD 的 `## Summary` 部分：

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 5
```

对于 `layer:` 或 `[system-name]` 模式：基于以下条件仅筛选范围内的 GDD：
摘要快速参考。跳过全文阅读任何超出范围的内容。

### 步骤 2b — 完整文档加载（仅限范围内的系统）

使用步骤 2a grep 结果确定哪些系统在范围内。 Read 完整文档**仅适用于范围内的系统** — 不要阅读范围外系统或层的 GDD 或 ADR。

Read 适用于范围内的系统：

- `design/gdd/systems-index.md` — 权威系统列表、层、优先级
- 仅限范围内的 GDD（已批准或设计状态，按步骤 2a 结果过滤）
- `docs/architecture/architecture.md` — 模块所有权和 API 边界
- 接受的 ADR **其域仅涵盖范围内的系统** — 阅读“GDD 已解决的要求”、“决策”和“引擎兼容性”部分；跳过不相关域的 ADR
- `docs/architecture/control-manifest.md` — 标头中的清单版本日期
- `docs/architecture/tr-registry.yaml` — 用于跟踪 ADR 覆盖范围的要求
- `docs/engine-reference/[engine]/VERSION.md` — 引擎名称、版本、风险级别

报告：“已加载 [N] GDD、[M] ADR，引擎：[名称 + 版本]。”

---

## 3. 处理订单

按照依赖安全层顺序进行处理：
1. **基础**（无依赖项）
2. **核心**（取决于基础）
3. **功能**（取决于核心）
4. **演示**（取决于功能 + 核心）

在每一层中，使用 `systems-index.md` 中的顺序。

---

## 4. 定义每个史诗

对于每个系统，将其映射到 `architecture.md` 中的架构模块。

根据 TR 注册表检查 ADR 覆盖范围：
- **跟踪的要求**：包含已接受的 ADR 的 TR-ID
- **未追踪的要求**：没有 ADR 的 TR-ID — 在继续之前发出警告

在编写任何内容之前向用户展示：

```
## Epic: [System Name]

**Layer**: [Foundation / Core / Feature / Presentation]
**GDD**: design/gdd/[filename].md
**Architecture Module**: [module name from architecture.md]
**Governing ADRs**: [ADR-NNNN, ADR-MMMM]
**Engine Risk**: [LOW / MEDIUM / HIGH — highest risk among governing ADRs]
**GDD Requirements Covered by ADRs**: [N / total]
**Untraced Requirements**: [list TR-IDs with no ADR, or "None"]
```

如果有未追踪的需求：
> “⚠️[N]要求[system]中没有ADR。可以创建史诗，但是
> 在 ADR 存在之前，满足这些要求的故事将被标记为“已阻止”。
> 首先运行 `/architecture-decision`，或使用占位符继续。”

问：“我要创建史诗：[name]吗？”
选项：“是的，创建它”、“跳过”、“暂停 - 我需要先写 ADR”

---

## 4b.制作人史诗结构之门

**审查模式检查** — 在生成 PR-EPIC 之前应用：
- `solo` → 跳过。注意：“PR-EPIC 已跳过 — 单人模式。”继续执行步骤 5（写入史诗文件）。
- `lean` → 跳过（不是相位门）。注意：“PR-EPIC 已跳过 — 精益模式。”继续执行步骤 5（写入史诗文件）。
- `full` → 正常生成。

定义当前层的所有史诗后（对所有范围内的系统完成步骤 4），并在写入任何文件之前，使用门 **PR-EPIC** (`.codex/docs/director-gates.md`) 通过 Task 生成 `producer`。

通过：完整的史诗结构摘要（所有史诗、其范围摘要、管理 ADR 计数）、正在处理的层、里程碑时间表和团队能力。

介绍制作人的评价。如果不现实，请在写作之前修改史诗边界（拆分超出范围的史诗或合并范围不足的史诗）。如果有疑虑，请将其提出并让用户决定。在生产者门解决之前，不要写入史诗文件。

---

## 5.Write史诗文件

批准后，询问：“我可以将史诗文件写入`production/epics/[epic-slug]/EPIC.md`吗？”

用户确认后，写入：

### `production/epics/[epic-slug]/EPIC.md`

```markdown
# Epic: [System Name]

> **Layer**: [Foundation / Core / Feature / Presentation]
> **GDD**: design/gdd/[filename].md
> **Architecture Module**: [module name]
> **Status**: Ready
> **Stories**: Not yet created — run `/create-stories [epic-slug]`

## Overview

[1 paragraph describing what this epic implements, derived from the GDD Overview
and the architecture module's stated responsibilities]

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|-----------------|-------------|
| ADR-NNNN: [title] | [1-line summary] | LOW/MEDIUM/HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-[system]-001 | [requirement text from registry] | ADR-NNNN ✅ |
| TR-[system]-002 | [requirement text] | ❌ No ADR |

## Definition of Done

This epic is complete when:
- All stories are implemented, reviewed, and closed via `/story-done`
- All acceptance criteria from `design/gdd/[filename].md` are verified
- All Logic and Integration stories have passing test files in `tests/`
- All Visual/Feel and UI stories have evidence docs with sign-off in `production/qa/evidence/`

## Next Step

Run `/create-stories [epic-slug]` to break this epic into implementable stories.
```

### 更新`production/epics/index.md`

创建或更新主索引：

```markdown
# Epics Index

Last Updated: [date]
Engine: [name + version]

| Epic | Layer | System | GDD | Stories | Status |
|------|-------|--------|-----|---------|--------|
| [name] | Foundation | [system] | [file] | Not yet created | Ready |
```

---

## 6. 登机口提醒

为所请求的范围编写所有史诗后：

- **基础 + 核心完成**：这些是预制作所必需的 →
  生产门。运行 `/gate-check production` 以检查准备情况。
- **提醒**：史诗定义范围。故事定义了实施步骤。运行
  `/create-stories [epic-slug]` 为每个史诗，然后开发人员可以开始工作。

---

## 协作协议

1. **一次一个史诗** - 在要求创建它之前呈现每个史诗定义
2. **警告差距** - 在继续之前标记未跟踪的需求
3. **写入前询问** — 在写入任何文件之前经过每个史诗的批准
4. **无发明** — 所有内容均来自 GDD、ADR 和架构文档
5. **永远不要创造故事**——这项技能仅限于史诗级别

处理完所有请求的史诗后：

- **结论：完整** — [N] 史诗已编写。每个史诗运行 `/create-stories [epic-slug]`。
- **判决：被阻止** - 用户拒绝所有史诗，或者找不到符合条件的系统。
