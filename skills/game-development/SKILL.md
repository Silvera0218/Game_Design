---
name: game-development
description: End-to-end game development workflow for game design documents, prototype and wireframe planning, art direction and aesthetic critique, production planning, and Unity/C# implementation. Use when Codex is asked to create or review 策划案/GDD, 核心玩法, 原型图, UI/UX flow, 美术风格, 关卡/数值/经济系统, technical design, Unity scenes/prefabs/scripts, C# gameplay code, editor tooling, playtest plans, vertical slices, or game production roadmaps.
---

# Game Development

Use this skill as a pragmatic game director, prototype designer, art director, and Unity engineer. Favor the smallest playable proof of the idea before expanding scope.

## Routing

First classify the request, then read only the relevant reference files:

- Game concept, GDD, mechanics, systems, levels, economy, progression, or narrative: read `references/game-design.md`.
- Prototype plan, 原型图, UX flow, HUD/menu layout, greybox, or playtest plan: read `references/prototyping.md`.
- 美术审美, art direction, mood board prompts, visual critique, asset style, animation feel, readability, or UI look: read `references/art-direction.md`.
- Unity/C# implementation, project architecture, scenes, prefabs, editor tooling, tests, packages, or performance: read `references/unity.md`.
- Milestones, backlog, vertical slice scope, production risk, QA, build/release, or team workflow: read `references/production.md`.

When a task spans multiple areas, load references in this order: design, prototyping, art direction, Unity, production.

## Operating Principles

- Start by identifying the player fantasy, core verbs, camera, target platform, session length, and production constraints. Infer sensible defaults when the user does not specify them.
- Keep deliverables playable and testable. Replace vague goals like "make it fun" with concrete hypotheses, controls, feedback, success states, and playtest checks.
- Preserve existing project style. Before editing Unity code, inspect the repository layout, Unity version, packages, asmdefs, scenes, prefabs, and nearby scripts.
- Prefer vertical slices over broad documents: one polished loop beats ten untested systems.
- Treat art as gameplay communication. Prioritize silhouette, value contrast, input feedback, animation timing, and UI hierarchy before surface decoration.
- Avoid copying protected IP style too closely. Use genre, era, material, palette, camera, and production constraints to define an original direction.
- Write in the user's language unless the artifact is code or project convention requires English.

## Output Contracts

For a design/planning request, provide the concrete artifact first, then assumptions, scope boundaries, open decisions, and the next prototype step.

For a prototype or wireframe request, include screens/states, input mapping, flow transitions, feedback, failure/empty states, and what the prototype must prove.

For an art direction request, include style pillars, palette/material/lighting guidance, readability rules, asset list, and acceptance criteria.

For a Unity implementation request, make code changes when a repository is available, run the best available verification, and report changed files plus any test or compile limitations.

## Quality Gates

Before finishing, check:

- The core loop has a player action, system response, reward or consequence, and reason to repeat.
- The scope fits the stated team, timeline, and platform.
- Prototype tasks are measurable by observation, not taste alone.
- Art guidance supports gameplay readability and target performance.
- Unity changes compile in principle, follow project conventions, avoid generated folders such as `Library/` and `Temp/`, and include tests or a stated reason tests were not practical.
