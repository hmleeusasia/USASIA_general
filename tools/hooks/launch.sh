#!/usr/bin/env bash
# Hook launcher (PLAN-lean-context-001-draft2 step 0).
# Usage in settings: bash "$CLAUDE_PROJECT_DIR/tools/hooks/launch.sh" <script.py>
# Picks the first working Python: python3 (cloud) -> py -> python (Windows).
# On Windows "python3" can be the Microsoft Store stub, so each candidate must run "-c ''".
# Fails open: no Python -> exit 0 (never blocks work).
DIR="$(cd "$(dirname "$0")" && pwd)"
S="$DIR/$1"
for p in python3 py python; do
  if command -v "$p" >/dev/null 2>&1 && "$p" -c "" >/dev/null 2>&1; then
    exec "$p" "$S"
  fi
done
exit 0
