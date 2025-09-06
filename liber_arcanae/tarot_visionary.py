"""\
✦ Codex 144:99 - preserve original intention
Tarot-informed visionary art generator.
"""

import argparse
import json
import math
from pathlib import Path
from typing import List
from PIL import Image, ImageDraw

DATA_FILE = Path(__file__).resolve().parents[1] / "assets" / "data" / "tarot_absyssia.json"


def _hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def load_card(card_name: str) -> dict:
    """Load card metadata by name."""
    cards = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for card in cards:
        if card["name"].lower() == card_name.lower():
            return card
    raise ValueError(f"Card '{card_name}' not found")


def render(card: dict, width: int, height: int, out_dir: Path) -> Path:
    """Render visionary art using the card's palette."""
    colors: List[tuple] = [_hex_to_rgb(c) for c in card.get("palette", [])]
    if not colors:
        colors = [(40, 0, 80), (70, 0, 130), (0, 128, 255), (0, 255, 128), (255, 200, 0)]

    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    cx, cy = width // 2, height // 2

    # radiating lines
    for i in range(360):
        angle = math.radians(i * card["id"] + card.get("toneHz", 0) / 10)
        r = i / 360 * (min(width, height) // 2)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        draw.line((cx, cy, x, y), fill=colors[i % len(colors)], width=2)

    # concentric circles
    for r in range(40, min(width, height) // 2, 40):
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=colors[r // 40 % len(colors)], width=3)

    # card name footer
    draw.text((10, height - 30), card["name"], fill=colors[0])

    out_dir.mkdir(parents=True, exist_ok=True)
    filename = out_dir / f"Visionary_Dream_{card['name'].replace(' ', '_')}.png"
    img.save(filename)
    return filename


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate tarot-infused visionary art")
    parser.add_argument("--card", default="The Fool", help="Tarot card name")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--out", default="img", help="Output directory")
    args = parser.parse_args()

    card = load_card(args.card)
    path = render(card, args.width, args.height, Path(args.out))
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
