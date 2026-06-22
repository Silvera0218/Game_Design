---
name: test-helpers
description: "为项目的测试套件生成特定于引擎的测试帮助程序库。读取现有测试模式并生成带有针对项目系统定制的断言实用程序、工厂函数和模拟对象的 tests/helpers/。减少新测试文件中的样板文件。"
---

# 测试助手

当常见的设置、拆卸、
断言模式被抽象为助手。该技能会产生一个
`tests/helpers/` 库根据项目的实际引擎、语言量身定制，
和系统——因此每个开发人员都会编写更少的样板文件和更多的断言。

**输出：** `tests/helpers/` 目录，其中包含特定于引擎的帮助程序文件

**何时运行：**
- `/test-setup`搭建框架后（第一次）
- 当多个测试文件重复相同的设置样板时
- 当开始为新系统编写测试时

---

## 1. 解析参数

**Modes:**
- `/test-helpers [system-name]` — 为特定系统生成帮助程序
  (e.g., `/test-helpers combat`)
- `/test-helpers all` — 为所有带有测试文件的系统生成帮助程序
- `/test-helpers scaffold` — 仅生成基本帮助程序库（无
  系统特定的助手）；第一次运行时使用它
- 无参数 - 如果不存在帮助程序，则运行 `scaffold`，否则运行 `all`

---

## 2. 检测引擎和语言

Read `.codex/docs/technical-preferences.md` 并提取：
- `Engine:` 值
- `Language:` 值
- 测试部分的 `Framework:`

如果未配置引擎：“引擎未配置。首先运行 `/setup-engine`。”

---

## 3.加载现有测试模式

扫描测试目录以查找已在使用的模式：

```
Glob pattern="tests/**/*_test.*" (all test files)
```

对于代表性样本（最多 5 个文件），读取测试文件并提取：
- 设置模式（如何编写 `before_each` / `setUp` / 夹具）
- 常见断言模式（最常断言的内容）
- 对象创建模式（游戏对象或场景如何在测试中实例化）
- Mock/stub 模式（如何替换依赖项）

这确保生成的助手与项目的现有样式匹配，而不是
通用模板。

另请阅读：
- `design/gdd/systems-index.md` — 了解存在哪些系统
- 范围内 GDD(s) — 了解哪些数据类型和值需要测试
- `docs/architecture/tr-registry.yaml` — 将需求映射到测试系统

---

## 4. 生成特定于引擎的助手

### Godot 4 (GDUnit4 / GDScript)

**基础助手** (`tests/helpers/game_assertions.gd`)：

```gdscript
## Game-specific assertion utilities for [Project Name] tests.
## Extends GdUnitAssertions with domain-specific helpers.
##
## Usage:
##   var assert = GameAssertions.new()
##   assert.health_in_range(entity, 0, entity.max_health)

class_name GameAssertions
extends RefCounted

## Assert a value is within the inclusive range [min_val, max_val].
## Use for any formula output that has defined bounds in a GDD.
static func assert_in_range(
    value: float,
    min_val: float,
    max_val: float,
    label: String = "value"
) -> void:
    assert(
        value >= min_val and value <= max_val,
        "%s %.2f is outside expected range [%.2f, %.2f]" % [label, value, min_val, max_val]
    )

## Assert a signal was emitted during a callable block.
## Usage: assert_signal_emitted(entity, "health_changed", func(): entity.take_damage(10))
static func assert_signal_emitted(
    obj: Object,
    signal_name: String,
    action: Callable
) -> void:
    var emitted := false
    obj.connect(signal_name, func(_args): emitted = true)
    action.call()
    assert(emitted, "Expected signal '%s' to be emitted, but it was not." % signal_name)

## Assert that a callable does NOT emit a signal.
static func assert_signal_not_emitted(
    obj: Object,
    signal_name: String,
    action: Callable
) -> void:
    var emitted := false
    obj.connect(signal_name, func(_args): emitted = true)
    action.call()
    assert(not emitted, "Expected signal '%s' NOT to be emitted, but it was." % signal_name)

## Assert a node exists at path within a parent.
static func assert_node_exists(parent: Node, path: NodePath) -> void:
    assert(
        parent.has_node(path),
        "Expected node at path '%s' to exist." % str(path)
    )
```

