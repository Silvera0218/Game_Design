# Game Design Reference

Read this when creating or reviewing a game concept, 策划案/GDD, core loop, mechanics, economy, progression, level design, enemies, abilities, onboarding, or narrative structure.

## Fast GDD Shape

Use the smallest document that answers the production question. For early ideas, write a one-page pitch. For build-ready work, expand only the sections that unblock prototyping.

One-page pitch:

- Title or working title
- Genre, camera, platform, target player, session length
- Player fantasy in one sentence
- Design pillars, usually 3
- Core verbs and primary input
- Core loop and meta loop
- Hook or differentiator
- Prototype scope and success criteria
- Main risks and cuttable features

Build-ready GDD sections:

- Overview: fantasy, audience, platform, controls, camera, content rating assumptions
- Pillars: non-negotiable experience goals with examples and anti-examples
- Core loop: moment-to-moment loop, session loop, long-term loop
- Mechanics: rules, inputs, feedback, failure states, edge cases
- Content: levels, enemies, items, skills, quests, encounters, UI screens
- Progression: unlocks, economy, difficulty curve, pacing targets
- Systems: data model, tuning variables, balancing tables, telemetry needs
- UX: HUD, menus, onboarding, accessibility, localization assumptions
- Production: vertical slice scope, dependencies, risks, acceptance criteria

## Mechanics Method

Design mechanics as a chain:

`player verb -> target/object -> rule -> feedback -> cost/risk -> reward -> mastery path -> variation`

For every mechanic, specify:

- What the player does
- What the game reads as input
- What state changes
- What feedback confirms the result
- What can go wrong
- What makes mastery visible
- How the mechanic combines with at least one other system

Avoid mechanics that only exist in text. If it cannot be shown through input, response, and feedback, it is probably lore, economy, or UI, not a gameplay mechanic.

## Core Loop

Separate three loops:

- Moment loop: seconds, such as aim, dodge, hit, collect
- Session loop: minutes, such as enter room, solve combat, choose reward, upgrade
- Meta loop: hours, such as unlock character, build deck, improve town, climb rank

For each loop, state the trigger, player decision, reward, reset condition, and what changes on repeat.

## Economy And Progression

For currencies, resources, XP, stamina, loot, crafting, cards, or upgrades, define:

- Sources and sinks
- Spend timing and pressure
- Soft caps, hard caps, and overflow behavior
- Expected earning curve by session
- Expected cost curve by upgrade tier
- Failure/recovery behavior
- Anti-hoarding and anti-grind safeguards

Use tables when values matter. Keep first-pass numbers simple and expose tuning variables for Unity prototypes.

## Level And Encounter Design

Every level or encounter should have:

- Intent: what the player learns, proves, or feels
- Constraint: space, timer, resources, enemy mix, visibility, or rules
- Pacing: introduction, variation, escalation, release
- Readability: landmarks, silhouettes, color/value grouping, path clarity
- Failure: how the player understands why they failed
- Reuse: which assets or mechanics can be recombined later

Onboarding should teach by safe interaction before punishment. Introduce one new idea at a time, then combine it with a previous idea.

## Review Rubric

When reviewing a design, look for:

- A clear player fantasy and target audience
- Verbs that are strong enough to prototype
- Loops with repeat motivation
- Interesting decisions rather than automatic optimal choices
- Scope that fits team/time/tools
- Concrete failure states and feedback
- Tuning variables that can be tested
- Content plans that reuse systems instead of multiplying one-off work

Ask at most three clarifying questions only when an answer changes the artifact materially.
