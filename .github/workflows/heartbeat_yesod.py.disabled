#!/usr/bin/env python3
"""
Moonchild · YESOD Heartbeat
- Fires only when aligned with YESOD (Moon) specs:
  • Monday OR current planetary hour ruler = Moon OR lunar phase at gates (new/quarters/full) ±1 day
  • OR master-number minute pulse (minute in {0, 33})
- Logs a pulse and (lightly) indexes grimoires.
"""

from datetime import datetime, timedelta, timezone
import os, sys, pathlib, re, yaml

# lightweight deps
from astral import LocationInfo
from astral.sun import sun
from astral import moon as astral_moon
import pytz

# ---------- Config ----------
DEFAULT_TZ = os.getenv("TIMEZONE", "America/Chicago")
LAT = float(os.getenv("LOCATION_LAT", "41.8781"))     # Chicago default
LON = float(os.getenv("LOCATION_LON", "-87.6298"))
CITY = LocationInfo(latitude=LAT, longitude=LON, timezone=DEFAULT_TZ)

# repo paths (match your layout)
ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "main/registry/04_registry-meta/registry.md"
LOG_DIR = ROOT / "main/registry/04_registry-meta/system/logs/moonchild"
LOG_FILE = LOG_DIR / "heartbeat.md"
GRIMOIRE_DIR = ROOT / "main/registry/characters/moonchild/meta_layers/grimoires"
GRIMOIRE_INDEX = GRIMOIRE_DIR / "index.yml"

CHAldeAn = ["Saturn","Jupiter","Mars","Sun","Venus","Mercury","Moon"]
DAY_RULER = {
    0:"Sun", 1:"Moon", 2:"Mars", 3:"Mercury", 4:"Jupiter", 5:"Venus", 6:"Saturn"
}  # 0=Mon? Actually Python: Monday=0; map accordingly:
# Correct mapping for Python weekday(): Monday=0 -> Moon, Tue=1 -> Mars, etc.
DAY_RULER = {0:"Moon",1:"Mars",2:"Mercury",3:"Jupiter",4:"Venus",5:"Saturn",6:"Sun"}

def now_tz():
    tz = pytz.timezone(DEFAULT_TZ)
    return datetime.now(tz)

def planetary_hour_ruler(dt):
    """Compute current planetary hour ruler for given dt (YESOD gating)."""
    # sunrise/sunset for this date at location
    s = sun(CITY.observer, date=dt.date(), tzinfo=dt.tzinfo)
    today_sunrise, today_sunset = s["sunrise"], s["sunset"]

    # next day's sunrise for night calculation
    s_next = sun(CITY.observer, date=(dt + timedelta(days=1)).date(), tzinfo=dt.tzinfo)
    next_sunrise = s_next["sunrise"]

    # daylight segment
    if today_sunrise <= dt < today_sunset:
        day_len = (today_sunset - today_sunrise).total_seconds()
        hour_len = day_len / 12.0
        idx = int((dt - today_sunrise).total_seconds() // hour_len)  # 0..11
        day_ruler = DAY_RULER[dt.weekday()]
        start_i = CHAldeAn.index(day_ruler)
        return CHAldeAn[(start_i + idx) % 7]
    # night segment
    else:
        # if after sunset: night until next sunrise
        start = today_sunset if dt >= today_sunset else sun(CITY.observer, date=(dt - timedelta(days=1)).date(), tzinfo=dt.tzinfo)["sunset"]
        end = next_sunrise if dt >= today_sunset else today_sunrise
        night_len = (end - start).total_seconds()
        hour_len = night_len / 12.0
        idx = int((dt - start).total_seconds() // hour_len)  # 0..11
        # sequence continues from last daylight hour
        day_ruler = DAY_RULER[(start.date().weekday())]
        start_i = CHAldeAn.index(day_ruler)
        # Daylight has 12 hours -> add 12 then advance idx
        return CHAldeAn[(start_i + 12 + idx) % 7]

def lunar_gate(dt):
    """Return True if lunar phase near new/quarter/full (±1 day)."""
    # Astral moon.phase returns age in days from new moon (0..29)
    age = int(round(astral_moon.phase(dt)))  # integer days
    gates = {0, 7, 14, 21, 29}
    # allow ±1 tolerance
    for g in gates:
        if abs((age - g)) <= 1:
            return True, age
    return False, age

def master_33_pulse(dt):
    return dt.minute in (0, 33)

def yesod_window(dt):
    reasons = []
    # Monday?
    if dt.weekday() == 0:
        reasons.append("Monday (Lunar day)")
    # Planetary hour?
    ruler = planetary_hour_ruler(dt)
    if ruler == "Moon":
        reasons.append("Planetary hour ruler = Moon")
    # Lunar phase gate?
    lg, age = lunar_gate(dt)
    if lg:
        reasons.append(f"Lunar gate (phase age ≈ {age}d)")
    # Master 33?
    if master_33_pulse(dt):
        reasons.append("Master 33 pulse")
    return (len(reasons) > 0, reasons, ruler)

def ensure_paths():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    GRIMOIRE_DIR.mkdir(parents=True, exist_ok=True)
    if not REGISTRY.exists():
        REGISTRY.parent.mkdir(parents=True, exist_ok=True)
        REGISTRY.write_text("- **Moonchild**\n  - Logs: `main/registry/04_registry-meta/system/logs/moonchild/`\n")

def index_grimoires():
    items = []
    if not GRIMOIRE_DIR.exists():
        return False
    for p in sorted(GRIMOIRE_DIR.glob("*.md")):
        title = None
        try:
            with p.open("r", encoding="utf-8") as fh:
                for line in fh:
                    m = re.match(r"^#\s+(.+)", line.strip())
                    if m:
                        title = m.group(1).strip()
                        break
        except Exception:
            pass
        items.append({"path": str(p.relative_to(ROOT)), "title": title or p.stem})
    # write index if changed
    old = None
    if GRIMOIRE_INDEX.exists():
        old = GRIMOIRE_INDEX.read_text(encoding="utf-8")
    new = yaml.safe_dump({"grimoires": items}, sort_keys=False, allow_unicode=True)
    if old != new:
        GRIMOIRE_INDEX.parent.mkdir(parents=True, exist_ok=True)
        GRIMOIRE_INDEX.write_text(new, encoding="utf-8")
        return True
    return False

def append_heartbeat(dt, reasons, ruler):
    ts = dt.strftime("%Y-%m-%d %H:%M %Z")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"## Pulse {ts}\n")
        fh.write(f"- Planetary hour ruler: **{ruler}**\n")
        for r in reasons:
            fh.write(f"- {r}\n")
        fh.write("\n")

def main():
    ensure_paths()
    dt = now_tz()
    ok, reasons, ruler = yesod_window(dt)
    changed = False

    # always maintain grimoire index (cheap)
    changed |= index_grimoires()

    if ok:
        append_heartbeat(dt, reasons, ruler)
        changed = True

    # Exit code 0 regardless; Action will commit only if files changed
    return 0

if __name__ == "__main__":
    sys.exit(main())