---
name: test-setup
description: "为项目引擎搭建测试框架和 CI/CD 管道。创建测试/目录结构、特定于引擎的测试运行程序配置和 GitHub 操作工作流程。在第一个冲刺开始之前的技术设置阶段运行一次。"
---

# 测试设置

该技能为项目搭建了自动化测试基础设施。
它检测配置的引擎，生成适当的测试运行程序
配置，创建标准目录布局，并连接 CI/CD
所以每次推送都会运行测试。

在任何实施之前的技术设置阶段运行一次
开始。在冲刺开始时安装的测试框架需要 30 分钟。
在 4 个 sprint 中安装的测试框架需要 3 个 sprint。

**输出：** `tests/` 目录结构 + `.github/workflows/tests.yml`

---

## 第 1 阶段：检测引擎和现有状态

1. **Read 引擎配置**：
   - Read `.codex/docs/technical-preferences.md` 并提取 `Engine:` 值。
   - 如果引擎未配置 (`[TO BE CONFIGURED]`)，则停止：
     “引擎未配置。首先运行 `/setup-engine`，然后重新运行 `/test-setup`。”

2. **检查现有的测试基础设施**：
   - Glob `tests/` — 该目录是否存在？
   - Glob `tests/unit/` 和 `tests/integration/` — 子目录是否存在？
   - Glob `.github/workflows/` — CI 工作流程文件是否存在？
   - Glob `tests/gdunit4_runner.gd` (Godot) 或 `tests/EditMode/` (Unity) 或
     `Source/Tests/` (Unreal) 用于引擎特定的工件。

3. **报告调查结果**：
   - “引擎：[engine]。测试目录：[found / not found]。CI工作流程：[found / not found]。”
   - 如果一切都已存在并且 `force` 参数未传递：
     “测试基础设施似乎已就位。使用 `/test-setup force` 重新运行
     重生。继续操作不会覆盖现有的测试文件。”

如果传递了 `force` 参数，则跳过“已存在”提前退出并
继续 - 但仍然不覆盖给定路径中已存在的文件。
仅创建丢失的文件。

---

## 第二阶段：当前计划

根据检测到的发动机和现有状态，提出计划：

```
## Test Setup Plan — [Engine]

I will create the following (skipping any that already exist):

tests/
  unit/           — Isolated unit tests for formulas, state, and logic
  integration/    — Cross-system tests and save/load round-trips
  smoke/          — Critical path test list (15-minute manual gate)
  evidence/       — Screenshot and manual test sign-off records
  README.md       — Test framework documentation

[Engine-specific files — see per-engine details below]

.github/workflows/tests.yml  — CI: run tests on every push to main

Estimated time: ~5 minutes to create all files.
```

问：“我可以创建这些文件吗？我不会覆盖任何测试文件
这些路径上已经存在了。”

未经批准不得继续。

---

## 第 3 阶段：创建目录结构

批准后，创建以下文件：

### `tests/README.md`

```markdown
# Test Infrastructure

**Engine**: [engine name + version]
**Test Framework**: [GdUnit4 | Unity Test Framework | UE Automation]
**CI**: `.github/workflows/tests.yml`
**Setup date**: [date]

## Directory Layout

```
tests/
  unit/ # 独立的单元测试（公式、状态机、逻辑）
  集成/#跨系统和save/load测试
  Smoke/ # /smoke-check 门的关键路径测试列表
  证据/ # 截图日志和手动测试签核记录
```

## Running Tests

[Engine-specific command — see below]

## Test Naming

- **Files**: `[system]_[feature]_test.[ext]`
- **Functions**: `test_[scenario]_[expected]`
- **Example**: `combat_damage_test.gd` → `test_base_attack_returns_expected_damage()`

## Story Type → Test Evidence

| Story Type | Required Evidence | Location |
|---|---|---|
| Logic | Automated unit test — must pass | `tests/unit/[system]/` |
| Integration | Integration test OR playtest doc | `tests/integration/[system]/` |
| Visual/Feel | Screenshot + lead sign-off | `tests/evidence/` |
| UI | Manual walkthrough OR interaction test | `tests/evidence/` |
| Config/Data | Smoke check pass | `production/qa/smoke-*.md` |

## CI

Tests run automatically on every push to `main` and on every pull request.
A failed test suite blocks merging.
```
```

### Engine-specific files

#### Godot 4 (`Engine: Godot`)

Create `tests/gdunit4_runner.gd`:

```gdscript
# GdUnit4 测试运行程序 — 由 CI 和 /smoke-check 调用
# 用法：godot --headless --script tests/gdunit4_runner.gd
扩展场景树

