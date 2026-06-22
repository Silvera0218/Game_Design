---
name: skill-test
description: "验证技能文件的结构合规性和行为正确性。三种模式：静态（linter）、规范（行为）、审计（覆盖率报告）。"
---

# 技能测试

验证 `.codex/skills/*/SKILL.md` 文件的结构合规性和
行为的正确性。没有外部依赖——完全在
现有的 skill/hook/template 架构。

**四种模式：**

| Mode | Command | Purpose | 代币成本 |
|------|---------|---------|------------|
| `static` | `/skill-test 静态 [名称\|all]` | 结构检查——每项技能 7 次合规性检查 | 低 (~1k/skill) |
| `spec` | `/skill-test spec [name]` | 行为验证器 - 评估测试规范中的断言 | 中 (~5k/skill) |
| `category` | `/skill-test 类别 [名称\|all]` | 类别标题——根据类别特定指标检查技能 | 低 (~2k/skill) |
| `audit` | `/skill-test audit` | 覆盖范围报告 — 技能、代理规格、上次测试日期 | 低（总共约 3k） |

---

## 第一阶段：解析参数

从第一个参数确定模式：

- `static [name]` → 对一项技能进行 7 次结构检查
- `static all` → 对所有技能运行 7 次结构检查 (Glob `.codex/skills/*/SKILL.md`)
- `spec [name]` → 阅读技能 + 测试规范，评估断言
- `category [name]` → 运行 `CCGS Skill Testing Framework/quality-rubric.md` 中的特定类别标题
- `category all` → 为目录中具有 `category:` 的每项技能运行类别标题
- `audit`（或无参数）→读取目录，列出所有技能和代理，显示覆盖范围

如果参数丢失或无法识别，则输出用法并停止。

---

## 阶段 2A：静态模式 — 结构检查

对于每项正在测试的技能，请完整阅读其 `SKILL.md` 并运行所有 7 个 Codex 兼容检查：

### 检查 1 — 必填 Frontmatter 字段
该文件必须在 YAML frontmatter 块中包含所有这些内容：
- `name:`
- `description:`

**失败**（如果不存在）。

### 检查 2 — 触发描述质量
`description` 是 Codex 触发 skill 的主要依据。它应该同时说明：
- 这个 skill 做什么
- 用户在什么场景、措辞或任务中应该触发它

如果描述过短、只写标题式概括，或没有“何时使用”的信息，则 **警告**。

### 检查 3 — 多阶段
该技能必须有 ≥2 个编号的阶段标题。寻找如下模式：
- `## Phase N` 或 `## Phase N:`
- `## N.`（编号的顶级部分）
- 如果阶段未明确编号，则至少有 2 个不同的 `##` 标题

如果找到少于 2 个类似阶段的标题，则 **失败**。

### 检查 4 — 判决关键字
该技能必须至少包含以下一项：`PASS`、`FAIL`、`CONCERNS`、`APPROVED`、
`BLOCKED`、`COMPLETE`、`READY`、`COMPLIANT`、`NON-COMPLIANT`

如果不存在则**失败**。

### 检查 5 — 协作协议语言
如果技能正文包含写文件、创建文件、修改文件、Write、Edit 等操作指令，则必须包含先问后写的语言。寻找：
- `"May I write"`（规范形式）
- `"before writing"` 或 `"approval"` 近文件写入指令
- `"ask"` + `"write"` 非常接近（在同一部分内）
- 中文等价表达，例如“我可以写入/更新/创建……吗”

如果技能明显会写文件但未找到写入前确认语言，则 **失败**。只读技能可以通过此检查。

### 检查 6 — 下一步切换
该技能必须以建议的下一步行动或后续路径结束。寻找：
- 最后一部分提到了另一项技能（例如，`/story-done`、`/gate-check`）
- “推荐下一步”或“下一步”措辞
- “后续”或“在此之后”部分

**警告** 如果不存在。

### 检查 7 — Codex Frontmatter 兼容性
Codex skill frontmatter 应保持简洁：`name` 和 `description` 必需；`metadata` 或 `license` 可以保留。

如果发现来自旧斜杠命令系统的字段，例如 `argument-hint`、`user-invocable`、`allowed-tools`、`context`、`model`、`agent` 或 `isolation`，则 **失败**，并建议把相关信息移入正文或删除。

---

### 静态模式输出格式

对于单一技能：
```
=== Skill Static Check: /[name] ===

Check 1 — Frontmatter Fields:    PASS
Check 2 — Trigger Description:    PASS
Check 3 — Multiple Phases:        PASS (7 phases found)
Check 4 — Verdict Keywords:       PASS (PASS, FAIL, CONCERNS)
Check 5 — Collaborative Protocol: PASS ("May I write" found)
Check 6 — Next-Step Handoff:      WARN (no follow-up section found)
Check 7 — Codex Frontmatter:      PASS

Verdict: WARNINGS (1 warning, 0 failures)
Recommended: Add a "Follow-Up Actions" section at the end of the skill.
```

