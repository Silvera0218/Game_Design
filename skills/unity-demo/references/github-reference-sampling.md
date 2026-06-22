# GitHub Reference Sampling

Use this reference only when the user asks to use GitHub examples or when a Unity mechanic is complex enough to benefit from external comparison.

## Sampling Rules

- Prefer official Unity repositories, high-star sample projects, and actively maintained templates.
- Use GitHub references for patterns, folder conventions, validation ideas, and tradeoff awareness.
- Do not copy external code into the demo unless the user explicitly asks and the license permits it.
- If a reference influences the demo, cite the repository URL in the demo README or report.
- If search results are stale or unavailable, continue from local Unity context and say that external reference sampling was skipped.

## Useful Reference Types

- Official Unity samples: validate package usage, scene setup patterns, and rendering/input expectations.
- Unity project templates: borrow isolation, folder naming, asmdef, and README conventions.
- AI/Unity tooling repositories: borrow validation and rollback principles, not their implementation.
- Mechanic-specific projects: compare controls, state machines, camera behavior, or physics parameters.

## Reference Notes From Prior Search

- `Unity-Technologies/FPSSample` is a full Unity FPS sample with source/assets and documentation; use it as inspiration for scene-scale demos and clear getting-started docs.
- `SamuelAsherRivello/unity-project-template` emphasizes project structure, coding standards, assembly definitions, URP, physics, ProBuilder, post-processing, TextMesh Pro, and unit testing; use it for demo organization cues.
- `nuskey8/UnityAgentClient` highlights AI workflow issues around Unity domain reload and editor context; use it as a reminder to keep CLI/editor validation explicit.
- `Jason-hub-star/unityctl` frames useful automation goals for agents: create scenes, validate builds, and support rollback; use these as workflow ideals if matching tools exist locally.
- `openai/skills` and `ComposioHQ/awesome-codex-skills` document the broader skill pattern: concise `SKILL.md`, clear triggering metadata, and task-specific workflow guidance.
