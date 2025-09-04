# Games

## LuxCrux V Engine

A minimal choose-your-own adventure runner for experimental scenes and
items. Scene and item data live under `games/luxcrux_v/assets` and player
progress persists in `games/luxcrux_v/data/save_state.json`.

### Run

```
python games/luxcrux_v/engine.py
```

### Media Hooks

`engine.py` exposes `trigger_art` and `trigger_music` functions. They are
stubs intended to call into the `cosmogenesis-living-engine` repository
so that choices can dynamically generate art or music for each node.
