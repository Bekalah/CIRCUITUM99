# Cosmic Helix Renderer

Static, offline renderer for layered sacred geometry. Double-click `index.html` in any modern browser.

## Layers
1. **Vesica field** – intersecting circles as foundation.
2. **Tree-of-Life scaffold** – ten sephirot with twenty-two paths.
3. **Fibonacci curve** – calm log spiral polyline.
4. **Double-helix lattice** – two static strands with gentle rungs.

## Palette
Colors are loaded from `data/palette.json`. If the file is missing, the renderer falls back to a built-in ND-safe palette and notes this in the header.

Layer colors map as follows:
- `layers[0]` – Vesica field
- `layers[1]` – Tree paths
- `layers[2]` – Tree nodes
- `layers[3]` – Fibonacci curve
- `layers[4]` – Helix strand A
- `layers[5]` – Helix strand B

## ND-Safety
- No animation or motion.
- Soft contrast on dark background for low visual strain.
- Static `<canvas>` only; no external requests.

## Numerology
Geometry routines use constants `3, 7, 9, 11, 22, 33, 99, 144` to keep alignment with the wider cathedral canon.

## Use
No build step or server. Open `index.html` directly.
