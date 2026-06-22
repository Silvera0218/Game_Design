# Unity Reference

Read this when implementing or reviewing Unity/C# gameplay, editor tooling, scenes, prefabs, packages, tests, project architecture, performance, or build issues.

## Recon First

Before editing a Unity project, locate and inspect:

- `ProjectSettings/ProjectVersion.txt`
- `Packages/manifest.json`
- `Assets/` structure and naming conventions
- `.asmdef` files
- Existing gameplay scripts near the requested feature
- Scenes and prefabs relevant to the task
- Test folders and CI/build scripts

Do not assume the render pipeline, input system, serialization pattern, folder layout, or dependency injection style. Follow the project.

## Greenfield Structure

When no structure exists, prefer a simple layout:

```text
Assets/
  _Project/
    Art/
    Audio/
    Materials/
    Prefabs/
    Scenes/
    ScriptableObjects/
    Scripts/
      Runtime/
      Editor/
      Tests/
    Settings/
```

Use asmdefs when the project already uses them or when tests/editor/runtime separation matters.

## C# Gameplay Patterns

- Use `MonoBehaviour` for scene-bound behavior and plain C# classes for deterministic gameplay logic.
- Use `ScriptableObject` for designer-tuned data, ability definitions, item definitions, spawn tables, and balance configs.
- Prefer `[SerializeField] private` fields with clear ranges/tooltips over public mutable fields.
- Keep expensive work out of `Update`; cache components, use events, or tick only when active.
- Use `FixedUpdate` for physics writes and `Update` for input reads unless the project has a specific input architecture.
- Avoid `FindObjectOfType`, scene-wide searches, and allocations in hot paths.
- Use object pooling for frequent spawn/despawn loops.
- Keep save data separate from runtime component state.
- Make important tuning values visible in the inspector and safe via validation.

Example component shape:

```csharp
using System;
using UnityEngine;

[DisallowMultipleComponent]
public sealed class Health : MonoBehaviour
{
    [SerializeField, Min(1)] private int maxHealth = 3;

    public int Current { get; private set; }
    public int Max => maxHealth;
    public event Action<int, int> Changed;
    public event Action Died;

    private void Awake()
    {
        Current = maxHealth;
        Changed?.Invoke(Current, Max);
    }

    public void ApplyDamage(int amount)
    {
        if (amount <= 0 || Current <= 0) return;

        Current = Mathf.Max(0, Current - amount);
        Changed?.Invoke(Current, Max);

        if (Current == 0)
        {
            Died?.Invoke();
        }
    }
}
```

## Scenes And Prefabs

- Prefer editor scripts or Unity APIs for large scene/prefab changes when possible.
- Avoid hand-editing `.unity` and `.prefab` YAML unless the change is small, reviewed, and version-control friendly.
- Keep prefab responsibilities narrow. Compose behavior from components.
- Keep temporary debug objects clearly named and removable.
- Do not edit generated folders such as `Library/`, `Temp/`, `Obj/`, or build output unless explicitly requested.

## UI

- Use the UI system already present: uGUI, UI Toolkit, custom world-space UI, or a project framework.
- Define navigation/focus states for controller and keyboard.
- Respect safe areas, localization expansion, dynamic text, and aspect ratios.
- Keep HUD updates event-driven when practical.
- For real-time games, prioritize glanceable state over decorative panels.

## Tests And Verification

Prefer this verification order:

1. Run existing automated tests.
2. Run Unity Test Framework EditMode tests for pure logic.
3. Run PlayMode tests for scene/prefab integration.
4. Trigger a Unity compile or batch-mode test run if Unity is available.
5. If Unity is unavailable, run static checks possible in the repo and clearly state the limitation.

Common Windows batch command pattern:

```powershell
Unity.exe -batchmode -quit -projectPath "<project>" -runTests -testPlatform EditMode -testResults "<project>\TestResults.xml"
```

After compile/test failures, inspect Unity logs and fix root causes before adding more code.

## Performance Baselines

- Watch GC allocations in per-frame paths.
- Pool projectiles, VFX, damage numbers, and temporary UI.
- Avoid per-frame LINQ and string formatting in gameplay loops.
- Prefer data-driven spawn/config tables for balancing.
- Budget particles, lights, post-processing, shadows, and overdraw according to platform.
- Keep mobile/touch constraints explicit when relevant.

## Final Report

For implementation tasks, report:

- Files changed
- Gameplay behavior added or changed
- Inspector setup or scene/prefab steps still required
- Tests/compile commands run and results
- Known limitations or tuning values the designer should adjust
