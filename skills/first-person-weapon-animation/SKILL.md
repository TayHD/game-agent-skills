---
name: first-person-weapon-animation
description: Build bespoke first-person and third-person weapon animation for an Unreal shooter - gun-space rig, measured hold poses, gun-first action authoring with key frames first, reload anatomy, modular weapon families with per-weapon profiles, procedural layers with stated interpolation, export and install with round-trip checks, a per-weapon review surface, calibrated blind critics, owner stamps and a no-regression champion take. Use when authoring hold poses, reloads or other weapon actions, installing weapon animation, tuning or debugging first-person feel, or reviewing weapon animation.
metadata:
  version: "0.2.0"
  updated: "2026-11-17"
---

# First-person weapon animation

The weapon carries every action. The body, hands, camera and sound follow it, and one gameplay truth serves both views: first person is how the owner sees their own body, third person is how everyone else sees it.

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `DCC_RIG` | The character rig file used for weapon authoring and its gun bone. |
| `WEAPON_SOCKETS` | The socket names every weapon carries (sight, muzzle, support grip, magazine, stock, magazine-in-hand). |
| `HOLD_CHECKS` | The pose checker and its bands (hold, neck, elbows, hand contact, finger anatomy). |
| `EXPORTER`, `INSTALLER` | The export and import scripts and their deliberate flags. |
| `FEEL_STANDARD` | The measured feel targets and pass bands, with the trace format the measuring tool reads. |
| `CAPTURE_LIST` | The fixed set of in-engine captures every delivery produces. |
| `WEAPON_LIBRARY` | The source weapon parts library (read-only) and the working copy where family rigs are built. |
| `REVIEW_SURFACE` | The per-weapon review page the owner uses, and its shared data store. |
| `STAMPS` | Where stamps are recorded, who may stamp and unstamp, and where the owner's key files live. |
| `CHAMPION` | The current best take of each clip and the approved live weapon feel that new work is measured against. |
| `CRITIC_RUBRIC` | The blind-critic prompt, rubric, verdict format and the calibration set of owner-approved takes. |
| `FOLEY_NOTIFIES` | The notify names used as sound and camera hooks, and the sound library they map to (read-only). |
| `QUALITY_REFERENCE` | The kind of shipped reference the owner holds up as the bar (studied for numbers, never copied). |

## Pipeline

1. **Weapon mesh:** re-pivot it and write the sockets; moving parts (bolt, magazine, catch, dust cover) stay as bones. Put the support grip socket mid-handguard, not at the back.
2. **Hold pose** on `DCC_RIG`: shouldered ready, passing `HOLD_CHECKS`. Typical bands: stock within about 3 cm of the shoulder pocket, bore level or at most about 5 degrees down, the sight a measured distance below and right of the eye (typically 12 to 20 cm below, 6 to 14 cm right; framing comes from a camera offset, never from bending the pose), head upright, palms on their grip targets, neck joints under about 15 degrees of twist and bend each, support elbow outside and below the handguard. Review it in an eye camera with the first-person framing preview on and in a third-person three-quarter camera with the full body on.
3. **Actions, gun first:** see "Action authoring order" below.
4. **Export** with a round-trip check (sub-millimetre) and a hold pose exported as two identical frames (a one-frame file imports as the reference pose). The exporter refuses frames taken with the framing preview on.
5. **Install** in steps: reimport is the default; tuning writes, graph rebuilds and installs are separate, deliberate flags. Imports keep the exported normals and tangents. The importer backs up every asset it saves, not only the clips.
6. **Profile:** the per-weapon profile holds zero transforms; tuning lives in the weapon class asset.
7. **Verify** with `CAPTURE_LIST` (first person hip, aim, walk, sprint; third person hip, aim, sprint; an orbit behind the first-person body; side views), the rig tests, and a feel readout.

## Action authoring order

