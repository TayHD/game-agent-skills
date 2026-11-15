---
name: unreal-automation-test-lessons
description: Checks to run before writing or running Unreal Engine automation tests, NetPIE runs, QA harnesses or commandlet batches - the recurring traps sorted by area (compile, launch flags, profiles, gates, measurement, disk). Use before any test run, harness change or batch of headless editor runs.
metadata:
  version: "0.1.1"
  updated: "2026-11-15"
---

# Unreal automation test lessons

Each line is a trap that cost at least one real run. Run the checks of every area your run touches.

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `TEST_PREFIX` | The project's automation test prefix. |
| `QA_PROFILE_RULE` | The saved-dir suffix or profile name the project's QA fixtures require. |
| `PROFILE_HELPER` | The helper that creates a clean test profile (UserDir) with a shared Python environment. |
| `SHARED_PIP` | The one shared folder every profile's `Intermediate/PipInstall` links to. |
| `BASELINE_DIR` | The latest full-run baseline to compare reds against. |
| `LEDGER` | The project's dated ledger of runs lost to test problems. |
| `GREEN_RUNS` | Where the exact command line of each test's last green run is kept. |
| `HARNESS_ROW_LIST` | The tests known to need a rendered editor, a sound device or their own QA switches, with their launch. |

## Before you compile

- Check every engine symbol a new test uses exists in the engine headers of the version you build against.
- Nothing in `PostLoad` or a class default constructor reaches managers that do not exist yet at load.
- Prefer adding tests to an existing file; a new or removed `.cpp` can leave a stale build makefile.
- Since UE 5.9 a module's `Tests/` folder is treated as low-level tests: UHT generates no headers there in non-test builds. Keep every reflected type (UCLASS, USTRUCT, UENUM) out of `Tests/`, and write includes relative to each includer's own folder.
- Resolve every quoted include the way the compiler will (own folder, includer folders, the target's include paths) before the slot; a lint that adds the module folder to the path hides misses.
- Never name a local after a class member; shadowing warnings are often errors.

## Before you launch

- Take the engine slot and check free RAM first (the `shared-engine-slot` skill).
- Copy launch flags from the test's last green run in `GREEN_RUNS`, never retype them; diff your line against it. Commands that take commas go in a script, not inside `-ExecCmds`, which splits on commas.
- Every batch uses `QA_PROFILE_RULE` (no dashes: Unreal strips them from the saved-dir suffix). A batch with the wrong suffix is invalid in full.
- Make profiles only through `PROFILE_HELPER`, which links `Intermediate/PipInstall` to `SHARED_PIP`. A bare `mkdir` per batch costs about 5 GB per profile. Reuse profiles by folder name between serial batches; do not wipe a profile before each batch unless the test needs a reset.
- Every engine command runs under a hard timeout that kills the whole process tree (on Windows a shell `timeout` around an editor may leave children running; check, or kill the tree explicitly).
- Never use a content-writing commandlet (for example `ResavePackages`) as a probe; it does not honour `-help` and resaves content.
- Tests that need a rendered editor, a sound device or their own QA switches fail in a headless `-NullRHI -nosound` batch. Run them singly with the launch `HARNESS_ROW_LIST` gives before calling them product reds.
- Live Coding is disabled in an editor started with `-unattended` until it is enabled explicitly.

## Gates and measurement

- Attribute each failing assertion to its own test; in the automation log a test's errors print inside its own begin and end events.
- Known-failure lists are per test and match exactly; a red identical to `BASELINE_DIR` is inherited.
- Expected values come from live data or a baseline run, never from reading the code.
- A row that claims something is visible reads pixels or an in-view measure, not a component's existence. Look at the frames after every green run that claims a visual result.
- A comparison needs a control run of the same build to size the noise, and its "before" must be the shipped build.
- A sim or offline model is a geometry check only; it never predicts an engine result on a clip-driven pose.
- Plant a fault for every gate before trusting it.

## Disk and files

- Write a new run's logs to its own run folder; never into `BASELINE_DIR`, which is only read for comparison.
- After the summary is kept, delete the run's profiles and saved-dir folders (by exact path, never by wildcard).
- Raw frame dumps, traces and per-run installs are deleted after encoding or once summarised; keep the CSV or report.
- Lab traces go where the engine's trace command is allowed to write, then get copied into the evidence folder.

## After the run

Add one dated line to `LEDGER` for any run lost to a test problem: date, work item, what went wrong, the rule. A lesson that recurs goes into the kit's own checks, not only into the ledger.
