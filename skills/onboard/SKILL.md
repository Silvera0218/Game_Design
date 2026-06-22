---
name: onboard
description: "为加入项目的新贡献者或代理生成上下文入职文档。总结与指定角色或领域相关的项目状态、架构、约定和当前优先级。"
---

## 第 1 阶段：加载项目上下文

Read AGENTS.md 用于项目概述和标准。

Read 如果指定了特定角色，则来自 `.codex/agents/` 的相关代理定义。

---

## 第 2 阶段：扫描相关区域

- 对于程序员：扫描 `client/Assets/Scripts/` 以获取架构、模式、关键文件
- 对于设计师：扫描 `design/` 获取现有设计文档
- 对于叙述：扫描 `design/narrative/` 获取世界构建和故事文档
- 对于 QA：扫描 `client/Assets/Tests/` 和 `server/tests/` 以获取现有测试覆盖范围
- 对于生产：扫描 `production/` 以获取当前的冲刺和里程碑

Read 最近的更改（git log 如果可用）以了解当前的势头。

---

## 第 3 阶段：生成入职文档

```markdown
# Onboarding: [Role/Area]

## Project Summary
[2-3 sentence summary of what this game is and its current state]

## Your Role
[What this role does on this project, key responsibilities, who you report to]

## Project Architecture
[Relevant architectural overview for this role]

### Key Directories
| Directory | Contents | Your Interaction |
|-----------|----------|-----------------|

### Key Files
| File | Purpose | Read Priority |
|------|---------|--------------|

## Current Standards and Conventions
[Summary of conventions relevant to this role from AGENTS.md and agent definition]

## Current State of Your Area
[What has been built, what is in progress, what is planned next]

## Current Sprint Context
[What the team is working on now and what is expected of this role]

## Key Dependencies
[What other roles/systems this role interacts with most]

## Common Pitfalls
[Things that trip up new contributors in this area]

## First Tasks
[Suggested first tasks to get oriented and productive]

1. [Read these documents first]
2. [Review this code/content]
3. [Start with this small task]

## Questions to Ask
[Questions the new contributor should ask to get fully oriented]
```

---

## 第四阶段：保存文档

向用户呈现入职文档。

问：“我可以把这个写到 `production/onboarding/onboard-[role]-[date].md` 吗？”

如果是，则写入文件，并根据需要创建目录。

---

## 第五阶段：后续步骤

结论：**完成** — 已生成入职文档。

- 在第一次会议之前与新贡献者分享入职文档。
- 运行 `/sprint-status` 以显示新贡献者当前进度。
- 如果贡献者需要有关下一步工作的指导，请运行 `/help`。
