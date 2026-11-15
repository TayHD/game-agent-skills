---
name: staged-change-landing-hold
description: Land a code or content change into a shared Unreal project through a staged, gated "hold" (stage offline, smoke first, run only the gates the change owns, inherit baseline reds, tell fixture reds from product reds, unwind on a product red). Use when a change must be built and tested under an exclusive engine slot, when writing or running a hold kit, or when deciding whether a red result blocks a landing.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Staged change and landing hold

A **hold** is one exclusive, scripted window in which a staged change is applied to the live project, built, tested against gates and either kept (landed) or restored (unwound). Everything that can happen outside the hold happens before it.

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `SLOT_RULES` | How the exclusive engine slot is taken and released (see the `shared-engine-slot` skill). |
| `BACKUP_DIR` | Where originals are copied before any change, per work item. |
| `EVIDENCE_DIR` | Where logs, reports and verdicts are kept after the work item closes. |
| `KIT_TEMPLATES` | The hold-kit templates a new kit copies (runner, gates, selftest). |
| `TEST_PREFIX` | The automation test name prefix the project owns. |
| `BASELINE_DIR` | Logs of the current engine and code baseline that reds are compared against. |
| `ENGINE_ROOT` | How scripts find the engine (one setting, never a literal path). |

## Method

1. **Stage offline.** Put changed files in the kit's own folder with the live originals beside them and a hash list of what the change expects to find live. Nothing live changes outside the hold.
2. **Write a trimmed stage list.** Only the gates this change owns: its build targets, its tests, its captures. Stages already green on identical source do not rerun. Post the list and a minute estimate before asking for the slot.
3. **Dry-run the kit.** Byte-compile every script, run the kit selftest, pass every engine command through the runner's real command path with a fake engine, and replay each gate against an old evidence folder. A kit fault found here costs seconds; found in the hold it costs the slot.
4. **Smoke first.** The first stage in the hold is one short test that proves the build, the launch flags and the gate parsing work, before any long stage.
5. **Candidate compile first.** Apply, build the candidate, and only then capture bases or audits. A compile error found after a long base capture wastes the whole capture.
6. **Judge every row.** Each gate row is classed PRODUCT (the change's behaviour) or FIXTURE (setup, harness, environment). A missing row fails. Rows after a fixture stop count as blocked, not as product failures.
7. **Inherit baseline reds.** A red row identical to its baseline row (same test, same failing assertion text, digits normalised) is inherited and does not block. A red with no baseline row is judged on its own.
8. **Decide.**
   - All owned product rows green: land, keep the backups, release the slot.
   - Fixture-only red with every product row green: keep the candidate and the slot, fix the fixture offline, rerun only that stage within a stated allowance.
   - Any product red or compile error: restore every staged file, rebuild the originals, verify the restore by hash, release.
9. **Leave evidence.** The verdict line, every stage log and the decision go to `EVIDENCE_DIR`, not only to scratch staging that is pruned later.

## Stop rules

- Two reds on the same row: stop and read the fixture and the row's purpose before anything is staged again. A rerun justified only by a reading of the code is refused.
- Before a third hold on one change, a reviewer replays every gate against known-good and planted-bad evidence and signs the kit.
- A measurement-only kit must not be able to land anything: its decision step is report-only.
- A gate revised after a run never lands on that run's evidence; it is replayed and the next hold judges it.
- Every engine command runs under a hard timeout.

## Pitfalls seen in practice

- Exit codes are not verdicts; read the verdict line and the rows.
- A gate that reads a component's state instead of the drawn or returned result passes broken products. Gates judge what a player or caller actually gets.
- New bars are report-only in their first hold and are calibrated from a clean run before they can stop a landing.
- Live edits by another worker during a hold break both. Live source changes only inside a runner that holds the slot.

## Done when

The change is landed with a green verdict on every owned product row, or unwound with the live project byte-identical to its originals, and the evidence folder explains which.
