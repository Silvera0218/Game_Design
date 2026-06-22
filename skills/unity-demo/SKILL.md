---
name: unity-demo
description: "Create isolated Unity demos and playable prototypes. Use when the user asks for a Unity demo/prototype, playable Unity scene, MonoBehaviour demo, mechanic feel test, or any validation that depends on Unity Play Mode, 2D/3D physics, input, camera feel, animation, Timeline, NavMesh, particles/VFX, shaders/materials, prefabs, scene composition, or Inspector tuning. Produces disposable demo code under Assets/Prototypes/ or prototypes/ without touching production systems unless explicitly requested."
---

# Unity Demo

Build a disposable Unity demo that answers one concrete design or feel question. The output is runnable evidence, not production code.

## Startup

Read project context before editing:

- `AGENTS.md`
- `.codex/docs/technical-preferences.md` if present
- Relevant brief/GDD/quick spec/story if the user points to one
- `ProjectSettings/ProjectVersion.txt`, `Packages/manifest.json`, `Assets/`, and `*.asmdef` to confirm Unity layout
- `references/local-unity-environment.md` if present, to use known local Editor paths and installed modules

If the user requests GitHub/high-star references, or the mechanic is nontrivial, read `references/github-reference-sampling.md` before planning.

## Triage

Define the core question in one sentence, then choose the smallest Unity artifact that can answer it:

- **Script-only demo**: one or more `MonoBehaviour` scripts plus setup instructions.
- **Scene demo**: a generated or manually assembled prototype scene with primitives, placeholder materials, prefabs, and scripts.
- **Editor builder demo**: an `Editor` script that creates the demo scene/assets from Unity APIs, useful when scene YAML would be fragile.
- **Not a demo**: stop and recommend design/architecture/story work if the request requires live services, production save data, real account flow, permanent package changes, or broad production refactors.

Prefer Unity demo over HTML when the question depends on Play Mode feel, physics, camera, animation, VFX, shaders, scene scale, Inspector tuning, or controller/keyboard input.

## Version Compatibility

Use the Unity project version as the authority when `ProjectSettings/ProjectVersion.txt` exists. If the requested project version differs from the locally installed Editor, warn before running Unity CLI and prefer generating isolated files plus manual run steps.

For Unity 2022.3 LTS projects:

- Use conservative Unity C# syntax and avoid newer .NET APIs unless the project already uses them.
- Prefer built-in `Input` APIs for disposable demos unless the project already has the new Input System package configured.
- Prefer primitives, built-in materials, URP-safe simple shaders, and standard `MonoBehaviour`/`Editor` APIs.
- Keep generated scene setup compatible with Windows Standalone unless another installed build module is confirmed.

## Plan

Before file edits, show a short plan:

```markdown
## Unity Demo Plan

Core Question: [what this demo must answer]
Unity Context: [version/render pipeline/input system if known]
Target Path: `Assets/Prototypes/[slug]/` or `prototypes/[slug]/UnityDemo/`

Includes:
- [scene/script/control/state]

Skips:
- [production system, asset polish, networking, save data]

Validation:
- [Unity CLI / Play Mode / manual steps]
```

Ask for confirmation only when the target path, Unity project location, or scope is genuinely ambiguous. Otherwise proceed.

## Placement

If the current repo is a Unity project, write all demo files under:

```text
Assets/Prototypes/[slug]/
```

Use this structure as needed:

```text
Assets/Prototypes/[slug]/
+-- Scripts/
+-- Editor/
+-- Scenes/
+-- Materials/
+-- Prefabs/
+-- README.md
```

If the repo is not a Unity project, write a portable demo package under:

```text
prototypes/[slug]/UnityDemo/
```

Do not modify `ProjectSettings/`, `Packages/manifest.json`, production scenes, production prefabs, production asmdefs, or production gameplay code unless the user explicitly asks.

## Implementation Rules

Every C# file starts with:

```csharp
// PROTOTYPE - NOT FOR PRODUCTION
// Question: [Core question being tested]
// Date: [YYYY-MM-DD]
```

Keep the demo self-contained:

- Use primitives, temporary materials, placeholder sprites, and serialized Inspector fields.
- Prefer a namespace like `Prototypes.[PascalSlug]`.
- Use clear controls and on-screen debug labels when useful.
- Prefer `SerializeField` for tuning values that the user should adjust in Inspector.
- Avoid dependencies on production gameplay code.
- If the project uses asmdefs, either stay in a folder covered by an existing permissive asmdef or create a local prototype asmdef only inside the prototype folder.
- If scene creation is needed, prefer an Editor builder script over hand-written `.unity` YAML.

Acceptable shortcuts:

- Hardcoded demo data
- Simplified collision shapes
- Placeholder art/audio/VFX
- Minimal error handling
- Copying small helper logic inside the demo instead of importing production code

## Unity Builder Pattern

For scene demos, create an Editor script when practical:

- Put it in `Assets/Prototypes/[slug]/Editor/[PascalSlug]DemoBuilder.cs`.
- Add a menu item such as `Tools/Prototypes/[Name]/Build Demo Scene`.
- Create primitives, cameras, lights, materials, and script-bearing GameObjects through Unity APIs.
- Save the scene to `Assets/Prototypes/[slug]/Scenes/[Name]Demo.unity`.

If Unity CLI is available, run the builder in batch mode when feasible. If not, leave exact menu steps in `README.md`.

## Validation

Validate at the highest level available:

- Confirm files exist in the prototype folder.
- Confirm C# files contain the prototype header.
- If Unity is installed and the project can open, run a compile/build or batch-mode editor method.
- If Play Mode cannot be run from the terminal, provide manual Play Mode steps and mark Play Mode as not verified.
- Never claim the demo was playable unless it was actually opened or run.

Common Windows Unity executable locations to check:

```text
D:\Unity\Editor\*\Editor\Unity.exe
C:\Program Files\Unity\Hub\Editor\*\Editor\Unity.exe
C:\Program Files\Unity*\Editor\Unity.exe
```

Common batch command shape:

```powershell
& "...\Unity.exe" -batchmode -quit -projectPath "<repo>" -executeMethod Prototypes.[PascalSlug].[PascalSlug]DemoBuilder.Build
```

Use the exact method name created in the Editor script.

## Report

Write a concise `README.md` inside the demo folder. Include:

- Core question
- Files created
- How to open/run
- Controls
- What to observe
- Known shortcuts
- Validation performed
- Recommendation: `PROCEED`, `PIVOT`, or `KILL`

If this demo is part of the broader `/prototype` workflow, also update or create `prototypes/[slug]/REPORT.md`.

## Handoff

End with:

- Demo path
- How to run it in Unity
- What was verified
- What was not verified
- Suggested next step: `/quick-design`, `/design-system`, `/architecture-decision`, `/create-stories`, or stop

If proceeding to production, state that production implementation should be rewritten from design/architecture requirements, not promoted from prototype code.
