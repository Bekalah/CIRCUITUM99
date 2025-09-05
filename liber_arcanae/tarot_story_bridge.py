"""Tarot Story Bridge
Connects Codex 144:99 aspects with tarot card metadata to seed a
choose-your-own-adventure narrative.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from codex_tarot_bridge import CodexEntry, TarotCard

# Narrative snippets mapped to codex aspects
STORY_SNIPPETS: Dict[str, str] = {
    "fire": "Flames dance around you, forging a path through the void.",
    "transcendence": "Your spirit rises, glimpsing realms beyond form.",
    "wisdom": "An ancient owl speaks in riddles of forgotten stars.",
}


def load_tarot_card(name: str, aspects: List[str]) -> TarotCard:
    """Load tarot metadata and bind it to Codex aspects."""
    data_path = Path(__file__).resolve().parents[1] / "assets" / "data" / "tarot_absyssia.json"
    with open(data_path) as f:
        tarot_data = json.load(f)
    card_info = next(card for card in tarot_data if card["name"].lower() == name.lower())
    codex = CodexEntry("144:99", aspects)
    return TarotCard(card_info["name"], codex)


def generate_story(card: TarotCard) -> str:
    """Compose a narrative seed using the card's codex aspects."""
    fragments = [STORY_SNIPPETS.get(a, f"The aspect of {a} guides your steps.") for a in card.codex.aspects]
    parts = " ".join(fragments)
    return f"You draw {card.name}. {parts}"


if __name__ == "__main__":
    # Example: bind codex aspects to The Fool and print the narrative seed
    tarot = load_tarot_card("The Fool", ["fire", "transcendence", "wisdom"])
    print(generate_story(tarot))
