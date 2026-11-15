---
name: motion-matching-kit-build
description: Build a motion-matching locomotion kit for a character or creature in Unreal (Pose Search) - species speed table, clip coverage blocks, root motion and lead-in rules, foot-contact curves, schema and database build, every clip wired, and measured checks. Use when planning clip coverage for motion matching, authoring or importing its clips, or building and debugging its databases.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Motion-matching kit build

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `SPEED_TABLE` | Per species: speed and tightest turn radius per gait. |
| `CLIP_NAMING` | The clip naming scheme and direction codes. |
| `CURVE_NAMES` | Foot-contact curve names (left and right plant). |
| `KIT_FOLDER` | Where the kit's assets are installed. |
| `LAB` | The lab map or session where selections are logged and measured. |

## Clip rules

- **Root motion required,** on a ground-level root under the pelvis. During travel the root yaw follows the direction of travel; in strafes it follows the facing. Add a ground root to rigs whose top bone is the pelvis before any work.
- **Speeds hold steady:** every steady stretch runs at exactly its gait's `SPEED_TABLE` speed with a constant root velocity.
- **Lead-in and lead-out:** starts end with at least one full cycle; stops begin with one cycle and end with at least a second of settled idle; pivots and transitions have a cycle on each side; loops contain at least two cycles and loop seamlessly.
- **No foot slide;** nothing goes through the ground.
- **Foot-contact curves on every clip,** 1 while planted and 0 in the air.
- **One frame rate per species,** 30 fps or more.
- **Shared gait cycles:** every clip of a gait uses the forward loop's stride length and contact timing.
- **Mirrors** may be authored once, but each side is delivered and checked as its own clip.
- **Direction codes** relative to the starting facing (forward, then 45-degree steps left and right).
- **Priorities:** a minimum set that makes motion matching look right first, then the coverage fill.

## Coverage blocks

1. Idle, single steps (side, back, diagonals) and turns in place (45 to 180 degrees; head leads, chest follows, hips lag, tail counter-swings).
2. One block per gait: loops, starts, stops, pivots, circles (tight at the tightest radius, wide at three times), and gait transitions.
3. Strafes where the character can face away from travel.
Actions (attacks, hurts, deaths) stay outside the database and play on top.

## Building

1. Fill `SPEED_TABLE` before authoring anything; compare each required speed with what the clips can actually reach.
2. Author or import, then validate every clip against the rules above with a script (root velocity, curve presence, cycle counts, frame rate).
3. Build the schema (trajectory and pose channels) and databases per gait or speed band; tag clips so the right database is searched.
4. Wire every clip; a clip in no database is unfinished.
5. In `LAB`, log the selected database and clip per frame before tuning any knob, and read clip advance per second and re-picks before any foot or pose fix.

## Checks

- Planted-foot drift and per-stride slide within the project's bands.
- Stop, start and turn times measured against the design targets.
- Selection logs show the expected database at each speed; a speed band that switches databases explains sudden pivot changes.

## Done when

Every priority-one clip is in, validated and wired, the databases build cleanly, and the lab measurements meet the design targets.