对于 `static all`，生成一个汇总表，然后列出所有不合规的技能：
```
=== Skill Static Check: All 52 Skills ===

Skill                  | Result       | Issues
-----------------------|--------------|-------
gate-check             | COMPLIANT    |
design-review          | COMPLIANT    |
story-readiness        | WARNINGS     | Check 5: no handoff
...

Summary: 48 COMPLIANT, 3 WARNINGS, 1 NON-COMPLIANT
Aggregate Verdict: N WARNINGS / N FAILURES
```

---

## 阶段 2B：规格模式 — 行为验证者

### 第 1 步 — 查找文件

在 `.codex/skills/[name]/SKILL.md` 上查找技能。
从 `CCGS Skill Testing Framework/catalog.yaml` 查找规范路径 — 使用
`spec:` 匹配技能条目的字段。

如果其中一个缺失：
- 缺少技能：“在 `.codex/skills/` 中找不到技能‘[name]’。”
- 目录中缺少规格路径：“catalog.yaml 中没有为‘[name]’设置规格路径。”
- 在路径中找不到规范文件：“[path] 处缺少规范文件。运行 `/skill-test audit`
  查看覆盖范围的差距。”

### 步骤 2 — Read 两个文件

Read 完整的技能文件和测试规范文件。

### 第 3 步 — 评估断言

对于规范中的每个**测试用例**：

1. Read **夹具**描述（项目文件的假定状态）
2. Read **预期行为**步骤
3. Read 每个 **断言** 复选框

对于每个断言，评估该技能是否有书面说明，如果
正确遵循给定的夹具状态，将满足它。这是一个
Codex-评估推理检查，而不是代码执行。

标记每个断言：
- **通过** — 技能说明显然满足这一断言
- **部分** — 技能说明部分解决了这个问题，但含糊不清
- **失败** - 给定固定装置，技能说明无法满足此断言

对于**协议合规性**断言（始终存在）：
- 文件写入前检查技能是否需要“我可以写吗”
- 在请求批准之前检查技能是否呈现结果
- 检查技能是否以建议的下一步结束
- 检查技能是否避免未经批准自动创建文件

### 第 4 步 — 构建报告

```
=== Skill Spec Test: /[name] ===
Date: [date]
Spec: CCGS Skill Testing Framework/skills/[category]/[name].md

Case 1: [Happy Path — name]
  Fixture: [summary]
  Assertions:
    [PASS] [assertion text]
    [FAIL] [assertion text]
       Reason: The skill's Phase 3 says "..." but the fixture state means "..."
  Case Verdict: FAIL

Case 2: [Edge Case — name]
  ...
  Case Verdict: PASS

Protocol Compliance:
  [PASS] Uses "May I write" before file writes
  [PASS] Presents findings before asking approval
  [WARN] No explicit next-step handoff at end

Overall Verdict: FAIL (1 case failed, 1 warning)
```

### 第 5 步 — 向 Write 结果提供

“我可以将这些结果写入 `CCGS Skill Testing Framework/results/skill-test-spec-[name]-[date].md`
并更新 `CCGS Skill Testing Framework/catalog.yaml`？”

If yes:
- Write 结果文件至 `CCGS Skill Testing Framework/results/`
- 更新 `CCGS Skill Testing Framework/catalog.yaml` 中的技能条目：
  - `last_spec: [date]`
  - `last_spec_结果：通过|PARTIAL|FAIL`

---

## 第 2D 阶段：类别模式 — 评分标准评估

### 第 1 步 — 找到技能和类别

在 `.codex/skills/[name]/SKILL.md` 上查找技能。
在 `CCGS Skill Testing Framework/catalog.yaml` 中查找 `category:` 字段。

如果未找到技能：“未找到技能‘[name]’。”
如果没有 `category:` 字段：“没有为 catalog.yaml 中的‘[name]’分配类别。
先将`category: [name]`添加到技能条目中。”

对于 `category all`：收集 `category:` 字段的所有技能并处理每个技能。
`category: utility` 技能根据 U1（静态检查通过）和 U2 进行评估
仅（门模式正确，如果适用）— 跳至 U1 的静态模式。

### 步骤 2 — Read 评分标准部分

Read `CCGS Skill Testing Framework/quality-rubric.md`。
提取与技能类别匹配的部分（例如，`### gate`、`### team`）。

### 第 3 步 — Read 技能

