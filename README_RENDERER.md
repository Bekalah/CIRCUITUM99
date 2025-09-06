# Cosmic Helix Renderer

Static HTML+Canvas renderer for layered sacred geometry.  Designed for offline use and neurodivergent safety.

## Layers
1. **Vesica field** – intersecting circles in a calm grid.
2. **Tree-of-Life scaffold** – ten nodes with twenty-two connecting paths.
3. **Fibonacci curve** – golden ratio spiral drawn once.
4. **Double-helix lattice** – two sine waves with gentle cross-links.

## Use
Open `index.html` in any modern browser.  No build step, server, or external network is required.

If `data/palette.json` is missing, the renderer falls back to a safe default palette and shows a short notice at the top of the page.

## Notes
- All geometry constants are exposed in the `NUM` object: 3, 7, 9, 11, 22, 33, 99, 144.
- Color and layer order favor high readability, soft contrast, and no motion.
- Files use UTF-8, LF newlines, ASCII quotes, and contain no dependencies or animation libraries.
