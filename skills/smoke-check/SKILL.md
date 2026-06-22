---
name: smoke-check
description: "在 QA 移交之前运行关键路径烟雾测试门。执行自动化测试套件，验证核心功能并生成 PASS/FAIL 报告。在实施冲刺故事之后、手册 QA 开始之前运行。失败的烟雾检查意味着构建尚未准备好 QA。"
---

# 烟雾检查

该技能是“实施完成”和“准备就绪”之间的大门 QA
放手”。它运行自动化测试套件，检查测试覆盖率差距，
与开发人员批量验证关键路径，并生成 PASS/FAIL
report.

规则很简单：**未通过烟雾检查的构建不会转到 QA。**
将损坏的构建交给 QA 会浪费他们的时间并使团队士气低落。

**输出：** `production/qa/smoke-[date].md`

---

## 解析参数

可以组合参数：`/smoke-check sprint --platform console`

**基本模式**（第一个参数，默认值：`sprint`）：
- `sprint` — 针对当前冲刺故事的全面烟雾检查
- `quick` — 跳过覆盖扫描（第 3 阶段）和第 3 批；用于快速复查

**平台标志**（`--platform`，默认值：无）：
- `--platform pc` — 添加特定于 PC 的检查（键盘、鼠标、窗口模式）
- `--platform console` — 添加特定于控制台的检查（游戏手柄、电视安全区、
  平台认证要求）
- `--platform mobile` — 添加特定于移动设备的检查（触摸、portrait/landscape、
  battery/thermal 行为）
- `--platform all` — 添加所有平台变体；输出每个平台的判决表

如果提供了 `--platform`，第 4 阶段将添加特定于平台的批次并
除了整体判决之外，第 5 阶段还输出每个平台的判决表。

---

## 第 1 阶段：检测测试设置

在运行任何东西之前，了解环境：

1. **测试框架检查**：验证 `tests/` 目录是否存在。
   如果没有：“在 `tests/` 处找不到测试目录。运行 `/test-setup`
   搭建测试基础设施，或手动创建目录
   如果测试在其他地方进行。”然后停下来。

2. **CI检查**：检查`.github/workflows/`是否包含工作流程文件
   参考测试。在报告中注意是否配置了 CI。

3. **发动机检测**：读取 `.codex/docs/technical-preferences.md` 并
   提取 `Engine:` 值。将其存储为测试命令选择
   Phase 2.

4. **冒烟测试清单**：检查是否有`production/qa/smoke-tests.md`或
   `tests/smoke/` 存在。如果找到烟雾测试列表，则将其加载以供使用
   第 4 阶段。如果两者都不存在，将从当前的 QA 中进行冒烟测试
   计划（第四阶段后备）。

5. **QA 计划检查**： glob `production/qa/qa-plan-*.md` 并取最多
   最近修改的文件。如果找到，请记下路径 - 它将用于
   第 3 阶段和第 4 阶段。如果未找到，请注意：“未找到 QA 计划。运行
`/qa-plan sprint` 在烟雾检查之前获得最佳结果。”

在继续操作之前报告结果：“环境：[engine]。测试目录：
[found / not found]。 CI 配置：[yes / no]。 QA 计划：[path / not found]。”

---

## 第 2 阶段：运行自动化测试

尝试通过 Bash 运行测试套件。根据引擎选择命令
在第一阶段检测到：

**Godot 4:**
```bash
godot --headless --script tests/gdunit4_runner.gd 2>&1
```
如果该路径中不存在 GDUnit4 运行程序脚本，请尝试：
```bash
godot --headless -s addons/gdunit4/GdUnitRunner.gd 2>&1
```
如果两条路径都不存在，请注意：“GDUnit4 运行程序未找到 - 确认运行程序
您的测试框架的路径。”

**Unity:**
Unity 测试需要编辑器，并且在大多数情况下无法通过 shell 无头运行
环境。检查最近的测试结果工件：
```bash
ls -t test-results/ 2>/dev/null | head -5
```
如果测试结果文件存在（XML或JSON），则读取最新的并解析
PASS/FAIL 很重要。如果不存在工件：“Unity 测试必须从
编辑器或 CI 管道。请在继续之前手动确认测试状态。”

