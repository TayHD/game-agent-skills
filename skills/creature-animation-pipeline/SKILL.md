---
name: creature-animation-pipeline
description: Author and ship a full bespoke animation set for a creature (dinosaur, beast, large biped or quadruped) with AI agents - biomechanics and mass first, rig profile and joint caps, key frames first, clip order and mirrors, a per-species animation studio for review, blind calibrated critics, the owner's stamp lock with a no-regression champion take, every clip wired, a species speed curve and the feel-bug rules. Use when starting a new species, authoring or fixing creature clips, setting up the review studio, critics or stamps, or deciding whether a creature clip is done.
metadata:
  version: "0.2.0"
  updated: "2026-11-17"
---

# Creature animation pipeline

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `RIG_SOURCES` | Where the source rigs live (read-only; work on copies). |
| `RIG_PROFILE_FORMAT` | The per-species bone map, chains, IK targets, side suffix and mesh names every tool reads. |
| `CLIP_LIST` | The project's standard clip set per species, with its gaits and which clips are L/R pairs. |
| `STAMPS` | The on-disk stamp file per species that the authoring and push tools read, and who may stamp. |
| `REVIEW_SURFACE` | Where the owner watches takes and stamps them (normally the `STUDIO` page). |
| `STUDIO` | The animation studio: its page, its build and publish steps, its shared data store and the sync step that writes the store back to `STAMPS`. |
| `CRITIC_RUBRIC` | The critic prompt, the rubric, the ship-bar exemplar list per clip group and the held-out calibration takes. |
| `CAPS_TABLE` | The per-species caps and gate thresholds (lean, tail, leg joints, leg snap, clearance, contact). |
| `PROBES` | The quick measurement scripts (body motion, feet, head, arms, contact, leg pops) and where their output goes. |
| `QUALITY_REFERENCE` | The kind of shipped reference the owner holds up as the bar (studied for calibration, never copied). |
| `SPEED_TABLE` | Per species: speed and tightest turn radius per gait (shared with `motion-matching-kit-build`). |
| `SPEED_CURVES` | Per species engine data: band edges, hysteresis, acceleration-by-speed curve, stop margin, stand-turn rate. |
| `LAB` | The engine map or session where wired clips are captured on video and measured. |
| `LEAD` | Who reviews workers' takes and decides parked items (a lead agent or a person), below the owner. |

Motion-matching details (bands, acceleration curve, foot lock, stand-turn ownership, selection logs) live in the `motion-matching-kit-build` skill. This skill points there instead of repeating them.

## 1. Biomechanics first (every species, every clip)

- Build a reference set per species from living relatives: large flightless birds for bipedal gait and head stabilisation, large mammals for mass and timing, crocodilians for tail and sprawl. Take the principle, never the surface motion. The result should read as its own animal, not an enlarged bird or a mammal's timing on a reptile's body.
- Respect the skeleton. A large biped's back is a stiff beam. Weight transfer happens at the hips: pelvis yaw, roll, sway and bob over the stance leg, and the stance hip goes down. Counter-motion lives in the shoulder girdle and neck base, the neck and head (holding their line) and the tail (a lagging counterweight).
- Estimate mass first and let it drive spacing, impact, settle and transitions. Never share timing charts between species of different mass. Heavy animals start slowly, stop late, take few long steps with a deep crouch, and never gallop.
- Plan foot contacts before animating: stride length, narrow gauge for bipeds, toe-first contact with the body settling over each planted step.
- Measure body motion with `PROBES` on the reference and on your take: amplitudes as a share of hip height, timing from touchdown. Land within a typical 30 percent of the reference (less for a heavier animal) with the same signs and timing.
- Rules that read as weight on a large biped (each one is a blocker when missing):
  - the front of the body droops a little on every leg lift and recovers;
  - feet hang in the air: toes down and curled in swing, levelling just before a toes-first contact that rolls back onto the ball; the swing knee stays below the hip;
  - the neck is a suspension: the shoulders rise and fall, the neck folds and unfolds, and the head floats with a little residual motion and a slow, smooth fore-aft bob (never a quick thrust, never locked, never floppy); at faster gaits the head may bob more but stays on its side-to-side line;
  - roll and yaw taper up the spine, full at the hips, almost nothing at the head;
  - the arms always move: a small drop after each foot strike, in proportion to the impact, damped, with the forearm a beat behind and the hand trailing the wrist;
  - no leg pops: the knee never locks straight at the reach and then snaps into the swing fold. Solve reach with crouch and stance timing, never by shortening the stride.
- Caps exist only to stop mesh breakage and cartoon exaggeration. A cap must never shrink weight transfer below the reference; that is how whole sets go stiff.
- This is a game: realistic biomechanics first, then push only for readability at play distance (typically 10 to 30 m).

