
"""Visionary Dream
Generates museum-quality visionary art using only the Python standard library.
"""

"""Liber Arcanae Visionary Dream generator.

This script showcases two approaches for crafting visionary art:

``matplotlib``
    Uses :mod:`numpy` and :mod:`matplotlib` to render layered spectral
    patterns.

``minimal``
    Relies only on the Python standard library to write a PNG file using a
    simple mathematical color field.
"""

from __future__ import annotations

import argparse
import math
import struct
import zlib

# ---------------------------------------------------------------
# Palette definitions
# ---------------------------------------------------------------
PALETTES = {
    "alex_grey": ["#000000", "#0d0887", "#6a00a8", "#b12a90", "#fdca26"],
    "surreal": ["#1b0034", "#3d0071", "#ff6f61", "#ffd700", "#00ffff"],
}


# ---------------------------------------------------------------
# Matplotlib-based renderer
# ---------------------------------------------------------------
def generate_matplotlib(width: int, height: int, palette: list[str], out: str) -> None:
    """Render layered mandala patterns using numpy/matplotlib."""


    import numpy as np  # local import to allow minimal mode without numpy
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    dpi = 100
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    # Coordinate grid
    gx = np.linspace(-3, 3, width)
    gy = np.linspace(-3, 3, height)
    X, Y = np.meshgrid(gx, gy)

    # Base pattern with sinusoidal waves
    Z = np.sin(X ** 2 + Y ** 2) + np.cos(3 * X) * np.sin(3 * Y)

    cmap = LinearSegmentedColormap.from_list("custom", palette)
    ax.imshow(Z, cmap=cmap, interpolation="bilinear")


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

    # Overlay radial symmetry for extra depth
    theta = np.arctan2(Y, X)
    radial = np.sin(10 * theta)
    ax.imshow(radial, cmap="twilight", alpha=0.4, interpolation="bilinear")

    plt.savefig(out, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


# ---------------------------------------------------------------
# Minimal standard library renderer
# ---------------------------------------------------------------
def generate_minimal(width: int, height: int, out: str) -> None:
    """Write a PNG using only the standard library."""

    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            nx = (x - width / 2) / (width / 2)
            ny = (y - height / 2) / (height / 2)
            r = math.hypot(nx, ny)
            angle = math.atan2(ny, nx)
            red = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle)))
            green = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle + 2.094)))
            blue = int(255 * (0.5 + 0.5 * math.sin(6 * r - 2 * angle + 4.188)))
            row.extend([red, green, blue])
        pixels.append(bytes(row))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack("!I", len(data))
            + tag
            + data
            + struct.pack("!I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    with open(out, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack("!2I5B", width, height, 8, 2, 0, 0, 0)))
        raw = b"".join(b"\x00" + row for row in pixels)
        f.write(chunk(b"IDAT", zlib.compress(raw)))
        f.write(chunk(b"IEND", b""))


# ---------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Liber Arcanae visionary demo")
    parser.add_argument("--mode", choices=["matplotlib", "minimal"], default="matplotlib")
    parser.add_argument("--palette", choices=sorted(PALETTES.keys()), default="alex_grey")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--out", default="Visionary_Dream.png")
    args = parser.parse_args()

    if args.mode == "matplotlib":
        generate_matplotlib(args.width, args.height, PALETTES[args.palette], args.out)
    else:
        generate_minimal(args.width, args.height, args.out)


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()


