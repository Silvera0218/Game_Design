# Production Reference

Read this for milestone planning, backlog shaping, vertical slice scope, risk management, QA, build/release planning, or team workflow.

## Milestone Ladder

Use milestone names as decision gates:

- Concept: prove the fantasy, audience, pillars, and scope.
- Playable prototype: prove the riskiest mechanic or loop with placeholder content.
- Vertical slice: one representative, shippable-quality loop that proves pipeline and quality bar.
- Alpha: all major systems present, content incomplete, tuning rough.
- Content complete: required content in, quality uneven but complete.
- Beta: feature/content locked, bug fixing, tuning, optimization.
- Release candidate: only critical fixes, final QA, store/platform checks.
- Live operations: telemetry, balance patches, events, content updates.

Do not let a milestone pass without acceptance criteria.

## Backlog Shape

Write backlog items with:

- Player-facing outcome
- Owner/discipline
- Dependencies
- Acceptance criteria
- Estimate range or confidence
- Risk level
- Validation method

Group backlog by player loop, not only by discipline. A slice should include design, code, art, audio, UI, QA, and build work needed to prove that loop.

## Vertical Slice Planning

A good vertical slice includes:

- One complete core loop
- Final-ish input, camera, feedback, HUD, and fail/retry
- Representative art and audio quality for a small area
- One example of each hard pipeline: character, environment, UI, VFX, save/build if relevant
- Instrumentation or playtest method
- Clear cut line for anything outside the slice

Avoid making the vertical slice a content sampler. It should prove production method and player experience.

## Risk Register

Track risks as:

- Risk
- Probability
- Impact
- Early signal
- Mitigation
- Owner
- Decision date

Common game risks:

- Core mechanic does not feel good
- Scope too large for content production
- Art style too expensive
- Camera unreadable
- Network/physics/save system complexity underestimated
- Platform performance fails late
- UI unusable on controller/touch
- Progression economy becomes grindy or trivial

## QA And Release

Plan QA around:

- Core loop smoke test
- Input devices and remapping
- Save/load and upgrade paths
- Resolution/aspect ratios and safe areas
- Localization expansion
- Performance scenes
- Accessibility settings
- Store/platform compliance
- Crash and log capture

For builds, record Unity version, target platform, scripting backend, render pipeline, quality settings, build symbols, and known issues.

## Scope Control

Use explicit cutlines:

- Must ship for the promise
- Should ship if the slice works
- Could ship after the core is stable
- Cut unless a test proves it is essential

When scope grows, trade content count, visual fidelity, systemic depth, or platform count deliberately. Do not silently add all four.
