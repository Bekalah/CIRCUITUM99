"""
✦ Codex 144:99 - preserve original intention
Visionary palette generator.
"""

# ✦ Codex 144:99 - preserve original intention

import argparse
import json
import math
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw

# Load palette JSON
DEFAULT_PALETTE = {
    "visionary": {
        "core": {
            "indigo": "#280050",
            "violet": "#460082",
            "blue": "#0080FF",
            "green": "#00FF80",
            "amber": "#FFC800",
            "light": "#FFFFFF",
        },
        "secondary": {
            "crimson": "#B7410E",
            "gold": "#FFD700",
            "slate": "#2E2E2E",
            "silver": "#C0C0C0",
            "sky": "#87CEFA",
            "shadow": "#4B0082",
        },
    }
}

def load_palette(path: Path) -> dict:
    """Load palette JSON or return default."""
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_PALETTE

def kaleido(draw: ImageDraw.ImageDraw, w: int, h: int, colors: list):
    """Draw kaleidoscopic radial pattern."""
    cx, cy = w / 2, h / 2
    max_radius = math.hypot(cx, cy)
    for r in range(int(max_radius)):
        color = colors[r % len(colors)]
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color)

def spiral(draw: ImageDraw.ImageDraw, w: int, h: int, colors: list):
    """Draw spiral arcs."""
    cx, cy = w / 2, h / 2
    steps = 200
    for i in range(steps):
        angle = i * math.pi / 10
        radius = i * (w / (2 * steps))
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        color = colors[i % len(colors)]
        draw.line((cx, cy, x, y), fill=color)

def flame_like(draw: ImageDraw.ImageDraw, w: int, h: int, colors: list, seed: int):
    """Draw pseudo flame-like noise pattern."""
    random.seed(seed)
    for y in range(h):
        for x in range(w):
            idx = (int((math.sin(x / 20) + math.cos(y / 20)) * 3 + random.random() * 3)) % len(colors)
            draw.point((x, y), fill=colors[idx])

def main():
    parser = argparse.ArgumentParser(description="Generate visionary art using shared palette")
    parser.add_argument("--mode", choices=["kaleido", "spiral", "flame_like"], default="kaleido")
    parser.add_argument("--width", type=int, default=1400)
    parser.add_argument("--height", type=int, default=1400)
    parser.add_argument("--symmetry", type=int, default=6)
    parser.add_argument("--seed", type=int, default=33)
    parser.add_argument("--out", default="assets/cymatics")
    args = parser.parse_args()

    random.seed(args.seed)

    palette = load_palette(Path("data/palettes/visionary.json"))
    colors = list(palette["visionary"]["core"].values())

    os.makedirs(args.out, exist_ok=True)
    img = Image.new("RGB", (args.width, args.height), palette["visionary"]["secondary"]["slate"])
    draw = ImageDraw.Draw(img)

    if args.mode == "kaleido":
        kaleido(draw, args.width, args.height, colors)
    elif args.mode == "spiral":
        spiral(draw, args.width, args.height, colors)
    else:
        flame_like(draw, args.width, args.height, colors, args.seed)

    out_path = Path(args.out) / "Visionary_Dream.png"
    img.save(out_path)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
