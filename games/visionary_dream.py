#!/usr/bin/env python3
"""Visionary Dream: generative art inspired by Alex Grey and tarot geometry."""

import numpy as np
from PIL import Image, ImageDraw
import colorsys

# Set gallery-grade canvas size
WIDTH, HEIGHT = 1920, 1080

# Lay out a coordinate grid for our cosmic canvas
x = np.linspace(-3, 3, WIDTH)
y = np.linspace(-3, 3, HEIGHT)
X, Y = np.meshgrid(x, y)

# Sculpt radial and angular fields to evoke immersive realms
radius = np.sqrt(X**2 + Y**2)
angle = np.arctan2(Y, X)

# Weave trigonometric waves for psychedelic motion
waves = np.sin(radius * 3) + np.cos(angle * 4)

# Blend geometry into an organic tapestry
pattern = np.sin(radius + waves)

# Mirror the tapestry for mandala-like symmetry
pattern = (pattern + np.flip(pattern, axis=1)) / 2

# Normalize to 0–1 to prepare for color mapping
norm = (pattern - pattern.min()) / (pattern.max() - pattern.min())

# Alex Grey–inspired spectral palette
def spectral_palette(v):
    return tuple(int(255 * i) for i in colorsys.hsv_to_rgb(v, 1.0, 1.0))

# Paint the canvas with radiant color
color_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for i in range(HEIGHT):
    for j in range(WIDTH):
        color_array[i, j] = spectral_palette(norm[i, j])

# Wrap into a Pillow image
img = Image.fromarray(color_array)

# Inscribe a tarot pentagram to bridge art and myth
draw = ImageDraw.Draw(img)
center = (WIDTH // 2, HEIGHT // 2)
r = HEIGHT // 4
vertices = []
for n in range(5):
    theta = np.pi / 2 + n * 2 * np.pi / 5
    vertices.append((center[0] + r * np.cos(theta),
                     center[1] + r * np.sin(theta)))
star = [vertices[i % 5] for i in (0, 2, 4, 1, 3)]
draw.line(star + [star[0]], fill=(255, 255, 255), width=3)

# Save the visionary masterpiece
img.save("Visionary_Dream.png")
