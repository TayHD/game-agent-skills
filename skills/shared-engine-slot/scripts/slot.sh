#!/usr/bin/env bash
# Shared engine slot helper. Usage:
#   slot.sh status
#   slot.sh take "<holder>"      create-if-absent; honours the reservation file
#   slot.sh release "<holder>"   only deletes a lock that names <holder>
# Settings (environment): LOCK_FILE, NEXT_FILE (both required).
set -u
: "${LOCK_FILE:?set LOCK_FILE}"; : "${NEXT_FILE:?set NEXT_FILE}"
cmd=${1:-status}; holder=${2:-}
case "$cmd" in
  status)
    printf 'lock: %s\n' "$( [ -f "$LOCK_FILE" ] && cat "$LOCK_FILE" || echo '(free)')"
    printf 'next: %s\n' "$( [ -s "$NEXT_FILE" ] && cat "$NEXT_FILE" || echo '(none)')" ;;
  take)
    [ -n "$holder" ] || { echo 'holder required' >&2; exit 2; }
    if [ -s "$NEXT_FILE" ] && [ "$(cat "$NEXT_FILE")" != "$holder" ]; then
      echo "BUSY: reserved for $(cat "$NEXT_FILE")"; exit 1; fi
    if ( set -o noclobber; printf '%s' "$holder" > "$LOCK_FILE" ) 2>/dev/null; then
      [ "$(cat "$LOCK_FILE")" = "$holder" ] || { echo 'LOST RACE'; exit 1; }
      [ -f "$NEXT_FILE" ] && [ "$(cat "$NEXT_FILE")" = "$holder" ] && rm -f -- "$NEXT_FILE"
      echo "TAKEN by $holder"
    else
      echo "BUSY: held by $(cat "$LOCK_FILE")"; exit 1
    fi ;;
  release)
    [ -n "$holder" ] || { echo 'holder required' >&2; exit 2; }
    if [ -f "$LOCK_FILE" ] && [ "$(cat "$LOCK_FILE")" = "$holder" ]; then
      rm -f -- "$LOCK_FILE"; echo "RELEASED by $holder"
    else
      echo "REFUSED: lock is not held by $holder"; exit 1
    fi ;;
  *) echo "unknown command: $cmd" >&2; exit 2 ;;
esac
