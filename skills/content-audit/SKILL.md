---
name: content-audit
description: "审核 GDD 指定的内容对已实施的内容进行计数。确定计划内容与已构建内容。"
---

当该技能被调用时：

解析论证：
- 没有争议 → 对所有系统进行全面审计
- `[system-name]` → 仅审核单个系统
- `--summary` → 仅汇总表，无文件写入

---

## 第一阶段 — 背景收集

1. **Read `design/gdd/systems-index.md`** 获取完整的系统列表、其
   类别和 MVP/priority 层。

2. **L0 预扫描**：在完全读取任何 GDD 之前，Grep 的所有 GDD 文件
   `## Summary` 部分以及常见的内容计数关键字：
   ```
   Grep pattern="(## Summary|N enemies|N levels|N items|N abilities|enemy types|item types)" glob="design/gdd/*.md" output_mode="files_with_matches"
   ```
   对于单系统审核：跳过此步骤，直接阅读全文。
   对于完整审核：仅完整读取与内容计数关键字匹配的 GDD。
没有内容计数语言的 GDD（纯机制 GDD）被标记为
   如果没有完整阅读，“没有可审核的内容”。

3. **完全读取范围内的 GDD 文件**（或者单个系统 GDD，如果系统
   名字已给出）。

4. **对于每个 GDD，提取显式内容计数或列表。** 查找模式
   like:
   - “N 个敌人”/“敌人类型：”/已命名的敌人列表
   - “N个关卡”/“N个区域”/“N个地图”/“N个阶段”
   - “N件物品”/“N件武器”/“N件装备”
   - “N种能力”/“N种技能”/“N种法术”
   - “N个对话场景”/“N个对话”/“N个过场动画”
   - “N 个任务”/“N 个任务”/“N 个目标”
   - 任何显式枚举列表（命名内容片段的项目符号列表）

4. **根据提取的数据构建内容清单表**：

   | System | 内容类型 | 指定 Count/List | 来源 GDD |
   |--------|-------------|---------------------|------------|

   注意：如果 GDD 定性描述内容但未给出计数，请记录
   “未指定”并标记它——未指定的计数是一个值得注意的设计差距。

---

## 第 2 阶段 — 实施扫描

对于第 1 阶段中找到的每种内容类型，扫描相关目录进行计数
已实施什么。使用 Glob 和 Grep 定位文件。

**关卡/区域/地图：**
- Glob `assets/**/*.tscn`、`assets/**/*.unity`、`assets/**/*.umap`
- Glob `src/**/*.tscn`, `src/**/*.unity`
- 在名为 `levels/`、`areas/`、`maps/` 的子目录中查找场景文件，
  `worlds/`、`stages/`
- 计算看似 level/scene 定义的唯一文件（不是 UI 场景）

**敌人/角色/NPC：**
- Glob `assets/data/**/enemies/**`, `assets/data/**/characters/**`
- Glob `src/**/enemies/**`, `src/**/characters/**`
- 查找定义实体统计信息的 `.json`、`.tres`、`.asset`、`.yaml` 数据文件
- 在角色子目录中查找 scene/prefab 文件

**物品/设备/战利品：**
- Glob `assets/data/**/items/**`, `assets/data/**/equipment/**`,
  `assets/data/**/loot/**`
- 查找 `.json`、`.tres`、`.asset` 数据文件

**能力/技能/法术：**
- Glob `assets/data/**/abilities/**`, `assets/data/**/skills/**`,
  `assets/data/**/spells/**`
- 查找 `.json`、`.tres`、`.asset` 数据文件

**对话/对话/过场动画：**
- Glob `assets/**/*.dialogue`、`assets/**/*.csv`、`assets/**/*.ink`
- Grep 用于 `assets/data/` 中的对话数据文件

**任务/任务：**
- Glob `assets/data/**/quests/**`、`assets/data/**/missions/**`
- 查找`.json`、`.yaml`定义文件

**发动机特定注释（在报告中确认）：**
- 计数是近似值——该技能无法完美解析每个引擎
格式化仅限编辑器的文件或将其与附带的内容区分开
- 场景文件可能包括游戏内容和 system/UI 场景；扫描
  计算所有匹配并记录此警告

---

## 第三阶段——差距报告

生成间隙表：

```
| System | Content Type | Specified | Found | Gap | Status |
|--------|-------------|-----------|-------|-----|--------|
```

**状态类别：**
- `COMPLETE` — 发现 ≥ 指定 (100%+)
- `IN PROGRESS` — 发现值为指定值的 50–99%
- `EARLY` — 发现值为指定值的 1–49%
- `NOT STARTED` — 找到的是 0

**优先级标志：**
如果出现以下情况，则在报告中将系统标记为 `HIGH PRIORITY`：
- 状态为 `NOT STARTED` 或 `EARLY`，并且
- 该系统在系统索引中被标记为 MVP 或垂直切片，或者
- 系统索引显示系统正在阻塞下游系统

**总结行：**
- 指定的总内容项（所有指定列值的总和）
- 找到的内容项总数（所有“找到”列值的总和）
- 总体间隙百分比：`(Specified - Found) / Specified * 100`

---

## 第四阶段——输出

### 全面审核和单系统模式

向用户呈现差距表和摘要。问：“我可以写完整的报告给 `docs/content-audit-[YYYY-MM-DD].md` 吗？”

如果是，则写入文件：

```markdown
# Content Audit — [Date]

## Summary
- **Total specified**: [N] content items across [M] systems
- **Total found**: [N]
- **Gap**: [N] items ([X%] unimplemented)
- **Scope**: [Full audit | System: name]

> Note: Counts are approximations based on file scanning.
> The audit cannot distinguish shipped content from editor/test assets.
> Manual verification is recommended for any HIGH PRIORITY gaps.

## Gap Table

| System | Content Type | Specified | Found | Gap | Status |
|--------|-------------|-----------|-------|-----|--------|

## HIGH PRIORITY Gaps

[List systems flagged HIGH PRIORITY with rationale]

## Per-System Breakdown

### [System Name]
- **GDD**: `design/gdd/[file].md`
- **Content types audited**: [list]
- **Notes**: [any caveats about scan accuracy for this system]

## Recommendation

Focus implementation effort on:
1. [Highest-gap HIGH PRIORITY system]
2. [Second system]
3. [Third system]

## Unspecified Content Counts

The following GDDs describe content without giving explicit counts.
Consider adding counts to improve auditability:
[List of GDDs and content types with "Unspecified"]
```

写完报告后，问：

> “您想针对任何内容差距创建积压故事吗？”

如果是：对于用户选择的每个系统，建议一个故事标题并指出他们
为 `/create-stories [epic-slug]` 或 `/quick-design`，具体取决于间隙的大小。

### --summary mode

直接将差距表和摘要打印到对话中。不要写入文件。
结尾为：“在没有 `--summary` 的情况下运行 `/content-audit` 来编写完整的报告。”

---

## 第五阶段——后续步骤

审核后，建议最高价值的后续行动：

- 如果任何系统带有 `NOT STARTED` 和 MVP 标签 → “运行 `/design-system [name]`
  在实施开始之前，将缺失的内容计数添加到 GDD。”
- 如果总差距 >50% →“运行 `/sprint-plan` 以在即将到来的冲刺中分配内容工作。”
- 如果需要积压故事→“针对每个高优先级差距运行 `/create-stories [epic-slug]`。”
- 如果使用 `--summary` →“运行 `/content-audit`（无标志）将完整报告写入 `docs/`。”

结论：**完成**——内容审核已完成。
