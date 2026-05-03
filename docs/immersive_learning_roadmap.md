# Immersive Upgrade Roadmap

## 1. Night mode
- Add a dedicated `Midnight` theme and a `Night mode` toggle.
- Persist the choice in browser storage so returning students stay in their preferred mode.

## 2. Realistic AI characters
- Keep the current in-browser avatar stage for low-cost prototyping.
- Upgrade path:
  - Use `Ready Player Me` or another avatar SDK for realistic web-ready characters.
  - Render the character with `three.js` or `Babylon.js`.
  - Use your existing tutor voice layer to drive lip-sync and speaking states.
- Safe rollout:
  - Phase 1: realistic static avatar
  - Phase 2: blink, head movement, mouth movement
  - Phase 3: full talking avatar with streamed audio and captions

## 3. Source links
- Keep `Live Sources` for current-affairs grounding.
- Add source chips under each reply where grounding exists.
- Build a `resource library` table for exam-specific strategy links, official sites, and curated prep references.

## 4. 3D concept visualization
- Start with canvas-based motion boards for concepts like projectile motion, percentages, probability, and electric fields.
- Move to full 3D using `three.js` only for concepts where spatial intuition matters.
- Suggested first 3D topics:
  - projectile motion
  - vectors
  - electric fields
  - 3D geometry
  - probability simulations

## 5. Video explanation system
- Current state: storyboard-style subtitles and reasoning panels
- Next state:
  - scene cards become a timed lesson player
  - captions switch language
  - per-scene calculations stay beside the player
- Later:
  - render short animated explainer videos from scene JSON
  - connect those scenes to a talking avatar host

## 6. Startup-ready architecture
- Move from file-backed learning state to PostgreSQL.
- Keep object storage for uploaded doubt images and future media outputs.
- Add queue-based media rendering later for heavy video/avatar generation.
