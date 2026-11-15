---
name: modular-environment-kit-production
description: Produce a modular environment kit (buildings, fences, structures) from baseline to shipped - one shared core library, closure before beauty, compliance by construction, scan-gated blind critics, generated prefabs, the finish bar, clash and coplanar checks, materials and import. Use when starting or running an environment kit, building prefabs from kit pieces, or reviewing kit pieces.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Modular environment kit production

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `GRID_CONTRACT` | The measured grid, heights, joint and overhang rules every piece obeys. |
| `FINISH_SPEC` | The measured edge, normal, profile, joint and density rules for the finish stage. |
| `CORE_LIBRARY` | The shared pieces every kit reuses before modelling anything. |
| `PIECE_CAP` | The maximum number of new and variant pieces per kit. |
| `CRITIC_TARGET` | The kind of shipped game the critic compares against, named in its prompt. |
| `MATERIAL_BAR` | The material style target for review renders. |
| `IMPORT_PATH` | How pieces and prefabs are imported into the engine. |

## Principles

1. **Closure before beauty.** Freeze the piece list by assembling the baseline into plans first.
2. **Reuse before rework.** Nothing is modelled that `CORE_LIBRARY` or a passed kit already does.
3. **Everything is a cycle folder;** nothing is overwritten.
4. **Evidence over claims:** scans and measurements decide; renders illustrate.
5. **Good is done:** majors and criticals block; minors go to a backlog.
6. **Decide, log, continue:** the lead decides parked items and logs them as kit rules.
7. **No new parts after the freeze;** gaps are solved by layout.
8. **Compliance by construction:** generators emit the contract (chamfers, trims, UV channels, collision margins), so critics judge look, not rules.
9. **Scan-gated critics:** a cycle reaches a critic only after numeric scans are clean (coplanar faces, collision, UV stretch, open ends, n-gons).

## Stages and phases

1. **Kickoff and contract:** measure every baseline export; tag each piece reuse, variant, new or withdraw within `PIECE_CAP`; run a closure test by assembling four plans (a rectangle, an L with both corners, a setback, the kit's signature form); write the kit contract.
2. **Archetype loop,** per family in parallel: fix the top three critic findings with a generic fixer, author every UV channel in the same cycle, verify with scans and a render sheet, then a fresh critic and a blind second critic. Pass on two consecutive clean critics, or by a mechanical or numeric rule. Budget about three cycles; park at five.
3. **Variants** by chained passes with one batched spot-check critic per family.
4. **Assembly and closure:** rebuild the plans from passed pieces; coplanar 0, gaps 0, walk probe clean.
5. **Kit gate:** three prefabs that exercise the kit's main systems; walkthrough at eye height plus an exterior orbit; a fresh critic.
6. **Building set** at small, medium and large scales, with a variety critic across the set.
7. **Finish stage** on every piece against `FINISH_SPEC`, with a section check before critics; triangle budgets are a soft ceiling, and fine detail may be baked to normal maps on a leaner mesh. Keep glass, masked and moving parts lean.
8. **Materials and decay** at `MATERIAL_BAR`, with a rain walkthrough; review renders always use real materials with wear, never untextured renders.
9. **Import** through `IMPORT_PATH`, verify counts, one play check, request the owner's stamp.
10. **Condition set** (damaged variants) and set dressing after the kit ships.

## Checks every reviewer runs

- A full-member interpenetration check on the piece and its layouts (every beam, brace and rail, not only the members a ticket touched), and every member looked at in the close render.
- The critic is told the target by name: would this sit in `CRITIC_TARGET` without reading cheap at 5 m and 50 m?
- A new asset type starts with one calibration piece reviewed by the lead.

## Prefabs after the kit ships

A prompt or a drawn layout becomes a recipe; the assembler builds it from passed pieces only; scans, walkthrough and one critic; fixes are layout changes. No hand-building in the engine and no new pieces for a prefab.

## Done when

The kit is stamped, its pieces pass the scans and finish rules, the building set and gate prefabs are imported, and the completion report lists measurements, critic paths and parked items.
