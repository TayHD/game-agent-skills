---
name: first-person-weapon-animation
description: Build first-person and third-person weapon animation for an Unreal shooter - gun-space rig, measured hold poses, gun-first action authoring, export and install with round-trip checks, per-weapon profiles, the blending law and measured feel checks. Use when authoring hold poses, reloads or other weapon actions, installing weapon animation, or reviewing weapon feel.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# First-person weapon animation

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `DCC_RIG` | The character rig file used for weapon authoring and its gun bone. |
| `WEAPON_SOCKETS` | The socket names every weapon carries (sight, muzzle, support grip, magazine, stock). |
| `HOLD_CHECKS` | The pose checker and its bands. |
| `EXPORTER`, `INSTALLER` | The export and import scripts and their deliberate flags. |
| `FEEL_STANDARD` | The measured feel targets and pass bands. |
| `CAPTURE_LIST` | The fixed set of in-engine captures every delivery produces. |

## Pipeline

1. **Weapon mesh:** re-pivot it and write the sockets; moving parts stay as bones. Put the support grip socket mid-handguard.
2. **Hold pose** on `DCC_RIG`: shouldered ready, passing `HOLD_CHECKS`. Typical bands: stock within a few centimetres of the shoulder pocket, bore near level, the sight a measured distance below and right of the eye (framing comes from a camera offset, never from bending the pose), head upright, palms on their grip targets, neck and elbow guards.
3. **Actions, gun first:** blockout; key poses on the gun bone; gun inbetweens; timing; detail; hands pass; physics pass; polish.
4. **Export** with a round-trip check (sub-millimetre) and a hold pose exported as two identical frames.
5. **Install** in steps: reimport is the default; tuning writes, graph rebuilds and installs are separate, deliberate flags.
6. **Profile:** the per-weapon profile holds zero transforms; tuning lives in the weapon class asset.
7. **Verify** with `CAPTURE_LIST` (first person hip, aim, walk, sprint; third person hip, aim, sprint; an orbit behind the first-person body; side views), the rig tests, and a feel readout.

## The blending law

- Everything visual in first person blends, reads and transitions smoothly. Every procedural layer, camera value, stance change, speed change and pose switch states its interpolation (a spring half-life, or a curve plus a settle time). No bare lerp speeds, no instant switches.
- Blends overlap by default; nothing waits for a previous blend to finish.
- The camera follows the same frame's pose, never a one-frame-stale socket.
- Every delivery carries a measured transition readout (values over time across the transition) and a capture.

## Rig contract

- The weapon attaches to the gun IK bone with an identity transform, never to a bone that a later correction moves.
- Comfort: camera bob within small vertical and lateral limits over a steady multi-second window, an option halves it, crouch and lean are never attenuated.
- Accuracy: the aim sight stays on the view axis within half a centimetre, walking included.
- Special states (swim, ladder, mantle, ragdoll, vehicle, death) hand the pose back within a fraction of a second.

## Review checklist

Compile and rig tests green from the log; backups present; first-person body orbit intact; third person reads at 10 m; no neck crease; elbows outside and below without folding into the torso; bob and cadence within limits; aim error within band; identity attach and zero-transform profile; other weapons unchanged; a feel-trace JSON with target, measured and pass per claimed item; hand contact checked on same-framing stills, not numbers alone.

## Rules

- Measured numbers come from shipped references of this kind; references inform, they are never copied.
- Clips play at rate 1; timing lives in the clip.
- Owner-keyed critical poses are never re-posed; gates only report on them.
- Good is done: stop when the feel standard passes.

## Done when

Every clip passes the hold and contact checks, the feel readout meets `FEEL_STANDARD`, the captures are attached, and the install is reproducible from the exporter and installer alone.