## 2. Species start-up (once, before any clip)

1. Probe the rig (bones, constraints, meshes, frame rate) and write the rig profile in `RIG_PROFILE_FORMAT`. Every tool reads it before a second species animates anything; after any shared-tool change, re-run an earlier species and prove its output is unchanged.
2. Audit the rig with close renders of rest and extremes (appendages, membranes, feathers, claws). Decide rig additions now, with the owner's agreement, and back up the source. Rig changes mid-run force re-authoring.
3. Set joint caps from where the mesh collapses (thin thigh, pinched ankle, limb sucked into the body), per joint, rest-relative, with sign conventions. Check claw and toe signs on a close-up.
4. Get the home pose right first: every one-shot starts and ends there and every chain pose derives from it. Check limb and appendage clearance against the thighs, front and side.
5. Fill `CAPS_TABLE` before authoring (lean per gait, tail lift and yaw per clip kind, head-yaw budget, leg caps by speed, clearance, leg snap), scaled from a finished species by size and mass.
6. Register the species in `STUDIO` and switch on the stamp lock before the first push (section 4).
7. Decide the left/right masters before any side clip.
8. Fill the species' gait speeds in `SPEED_TABLE` and check gait spacing size-for-size against a species that already looks right (section 9).

## 3. The authoring loop (per clip)

1. **Study.** Write the clip's target in your own words: purpose, feel, beats, gameplay constraints, what would read wrong. Before briefing a new clip, check that the set does not already have one that covers it.
2. **Key frames first.** Block the key poses and review stills of the key moments beside the reference, with the gate numbers for those frames, before any inbetweens, polish, full renders, export or push. A wrong pose visible in one still must never cost a full production pass.
3. **Cycle folders.** Each cycle holds take A and take B. From cycle 2, A is the champion (the best take so far, copied unchanged) and B is the one change being tried.
4. **Measure, then render.** Run the relevant `PROBES` (seconds each) on the exact quantity you are changing, then the gates, then the critic. The sheets are too small to judge toes, necks or hands by eye.
5. **Add one tool feature at a time.** New authoring knobs default off, are tested on a scratch take against the real gates, and are measured one by one.
6. **Critic** (section 5), then push the winner to `STUDIO`, never a take that looks worse than the champion.
7. **Read notes in pose terms.** Restate an owner note as which joint goes which way before acting. When a fix fails twice in the same direction, the brief is wrong, not the knob: re-read the owner's words.

## 4. The animation studio (review surface and shared data)

One private review page for every species, never a cloned page per species or per pass. It shows, per species:
- a home view with progress per species, the review count and recent updates;
- a clip grid by group with thumbnails, filters (needs review, stamped, not stamped) and search;
- a review queue, oldest first: each candidate beside the stamped (champion) take on one clock, with Stamp, Ask for changes (with a note) and Skip;
- a clip page: player with views (all, side, front, far side, top), speed and frame step; every take that has a preview; key-frame sheets, contact sheets, motion and head plots; gate and probe numbers; the critic verdict and score; the clip status (wip, candidate, pass, stamped);
- a compare view for any two takes, a library of the animation docs and an updates feed from the change log.
It must play well on a phone: small encoded videos (H.264, a few hundred px wide), keyboard shortcuts on desktop, large buttons on touch.

**Data store.** The page reads build outputs plus a shared store any agent session can read and write:
- `stamps/<species>__<clip>`: take, label, time, by, by-role (owner or a labelled proxy), removed flag, history;
- `reviews/<species>__<clip>__<take>`: verdict (changes or rejected), note, time;
- `notes/<species>__<clip>` and `threads/<species>__<clip>` for the owner's requests and replies.
A newer store stamp wins over the file stamp.

**Pushing a take.** The take passes its gates and critic and has its renders. Register it as a candidate with a label in one fixed format (cycle zero-padded, then take letter, then a short description), the critic verdict and one or two measured facts. Build, encode any new media in one DCC job, then publish only the files whose hash changed, at the exact paths the page fetches, and list the published files to confirm. Add a change-log line. Mirrors are pushed as their own candidates with the same cycle number.

**Version menus.** When a tuning amount needs the owner's choice, push two to four versions as one group, each with a short name and one-line description, and mark your pick with the reason. Stamping one withdraws the rest; roll the choice out as single candidates afterwards.

**Sync at the start of every animation session.** Dump the store, run the sync step: newer stamps are written into `STAMPS` (back up the file first), candidates move to stamped or changes, and an inbox of change requests and notes is written. A change request becomes a new take, pushed as a new candidate. Read threads but answer the owner in the main conversation, not inside the page; never close a thread for the owner.

