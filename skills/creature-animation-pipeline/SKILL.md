---
name: creature-animation-pipeline
description: Author a full animation set for a large creature (dinosaur, beast) with AI help - biomechanics first, rig profile and joint caps from the mesh, key frames first, clip order, mirrors, calibrated gates, the owner's stamp loop and a no-regression champion take. Use when starting a new species, authoring or fixing creature clips, or setting up creature animation critics and gates.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Creature animation pipeline

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `RIG_SOURCES` | Where the source rigs live (read-only). |
| `RIG_PROFILE_FORMAT` | The bone map, chains, IK targets and side suffix every tool reads. |
| `STAMPS` | Where approved (locked) clips are recorded, and who may stamp. |
| `REVIEW_SURFACE` | Where takes are shown to the owner beside the stamped take. |
| `CLIP_LIST` | The project's standard clip set per species. |
| `QUALITY_REFERENCE` | The kind of shipped reference the owner holds up as the bar (studied, never copied). |

## Biomechanics first

- Build a reference set per species from living relatives (large birds for bipedal gait and head stabilisation, large mammals for mass and timing, crocodilians for tail and sprawl). Take the principle, never the surface motion.
- Respect the skeleton: a large biped's back is a stiff beam; weight transfer happens at the hips (yaw, roll, sway and bob over the stance leg); counter-motion lives in the shoulders, neck base, neck and head (holding its line) and the tail (a lagging counterweight).
- Estimate mass first and let it drive spacing, impact, settle and transitions. Heavy animals start slowly, stop late and never gallop.

## Species start-up (once, before any clip)

1. Probe the rig (bones, constraints, meshes, frame rate) and write the rig profile; make every tool read it before a second species animates anything.
2. Audit the rig with close renders of rest and extremes (appendages, membranes, claws); decide rig additions now, with the owner's agreement, and back up the source.
3. Set joint caps from where the mesh collapses, not from taste, per joint and rest-relative, with sign conventions.
4. Get the home pose right first; every one-shot starts and ends there.
5. Set the caps table before authoring: lean per gait, tail lift and yaw per clip kind, head-yaw budget, leg caps by speed, appendage clearance.
6. Calibrate every gate on a take the owner approved, never on a guess.
7. Register the species on `REVIEW_SURFACE` and turn on the stamp lock before the first push.
8. Decide the left/right masters before any side clip.

## Clip order

Idle and home; forward gaits (each stamped before its sides); one master side per pair built from the stamped forward cycle (same duty, contact timing and joint ranges), the other mirrored; turns; one-shots from home; chains last with shared seam poses. Never run open cycles on two clips that share a chain pose.

## Gates that stop regressions

- Lean follows physics, not readability: small bank at walk, more at run.
- The tail is a counterweight, not a whip: capped lift and yaw, at least a few frames rest to peak, no hooks.
- Leg joints capped by speed; free and air clips still held to the knee cap.
- Leg snap: cap the median leg acceleration, scaled by speed.
- Appendage clearance by folding or tucking, never by hiding the limb.
- Gates are absolute, every exemption is listed and reviewed, and a new gate is calibrated on approved takes before it can fail anything.

## The loop

- **Key frames first:** block the key poses and get them right before inbetweens and polish.
- **Mirrors:** author only the master; regenerate the mirror whenever the master changes; a mirror inherits its master's status; previews show both sides of the animal.
- **Stamps lock clips.** Only the owner unstamps; a defect on a stamped clip is raised first, then fixed with one targeted change.
- **Champion take:** the current best is always kept and compared; a new take replaces it only when it is better, never on critic notes alone.
- **Know when to stop.** Critics are calibrated to what the owner stamped; minor notes go to a backlog. Over-cycling on critic notes is where regressions come from.
- **Read notes in pose terms** and restate them before acting.
- **Every clip gets wired** into the game; an unwired clip is unfinished work.

## Done when

The species' clip list is stamped, every clip is wired, and the gates and caps that were needed are written into the species' profile for the next species to copy.