func _init() -> void:
    var runner := load("res://addons/gdunit4/GdUnitRunner.gd")
    如果跑步者==空：
        Push_error("未找到 GdUnit4。通过 AssetLib 或 addons/. 安装")
        quit(1)
        return
    var 实例 = runner.new()
    实例.run_tests()
    quit(0)
```

Create `tests/unit/.gdignore_placeholder` with content:
`# Unit tests go here — one subdirectory per system (e.g., tests/unit/combat/)`

Create `tests/integration/.gdignore_placeholder` with content:
`# Integration tests go here — one subdirectory per system`

Note in the README: **Installing GdUnit4**
```
1. 打开Godot → AssetLib → 搜索“GdUnit4” → 下载并安装
2. 启用插件：项目→项目设置→插件→GdUnit4 ✓
3. 重新启动编辑器
4. 验证：res://addons/gdunit4/ 存在
```

#### Unity (`Engine: Unity`)

Create `tests/EditMode/` placeholder file `tests/EditMode/README.md`:
```markdown
# Edit 模式测试
无需进入播放模式即可运行的单元测试。
用于纯逻辑：公式、状态机、数据验证。
所需的装配定义：`tests/EditMode/EditModeTests.asmdef`
```

Create `tests/PlayMode/README.md`:
```markdown
# 播放模式测试
在真实游戏场景中运行的集成测试。
用于跨系统交互、物理和协程。
所需的程序集定义：`tests/PlayMode/PlayModeTests.asmdef`
```

Note in the README: **Enabling Unity Test Framework**
```
窗口 → 常规 → 测试运行器
（Unity 测试框架默认包含在 Unity 2019+ 中）
```

#### Unreal Engine (`Engine: Unreal` or `Engine: UE5`)

Create `Source/Tests/README.md`:
```markdown
# Unreal 自动化测试
测试使用 UE 自动化测试框架。
运行方式：会话前端 → 自动化 → 选择“MyGame”。测试
或者无头：UnrealEditor -nullrhi -ExecCmds="Automation RunTests MyGame.; Quit"

测试类命名：F[SystemName]Test
测试类别命名：“MyGame.[System].[Feature]”
```

---

## Phase 4: Create CI/CD Workflow

### Godot 4

Create `.github/workflows/tests.yml`:

```yaml
名称： 自动化测试

on:
  push:
    分支机构：[main]
  拉请求：
    分支机构：[main]

jobs:
  test:
    名称：运行 GdUnit4 测试
    运行：ubuntu-latest

    steps:
      - 名称：结帐
        用途：actions/checkout@v4
        with:
          lfs: 正确

      - 名称：运行 GdUnit4 测试
        用途：MikeSchulze/gdUnit4-action@v1
        with:
          godot 版本：'[VERSION FROM docs/engine-reference/godot/VERSION.md]'
          paths: |
            tests/unit
            tests/integration
          报告名称：测试结果

      - 名称：上传测试结果
        if: always()
        用途：actions/upload-artifact@v4
        with:
          名称：测试结果
          路径：报告/
```

### Unity

Create `.github/workflows/tests.yml`:

```yaml
名称： 自动化测试

on:
  push:
    分支机构：[main]
  拉请求：
    分支机构：[main]

jobs:
  test:
    名称：运行 Unity 测试
    运行：ubuntu-latest

    steps:
      - 名称：结帐
        用途：actions/checkout@v4
        with:
          lfs: 正确

      - 名称：运行 Edit 模式测试
        用途：game-ci/unity-test-runner@v4
        env:
          UNITY_LICENSE：${{ secrets.UNITY_LICENSE }}
        with:
          测试模式：编辑模式
          工件路径：test-results/editmode

      - 名称：运行播放模式测试
        用途：game-ci/unity-test-runner@v4
        env:
          UNITY_LICENSE：${{ secrets.UNITY_LICENSE }}
        with:
          测试模式：播放模式
          工件路径：test-results/playmode

      - 名称：上传测试结果
        if: always()
        用途：actions/upload-artifact@v4
        with:
          名称：测试结果
          路径：测试结果/
```

