
<!-- MOONCHILD: FIXED-COORDINATES HEADER -->
ID: MC-ROOT-0001
Name: Moonchild Node
Type: Repair & Reconstruction Daemon
Status: ACTIVE
Static Story Mode: ON
Dynamic Repair Mode: ON
Coordinates:
  - Registry Index: 0.0
  - Source Folder: /core/moonchild
  - Repair Scripts: /scripts/moonchild_repair.md
Permissions:
  - READ from /source_texts/*
  - WRITE to /drafts/*
  - APPEND ONLY to /main_story/*
Lock:
  - Immutable Story Lock: ON
  - Old Text Import Lock: OFF (Manual Approval)
  
  
# CIRCUITUM99 – Registry Guide

This registry is the structured map for the LuxCrux universe.  
Every file belongs in one of these numbered sections:

1. **01_main_narrative** → Story spine & approved chapters.
2. **02_grimoire** → Magical reference library & meta layers.
3. **03_codexes** → Systems, rules, archetypes, and correspondences.
4. **04_registry_meta** → The registry about the registry.
5. **characters** → Profiles, grimoires, and meta layers for each character.

## Storage Rules
- **Real-world material** (manuals, certifications, summaries) → `02_grimoire`  
- **Story content** → `01_main_narrative` or `characters/` if tied to a specific character.
- **Systems & mechanics** → `03_codexes`
- **Meta organisation** → `04_registry_meta`

Keep `_index.md` as the clickable map.  
Update `registry.md` whenever you add a new section or rule.