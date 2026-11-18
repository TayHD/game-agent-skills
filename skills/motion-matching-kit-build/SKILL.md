---
name: motion-matching-kit-build
description: Build and tune a motion-matching locomotion kit for a character or creature in Unreal (Pose Search) - species speed table and acceleration curve, separate databases per speed band with edges set from the species' own gaits, clip coverage blocks, root motion and lead-in rules, starts sampled head-only and ending in stance, foot-contact curves and a frozen foot lock, stand-turn ownership on both sides, pick-hold, selection logs before any knob and a measured readout. Use when planning clip coverage for motion matching, authoring or importing its clips, building its databases, or debugging hitches, kicks, slides or sticky feet in a motion-matched character.
metadata:
  version: "0.2.0"
  updated: "2026-11-17"
---

# Motion-matching kit build

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `SPEED_TABLE` | Per species: speed and tightest turn radius per gait. |
| `SPEED_CURVES` | Per species engine data: band edges, hysteresis, acceleration-by-speed curve, stop margin, stand-turn rate. |
| `CLIP_NAMING` | The clip naming scheme and direction codes. |
| `CURVE_NAMES` | Foot-contact curve names (left and right plant, and skid if used). |
| `KIT_FOLDER` | Where the kit's assets are installed, kept apart from any approved clip set. |
| `LAB` | The lab map or session where selections are logged, courses run and videos captured. |
| `REFERENCE_SPECIES` | A species already on the system that looks right, used as the yardstick on the same course. |

Review, critics and the owner's stamps follow the `creature-animation-pipeline` skill (for creatures) or the project's review process; this skill covers the motion-matching mechanics.

## Clip rules

- **Root motion required,** on a ground-level root at the origin under the pelvis. During travel the root yaw follows travel; in strafes it follows the facing. Add a root to rigs whose top bone is the pelvis, in a kit copy of the rig, never in the approved source.
- **Export the root as identity** in the engine's component space (check the up and forward axes) and import with root lock on; otherwise the search sees no travel or double travel. Compare bone rotations as well as positions after import.
- **Speeds hold steady:** every steady stretch runs at its gait's `SPEED_TABLE` speed with a constant root velocity.
- **Lead-in and lead-out:** starts end with at least one full cycle and **end in stance, never airborne**; stops begin with one cycle and end with at least a second of settled idle; pivots and transitions have a cycle on each side; loops contain at least two cycles and loop seamlessly.
- **No foot slide,** nothing through the ground. Slide is allowed only inside marked skid windows on hard stops and skidding pivots, where the plant curve is 0 and a skid curve is 1, so the foot lock releases.
- **Foot-contact curves on every clip,** from stance rather than strict contact: planted while the foot's lowest point is within a small fraction of hip height of the ground and moving slower than a fraction of the square root of g times hip height, with hysteresis. Idle and walk clips always keep a foot down.
- **One frame rate per species,** 30 fps or more. **Shared gait cycles:** every clip of a gait uses the forward loop's stride length and contact timing.
- **Mirrors** may be authored once, but each side is delivered and checked as its own clip.
- **Direction codes** relative to the starting facing (forward, then 45-degree steps left and right).
- **Converted clips:** an approved in-place cycle becomes a travelling loop by moving the root at gait speed; the pose relative to the root is untouched, so it needs gates, not a new critic.
- **Before briefing a new clip,** check the existing set and installed clips; a "missing" list is a claim to verify. Top speed may simply be the run clip played faster.

## Coverage blocks

1. Idle, single steps (side, back, diagonals) and turns in place (45 to 180 degrees; head leads, chest follows, hips lag, tail counter-swings).
2. One block per gait: loops, starts, stops, sudden stops, pivots, circles (tight at the tightest radius, wide at three times), and gait transitions. Heavy species do their fastest pivots as skidding arcs.
3. Strafes where the character can face away from travel.
Actions (attacks, hurts, deaths) stay outside the databases and play on top.
Priorities: a minimum set that makes motion matching look right first, then the coverage fill.

## Species speed data (before the first engine look)

