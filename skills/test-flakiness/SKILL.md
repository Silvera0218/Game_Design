---
name: test-flakiness
description: "通过读取 CI 运行日志或测试结果历史记录来检测非确定性（片状）测试。汇总每次测试的通过率，识别间歇性故障，建议隔离或修复，并维护不稳定的测试注册表。最好在抛光阶段或多次 CI 运行后运行。"
---

# 测试片状检测

片状测试是指在没有任何代码的情况下有时会通过有时会失败的测试
改变。从某些方面来说，不稳定的测试比没有测试更糟糕——它们可以训练团队
忽略红色 CI 运行，掩盖真正的故障。这种技能可以识别他们，
解释可能的原因，并建议是否隔离或修复每个原因。

**输出：**更新的`tests/regression-suite.md`隔离部分+可选
`production/qa/flakiness-report-[date].md`

**何时运行：**
- 抛光阶段（测试已进行多次；统计信号可靠）
- 当开发人员开始将 CI 故障视为“可能不稳定”时
- `/regression-suite` 识别出需要诊断的隔离测试后

---

## 1. 解析参数

**Modes:**
- `/test-flakiness [ci-log-path]` — 分析特定的 CI 运行日志文件
- `/test-flakiness scan` — 扫描 `.github/` 中所有可用的 CI 日志或
  标准日志输出目录
- `/test-flakiness registry` — 读取现有的 regression-suite.md 隔离区
  部分并为已知的片状测试提供修复指南
- 无参数 — 自动检测：如果 CI 日志可访问，则运行 `scan`，否则
  `registry`

---

## 2. 找到CI日志数据

### 选项 A — GitHub 操作（首选）

检查测试结果工件：
```bash
ls -t .github/ 2>/dev/null
ls -t test-results/ 2>/dev/null
```

对于 Godot 项目：GdUnit4 输出与 JUnit 格式兼容的 XML 结果。
检查 `test-results/` 中的 `.xml` 文件。

对于 Unity 项目：game-ci 测试运行程序将 NUnit XML 输出到 `test-results/`
by default.

对于 Unreal 项目：自动化日志转到 `Saved/Logs/`。 Grep 为
`Result: Success` 和 `Result: Fail` 模式。

### 选项 B — 本地日志文件

如果提供了路径参数，则直接读取该文件。

### 选项 C — 无可用日志数据

如果没有找到日志：
> “未找到 CI 日志数据。要检测片状测试，此技能需要测试结果
> 多次运行的历史记录。选项：
> 1. 运行测试套件至少3次并收集输出日志
> 2.检查CI管道输出并将日志保存到`test-results/`
> 3. 运行 `/test-flakiness registry` 来检查已标记为不稳定的测试
>    in `tests/regression-suite.md`"

停下来询问用户要选择哪个选项。

---

## 3. 解析测试结果

对于找到的每个 CI 日志或结果文件，解析：

**JUnit XML 格式** (GdUnit4 / Unity)：
- Grep 用于 `<testcase name=` 获取测试名称
- Grep 用于 `<failure` 或 `<error` 识别故障
- 解析 `classname` 和 `name` 属性以获得完整的测试标识符

**纯文本日志**：
- Grep 对于 pass/fail 模式：
  - Godot：`PASSED` / `FAILED` 与测试名称相邻
  - Unreal: `Result: Success` / `Result: Fail`
  - Unity: `Test passed` / `Test failed`

建表：`test_id → [run1_result, run2_result, run3_result, ...]`

---

## 4. 识别不稳定的测试

如果某个测试出现在结果历史记录中同时具有 PASS 和 PASS 则该测试是“不稳定的”
不同运行之间没有代码更改的 FAIL 结果。

片状阈值：
- **高片状性**：超过 25% 的运行失败 — 立即隔离
- **中度不稳定**：5-25% 的运行失败 - 尽快调查并修复
- **Low/suspected 片状**：1-5% 的运行失败 — 监控；可能是
  真正罕见的失败

对于每个不稳定测试，对可能的原因进行分类：

### 原因分类

