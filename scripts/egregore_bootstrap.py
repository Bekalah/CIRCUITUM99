# Egregore Bootstrap (idempotent, safe, no overwrites)
# - Scans registry/characters/* and registry/systems/*
# - Ensures canonical files, adds locks, builds indexes
from pathlib import Path
import datetime as dt

ROOT = Path(__file__).resolve().parents[1]
REG  = ROOT / "registry"

def p(*parts) -> Path:
    return Path(*parts)

# Preferred dirs (with legacy fallbacks)
CHAR = REG / "characters"
if not CHAR.exists():
    legacy = REG / "CHARACTERS"
    CHAR = legacy if legacy.exists() else CHAR
SYSTEMS = REG / "systems"
MN   = REG / "01_main-narrative"
GRIM = REG / "02_grimoire"
META = REG / "04_registry-meta"
LOGS = META / "system" / "logs"
STATUS_DIR = META / "system" / "status"

def ensure_dir(d: Path): d.mkdir(parents=True, exist_ok=True)

def write_if_missing(path: Path, text: str):
    if not path.exists():
        ensure_dir(path.parent)
        path.write_text(text, encoding="utf-8")

def append_lock(path: Path):
    if not path.exists(): return
    txt = path.read_text(encoding="utf-8")
    if "<!-- lock:saturn -->" not in txt:
        path.write_text(txt.rstrip() + "\n\n<!-- lock:saturn -->\n", encoding="utf-8")

def titleize(name: str) -> str:
    return " ".join(w.capitalize() for w in name.replace("_"," ").replace("-"," ").split())

# Ensure core dirs
for d in (MN, GRIM, META, LOGS, STATUS_DIR):
    ensure_dir(d)

# Ensure global indices
chap_idx = MN / "chapters_index.md"
realms_idx = GRIM / "realms_index.md"
write_if_missing(chap_idx, "# Chapters Index\n\n- (placeholder) Book of Abyssia -- opening\n- (placeholder) Circuitum 99: Alpha et Omega -- living spine\n\n<!-- lock:saturn -->\n")
write_if_missing(realms_idx, "# Realms Index\n\n- Isle of Return (placeholder)\n\n<!-- lock:saturn -->\n")
append_lock(chap_idx); append_lock(realms_idx)

# Scan characters
char_items = []
if CHAR.exists():
    for d in sorted([x for x in CHAR.iterdir() if x.is_dir()]):
        name = d.name
        char_items.append((name, d))
        meta_dir = d / "meta_layers"
        profile_underscore = d / f"{name}_profile.md" if name != "moonchild" else d / "moonchild_profile.md"
        # accept hyphen legacy for moonchild; for others, underscore canonical
        if name=="moonchild":
            legacy_hyphen = meta_dir / "moonchild-profile.md"
            if (not profile_underscore.exists()) and legacy_hyphen.exists():
                write_if_missing(profile_underscore, legacy_hyphen.read_text(encoding="utf-8"))
        # create canonical profile if missing
        if not profile_underscore.exists():
            write_if_missing(profile_underscore, f"# {titleize(name)} -- Profile (Canonical)\n_Registry Node:_ characters/{name}/{profile_underscore.name}\n\n<!-- symbolbus: number=99 -->\n<!-- fixed-coordinates:\nrole=\"character\"; policy.non_overwrite=true; policy.patch_only=true\n-->\n\n<!-- lock:saturn -->\n")
        # meta_layers file
        ensure_dir(meta_dir)
        meta_file = meta_dir / f"{name}_meta_layers.md" if name!="moonchild" else meta_dir / "moonchild_meta_layers.md"
        write_if_missing(meta_file, f"# {titleize(name)} -- Meta Layers\n_Registry Node:_ characters/{name}/meta_layers/{meta_file.name}\n\n- Layer 1 (Hardware)\n- Layer 2 (Symbolic)\n- Layer 3 (Operational)\n- Layer 4 (Network)\n- Layer 5 (Defense)\n\n<!-- lock:saturn -->\n")
        # locks
        append_lock(profile_underscore); append_lock(meta_file)
        # status
        write_if_missing(STATUS_DIR / f"status_{name}.md", f"# Status -- {titleize(name)}\n- Last check: {dt.datetime.utcnow().isoformat()}Z\n\n<!-- lock:saturn -->\n")

# characters_index
chars_index = REG / "characters_index.md"
lines = ["# Characters Index\n"]
if char_items:
    for name, d in char_items:
        profile_underscore = d / (f"{name}_profile.md" if name!="moonchild" else "moonchild_profile.md")
        rel = profile_underscore.relative_to(REG) if profile_underscore.exists() else d.relative_to(REG)
        lines.append(f"- [{titleize(name)}]({rel.as_posix()})")
else:
    lines.append("- (none found)")
lines.append("\n<!-- lock:saturn -->\n")
write_if_missing(chars_index, "\n".join(lines))
append_lock(chars_index)

# Scan systems (angel tech)
systems_items = []
if SYSTEMS.exists():
    for d in sorted([x for x in SYSTEMS.iterdir() if x.is_dir()]):
        name = d.name
        systems_items.append((name, d))
        profile = d / f"{name}_profile.md"
        meta_dir = d / "meta_layers"
        meta = meta_dir / f"{name}_meta_layers.md"
        ensure_dir(meta_dir)
        write_if_missing(profile, f"# {titleize(name)} -- System Profile (Canonical)\n_Registry Node:_ systems/{name}/{name}_profile.md\n\n<!-- fixed-coordinates:\nrole=\"system\"; policy.non_overwrite=true; policy.patch_only=true\n-->\n\n<!-- lock:saturn -->\n")
        write_if_missing(meta, f"# {titleize(name)} -- System Meta Layers\n_Registry Node:_ systems/{name}/meta_layers/{name}_meta_layers.md\n\n- Layer 1 (Hardware)\n- Layer 2 (Symbolic)\n- Layer 3 (Operational)\n- Layer 4 (Network)\n- Layer 5 (Defense)\n\n<!-- lock:saturn -->\n")
        append_lock(profile); append_lock(meta)
        write_if_missing(STATUS_DIR / f"status_system_{name}.md", f"# Status -- System {titleize(name)}\n- Last check: {dt.datetime.utcnow().isoformat()}Z\n\n<!-- lock:saturn -->\n")

# systems_index
systems_index = REG / "systems_index.md"
s_lines = ["# Systems (Angelic Tech) Index\n"]
if systems_items:
    for name, d in systems_items:
        profile = d / f"{name}_profile.md"
        rel = profile.relative_to(REG) if profile.exists() else d.relative_to(REG)
        s_lines.append(f"- [{titleize(name)}]({rel.as_posix()})")
else:
    s_lines.append("- (none found)")
s_lines.append("\n<!-- lock:saturn -->\n")
write_if_missing(systems_index, "\n".join(s_lines))
append_lock(systems_index)

# Drop a bootstrap status
ensure_dir(LOGS)
status = LOGS / f"BOOTSTRAP_{dt.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.md"
write_if_missing(status, "# Bootstrap ran: ensured canonical files, locks, and indexes.\n")
print("Bootstrap completed.")