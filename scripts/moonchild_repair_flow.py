#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moonchild Repair Flow (PATCH-only)
- Scans known registry nodes and proposes non-destructive patches:
  * H1 title line
  * Registry line (fixed coordinates)
  * Invisible symbolbus header comment
- Writes PATCH suggestions to:
    main/registry/04_registry-meta/system/logs/moonchild/
- Never edits tracked files directly.

Run:
  python3 main/scripts/moonchild_repair_flow.py
"""

from __future__ import annotations
import re
import os
from pathlib import Path
from datetime import datetime

# ---------- FIXED COORDINATES / PATHS ----------
ROOT = Path(__file__).resolve().parents[1]             # repo root assumed at 'main/'
REG  = ROOT / "main" / "registry"                      # main/registry
LOGS = REG / "04_registry-meta" / "system" / "logs" / "moonchild"
QUAR = REG / "04_registry-meta" / "system" / "quarantine"

# Targets
P_MOONCHILD_PROFILE = REG / "characters" / "moonchild" / "moonchild-profile.md"
P_MOONCHILD_LAYERS  = REG / "characters" / "moonchild" / "meta_layers" / "moonchild_meta_layers.md"
P_MOONCHILD_PARADOX = REG / "characters" / "moonchild" / "crowley_paradox.md"

P_GATE_11 = REG / "01_main-narrative" / "gate_11.md"
P_GATE_22 = REG / "01_main-narrative" / "gate_22.md"
P_GATE_33 = REG / "01_main-narrative" / "gate_33.md"

DIR_REALMS = REG / "02_grimoire" / "realms"            # *.md

# ---------- REGEX ----------
RE_HEADER_COMMENT = re.compile(r'<!--\s*symbolbus:.*?-->\s*$', re.IGNORECASE)
RE_HAS_H1         = re.compile(r'^\s*#\s+', re.MULTILINE)
RE_YAML_START     = re.compile(r'^\s*---\s*$', re.MULTILINE)

# ---------- UTIL ----------
def ts() -> str:
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

def write_patch_for(target: Path, patch_body: str) -> Path:
    LOGS.mkdir(parents=True, exist_ok=True)
    filename = f"PATCH_{target.name}.{ts()}.md"
    out = LOGS / filename
    out.write_text(patch_body, encoding="utf-8")
    return out

def title_case_from_filename(p: Path) -> str:
    name = p.stem.replace("_", " ").strip()
    return " ".join(w.capitalize() for w in name.split())

def inject_after_frontmatter(txt: str, inject: str) -> str:
    """
    If YAML frontmatter exists (--- ... ---), inject after it. Otherwise at very top.
    """
    lines = txt.splitlines()
    if len(lines) >= 1 and lines[0].strip() == "---":
        # find closing ---
        try:
            close_idx = next(i for i, L in enumerate(lines[1:], start=1) if L.strip() == "---")
            return "\n".join(lines[:close_idx+1] + [""] + [inject] + [""] + lines[close_idx+1:])
        except StopIteration:
            # malformed frontmatter; just put at top
            return inject + "\n\n" + txt
    else:
        return inject + "\n\n" + txt

def ensure_title_and_registry(txt: str, title: str, coord: str) -> tuple[str, list[str]]:
    """
    Ensure first two visible lines are H1 + registry line.
    Returns (maybe_new_text, patch_steps)
    """
    patch_steps = []
    # If there is YAML frontmatter at the very beginning, we preserve it and inject after.
    def build_block():
        return f"# {title}\n_Registry Node: Circuitum 99 -- Alpha et Omega / {coord}_"

    if txt.startswith("---\n"):
        # Respect frontmatter; check if we already have the H1 + registry immediately after fm.
        # Simpler approach: always propose inserting after frontmatter if missing H1 or registry line.
        body_after = txt
        # We will evaluate presence later; easier: detect H1 anywhere near top
        if not RE_HAS_H1.search(txt[:300]):
            # propose injecting both lines after frontmatter
            patched = inject_after_frontmatter(txt, build_block())
            patch_steps.append("Insert H1 title + Registry line after YAML frontmatter.")
            return patched, patch_steps
        else:
            # Has some H1; ensure second line includes "Registry Node:"
            lines = txt.splitlines()
            # Try to find first non-frontmatter content line index
            idx = 0
            if lines and lines[0].strip() == "---":
                try:
                    idx = next(i for i, L in enumerate(lines[1:], start=1) if L.strip() == "---") + 1
                except StopIteration:
                    idx = 0
            # After idx, if the next line doesn't contain "Registry Node:" propose inserting it beneath the first H1 we encounter.
            h1_idx = None
            for i in range(idx, min(idx+10, len(lines))):
                if lines[i].lstrip().startswith("# "):
                    h1_idx = i
                    break
            if h1_idx is not None:
                if (h1_idx + 1 >= len(lines)) or ("Registry Node:" not in lines[h1_idx+1]):
                    # build registry line only
                    new_lines = lines[:h1_idx+1] + [f"_Registry Node: Circuitum 99 -- Alpha et Omega / {coord}_", ""] + lines[h1_idx+1:]
                    patch_steps.append("Insert Registry line under existing H1 after YAML frontmatter.")
                    return "\n".join(new_lines), patch_steps
    else:
        # No frontmatter; check first two lines
        lines = txt.splitlines()
        changed = False
        if not lines or not lines[0].lstrip().startswith("# "):
            # insert both lines at top
            patched = build_block() + "\n\n" + txt
            patch_steps.append("Insert H1 title + Registry line at top.")
            return patched, patch_steps
        else:
            # has H1; ensure next line is registry
            if len(lines) < 2 or "Registry Node:" not in lines[1]:
                new_lines = [lines[0], f"_Registry Node: Circuitum 99 -- Alpha et Omega / {coord}_", ""] + lines[1:]
                patch_steps.append("Insert Registry line under existing H1.")
                return "\n".join(new_lines), patch_steps

    # If we get here, nothing needed
    return txt, patch_steps

def ensure_symbolbus(txt: str, symbolbus_line: str) -> tuple[str, list[str]]:
    """
    Ensure the invisible symbolbus comment is present within first ~50 lines.
    """
    patch_steps = []
    head = "\n".join(txt.splitlines()[:50])
    if RE_HEADER_COMMENT.search(head):
        return txt, patch_steps
    # Insert the symbolbus under the H1/registry block or right after frontmatter injection we already proposed
    lines = txt.splitlines()
    insert_idx = 0
    if lines and lines[0].strip() == "---":
        # place after closing fm and possibly after H1+registry if they exist
        try:
            close_idx = next(i for i, L in enumerate(lines[1:], start=1) if L.strip() == "---")
            insert_idx = close_idx + 1
        except StopIteration:
            insert_idx = 0
    else:
        # if first line is H1 and second is registry, place after them
        if lines and lines[0].lstrip().startswith("# "):
            insert_idx = 2 if len(lines) >= 2 else 1
    new_lines = lines[:insert_idx] + [symbolbus_line, ""] + lines[insert_idx:]
    patch_steps.append("Insert invisible symbolbus header.")
    return "\n".join(new_lines), patch_steps

def make_patch(target: Path, original: str, proposed: str, steps: list[str]) -> None:
    if not steps:
        return
    patch = [
        f"# PATCH for {target}",
        "",
        "## Steps",
        *[f"- {s}" for s in steps],
        "",
        "## Snippet (paste at indicated location)",
        "```markdown",
    ]
    # Build minimal snippet: only the *added* top block lines for safety.
    # We’ll diff by lines to include only new ones.
    orig_lines = original.splitlines()
    prop_lines = proposed.splitlines()
    # naive: include first ~12 lines of proposed version (headers area)
    snippet = "\n".join(prop_lines[:12])
    patch.append(snippet)
    patch.append("```")
    out = write_patch_for(target, "\n".join(patch))
    print(f"  ↳ Wrote PATCH: {out.relative_to(ROOT)}")

# ---------- TASKS ----------
def process_known_file(target: Path, title: str, coord: str, symbolbus_line: str):
    print(f"• Scan: {target.relative_to(ROOT)}")
    if not target.exists():
        print("  ⚠ Skipped (missing).")
        return
    txt0 = read_text(target)
    txt1, stepsA = ensure_title_and_registry(txt0, title, coord)
    txt2, stepsB = ensure_symbolbus(txt1, symbolbus_line)
    steps = stepsA + stepsB
    if steps:
        make_patch(target, txt0, txt2, steps)
    else:
        print("  ✓ OK (headers already present)")

def process_gate(gate_file: Path, gate_num: int):
    title = f"Gate {gate_num} -- <Chapter Title>"
    coord = f"narrative:gate / coord: GATE-{gate_num}"
    symbolbus = f"<!-- symbolbus: numkey={gate_num} | geom=vesica | chrom=silver_yesod | pHour=Moon | gate=true -->"
    process_known_file(gate_file, title, coord, symbolbus)

def process_realms(dir_path: Path):
    if not dir_path.exists():
        print(f"• Scan: {dir_path.relative_to(ROOT)} (no realms directory yet)")
        return
    for md in sorted(dir_path.glob("*.md")):
        slug = md.stem.upper()
        pretty = f"{title_case_from_filename(md)} -- Grimoire Entry"
        coord = f"grimoire:realm / coord: REALM-{slug}"
        symbolbus = "<!-- symbolbus: numkey=33 | geom=vesica | chrom=octarine_violet -->"
        process_known_file(md, pretty, coord, symbolbus)

def banner():
    print("\n" + "="*72)
    print("  MOONCHILD REPAIR FLOW -- PATCH-ONLY INITIALIZER")
    print("="*72)
    print("This will scan known nodes and write PATCH suggestions (no edits).")
    print("PATCHes go to: main/registry/04_registry-meta/system/logs/moonchild/")
    print("Approve manually, then append <!-- lock:saturn --> at page bottom.\n")

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

    # Gate files
    process_gate(P_GATE_11, 11)
    process_gate(P_GATE_22, 22)
    process_gate(P_GATE_33, 33)

    # Realms
    process_realms(DIR_REALMS)

    print("\n✓ Done. Review PATCH files in logs and paste into targets you approve.")
    print("  After pasting, add this at the bottom of each approved page:\n")
    print("    <!-- lock:saturn -->\n")
# -------- CHAPTER INDEX PROPOSAL (book/chapters -> registry index) --------
def human_title_from_filename(fname: str) -> str:
    # "10-circuitum99-formation.md" -> "10 -- Circuitum99 Formation"
    stem = Path(fname).stem
    parts = stem.split("-", 1)
    if len(parts) == 2 and parts[0].isdigit():
        num, rest = parts
        title = rest.replace("-", " ").strip().title()
        return f"{num} -- {title}"
    # fallback
    return stem.replace("-", " ").strip().title()

def propose_chapter_index():
    chapters_dir = ROOT / "book" / "chapters"
    index_target = REG / "01_main-narrative" / "chapters_index.md"
    if not chapters_dir.exists():
        print(f"• Scan: {chapters_dir.relative_to(ROOT)} (no chapters dir yet)")
        return

    # Gather chapter files in numeric order when possible
    files = sorted(chapters_dir.glob("*.md"), key=lambda p: p.name)
    if not files:
        print("  ⚠ No chapter files found in book/chapters.")
        return

    # Build a non-destructive index body
    lines = []
    lines.append("# Chapters -- Working Index")
    lines.append("_Registry Node: Circuitum 99 -- Alpha et Omega / narrative:index / coord: CIDX-0001_")
    lines.append("")
    lines.append("> Proposed by Moonchild (PATCH-only). Paste into chapters_index.md.")
    lines.append("")
    for f in files:
        nice = human_title_from_filename(f.name)
        rel = os.path.relpath(f, REG / "01_main-narrative")  # link relative to narrative folder
        # Link back to the actual chapter file in /book/chapters
        lines.append(f"- [{nice}](../{rel.replace(os.sep,'/')})")

    body = "\n".join(lines)
    # Write the PATCH file; target may or may not exist yet
    patch_content = (
        f"# PATCH for {index_target}\n\n"
        "## Steps\n"
        "- Create or replace the contents of `chapters_index.md` with the snippet below.\n"
        "- This does not alter any chapter files; it only creates an index.\n\n"
        "## Snippet\n```markdown\n" + body + "\n```\n"
    )
    out = write_patch_for(index_target, patch_content)
    print(f"  ↳ Wrote PATCH: {out.relative_to(ROOT)} (chapter index)")
if __name__ == "__main__":
    main()