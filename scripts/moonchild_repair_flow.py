#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moonchild Repair Flow (PATCH-only, layout auto-detect)

- Scans known registry nodes and proposes non-destructive patches:
  * H1 title
  * Registry line (fixed coordinates)
  * Invisible symbolbus header comment

- Writes PATCH suggestions to:
    registry/04_registry-meta/system/logs/moonchild/
  (or main/registry/... if that layout exists)

- Never edits tracked files directly.
"""
from __future__ import annotations
import os, re
from pathlib import Path
from datetime import datetime

# ---------- ROOT & REGISTRY AUTO-DETECT ----------
ROOT = Path(__file__).resolve().parents[1]  # repo root
REG = None
for candidate in [ROOT / "registry", ROOT / "main" / "registry"]:
    if candidate.exists():
        REG = candidate
        break
if REG is None:
    raise SystemExit("❌ Could not find registry root. Expected 'registry/' or 'main/registry/'")

LOGS = REG / "04_registry-meta" / "system" / "logs" / "moonchild"
QUAR = REG / "04_registry-meta" / "system" / "quarantine"

# ---------- TARGET PATHS (match your repo exactly) ----------
# NOTE: your repo uses uppercase 'CHARACTERS' and underscore filename
P_MOONCHILD_PROFILE = REG / "CHARACTERS" / "moonchild" / "moonchild_profile.md"
P_MOONCHILD_LAYERS  = REG / "CHARACTERS" / "moonchild" / "meta_layers" / "moonchild_meta_layers.md"
P_MOONCHILD_PARADOX = REG / "CHARACTERS" / "moonchild" / "crowley_paradox.md"  # create later if needed

P_GATE_11 = REG / "01_main-narrative" / "gate_11.md"
P_GATE_22 = REG / "01_main-narrative" / "gate_22.md"
P_GATE_33 = REG / "01_main-narrative" / "gate_33.md"

DIR_REALMS = REG / "02_grimoire" / "realms"

# ---------- REGEX ----------
RE_HEADER_COMMENT = re.compile(r'<!--\s*symbolbus:.*?-->\s*$', re.IGNORECASE)
RE_HAS_H1         = re.compile(r'^\s*#\s+', re.MULTILINE)

def ts():
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except:
        return ""

def write_patch_for(target: Path, patch_body: str) -> Path:
    LOGS.mkdir(parents=True, exist_ok=True)
    out = LOGS / f"PATCH_{target.name}.{ts()}.md"
    out.write_text(patch_body, encoding="utf-8")
    return out

def inject_after_frontmatter(txt: str, inject: str) -> str:
    lines = txt.splitlines()
    if lines[:1] == ["---"]:
        try:
            close = next(i for i, L in enumerate(lines[1:], 1) if L.strip() == "---")
            return "\n".join(lines[:close+1] + ["", inject, ""] + lines[close+1:])
        except StopIteration:
            return inject + "\n\n" + txt
    return inject + "\n\n" + txt

def ensure_title_and_registry(txt: str, title: str, coord: str):
    steps = []
    def block():
        return f"# {title}\n_Registry Node: Circuitum 99 -- Alpha et Omega / {coord}_"
    lines = txt.splitlines()
    if lines[:1] == ["---"]:
        if not RE_HAS_H1.search("\n".join(lines[:300])):
            patched = inject_after_frontmatter(txt, block())
            steps.append("Insert H1 + Registry after YAML frontmatter.")
            return patched, steps
        # has some H1; ensure registry line under it
        idx_after_yaml = 0
        try:
            idx_after_yaml = next(i for i, L in enumerate(lines[1:], 1) if L.strip() == "---") + 1
        except StopIteration:
            idx_after_yaml = 0
        h1 = next((i for i in range(idx_after_yaml, min(idx_after_yaml+10, len(lines)))
                   if lines[i].lstrip().startswith("# ")), None)
        if h1 is not None and (h1+1 >= len(lines) or "Registry Node:" not in lines[h1+1]):
            new = lines[:h1+1] + [f"_Registry Node: Circuitum 99 -- Alpha et Omega / {coord}_", ""] + lines[h1+1:]
            steps.append("Insert Registry line under existing H1 after frontmatter.")
            return "\n".join(new), steps
    else:
        if not lines or not lines[0].lstrip().startswith("# "):
            patched = block() + "\n\n" + txt
            steps.append("Insert H1 + Registry at top.")
            return patched, steps
        if len(lines) < 2 or "Registry Node:" not in lines[1]:
            new = [lines[0], f"_Registry Node: Circuitum 99 -- Alpha et Omega / {coord}_", ""] + lines[1:]
            steps.append("Insert Registry line under existing H1.")
            return "\n".join(new), steps
    return txt, steps

def ensure_symbolbus(txt: str, symbolbus_line: str):
    steps = []
    head = "\n".join(txt.splitlines()[:50])
    if RE_HEADER_COMMENT.search(head):
        return txt, steps
    lines = txt.splitlines()
    insert_idx = 0
    if lines[:1] == ["---"]:
        try:
            insert_idx = next(i for i, L in enumerate(lines[1:], 1) if L.strip() == "---") + 1
        except StopIteration:
            insert_idx = 0
    else:
        if lines and lines[0].lstrip().startswith("# "):
            insert_idx = 2 if len(lines) >= 2 else 1
    new_lines = lines[:insert_idx] + [symbolbus_line, ""] + lines[insert_idx:]
    steps.append("Insert invisible symbolbus header.")
    return "\n".join(new_lines), steps

def make_patch(target: Path, original: str, proposed: str, steps):
    if not steps:
        return
    prop_lines = proposed.splitlines()
    snippet = "\n".join(prop_lines[:12])
    patch = (
        f"# PATCH for {target}\n\n"
        "## Steps\n" + "\n".join(f"- {s}" for s in steps) +
        "\n\n## Snippet (paste at indicated location)\n```markdown\n" +
        snippet + "\n```"
    )
    out = write_patch_for(target, patch)
    print(f"  ↳ Wrote PATCH: {out.relative_to(ROOT)}")

def process_known_file(target: Path, title: str, coord: str, symbolbus_line: str):
    print(f"• Scan: {target.relative_to(ROOT)}")
    if not target.exists():
        print("  ⚠ Skipped (missing).")
        return
    t0 = read_text(target)
    t1, a = ensure_title_and_registry(t0, title, coord)
    t2, b = ensure_symbolbus(t1, symbolbus_line)
    steps = a + b
    if steps:
        make_patch(target, t0, t2, steps)
    else:
        print("  ✓ OK (headers present)")

def process_gate(p: Path, num: int):
    process_known_file(
        p,
        f"Gate {num} -- <Chapter Title>",
        f"narrative:gate / coord: GATE-{num}",
        f"<!-- symbolbus: numkey={num} | geom=vesica | chrom=silver_yesod | pHour=Moon | gate=true -->"
    )

def process_realms(dir_path: Path):
    if not dir_path.exists():
        print(f"• Scan: {dir_path.relative_to(ROOT)} (no realms dir yet)")
        return
    for rp in sorted(dir_path.glob("*.md")):
        slug = rp.stem.upper().replace(" ", "_")
        title = f"{rp.stem.replace('_', ' ').title()} -- Grimoire Entry"
        process_known_file(
            rp,
            title,
            f"grimoire:realm / coord: REALM-{slug}",
            "<!-- symbolbus: numkey=33 | geom=vesica | chrom=octarine_violet -->"
        )

def banner():
    print("\n" + "="*72)
    print("  MOONCHILD REPAIR FLOW -- PATCH-ONLY INITIALIZER (auto-detect layout)")
    print("="*72)
    print("Writes PATCH suggestions -> registry/.../logs/moonchild/  (no edits)\n"
          "Approve manually, then append <!-- lock:saturn --> at page bottom.\n")

def main():
    banner()
    LOGS.mkdir(parents=True, exist_ok=True)
    QUAR.mkdir(parents=True, exist_ok=True)

    # Moonchild registry nodes
    process_known_file(
        P_MOONCHILD_PROFILE,
        "Moonchild -- Canon Profile (Registry)",
        "characters:moonchild / coord: MC-PROFILE-0001",
        "<!-- symbolbus: numkey=33 | geom=vesica | chrom=silver_yesod | pHour=Moon -->"
    )
    process_known_file(
        P_MOONCHILD_LAYERS,
        "Moonchild -- Meta Layers (Angelic OS)",
        "characters:moonchild:meta_layers / coord: MC-LAYERS-0001",
        "<!-- symbolbus: numkey=33 | geom=vesica | chrom=octarine_violet | pHour=Moon -->"
    )
    process_known_file(
        P_MOONCHILD_PARADOX,
        "The Crowley Paradox -- Moonchild Registry Notes",
        "characters:moonchild:paradox / coord: MC-PARADOX-0001",
        "<!-- symbolbus: numkey=33 | geom=vesica -->"
    )

    # Gates (only if you create these files)
    process_gate(P_GATE_11, 11)
    process_gate(P_GATE_22, 22)
    process_gate(P_GATE_33, 33)

    # Realms (picked up automatically when you add files)
    process_realms(DIR_REALMS)

    print("\n✓ Done. Review PATCH files in logs and paste into targets you approve.")
    print("  After pasting, add this at the bottom of each approved page:\n    <!-- lock:saturn -->\n")

if __name__ == "__main__":
    main()