Read 技能`SKILL.md` 完全。

### 第 4 步 — 评估评分标准

对于类别的标题表中的每个指标：
1. 检查技能的书面说明是否明确满足标准
2. 标记“通过”、“失败”或“警告”
3. 对于 FAIL/WARN，确定技能文本中的确切差距（引用相关部分
   或注意它的缺失）

### 第 5 步 — 输出报告

```
=== Skill Category Check: /[name] ([category]) ===

Metric G1 — Review mode read:      PASS
Metric G2 — Full mode directors:   FAIL
  Gap: Phase 3 spawns only CD-PHASE-GATE; TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE absent
Metric G3 — Lean mode: PHASE-GATE only: PASS
Metric G4 — Solo mode: no directors:    PASS
Metric G5 — No auto-advance:       PASS

Verdict: FAIL (1 failure, 0 warnings)
Fix: Add TD-PHASE-GATE, PR-PHASE-GATE, and AD-PHASE-GATE to the full-mode director
     panel in Phase 3.
```

### 第 6 步 — 提出更新目录

“我可以更新 `CCGS Skill Testing Framework/catalog.yaml` 来记录此类别检查吗
（`last_category`、`last_category_result`）用于 [name]？”

---

## 阶段 2C：审核模式 — 覆盖率报告

### 第 1 步 — Read 目录

Read `CCGS Skill Testing Framework/catalog.yaml`。如果丢失，请注意该目录不存在
还（首次运行状态）。

### 第 2 步 — 枚举所有技能和代理

Glob `.codex/skills/*/SKILL.md` 获取完整的技能列表。
从每个路径（目录名称）中提取技能名称。

另请阅读 `CCGS Skill Testing Framework/catalog.yaml` 中的 `agents:` 部分以获取
完整的代理商名单。

### 第 3 步 — 构建技能覆盖表

对于每个技能：
- 检查规范文件是否存在（使用目录中的 `spec:` 路径，或 glob `CCGS Skill Testing Framework/skills/*/[name].md`）
- 查找 `last_static`、`last_static_result`、`last_spec`、`last_spec_result`、
  目录中的 `last_category`、`last_category_result`、`category`（或标记为
  “从不”/“—”如果不在目录中）
- 优先来自目录`priority:`字段(critical/high/medium/low)

### 步骤 3b — 构建代理覆盖表

对于目录 `agents:` 部分中的每个代理：
- 检查规范文件是否存在（使用目录中的 `spec:` 路径，或 glob `CCGS Skill Testing Framework/agents/*/[name].md`）
- 从目录中查找 `last_spec`、`last_spec_result`、`category`

### 第 4 步 — 输出报告

```
=== Skill Test Coverage Audit ===
Date: [date]

SKILLS (72 total)
Specs written: 72 (100%) | Never static tested: 72 | Never category tested: 72

Skill                  | Cat      | Has Spec | Last Static | S.Result | Last Cat | C.Result | Priority
-----------------------|----------|----------|-------------|----------|----------|----------|----------
gate-check             | gate     | YES      | never       | —        | never    | —        | critical
design-review          | review   | YES      | never       | —        | never    | —        | critical
...

AGENTS (49 total)
Agent specs written: 49 (100%)

Agent                  | Category   | Has Spec | Last Spec   | Result
-----------------------|------------|----------|-------------|--------
creative-director      | director   | YES      | never       | —
technical-director     | director   | YES      | never       | —
...

Top 5 Priority Gaps (skills with no spec, critical/high priority):
(none if all specs are written)

Skill coverage:  72/72 specs (100%)
Agent coverage:  49/49 specs (100%)
```

在审核模式下没有文件写入。

提供：“您想运行 `/skill-test static all` 来检查结构吗？
所有技能的合规性？ `/skill-test category all` 运行类别标题
检查？或者 `/skill-test spec [name]` 来运行特定的行为测试？”

---

## 第 3 阶段：建议的后续步骤

任何模式完成后，提供上下文跟进：

- `static [name]` 之后：“运行 `/skill-test spec [name]` 来验证行为
  如果存在测试规范，则正确性。”
- `static all` 失败后：“首先解决不兼容的技能。运行
  `/skill-test static [name]` 单独提供详细的修复指南。”
- `spec [name]` PASS后：“更新`CCGS Skill Testing Framework/catalog.yaml`以记录此
  通过日期。考虑运行 `/skill-test audit` 来查找下一个规格差距。”
- `spec [name]` 失败后：“查看失败的断言并更新技能
  或解决不匹配问题的测试规范。”
- 在 `audit` 之后：“从关键优先级差距开始。使用规范模板
  在 `CCGS Skill Testing Framework/templates/skill-test-spec.md` 创建新规格。”
