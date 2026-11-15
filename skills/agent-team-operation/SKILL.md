---
name: agent-team-operation
description: Run a small team of AI agents on a game project with fixed roles (manager, implementers, a watch), one live state kept only in the work tracker, heartbeats, phase-sized workers with resume notes, and "blocked means report and stop". Use when setting up or operating a multi-agent workflow, launching a worker for a phase, or deciding who does what.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Agent team operation

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `TRACKER` | The work tracker and how agents reach it (tools or a shell client). |
| `ROLE_CARDS` | One static card per role: job, what it owns, start and stop steps, binding rules. |
| `OWNER` | The human who decides vision and story and gives final approval. |
| `HEARTBEAT_LOG` | One line per step per work item. |
| `RESUME_NOTE` | The per-item note a fresh worker reads first. |
| `RULINGS_LOG` | Where the owner's standing decisions are recorded, dated. |

## Roles

- **Manager (one session).** Scopes, briefs, launches and reviews workers; makes design and process calls; keeps the slot order and the docs. Takes only vision and story to the owner.
- **Implementers (one subagent per work item or phase).** Bounded engineering from a brief that states the architecture as a given. Never decide shape or taste. A smaller model does bounded work; a stronger model takes a work item when judgment is needed, after two review rounds, or when tests were not run.
- **Watch (optional).** Dispatches the engine slot, watches heartbeats, records events. No judgment.

## Rules that keep it working

1. **One live state.** What a seat holds, the queue order and parked work live in the tracker and nowhere else: no handoff file, chat thread or card holds a queue or a status.
2. **Cards are static.** A card changes only when a role's job changes.
3. **One worker per phase, not per work item.** A worker ends its turn at every review stop and leaves `RESUME_NOTE` (under about 60 lines: state, staged files, rulings in force with dates, evidence paths, the exact next command, open questions). The next worker reads that first and the history only for what it lacks.
4. **First action fast.** Within about 15 minutes a worker is doing the work (backup, stage, edit), not reading around.
5. **Heartbeat.** One line per step: time, doing, waiting on. Twenty minutes of silence is a stall.
6. **Blocked means report and stop.** Write the exact blocker to the work item and the heartbeat, release shared resources, end the turn. Never sit in a loop.
7. **Readable progress.** Every progress note is plain sentences a human can follow. Anything addressed to the owner is a few lines: outcome, what they must do, where the detail is.
8. **Owner answers are applied at once,** folded into the brief the same session, and recorded in `RULINGS_LOG`.
9. **Nobody queues approvals on the owner.** A refused action is pasted on the work item and re-routed by the manager.
10. **Save what you find.** A location you had to search for goes into the project map; a lesson goes into the system's playbook or the test lessons ledger, the same session.

## Launching a worker

Give it: the work item, its card, the model, its holder string for the slot, the backup and evidence folders, the stop point for this phase, and any ruling not yet in `RESUME_NOTE`. Nothing else; the card and the note carry the rest.

## Done when

Every in-progress item has a current progress note, the slot is free or handed on, and nothing about the state lives outside the tracker.