**Keeping the DCC files in step.** The authoring tool and the push tool read `STAMPS` and refuse a stamped clip ("REFUSED: stamped"); workers check it before every cycle and stop on a refusal. One writer publishes the page; workers push candidates and report. The stamp button for a clip appears only once its gates pass, a calibrated critic gave SHIP (for new clips) and the `LEAD` has looked at the renders.

## 5. Critics

**Blind A/B.** Copy each take's sheets, plots and measurements into `blind/X` and `blind/Y` with a random mapping saved where the critic cannot read it. Launch a fresh critic agent per cycle with one task line: clip, cycle, mode (A/B or SHIP CHECK), one-line spec. The critic reads only the rubric, the ship-bar exemplars for the clip's group (two of them), the clip's target note, the reference sheets for calibration and the blind folders. It never opens the takes, the tools or the mapping, and never edits anything but its report.

**Two bars.** `QUALITY_REFERENCE` sets how alive, weighted and readable top quality is. The owner-stamped exemplars in `CRITIC_RUBRIC` are the ship bar. A take at the exemplars' level is finished; the critic's job is to catch what is broken or clearly below them.

**Rubric and score.** Score the reference and the take 1 to 10 on aliveness, weight and balance, readability at play distance, naturalness, and secondary motion, then give the take's total as a percentage of the reference's. Stamped sets typically land between about 65 and 95 percent, median about 80.

**Severity.** A BLOCKER is visibly broken or clearly below both exemplars: visible slide or penetration, parts passing through each other, pops or one-frame jerks, mesh collapse, a joint bending the wrong way, a seam or home-pose break, an implausible pose, missing weight transfer or decoupling, a wagging head, motionless arms, or (in A/B) a part of the winner worse than the loser's. Everything else is POLISH, at most five lines, logged and never actioned unless the owner asks.

**Guard rails.** The critic never asks for more turn lean, tail, heel lift, knee straightening or leg reach. Fix directions are limited to timing, spacing, overlap, contact, clearance or less amplitude. A taste note both exemplars share is shipped quality.

**Heavy-creature rules** (add to the prompt for large animals): slower, longer, heavier steps (quick, short, busy steps are a blocker; never ask for faster cadence); a front droop on every leg lift; smooth legs with no knee locks or wide knee swings; hanging feet with the swing knee below the hip; the neck suspension and floating head, holding the centerline on walks (a skull that sways or wags its nose with the steps is a blocker); the taper up the spine; arms answering the impact; walks keep double support. Give the critic the probe readouts (cadence, stride, head versus shoulder range, head side-to-side, knee snap), because sheets are too small for these.

**Calibration before trust.** Run the critic in SHIP CHECK mode on held-out takes, answers hidden: it must SHIP the stamped ones and NOT SHIP the regressions the owner flagged. Gates are calibrated the same way: a stamped take is ground truth, so a gate that fails it is too strict and is recalibrated, never the clip. A new gate is calibrated on stamped takes before it can fail anything. For a new species, rebuild the exemplar list from its first stamped take per clip group; until then borrow another species' exemplars for timing and weight only.

**Report format.** Verdict first (SHIP or NOT SHIP, and below, on par or above the exemplars); in A/B the pick and what the loser does better; the rubric table and percentage; numbered blockers, each with view, frames, what is seen and a fix direction inside the guard rails; at most five polish lines; failed gates and whether they actually read wrong on the sheet. Keep it short (typically under 600 words).

**Triage and stopping.**
- Done means gates pass and one calibrated critic says SHIP. Push with status pass, stop authoring, hand it to the owner. No confirm critic.
- NOT SHIP: the next B fixes the blockers only. Polish goes to the backlog.
- Readability notes never buy amplitude past `CAPS_TABLE`. If a fix moves a pose away from natural, stop and keep A.
- Compare every challenger with the best-ever sheet, not the last one; if it is not visibly better, it loses whatever the scores say.
- Budget: typically six cycles to a candidate, then park with the reason; up to three finishing cycles on the listed blockers; past ten, the `LEAD` reviews the sheets and decides whether the clip is fine or the gate or critic is wrong.
- After every round, audit amplitude drift between the first and final take.

## 6. Stamps, champion and no-regression

