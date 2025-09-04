# Visionary Dream: Living Tarot Art
# Generates a museum-quality piece of visionary art inspired by Alex Grey.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Canvas configuration
width, height = 1920, 1080
dpi = 100
fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

# Coordinate grid
gx = np.linspace(-3, 3, width)
gy = np.linspace(-3, 3, height)
X, Y = np.meshgrid(gx, gy)

# Base pattern
Z = np.sin(X**2 + Y**2) + np.cos(3 * X) * np.sin(3 * Y)

# Custom palette inspired by Alex Grey's vivid spectrum
colors = ['#000000', '#0d0887', '#6a00a8', '#b12a90', '#fdca26']
cmap = LinearSegmentedColormap.from_list('alex_grey', colors)

# Render base layer
ax.imshow(Z, cmap=cmap, interpolation='bilinear')

# Overlay radial symmetry
theta = np.arctan2(Y, X)
radial = np.sin(10 * theta)
ax.imshow(radial, cmap='twilight', alpha=0.4, interpolation='bilinear')

# Save result
plt.savefig('Visionary_Dream.png', dpi=dpi, bbox_inches='tight', pad_inches=0)
plt.close()
