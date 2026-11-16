# Changelog

## 0.1.5 (2026-11-15)

- New skill `project-knowledge-system` 0.1.0: a project's knowledge base as plain Markdown in the project folder (knowledge map, decisions log, doc index, project map, design docs, playbooks, lessons ledger, one live status file, archive), with starter templates and the drift check `scripts/kb_check.sh`. Engine- and genre-neutral; needs no tracker. Every setting has a default, so it works without a binding. Tested before listing by a fresh worker setting it up for an unrelated engine and genre; its findings were fixed before release: store templates and per-use templates are separate, one placeholder list, setup creates the folders and copies the check script into the project, owner questions have one home, and the check matches index paths exactly and validates dates strictly.

## 0.1.4 (2026-11-15)

- Marketplace manifest: the plugin's relative source is now written `./`, the form the plugin loader expects for a path inside the marketplace.

## 0.1.3 (2026-11-15)

From the package smoke of an engine upgrade:
- editor-agent-toolsets 0.1.1: keep the toolset registry's generated manifest content out of server and client cooks (a never-cook directory); the shipping gate matches the named agent plugins, not the bare word `Toolset`, because stock engine modules share it.
- engine-version-upgrade 0.1.1: four new traps: gitignored files the automation tool needs can be missing from a source-built engine; editor plugins can add folders to every cook; gate on exact plugin names; a shipping client may ignore command-line travel and exec commands, so the unattended join check uses a development client with the project's test switches.

## 0.1.2 (2026-11-15)

- first-person-weapon-animation: the gun-first step is now stated as a principle in the library's own words instead of a fixed step list.

## 0.1.1 (2026-11-15)

From the first fresh-worker tests (README rule 3), run on three skills with fresh workers given only the skill:
- shared-engine-slot: `slot.sh reserve`; holder strings match exactly; only the coordinator clears a stale reservation; the script enforces the lock and reservation only (RAM, order and heartbeat stay manual).
- unreal-automation-test-lessons: new settings `GREEN_RUNS` and `HARNESS_ROW_LIST`; take the slot and check RAM first; diff the launch line against the last green run; reuse profiles by folder name; timeouts kill the whole process tree; new run logs never go into the baseline folder; clean profiles and saved dirs by exact path.
- agent-work-review: with no brief, judge against the task statement; equal pass counts with different output is a claim to correct; a test for "changes how a system works"; blocking versus advisory findings.
- The other twelve skills are not yet tested by a fresh worker (they need the engine, a DCC tool or a long run).

## 0.1.0 (2026-11-15)

- First set of 15 skills: staged-change-landing-hold, shared-engine-slot (with `scripts/slot.sh`), agent-team-operation, worker-brief-writing, agent-work-review, unreal-automation-test-lessons, blueprint-to-cpp-migration, engine-version-upgrade, editor-agent-toolsets (with `scripts/mcp_call.py`), creature-animation-pipeline, first-person-weapon-animation, motion-matching-kit-build, modular-environment-kit-production, creature-ai-state-trees, human-npc-ai.
- Plugin manifest and one-plugin local marketplace.
- Licence pending (owner's decision); repository local and private.
- Not yet done: the fresh-worker test of each skill (rule 3 of the README), and an install test in an empty project.
