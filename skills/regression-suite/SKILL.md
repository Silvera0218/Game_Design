---
name: regression-suite
description: "将测试覆盖范围映射到 GDD 关键路径，无需回归测试即可识别已修复的错误，标记新功能的覆盖范围漂移，并在实施错误修复后或发布门之前维持 tests/regression-suite.md. 运行。"
---

# 回归套件

这项技能可确保每个错误修复都得到测试的支持
抓住了最初的错误——并且回归套件保持最新
游戏不断发展。它还可以检测何时添加新功能，而无需
相应的回归覆盖率。

回归套件不是一个新的测试类别 - 它是一个**策划的列表
`tests/`** 中已有的测试共同涵盖了游戏的关键路径
以及已知的故障点。该技能维护该列表。

**输出：** `tests/regression-suite.md`

**何时运行：**
- 修复错误后（确认编写了回归测试或识别差距）
- 在发布门之前（`/gate-check polish` 需要存在回归套件）
- 作为冲刺的一部分，接近检测覆盖范围漂移

---

## 1. 解析参数

**Modes:**
- `/regression-suite update` — 扫描新错误修复此冲刺并检查
  用于回归测试的存在；将新测试添加到套件清单中
- `/regression-suite audit` — 对所有 GDD 关键路径与其他关键路径进行全面审核
  现有的测试覆盖率；标记没有回归测试的路径
- `/regression-suite report` — 只读状态报告（不可写入）；适合的
  用于冲刺评审
- 无参数 - 如果冲刺处于活动状态，则运行 `update`，否则运行 `audit`

---

## 2. 加载上下文

### 步骤 2a — 加载现有回归套件

Read `tests/regression-suite.md`（如果存在）。摘录：
- 总注册回归测试
- 最后更新日期
- 任何标记为 `STALE` 或 `QUARANTINED` 的测试

如果不存在：请注意“未找到回归套件 - 将创建一个。”

### 步骤 2b — 负载测试库存

Glob所有测试文件：
```
tests/unit/**/*_test.*
tests/integration/**/*_test.*
tests/regression/**/*
```

对于每个文件，记下系统（来自目录路径）和文件名。
除非名称到测试映射需要，否则不要读取测试文件内容。

### 步骤 2c — 加载 GDD 关键路径

对于 `audit` 模式：读取 `design/gdd/systems-index.md` 以获取所有系统。
对于每个 MVP 层系统，读取其 GDD 并提取：
- 验收标准（这些定义了关键路径）
- 公式部分（公式必须有回归测试）
- 边缘案例部分（已知的边缘案例应该进行回归测试）

对于 `update` 模式：跳过完整的 GDD 扫描。相反，阅读当前的冲刺计划
和故事文件来查找状态为：完成此冲刺的故事。

### 步骤 2d — 加载已关闭的错误

Glob `production/qa/bugs/*.md` 并使用 `Status: Closed` 过滤错误
或 `Status: Fixed` 字段。注意：
- 该错误出现在哪个故事或系统中
- 修复说明中是否提及回归测试

---

## 3. 地图覆盖范围——关键路径

仅适用于 `audit` 模式：

对于每个 GDD 验收标准，确定是否存在测试：

1. Grep `tests/unit/[system]/` 和 `tests/integration/[system]/` 用于文件名
   以及与标准的键 noun/verb 相关的函数名称
2. 分配覆盖范围：

| Status | Meaning |
|--------|---------|
| **COVERED** | 存在针对该标准逻辑的测试文件 |
| **PARTIAL** | 存在测试，但并未涵盖所有情况（例如仅快乐路径） |
| **MISSING** | 未找到此关键路径的测试 |
| **EXEMPT** | Visual/Feel 或 UI 标准 — 设计上不可自动化 |

3. 将与公式或状态机对应的 MISSING 项提升为
   **高优先级**差距 - 这些是最可能的回归源。

---

## 4. 地图覆盖范围——修复错误

对于每个已关闭的错误：

1. 从 bug 的元数据中提取系统 slug
2. Grep `tests/unit/[system]/` 和 `tests/integration/[system]/` 用于测试
   引用错误 ID 或特定故障场景
3. Assign:
   - **有回归测试** - 发现一个测试可以捕获此错误
   - **缺少回归测试** - 错误已修复，但没有测试可以防止复发

对于缺少回归测试项目：
- 将它们标记为回归差距
- 建议测试文件路径：`tests/unit/[system]/[bug-slug]_regression_test.[ext]`
- 注意：“如果没有进行此测试，此错误可能会在未来的冲刺中悄无声息地返回。”

