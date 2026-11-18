---
name: human-character-animation
description: Build bespoke third-person human character animation for a multiplayer Unreal shooter (NPC bodies and the player's third-person body) - rig and retargeting hygiene, vetting clip drops, locomotion with motion matching, turn-in-place, layered upper body and aim offsets, third-person weapon read, cover, hit reactions and deaths, a review studio, calibrated blind critics with measured checks, owner stamps with a champion take, key frames first and the blending law. Use when authoring, importing, wiring or reviewing human character clips, setting up a human animation review loop, or fixing a human body feel bug.
metadata:
  version: "0.1.0"
  updated: "2026-11-17"
---

# Human character animation

The body is the part of a human character the player reads first. This skill covers the clips, the layers that play them and the review loop that decides when a clip is done. Behaviour (perception, squads, fairness) belongs to `human-npc-ai`; first-person hold poses and weapon actions belong to `first-person-weapon-animation`; motion-matching coverage and databases belong to `motion-matching-kit-build`.

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `HUMAN_RIG` | The canonical skeleton, its bone names (pelvis, spine chain, weapon IK bone, foot and hand IK bones), the authoring rig in the DCC and the retargeters to it. |
| `CLIP_REGISTRY` | The data file listing every animation state, its candidate sources, kind, loop flag and measured results; the source of truth for what plays. |
| `CLIP_LIST` | The standard human clip set per class (unarmed, rifle, pistol, shotgun) and stance. |
| `STUDIO` | The review page per character or clip set, its shared data store and how takes are pushed to it. |
| `CRITIC_RUBRIC` | The critic prompt, the verdict words, the guard rails and the calibration set. |
| `STAMPS` | Where stamps live, who may stamp and unstamp, and how a stamp reaches the agents. |
| `FEEL_TARGETS` | The measured bands: foot slide, stop settle, turn trigger, max joint change, contact gaps, transition smoothness. |
| `LAB` | The lab map, its courses, console commands and trace columns. |
| `CAPTURE_LIST` | The fixed set of in-engine captures every delivery produces. |
| `QUALITY_REFERENCE` | The kind of shipped work the owner holds up as the bar (studied, never copied). |
| `REPLY_CHANNEL` | Where agents answer the owner's notes (usually the main chat, not the studio's threads). |

## Rig and retargeting

1. **Same rig or retarget, never a skeleton swap.** A clip is usable as-is only when every bone exists on `HUMAN_RIG` with the same parent and a reference rotation within about a degree. Anything else goes through a retargeter into an owned copy.
2. **Derive IK bones from FK after every retarget.** Batch retargets often move the chains only and leave the foot, hand and weapon IK bones at the reference pose. Leg IK then solves to those stale targets and the legs freeze. Rebuild the IK tracks from the FK bones on every import pass.
3. **A loop that drifts by a fixed percentage of its root travel** means two parts of the retargeter use different scales (for example IK goals pinned to unscaled source feet while the root chain is scaled). Measure first-to-last feet and hands in root space on the source and on the result, and trial one retargeter op at a time.
4. **Lock the root explicitly on a capsule-driven body.** Many engines lock a sequence's root only when the clip itself asks for it. Without the flag, the mesh walks off the capsule by the clip's travel in pivots and turning starts. A trace column for root offset from the capsule catches this at once.
5. **Evaluate the clip on the game path before tuning mechanics.** Read the pose as the game plays it (compressed, through the live graph) and log a frozen-legs share per clip. A slide number is only as real as the pose behind it.
6. **Read compiled values, not editor graph values.** A generated node can compile from its pin default while the editor shows something else. Read the node at run time before trusting a setting, and walk upstream from the consumer node, not from the producer.

## Clip sources and vetting a drop

