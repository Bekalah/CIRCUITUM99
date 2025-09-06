"""Visionary Dream Generator
Creates a museum-quality piece of visionary art using pure Python.
Color palette inspired by Alex Grey.
Resolution: 1920x1080.
Outputs Visionary_Dream.png.
"""

import math
import random
import struct
import zlib
from pathlib import Path

# Prepare canvas and output path
WIDTH, HEIGHT = 1920, 1080
OUTPUT = Path(__file__).resolve().parent.parent / "Visionary_Dream.png"

# Alex Grey-inspired palette
PALETTE = [
    (30, 30, 60),    # deep indigo
    (60, 90, 150),   # electric blue
    (120, 180, 200), # aquamarine
    (200, 100, 150), # magenta glow
    (240, 240, 200), # ethereal gold
]

# Initialize pixel buffer with background color
BASE = bytes(PALETTE[0])
PIXELS = bytearray(BASE * (WIDTH * HEIGHT))


def put_pixel(x: int, y: int, color: tuple[int, int, int]) -> None:
    """Set a pixel if within bounds."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        idx = (y * WIDTH + x) * 3
        PIXELS[idx:idx + 3] = bytes(color)


def draw_line(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
    """Bresenham line algorithm."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        put_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def draw_circle(cx: int, cy: int, radius: int, color: tuple[int, int, int]) -> None:
    """Approximate circle outline by connecting points."""
    prev_x = cx + radius
    prev_y = cy
    for deg in range(1, 361):
        rad = math.radians(deg)
        x = int(cx + radius * math.cos(rad))
        y = int(cy + radius * math.sin(rad))
        draw_line(prev_x, prev_y, x, y, color)
        prev_x, prev_y = x, y


def save_png(filename: Path) -> None:
    """Write the pixel buffer to a PNG file."""
    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        return (struct.pack("!I", len(data)) + chunk_type + data +
                struct.pack("!I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF))

    raw = b"".join(
        b"\x00" + PIXELS[y * WIDTH * 3:(y + 1) * WIDTH * 3]
        for y in range(HEIGHT)
    )

    with open(filename, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack("!IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        f.write(chunk(b"IEND", b""))


def main() -> None:
    """Generate visionary art and save as a PNG."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    max_radius = min(center_x, center_y)

    # Draw concentric circles for layered depth
    for i, color in enumerate(PALETTE[1:], start=1):
        radius = int(max_radius * i / len(PALETTE))
        draw_circle(center_x, center_y, radius, color)

    # Radiating symmetry lines
    num_lines = 90
    for i in range(num_lines):
        angle = 2 * math.pi * i / num_lines
        x = int(center_x + max_radius * math.cos(angle))
        y = int(center_y + max_radius * math.sin(angle))
        color = PALETTE[i % len(PALETTE)]
        draw_line(center_x, center_y, x, y, color)

    # Star-like points for organic patterning
    for _ in range(2000):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        color = random.choice(PALETTE)
        put_pixel(x, y, color)

    # Save the final visionary piece
    save_png(OUTPUT)


if __name__ == "__main__":
    main()

