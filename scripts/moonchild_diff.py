import re, os, sys, pathlib, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "main/registry/04_registry-meta/system/logs/moonchild"
QUAR = ROOT / "main/registry/04_registry-meta/system/quarantine"
LOGS.mkdir(parents=True, exist_ok=True)
QUAR.mkdir(parents=True, exist_ok=True)

# Targets
GATES = [
    ROOT/"main/registry/01_main-narrative/gate_11.md",
    ROOT/"main/registry/01_main-narrative/gate_22.md",
    ROOT/"main/registry/01_main-narrative/gate_33.md",
]
REALMS_DIR = ROOT/"main/registry/02_grimoire/realms"
CHAR_MC_PROFILE = ROOT/"main/registry/characters/moonchild/moonchild-profile.md"
CHAR_MC_LAYERS  = ROOT/"main/registry/characters/moonchild/meta_layers/moonchild_meta_layers.md"
CHAR_MC_PARADOX = ROOT/"main/registry/characters/moonchild/crowley_paradox.md"

HEADER_RE = re.compile(r'<!--\s*symbolbus:.*-->')
SATURN_RE = re.compile(r'<!--\s*lock:saturn\s*-->')

def load(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def needs_header(txt:str) -> bool:
    return not HEADER_RE.search(txt)

def gate_header(num:int) -> str:
    return f'<!-- symbolbus: numkey={num} | geom=vesica | chrom=silver_yesod | pHour=Moon | gate=true -->'

def default_header() -> str:
    return '<!-- symbolbus: numkey=33 | geom=vesica | chrom=silver_yesod -->'

def ensure_title_block(txt:str, title:str, coord:str) -> str:
    lines = txt.splitlines()
    # Insert H1 + registry line if missing at very top
    h1 = f"# {title}"
    reg = f"_Registry Node: Circuitum 99 -- Alpha et Omega / {coord}_"
    changed = False
    if not lines or not lines[0].startswith("# "):
        lines = [h1, reg, ""] + lines
        changed = True
    elif len(lines) < 2 or "Registry Node:" not in lines[1]:
        lines = [lines[0], reg] + lines[1:]
        changed = True
    return "\n".join(lines), changed

def propose_patch(p: Path, patch_txt: str):
    stamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    out = LOGS / f"PATCH_{p.name}.{stamp}.md"
    out.write_text(patch_txt, encoding="utf-8")

def main():
    # characters: Moonchild
    for p, title, coord in [
        (CHAR_MC_PROFILE, "Moonchild -- Canon Profile (Registry)", "characters:moonchild / coord: MC-PROFILE-0001"),
        (CHAR_MC_LAYERS,  "Moonchild -- Meta Layers (Angelic OS)", "characters:moonchild:meta_layers / coord: MC-LAYERS-0001"),
        (CHAR_MC_PARADOX, "The Crowley Paradox -- Moonchild Registry Notes", "characters:moonchild:paradox / coord: MC-PARADOX-0001"),
    ]:
        if p.exists():
            txt = load(p)
            new, changed = ensure_title_block(txt, title, coord)
            hdr_needed = needs_header(new)
            if changed or hdr_needed:
                patch = []
                if changed:
                    patch.append(">>> INSERT AT TOP (title + registry line)\n" + new.splitlines()[0] + "\n" + new.splitlines()[1] + "\n")
                if hdr_needed:
                    hdr = default_header()
                    patch.append(">>> INSERT AFTER TITLE BLOCK (symbolbus)\n" + hdr + "\n")
                if patch:
                    propose_patch(p, f"# PATCH for {p}\n\n" + "\n\n".join(patch))

    # gates
    for p, num in zip(GATES, [11,22,33]):
        if p.exists():
            txt = load(p)
            new, changed = ensure_title_block(txt, f"Gate {num} -- <Chapter Title>", f"narrative:gate / coord: GATE-{num}")
            hdr_needed = needs_header(new)
            if changed or hdr_needed:
                patch = []
                if changed:
                    patch.append(">>> INSERT AT TOP (title + registry line)\n" + new.splitlines()[0] + "\n" + new.splitlines()[1] + "\n")
                if hdr_needed:
                    patch.append(">>> INSERT AFTER TITLE BLOCK (symbolbus)\n" + gate_header(num) + "\n")
                propose_patch(p, f"# PATCH for {p}\n\n" + "\n\n".join(patch))

    # realms
    if REALMS_DIR.exists():
        for rp in REALMS_DIR.glob("*.md"):
            txt = load(rp)
            changed_any = False
            new, changed = ensure_title_block(txt, f"{rp.stem.replace('_',' ').title()} -- Grimoire Entry",
                                              f"grimoire:realm / coord: REALM-{rp.stem.upper()}")
            hdr_needed = needs_header(new)
            if changed or hdr_needed:
                patch = []
                if changed:
                    patch.append(">>> INSERT AT TOP (title + registry line)\n" + new.splitlines()[0] + "\n" + new.splitlines()[1] + "\n")
                if hdr_needed:
                    patch.append(">>> INSERT AFTER TITLE BLOCK (symbolbus)\n" + default_header() + "\n")
                propose_patch(rp, f"# PATCH for {rp}\n\n" + "\n\n".join(patch))

if __name__ == "__main__":
    main()