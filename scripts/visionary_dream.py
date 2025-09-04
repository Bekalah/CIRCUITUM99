import numpy as np
from PIL import Image, ImageDraw
import math
import random

# Canvas dimensions for high-resolution visionary art
WIDTH, HEIGHT = 1920, 1080

# Color palette inspired by Alex Grey's surreal vision
PALETTE = [
    (30, 30, 60),    # deep indigo
    (60, 90, 150),   # electric blue
    (120, 180, 200), # aquamarine
    (200, 100, 150), # magenta glow
    (240, 240, 200)  # ethereal gold
]

# Initialize blank canvas
img = Image.new("RGB", (WIDTH, HEIGHT))
pixels = img.load()

# Generate layered sine-wave patterns for fractal flow
for y in range(HEIGHT):
    for x in range(WIDTH // 2):
        r = 0
        for i in range(3):
            angle = random.random() * 2 * math.pi
            freq = 0.002 + i * 0.001
            r += math.sin(freq * (math.cos(angle) * x + math.sin(angle) * y))
        index = int(abs(r) * len(PALETTE)) % len(PALETTE)
        color = PALETTE[index]
        pixels[x, y] = color
        pixels[WIDTH - 1 - x, y] = color  # mirror for symmetry

# Overlay concentric visionary glyphs
draw = ImageDraw.Draw(img)
center = (WIDTH // 2, HEIGHT // 2)
for radius in range(50, min(WIDTH, HEIGHT) // 2, 80):
    color = PALETTE[(radius // 80) % len(PALETTE)]
    bbox = [
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    ]
    draw.ellipse(bbox, outline=color)

# Save the final visionary piece
img.save("Visionary_Dream.png")
