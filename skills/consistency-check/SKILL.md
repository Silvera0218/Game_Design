---
name: consistency-check
description: "根据实体注册表扫描所有 GDD，以检测跨文档不一致：具有不同统计数据的同一实体、具有不同值的同一项目、具有不同变量的相同公式。 Grep-first 方法 — 读取注册表，然后仅针对冲突的 GDD 部分，而不是读取完整文档。"
---

# 一致性检查

通过将所有 GDD 与
实体注册表（`design/registry/entities.yaml`）。使用 grep-first 方法：
读取注册表一次，然后仅针对提到的 GDD 部分
注册名称——除非需要调查冲突，否则不会读取完整文件。

**此技能是写入时安全网。** 它捕获了 `/design-system` 的内容
每个部分的检查可能会遗漏，`/review-all-gdds` 的整体审查是什么
赶得太晚了。

**何时运行：**
- 写入每个新的 GDD 后（移动到下一个系统之前）
- 在 `/review-all-gdds` 之前（以便技能从干净的基线开始）
- 在 `/create-architecture` 之前（不一致会毒害下游 ADR）
- 按需：`/consistency-check entity:[name]`专门检查一个实体

**输出：** 冲突报告+可选的注册表更正

---

## 第 1 阶段：解析参数并加载注册表

**Modes:**
- 无参数 / `full` — 根据所有 GDD 检查所有注册条目
- `since-last-review` — 仅检查自上次审核报告以来修改的 GDD
- `entity:<name>` — 检查所有 GDD 中的一个特定实体
- `item:<name>` — 检查所有 GDD 中的一项特定项目

**加载注册表：**

```
Read path="design/registry/entities.yaml"
```

如果文件不存在或没有条目：
> “实体注册表为空。运行 `/design-system` 写入 GDD — 注册表
> 每个 GDD 完成后自动填充。还没有什么可检查的。”

停止并退出。

从注册表中构建四个查找表：
- **实体_地图**：`{ name → { source, attributes, referenced_by } }`
- **项目地图**：`{ name → { source, value_gold, weight, ... } }`
- **公式_映射**：`{ name → { source, variables, output_range } }`
- **constant_map**：`{ name → { source, value, unit } }`

计算注册条目总数。报告：
```
Registry loaded: [N] entities, [N] items, [N] formulas, [N] constants
Scope: [full | since-last-review | entity:name]
```

---

## 第 2 阶段：找到范围内的 GDD

```
Glob pattern="design/gdd/*.md"
```

排除：`game-concept.md`、`systems-index.md`、`game-pillars.md` — 这些是
不是系统 GDD。

对于 `since-last-review` 模式：
```bash
git log --name-only --pretty=format: -- design/gdd/ | grep "\.md$" | sort -u
```
自最新 `design/gdd/gdd-cross-review-*.md` 以来修改的 GDD 限制
文件的创建日期。

扫描前报告范围内的 GDD 列表。

---

## 第 3 阶段：Grep - 首次冲突扫描

对于每个注册条目，grep 每个范围内的 GDD 以获取该条目的名称。
不要进行完整读取——仅提取匹配的行及其立即数
上下文（-C 3 行）。

这是核心优化：而不是每次读取 10 个 GDD × 400 行
（4,000 行），您 grep 50 个实体名称 × 10 GDD（50 个有针对性的搜索，
每次点击都会返回约 10 行）。

### 3a：实体扫描

对于entity_map中的每个实体：

```
Grep pattern="[entity_name]" glob="design/gdd/*.md" output_mode="content" -C 3
```

对于每个 GDD 命中，提取实体名称附近提到的值：
- 任何数字属性（计数、成本、持续时间、范围、费率）
- 任何分类属性（类型、层级、类别）
- 任何派生值（总计、输出、结果）
- 在entity_map中注册的任何其他属性

将提取的值与注册表项进行比较。

**冲突检测：**
- 注册表显示 `[entity_name].[attribute] = [value_A]`。 GDD 表示 `[entity_name] has [value_B]`。 → **冲突**
- 注册表显示 `[item_name].[attribute] = [value_A]`。 GDD 表示 `[item_name] is [value_B]`。 → **冲突**
- GDD 提到了 `[entity_name]` 但未指定该属性。 → **注意**（没有冲突，只是无法验证）

### 3b：物品扫描

对于 item_map 中的每个项目，grep 查找该项目名称的所有 GDD。摘录：
- 卖出价/价值/黄金价值
- weight
- 堆叠规则（可堆叠/不可堆叠）
- category

与注册表项值进行比较。

### 3c：公式扫描

对于 Formula_map 中的每个公式，grep 公式名称的所有 GDD。摘录：
- 公式附近提到的变量名称
- 提到的输出范围或上限值

与注册表项进行比较：
- 不同的变量名称 → **冲突**
- 输出范围有不同说明 → **冲突**

### 3d：持续扫描

对于constant_map中的每个常量，grep所有GDD以查找常量名称。摘录：
- 常量名称附近提到的任何数值

