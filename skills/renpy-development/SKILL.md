---
name: renpy-development
description: Build, modify, debug, review, test, localize, and package Ren'Py visual novel projects. Use when Codex works with Ren'Py, `.rpy` files, dialogue and branching, labels/call/jump, Characters, images and layered images, ATL/transforms/transitions, audio/video/voice, screens/GUI/styles/actions, save/load/rollback/persistent data, Python integration, galleries/achievements, translations, accessibility, lint/testing, Android/iOS/Web/desktop builds, or Ren'Py errors and project architecture.
---

# Ren'Py Development

Treat a Ren'Py project as an interactive narrative program, not a pile of dialogue files. Preserve rollback correctness, save compatibility, UI behavior, localization, and build targets while making the smallest coherent change.

## Phase 1: Inspect and Scope

1. Determine whether the request is explanation, review, diagnosis, implementation, migration, or release work.
2. Locate the project and inspect:
   - Ren'Py/SDK version, when discoverable.
   - `game/options.rpy`, `game/gui.rpy`, `game/screens.rpy`, story `.rpy` files, and `game/tl/`.
   - Assets under `game/images/`, `game/audio/`, `game/gui/`, fonts, videos, and voice directories.
   - Existing naming, label, screen, style, state, save, localization, and build conventions.
3. Run `scripts/audit_renpy_project.py <project-or-game-dir>` for a structural snapshot when a project is available.
4. Do not edit `.rpyc`, `cache/`, generated distributions, or SDK internals unless the user explicitly requests engine-level work.
5. If the user asked only for advice, review, or diagnosis, remain read-only. If file-write authorization is ambiguous, ask “May I write these Ren'Py changes?” before writing. An explicit request to create, change, fix, or implement is already approval.

## Phase 2: Resolve Version and Load References

Use the project’s target Ren'Py version as the authority.

- The bundled Chinese knowledge map is based on the complete 103-page Traditional Chinese documentation index at `https://doc.renpy.cn/zh-TW/`, identified as Ren'Py 8.4.2 when this skill was authored.
- The locally verified SDK was Ren'Py 8.5.3. Its documentation adds `testcases` and `display_problems`, while the 8.4.2 Chinese index contains `modes` and `distributor`.
- For exact signatures, platform requirements, deprecations, security guidance, or version-sensitive behavior, verify against the matching SDK documentation or current official `renpy.org` documentation. State any version mismatch.

Load only the references relevant to the task:

- Story syntax, characters, labels, branching, audio, video, and voice: `references/core-language.md`
- Images, text, transforms, ATL, transitions, layered images, 3D stage, and Live2D: `references/presentation.md`
- GUI, screens, styles, actions, special screens, and optimization: `references/ui-screens.md`
- Python, namespaces, lifecycle, save/load/rollback, persistent data, and file access: `references/state-python.md`
- NVL, bubbles, galleries, replay, drag/drop, achievements, history, and related features: `references/game-features.md`
- Translation, fonts, self-voicing, input, and accessible interaction: `references/localization-accessibility.md`
- Launcher, lint, automated tests, builds, platforms, updates, security, and troubleshooting: `references/build-tools-platforms.md`
- Creator-defined extensions, callbacks, rendering, matrices, shaders, networking, and `_ren.py`: `references/advanced-extension.md`
- Every official document page and its routing category: `references/docs-map.md`
- Project organization and acceptance checks: `references/project-quality.md`

## Phase 3: Design the Change

Apply these Ren'Py-specific rules:

1. Use `define` for constants and configuration-like objects that must not change after initialization.
2. Use `default` for mutable game state that participates in new games, saves, loads, and rollback.
3. Use `persistent` only for data that intentionally survives across playthroughs; include migration-safe defaults.
4. Prefer `call` plus `return` for reusable narrative scenes and `jump` for one-way flow.
5. Keep story labels, presentation, UI, and reusable Python logic separated when project size justifies it.
6. Keep screen evaluation side-effect free. Prefer Ren'Py screen actions and functions over mutating state during display.
7. Preserve rollback semantics. Avoid irreversible external side effects in rollback-capable narrative execution.
8. Use Ren'Py asset loading and build classification instead of OS-specific absolute paths.
9. Design for localization expansion, variable interpolation, fonts, controller/keyboard focus, self-voicing, and target aspect ratios.
10. Avoid unnecessary custom Python or creator-defined components when standard Ren'Py statements, screens, actions, transforms, or displayables solve the problem.

For a new game, prove a vertical slice first:

- Main menu → start → dialogue → image/expression change → choice → state consequence → save/load → ending.
- Add one representative custom screen and one build target only after the core loop works.

## Phase 4: Implement

Follow existing project style and make changes in source-controlled `.rpy` and asset files.

- Keep top-level initialization declarations outside labels.
- Use four-space indentation consistently; never mix tabs and spaces.
- Use stable, descriptive names for labels, screens, transforms, styles, images, and variables.
- Split files by responsibility rather than arbitrary line count.
- Keep player-facing strings translatable and avoid assembling sentences from fragments.
- Keep save data simple and serializable. Do not store live file handles, sockets, iterators, displayables with unmanaged state, or platform objects in rollback state.
- When changing existing saved-state shape, add defensive defaults or migration logic.
- Preserve special screens and labels unless intentionally replacing their contract.
- Do not overwrite template GUI files wholesale for a small customization.

## Phase 5: Verify

Use the strongest available checks:

1. Run the bundled structural audit again and resolve blockers.
2. Run Ren'Py **Lint** from the launcher or command line.
3. If the target version supports automated tests and the project uses them, run the Ren'Py test cases.
4. Launch the project and exercise the changed path.
5. Check:
   - New game and return to main menu.
   - Branch conditions and label flow.
   - Save, load, quick save/load, and rollback.
   - Skip, auto-forward, history, and preferences where relevant.
   - Missing image/audio/font/video/voice resources.
   - Screen keyboard/controller focus and mobile interaction where relevant.
   - At least one non-default language when localization is in scope.
   - The requested desktop/mobile/web build.
6. Review `log.txt`, `traceback.txt`, lint output, and platform build logs after failure.

Classify the result:

- `PASS`: requested behavior works and relevant checks pass.
- `CONCERNS`: implementation is usable but a manual, platform, version, or compatibility check remains.
- `BLOCKED`: a required SDK, signing credential, platform toolchain, asset, or user decision is missing.
- `FAIL`: syntax, lint, runtime, save compatibility, or acceptance behavior is known to be broken.

## Phase 6: Report and Hand Off

Lead with the gameplay or authoring outcome, then report:

- Files changed.
- Narrative/UI/runtime behavior added or changed.
- Ren'Py version targeted.
- Lint, tests, launch, save/rollback, and build checks run.
- Any editor, launcher, asset, signing, or platform step still required.
- Known save compatibility or migration impact.
- Final verdict: `PASS`, `CONCERNS`, `BLOCKED`, or `FAIL`.

Recommend the smallest useful next step, such as a playtest pass, localization check, GUI polish, automated test, or distribution build.