- **Originals only.** New clips are authored fresh. Reference clips, packs and shipped work are studied for timing, spacing and contact, never traced, re-fitted or used as the base of a new clip.
- **Unpack outside the project.** Extract each archive into its own new empty folder, never run anything from inside it, and remove any shortcut or link files that came with it.
- **Vendor folders stay read-only.** The import pass saves only owned copies under the project's own folder, hashes every chosen source before and after, and fails if a source changed.
- **Measure, do not infer.** For every candidate record length, loop flag, additive flag, root travel and yaw, loop seam (feet and hands within about 2 cm, typical) and a key-frame still. Anything taken from a file name is marked "inferred" until measured.
- **Choose per state.** Starts, stops and pivots take the first candidate whose root really moves (typical threshold 5 cm or 5 degrees); everything else takes the first usable one. A state with no good candidate is flagged needs-authoring in `CLIP_REGISTRY`, never silently filled.
- **Normalise every copy:** strip vendor notifies, add left and right sync markers at each foot plant on cycles, pad stops with about 15 to 20 frames of the held end pose (typical), and keep root-motion and in-place pairs both when the ship path and motion matching each need one.
- **Generated clips are vetted like any other clip:** the same measurements, then the full studio loop with critics and a stamp. A learned runtime controller produces no clip to vet, so it stays a lab experiment until it can be captured and measured.
- **Fill gaps in this order:** mirror an existing clip; compose it from existing clips (an upper-body overlay or a graph sequence); acquire one; author one. Authoring is last, and it runs through the full studio loop below.

## The body

### Locomotion
- One native, thread-safe locomotion core (idle, start, cycle, stop, pivot, turn-in-place) that NPCs and the player's third-person body share. Graphs only read bound values.
- Starts and stops are distance matched to the capsule's own prediction, with the play rate clamped (typically 0.8 to 1.2). Brake at a constant deceleration so the predicted stop point is exact.
- Pick the stop clip by phase: the stop starts with the foot about to plant, read from the clip's measured foot timeline rather than its name.
- Cycles use direction by speed blend spaces with each sample at its measured speed, cadence-synced by markers; orientation warping covers the remaining angle and stride warping the remaining speed.
- Crouch, aim and hurt are dimensions of the cycle, not extra states.
- Foot placement then leg IK run after the chain. Prefer a leg IK that keeps the incoming bend plane; a pole-vector solver re-aims every knee each frame.
- Motion matching for near, significant bodies follows `motion-matching-kit-build`. The ship path must stand on its own first.

### Stances
- Stance (stand, crouch, prone) is a dimension of the body, not a separate graph.
- Every stance change is a blend with a stated time, and the upper body follows with its own stated time.
- Each stance needs its own hold pose. A standing hold layered from the lower spine onto a crouched or prone body stands the torso upright, so gate a stance off until its pose exists.

### Turn-in-place and facing
- An idle body holds its yaw while the aim offset covers the difference. Past a threshold (typically 60 to 70 degrees) it commits one stepped turn: the head leads, the chest follows, the hips lag and the feet step. It never spins on the spot.
- A body moving with aim faces the aim and plays strafes; a body moving without aim faces travel.
- Rotate the capsule before the mesh evaluates, or world-locked feet lag a frame and slide on every turn.

### Layered upper body and aim
- Layer the upper body from the lower spine over the cached locomotion pose.
- Readiness is a value, not a state machine: low, ready, aimed, with a stated time for each segment.
- Build the aim offset from additive samples against a reference pose. Measure each sample's real weapon yaw and pitch and place it at those coordinates; authored grids are often wrong.
- Fire and reload play on an upper-body slot, and the additive aim offset is applied on top of that slot's output, so the montages keep the aim.
- Sprint lowers the carry and fades the aim layer with stated blend times, and both return when the stop clip starts, not when the body comes to rest.
- Lean terms (acceleration, turn) go through a damped spring and are split down the spine chain.

### Third-person weapon read
- Hold poses are authored per `first-person-weapon-animation` on the weapon IK bone. The NPC and the player's third-person body use the same hold for the same weapon.
- One gameplay truth, two presentations. Which weapon, where it points, its state and the body's exposure are identical in every view. Third person may add a read offset, a shoulder mount with cheek weld for aiming, and a carry that reads at typical engagement distances (5 to 50 m). It never moves the gun in the hand.
- Derive the weapon attach and the support-hand target from the hold pose. A grip socket is a palm point, so the wrist sits a few centimetres off it.
- Check every weapon in a third-person orbit and a first-person/third-person side by side. A single frozen pose for every weapon, or arms broken behind the camera, are rejects.