1. **Measure the reference first.** Before any hand work, measure the absolute grip in the item's own frame from a reference (palm point, knuckle direction, palm normal, per-joint flexion, thumb) and the timing of each phase. Transfer hand poses between rigs by gun-space geometry, never by copying local bone rotations: bone rolls and hand sizes differ.
2. **Key frames first.** Block only the key moments (for a reload: hold, release, strip, carry down, carry up, insert, seat, bolt, return) and render them as same-camera stills beside the reference, with the gate lines for those frames. A reviewer looks within minutes. Only after an OK does the full production pass run (every-frame gates, export, flipbooks, encodes, review push). A bad pose visible in one still must never cost a full production pass.
3. **Gun path first.** Settle the weapon's path, poses and timing on the gun bone (blockout, key poses, in-betweens, timing pass, detail actions) before the hands exist.
4. **Hands follow.** Hands go to their grip targets on the gun and its parts. Carry a keyed grip by holding the hand rigid in the item's frame (hand = item path times the keyed hand-in-item offset) instead of re-solving fingers every frame; the pads stay where they were keyed and the contact gate passes by construction.
5. **Secondary motion and polish last** (physics pass, overshoots, finger settles), so a timing change never means re-keying the hands.
6. **Owner keys are locked.** Where the owner keys critical poses (the hold grip, reload start, magazine grip, each foregrip's support hand), agents fill everything around them: timing, gun motion, in-betweens, the pistol-grip hand, contact on non-key frames. Never re-pose a locked key; a gate failure on one is reported to the owner with a still. Read the owner's key file from a copy, check every key for shared channels that disagree (a finger changed in one key but not the next drags through the trigger), and carry a changed grip as a local offset on every frame where the hand holds it, eased over several evenly spaced frames.
7. **Gate hands on the evaluated skinned mesh,** never on joint capsules: typical touch within 0.3 cm for palm and wrapping fingers, penetration at most 0.5 cm for palm and proximal phalanges and about 1 cm for pads, hollow parts also judged against their outer envelope. Gate finger anatomy too (per-joint flexion, abduction and twist ranges, no crossed fingertips): a grip can pass contact and still look broken.
8. **Handling clips from one source.** Draw, holster and inspect start from frame 0 of the approved reload's hold so every clip shares one hold exactly; bake every channel per frame from monotone curves so nothing overshoots between keys.

## Reload anatomy

Inside the stamped phase lengths (rate 1, never time-stretched, so seat, hide and ammo-commit times do not move). The numbers are typical starting values at 30 fps:

1. **Stick, then breakaway.** After the hand grips the magazine, 2 to 3 frames of stick: the wrist and forearm tense 0.3 to 0.5 cm while the magazine stays seated. Then it breaks free in 1 to 2 frames at high speed and eases out.
2. **Counter-force on the gun.** At the breakaway the gun kicks typically 0.4 to 0.8 cm up and 1 to 2 degrees toward the support side and settles over about 4 frames; the gun hand rides it. Mirror it on the seat: the gun dips 0.5 to 1 cm at the impact and settles.
3. **Imperfection.** Every hand arrival (magazine grip, well entry, bolt slap) overshoots 0.2 to 0.4 cm along the arrival direction, never into the part, and settles in 1 to 2 frames. One small thumb pressure shift before the insert. Nothing linear-smooth.
4. **Magazine swap.** Hide the gun's magazine bone near the body and show a hand-attached magazine until the seat. The hand holds it rigid from hide to seat (typical drift at most 0.5 cm and 3 degrees). A constant scale key arrives in the engine as a one-frame ramp, so place the hide notify one frame before the scale-zero key and the seat notify on the scale-one key. Check sockets on the visible frames either side of the hidden window, because a zero-scaled bone's rotation is undefined after import.
5. **Empty and tactical variants** share the carry and differ at the bolt. A heavier magazine (drum) adds a few frames to carry and insert and a push-seat; it never stretches the standard clip.
6. **Gameplay time follows the clip:** the ammo commit sits at clip length minus blend-out. The weapon's own clip (bolt, magazine) is clocked from the body montage position every frame, never started alongside it, or it drifts on remote copies and the magazine doubles or vanishes.
7. **Prove visibility from frames.** A check that the in-hand magazine exists does not prove the player sees it; look at the first-person frames between hide and seat.

## Modular weapon library and per-weapon profiles

- One skeletal **family rig** per weapon family carries the moving parts; static parts (optics, foregrips, muzzles, magazines) attach through a socket chain. Socket frames are gun axes (X along the bore, Z up).
- **Find the family root, don't assume it:** grid-search it with an approved gun hand on the new pistol grip and trigger until the grip gate passes.
- **Re-fit an approved set to a new family by transferring parts as frames:** carry the magazine as its frame, and the hand rigid on it moves with it.
- **A same-class part is not the same shape.** Gate the key magazine grip on every new magazine part; a curved front can sink a finger that cleared the last one.
- **Each grip attachment supplies its support socket plus a support-hand pose** from a small set (handguard, vertical, angled, rail). A grip changes the support wrist, not just the fingers; one gun-space pose per grip serves hip and aim.
- Default loadouts are bare (the weapon, its standard muzzle device and magazine, its iron sights); attachments are separate parts.
- The source library is read-only: copy into the working area, import only what is scheduled, and use generic in-game names.
- Per-weapon profiles keep zero transforms; per-weapon feel tuning lives in data, as live knobs during exploration and as class data once landed.

## Procedural layers

Every layer states its interpolation. Use the closed-form critically damped spring set by a half-life (frame-rate independent, one knob), or an under-damped spring where overshoot is designed. Never a per-frame lerp. Typical starting points:

| Layer | Interpolation | Typical start |
|---|---|---|
| Look sway (gun trails the head) | critically damped spring | half-life about 0.10 s, a few degrees cap, aim scale about 0.3 |
| Aim in and out | spring plus a short roll settle | half-life about 0.07 s (95% near 0.24 s), settle gone by 0.25 s |
| Walk bob on the gun | phase from the camera rig's bob clock, run from speed and stride (see the bob clock lesson) | about 1 cm translation, rotation carries the weight; run and sprint scale from walk, sprint widens sideways |
| Recoil kick | translation and rotation springs | peak within one frame, 90% recovered by about 0.2 s and 0.33 s; the rifle twists, it does not climb |
| Movement inertia (horizontal only) | spring on acceleration | about 1 cm per 1000 cm/s squared, capped near 2 cm and 3 degrees |
| Stance and sprint poses | spring plus an under-damped entry settle | in about 0.2 s, out about 0.15 s |
| Air and landing | curve plus settle, scaled by impact speed | compression peak near 0.13 s, no bounce |
| Cosmetic camera kick or reload sway | rendered view only, short and recovering | settled by about 0.3 s; gameplay aim never moves |

- Measure feel gun-versus-camera on the rendered view, at a fixed timestep, over steady windows of 3 s or more (per stride and whole loop); typical pass bands are amplitude 25%, timing 20%, frequency 10%, signs matching, with hard ceilings.
- One first-person camera rig, rigid to the view, owns the camera in every on-foot state: stance eye height, a rigid pitch pivot, analytic lean, the designed bob (its clock lives here) and the landing curve, with only a small clamped residual from the animated head. The hip gun rotation locks to this rig and the visible body follows the camera. Only in climb, mantle and vault does the camera ride the animated head, so looking down never shows the inside of the body.
- Design bob rotations in camera axes, so channel ratios hold in any pose. The view stays nearly still; most bob and sway live on the gun.
- Anything clocked on a gameplay montage reads the montage position plus the current frame's advance, or it lands a frame late.
- Test every procedural pose that moves the gun for hand-to-goal gaps over its whole curve, not just at its end. The elbow pole follows the gun.
- Numbers borrowed from a camera-attached reference carry a flag: target, ceiling only, or not transferable. Viewmodel camera motion, step rate and framing distances are never targets for a true first-person body.

## The bob clock lesson

Symptom: a first-person speed spike ("fast-forward") for a second or two on walk-to-run and run-to-walk transitions. Cause: the camera rig's bob clock re-timed instantly. It took its period from the interval between foot events, so one short interval made the bob race at up to about 2.4 times the right rate after the speed had already settled. Third-person checks all passed, because that clock only drives the first-person view.

- Run the clock at a nominal rate (about pi times speed over a nominal stride) and smooth it; never retime it on an event.
- A foot plant may only nudge the phase: a correction capped at a small band of nominal (typically 10 to 15%), applied as a smooth bump that is zero at both ends, sized to close the error over about a stride.
- Check it on every frame of the first-person stream through walk, run and sprint, up and down with no reset: bob rate over nominal stays inside the band, no rate steps, amplitude unchanged. Keep the old clock behind a switch so one build gives both takes on the same inputs.
- Check first person separately from third person. A bug may exist in only one view; ask which view first.

## Feel bugs: reproduce before tuning

1. Get a video in the view the owner reported, and the owner's own words on what is wrong at which moment.
2. Trace that exact channel at that moment, frame by frame, before designing any fix. Get the owner to confirm the reproduction is the fault.
3. Then tune. If it is not obviously better after one test session, stop and show the owner. Passing metrics do not close a feel bug; the owner's eye does.
4. Re-read any bar taken from a trace whenever the trace's clock precision changes.

## Foley sync points

- Place notifies at exact frames as both sound and camera hooks: magazine release click, breakaway, scrape, seat impact, bolt release, and a gun kick with a strength value on breakaway and seat. Ship them in a per-clip notify file that the installer places unchanged.
- In game, a one-shot visual camera impulse on heavy pulls and slaps sits on top of the authored motion, first-person owner only, aim untouched.
- Sound in game must match what the review surface shows. Read sound timing from a run that saves no image files: saving frames slows the game and shifts the log by a frame.
- The sound library is read-only; copy what is imported.

## Third-person sync

- The same body montage serves both views at rate 1, on the same clock and the same fire counter. First-person-only framing presets (sprint, low ready, reload lift) move only the owner's rendered view, never the capsule, the third-person pose or gameplay aim, and still pass an arm-reach check.
- Third person must read at 10 m: the weapon's own pose, cheek weld at aim, sprint carry, lean and reload. Authored poses often look worse in third person, so review both views side by side in every delivery, with an orbit behind the first-person body for broken arms.
- A per-weapon value that drives both views (a canted roll) uses one pivot in both.

## Review surface

**Setup.** One shared review surface for all weapon animation (`REVIEW_SURFACE`), private, phone-viewable, and updatable by any session; it is never cloned per weapon or per pass. Adding a weapon family is a config entry (its folder, clip groups and the view layout of its frames); the page itself does not change. Weapon and creature animation may have separate surfaces, each with its own store.

**What each weapon's page shows:**
- For each action (hold, tactical and empty reloads, draw, holster, inspect, support-hand grips): the current take beside the champion or stamped take on one clock, with frame step, speed control and view switching (eye, third-person three-quarter, side, close on the hands).
- Key-frame sheets and same-framing stills, the contact heat stills, and in-engine captures from `CAPTURE_LIST` once installed.
- A status per clip (in work, ready for review, changes asked, stamped), the critic verdict and the key measured facts behind it.
- A stamp button, a request-changes note, and a version menu when a tuning amount needs choosing (two to four named versions side by side, the recommended one marked with a one-line reason; stamping one withdraws the rest).
- An updates feed and the related docs, so the owner can see what changed since the last look.

**Push flow.** A take reaches the page only after it passes its gates and the critic. Register it as a candidate with a label, the critic verdict and two or three measured facts; build the page data; encode the videos (short, small, frame-accurate); publish only files whose content changed; add an updates line.

**The shared store.** Stamps per clip (take, label, time, who, history), review verdicts with a note per take, notes, and one request thread per clip. Only the owner writes stamps; a newer stamp in the store wins over any copy on disk. A stamp notifies the working session at once, with a periodic sync as the fallback. A proxy stamp is written only when the owner has asked for it, and is labelled as a proxy so the owner can remove it.

**Every animation session starts by syncing the store to disk:** stamps move candidates to stamped, change requests become new takes pushed as new candidates. The owner can send any clip back, stamped or not. Reply to the owner in the main conversation, never inside page threads, and never close a thread for the owner.

## Critic process

- **Blind critics** see only the stills or video of the take and the champion, labelled A and B (A is always the champion copied unchanged), plus `CRITIC_RUBRIC`. They do not see the author's report or the gate results. Their verdict is ship or not ship with blockers only; they never ask for more amplitude.
- **The rubric scores:** hand contact (no floating or sunk fingers), finger and wrist anatomy, the gun path and its weight (anticipation, counter-force, settles), phase timing against the reference, the read in both views (first person framed, third person at distance), and the transitions into and out of the hold. Each note carries a severity: critical (broken, must fix), major (visible to a player in normal play), minor (polish).
- **The pass threshold is set from the scores of owner-approved takes,** not guessed. Approved takes often score well short of perfect and still carry a "major", so a zero-major rule is usually too strict.
- **Feel traces:** every feel claim attaches a trace metrics file with target, measured and pass per item, and a transition readout (values over time across each switch).
- **Hand contact is checked on same-framing stills,** not numbers alone; contact and anatomy reports per digit go with every hand delivery.
- **Calibrate** critics and gates on owner-approved takes before they can fail anything. If approved takes would fail a rule, the rule is wrong.
- **Triage:** blockers (pops, broken hands, clipping, wrong timing, view-only faults) earn a cycle; minor notes go to a backlog; readability notes never buy amplitude past the caps.
- **Read owner notes in pose terms.** When an owner note is ambiguous, restate it as which joint or part moves which way, and confirm before briefing anyone. A critic who dislikes the result may be right.
- **Stop:** one ship verdict plus passing gates means done, freeze it and ask for the stamp. Past about ten cycles on a clip, the lead reviews the sheets personally instead of letting workers grind. Over-cycling on critic notes is where regressions come from.

## Stamping

- **Stamps lock clips** and owner-keyed critical poses. A stamped clip is never modified or re-run through a loop; authoring and push tools refuse stamped clips. Only the owner unstamps.
- A defect on a stamped clip is raised first, then fixed with one minimal change compared visually against the stamped take; keep the stamped take as a backup.
- **Champion take:** the current best is always kept as A. When the owner approves the live weapon feel, that build becomes the feel champion, and any later rig or camera change that reads rougher is rejected however green its gates.
- **No regression:** before pushing anything, view the new sheet against the best earlier sheet. When the owner flags a regression, restore the earlier good take first, then fix minimally.
- **No partial looks:** nothing goes to the owner until the lead has watched a capture of every clip and test route against the readiness criteria. Known-broken or half-finished work is never shown.
- **Close on stamp:** in the same step as recording a stamp, mark the work done; leftovers go to a new follow-up item, never "kept open".

## The blending law

- Everything visual in first person blends, reads and transitions smoothly. Every procedural layer, camera value, stance change, speed change and pose switch states its interpolation (a spring half-life, or a curve plus a settle time). No bare lerp speeds, no instant switches. Working but rough is a reject.
- Blends overlap by default; nothing waits for a previous blend to finish. Transitions carry velocity (inertialization or dead blending, about 0.2 s typical) instead of a linear alpha with corners.
- The camera follows the same frame's pose, never a one-frame-stale socket.
- Every delivery carries a measured transition readout (values over time across the transition) and a capture. Camera reviews also measure frame-to-frame jitter (jerk and direction reversals) on a network client's view as well as standalone.

## Rig contract

- The weapon attaches to the gun IK bone with an identity transform, never to a bone that a later correction moves.
- Comfort: camera bob within small vertical and lateral limits (typically 3.5 and 1.5 cm) over a steady multi-second window, an option halves it, crouch and lean are never attenuated.
- Accuracy: the aim sight stays on the view axis within half a centimetre, walking included; cosmetic overlays finish within about 0.3 s and never move gameplay aim or hits.
- Special states (swim, ladder, mantle, ragdoll, vehicle, death) hand the pose back within a fraction of a second.

## Review checklist

Compile and rig tests green from the log; backups present; first-person body orbit intact; third person reads at 10 m; no neck crease; elbows outside and below without folding into the torso; bob and cadence within limits, the bob rate checked on the first-person stream; aim error within band; identity attach and zero-transform profile; other weapons unchanged; a feel-trace file with target, measured and pass per claimed item; hand contact checked on same-framing stills, not numbers alone; notifies on their frames and sound matching the review surface; no stamped clip or owner key changed.

## Rules

- Measured numbers come from shipped references of this kind (`QUALITY_REFERENCE`); references are studied for numbers, timing and grip geometry and never copied. Every new clip is original: author your own key poses and timing, never a reference clip's body action as the base.
- Clips play at rate 1; timing lives in the clip.
- Owner-keyed critical poses are never re-posed; gates only report on them.
- Explore fast with live tuning values in one persistent test session; land carefully through one gated change.
- Good is done: stop when the feel standard passes and the owner likes it.
- "Does it make sense?" beats any gate row: if obeying a rule would make the motion worse, ask for an exception.

## Done when

Every clip passes the hold, contact and anatomy checks, the feel readout meets `FEEL_STANDARD`, the captures are attached, the clips are stamped on `REVIEW_SURFACE`, notifies and sound line up in game, and the install is reproducible from the exporter and installer alone.
