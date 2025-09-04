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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def main() -> None:
    """Generate a spiral mandala with an Alex Grey-inspired palette."""
    # -- Visionary Dream generator --
    # Resolution for museum-quality output
    WIDTH, HEIGHT = 1024, 1024

    # Create a spectral palette inspired by Alex Grey
    colors = [
        (48/255, 0/255, 108/255),   # deep indigo
        (0/255, 33/255, 105/255),   # cosmic blue
        (0/255, 148/255, 68/255),   # vivid green
        (241/255, 243/255, 54/255), # radiant yellow
        (255/255, 153/255, 0/255),  # luminous orange
        (208/255, 0/255, 0/255),    # crimson red
        (115/255, 0/255, 128/255)   # ultraviolet magenta
    ]
    cmap = LinearSegmentedColormap.from_list("alex_grey", colors, N=256)

    # Prepare a radial grid for symmetrical patterns
    x = np.linspace(-4 * np.pi, 4 * np.pi, WIDTH)
    y = np.linspace(-4 * np.pi, 4 * np.pi, HEIGHT)
    X, Y = np.meshgrid(x, y)

    # Calculate spiral waves to form a mandala
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    Z = np.sin(R + Theta * 3) * np.cos(R * 2 - Theta * 5)

    # Render the visionary art
    plt.figure(figsize=(WIDTH/100, HEIGHT/100), dpi=100)
    plt.axis("off")
    plt.imshow(Z, cmap=cmap, interpolation="bilinear")
    plt.tight_layout(pad=0)

    # Save the final image
    plt.savefig("Visionary_Dream.png", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    main()

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
