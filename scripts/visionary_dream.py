"""Visionary Dream Generator
Creates a museum-quality piece of visionary art using Python and Pillow.
Color palette inspired by Alex Grey.
Resolution: 1920x1080.
Outputs Visionary_Dream.png.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

# Prepare canvas and output path
WIDTH, HEIGHT = 1920, 1080
OUTPUT = Path(__file__).resolve().parent.parent / "Visionary_Dream.png"

# Alex Grey-inspired palette
PALETTE = [
    (30, 30, 60),    # deep indigo
    (60, 90, 150),   # electric blue
    (120, 180, 200), # aquamarine
    (200, 100, 150), # magenta glow
    (240, 240, 200), # ethereal gold
]


def main() -> None:
    """Generate visionary art and save as a PNG."""
    # Initialize canvas
    img = Image.new("RGB", (WIDTH, HEIGHT), PALETTE[0])
    draw = ImageDraw.Draw(img)
    center = (WIDTH // 2, HEIGHT // 2)
    max_radius = min(center)

    # Draw concentric ellipses for layered depth
    for i, color in enumerate(PALETTE[1:], start=1):
        radius = max_radius * i / len(PALETTE)
        bbox = [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ]
        draw.ellipse(bbox, outline=color, width=3)

    # Radiating symmetry lines
    num_lines = 90
    for i in range(num_lines):
        angle = 2 * math.pi * i / num_lines
        x = center[0] + max_radius * math.cos(angle)
        y = center[1] + max_radius * math.sin(angle)
        color = PALETTE[i % len(PALETTE)]
        draw.line([center, (x, y)], fill=color, width=2)

    # Star-like points for organic patterning
    for _ in range(2000):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        color = random.choice(PALETTE)
        draw.point((x, y), fill=color)

    # Save the final visionary piece
    img.save(OUTPUT)


if __name__ == "__main__":
    main()
