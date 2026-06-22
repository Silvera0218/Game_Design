# Art Direction Reference

Read this when defining 美术审美, art style, visual identity, mood boards, asset specs, UI look, animation feel, VFX language, or when critiquing game visuals.

## Art Direction Frame

Anchor every visual choice in:

- Player fantasy
- Genre expectations and how to bend them
- Camera distance and gameplay readability
- Target platform and performance budget
- Team size, asset pipeline, and reuse needs
- Emotional tone and pacing

Avoid style labels alone. "Cozy low-poly" is not enough; define shape language, palette, material treatment, lighting, animation timing, UI density, and what should never appear.

## Style Guide Structure

Use this structure for an art guide:

- Style pillars: 3 short rules with examples and anti-examples
- Camera/readability: silhouette size, value contrast, enemy/friendly coding, UI safe areas
- Shape language: round/angular, chunky/slender, realistic/exaggerated, modular/organic
- Palette: dominant, support, accent, danger, reward, neutral, disabled
- Lighting: key mood, contrast range, time of day, fog/post-processing rules
- Materials: roughness, texture density, edge wear, outline, shader constraints
- Characters: proportions, face detail, costume rules, animation energy
- Environments: scale, landmarks, set dressing density, traversal clarity
- UI: typography, icon style, panel density, state colors, motion rules
- VFX: timing, color semantics, scale, screen shake, particles, hit confirmation
- Audio notes when visual feedback depends on sound
- Asset list and production acceptance criteria

## Readability First

Gameplay readability beats decoration:

- Use silhouette before color for important entities.
- Separate interactable, hazard, collectible, objective, and background values.
- Reserve high saturation and high contrast for decisions and feedback.
- Avoid visual noise around the player, reticle, health, timers, and enemy tells.
- Make animation anticipation and recovery readable at gameplay speed.
- Make UI scannable in peripheral vision when the game is real-time.

Check grayscale value, colorblind ambiguity, small-screen scale, motion blur, and compression artifacts for target platforms.

## Originality And References

Use references to identify visual properties, not to clone a brand. When a user names an existing game or studio style, translate it into neutral traits:

- Camera and composition
- Proportion and silhouette
- Palette and contrast
- Material finish
- Line/detail density
- Animation timing
- UI hierarchy
- Emotional tone

Then combine those traits with the user's game fantasy, platform, and production constraints to produce an original direction.

## Asset Specification

For production-ready asset requests, specify:

- Asset name and purpose
- Size, units, pivot/origin, collision expectations
- Texture resolution, channels, compression, import settings
- Animation states, frame counts, loops, events, root motion rules
- LODs, batching, atlas, material variants, shader requirements
- Naming conventions and folder destination
- Done criteria in engine, not just in the art tool

## Unity Art Pipeline Notes

- Match the render pipeline already in the project: Built-in, URP, or HDRP.
- Keep placeholder and final assets clearly separated.
- Prefer material variants and shared atlases over one-off materials.
- For sprites, define pixels-per-unit, pivot, slicing, packing, compression, and filter mode.
- For 3D, define unit scale, forward/up axes, collider strategy, lightmap/static flags, and LOD policy.
- For UI, verify canvas scaling, safe areas, dynamic text length, localization, and controller focus states.

## Critique Rubric

When critiquing visuals, assess:

- Does the first read show the objective, threat, player, and affordances?
- Do style choices reinforce the player fantasy?
- Are color/value/shape semantics consistent?
- Is the detail density appropriate for the camera?
- Does animation timing communicate state changes?
- Can the team produce enough content in this style?
- Are performance and memory risks visible early?
