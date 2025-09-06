"""Codex 144:99 ↔ Living Tarot Bridge
Generates visionary art influenced by a tarot card's codex aspects.
"""

# Imports
import math
import struct
import zlib
from typing import List, Tuple


# Data structures
class CodexEntry:
    """Codex 144:99 entry describing archetypal aspects."""

    def __init__(self, identifier: str, aspects: List[str]):
        self.identifier = identifier
        self.aspects = aspects


class TarotCard:
    """Living tarot card linked to a codex entry."""

    def __init__(self, name: str, codex: CodexEntry):
        self.name = name
        self.codex = codex


# Palette generation
def palette_from_aspects(aspects: List[str]) -> List[Tuple[int, int, int]]:
    """Rotate Alex Grey-inspired palette based on codex aspects."""
    base = [
        (15, 15, 61),   # deep indigo
        (30, 144, 255), # electric blue
        (255, 0, 255),  # magenta
        (255, 136, 0),  # orange
        (255, 255, 0),  # yellow
        (0, 255, 0),    # green
        (255, 255, 255) # white
    ]
    shift = sum(ord(ch) for ch in ''.join(aspects)) % len(base)
    return base[shift:] + base[:shift]


# Visionary art renderer
def render_card(card: TarotCard, width: int = 1024, height: int = 1024) -> None:
    """Render a visionary piece influenced by the card and save to Visionary_Dream.png."""
    palette = palette_from_aspects(card.codex.aspects)
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            # Normalized coordinates centered at zero
            nx = (x - width / 2) / (width / 2)
            ny = (y - height / 2) / (height / 2)
            r = math.hypot(nx, ny)
            angle = math.atan2(ny, nx)
            wave = math.sin(6 * r - 2 * angle)
            idx = int((wave + 1) / 2 * (len(palette) - 1))
            color = palette[idx]
            row.extend(color)
        pixels.append(bytes(row))

    write_png('Visionary_Dream.png', width, height, pixels)


# Minimal PNG writer
def write_png(filename: str, width: int, height: int, pixel_rows: List[bytes]) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack('!I', len(data)) +
            tag +
            data +
            struct.pack('!I', zlib.crc32(tag + data) & 0xffffffff)
        )

    with open(filename, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack('!2I5B', width, height, 8, 2, 0, 0, 0)))
        raw = b''.join(b'\x00' + row for row in pixel_rows)
        f.write(chunk(b'IDAT', zlib.compress(raw)))
        f.write(chunk(b'IEND', b''))


# Demonstration
if __name__ == "__main__":
    entry = CodexEntry("144:99", ["fire", "transcendence", "wisdom"])
    card = TarotCard("Egregore", entry)
    render_card(card)