**工厂助手** (`tests/helpers/game_factory.gd`)：

```gdscript
## Factory functions for creating test game objects.
## Returns minimal objects configured for unit testing (no scene tree required).
##
## Usage: var player = GameFactory.make_player(health: 100)

class_name GameFactory
extends RefCounted

## Create a minimal player-like object for testing.
## Override fields as needed.
static func make_player(health: int = 100) -> Node:
    var player = Node.new()
    player.set_meta("health", health)
    player.set_meta("max_health", health)
    return player
```

**场景助手** (`tests/helpers/scene_runner_helper.gd`)：

```gdscript
## Utilities for scene-based integration tests.
## Wraps GdUnitSceneRunner for common patterns.

class_name SceneRunnerHelper
extends GdUnitTestSuite

## Load a scene and wait one frame for _ready() to complete.
func load_scene_and_wait(scene_path: String) -> Node:
    var scene = load(scene_path).instantiate()
    add_child(scene)
    await get_tree().process_frame
    return scene
```

---

### Unity（NUnit / C#）

**基础助手** (`tests/helpers/GameAssertions.cs`)：

```csharp
using NUnit.Framework;
using UnityEngine;

/// <summary>
/// Game-specific assertion utilities for [Project Name] tests.
/// Extends NUnit's Assert with domain-specific helpers.
/// </summary>
public static class GameAssertions
{
    /// <summary>
    /// Assert a value is within an inclusive range [min, max].
    /// Use for any formula output defined in GDD Formulas sections.
    /// </summary>
    public static void AssertInRange(float value, float min, float max, string label = "value")
    {
        Assert.That(value, Is.InRange(min, max),
            $"{label} ({value:F2}) is outside expected range [{min:F2}, {max:F2}]");
    }

    /// <summary>Assert a UnityEvent or C# event was raised during an action.</summary>
    public static void AssertEventRaised(ref bool wasCalled, System.Action action, string eventName)
    {
        wasCalled = false;
        action();
        Assert.IsTrue(wasCalled, $"Expected event '{eventName}' to be raised, but it was not.");
    }

    /// <summary>Assert a component exists on a GameObject.</summary>
    public static void AssertHasComponent<T>(GameObject obj) where T : Component
    {
        var component = obj.GetComponent<T>();
        Assert.IsNotNull(component,
            $"Expected GameObject '{obj.name}' to have component {typeof(T).Name}.");
    }
}
```

**工厂助手** (`tests/helpers/GameFactory.cs`)：

```csharp
using UnityEngine;

/// <summary>
/// Factory methods for creating minimal test objects without loading scenes.
/// </summary>
public static class GameFactory
{
    /// <summary>Create a minimal GameObject with a named component for testing.</summary>
    public static GameObject MakeGameObject(string name = "TestObject")
    {
        var go = new GameObject(name);
        return go;
    }

    /// <summary>
    /// Create a ScriptableObject of type T for data-driven tests.
    /// Dispose with Object.DestroyImmediate after test.
    /// </summary>
    public static T MakeScriptableObject<T>() where T : ScriptableObject
    {
        return ScriptableObject.CreateInstance<T>();
    }
}
```

---

### Unreal 引擎 (C++)

**基础助手** (`tests/helpers/GameTestHelpers.h`)：

