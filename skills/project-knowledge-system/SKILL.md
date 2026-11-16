---
name: project-knowledge-system
description: Set up and keep a game project's knowledge base as plain Markdown files in the project folder, so the lead agent always has one source of truth and stays consistent across sessions, context resets and model or account changes. A knowledge map as the single entry point, a dated decisions log, a document index with status, a project map of locations, living design docs, pipeline playbooks, a lessons ledger and one live status file. No tracker, engine or service needed. Use when starting or adopting a project, at the start of every lead-agent session, when the owner makes a decision, when you had to search for something, when writing, changing or retiring a doc, or when asked where knowledge lives.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Project knowledge system

The point: an agent forgets everything between sessions; the project must not. Every fact another session will need is written into one known file the same session, and one entry page says where every kind of fact lives. The lead agent reads that page first, every session, and keeps it true. Consistency comes from two habits: decisions are looked up before acting, and new decisions are written down before moving on.

Works for any kind of game and any engine. Everything is plain Markdown in the project folder; version control is optional but makes history free.

## Settings the project supplies

Every setting has a default, so the skill works without a binding. A project that already keeps some of these somewhere else (a tracker, a wiki, another folder) maps the setting to that place instead.

| Setting | Default | Meaning |
|---|---|---|
| `KNOWLEDGE_ROOT` | `Docs/` | Folder that holds the knowledge files. |
| `KNOWLEDGE_MAP` | `Docs/KNOWLEDGE.md` | The single entry page: the stores, where to put X, where to look for X, session start. |
| `DECISIONS_LOG` | `Docs/DECISIONS.md` | Every standing decision by the owner (and the lead's own provisional calls), dated, one line each, by area. |
| `DOC_INDEX` | `Docs/INDEX.md` | Every document, by system, with its status. |
| `PROJECT_MAP` | `Docs/PROJECT_MAP.md` | Where things are: code, assets, data, tools, tests, build outputs. |
| `DESIGN_DIR` | `Docs/Design/` | Living design documents, one per system. |
| `PLAYBOOK_DIR` | `Docs/Playbooks/` | One playbook per production pipeline, each with a lessons log. |
| `LESSONS_LEDGER` | `Docs/LESSONS.md` | Cross-cutting lessons (testing, tooling, process) that are not one pipeline's. |
| `LIVE_STATE` | `Docs/STATUS.md` | The one place that says what is in progress, next, blocked and waiting on the owner. A tracker replaces it if the project has one. |
| `ARCHIVE_DIR` | `Docs/Archive/` | Historical notes, kept for the record and indexed as historical. |
| `HISTORY` | `git` if the folder is under version control, else `Docs/_history/` | How earlier versions of a doc are kept. |
| `RULES_FILE` | The agent rules file the tools read every session (for example `CLAUDE.md` or `AGENTS.md`) | Points at the knowledge map; holds only standing rules. |
| `OWNER` | The person who started the project | Has the final say on vision and story. |
| `LEAD` | The main agent session | The one session that keeps the knowledge base: edits design docs, the map and the index. Other agents and helpers propose; they do not edit those. |

Beside this file:
- `templates/stores/`: one starter file per store, copied once at setup.
- `templates/new/`: `DESIGN_DOC.md` and `PLAYBOOK.md`, copied each time a new design doc or playbook is made.
- `templates/RULES_SNIPPET.md`: the lines to paste into the rules file (not copied into the knowledge root).
- `scripts/kb_check.sh`: the drift check, copied into the project at setup.

Fill-in placeholders in the templates are `<Project>`, `<owner>`, `<lead>`, `<date>` (today, as YYYY-MM-DD), `<rules file>` and `<check script>` (the project's copy of `kb_check.sh`). Text written `YYYY-MM-DD` inside a format line or example stays as it is.

## The stores

| Store | Holds | Writes | Rule |
|---|---|---|---|
| Knowledge map | The table of stores, "where do I put X", "where do I look for X", the session-start order, known gaps | `LEAD` | Short enough to read every session. If it grows past about two screens, move detail into the store it describes. |
| Decisions log | Dated one-line decisions grouped by area, each with who decided and where it came from | Whoever received the decision, the same session | Append only. A changed decision is a new line that says what it supersedes; the old line stays. |
| Doc index | One row per document: path, one-line purpose, status (`current`, `draft`, `historical`, `superseded by <path>`), last updated | Whoever writes, retires or supersedes a doc | Every doc under `KNOWLEDGE_ROOT` has a row. A doc with no row does not exist for the next session. |
| Project map | Locations by system: source files and their main types, asset folders, data tables, tools and how to run them, test suites, folders never to search | Whoever had to look for something | Add the location the moment you had to search for it. |
| Design docs | How one system works and why: goal, rules, numbers, open questions, change log | `LEAD` and `OWNER` edit; anyone proposes | Proposals and questions the lead can settle go into the doc's "Open questions and proposals" section, dated and signed; the lead folds agreed ones into the body and removes them, noting it in the change log. Questions only the owner can answer go to `LIVE_STATE`, not here. |
| Playbooks | The method for a repeatable kind of work (characters, levels, quests, audio, balance passes, releases): law, steps, checklists, brief template, lessons log | Builders append lessons; `LEAD` edits the rules | Made when a kind of work has been done twice the same way; an empty playbook folder is fine. Read at the start of any work of that kind. |
| Lessons ledger | One line per lesson not owned by a pipeline: date, what went wrong, the rule now | Whoever learned it | The rule also goes into the section of the ledger (or playbook) it belongs to, so the ledger is history and the sections are law. |
| Live state | In progress (who, what, last step), next up in order, blocked (on what), waiting on the owner (exact question) | Every session that starts or stops work | The only place state lives. No handoff note, chat, doc or memory holds a queue or a status. |
| Rules file | Standing rules for every agent, and the line "read the knowledge map first" | `OWNER`, or `LEAD` with the owner's dated agreement | Rules only. No status, no history. |
| Archive | Dated notes and superseded docs | Closed | Never the place to learn current truth; the index marks it historical. |
| Agent memory | One agent's private notes | That agent | A cache, not a store. Anything another session needs is copied into the decisions log or a doc. |

## Where to put what

| You have | It goes to | Then |
|---|---|---|
| A decision from the owner (chat, comment, playtest note) | One dated line in `DECISIONS_LOG` | Apply it the same session to every doc, brief or plan it changes; note it in `LIVE_STATE` if it unblocks work. |
| A design call the lead made without the owner | `DECISIONS_LOG`, marked "lead call, pending owner" | The owner confirms or overrides later; never block on it. |
| How a system works, or a change to it | That system's design doc | Its change-log line and its index row's date. |
| A file, asset, tool or setting you had to search for | `PROJECT_MAP` | Nothing else. |
| A lesson from building something | One line in the playbook's lessons log | If it changes the method, the lead moves it into the playbook's steps or law. |
| A lesson from testing, tooling or process | One line in the `LESSONS_LEDGER` ledger, plus the rule in the ledger section it belongs to | Read the ledger before writing tests or scripts. |
| A measured number (performance, feel, balance) | The design doc that owns the number, with how and when it was measured and where the evidence is | Other docs link to it instead of copying it. |
| Where your work stands when you stop | `LIVE_STATE` | Nothing else. |
| A new doc | A file in the right folder | An index row, and a map line if it is a new kind of store. |
| A doc that is replaced | Mark it `superseded by <path>` in the index and at its own top | Move it to `ARCHIVE_DIR` when nothing links to it any more. |
| A question only the owner can answer | `LIVE_STATE` "Waiting on the owner", one specific question each, and nowhere else | The affected design rule says "pending the owner". When answered, the answer becomes a decisions-log line and the question is removed. |
| A secret, password, key or personal detail | Nowhere in the knowledge base | It is meant to be readable and shareable. |

## Rules

1. **One home per fact.** A fact is written in one store; every other place links to it. Two copies drift and the next session believes the wrong one.
2. **Same session.** Knowledge is written down before the session that learned it ends. Chat and agent memory are not storage.
3. **Look up before deciding.** Before a design call, a brief or a change to a system, read that area's lines in the decisions log and that system's design doc. A call that contradicts a logged decision is either a new superseding decision (logged, with the reason) or a mistake.
4. **Decisions are applied at once.** An owner's answer is logged and folded into every affected doc and plan the same session, so nobody has to repeat it.
5. **Never rewrite history.** Decisions are superseded, not edited. Design docs keep a change log; earlier text is recoverable through `HISTORY` (commit before large edits, or copy the old version into the history folder with the date).
6. **Status is explicit.** Every doc is `current`, `draft`, `historical` or `superseded`, in the index and at its top. Old notes are never deleted for being old; they are marked and archived.
7. **Absolute dates and plain sentences.** "2026-03-04", never "yesterday". Write so a person, or a fresh agent with no context, can follow it.
8. **The lead keeps it, the review checks it.** Any change that alters how a system works (what a player, a tool or a teammate would see) is not finished until its design doc, the index and, if needed, the project map are updated. Reviewing work includes checking this.
9. **Small and true beats big and stale.** Prune the map, close known gaps, and archive what no longer applies. A short base everyone trusts is the goal.
10. **Shareable by default.** Keep secrets, credentials and personal details out, so any doc can be shown to a collaborator.

## Lead agent: every session, in order

1. The rules file, then `KNOWLEDGE_MAP` (if it changed since you last read it).
2. `LIVE_STATE`: what is in progress, what is next, what is waiting on the owner.
3. For the area you are about to touch: its decisions-log lines, its design doc and its playbook.
4. `PROJECT_MAP` for paths, instead of searching. Never search heavy generated folders (build output, caches, imported asset packs) that the map lists as off limits.
5. Do the work. Write each new fact to its store as it appears, not at the end.
6. Before stopping: update `LIVE_STATE`, add any decisions, lessons and locations from this session, and run the check. Fix what it reports; anything you cannot fix this session goes under "Known gaps" in the knowledge map, dated.

## Setting it up in a new project

1. Create `KNOWLEDGE_ROOT` with the folders `DESIGN_DIR`, `PLAYBOOK_DIR` and `ARCHIVE_DIR` inside it.
2. Copy every file in `templates/stores/` into `KNOWLEDGE_ROOT`, renaming any whose setting you changed. Replace the placeholders (`<Project>`, `<owner>`, `<lead>`, `<date>`, `<rules file>`, `<check script>`) in every copied file; afterwards a search for `<date>` should find nothing.
3. Copy `scripts/kb_check.sh` into the project's tools or scripts folder; its path is `<check script>`. The project then does not depend on where this skill is installed.
4. Paste the section from `templates/RULES_SNIPPET.md` into the rules file, with `<check script>` filled in, so every session starts at the map.
5. Write the first decisions: genre, platform, engine, camera, player count, art direction, scope limits, whatever the owner has already settled. One dated line each, under its area.
6. Write the project map's first rows: where source, assets, data, tools and tests live, and which folders are never searched.
7. For each system that already has rules, copy `templates/new/DESIGN_DOC.md` into `DESIGN_DIR` as `<System>.md`, fill it in and add its index row. Do the same with `PLAYBOOK.md` in `PLAYBOOK_DIR` for any kind of work that already has a method.
8. Run the check and fix what it reports.

## Adopting it in an existing project

1. Inventory every existing note, doc and readme. Classify each as current, historical or superseded; write its index row.
2. Move dated notes and handoff files into `ARCHIVE_DIR`, indexed as historical, after checking nothing still links to them only by their old path.
3. Read the existing docs, chats you have access to and the rules file for decisions; write each as a dated decisions-log line with its source. Mark any you are unsure of "to confirm with the owner".
4. Pull every stated location into the project map.
5. Make one live-state file; delete status sections from every other doc and point them at it.
6. Write the knowledge map last, from what you found, with a "known gaps" section for what is still missing.

## Checking for drift

Run `bash <check script> [KNOWLEDGE_ROOT]` (bash; works in Git Bash on Windows). Store paths that differ from the defaults are passed as environment variables named after the settings; `LIVE_STATE=none` when live state is kept in a tracker. It reports:
- the stores from the settings that are missing;
- docs under the root (outside the history folder) whose path relative to the index is not exactly an index link target or a backticked path;
- index links that point at files that do not exist;
- decisions-log list entries (`-`, `*` or `+`) that do not start with a valid YYYY-MM-DD date;
- design docs without a `Status:` line in their first 12 lines.

It exits non-zero when it finds a problem. Run it at the end of every lead session and before sharing the project. It checks shape, not truth: the review still asks whether each doc says what the game now does.

## Done when

A fresh agent given only the rules file can find, in under five minutes and without searching the project, what the game is, what has been decided in the area it will touch, what is in progress, where the relevant files are, and how that system works; and the check reports nothing.