- **A stamp means complete and locked.** Only the owner stamps (or a proxy the owner has explicitly asked for, labelled as such and removable). Stamping one side of a mirrored pair stamps the partner only when the partner is the current mirror of that master; removing the stamp removes the partner's too. Removing a stamp needs a deliberate second click.
- **Only the owner unstamps.** A defect found on a stamped clip is raised with the owner first. With the owner's OK, either unstamp, fix with one targeted change, re-mirror and push; or, for a minimal defect fix the owner allows, record a fix entry beside the stamp (by, when, what) without changing the stamp.
- **Stamped and passed clips are frozen.** New tools and gates apply to unfinished clips only.
- **Champion.** The current best take is always kept and compared; a challenger replaces it only when it wins blind and looks no less natural. When the owner flags a regression, restore the earlier good take first, then fix minimally.
- **The owner's eye beats the critics.** A take the owner calls good is the champion. Work the owner approved in a tool is final; when an engine check disagrees with the owner's eye, treat it first as a measurement question (reference point, frame, convention) and report it.
- **Close on stamp.** In the same step as recording a stamp, close the work item and log it; leftovers go to a new item.
- **No partial looks.** Never call the owner to look at partial or known-broken work. The owning agent captures a video of every clip or course, the `LEAD` reviews it against the ready bar, and only then is the owner called. A full-movement showcase of a creature runs only once it has no open movement or feature bugs.

## 7. Clip order and mirrors

Order: idle and home; forward gaits, each stamped before its sides; one master side per pair, built from the stamped forward cycle (same duty, contact timing and joint ranges; only curve, bank and look change), the other mirrored; turns (master plus mirror); one-shots from home; chains last, with seam poses shared exactly through a short blend to the neighbour's first frame. Never run open cycles on two clips that share a chain pose.

Mirrors: author only the master; generate the other side with a bone-by-bone flip that self-checks its error; never tune a mirror; regenerate it whenever the master changes; it inherits the master's status. If a clip is not left/right symmetric (alternating head beats), compose the other side from the master's spec with the yaw negated and the phase shifted half a cycle instead. Previews always show both sides of the animal, including a far-side view.

## 8. Caps and gates

- Turn lean follows physics, not readability: small bank at walk (typically under 10 deg), more at run; the turn reads from the top-view curve of the trunk, the tail carried to the outside and the stride. The bank cap is for turn lean only; per-step pelvis roll follows the reference.
- The tail is a counterweight, not a whip: capped lift and yaw per clip kind, at least a few frames from rest to peak, no hooks, an R side never bigger than its L.
- Leg joints capped by speed, rest-relative; free and air clips are still held to the knee cap.
- Leg snap: cap the median leg acceleration, scaled by speed; a relative pop check misses a clip that snaps on every frame.
- Appendage clearance by folding or tucking, never by hiding the limb.
- Contact on the skinned mesh, every frame: penetration, touchdown gap per stance, hover and slide, with height thresholds scaled to the animal's size.
- Gates are absolute, every exemption is listed and reviewed, and the leg caps are recalibrated on the first stamped forward gaits.

## 9. In the engine

- **Every clip gets wired.** A species kit maps every clip to a runtime home, or records why not. Check the kit's clip map against `CLIP_LIST` before approving. Confirm which asset the game actually plays (a kit copy or the art clip) and refresh both when a clip changes.
- **Species speed curve.** Each creature carries its own speed data: gait speeds in `SPEED_TABLE`, and in `SPEED_CURVES` band edges set from its own gaits so normal speeds sit mid-band, and an eased acceleration-by-speed curve built from its own start and transition clips. Never a flat ramp, never values carried over from another species or a linear scale, and speed bands are never merged. Procedure: `motion-matching-kit-build`.
- **Momentum.** A creature changing direction at speed plays its stop for that speed and lets root motion set the slowdown before moving laterally.
- **Foot lock is frozen.** Keep it on; add no new knobs. A foot slide or pop fix must first name its cause in a clip, a database pool or the query.
- **Stand turns on both sides.** Left and right turns in place of every size are covered, handed to the gameplay turn (the movement code that turns the body in place) the same way, and checked on video on both sides.
- **Size scaling.** Distances and tolerances scale with hip height; angles and slide bars stay absolute. Gate slide against a species that looks right, on the same course and session.

## 10. Feel bugs and originality

- **Reproduce first.** The first step of any feel bug is a video in the view the owner reported it from, with the owner's words on what is wrong, and the owner's confirmation that the video shows it, before any tuning.
- **Fix the cause, not the symptom.** Trace the exact moment; measure a pop offline on the take before scoping a fix to particular bones. If it is not clearly improving after one lab round, stop and show the owner; the owner's eye closes a feel bug, not a bar.
- **Original clips only.** References (shipped games, reference footage, sample sets) are studied for calibration: ranges, liveliness and feel. Never trace, retarget, import or describe their poses, key timing or curves, keep reference renders outside the project, and author every clip from your own key poses.

## Done when

The species' `CLIP_LIST` is stamped, every clip is wired and plays in `LAB` on video, its speed data is filled, and the caps, gates, exemplars and lessons it needed are written into the species profile and the lessons log for the next species to copy.