---

## 5. 检测覆盖范围漂移

当游戏增长但回归套件不会增长时，就会发生覆盖漂移。

检查漂移指标：
- 故事完成了本次冲刺，`tests/` 中没有相应的测试文件
- 自上次回归套件更新以来，新系统已添加到 `systems-index.md`
- 自上次更新回归套件以来添加或修订的 GDD 部分
  （如果可用，请在 GDD 文件修改提示上使用 Grep，或询问用户）
- `tests/regression-suite.md` 最后更新日期与当前日期 — 如果差距 >
  2 次冲刺，标记为可能已过时

---

## 6. 生成报告和套件清单

### 报告格式（对话中）

```
## Regression Suite Status

**Mode**: [update | audit | report]
**Existing registered tests**: [N]
**Test files scanned**: [N]

### Critical Path Coverage (audit mode only)
| System | Total ACs | Covered | Partial | Missing | Exempt |
|--------|-----------|---------|---------|---------|--------|
| [name] | [N] | [N] | [N] | [N] | [N] |

**Coverage rate (non-exempt)**: [N]%

### Bug Regression Coverage
| Bug ID | System | Severity | Has Regression Test? |
|--------|--------|----------|----------------------|
| BUG-NNN | [system] | S[N] | YES / NO ⚠ |

**Bugs without regression tests**: [N]

### Coverage Drift Indicators
[List new systems or stories with no test coverage, or "None detected."]

### Recommended New Regression Tests
| Priority | System | Suggested Test File | Covers |
|----------|--------|---------------------|--------|
| HIGH | [system] | `tests/unit/[system]/[slug]_regression_test.[ext]` | BUG-NNN / AC-[N] |
| MEDIUM | [system] | `tests/unit/[system]/[slug]_test.[ext]` | [criterion] |
```

### 套件清单格式 (`tests/regression-suite.md`)

清单是一个策划索引——不是测试本身，而是一个注册表
在发布之前应始终通过其中的测试：

```markdown
# Regression Suite Manifest

> Last Updated: [date]
> Total registered tests: [N]
> Coverage: [N]% of GDD critical paths

## How to run

[Engine-specific command to run all regression tests]

## Registered Regression Tests

### [System Name]

| Test File | Test Function (if known) | Covers | Added |
|-----------|--------------------------|--------|-------|
| `tests/unit/[system]/[file]_test.[ext]` | `test_[scenario]` | AC-N / BUG-NNN | [date] |

## Known Gaps

Tests that should exist but don't yet:

| Priority | System | Suggested Path | Covers | Reason Not Yet Written |
|----------|--------|----------------|--------|------------------------|
| HIGH | [system] | `tests/unit/[system]/[path]` | BUG-NNN | Bug fixed without test |

## Quarantined Tests

Tests that are flaky or disabled (do not run in CI):

| Test File | Function | Reason | Quarantined Since |
|-----------|----------|--------|-------------------|
| (none) | | | |
```

---

## 7. Write 输出

问：“我可以将 write/update `tests/regression-suite.md` 与当前
回归套件清单？”

对于 `update` 模式：追加新条目；永远不要删除现有条目
（使用 `Edit` 进行定向插入）。
对于 `audit` 模式：使用更新的覆盖数据重写完整清单。
对于 `report` 模式：请勿写入任何内容。

写完后（如果获得批准）：

- 对于每个高优先级差距：“考虑创建缺失的回归测试
  在下一个冲刺之前。运行 `/test-helpers` 以搭建测试文件。”
- 如果 bug 回归差距 > 0：“这些 bug 可以默默地返回而不进行回归
  测试。下一个冲刺应该包括一个故事来编写缺失的测试。”
- 如果检测到覆盖范围漂移：“回归套件可能正在漂移。考虑
  在下一个冲刺边界运行 `/regression-suite audit`。”

结论：**完成**——回归套件已更新。 （如果用户拒绝写入：判决：**被阻止**。）

---

## 协作协议

- **永远不要从清单中删除现有的回归测试**
  明确的用户批准——删除故意编写的测试是一种
  回归风险本身
- **差距是建议性的，而不是阻碍** - 清楚地显示它们，但不会阻止
  继续进行的其他工作（除了需要回归套件的发布门）
- **隔离不是删除** - 间歇性失败的测试应该
  已隔离（在舱单中注明）但未移除；它们应该由
  `/test-flakiness`
- **写入前询问** — 在创建或更新清单之前始终确认
