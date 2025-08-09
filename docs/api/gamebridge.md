# GameBridge • Book ⇄ Game API (LuxCrux V)

**Purpose:** Let game choices unlock/change Book content, and reading the Book unlocks game scenes/items -- without heavy code.

## Data Layer
- Path: `/games/luxcrux_v/data/save_state.json`
- Schema (v0.1):
```json
{
  "version": "0.1.0",
  "player_id": "anon",
  "flags": {
    "found_violet_sigil": false,
    "read_ch06": false,
    "forest_trial_passed": false
  },
  "inventory": [],
  "unlocked_scenes": [],
  "last_event_at": ""
}

---
### Unloackables

Game ← Book: when Chapter 06 front‑matter loads, set flags.read_ch06=true
On next game load: if read_ch06=true and not already in inventory, add aqua_lotus_pin

