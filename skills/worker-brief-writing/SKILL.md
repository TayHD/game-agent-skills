---
name: worker-brief-writing
description: Write an implementation brief for an AI worker that it can execute without judgment calls - facts read before writing, architecture given, acceptance stated as observable measured results, a trimmed stage list and an exact report format. Use when a manager or lead hands a ticket, phase or task to another agent.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Writing a worker brief

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `DESIGN_DOCS` | Where the authoritative design for each system lives. |
| `PROJECT_MAP` | Where code, assets, tools and data live. |
| `TEST_RULES` | The project's test and harness rules (read before any test). |
| `BACKUP_DIR`, `EVIDENCE_DIR`, `HEARTBEAT_LOG` | Per work item. |
| `BRIEF_DIR` | Where long briefs are filed. |

## Before writing

1. **Confirm the problem is real and where it lives:** read the ticket, its design doc and the code, with file and line references.
2. **Read every fact the design rests on** and put the number and its source in the brief: clip root travel and play rate, curves, notifies, stored data classes, property types, schema versions, profile names. A design resting on a fact nobody has read is not ready; if the number cannot be read yet, the read is step one.
3. **Map research to work.** When a design rests on a research report, every recommendation maps to a task or to an explicit "not doing, because" line.
4. **For a second instance of a template** (a second species, a second weapon family), grep the tools and builders once for the first instance's hard-coded names and list every one as a gap.
5. **Decide design questions yourself** or escalate them; never leave taste or shape to the worker.

## What the brief contains

1. **Goal and why**, in two or three sentences.
2. **Architecture as a given:** the classes, files and data the change uses, with line references. No options for the worker to choose between.
3. **Constraints:** backups before every change, live files only under the slot, imported art read-only, no patching of retired paths, performance and authority rules.
4. **Ordered steps,** including which iteration path each change takes (a function-body edit can be tried live; a header or reflected-type change needs a restart or rebuild).
5. **Acceptance as observable, measured results:** a value, a band, a log line, a test name with its expected verdict, a capture that shows a named thing. Never "works" or "looks good".
6. **A trimmed stage list:** only the gates the change owns, a smoke stage first, and the expected minutes.
7. **Tests:** the one targeted check that proves the change, the suites to run, expected values taken from live data or a baseline run, never from reading the code.
8. **Report format:** what was built, how the owner verifies it (map, input, expected result), the validation actually run with evidence paths, files changed, backups, remaining risks, and the doc updated.
9. **Stop points:** where the worker ends its turn for review.

## Done when

A fresh worker with only the brief, its role card and the project map could finish the task and you could check every acceptance line from its evidence without asking it anything.