**Unreal 引擎：**
```bash
ls -t Saved/Logs/ 2>/dev/null | grep -i "test\|automation" | head -5
```
如果没有找到匹配的日志：“UE自动化测试必须通过会话运行
前端或 CI 管道。请手动确认测试状态。”

**未知引擎/未配置：**
“`.codex/docs/technical-preferences.md` 中未配置引擎。运行
`/setup-engine` 指定引擎，然后重新运行 `/smoke-check`。”

**如果测试运行程序在此环境中不可用**（引擎二进制文件不可用）
在 PATH 上，未找到运行程序脚本等），清楚地报告：

“无法执行自动化测试 - 在 PATH 上找不到引擎二进制文件。
状态将记录为“未运行”。从本地 IDE 确认测试结果
或 CI 管道。未确认的 NOT RUN 被视为 PASS WITH WARNINGS，而不是
失败——开发人员必须手动确认结果。”

不要将 NOT RUN 视为自动失败。记录下来作为警告。的
第四阶段开发者手动确认即可解决。

解析运行器输出并提取：
- 运行的测试总数
- 通过次数
- 失败计数
- 任何失败测试的名称（最多 10 个；如果更多，请记下计数）
- 运行器本身的任何崩溃或错误输出

---

## 第 3 阶段：检查测试覆盖率

按优先顺序绘制故事列表：
1. 第 1 阶段中发现的 QA 计划（其测试摘要表列出了预期测试
   每个故事的文件路径）
2. 当前的冲刺计划来自`production/sprints/`（最近修改
   file)
3. 如果传递了 `quick` 参数，则完全跳过此阶段并注意：
   “跳过覆盖扫描 — 运行 `/smoke-check sprint` 进行全面覆盖
   analysis."

对于范围内的每个故事：

1. 从故事的文件路径中提取系统 slug
   （例如，`production/epics/combat/story-001.md` → `combat`）
2. 文件的 Glob `tests/unit/[system]/` 和 `tests/integration/[system]/`
其名称包含故事段或密切相关的术语
3. 检查故事文件本身的 `Test file:` 标头字段或
   “测试证据”部分

为每个故事分配报道状态：

| Status | Meaning |
|--------|---------|
| **COVERED** | 找到了与该故事的系统和范围相匹配的测试文件 |
| **MANUAL** | 故事类型为 Visual/Feel 或 UI；找到了测试证据文件 |
| **MISSING** | 没有匹配测试文件的逻辑或集成故事 |
| **EXPECTED** | Config/Data 故事 — 无需测试文件；抽查就足够了 |
| **UNKNOWN** | 故事文件丢失或无法读取 |

缺失的条目是建议性的空白。它们不会导致 FAIL 判决，但必须
在报告中突出显示，必须先解决 `/story-done` 才能
完全结束这些故事。

---

## 第 4 阶段：运行手动烟雾检查

按优先顺序从以下位置绘制烟雾测试清单：
1. QA 计划的“冒烟测试范围”部分（如果在第 1 阶段找到 QA 计划）
2. `production/qa/smoke-tests.md`（如果存在）
3. `tests/smoke/` 目录内容（如果存在）
4. 下面的标准后备列表（仅当以上都不存在时使用）

根据 sprint 或 QA 确定的实际系统定制批次 2 和 3
计划。将括号中的占位符替换为当前的真实机械师名称
斯普林特的故事。

使用`AskUserQuestion`进行批量验证。最多保持 3 次通话。

**第 1 批 — 核心稳定性（始终运行）：**
```
question: "Smoke check — Batch 1: Core stability. Please verify each:"
options:
  - "Game launches to main menu without crash — PASS"
  - "Game launches to main menu without crash — FAIL"
  - "New game / session starts successfully — PASS"
  - "New game / session starts successfully — FAIL"
  - "Main menu responds to all inputs — PASS"
  - "Main menu responds to all inputs — FAIL"
```

