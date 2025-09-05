"""Versatile Visionary Dream art generator.

This demo expands on earlier prototypes by offering multiple palettes and
pattern modes for rendering a museum-quality piece of visionary art.  The
output is always saved as ``Visionary_Dream.png`` unless a different path is
specified via the ``--out`` argument.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

# ---------------------------------------------------------------
# Palette definitions inspired by visionary artists and movements
# ---------------------------------------------------------------
PALETTES = {
    "alex_grey": [
        "#280050",  # deep indigo
        "#460082",  # ultraviolet violet
        "#0080FF",  # electric blue
        "#00FF80",  # neon green
        "#FFC800",  # solar amber
        "#FFFFFF",  # pure light
    ],
    "hilma_af_klint": [
        "#0b1e3d",  # lapis background
        "#f1c40f",  # alchemical gold
        "#2ecc71",  # peacock green
        "#0a0a0a",  # obsidian shadow
        "#8a2be2",  # octarine shimmer
    ],
    "surrealism": [
        "#6A0DAD",  # royal purple
        "#FF6F61",  # dream coral
        "#00FFFF",  # cyan aura
        "#FFD700",  # golden vision
        "#1E90FF",  # azure spark
    ],
}


# ---------------------------------------------------------------
# Pattern drawing helpers
# ---------------------------------------------------------------
def radial(draw: ImageDraw.ImageDraw, width: int, height: int, colors: list[str]) -> None:
    """Radiating lines from the center."""
    center = (width // 2, height // 2)
    radius = min(width, height) // 2
    for i in range(360):
        angle = math.radians(i)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        draw.line([center, (x, y)], fill=colors[i % len(colors)], width=1)


def mandala(draw: ImageDraw.ImageDraw, width: int, height: int, colors: list[str]) -> None:
    """Concentric circles forming a mandala."""
    center = (width // 2, height // 2)
    max_radius = min(width, height) // 2
    for r in range(50, max_radius, 50):
        color = colors[(r // 50) % len(colors)]
        bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
        draw.ellipse(bbox, outline=color, width=3)


def spiral(draw: ImageDraw.ImageDraw, width: int, height: int, colors: list[str]) -> None:
    """Outward spiral made of flowing arcs."""
    center = (width // 2, height // 2)
    steps = 360
    for i in range(steps):
        angle = math.radians(i * 5)
        radius = i * min(width, height) / (2 * steps)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        draw.line([center, (x, y)], fill=colors[i % len(colors)], width=2)


PATTERNS = {
    "radial": radial,
    "mandala": mandala,
    "spiral": spiral,
}
#!/usr/bin/env python3
"""
Visionary Dream Generator
Creates a museum-quality piece of visionary art with a palette inspired by Alex Grey.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random
import math

# Canvas dimensions (HD resolution)
WIDTH, HEIGHT = 1920, 1080

# Output path
OUTPUT = Path(__file__).resolve().parents[1] / "img" / "Visionary_Dream.png"

def main() -> None:
    """Command-line interface for the Visionary Dream generator."""

    # ------------------------
    # Argument parsing & setup
    # ------------------------
    parser = argparse.ArgumentParser(description="Generate visionary art")
    parser.add_argument("--width", type=int, default=1024, help="canvas width")
    parser.add_argument("--height", type=int, default=1024, help="canvas height")
    parser.add_argument(
        "--palette",
        choices=sorted(PALETTES.keys()),
        default="alex_grey",
        help="color palette",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(PATTERNS.keys()),
        default="radial",
        help="pattern to render",
    )
    parser.add_argument("--seed", type=int, default=0, help="random seed")
    parser.add_argument("--out", default="Visionary_Dream.png", help="output file")
    args = parser.parse_args()

    random.seed(args.seed)

    # ------------------------
    # Canvas and drawing setup
    # ------------------------
    image = Image.new("RGB", (args.width, args.height), "black")
    draw = ImageDraw.Draw(image)
    colors = PALETTES[args.palette]

    # ------------------------
    # Render selected pattern
    # ------------------------
    PATTERNS[args.mode](draw, args.width, args.height, colors)

    # ------------------------
    # Save final piece
    # ------------------------
    out_path = Path(args.out)
    image.save(out_path)


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()

    """Render the visionary scene and save it as an image."""
    # Step 1: Cosmic dusk gradient backdrop
    image = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = image.load()
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(30 + 100 * t)
        g = int(0 + 60 * t)
        b = int(60 + 180 * t)
        for x in range(WIDTH):
            pixels[x, y] = (r, g, b)

    # Step 2: Scatter starlight across the sky
    draw = ImageDraw.Draw(image)
    for _ in range(1500):
        x, y = random.randrange(WIDTH), random.randrange(HEIGHT)
        star = random.choice([(255, 255, 255), (255, 210, 180), (200, 220, 255)])
        draw.point((x, y), fill=star)

    # Step 3: Raise luminous columns of a dream temple
    center_x = WIDTH // 2
    for i in range(-3, 4):
        column_x = center_x + i * 140
        draw.rectangle([column_x - 20, 400, column_x + 20, HEIGHT - 120], fill=(80, 20, 120))
        draw.ellipse([column_x - 60, 300, column_x + 60, 420], outline=(255, 215, 0), width=3)

    # Step 4: Spiral energy halo around the sanctuary
    for angle in range(0, 360, 4):
        radius = 0
        for step in range(180):
            radius += 2
            x = center_x + radius * math.cos(math.radians(angle + step))
            y = HEIGHT // 2 + radius * math.sin(math.radians(angle + step))
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                color = random.choice([(255, 0, 128), (0, 255, 255), (255, 255, 0)])
                image.putpixel((int(x), int(y)), color)

    # Step 5: Gentle blur for ethereal glow
    image = image.filter(ImageFilter.GaussianBlur(0.8))

    # Step 6: Save final piece
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT)

if __name__ == "__main__":
    main()
