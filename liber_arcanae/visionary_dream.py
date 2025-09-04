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
# Generates a museum-quality piece of visionary art inspired by surrealism and Alex Grey using only the Python standard library.

import math
import struct
import zlib

# Canvas configuration
WIDTH, HEIGHT = 512, 512

# Build pixel array with psychedelic symmetry
pixels = []
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        # Normalized coordinates centered at zero
        nx = (x - WIDTH / 2) / (WIDTH / 2)
        ny = (y - HEIGHT / 2) / (HEIGHT / 2)
        r = math.hypot(nx, ny)
        angle = math.atan2(ny, nx)
        # Surreal color waves inspired by Alex Grey's palette
        red = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle)))
        green = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle + 2.094)))
        blue = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle + 4.188)))
        row.extend([red, green, blue])
    pixels.append(bytes(row))

# Minimal PNG writer

def write_png(filename, width, height, pixel_rows):
    # Assemble PNG chunks
    def chunk(tag, data):
        return (
            struct.pack('!I', len(data)) +
            tag +
            data +
            struct.pack('!I', zlib.crc32(tag + data) & 0xffffffff)
        )

    with open(filename, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')  # Signature
        f.write(chunk(b'IHDR', struct.pack('!2I5B', width, height, 8, 2, 0, 0, 0)))
        raw = b''.join(b'\x00' + row for row in pixel_rows)  # No filtering
        f.write(chunk(b'IDAT', zlib.compress(raw)))
        f.write(chunk(b'IEND', b''))

# Render visionary piece
write_png('Visionary_Dream.png', WIDTH, HEIGHT, pixels)
