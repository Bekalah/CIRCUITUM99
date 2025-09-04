# Visionary art generator using Pillow
# Color palette inspired by Hilma af Klint and surrealism

from PIL import Image, ImageDraw
import math
import random

# Canvas resolution
WIDTH, HEIGHT = 1920, 1080

# Define mystical color palette
PALETTE = [
    (11, 30, 61),   # deep lapis blue
    (241, 196, 15), # alchemical gold
    (46, 204, 113), # peacock green
    (10, 10, 10),   # obsidian black
    (138, 43, 226), # octarine shimmer
]

# Create base image and drawing context
img = Image.new("RGB", (WIDTH, HEIGHT), PALETTE[0])
draw = ImageDraw.Draw(img)

# Radiant concentric gradient
center = (WIDTH // 2, HEIGHT // 2)
max_radius = int(math.hypot(WIDTH, HEIGHT) / 2)
for r in range(max_radius, 0, -10):
    color = PALETTE[r % len(PALETTE)]
    bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
    draw.ellipse(bbox, fill=color)

# Symmetrical light rays
for i in range(360):
    angle = math.radians(i)
    radius = random.randint(200, max_radius)
    x = center[0] + int(math.cos(angle) * radius)
    y = center[1] + int(math.sin(angle) * radius)
    color = PALETTE[i % len(PALETTE)]
    draw.line([center, (x, y)], fill=color, width=2)

# Mandala circles
for i in range(0, 360, 15):
    angle = math.radians(i)
    r = 100 + 50 * math.sin(math.radians(i * 4))
    x = center[0] + int(math.cos(angle) * r * 4)
    y = center[1] + int(math.sin(angle) * r * 4)
    bbox = [x - r, y - r, x + r, y + r]
    color = PALETTE[(i // 15) % len(PALETTE)]
    draw.ellipse(bbox, outline=color, width=3)

# Save masterpiece
img.save("Visionary_Dream.png")
