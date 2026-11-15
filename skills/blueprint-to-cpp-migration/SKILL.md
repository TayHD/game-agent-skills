---
name: blueprint-to-cpp-migration
description: Migrate gameplay behaviour from Unreal Blueprint graphs to C++ with parity tests, retire the graph instead of patching it, and keep designers able to tune everything. Use when a task touches a Blueprint-driven gameplay system, when a bug fix would add a guard to a graph, or when planning a native migration.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Blueprint to C++ migration

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `BP_ROOTS` | Content folders whose gameplay Blueprints count as project code to migrate. |
| `READ_ONLY_ART` | Imported content that is never modified. |
| `SAVE_MIGRATION` | How saved data is versioned and migrated. |
| `BACKUP_DIR` | Where originals of every asset and file go before a change. |

## Target pattern

| Layer | Lives in |
|---|---|
| Logic, state, validation, replication, persistence | C++ components, subsystems and base classes |
| Tuning | `EditDefaultsOnly` properties or a data asset |
| Designer hooks | Implementable or native events for cosmetic reactions only, never authority |
| Presentation | Blueprint subclasses, widget layout, animation graphs |
| Imported art | Referenced or wrapped, never edited |

A Blueprint subclass that only sets defaults and art is the goal; a graph that decides gameplay is migration debt.

## Rules

1. **Touch rule.** Work that touches a Blueprint-driven system migrates the touched behaviour to C++ and retires the Blueprint path: callers removed, nodes deleted, graph audited.
2. **Never patch a retiring graph.** A guard on an old graph is a stopgap only for a blocking bug today, with a migration task filed beside it.
3. **No duplicates.** A native replacement is not done while the graph still runs.
4. **Authority first.** Any graph that decides a server-authoritative outcome (hits, damage, kills, loot, currency, stat writes) gets its own migration task in the active order; it is never parked behind a polish task.
5. **Parity, then improvement.** Reproduce current behaviour with tests first; improve in a separate step unless the old behaviour is a known bug.
6. **Saved data** goes through `SAVE_MIGRATION`.
7. **Designability.** After migration a designer can tune everything they could before, without code; the report lists the exposed tuning.

## Method

1. **Audit:** node and function counts, authority and replication (RPCs, replicated variables, authority branches), persistence, tick use, callers, existing native partials, bug history. Enumerate users by path or referencers and load them; never filter on saved registry class tags, which go stale.
2. **Write parity tests** through real entry points on the current behaviour.
3. **Implement natively,** exposing tuning.
4. **Retire in a dry run first:** a scripted retire with a dry-run mode, then the real retire, with backups. A native function wired in place of a Blueprint read gives array inputs a default reference term so the graph still compiles.
5. **Referencer scan before a component retirement** over every game package; an unreviewed user outside the set refuses the retire.
6. **Audit the saved graph** afterwards: list every remaining node and why it is cosmetic.
7. **Verify** on a dedicated server with two clients, with no new warnings.

## Done when

All authority, state and persistence live in C++ with tests, the graph holds no gameplay decisions (audited), tuning is exposed and documented, and the retired nodes or assets are removed with backups.