**第 2 批 — 冲刺机制和回归（始终运行）：**
```
question: "Smoke check — Batch 2: This sprint's changes and regression check:"
options:
  - "[Primary mechanic this sprint] — PASS"
  - "[Primary mechanic this sprint] — FAIL: [describe what broke]"
  - "[Second notable change this sprint, if any] — PASS"
  - "[Second notable change this sprint] — FAIL"
  - "Previous sprint's features still work (no regressions) — PASS"
  - "Previous sprint's features — regression found: [brief description]"
```

**第 3 批 — 数据完整性和性能（除非 `quick` 参数运行）：**
```
question: "Smoke check — Batch 3: Data integrity and performance:"
options:
  - "Save / load completes without data loss — PASS"
  - "Save / load — FAIL: [describe what broke]"
  - "Save / load — N/A (save system not yet implemented)"
  - "No new frame rate drops or hitches observed — PASS"
  - "Frame rate drops or hitches found — FAIL: [where]"
  - "Performance — not checked in this session"
```

逐字记录第 5 阶段报告的每个响应。

**平台批次** *（仅在提供 `--platform` 参数时运行）*：

**PC平台**（`--platform pc`或`--platform all`）：
```
question: "Smoke check — PC Platform: Verify platform-specific behaviour:"
options:
  - "Keyboard controls work correctly across all menus and gameplay — PASS"
  - "Keyboard controls — FAIL: [describe issue]"
  - "Mouse input and cursor visibility correct in all states — PASS"
  - "Mouse input — FAIL: [describe issue]"
  - "Windowed and fullscreen modes function without graphical issues — PASS"
  - "Windowed/fullscreen — FAIL: [describe issue]"
  - "Resolution changes apply correctly — PASS"
  - "Resolution changes — FAIL: [describe issue]"
```

**控制台平台**（`--platform console` 或 `--platform all`）：
```
question: "Smoke check — Console Platform: Verify platform-specific behaviour:"
options:
  - "Gamepad input works correctly for all actions — PASS"
  - "Gamepad input — FAIL: [describe issue]"
  - "UI fits within TV safe zone margins (no text clipped) — PASS"
  - "TV safe zone — FAIL: [describe what is clipped]"
  - "No keyboard/mouse-only fallbacks shown to gamepad user — PASS"
  - "Input prompt inconsistency — FAIL: [describe]"
  - "Game boots correctly from cold start (no prior save) — PASS"
  - "Cold start — FAIL: [describe issue]"
```

**移动平台**（`--platform mobile` 或 `--platform all`）：
```
question: "Smoke check — Mobile Platform: Verify platform-specific behaviour:"
options:
  - "Touch controls work correctly for all primary actions — PASS"
  - "Touch controls — FAIL: [describe issue]"
  - "Game handles orientation change (portrait ↔ landscape) correctly — PASS"
  - "Orientation change — FAIL: [describe what breaks]"
  - "Background / foreground transitions (home button) handled gracefully — PASS"
  - "Background/foreground — FAIL: [describe issue]"
  - "No visible performance issues on target device (no thermal throttling signs) — PASS"
  - "Mobile performance — FAIL: [describe issue]"
```

---

## 第五阶段：生成报告

组装完整的烟雾检查报告：

````markdown
## Smoke Check Report
**Date**: [date]
**Sprint**: [sprint name / number, or "Not identified"]
**Engine**: [engine]
**QA Plan**: [path, or "Not found — run /qa-plan first"]
**Argument**: [sprint | quick | blank]

---

### Automated Tests

**Status**: [PASS ([N] tests, [N] passing) | FAIL ([N] failures) |
NOT RUN ([reason])]

[If FAIL, list failing tests:]
- `[test name]` — [brief failure description from runner output]

[If NOT RUN:]
"Manual confirmation required: did tests pass in your local IDE or CI? This
will determine whether the automated test row contributes to a FAIL verdict."

---

### Test Coverage