| Cause | Symptoms | 固定方向 |
|-------|----------|---------------|
| **定时/异步** | 等待信号或定时器后失败；通过率与系统负载相关 | 添加显式await/synchronisation；避免基于时间的延误 |
| **订单依赖性** | 在特定的其他测试后运行时失败；孤立地通过 | 添加适当的setup/teardown；确保测试隔离 |
| **随机种子** | 间歇性失败，无规律；涉及RNG | 传递显式种子；不要在测试中使用 `randf()` |
| **资源泄漏** | 稍后在测试运行中失败的频率更高 | 修复拆卸中的清理问题；检查孤立节点 (Godot) 或对象处置 (Unity) |
| **外部状态** | 当先前测试中存在文件、场景或全局时失败 | 将测试与文件系统隔离；使用内存中的模拟 |
| **浮点** | 类似 `== 0.5` 的比较失败 | 使用 epsilon 比较（`is_equal_approx`、`Assert.AreApproximately`） |
| **Scene/prefab 负载竞赛** | 场景尚未准备好时失败 | 实例化后等待一帧；使用 `await get_tree().process_frame` |

使用 Grep 检查测试文件的定时调用、randf、全局状态访问、
或对浮点数进行相等比较以缩小原因范围。

---

## 5. 建议行动

对于每个片状测试：

**检疫（高片状）：**
> “立即隔离此测试。通过添加在 CI 中禁用它
> `@pytest.mark.skip` / `[Ignore]` / `GdUnitSkip` 注释。登录
> `tests/regression-suite.md` 隔离部分。该测试现在仅供选择加入。
> 在取消隔离之前解决根本原因。”

**尽快调查并修复（中等）：**
> “此测试间歇性不可靠。根本原因似乎是 [cause]。
> 建议修复：[specific fix based on cause classification]。不要隔离
> 然而——直接修复测试。”

**监视器（Low/suspected）：**
> “此测试显示出可疑的不稳定情况。之前收集更多运行数据
> 隔离。在回归套件中将其记为“可疑”。”

---

## 6. 生成报告

### 谈话中总结

```
## Flakiness Detection Results

**Runs analysed**: [N]
**Tests tracked**: [N]

### Flaky Tests Found

| Test | System | Fail Rate | Likely Cause | Recommendation |
|------|--------|-----------|--------------|----------------|
| [test_name] | [system] | [N]% | Timing | Quarantine + fix async |
| [test_name] | [system] | [N]% | Float comparison | Fix: use epsilon compare |
| [test_name] | [system] | [N]% | Order dependency | Investigate teardown |

### Clean Tests (no flakiness detected)

[N] tests ran across [N] runs with consistent results — no flakiness detected.

### Data Limitations

[Note if fewer than 5 runs were available — fewer runs = less statistical confidence]
```

---

## 7.更新回归套件+可选报告文件

问：“我可以更新 `tests/regression-suite.md` 的隔离部分吗？
发现了片状测试？”

如果是：使用 `Edit` 将条目附加到隔离测试表中。
切勿删除现有的隔离条目 — 仅添加新条目。

（单独）询问：“我可以写一份完整的不稳定报告给
`production/qa/flakiness-report-[date].md`？”

完整的报告包括每次测试分析以及原因详细信息和
特定于引擎的修复片段。

写完后：

- 对于每个隔离测试：“将特定于引擎的跳过注释添加到
  在 CI 中禁用此测试。修复根本原因后重新启用。”
- 对于符合修复资格的测试：“[test] 的修复很简单 -
  将 [N] 行上的相等比较更改为使用 `is_equal_approx`。”
- 摘要：“应用所有隔离注释后，CI 应运行绿色。
  在发布之前安排 [N] 隔离测试的修复工作。”

---

## 协作协议

- **永远不要删除测试文件** - 隔离意味着注释+列出，而不是删除
- **统计置信度很重要** — 运行 < 3 次，将结果标记为
  “疑似”而非“确诊”；询问是否有更多运行数据可用
- **修复始终是目标** — 隔离是暂时的；表面修复
  即使建议隔离时也有方向
- **写作前询问** - 回归套件更新和报告
  文件需要明确批准。写入时：判决：**完成** — 已写入不稳定报告。拒绝时：判决：**被阻止** - 用户拒绝写入。
- **CI 中的不稳定是一个团队问题** — 列出列表并推荐
  行动明确；不要在团队不知情的情况下默默隔离
