---
name: project-stage-detect
description: "自动分析项目状态、检测阶段、识别差距并根据现有工件推荐后续步骤。当用户询问“我们处于开发阶段”、“我们处于哪个阶段”、“全面项目审核”时使用。"
# Read 仅限诊断技能 — 无需专业代理委派
---

# 项目阶段检测

该技能会扫描您的项目以确定其当前的开发阶段、完整性
的工件和需要注意的差距。它在以下情况下特别有用：
- 从现有项目开始
- 加入代码库
- 检查里程碑之前缺少什么
- 理解“我们在哪里？”

---

## Workflow

### 1. 扫描关键目录

分析项目结构和内容：

**设计文档** (`design/`)：
- 统计 `design/gdd/*.md` 中的 GDD 文件数
- 检查 game-concept.md、game-pillars.md、systems-index.md
- 如果 systems-index.md 存在，则计算总系统与设计系统的数量
- 分析完整性（概述、详细设计、边缘案例等）
- 计算 `design/narrative/` 中的叙述性文档
- `design/levels/` 中的计数级设计

**源代码** (`src/`)：
- 计算源文件数量（与语言无关）
- 识别主要系统（包含 5 个以上文件的目录）
- 检查 core/、gameplay/、ai/、networking/、ui/ 目录
- 估计代码行数（粗略）

**生产工件** (`production/`)：
- 检查活跃的冲刺计划
- 寻找里程碑定义
- 查找路线图文档

**原型** (`prototypes/`)：
- 计算原型目录
- 检查自述文件（已记录与未记录）
- 评估原型是否已存档或处于活动状态

**架构文档** (`docs/architecture/`)：
- 计算 ADR（架构决策记录）
- 检查 overview/index 文档

**测试** (`tests/`)：
- 计算测试文件数
- 估计测试覆盖率（粗略启发式）

### 2. 项目阶段分类

根据扫描的工件，确定阶段。首先检查 `production/stage.txt` —
如果存在，则使用其值（来自 `/gate-check` 的显式覆盖）。否则，
使用这些启发式自动检测（从最先进的向后检查）：

| Stage | Indicators |
|-------|-----------|
| **Concept** | 没有游戏概念文档，头脑风暴阶段 |
| **系统设计** | 游戏概念存在，系统索引缺失或不完整 |
| **技术设置** | 系统索引存在，引擎未配置 |
| **Pre-Production** | 引擎已配置，`client/` 具有 <10 个源文件 |
| **Production** | `client/`有10+源文件，正在积极开发 |
| **Polish** | 仅显式（由 `/gate-check` Production → Polish Gate 设置） |
| **Release** | 仅显式（由 `/gate-check` Polish 设置 → Release Gate） |

### 3. 协作差距识别

**不要** 仅列出丢失的文件。相反，**提出澄清问题**：

- “我看到战斗代码 (`client/Assets/Scripts/Gameplay/Combat/`)，但没有看到 `design/gdd/combat-system.md`。这是首先原型化的，还是我们应该反向记录？”
- “您有 15 个 ADR，但没有架构概述。我应该创建一个来帮助新贡献者吗？”
- “`production/` 中没有冲刺计划。您是否在其他地方（Jira、Trello 等）跟踪工作？”
- “我找到了一个游戏概念，但没有系统索引。您是否已将该概念分解为单独的系统，或者我们应该运行 `/map-systems`？”
- `client/Prototypes/` 目录有 3 个没有 README 的项目。这些是实验，还是需要文档？”

### 4. 生成阶段报告

使用模板：`.codex/docs/templates/project-stage-report.md`

**报告结构**：
```markdown
# Project Stage Analysis

**Date**: [date]
**Stage**: [Concept/Systems Design/Technical Setup/Pre-Production/Production/Polish/Release]
**Stage Confidence**: [PASS — clearly detected / CONCERNS — ambiguous signals / FAIL — critical gaps block progress]

## Completeness Overview
- Design: [X%] ([N] docs, [gaps])
- Code: [X%] ([N] files, [systems])
- Architecture: [X%] ([N] ADRs, [gaps])
- Production: [X%] ([status])
- Tests: [X%] ([coverage estimate])

## Gaps Identified
1. [Gap description + clarifying question]
2. [Gap description + clarifying question]

## Recommended Next Steps
[Priority-ordered list based on stage and role]
```

### 5. 角色过滤推荐（可选）

如果用户提供了角色参数（例如 `/project-stage-detect programmer`）：

**Programmer**:
- 关注架构文档、测试覆盖率、缺失的 ADR
- 代码到文档的差距

**Designer**:
- 关注 GDD 完整性，缺少设计部分
- 原型文档

**Producer**:
- 专注于冲刺计划、里程碑跟踪、路线图
- 跨团队协调文档

**一般**（无作用）：
- 全面审视所有差距
- 跨域的最高优先级项目

### 6. 写作前请求批准

**协作协议**：
```
I've analyzed your project. Here's what I found:

[Show summary]

Gaps identified:
1. [Gap 1 + question]
2. [Gap 2 + question]

Recommended next steps:
- [Priority 1]
- [Priority 2]
- [Priority 3]

May I write the full stage analysis to production/project-stage-report.md?
```

创建文件之前等待用户批准。

---

## 用法示例

```bash
# General project analysis
/project-stage-detect

# Programmer-focused analysis
/project-stage-detect programmer

# Designer-focused analysis
/project-stage-detect designer
```

---

## 后续行动

生成报告后，建议相关的后续步骤：

- **概念存在但没有系统索引？** → `/map-systems` 分解为系统
- **缺少设计文档？** → `/reverse-document design src/[system]`
- **缺少架构文档？** → `/architecture-decision` 或 `/reverse-document architecture`
- **原型需要文档吗？** → `/reverse-document concept prototypes/[name]`
- **没有冲刺计划？** → `/sprint-plan`
- **接近里程碑？** → `/milestone-review`

---

## 协作协议

该技能遵循协作设计原则：

1. **问题第一**：询问差距，不要假设
2. **当前选项**：“我应该创建 X，还是在其他地方跟踪它？”
3. **用户决定**：等待指示
4. **显示草稿**：显示报告摘要
5. **获得批准**：“我可以写信给 production/project-stage-report.md 吗？”

**永远不要**默默地写入文件。 **始终**在创建工件之前展示发现并询问。
