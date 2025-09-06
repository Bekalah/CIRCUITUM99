"""Visionary Dream
Generates museum-quality visionary art using only the Python standard library.
"""

import math
import struct
import zlib

# Canvas configuration
WIDTH, HEIGHT = 1024, 1024

# Build pixel rows with psychedelic symmetry
pixels = []
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        # Normalized coordinates centered at zero
        nx = (x - WIDTH / 2) / (WIDTH / 2)
        ny = (y - HEIGHT / 2) / (HEIGHT / 2)
        r = math.hypot(nx, ny)
        angle = math.atan2(ny, nx)
        # Alex Grey-inspired chromatic waves
        red = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle)))
        green = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle + 2.094)))
        blue = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle + 4.188)))
        row.extend([red, green, blue])
    pixels.append(bytes(row))

# Minimal PNG writer

def chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", zlib.crc32(tag + data) & 0xFFFFFFFF)

with open("Visionary_Dream.png", "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n")
    f.write(chunk(b"IHDR", struct.pack("!2I5B", WIDTH, HEIGHT, 8, 2, 0, 0, 0)))
    raw = b"".join(b"\x00" + row for row in pixels)
    f.write(chunk(b"IDAT", zlib.compress(raw)))
    f.write(chunk(b"IEND", b""))
