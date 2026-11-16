#!/usr/bin/env bash
# kb_check.sh: drift check for a project knowledge base (project-knowledge-system skill).
#
# Usage: bash kb_check.sh [KNOWLEDGE_ROOT]        (default: Docs)
# Store paths can be overridden with environment variables:
#   KNOWLEDGE_MAP DECISIONS_LOG DOC_INDEX PROJECT_MAP LESSONS_LEDGER LIVE_STATE DESIGN_DIR HISTORY_DIR
# Set LIVE_STATE=none if live state is kept in a tracker instead of a file.
#
# Reports: missing stores, docs with no index row, index links to missing files,
# decisions-log entries without a date, design docs without a status line.
# Exits 0 when clean, 1 when it found a problem, 2 on bad usage.

set -u

ROOT="${1:-Docs}"
ROOT="${ROOT%/}"
if [ ! -d "$ROOT" ]; then
  echo "kb_check: knowledge root '$ROOT' is not a folder" >&2
  exit 2
fi

KNOWLEDGE_MAP="${KNOWLEDGE_MAP:-$ROOT/KNOWLEDGE.md}"
DECISIONS_LOG="${DECISIONS_LOG:-$ROOT/DECISIONS.md}"
DOC_INDEX="${DOC_INDEX:-$ROOT/INDEX.md}"
PROJECT_MAP="${PROJECT_MAP:-$ROOT/PROJECT_MAP.md}"
LESSONS_LEDGER="${LESSONS_LEDGER:-$ROOT/LESSONS.md}"
LIVE_STATE="${LIVE_STATE:-$ROOT/STATUS.md}"
DESIGN_DIR="${DESIGN_DIR:-$ROOT/Design}"
HISTORY_DIR="${HISTORY_DIR:-$ROOT/_history}"

problems=0
report() { echo "  $1"; problems=$((problems + 1)); }

# 1. Missing stores
echo "Stores:"
missing_before=$problems
for store in "$KNOWLEDGE_MAP" "$DECISIONS_LOG" "$DOC_INDEX" "$PROJECT_MAP" "$LESSONS_LEDGER" "$LIVE_STATE"; do
  [ "$store" = "none" ] && continue
  [ -f "$store" ] || report "missing: $store"
done
[ $problems -eq $missing_before ] && echo "  all present"

# 2. Docs with no index row
echo "Docs with no index row:"
before=$problems
if [ -f "$DOC_INDEX" ]; then
  index_dir="$(dirname "$DOC_INDEX")"
  # Every link target and backticked path in the index, without anchors or a leading ./
  indexed="$(sed 's/\r$//' "$DOC_INDEX" | {
      grep -oE '\]\([^)]+\)|`[^`]+`' || true
    } | sed -E -e 's/^\]\((.*)\)$/\1/' -e 's/^`(.*)`$/\1/' -e 's/#.*$//' -e 's#^\./##')"
  while IFS= read -r doc; do
    case "$doc" in "$HISTORY_DIR"/*) continue ;; esac
    rel="${doc#"$index_dir"/}"
    # Accept the path relative to the index, or the path as written from the project root.
    if ! printf '%s\n' "$indexed" | grep -qxF -- "$rel" \
       && ! printf '%s\n' "$indexed" | grep -qxF -- "$doc"; then
      report "$doc"
    fi
  done < <(find "$ROOT" -type f -name '*.md' | sort)
else
  report "no index to check against"
fi
[ $problems -eq $before ] && echo "  none"

# 3. Index links to files that do not exist
echo "Index links to missing files:"
before=$problems
if [ -f "$DOC_INDEX" ]; then
  index_dir="$(dirname "$DOC_INDEX")"
  while IFS= read -r target; do
    target="${target%%#*}"
    [ -z "$target" ] && continue
    case "$target" in http://*|https://*|mailto:*) continue ;; esac
    if [ ! -e "$index_dir/$target" ] && [ ! -e "$target" ]; then
      report "$target"
    fi
  done < <(sed 's/\r$//' "$DOC_INDEX" | grep -oE '\]\([^)]+\)' | sed -E 's/^\]\((.*)\)$/\1/')
fi
[ $problems -eq $before ] && echo "  none"

# 4. Decisions-log entries without a date
echo "Decisions without a date:"
before=$problems
if [ -f "$DECISIONS_LOG" ]; then
  n=0
  while IFS= read -r line; do
    n=$((n + 1))
    case "$line" in
      "- "*|"* "*|"+ "*)
        if ! printf '%s\n' "$line" | grep -qE '^[-*+] [0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])([^0-9]|$)'; then
          report "line $n: $line"
        fi
        ;;
    esac
  done < <(sed 's/\r$//' "$DECISIONS_LOG")
fi
[ $problems -eq $before ] && echo "  none"

# 5. Design docs without a status line
echo "Design docs without a status line:"
before=$problems
if [ -d "$DESIGN_DIR" ]; then
  while IFS= read -r doc; do
    if ! head -n 12 "$doc" | sed 's/\r$//' | grep -qE '^(\*\*)?Status(\*\*)?:'; then
      report "$doc"
    fi
  done < <(find "$DESIGN_DIR" -type f -name '*.md' | sort)
fi
[ $problems -eq $before ] && echo "  none"

echo
if [ $problems -eq 0 ]; then
  echo "kb_check: clean"
  exit 0
fi
echo "kb_check: $problems problem(s)"
exit 1
