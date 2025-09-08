# Circuitum99 Integration Tasks

Summary of current state and next steps for linking repos, games, and world-building tools.

## Working
- **Cosmic Helix Renderer** (`index.html`, `js/helix-renderer.mjs`)
  - Replaced the broken helix script with a modern offline canvas.
  - Renders Vesica, Tree, Fibonacci, and a static double helix using a palette from `data/` with graceful fallback.
- **LuxCrux V Engine** (`games/luxcrux_v/engine.py`)
  - CLI adventure runner with hooks for dynamic art and music.
- **Registry scaffolding** (`registry/`)
  - Initial indexes for characters, systems, and narrative nodes.

## Current Repo Links
- `Circuitum99` (soul) hosts the codex and world lore.
- `Cosmogenesis Learning Engine` (mind) is referenced by game hooks for generative media.
- `Stone Cathedral` (body) contains spatial/asset work (external repo referenced in docs).
- Game modules live under `games/` and reference the mind layer via hooks.

## Expansion for Multiple Games & Complex Environments
- Define a common **API contract** for `trigger_art` / `trigger_music` so any game can request media from the mind layer.
- Extend the **registry** to index game modules, scenes, and assets for cross-game reuse.
- Provide **world node metadata** (e.g., location, theme, palette) so the renderer can visualize any node.
- Offer a **JSON schema** for games to register themselves and their hooks.

## Outstanding Work
- Implement the `trigger_art` and `trigger_music` hooks to call the Cosmogenesis Learning Engine or another ND-safe renderer.
- Replace `games/visionary_dream.py` Pillow script with a pure-canvas or NumPy alternative.
- Populate `registry/` with full lists of systems, characters, and node connections.
- Add more game modules and ensure they read from shared registry data.
- Document how to contribute new layers, palettes, and numerology constants.
- Build a toggle system so art, learning, and music modes can switch styles.
- Create identity anchor art for Rebecca Respawn and other avatars before layering fusion effects.
- Produce book-ready art variants: illuminated manuscript plates, engraved diagrams, visionary scenes, and cinematic frames.

