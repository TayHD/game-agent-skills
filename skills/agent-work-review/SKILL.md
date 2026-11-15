---
name: agent-work-review
description: Review an AI worker's finished change by reading the real diff, backups and evidence rather than its report; run the third-attempt review before a third try; and ask the process question after every result. Use when approving or rejecting agent work, closing a ticket, or deciding whether another hold or retry may run.
metadata:
  version: "0.1.1"
  updated: "2026-11-15"
---

# Reviewing agent work

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `BACKUP_DIR` | Originals to diff against. |
| `EVIDENCE_DIR` | Logs, captures and verdicts. |
| `RULES` | The project rules and the brief's constraints. |
| `PLAYTEST_LIST` | Where look, feel and sound checks for the owner are collected. |

## Every review

1. **Read the real change:** diff every changed file against its backup. A file changed with no backup is a finding.
2. **Check the brief's constraints were kept** (with no written brief, judge against the task statement and say so): files only in scope, live edits only under the slot, imported art untouched, retired paths not patched.
3. **Check every claim has evidence:** each "built", "passed", "measured" or "looks right" has a path you open yourself. An exit code is not a verdict. Tests use real entry points. Matching pass counts with different output is a claim to correct, not a pass: say what differs.
4. **Check the knowledge was left behind:** the system doc, the project map and the index were updated where the change altered how a system works. A change alters how a system works when a user of it (a worker, a script, a player) would see different behaviour, output or rules.
5. **Grade each finding:** blocking when it breaks correctness, safety, data or a stated rule, or when a claim lacks evidence; advisory otherwise. Only blocking findings stop an approval.
6. **Decide:** approve and close with a one-line note, or request changes as a numbered list of exactly what must change. Feel, look and sound are not gates: close on evidence and add the item to `PLAYTEST_LIST`.
7. **Ask the process question** and write the answer as one line: "Is this process efficient? If not, how do we improve it?" Two reds on one item, or a run over 45 minutes, cannot be answered "fine" without a reason.

## Third-attempt review

Before any third attempt on one item (counting every red and every kit stop), the reviewer reads, personally:
1. every stage gate replayed offline against the baseline and the last run's evidence, passing known-good and flagging a planted bad row;
2. every builder's real save path replayed against saved dumps, not only its dry run;
3. every fixture input checked against the files it depends on (versions, schema numbers, paths, profile names);
4. a diff of the kit since the last attempt, and nothing else in it;
5. the stage list trimmed to owned gates.
Then sign the read. A bounded worker's item moves to a stronger worker at this point.

## Escalation

- Past two review rounds, or submitted with tests not run: re-route to a stronger worker with a sharper brief.
- Three rounds on one item: raise the sticking point with the owner.
- For a top-priority or hard review, get an unanchored second read from a fresh reviewer given the code, not your conclusion.

## Done when

You could defend the verdict from the files alone, and the process line is written.
