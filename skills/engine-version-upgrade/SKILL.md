---
name: engine-version-upgrade
description: Move an Unreal Engine source-build project to a new engine version - inventory, port and commit engine patches, snapshot, one engine-root setting, build every target, re-baseline tests, verify saves, package, then cut over and leave the knowledge behind. Use when planning or executing an engine upgrade or a move between engine previews and releases.
metadata:
  version: "0.1.1"
  updated: "2026-11-15"
---

# Engine version upgrade

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `ENGINE_ROOT_FILE` | The one file that names the engine root, plus its readers for each script language. |
| `ENGINE_CHECKOUT` | The engine source checkout and the local branch that carries project patches. |
| `TARGETS` | Every build target and configuration the project ships (editor, server, client). |
| `SUITES` | The automation suites and network runs that form the test baseline. |
| `SNAPSHOT_DIR` | Where the pre-upgrade project copy goes, outside the project tree. |
| `SLOT_RULES` | The exclusive engine slot (see `shared-engine-slot`). |
| `SHIP_GATE` | Modules that must never appear in a shipping receipt. |

## Method

1. **Inventory (offline).** Every engine-side change and its diff base; every plugin the project ships or depends on with a support note for the new version; engine APIs the code leans on that may be deprecated; every script and kit that names an engine path.
2. **Patches on a branch.** Commit the project's engine patches to a local branch on top of the new version's tag (never pushed), so the next point release is a rebase. Compare the commit with the patch files and report anything in one but not the other.
3. **One engine root.** Put the root in `ENGINE_ROOT_FILE` and make every live tool, script and kit template read it. In-flight kits are not path-swapped mid-flight; they repoint and re-baseline before their next run.
4. **Snapshot** Content, Config, Source and Plugins to `SNAPSHOT_DIR` before the first save under the new version, and verify file counts and bytes.
5. **Build in two steps,** so a red is never ambiguous:
   - 1a: build every `TARGETS` entry and run `SUITES` with no new plugins enabled; classify every red as inherited (identical to the old baseline), pre-existing, harness or new.
   - 1b: enable new editor plugins or toolsets, rebuild the editor, re-smoke.
6. **Save the new baseline:** every log of step 5 becomes the comparison baseline for the new version.
7. **Editor checks:** Blueprint compile audit, a map check, start time and RAM on the largest map, a network test, and a **save round-trip on scratch copies** (a Blueprint, a data table, an animation asset, a map: duplicate, save, reload after restart, cook) before any real asset is saved.
8. **Package** every shipping target, boot the server, connect a client, and run `SHIP_GATE` on the receipts.
9. **Cut over:** update the project map, the agent rules, the role cards, the test lessons and the index; record each phase's outcome with evidence; then retire the old engine (after confirming nothing still points at it or lives only in its folder) and remove the snapshot once the first real save on the new version has reloaded cleanly.

## Traps seen in practice

- New versions can change build conventions silently (for example which module subfolders get header generation); read the first compile error as a convention change before patching code.
- A commandlet used as a "harmless" probe can write content.
- A per-run profile folder can reinstall gigabytes of Python packages; share one install.
- Plugins can become default-on and carry runtime modules; pin them to the editor target explicitly and gate the shipping receipts.
- The old engine folder may hold data that is not engine (exports, tests, scenes); check before deleting it.
- A source-built engine can lack files that the engine repository ignores but the automation tool still needs (for example small resource images for a platform project the tool compiles). The first package run then fails within seconds while compiling the tool. Read the first compile error for a missing file, copy the files in from an engine build that has them, and record them, because they exist only in that tree and a fresh checkout needs them again.
- New editor plugins can add their own folders to every cook without checking the target platform, which fails server and client cooks on editor-only classes. Exclude that content from the cook (a never-cook directory) and note when to remove the exclusion.
- Gate shipping builds on the exact names of the plugins that must not ship, never on a bare word: stock engine modules often share a word with the agent plugins and are expected in every build.
- A shipping client may ignore command-line travel URLs and exec commands by design. Run the unattended join check with a development client and the project's isolated test switches (including any authentication bypass the server honours only in test mode), and take a clean shipping boot to the menu as the shipping client's proof.

## Done when

Every target builds, the suites run with every red classified, the save round-trip and package smoke pass, the docs point only at the new engine, and the old engine is retired on evidence.
