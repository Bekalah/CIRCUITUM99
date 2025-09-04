"""Simple CLI engine for LuxCrux scenes.

Loads scene and item data from JSON files and persists player state.
Hooks `trigger_art` and `trigger_music` allow integration with the
`cosmogenesis-living-engine` repository for dynamic media.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

# Paths
BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets" / "inventory"
SCENE_DIR = ASSET_DIR / "SCENES"
ITEM_DIR = ASSET_DIR / "ASSETS" / "INVENTORY"
DATA_DIR = BASE_DIR / "data"
SAVE_STATE_FILE = DATA_DIR / "save_state.json"

@dataclass
class GameState:
    """Persistent game state."""

    version: str = "0.1.0"
    player_id: str = "anon"
    flags: Dict[str, bool] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)
    unlocked_scenes: List[str] = field(default_factory=lambda: ["00-prologue-violet-library"])
    last_event_at: str = ""

    def save(self) -> None:
        """Write state to disk."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.last_event_at = datetime.now(timezone.utc).isoformat()
        with SAVE_STATE_FILE.open("w") as fh:
            json.dump(self.__dict__, fh, indent=2)

    @classmethod
    def load(cls) -> "GameState":
        """Load state from disk or create default."""
        if SAVE_STATE_FILE.exists():
            with SAVE_STATE_FILE.open() as fh:
                data = json.load(fh)
            return cls(**data)
        state = cls()
        state.save()
        return state

def load_scene(scene_id: str) -> Dict:
    """Return scene data for given ID."""
    path = SCENE_DIR / f"{scene_id}.json"
    with path.open() as fh:
        return json.load(fh)

def apply_effects(state: GameState, effects: List[Dict]) -> str | None:
    """Apply effects to state and return next scene if unlocked."""
    next_scene = None
    for eff in effects:
        if "set_flag" in eff:
            state.flags[eff["set_flag"]] = eff.get("to", True)
        if "unlock_scene" in eff:
            next_scene = eff["unlock_scene"]
            if next_scene not in state.unlocked_scenes:
                state.unlocked_scenes.append(next_scene)
        if "add_item" in eff:
            item = eff["add_item"]
            if item not in state.inventory:
                state.inventory.append(item)
        if "trigger_art" in eff:
            trigger_art(eff["trigger_art"])
        if "trigger_music" in eff:
            trigger_music(eff["trigger_music"])
    state.save()
    return next_scene

def trigger_art(node_id: str) -> None:
    """Placeholder for cosmogenesis-living-engine art hook."""
    # Implementation would call external repository to generate art for node_id.
    pass

def trigger_music(node_id: str) -> None:
    """Placeholder for cosmogenesis-living-engine music hook."""
    # Implementation would call external repository to generate music for node_id.
    pass

def main() -> None:
    state = GameState.load()
    current_scene = state.unlocked_scenes[-1]
    while True:
        scene = load_scene(current_scene)
        print(f"\n{scene.get('title', current_scene)}")
        print("-" * 40)
        print(scene.get("text", ""))
        choices = scene.get("choices", [])
        for idx, choice in enumerate(choices, start=1):
            print(f"{idx}. {choice['label']}")
        try:
            selection = int(input("Select: ")) - 1
            chosen = choices[selection]
        except (ValueError, IndexError):
            print("Invalid choice. Try again.")
            continue
        next_scene = apply_effects(state, chosen.get("effects", []))
        if next_scene:
            current_scene = next_scene
        else:
            print("No further scenes unlocked. Game over.")
            break

if __name__ == "__main__":
    main()
