# Lines to add to the agent rules file

Paste the section below into the rules file your agent tools read every session (for example `CLAUDE.md` or `AGENTS.md`). Replace `<check script>` with the path of the project's copy of `kb_check.sh`, and change the `Docs/` paths if your settings differ.

---

## Project knowledge (read first)

- **Start every session at `Docs/KNOWLEDGE.md`.** It says where every kind of knowledge lives. Then read `Docs/STATUS.md`, and for the area you will touch, its lines in `Docs/DECISIONS.md`, its design doc and its playbook.
- **Look up before deciding.** Check the decisions log and the design doc before any design call or change. A call that contradicts a logged decision needs a new, dated decision line with the reason.
- **Write it down the same session.** Decisions go to `Docs/DECISIONS.md` (dated, append only); locations you had to search for go to `Docs/PROJECT_MAP.md`; lessons go to the pipeline's playbook or `Docs/LESSONS.md`; changes to how a system works go to its design doc and `Docs/INDEX.md`. Chat and agent memory are not storage.
- **One live state.** What is in progress, next, blocked or waiting on the owner lives only in `Docs/STATUS.md`. Update it when you start and stop.
- **One home per fact.** Link to a fact instead of copying it.
- **Before stopping,** run `bash <check script> Docs` and fix what it reports. Anything you cannot fix this session goes under "Known gaps" in `Docs/KNOWLEDGE.md`, dated.
