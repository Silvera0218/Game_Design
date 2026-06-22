---
name: skill-improve
description: "使用测试-修复-再测试循环提高技能。运行静态检查，提出有针对性的修复方案，重写技能，重新测试，并根据分数变化保留或恢复。"
---

# 技能提升

对单个技能运行改进循环：
测试→修复→重新测试→保留或恢复。

---

## 第一阶段：解析参数

Read 第一个参数中的技能名称。如果丢失，输出使用情况并停止：

```
Usage: /skill-improve [skill-name]
Example: /skill-improve tech-debt
```

验证 `.codex/skills/[name]/SKILL.md` 是否存在。如果没有，请停止：
“未找到技能‘[name]’。”

---

## 第 2 阶段：基线测试

运行 `/skill-test static [name]` 并记录基线分数：
- 失败次数
- 警告计数
- 哪些具体检查失败（检查 1-7）

向用户显示：
```
Static baseline:   [N] failures, [M] warnings
Failing: Check 4 (no ask-before-write), Check 5 (no handoff)
```

如果基线为 0 个失败和 0 个警告，请记下它并继续到阶段 2b。

### 第 2b 阶段：类别基线

在 `CCGS Skill Testing Framework/catalog.yaml` 中查找技能的 `category:` 字段。

如果没有找到`category:`字段，则显示：
“类别：尚未分配 - 跳过类别检查。”
并跳至第 3 阶段。

如果找到类别，则运行 `/skill-test category [name]` 并记录类别基线：
- 失败次数
- 警告计数
- 哪些特定类别的指标指标失败

向用户显示：
```
Category baseline: [N] failures, [M] warnings  ([category] rubric)
```

如果静态基线和类别基线均为 0 次失败和 0 次警告，则停止：
“这项技能已经通过了所有静态和类别检查。无需改进。”

---

## 第三阶段：诊断

Read 完整技能文件位于 `.codex/skills/[name]/SKILL.md`。

对于每个失败或警告的**静态**检查，确定确切的差距：

- **检查 1 失败** → 缺少 `name` 或 `description`
- **检查 2 警告** → `description` 没有清楚说明用途和触发场景
- **检查 3 失败** → 找到多少阶段与所需的最少阶段数
- **检查 4 失败** → 技能正文中的任何位置都没有判定关键字
- **检查 5 失败** → 技能会写入/修改文件，但没有写入前确认语言
- **检查 6 警告** → 最后没有后续或下一步部分
- **检查 7 失败** → frontmatter 仍包含旧斜杠命令字段，例如 `argument-hint`、`user-invocable`、`allowed-tools`、`context`、`model`、`agent` 或 `isolation`

对于每个失败或警告**类别**检查（如果在阶段 2b 中分配了类别），
确定技能文本中的确切差距。例如：
- 如果 G2 失败（门模式，未生成完整导演）：技能体永远不会引用所有 4 个
  PHASE-GATE 导演提示
- 如果 A2 失败（创作，没有每个部分“我可以写”）：技能在最后询问一次，而不是
  在每个部分之前写
- 如果T3失败（团队，被阻止未浮出水面）：技能不会停止对被阻止代理的依赖工作

在提出任何更改之前，向用户显示完整的组合诊断。

---

## 第 4 阶段：提出修复建议

Write 针对每个故障和警告的有针对性的修复。显示建议的更改
作为明确标记的 before/after 块。只改变失败的地方——不改变
重写正在通过的部分。

问：“我可以将这个改进版本写入`.codex/skills/[name]/SKILL.md`吗？”

如果用户说不，就到此为止。

---

## 第 5 阶段：Write 和重新测试

记录技能文件的当前内容（以便在需要时恢复）。

Write 改进了 `.codex/skills/[name]/SKILL.md` 的技能。

重新运行 `/skill-test static [name]` 并记录新的静态分数。
如果分配了类别，还需重新运行 `/skill-test category [name]` 并记录新的类别分数。

显示比较：
```
Static:   Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings
Category: Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings  (if applicable)
Combined change: improved / no change / worse
```

---

## 第六阶段：判决

计算组合故障总数：静态 FAIL + 类别 FAIL + 静态 WARN + 类别 WARN。

**如果综合分数有所提高（综合失败计数低于基线）：**
报告：“分数提高了。变化保持不变。”
显示每个维度中修复内容的摘要。

**如果综合得分相同或更差：**
报告：“综合分数没有提高。”
展示发生了什么变化以及为什么它可能没有帮助。
问：“我可以使用 git checkout 恢复 `.codex/skills/[name]/SKILL.md` 吗？”
如果是：运行 `git checkout -- .codex/skills/[name]/SKILL.md`

---

## 第 7 阶段：后续步骤

- 运行 `/skill-test static all` 查找下一个失败的技能。
- 运行 `/skill-improve [next-name]` 以继续循环另一个技能。
- 运行 `/skill-test audit` 以查看整体覆盖进度。
