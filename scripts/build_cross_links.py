#!/usr/bin/env python3
"""Generate deterministic wormhole cross-links between nodes.

Creates registry/cross_links.json containing 99 wormhole mappings
based on a numerological offset (108) that maps node 3 -> node 111.
"""
import json
from pathlib import Path

NUM_NODES = 144
NUM_WORMHOLES = 99
OFFSET = 108  # sacred offset producing mapping 3 -> 111

def build_links(num_nodes: int = NUM_NODES,
                num_wormholes: int = NUM_WORMHOLES,
                offset: int = OFFSET):
    """Build a list of deterministic wormhole links."""
    links = []
    for src in range(1, num_wormholes + 1):
        dest = ((src + offset - 1) % num_nodes) + 1
        links.append({"from": src, "to": dest})
    return links

def main() -> None:
    links = build_links()
    out_path = Path('registry') / 'cross_links.json'
    out_path.write_text(json.dumps(links, indent=2))
    print(f"Wrote {out_path} with {len(links)} wormholes.")

if __name__ == "__main__":
    main()