1. Fill `SPEED_TABLE` before authoring. Check gait spacing size-for-size (Froude number: speed squared over g times hip height) against `REFERENCE_SPECIES`; a jog too close to its run leaves no room between bands.
2. **Band edges from the species' own gaits,** so each normal speed sits mid-band. If a typical turning dip or a jog sits within about 15 percent of an edge, move the edge or the gait speeds (typical threshold; tune per project). Never copy edges or hysteresis from another species or scale them linearly.
3. **Acceleration is an eased curve by speed,** built from that species' own start and transition clips (speed against acceleration across the chain), with a small margin (typically about a quarter) so the capsule can beat a clip slightly. Never a flat ramp, and never the steepest short window of any clip held for the whole ramp: a capsule that outruns its clips gets entered mid-clip and kicks.
4. Stop margins and stand-turn rates come from the species' own clips (stop distance, clip yaw rate), not from another species.
5. Store all of it in `SPEED_CURVES` as data, never as code constants.

## Databases and building

1. **Separate databases per speed band, never merged,** plus separate stand, moving and stop phases (and facing modes if the character strafes). Stops live only in the stop phase; starts live in the stand phase.
2. **Starts also sit in the moving band only where a moving body needs their acceleration, and there they are sampled head-only** (a sampling range that ends before the start's tail), so a moving body is never offered a start's tail.
3. Validate every clip against the rules above with a script (root velocity, curve presence, cycle counts, frame rate, ends in stance, the source tool's QA flags). A flag stops that clip's install and goes to review; the reviewer decides whether to regenerate it. A clip the owner approved is never regenerated on a flag alone: a check that disagrees with the owner's eye is a measurement question first.
4. Build the schema (trajectory and pose channels) and the databases; tag clips so the right database is searched.
5. **Write a pool report per database** at build time: clips by family, entry and exit stance of each, sampling ranges, and the frames the search can enter that turn more than a typical 20 degrees within the trajectory horizon. An empty turn-entry list means moving turns have nothing to match.
6. Wire every clip; a clip in no database is unfinished.

## Runtime rules

- **Pick-hold.** A short hold after each pick with a cost margin and a repeat veto, with explicit, logged override reasons (first pick, clip end, database change). A held pick must never keep a clip far off the travel direction; if it does, the hold is wrong for that case.
- **Stand turns are owned by the gameplay turn** (the movement code that turns the capsule in place). While it runs, stand-turn clips play at the species' stand-turn rate; outside it they are vetoed. The owned list must be symmetric: every size on both sides, so no side's clips play unowned. Check that the turn course is really still (root drift under the still-speed threshold), or turns are never handed over. Rebuild the gameplay turn's curves from the same full list.
- **Foot lock.** Lock the ball of the foot and solve the ankle with IK; engage from the plant curve with a speed gate, release smoothly when the curve falls. The forced release distance scales with body size (hip height relative to a species where it is right). Once it works, freeze it: no new knobs, and any foot ticket must first name a clip, pool or query cause.
- **Momentum.** At speed, a change of direction goes through the stop for that band before lateral movement; never straight from top speed into a strafe.

## Diagnosing (selection logs before any knob)

1. In `LAB`, log per frame the selected database, clip, clip time, pick cost and override reason, and the band. Read clip advance per second and re-picks before any foot or pose fix.
2. **Readout rows** on every course, against `REFERENCE_SPECIES` on the same course: band changes per second, database changes per second, picks per second, pick cost p90, foot jerk p95, planted-foot drift and per-stride slide, lock hold time and gap, the **measured capsule acceleration and jerk** against the clips' own acceleration at the same speeds, and stop, start and turn times against the design targets.
3. Capture video with the camera near the body (a foot crop at 30 fps for any foot comparison); a far contact sheet is for layout only.
4. Typical causes, in order: a band edge under the species' own speed (forced re-picks), a capsule accelerating harder than its clips, a start tail entered mid-run, an unowned or one-sided turn list, then the lock. Change data first, one value per take, two or three fresh launches per side for any parity claim.
5. Keep harness changes free of per-frame overhead; they move what the meters sample.

## Done when

Every priority-one clip is in, validated and wired, the databases build cleanly with a pool report, the species' speed data is filled, and the readout rows meet the design targets and match `REFERENCE_SPECIES` size-for-size, with a near-camera video of every course reviewed before the owner is asked to look.
