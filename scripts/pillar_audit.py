#!/usr/bin/env python3
"""Pillar Audit Tool

Scans the `main/registry/pillars` directory to verify pillar files
follow naming conventions and that all 21 pillars exist.
"""

import re
from pathlib import Path

# Step 1: Locate pillar directory
PILLAR_DIR = Path(__file__).resolve().parents[1] / "main" / "registry" / "pillars"

# Step 2: Gather pillar files (exclude index)
files = [p for p in PILLAR_DIR.iterdir() if p.name != "index.md" and p.is_file()]

# Step 3: Extract pillar numbers from filenames
pattern = re.compile(r"^(\d{2})_")
found_numbers = []
unknown = []
for f in files:
    match = pattern.match(f.name)
    if match:
        found_numbers.append(int(match.group(1)))
    elif f.name.startswith("pillar_21"):
        found_numbers.append(21)
    else:
        unknown.append(f.name)

# Step 4: Determine missing pillars from expected 1-21
expected = set(range(1, 22))
found = set(found_numbers)
missing = sorted(expected - found)

# Step 5: Report audit findings
print(f"Pillar files found: {len(files)}")
print(f"Identified pillars: {sorted(found)}")
if missing:
    print(f"Missing pillars: {missing}")
else:
    print("All 21 pillars are present and accounted for.")
if unknown:
    print(f"Unrecognized files: {unknown}")
