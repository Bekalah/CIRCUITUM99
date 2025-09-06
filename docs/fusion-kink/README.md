# Fusion-Kink Portable Library

## Install
Drop `/chapels/fusion-kink`, `/assets`, and `/docs/sources` onto any static host. Open `chapels/fusion-kink/library.html` in a browser.

## Add a Grimoire
```json
{ "id":"new_id","title":"Title","author":"Author","type":"pdf","path":"/docs/sources/.../file.pdf","tags":["tag"],"summary":"Short note","rights":"License text","provenance_id":"prov_new" }
```
Append to `assets/data/fusion/grimoires.json` and record provenance in `provenance.json`.

## Add an Artifact
```json
{ "id":"artifact_id","title":"Title","kind":"scroll","fusionist_id":"sophia7","primary_text_id":"new_id","display_hint":"scroll","location":"shelf_1/drawer_1","unlocked":false,"spawn":["explore"],"lore":"Description","provenance_id":"prov_new" }
```
Append to `assets/data/fusion/artifacts.json` and reference a grimoire id.

## Add a Quest
```json
{ "id":"q_new","title":"Quest Title","giver":"Sophia7","requires":["artifact_id"],"steps":[{"id":"step_1","action":"read","text_id":"new_id","hint":"Hint","result":"flag_done"}],"rewards":["mark_new"] }
```
Append to `assets/data/fusion/quests.json`.

## Spawn-All Toggle
Set `localStorage.sophia7_spawn_all = "true"` to reveal all artifacts. Remove to veil again.

## ND-Safe Rules
- No autoplay media
- Respect `prefers-reduced-motion`
- Keyboard reachable buttons and focus outlines
- No strobe or high-contrast flash

## Provenance Duties
- Never claim rights you do not hold
- Always display license strings from `provenance.json` when showing sources
- Provide download links for originals
