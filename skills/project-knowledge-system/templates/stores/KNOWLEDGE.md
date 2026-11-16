# <Project> knowledge map

Status: current. Owner: <owner>. Kept by: <lead>. Last updated: <date>.

**This page is the entry point.** Read it at the start of every session. If you learn something another session will need, it goes into one of the stores below before your session ends. Chat and agent memory are not storage.

## 1. The stores

| Store | What lives there | Who writes | How to add |
|---|---|---|---|
| `Docs/DECISIONS.md` | Every standing decision, dated, one line each, by area | Whoever received it, the same session | Append a dated line; supersede, never rewrite |
| `Docs/INDEX.md` | Every document with its status | Whoever writes or retires a doc | Add or change its row |
| `Docs/PROJECT_MAP.md` | Where code, assets, data, tools and tests are | Whoever had to search | Add the location when you find it |
| `Docs/Design/` | One living design doc per system | Lead and owner edit; anyone proposes | Proposals in the doc's "Open questions and proposals" section |
| `Docs/Playbooks/` | One method per pipeline, with a lessons log | Builders add lessons; lead edits rules | Append to the lessons log |
| `Docs/LESSONS.md` | Lessons that are not one pipeline's | Whoever learned it | One ledger line plus the rule in its section |
| `Docs/STATUS.md` | In progress, next, blocked, waiting on the owner | Every session that starts or stops work | Edit in place; the only place state lives |
| `Docs/Archive/` | Historical notes and superseded docs | Closed | Move retired docs here once nothing links to them |
| `<rules file>` | Standing rules for every agent | Owner, or lead with the owner's dated agreement | Rules only |

## 2. Where do I put X

| You have | It goes to |
|---|---|
| A decision from the owner | `Docs/DECISIONS.md`, then apply it to every affected doc the same session |
| A design call made without the owner | `Docs/DECISIONS.md`, marked "lead call, pending owner" |
| How a system works, or a change to it | Its design doc in `Docs/Design/`, with a change-log line |
| A location you had to search for | `Docs/PROJECT_MAP.md` |
| A lesson from building something | That pipeline's playbook lessons log |
| A lesson from testing, tooling or process | `Docs/LESSONS.md` |
| A measured number | The design doc that owns it, with method, date and evidence path |
| Where your work stands when you stop | `Docs/STATUS.md` |
| A question for the owner | `Docs/STATUS.md`, "Waiting on the owner" |

## 3. Where do I look for X

| You need | Look in |
|---|---|
| What to do now | `Docs/STATUS.md` |
| What was decided about something | `Docs/DECISIONS.md`, that area's section |
| How a system works | `Docs/INDEX.md` for its design doc |
| Where a file, asset or tool is | `Docs/PROJECT_MAP.md` |
| How to make something in a pipeline | `Docs/Playbooks/` |
| How something got this way | The design doc's change log, then the archive rows in the index |

## 4. Session start, in order

1. The rules file, then this map if it changed.
2. `Docs/STATUS.md`.
3. For the area you will touch: its lines in `Docs/DECISIONS.md`, its design doc, its playbook.
4. `Docs/PROJECT_MAP.md` for paths. Never search the folders it lists as off limits.
5. Before stopping: update `Docs/STATUS.md`, write down this session's decisions, lessons and locations, run the drift check.

## 5. Known gaps

- <What is not written down yet, dated. Remove a line when it is closed.>
