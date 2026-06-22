---
name: propagate-design-change
description: "当修改 GDD 时，扫描所有 ADR 和可追溯性索引，以识别哪些架构决策现在可能已过时。生成变更影响报告并指导用户解决问题。"
---

# 传播设计变更

当 GDD 发生变化时，针对它编写的架构决策可能不再有效
有效的。此技能找到每个受影响的 ADR，将 ADR 的假设与进行比较
GDD 现在所说的内容，并指导用户解决问题。

**用途：** `/propagate-design-change design/gdd/combat-system.md`

---

## 1. 验证论点

GDD 路径参数是**必需的**。如果丢失，则失败并显示：
> ”用途：`/propagate-design-change design/gdd/[system].md`
> 提供已更改的 GDD 的路径。”

验证文件是否存在。如果没有，则失败：
> “未找到 [path]。检查路径并重试。”

---

## 2. Read 变更后的 GDD

Read 为当前 GDD 的完整版本。

---

## 3. Read 之前版本

运行 git 获取之前提交的版本：

```bash
git show HEAD:design/gdd/[filename].md
```

如果文件没有git历史记录（新文件），报告：
> “git 中没有以前的版本 - 这似乎是新的 GDD，而不是修订版。
> 没什么可宣传的。”

如果 git 返回以前的版本，请进行概念性比较：
- 识别已更改的部分（新规则、删除的规则、修改的公式、
  改变了验收标准，改变了调谐旋钮）
- 识别未更改的部分
- 生成变更摘要：

```
## Change Summary: [GDD filename]
Date of revision: [today]

Changed sections:
- [Section name]: [what changed — new rule, removed rule, formula modified, etc.]

Unchanged sections:
- [Section name]

Key changes affecting architecture:
- [Change 1 — likely to affect ADRs]
- [Change 2]
```

---

## 4. 加载架构输入

Read `docs/architecture/` 中的所有 ADR：
- 对于每个 ADR，读取完整文件
- 提取“GDD 已解决的要求”表
- 请注意每个 ADR 引用了哪些 GDD 文档和要求 ID

Read `docs/architecture/architecture-traceability.md`（如果存在）。

报告：“已加载 [N] ADR。[M] 参考 [gdd filename]。”

---

## 5.影响分析

对于引用更改后的 GDD 的每个 ADR：

将 ADR 的“GDD 已解决的要求”条目与更改的部分进行比较
GDD 的。对于每个引用的要求：

1. **在当前的 GDD 中找到需求** — 它仍然存在吗？
2. **比较**：ADR 编写时的 GDD 与现在的内容有何不同？
3. **评估 ADR 决策**：架构决策仍然有效吗？

将每个受影响的 ADR 分类为以下之一：

| Status | Meaning |
|--------|---------|
| ✅ **仍然有效** | GDD 的更改不会影响 ADR 的决定 |
| ⚠️ **需要审查** | GDD 的更改可能会影响此 ADR — 需要人工判断 |
| 🔴 **可能被取代** | GDD 的更改直接与 ADR 的假设相矛盾 |

对于每个受影响的 ADR，生成一个影响条目：

```
### ADR-NNNN: [title]
Status: [Still Valid / Needs Review / Likely Superseded]

What the ADR assumed about this GDD:
  "[relevant quote from the ADR's GDD Requirements Addressed section]"

What the GDD now says:
  "[relevant quote from the current GDD]"

Assessment:
  [Explanation of whether the ADR decision is still valid, and why]

Recommended action:
  [Keep as-is | Review and update | Mark Superseded and write new ADR]
```

---

## 6. 提交影响报告

在要求采取任何操作之前，向用户提供完整的影响报告。格式：

```
## Design Change Impact Report
GDD: [filename]
Date: [today]
Changes detected: [N sections changed]
ADRs referencing this GDD: [M]

### Not Affected
[ADRs referencing this GDD whose decisions remain valid]

### Needs Review ([count])
[ADRs that may need updating]

### Likely Superseded ([count])
[ADRs whose assumptions are now contradicted]
```

