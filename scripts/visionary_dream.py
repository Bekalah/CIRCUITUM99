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
