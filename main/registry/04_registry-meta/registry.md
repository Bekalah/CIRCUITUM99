# CIRCUITUM99 · Master Registry

This is the canonical index for your living book. It links only to **real files** in your repo and keeps the hierarchy stable.

---

## Safety Order (do not change)
1. **canon/** – read-only (true grimoires)
2. **confirmed/** – approved pages
3. **recovered/** – verbatim pulls from logs
4. **lore/** – in-progress drafts
5. **build/preview/** – generated only

Automation must **never** edit `canon/` or `confirmed/`.

---

## Indices (linked to actual files)

- **Pillar 21 -- Moonchild**  
  `../registry/pillars/pillar_21_moonchild.md`

- **Living Spine (33 stations)**  
  `../registry/spine/living_spine_33.md`

- **Realms Index**  
  `../registry/realms/index.md`

- **Characters Index**  
  `../registry/characters/index.md`

- **Moonchild (character / profile)**  
  `../registry/characters/moonchild/moonchild_profile.md`

> Each linked file should contain **verbatim or confirmed text**. Do not replace with placeholders.

---

## Logs (Moonchild) -- allowed for bots to append

- Heartbeat → `./system/logs/moonchild/heartbeat.md`  
- Activation → `./system/logs/moonchild/activation-log.md`  
- Dream → `./system/logs/moonchild/dream-log.md`  
- System → `./system/logs/moonchild/system-log.md`  
- Grimoire Intake → `./system/logs/moonchild/grimoire-intake.md`

> These paths are **relative to this file** and live inside `04_registry-meta/system/logs/moonchild/`.

---

## Promotion Flow (how recovered text becomes canon)

1) **Recover** text into the correct section file under `../registry/...` (characters, realms, pillars, spine).  
2) **Review** and mark what’s true.  
3) **Promote** by copying the approved passage into `confirmed/` (new file with the same slug).  
4) **Record** the promotion in the activation log.

_Recovered stays as evidence. Confirmed is the version you read publicly._

---

## Quick Path Reference (no guessing)

- **Characters (index):** `../registry/characters/index.md`  
- **Character → Moonchild:** `../registry/characters/moonchild/moonchild_profile.md`  
- **Characters (others):**  
  - Ann Abyss → `../registry/characters/ann_abyss.md`  
  - Bea Betwixted → `../registry/characters/bea_betwixted.md`  
  - Gemini Rivers → `../registry/characters/gemini_rivers.md`  
  - Morticia Moonbeamer → `../registry/characters/morticia_moonbeamer.md`  
  - Zidaryen → `../registry/characters/zidaryen.md`  
  - Virelai Ezra Lux → `../registry/characters/virelai_ezra_lux.md`  
  - Fenrix Thorne → `../registry/characters/fenrix_thorne.md`  
  - Winne Reweave → `../registry/characters/winne_reweave.md`  
  - Rebecca Respawn → `../registry/characters/rebecca_respawn.md`

- **Pillars:** `../registry/pillars/pillar_21_moonchild.md` (add others as recovered)

- **Spine:** `../registry/spine/living_spine_33.md`

- **Realms:** `../registry/realms/index.md`

- **Sigils / art assets (images Moonchild can reference):**  
  `../../art/img/sigils/`  
  (e.g., `../../art/img/sigils/raku_kei_affirmation.png`)

> All paths above are **relative to this registry.md** location (`circuitum99/main/04_registry-meta/`).

---

## Integrity Rules (Pillar 21 · Moonchild)

- **Continuity lock:** Pillar 21 denies false seams and prevents overwrites.  
- **Two-key repair:** Major merges require Moonchild + one guardian signature.  
- **Traceability:** Every promotion has a log entry with file path + commit hash.

---

## What’s next

- Keep filling the linked section files with **your recovered text** (not placeholders).  
- As soon as a section is correct, mirror it into `confirmed/` and log the promotion.  
- If a workflow fails, check that it points exactly at these paths.

---