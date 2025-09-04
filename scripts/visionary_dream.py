import math
import random
from PIL import Image, ImageDraw

# Set canvas size
WIDTH, HEIGHT = 1024, 1024

# Create base image with black background
img = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(img)

# Define color palette inspired by Alex Grey's luminous spectra
palette = [
    (32, 0, 64),    # deep indigo
    (64, 0, 128),   # royal violet
    (0, 128, 255),  # electric blue
    (255, 165, 0),  # vibrant orange
    (255, 255, 0),  # golden yellow
    (255, 0, 128)   # magenta pulse
]

# Draw radiating lines for visionary geometry
center = (WIDTH // 2, HEIGHT // 2)
for i in range(360):
    angle = math.radians(i)
    radius = WIDTH // 2
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    color = palette[i % len(palette)]
    draw.line([center, (x, y)], fill=color, width=1)

# Overlay concentric circles for mandala symmetry
for r in range(50, WIDTH // 2, 50):
    color = palette[r // 50 % len(palette)]
    bbox = [center[0]-r, center[1]-r, center[0]+r, center[1]+r]
    draw.ellipse(bbox, outline=color)

# Add randomized star-like points for organic patterning
for _ in range(2000):
    x = random.randint(0, WIDTH-1)
    y = random.randint(0, HEIGHT-1)
    color = random.choice(palette)
    draw.point((x, y), fill=color)

# Save final image
img.save("Visionary_Dream.png")
