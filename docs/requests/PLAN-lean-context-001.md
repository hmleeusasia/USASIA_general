# PLAN-lean-context-001 (draft, 2026-11-03)
Goal: keep always-loaded md files minimal and keep the working context small. Rules are **enforced by hooks**, not by re-reading md. Related: ai-system-questions Q10, Q14.

## 1. Measured now (2026-11-03)
| Loaded when | Files | Size (chars) |
|---|---|---|
| Every session (auto) | CLAUDE.md + personal CLAUDE.md + MEMORY.md | ~5,000 |
| Session start (read by rule) | CURRENT_STATE 3.5k, facts 1.3k, project_instructions 3.7k | ~8,500 |
| start-day extra | todo.md 6.5k, mail_triage 2.5k, orgs, skills (start-day + mail-triage + todo-sync ~7.4k) | ~18,000 |
| Task work (biggest cost) | Browser screenshots per scroll, long read_page trees | 10k–50k+ per task |
→ About 30k chars go in before any real work starts. Browser output is the largest variable cost.

## 2. Three layers
| Layer | What goes here | Limit |
|---|---|---|
| L0 always loaded | CLAUDE.md: pointers + rules that need **judgment** only (ask about new contacts, conclusion first, confirm before sending) | ≤ 40 lines |
| L1 on demand | skills (per task), kb/*, decisions.md, CURRENT_STATE detail | skill ≤ 80 lines; read only when the task needs it |
| L2 enforced | Rules a script can check → hooks. md keeps one line: "enforced by hook <name>" | — |

**Rule intake (every new rule):** Can a script check it? → yes: hook + 1 line. → no, task-specific: put it in that skill. → no, global judgment: CLAUDE.md (and remove an old line if over the limit).

## 3. Hooks (`.claude/settings.json`, Python in `tools/hooks/`)
| Hook | Checks | On violation |
|---|---|---|
| SessionStart | Runs `tools/digest.py`: last start date, overdue/due-in-7-days, open count, H-sheet count, branch/uncommitted state → **~10 lines** injected | Replaces reading full CURRENT_STATE + facts at start |
| PreToolUse Write/Edit | Sensitive values (email, phone, account/circuit ID, password-like); log path/name `docs/log/YYYY/YYYY-MM-DD_<id>.md`; writes to `users/` need known user; new repo text in English | Block (exit 2) with reason → Claude fixes and retries |
| PostToolUse Write/Edit | `check.py --file <path>`: unregistered tags, hub missing, line budgets (CLAUDE.md 40, CURRENT_STATE 80, facts 50, skill 80) | Feedback to Claude to fix now |
| PreToolUse Bash | `git push --force`, push to non-main without request, `rm -rf` on docs | Block |
| Stop | Uncommitted changes; CURRENT_STATE over budget; new #open entries not in C section | Block stop once with checklist (replaces most of session-end md reading) |
Rollout: 2 weeks **warn only** (log hits to `tools/hooks/hits.log`, no secrets), tune false positives (e.g. the word "password" alone), then switch to block.

## 4. Working-context rules (put in skills, not CLAUDE.md)
- Browser: summarize in page JS (`javascript_tool` returns ≤ ~1k chars per call; split into batches); avoid `computer scroll` (returns a screenshot each time) — scroll by JS. Screenshots only when text fails, scale ≤ 0.6.
- Bulk reads → subagent, return a table only. Results go to a file, chat gets the conclusion.
- Read long files by section (`find.py`, grep), not whole. todo.md: read the "Now" section only unless syncing.
- CURRENT_STATE: overwrite, never append history; closed items leave the same day.
- Auto-memory (MEMORY.md): only facts not in the repo; ≤ 15 lines; consolidate monthly.

## 5. Steps
| # | Step | Size |
|---|---|---|
| 1 | `check.py --file` mode + hook JSON input/exit codes | heavy |
| 2 | `tools/digest.py` + SessionStart hook; change CLAUDE.md "session start" to "read digest; open files only when needed" | medium |
| 3 | PreToolUse sensitive/path guard (warn mode) | medium |
| 4 | Stop hook checklist; shorten session-end skill | medium |
| 5 | Trim CLAUDE.md to ≤ 40 lines (move tables to docs/skills.md / kb INDEX) | light |
| 6 | Browser/context rules into start-day, mail-triage, drive-index skills | light |
| 7 | After 2 weeks: review hits.log, switch to block, measure start-of-session size again | light |

## 6. Open questions
- Who approves shared hook changes (same as Q2)?
- Hooks in shared `settings.json` apply to every teammate — personal extra checks go in `settings.local.json`.
- Cloud sessions: hooks run there too only if Python is available (it is); Windows uses `py`.
