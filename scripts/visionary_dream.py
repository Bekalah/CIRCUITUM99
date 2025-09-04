# Visionary Dream Generator
# Produces museum-quality visionary art using Python + Pillow

from PIL import Image, ImageDraw
import math
import random
from pathlib import Path

# Step 1: Prepare canvas and output
WIDTH, HEIGHT = 1024, 1024  # Resolution
output_path = Path(__file__).resolve().parents[1] / "img" / "Visionary_Dream.png"

# Step 2: Create a midnight backdrop for the vision
image = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(image)

# Step 3: Set the psychedelic palette (Alex Grey meets surrealism)
palette = ["#6A0DAD", "#FF6F61", "#00FFFF", "#FFD700", "#1E90FF"]

# Step 4: Weave radiating symmetry lines from the center
center = (WIDTH // 2, HEIGHT // 2)
for i in range(360):
    angle = math.radians(i * 3)
    radius = i / 360 * (WIDTH // 2)
    x = center[0] + radius * math.cos(angle * 2)
    y = center[1] + radius * math.sin(angle * 2)
    draw.line([center, (x, y)], fill=palette[i % len(palette)], width=2)

# Step 5: Overlay concentric orbs for layered depth
for r in range(50, WIDTH // 2, 25):
    color = random.choice(palette)
    draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], outline=color, width=3)

# Step 6: Seal the vision as a PNG image
output_path.parent.mkdir(parents=True, exist_ok=True)
image.save(output_path)