```cpp
#pragma once

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"

/**
 * Game-specific assertion macros and helpers for [Project Name] automation tests.
 * Include in any test file that needs domain-specific assertions.
 *
 * Usage:
 *   GAME_TEST_ASSERT_IN_RANGE(TestName, DamageValue, 10.0f, 50.0f, TEXT("Damage"));
 */

// Assert a float value is within inclusive range [Min, Max]
#define GAME_TEST_ASSERT_IN_RANGE(TestName, Value, Min, Max, Label) \
    TestTrue( \
        FString::Printf(TEXT("%s (%.2f) in range [%.2f, %.2f]"), Label, Value, Min, Max), \
        (Value) >= (Min) && (Value) <= (Max) \
    )

// Assert a UObject pointer is valid (not null, not garbage collected)
#define GAME_TEST_ASSERT_VALID(TestName, Ptr, Label) \
    TestTrue( \
        FString::Printf(TEXT("%s is valid"), Label), \
        IsValid(Ptr) \
    )

// Assert an Actor is in the world (spawned successfully)
#define GAME_TEST_ASSERT_SPAWNED(TestName, ActorPtr, ClassName) \
    TestNotNull( \
        FString::Printf(TEXT("Spawned actor of class %s"), TEXT(#ClassName)), \
        ActorPtr \
    )

/**
 * Helper to create a minimal test world.
 * Remember to call World->DestroyWorld(false) in teardown.
 */
namespace GameTestHelpers
{
    inline UWorld* CreateTestWorld(const FString& WorldName = TEXT("TestWorld"))
    {
        UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
        FWorldContext& WorldContext = GEngine->CreateNewWorldContext(EWorldType::Game);
        WorldContext.SetCurrentWorld(World);
        return World;
    }
}
```

---

## 5. 生成系统特定的助手

对于 `[system-name]` 或 `all` 模式，为每个系统生成一个帮助程序：

Read 系统的GDD 提取：
- 数据类型（实体类型、组件名称）
- 公式变量及其界限
- 边缘案例中提到的常见测试场景

生成带有工厂函数的`tests/helpers/[system]_factory.[ext]`
特定于该系统的对象。

`combat` 系统 (Godot/GDScript) 的示例模式：

```gdscript
## Factory and assertion helpers for Combat system tests.
## Generated by /test-helpers combat on [date].
## Based on: design/gdd/combat.md

class_name CombatTestFactory
extends RefCounted

const DAMAGE_MIN := 0
const DAMAGE_MAX := 999  # From GDD: damage formula upper bound

## Create a minimal attacker object for damage formula tests.
static func make_attacker(attack: float = 10.0, crit_chance: float = 0.0) -> Node:
    var attacker = Node.new()
    attacker.set_meta("attack", attack)
    attacker.set_meta("crit_chance", crit_chance)
    return attacker

## Create a minimal target object for damage receive tests.
static func make_target(defense: float = 0.0, health: float = 100.0) -> Node:
    var target = Node.new()
    target.set_meta("defense", defense)
    target.set_meta("health", health)
    target.set_meta("max_health", health)
    return target

## Assert damage output is within GDD-specified bounds.
static func assert_damage_in_bounds(damage: float) -> void:
    GameAssertions.assert_in_range(damage, DAMAGE_MIN, DAMAGE_MAX, "damage")
```

---

## 6. Write 输出

总结一下将要创建的内容：

```
## Test Helpers to Create

Base helpers (engine: [engine]):
- tests/helpers/game_assertions.[ext]
- tests/helpers/game_factory.[ext]
[engine-specific extras]

System helpers ([mode]):
- tests/helpers/[system]_factory.[ext]  ← from [system] GDD
```

问：“我可以将这些帮助文件写入 `tests/helpers/` 吗？”

**切勿覆盖现有文件。** 如果文件已存在，则报告：
“正在跳过 `[path]` — 已存在。如果需要，请手动删除该文件
regenerated."

写入后：结论：**完成** — 创建辅助文件。

“已创建帮助文件。要在测试中使用它们：
- Godot：`class_name` 是自动导入的 — 无需显式导入
- Unity：添加 `using` 指令或引用测试程序集
- Unreal: `#include \"tests/helpers/GameTestHelpers.h\"`"

---

## 协作协议

- **永远不要覆盖现有的助手** - 它们可能包含手写的
  定制。只生成尚不存在的新文件
- **生成的代码是一个起点** - 生成的工厂函数使用
  为简单起见，元数据模式；适应实际班级结构一次
  该代码存在
- **帮助程序应反映 GDD** — 帮助程序中的界限和常量应
  追溯到 GDD 公式部分，而不是发明值
- **写入前询问** — 在 `tests/` 中创建文件之前始终确认

## 下一步

- 如果测试框架尚未搭建，请运行 `/test-setup`。
- 使用 `/dev-story` 实现故事 - 帮助减少新测试文件中的样板文件。
- 运行 `/skill-test` 以验证可能需要帮助者覆盖的其他技能。
