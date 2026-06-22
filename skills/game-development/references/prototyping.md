# Prototyping Reference

Read this when making 原型图, UX flows, HUD/menu layouts, greyboxes, playable prototypes, control feel tests, or playtest plans.

## Prototype Goal

Start with the question the prototype must answer:

- Can the core verb feel good?
- Can players understand the objective without explanation?
- Is the camera readable?
- Does the loop create a repeatable decision?
- Is the UI state legible under pressure?
- Can the system be built within the target constraints?

Do not prototype every feature. Build the cheapest artifact that tests the riskiest assumption.

## Prototype Types

- Paper sketch: fastest for screen flow, economy, cards, puzzles, dialogue branches
- Clickthrough: useful for menus, onboarding, inventory, shop, settings, results
- Greybox: useful for level scale, camera, collision, navigation, encounter pacing
- Playable mechanic: useful for movement, combat, physics, timing, feel
- Vertical slice: one polished loop with representative art, audio, UI, and production path

Choose the prototype type based on the risk, not on how impressive the output looks.

## Wireframe Contents

For each screen or state, specify:

- Purpose and player decision
- Layout zones and priority order
- Persistent HUD elements
- Contextual controls
- State changes and transitions
- Empty, disabled, loading, success, failure, and pause states
- Controller/keyboard/touch mapping
- Accessibility needs such as text size, contrast, remapping, colorblind support

Use ASCII, Mermaid, simple tables, or generated image/UI mockups depending on the user's request and available tooling. For implementation-ready UI, include component names and data dependencies.

## Game Feel Prototype

For action prototypes, expose tunables:

- Movement speed, acceleration, deceleration, gravity, jump buffer, coyote time
- Attack startup, active frames, recovery, hit stop, knockback
- Aim assist, lock-on rules, camera damping, field of view
- Invulnerability frames, cooldowns, stamina costs
- VFX/audio feedback timing

Add debug display for key state when practical: grounded, velocity, current action, combo step, damage events, AI state, objective progress.

## Greybox Rules

- Use primitive shapes, clear scale markers, and strong contrast.
- Lock camera and movement metrics before decorating.
- Mark critical paths, optional paths, hazards, pickups, and spawn points.
- Use temporary labels only for development. Do not rely on labels to make the design understandable.
- Capture top-down and player-view diagrams when explaining spatial flow.

## Playtest Plan

Write playtest plans as observation tools:

- Hypothesis
- Target tester profile
- Setup and build version
- Tasks to complete
- Metrics to capture
- Observations to record
- Post-test questions
- Pass/fail or iterate criteria

Prefer behavioral questions: "Where did the player hesitate?" beats "Was it fun?"

## Prototype Acceptance Checklist

Before calling a prototype done, confirm:

- It answers one or two explicit questions
- It has a start, objective, feedback, failure/retry, and end condition
- It can be tested by someone other than the creator
- It records or exposes enough state to diagnose problems
- It has a clear next decision: continue, revise, cut, or expand
