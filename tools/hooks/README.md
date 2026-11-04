# tools/hooks — supervisor hooks
Plan: docs/requests/PLAN-lean-context-001-draft2.md. Per-rule mode: config.json (off/warn/block).

| File | Role |
|---|---|
| launch.sh | Picks working Python (python3 → py → python), skips the Windows Store stub, fails open |
| common.py | UTF-8 stdin/stdout, config, log, `context()` (warn), `block()` (exit 2) |
| probe.py | Step-0 probe: logs event/shell/Python to hits.log (gitignored) |

Register in settings: `bash "$CLAUDE_PROJECT_DIR/tools/hooks/launch.sh" <script.py>`.
While testing, hooks live in `.claude/settings.local.json` (personal); they move to shared `.claude/settings.json` only after review (Q2).

## Step-0 results (2026-11-03, local Windows)
| Check | Result |
|---|---|
| Python on Windows | `python3` = Microsoft Store stub (fails); `py` and `python` = 3.13. stdin default cp1252 → read bytes as UTF-8 (done in common.py) |
| Launcher manual run | OK with Korean JSON; picks `py`; additionalContext JSON printed |
| permissions.deny matching | **Prefix only.** `git push --force …` denied; `git push --dry-run --force …` and `git push … +main` NOT denied → deny is a soft net; a real guard needs a PreToolUse Bash regex script |
| Hooks added mid-session | Active right away (PostToolUse fired on the next Write, settings.local.json) |
| Hook shell (Claude Code) | Git Bash (MSYSTEM=UCRT64) + `py` → `bash launch.sh` command works. PostToolUse input keys: cwd, tool_input, tool_name, tool_response, session_id, transcript_path, permission_mode … |
| Stop (normal turn end) | Fires every turn end, stop_hook_active=False; input has last_assistant_message, background_tasks |
| Stop on user interrupt | **Does not fire** (Esc during a tool call, no log line) → Stop checks are skipped when the user interrupts; pre-commit stays the backstop |
| Cloud session | pending |
