#!/usr/bin/env python3
"""Primitive symbol-sound-visual generator for nodes.

Produces a simple PPM sigil, WAV tone, rudimentary animation frames,
 and a text invocation for a given node id using only the Python
standard library. Designed as a lightweight placeholder for the more
elaborate Visionary_Dream and Bilateral_Sound systems.
"""
import math
import struct
import wave
from pathlib import Path


def generate_sigil(node_id: int, out_dir: Path) -> Path:
    """Create a simple PPM image as a sigil."""
    size = 128
    path = out_dir / f"node_{node_id}_sigil.ppm"
    with open(path, "w") as f:
        f.write(f"P3\n{size} {size}\n255\n")
        for y in range(size):
            for x in range(size):
                val = (x * y * node_id) % 255
                f.write(f"{val} {255 - val} {(val * node_id) % 255} ")
            f.write("\n")
    return path


def generate_tone(node_id: int, out_dir: Path) -> Path:
    """Create a simple sine-wave tone."""
    path = out_dir / f"node_{node_id}_tone.wav"
    framerate = 44100
    duration = 1
    freq = 200 + node_id
    with wave.open(str(path), "w") as wav:
        wav.setparams((1, 2, framerate, duration * framerate, 'NONE', 'not compressed'))
        for i in range(duration * framerate):
            value = int(32767 * math.sin(2 * math.pi * freq * i / framerate))
            wav.writeframes(struct.pack('<h', value))
    return path


def generate_animation(node_id: int, out_dir: Path) -> Path:
    """Create a directory of PPM frames as a rudimentary animation."""
    anim_dir = out_dir / "animation"
    anim_dir.mkdir(exist_ok=True)
    size = 64
    frames = 10
    for frame in range(frames):
        frame_path = anim_dir / f"frame_{frame:03d}.ppm"
        with open(frame_path, "w") as f:
            f.write(f"P3\n{size} {size}\n255\n")
            for y in range(size):
                for x in range(size):
                    val = (x * node_id + frame * y) % 255
                    f.write(f"{val} {(val + 80) % 255} {(255 - val) % 255} ")
                f.write("\n")
    return anim_dir


def generate_invocation(node_id: int, out_dir: Path) -> Path:
    """Write a simple text invocation."""
    path = out_dir / f"node_{node_id}_invocation.txt"
    path.write_text(f"Invocation for node {node_id}\n")
    return path


def generate(node_id: int) -> None:
    out_dir = Path("assets") / f"node_{node_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    sigil = generate_sigil(node_id, out_dir)
    tone = generate_tone(node_id, out_dir)
    anim = generate_animation(node_id, out_dir)
    invocation = generate_invocation(node_id, out_dir)
    print(f"Created {sigil}, {tone}, {anim}, {invocation}")


if __name__ == "__main__":
    import sys
    node_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    generate(node_id)