| Story | Type | Test File | Coverage Status |
|-------|------|-----------|----------------|
| [title] | Logic | `tests/unit/[system]/[slug]_test.[ext]` | COVERED |
| [title] | Visual/Feel | `tests/evidence/[slug]-screenshots.md` | MANUAL |
| [title] | Logic | — | MISSING ⚠ |
| [title] | Config/Data | — | EXPECTED |

**Summary**: [N] covered, [N] manual, [N] missing, [N] expected.

---

### Manual Smoke Checks

- [x] Game launches without crash — PASS
- [x] New game starts — PASS
- [x] [Core mechanic] — PASS
- [ ] [Other check] — FAIL: [user's description]
- [x] Save / load — PASS
- [-] Performance — not checked this session

---

### Missing Test Evidence

Stories that must have test evidence before they can be marked COMPLETE via
`/story-done`:

- **[story title]** (`[path]`) — Logic story has no test file.
  Expected location: `tests/unit/[system]/[story-slug]_test.[ext]`

[If none:] "All Logic and Integration stories have test coverage."

---

### Platform-Specific Results *(only if `--platform` was provided)*

| Platform | Checks Run | Passed | Failed | Platform Verdict |
|----------|-----------|--------|--------|-----------------|
| PC | [N] | [N] | [N] | PASS / FAIL |
| Console | [N] | [N] | [N] | PASS / FAIL |
| Mobile | [N] | [N] | [N] | PASS / FAIL |

**Platform notes**: [any platform-specific observations not captured in pass/fail]

Any platform with one or more FAIL checks contributes to the overall FAIL verdict.

---

### Verdict: [PASS | PASS WITH WARNINGS | FAIL]

[Verdict rules — first matching rule wins:]

**FAIL** if ANY of:
- Automated test suite ran and reported one or more test failures
- Any Batch 1 (core stability) check returned FAIL
- Any Batch 2 (primary sprint mechanic or regression check) returned FAIL

**PASS WITH WARNINGS** if ALL of:
- Automated tests PASS or NOT RUN (developer has not yet confirmed)
- All Batch 1 and Batch 2 smoke checks PASS
- One or more Logic/Integration stories have MISSING test evidence

**PASS** if ALL of:
- Automated tests PASS
- All smoke checks in all batches PASS or N/A
- No MISSING test evidence entries
````

---

## 第 6 阶段：Write 和门

在对话中呈现完整的报告，然后提问：

“我可以将这份烟雾检查报告写给 `production/qa/smoke-[date].md` 吗？”

Write 仅在批准后。

写完后，下达门判定：

**如果判决失败：**

“烟雾检查失败。在这些故障得到解决之前，请勿将其移交给 QA
resolved:

[List each failing automated test or smoke check with a one-line description]

修复故障并再次运行 `/smoke-check` 以在 QA 切换之前重新选通。”

**如果判决通过但带有警告：**

“烟雾检查已通过，但有警告。构建已准备好用于手动 QA。

在受影响的故事上运行 `/story-done` 之前需要解决的建议事项：
[list MISSING test evidence entries]

QA 交接：与 QA 测试人员共享 `production/qa/qa-plan-[sprint].md`
代理开始手动验证。”

**如果判决通过：**

“烟雾检查顺利通过。构建已准备好进行手动 QA。

QA 交接：与 QA 测试人员共享 `production/qa/qa-plan-[sprint].md`
代理开始手动验证。”

---

## 协作协议

- **永远不要将 NOT RUN 视为自动失败** - 将其记录为 NOT RUN 并让
  开发人员手动确认状态。未经确认的 NOT RUN 有助于
  通过但有警告，不要失败。
- **切勿自动修复故障** - 报告故障并说明必须解决的问题。
  不要尝试编辑源代码或测试文件。
- **“带警告通过”不会阻止 QA 交接** — 它记录建议
  `/story-done` 后续的差距。
- **`quick` 参数** 跳过阶段 3（覆盖扫描）和阶段 4 批次 3。
  修复特定故障后使用它进行快速重新检查。
- 使用 `AskUserQuestion` 进行所有手动烟雾检查验证。
- **永远不要在没有询问的情况下写报告**——第 6 阶段要求明确
  在创建任何文件之前进行批准。