### Cover
- Cover is a posture and a movement mode, not a crouch beside a wall. Required states: stand and crouch idles, cover walk with starts and stops, approach at jog and sprint landing in the idle, side swap, corner lean and peek, over-the-top pop-up, blind fire (corner and over the top), exit to open, and cover-to-cover.
- A peek exposes for a measured time (typically 0.5 to 0.9 s) without a sideways step.
- Pick approach clips by the foot phase at arrival. Verify the side convention (left or right of the character) by measuring, not by the suffix.

### Hits and deaths
- Hit reactions come from a set indexed by zone, direction and weight, chosen by damage and stagger resistance. Light hits are additive; a stagger is full body and interrupts aim and movement.
- On the player's own third-person body, hit reactions are visual only and never move the aim or slow the player.
- Knockdown and get-up by direction. Deaths play to a hit frame and then blend into ragdoll, carrying the clip's velocity, with a straight-ragdoll fallback near walls and ledges. Deaths must read directionally.
- Hit, death, melee, grenade and reload stay authored clips played as montages with server-timed starts. Learned or generated locomotion controllers are research only for these.

## The studio (review surface)

Set up one `STUDIO` page per character or clip set before the first take is pushed.
- **Review queue:** every candidate awaiting a stamp, oldest first, with the stamped take or champion beside it, playing on one clock.
- **Clip page:** a player with fixed views (side, front, top, far side, and the in-game camera), speed control, frame step, every earlier take, any two takes side by side, and the measurements.
- **Sheets:** a key-frame sheet (contact, passing, extremes) and a contact sheet (every few frames) beside the reference, plus the probe readouts.
- **Captures:** short video of the clip in the engine from `CAPTURE_LIST`: the lab course, the third-person orbit and the reported view.
- **Status per clip:** not started, in work, candidate, changes asked, stamped, wired.
- **Owner actions:** stamp, ask for changes with a note, skip. A version menu lets the agent offer two to four labelled versions of one tuning choice with its pick marked; stamping one withdraws the rest.
- **Shared data store:** stamps, change requests and notes live in the page's store so any session can read them. The build regenerates the page from files; the store is never edited by hand.
- **Phone-viewable:** single column, short H.264 clips (typically around 860 px wide), large previews, and the stamp button reachable by thumb.
- **Every session starts by syncing:** read the store, write new stamps to the on-disk record, turn change requests into an inbox, and answer them in `REPLY_CHANNEL`. Never close the owner's thread for them.

## The critic process

- **Blind.** From the second take on, a critic sees two takes labelled at random: the champion and the challenger. It never knows which is new. The first take is judged alone against the exemplars.
- **Rubric from `CRITIC_RUBRIC`.** The owner's rules are given verbatim, together with two stamped exemplars from the same clip group and the probe readouts. Stills are too small to judge on their own.
- **Verdict:** SHIP or NOT SHIP.
  - A blocker is visibly broken or clearly below the exemplars: clipping, foot slide, pops, mesh collapse, a joint bending the wrong way, a seam break, hands off the weapon, an implausible pose, or a regression against the other take.
  - Everything else is polish. It is logged and never earns a cycle unless the owner asks for it.
- **Guard rails:** the critic may never ask for more amplitude (lean, bob, arm swing, stride). Fixes are limited to timing, spacing, overlap, contact, clearance or less amplitude.
- **Calibrate before trusting.** Run the critic on held-out takes. It must SHIP the owner-stamped ones and NOT SHIP the regressions the owner flagged. Recalibrate whenever the stamped set grows in a new clip group.