与注册表值比较：
- 不同的数字 → **冲突**

---

## 第 4 阶段：深入调查（仅限冲突）

对于第 3 阶段中发现的每个冲突，有针对性地进行全节阅读
冲突 GDD 以获得精确的上下文：

```
Read path="design/gdd/[conflicting_gdd].md"
```
（或者如果文件很大，则使用具有更广泛上下文的 Grep）

通过完整的上下文确认冲突。确定：
1. **哪个 GDD 是正确的？** 检查注册表中的 `source:` 字段 —
   来源GDD是权威所有者。任何其他与其相矛盾的 GDD
   是需要更新的。
2. **注册表本身是否已过时？** 如果源 GDD 在之后更新
   注册表项已写入（检查 git 日志），注册表可能已过时。
3. **这是真正的设计变更吗？** 如果冲突代表有意为之
   设计决策，解决方案是：更新源码GDD，更新注册表，
   然后修复所有其他 GDD。

对于每个冲突，进行分类：
- **🔴冲突** — 名称相同但值不同的 entity/item/formula/constant
  在不同的 GDD 中。必须在架构开始之前解决。
- **⚠️ STALE REGISTRY** — 源 GDD 值已更改，但注册表未更新。
  注册表需要更新；其他 GDD 可能已经是正确的。
- **ℹ️ 无法验证** — 提到了实体，但没有说明可比较的属性。
  不是冲突；只是注意参考。

---

## 第五阶段：输出报告

```
## Consistency Check Report
Date: [date]
Registry entries checked: [N entities, N items, N formulas, N constants]
GDDs scanned: [N] ([list names])

---

### Conflicts Found (must resolve before architecture)

🔴 [Entity/Item/Formula/Constant Name]
   Registry (source: [gdd]): [attribute] = [value]
   Conflict in [other_gdd].md: [attribute] = [different_value]
   → Resolution needed: [which doc to change and to what]

---

### Stale Registry Entries (registry behind the GDD)

⚠️ [Entry Name]
   Registry says: [value] (written [date])
   Source GDD now says: [new value]
   → Update registry entry to match source GDD, then check referenced_by docs.

---

### Unverifiable References (no conflict, informational)

ℹ️ [gdd].md mentions [entity_name] but states no comparable attributes.
   No conflict detected. No action required.

---

### Clean Entries (no issues found)

✅ [N] registry entries verified across all GDDs with no conflicts.

---

Verdict: PASS | CONFLICTS FOUND
```

**Verdict:**
- **通过** — 没有冲突。注册管理机构和 GDD 就所有检查值达成一致。
- **发现冲突** — 检测到一个或多个冲突。列出解决步骤。

---

## 第 6 阶段：注册表更正

如果发现过时的注册表项，请询问：
> “我可以更新 `design/registry/entities.yaml` 来修复 [N] 过时的条目吗？”

对于每个陈旧条目：
- 更新 `value`/属性字段
- 将 `revised:` 设置为今天的日期
- 添加带有旧值的 YAML 注释：`# was: [old_value] before [date]`

如果在 GDD 中发现注册表中没有的新条目，请询问：
> “发现 GDD 中提到的 [N] entities/items 尚未在注册表中。
> 我可以将它们添加到 `design/registry/entities.yaml` 吗？”

仅添加出现在多个 GDD 中的条目（真正的跨系统事实）。

**切勿删除注册表项。** 如果删除了注册表项，则设置 `status: deprecated`
来自所有 GDD。

写入后：结论：**完成** - 一致性检查完成。
如果冲突仍未解决：结论：**已阻止** — [N] 冲突需要在架构开始之前手动解决。

### 6b：附加到反射日志

如果发现任何🔴冲突条目（无论是否已解决），
对于每个冲突，将一个条目附加到 `docs/consistency-failures.md`：

```markdown
### [YYYY-MM-DD] — /consistency-check — 🔴 CONFLICT
**Domain**: [system domain(s) involved]
**Documents involved**: [source GDD] vs [conflicting GDD]
**What happened**: [specific conflict — entity name, attribute, differing values]
**Resolution**: [how it was fixed, or "Unresolved — manual action needed"]
**Pattern**: [generalised lesson, e.g. "Item values defined in combat GDD were not
referenced in economy GDD before authoring — always check entities.yaml first"]
```

仅当 `docs/consistency-failures.md` 存在时才附加。如果文件丢失，
默默地跳过此步骤 - 不要通过此技能创建文件。

---

## 下一步

- **如果通过**：运行 `/review-all-gdds` 进行整体设计理论审查，或者
  `/create-architecture`（如果所有 MVP GDD 均已完成）。
- **如果发现冲突**：修复标记的 GDD，然后重新运行
  `/consistency-check` 确认分辨率。
- **如果注册表陈旧**：更新注册表（第 6 阶段），然后重新运行以验证。
- 编写每个新的 GDD 后运行 `/consistency-check` 以尽早发现问题，
  不是在架构时间。