---

## 6b. Director Gate — 技术影响审查

**审查模式检查** — 在生成 TD-CHANGE-IMPACT 之前应用：
- `solo` → 跳过。注意：“TD-CHANGE-IMPACT 已跳过 — 单人模式。”进入第 7 阶段。
- `lean` → 跳过。注意：“跳过 TD-CHANGE-IMPACT — 精益模式。”进入第 7 阶段。
- `full` → 正常生成。

使用门 **TD-CHANGE-IMPACT** (`.codex/docs/director-gates.md`) 通过 Task 生成 `technical-director`。

通过：第 6 阶段的完整设计变更影响报告（变更摘要、所有受影响的 ADR 及其仍然有效/需要审查/可能被取代的分类以及建议的行动）。

技术总监审查是否：
- 影响分类正确（没有 ADR 分类不足）
- 建议的操作在架构上是合理的
- 对其他 ADR 或系统的任何连锁效应都被忽略了

执行判决：
- **批准** → 继续进行第 7 阶段解决工作流程
- **担忧** → 提出标记的具体 ADR 或建议；使用 `AskUserQuestion` 和选项：`Revise the impact assessment` / `Accept with noted concerns` / `Discuss further`
- **拒绝** → 不进行解决；在继续之前重新分析影响

---

## 7. 解决工作流程

对于每个标记为“需要审核”或“可能被取代”的 ADR，询问用户该怎么做：

依次询问每个 ADR：
> “ADR-NNNN ([title]) — [status]。您想做什么？”
> Options:
> -“Mark Superseded（我将编写新的 ADR）”— 将 ADR 状态行更新为 `Superseded by: [pending]`
> - “就地更新（小修订）”— 打开 ADR 进行编辑；注意要修改的内容
> - “保持原样（更改实际上并不影响此决定）”
> - “暂时跳过（稍后再看）”

对于标记为**取代**的 ADR：
- 更新 ADR 的状态字段：`Superseded by ADR-[next number] (pending — see change-impact-[date]-[system].md)`
- 问：“我可以更新 [ADR filename] 中的状态吗？”

---

## 8.更新追溯索引

如果 `docs/architecture/architecture-traceability.md` 存在：
- 将更改后的 GDD 要求添加到“取代的要求”表中：

```markdown
## Superseded Requirements
| Date | GDD | Requirement | Changed To | ADRs Affected | Resolution |
|------|-----|-------------|------------|---------------|------------|
| [date] | [gdd] | [old requirement text] | [new requirement text] | ADR-NNNN | [Superseded/Updated/Valid] |
```

问：“我可以更新追溯索引吗？”

---

## 9. 输出变更影响文件

问：“我可以将变更影响报告写入 `docs/architecture/change-impact-[date]-[system-slug].md` 吗？”

该文件包含：
- 步骤 3 的变更摘要
- 第 5 步的完整影响分析
- 第 7 步中做出的决议决定
- 需要编写或更新的 ADR 列表

如果用户批准：结论：**完成** — 更改影响报告已保存。
如果用户拒绝：判决：**被阻止** - 用户拒绝写入。

---

## 10. 后续行动

根据决议决定，建议：

- **ADR 标记为已取代**：“运行 `/architecture-decision [title]` 来写入
  更换 ADR。然后重新运行 `/propagate-design-change` 以验证覆盖范围。”
- **要就地更新的 ADR**：列出每个 ADR 中要更新的特定字段
- **如果许多 ADR 受到影响**：“更新所有 ADR 后运行 `/architecture-review`
验证完整的可追溯性矩阵仍然是一致的。”

---

## 协作协议

1. **Read 默默** - 在呈现任何内容之前计算全部影响
2. **首先显示完整报告** — 让用户在要求采取行动之前查看范围
3. **按照 ADR 询问** — 不要批量决策；每个受影响的 ADR 可能需要不同的治疗
4. **写入前询问** — 修改任何文件之前始终确认
5. **非破坏性** — 永远不会删除 ADR 内容；仅添加“取代”注释