### Measured checks (gates)
| Check | How to measure it |
|---|---|
| Foot slide | Planted-foot world drift at the sole or ball (not a toe tip that swings as the foot rolls), per stance, from the lab trace. Skip samples where the pose did not refresh. Typical band: 2 cm or less in stops and turns. |
| Jerk and pops | Per-joint angular speed in the body frame (so the body's own turn is not counted), as a rate per second that does not depend on frame rate. Typical: flag samples above about 600 degrees per second outside hits and deaths. Also check frame-to-frame deltas across every transition. |
| Joint limits | Per-joint caps set from where the skinned mesh collapses, relative to rest, with stated sign conventions. Never set them from taste. |
| Hand contact on the weapon | Evaluated skinned hand against the weapon mesh on every frame, with a signed gap. Calibrate the band on a stamped grip, since a good grip overlaps slightly. |
| Silhouette at distance | Render downscaled to the size the body appears at a typical 30 to 50 m. A blind reader must name the stance, weapon state and facing. |

- Gates are absolute. Every exemption is listed and reviewed.
- A new gate is calibrated on stamped takes before it can fail anything. If a gate fails a stamped take, suspect the gate first: its reference point, frame and convention.

### Triage and stopping rules
- **Read notes in pose terms** (which joint goes which way) and restate an ambiguous note before acting.
- **Good is done.** A take is done when the gates pass and one calibrated critic says SHIP. Then stop authoring it and push it for the owner's stamp.
- **Budget:** typically 6 cycles to a candidate, then park the clip with the reason. A parked near-pass gets up to 3 cycles that fix only the listed blockers. Past about 10 cycles, the lead looks at the sheets and decides whether the clip, the gate or the critic is wrong.
- **When a fix fails twice in the same direction,** the brief is probably wrong, not the value. Re-read the owner's words.

## Stamping

- **A stamp locks the clip.** The authoring tools refuse stamped clips, and a stamp means done.
- **Only the owner unstamps.** A defect found on a stamped clip is raised with the owner first. With an OK, fix it with one targeted change, compare it visually, and record the fix next to the stamp rather than replacing it.
- **Champion take and no regression.** The best take so far is always kept unchanged. A challenger replaces it only when it wins blind and looks no less natural on the sheet. It never wins on critic notes alone. When the owner flags a regression, restore the champion first, then fix minimally.
- **The owner's eye beats the critics.** If the owner says a take looks good, it is the champion. If a check disagrees with a stamped take, suspect the measurement.
- **Mirrors inherit status.** Stamping one side of a mirrored pair stamps the other only while the mirror was built from the stamped master.
- **No partial looks.** Nothing partial or known-broken reaches the owner. The lead first watches a capture of every course against the ready bar (no visible pops, feet planted, correct facing, server path).
- **Close on stamp.** Mark the work done when the stamp is logged. Anything left over becomes a follow-up item; nothing stays "kept open".

## Techniques

- **Key frames first.** Block the key poses and show them as stills beside the reference, with the gate lines for those frames, before inbetweens, polish, export or encode. One still catches what a full production pass would waste a round on.
- **The blending law.** Nothing starts, stops or switches on a frame. Every state change, layer weight, procedural target and camera value states its interpolation (crossfade, spring or curve) and its time or half-life. Blends overlap; the next motion begins before the last one ends. Every animation change carries a transition-smoothness check in its acceptance (a measured band, or stills across the switch). A working but rough transition is a reject.
- **Every clip is wired.** Each clip in `CLIP_LIST` has a runtime home, or the registry records why not. An unwired clip is unfinished work; audit the map before calling a set done.
- **Reproduce a feel bug first.** Capture a video in the exact view the player reported, and have the owner confirm that the video shows the fault, in their words, before any tuning starts. Then trace that exact moment before designing a fix. If nothing visibly improves after one lab round, stop and show the owner. The owner's eye closes a feel bug, not a passing bar.
- **Decompose before tuning.** Under a root lock a planted foot moves by the capsule's step minus the clip's root step, so split a slide that way, per clip and per foot phase. Align separate traces on a shared column before reading a window. Read the diff before bisecting.
- **Gated landing.** Clip imports, graph installs and code land through the staged, gated run in `staged-change-landing-hold`: back up first, smoke first, run only the gates the change owns, and capture `CAPTURE_LIST`.
- **Study the bar, never copy it.** Keep notes on how shipped work in `QUALITY_REFERENCE` achieves its feel, written as measurable targets.

## Done when

Every state in `CLIP_REGISTRY` resolves to an owned, measured clip or a recorded gap. Every clip is wired. The locomotion, transition and contact rows of `FEEL_TARGETS` pass on `LAB` traces. `CAPTURE_LIST` shows nothing sliding, popping or breaking. The owner has stamped the set in `STUDIO`.
