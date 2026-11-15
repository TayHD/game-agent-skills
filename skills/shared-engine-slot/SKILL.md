---
name: shared-engine-slot
description: Share one machine's single Unreal process slot (editor, commandlet or UBT build) between several agents and a human through a lock file and a reservation file, with direct take, release and stall rules. Use before launching any Unreal editor, commandlet, build or MCP editor session on a machine where only one Unreal process may run.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Shared engine slot

On a machine with limited RAM, one Unreal process at a time: an editor, a commandlet, a UBT build, or an editor serving MCP tools. A human's open editor counts.

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `LOCK_FILE` | The lock file; its content names the holder. |
| `NEXT_FILE` | The reservation file; it names the only holder allowed to take a free slot. |
| `HOLDER_FORMAT` | The exact holder string, for example `<work-item> (<role>)`. |
| `SLOT_ORDER` | Where the queue order lives (a ticket or board item, never a chat). |
| `MIN_FREE_RAM_GB` | Free RAM required before a take. |
| `HEARTBEAT_LOG` | Where a holder writes one line per step. |

## Method

1. **Check.** If `LOCK_FILE` exists, the slot is busy: do offline work or end the turn; never wait in a polling loop that notifies nobody.
2. **Take.** Only when the lock is absent and `NEXT_FILE` is empty (and you are first ready in `SLOT_ORDER`) or names you exactly. Write the lock with a create-if-absent write that fails when the file exists, then read it back to confirm it names you. Delete `NEXT_FILE` in the same step when it named you. `scripts/slot.sh take "<holder>"` does this.
3. **Before launching,** confirm `MIN_FREE_RAM_GB` and state a time limit for the run.
4. **Release** the moment the Unreal run ends (`scripts/slot.sh release "<holder>"` refuses to delete someone else's lock). Hold per session, never across idle gaps.
5. **Reserve** with `NEXT_FILE` only when your Unreal step is ready to start the instant the slot frees; a reservation nobody is ready to use idles the slot.
6. **Back-to-back rounds** check `NEXT_FILE` before each new round and yield to whoever it names.

## Rules

- Never kill an Unreal process you did not start. Report a foreign Unreal or UBT process that holds no lock; do not stop it.
- Builds of other projects on the same machine take the slot too.
- A blocked holder writes the exact blocker to its work item and heartbeat, releases unless a retry is minutes away, and ends its turn.
- Twenty minutes of heartbeat silence on a live hold is a stall for the coordinator to handle.
- A human's urgent need outranks the queue; a top-priority item goes to the head of `SLOT_ORDER` the moment it is ready.

## Done when

Your run finished, the lock is gone (or names the next holder you handed to), and your heartbeat says so.
