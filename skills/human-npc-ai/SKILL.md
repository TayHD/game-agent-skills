---
name: human-npc-ai
description: Build human NPC AI for a multiplayer Unreal shooter - server-authoritative layers (perception, belief, readable awareness, squads), fair accuracy that ramps with exposure, squads that coordinate audibly, a body that tells the truth, measured targets from a lab map, and bounded cost. Use when designing or changing NPC behaviour, combat fairness, squads or NPC locomotion, or reviewing human AI.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Human NPC AI

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `FEEL_TARGETS` | Measured targets (foot slide, stop settle, turn trigger, time to first shot, hit chance by exposure, detection time, peek cycle). |
| `LAB` | The lab map, its console commands and trace columns. |
| `PROFILES` | NPC profile data assets (reaction time, accuracy curves, voice, role). |
| `ANIM_BUDGET` | The shared client animation budget for all characters. |
| `TEST_PREFIX` | The NPC automation test prefix. |

## Architecture

- **Layers:** perception, then belief (contacts with decay and a best contact), then awareness (unaware, suspicious, alert, combat), then squad (roles and reservations), then selection and presentation.
- **Selection is pure** and runs before the State Tree ticks; one tree state per branch.
- **One presentation channel:** the server fills a replicated intent struct in one place; events are unreliable multicasts; clients only read.
- **Bodies are budgeted** on equal terms with remote players; dedicated servers never animate.
- **Server authority:** every decision, perception, damage and inventory change is on the server. Difficulty changes behaviour and profiles before it changes damage.

## Feel pillars

1. **They are people:** names, voices, jobs, fear, breaking points; they talk, panic, flee and surrender.
2. **Awareness is readable:** each stage has its own posture, head, gait and voice; transitions are never silent or instant; no HUD markers.
3. **Lethal but fair:** the first burst at a newly seen player misses by design; accuracy ramps with exposure time and falls with distance, target speed and suppression; reaction time never below a profile floor; melee has a windup and a dodge window.
4. **Squads think together:** a leader, capped roles, audible orders and callouts that narrate what the squad believes (including wrong guesses), attack tokens for tempo.
5. **The body tells the truth:** feet plant, stops settle, turns step, cover is a posture, hits move the whole body, nothing slides.
6. **Other threats change everything:** NPCs react to dangerous wildlife or other factions in kind.
7. **Bounded cost:** async pathing, cached cover points, think level-of-detail tiers, significance-gated animation.

## Method

1. Write each change against `FEEL_TARGETS`; every report claim is a row: target, measured, pass.
2. Build and try in `LAB` with tagged trace columns; tune `PROFILES`, not code constants.
3. Tests on real entry points (the brain, the character, the world subsystem) under `TEST_PREFIX`; the full NPC suite stays green or each change is explained in one line.
4. Measure fairness on firing courses (first-burst hit chance, hit chance after sustained exposure), detection on stealth courses, locomotion from the pose trace.
5. Before calling it done, watch the camp untouched for a minute, and watch a capture of the fight.

## Rules

- Logic in C++, tuning in data, selection in State Trees, Blueprints for cosmetics.
- A behaviour that cannot be bounded does not ship.
- Never let a client value feed back into a server decision.

## Done when

The change meets the measured targets on lab traces, the suite is green, cost stays within `ANIM_BUDGET`, and a capture shows the behaviour reading clearly.