Note: Unity CI requires a `UNITY_LICENSE` secret. Add to GitHub repository
secrets before the first CI run.

### Unreal Engine

Create `.github/workflows/tests.yml`:

```yaml
名称： 自动化测试

on:
  push:
    分支机构：[main]
  拉请求：
    分支机构：[main]

jobs:
  test:
    名称：运行 UE 自动化测试
    running-on: self-hosted # UE 需要安装了编辑器的本地运行器

    steps:
      - 名称：结帐
        用途：actions/checkout@v4
        with:
          lfs: 正确

      - 名称：运行自动化测试
        run: |
          “$UE_EDITOR_PATH”“${{ github.workspace }}/[ProjectName].uproject”\
            -nullrhi -nosound \
            -ExecCmds="Automation RunTests MyGame.;退出" \
            -log-无人值守
        外壳：bash

      - 名称：上传日志
        if: always()
        用途：actions/upload-artifact@v4
        with:
          名称：测试日志
          路径：Saved/Logs/
```

Note: UE CI requires a self-hosted runner with Unreal Editor installed.
Set the `UE_EDITOR_PATH` environment variable on the runner.

---

## Phase 5: Create Smoke Test Seed

Create `tests/smoke/critical-paths.md`:

```markdown
# 冒烟测试：关键路径

**目的**：在任何 QA 移交之前，在 15 分钟内运行这 10-15 次检查。
**运行通过**：`/smoke-check`（读取此文件）
**更新**：在实施新的核心系统时添加新条目。

## 核心稳定性（始终运行）

1. 游戏启动至主菜单而不会崩溃
2. 可以从主菜单开始新游戏/会话
3. 主菜单响应所有输入而不会冻结

## 核心机制（每个冲刺更新）

<!-- 在实施时为每个冲刺添加主要机制 -->
<!-- 示例：“玩家可以移动、跳跃，并且摄像机正确跟随” -->
4. [主要机制——第一个核心系统实现时更新]

## 数据完整性

5. 保存游戏完成且没有错误（保存系统实施后）
6. 加载游戏恢复正确状态（一旦加载系统实现）

## Performance

7. 目标硬件上没有明显的帧速率下降（60fps 目标）
8. 玩 5 分钟后内存不会增长（一旦实现核心循环）
```

---

## Phase 6: Post-Setup Summary

After writing all files, report:

```
为 [engine] 创建的测试基础设施。

创建的文件：
- tests/README.md
- tests/unit/（目录）
- tests/integration/（目录）
- tests/smoke/critical-paths.md
- tests/evidence/（目录）
[engine-specific files]
- .github/workflows/tests.yml

后续步骤：
1. [特定于引擎的安装步骤，例如“通过 AssetLib 安装 GdUnit4”]
2. Write 您的第一个测试：创建 tests/unit/[first-system]/[system]_test.[ext]
3. 在第一次冲刺之前运行 `/qa-plan sprint` 对故事进行分类并设置
   测试证据要求
4. 每次 QA 切换之前的 `/smoke-check`

门注：/gate-check 技术设置 → 预生产现在需要：
- 带有unit/和integration/子目录的tests/目录
- .github/workflows/tests.yml
- 至少一个示例测试文件
运行 /test-setup 并在继续之前编写一个示例测试。

结论：**完成** — 测试框架搭建完毕并连接 CI/CD。
```

---

## Collaborative Protocol

- **Never overwrite existing test files** — only create files that are missing.
  If a test runner file exists, leave it as-is.
- **Always ask before creating files** — Phase 2 requires explicit approval.
- **Engine detection is non-negotiable** — if the engine is not configured,
  stop and redirect to `/setup-engine`. Do not guess.
- **`force` flag skips the "already exists" early-exit but never overwrites.**
  It means "create any missing files even if the directory already exists."
- For Unity CI, note that the `UNITY_LICENSE` secret must be configured
  manually. Do not attempt to automate license management.
