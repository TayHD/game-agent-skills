# Game agent skills: catalogue

A library of transferable skills for AI agent teams working on an Unreal Engine game. Each skill carries a **method only**: no project names, paths, ticket ids, people, assets or third-party material. Anything a project must supply is a named **setting** listed at the top of the skill; the host project provides the values in a thin binding of its own (for example a project skill that maps each setting to a path or rule).

Layout: a Claude Code plugin. `.claude-plugin/plugin.json` is the manifest, `.claude-plugin/marketplace.json` lets the folder be added as a one-plugin local marketplace, and each skill is `skills/<name>/SKILL.md` with any scripts beside it.

Version 0.1.0, 2026-11-15. Licence: pending, see `LICENSE-PENDING.md`.

## Skills

| Skill | What it is for | Settings it needs | Drawn from | Version |
|---|---|---|---|---|
| `staged-change-landing-hold` | Land a change through a staged, gated exclusive run: smoke first, owned gates only, inherited baseline reds, fixture versus product reds, unwind on a product red. | SLOT_RULES, BACKUP_DIR, EVIDENCE_DIR, KIT_TEMPLATES, TEST_PREFIX, BASELINE_DIR, ENGINE_ROOT | The test and harness guide, test lessons | 0.1.0 |
| `shared-engine-slot` | One Unreal process at a time through a lock file and a reservation file; direct take, release, stalls. Script `scripts/slot.sh`. | LOCK_FILE, NEXT_FILE, HOLDER_FORMAT, SLOT_ORDER, MIN_FREE_RAM_GB, HEARTBEAT_LOG | The project's slot rules | 0.1.0 |
| `agent-team-operation` | Manager, implementers and watch; one live state in the tracker; phase-sized workers with resume notes; heartbeats; blocked means report and stop. | TRACKER, ROLE_CARDS, OWNER, HEARTBEAT_LOG, RESUME_NOTE, RULINGS_LOG | Role cards, the organisation spec | 0.1.0 |
| `worker-brief-writing` | Briefs a worker can execute without judgment: facts read first, architecture given, measured acceptance, trimmed stage list. | DESIGN_DOCS, PROJECT_MAP, TEST_RULES, BACKUP_DIR, EVIDENCE_DIR, HEARTBEAT_LOG, BRIEF_DIR | The manager card | 0.1.0 |
| `agent-work-review` | Review the real diff and evidence, the third-attempt review, escalation, the process question. | BACKUP_DIR, EVIDENCE_DIR, RULES, PLAYTEST_LIST | The manager card, test lessons | 0.1.0 |
| `unreal-automation-test-lessons` | Recurring traps in Unreal automation tests, NetPIE runs and headless batches, as checks by area. | TEST_PREFIX, QA_PROFILE_RULE, PROFILE_HELPER, SHARED_PIP, BASELINE_DIR, LEDGER | The test lessons ledger | 0.1.0 |
| `blueprint-to-cpp-migration` | Migrate touched Blueprint behaviour to C++ with parity tests, retire the graph, never patch it. | BP_ROOTS, READ_ONLY_ART, SAVE_MIGRATION, BACKUP_DIR | The native migration doc | 0.1.0 |
| `engine-version-upgrade` | Inventory, patches on a branch, one engine root, snapshot, two-step builds, new baseline, save round-trip, package, cut over. | ENGINE_ROOT_FILE, ENGINE_CHECKOUT, TARGETS, SUITES, SNAPSHOT_DIR, SLOT_RULES, SHIP_GATE | The UE 5.9 cutover | 0.1.0 |
| `editor-agent-toolsets` | Enable and use the UE 5.9 editor MCP server and toolsets: editor only, loopback, the four meta-tools, the proxy, the shipping gate. Script `scripts/mcp_call.py`. | ENGINE_ROOT, UPROJECT, MCP_JSON, TOOLSET_LIST, SLOT_RULES, INSTRUCTIONS_TEXT | The UE 5.9 cutover | 0.1.0 |
| `creature-animation-pipeline` | Large-creature animation: biomechanics, rig profile and caps, key frames first, clip order, mirrors, calibrated gates, stamps, champion take. | RIG_SOURCES, RIG_PROFILE_FORMAT, STAMPS, REVIEW_SURFACE, CLIP_LIST, QUALITY_REFERENCE | The creature animation playbook | 0.1.0 |
| `first-person-weapon-animation` | Gun-space rig, measured hold poses, gun-first actions, export and install, profiles, the blending law, feel checks. | DCC_RIG, WEAPON_SOCKETS, HOLD_CHECKS, EXPORTER, INSTALLER, FEEL_STANDARD, CAPTURE_LIST | The weapon animation playbook | 0.1.0 |
| `motion-matching-kit-build` | Motion-matching coverage, clip rules, curves, schema and databases, every clip wired, lab measurement. | SPEED_TABLE, CLIP_NAMING, CURVE_NAMES, KIT_FOLDER, LAB | The motion-matching set and kit docs | 0.1.0 |
| `modular-environment-kit-production` | Kit production from baseline to shipped: core library, closure, compliance by construction, scan-gated critics, prefabs, finish bar. | GRID_CONTRACT, FINISH_SPEC, CORE_LIBRARY, PIECE_CAP, CRITIC_TARGET, MATERIAL_BAR, IMPORT_PATH | The kit production playbook and finish spec | 0.1.0 |
| `creature-ai-state-trees` | Server-authoritative creature brains on State Trees: layers, pure selection, roles, species as data, measured feel, capture before claiming. | FEEL_TARGETS, ROLES, SPECIES_DATA, LAB, SANITY_CHECK, BUDGETS | The creature AI playbook | 0.1.0 |
| `human-npc-ai` | Human NPCs: readable awareness, fair accuracy, squads, a truthful body, lab measurement, bounded cost. | FEEL_TARGETS, LAB, PROFILES, ANIM_BUDGET, TEST_PREFIX | The human AI playbook | 0.1.0 |

## Using the library in a project

- **Try it for one session:** start Claude Code with `--plugin-dir <path to this folder>`.
- **Install it in a project:** add the folder as a local marketplace (`/plugin marketplace add <path>`), then `/plugin install game-agent-skills@game-agent-skills-local` with project scope. Skills appear as `/game-agent-skills:<skill>`.
- **Bind it:** write one project skill (or doc) that gives a value for every setting the skills you use list. Keep project facts there, never in this library.
- **Check it:** `claude plugin validate <path>`.

## Rules for adding or changing a skill

1. **Methods only.** No third-party assets, code or reference material, no licensed or private content. A skill may say "study a shipped reference of this kind"; it never names or includes one.
2. **No private details:** no account names, machine paths, session ids, ticket text or tracker contents.
3. **Tested before listed:** a fresh worker with only the skill and a project binding performs the task once, and the skill is fixed until it does.
4. **One home per procedure:** the source document keeps the history and the reasons and points at the skill; the steps live here only.
5. Bump the skill's `metadata.version`, its row above, and `CHANGELOG.md`.
