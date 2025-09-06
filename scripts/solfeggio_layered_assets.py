#!/usr/bin/env python3
"""Generate visionary art and lossless solfeggio tones for 144 nodes.

Each node receives:
- A high-resolution visionary image inspired by Alex Grey's palette.
- A lossless WAV tone based on a solfeggio frequency.
The script defaults to generating assets for all 144 nodes but can be
limited via ``--count`` for testing.
"""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path
import shutil

# --- Configuration ---------------------------------------------------------
WIDTH, HEIGHT = 1024, 1024  # Resolution for each image
PALETTE = [
    (48, 0, 108),    # deep indigo
    (0, 33, 105),    # cosmic blue
    (0, 148, 68),    # vivid green
    (241, 243, 54),  # radiant yellow
    (255, 153, 0),   # luminous orange
    (208, 0, 0),     # crimson red
    (115, 0, 128),   # ultraviolet magenta
]
SOLFEGGIO = [174, 285, 396, 417, 528, 639, 741, 852, 963]
FRAMERATE = 48000  # High-quality audio
DURATION = 2       # seconds


# --- Asset Generators -----------------------------------------------------
def generate_image(node_id: int, out_dir: Path) -> Path:
    """Create a symmetrical visionary image for the given node in PPM format."""
    path = out_dir / f"node_{node_id:03d}_vision.ppm"
    center_x, center_y = WIDTH / 2, HEIGHT / 2
    with open(path, "w") as f:
        f.write(f"P3\n{WIDTH} {HEIGHT}\n255\n")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - center_x
                dy = y - center_y
                angle = math.atan2(dy, dx)
                dist = math.hypot(dx, dy)
                line = int((angle % (2 * math.pi)) / (2 * math.pi / 144))
                ring = int(dist / 20)
                r, g, b = PALETTE[(line + ring) % len(PALETTE)]
                f.write(f"{r} {g} {b} ")
            f.write("\n")
    if node_id == 1:
        preview_dir = Path("img")
        preview_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, preview_dir / "Visionary_Dream.ppm")
    return path


def generate_audio(node_id: int, freq: int, out_dir: Path) -> Path:
    """Create a lossless WAV tone for the given node."""
    path = out_dir / f"node_{node_id:03d}_tone.wav"
    with wave.open(str(path), "w") as wav:
        wav.setparams((1, 2, FRAMERATE, 0, "NONE", "not compressed"))
        for i in range(DURATION * FRAMERATE):
            sample = int(32767 * math.sin(2 * math.pi * freq * i / FRAMERATE))
            wav.writeframes(struct.pack('<h', sample))
    return path


def generate_node(node_id: int) -> None:
    """Generate both audio and visual assets for a single node."""
    out_dir = Path("assets") / f"node_{node_id:03d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    freq = SOLFEGGIO[(node_id - 1) % len(SOLFEGGIO)]
    generate_image(node_id, out_dir)
    generate_audio(node_id, freq, out_dir)


# --- Entrypoint ------------------------------------------------------------
def main(count: int = 144) -> None:
    for node_id in range(1, count + 1):
        generate_node(node_id)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate assets for nodes.")
    parser.add_argument(
        "--count", type=int, default=144, help="Number of nodes to generate"
    )
    args = parser.parse_args()
    main(args.count)
