# PLAN-lean-context-001-draft2 (agreed Opus + Sonnet, 2026-11-03 — awaiting user approval)
draft1 → docs/requests/archive/. Related: ai-system-questions Q10, Q14, Q2.

## Principle (user, 2026-11-03)
Let Claude work freely; a **supervisor (hooks)** watches actions and stops it only when work drifts, stating the one rule broken. md = *how to be* (judgment rules); hooks = *what not to do* (checkable). Hooks see file writes, commands and turn ends — not chat replies or judgment.

## 1. Measured (2026-11-03)
Always loaded ~5k chars (CLAUDE.md 4.4k). Session start reads ~8.5k more; start-day ~18k more. **Browser output is the largest cost (10–50k per task).** So: browser/context rules first, hooks are mainly for enforcement, md trimming second.

## 2. Layers and budgets (chars, ratchet = warn only when an edit grows a file past its budget)
| Layer | Content | Budget |
|---|---|---|
| L0 always | CLAUDE.md: pointers + judgment rules | ~3,000 chars (question table → docs/skills.md / kb INDEX, 1-line pointer) |
| L0 personal | users/<id>/CLAUDE.md, MEMORY.md | counted separately; MEMORY ≤ 15 lines |
| L1 on demand | skills, kb, decisions, CURRENT_STATE detail | skill ~80 lines |
| L2 enforced | checkable rules → hook / pre-commit; md keeps 1 line "enforced by <rule ID>" | — |
Rule intake: checkable → hook; task-specific → that skill; global judgment → CLAUDE.md (remove a line if over budget).

## 3. Supervisor parts
| Part | Does | Mode |
|---|---|---|
| SessionStart (startup, compact, resume) | `tools/digest.py` → ~10 lines: user ID (git user → users/INDEX.md), local/cloud, last start-day, overdue IDs, due ≤7 days, open count, H-sheet count, section F trap one-liners, branch/uncommitted/ahead-behind (no fetch), "open on demand" pointer | always on |
| PreToolUse Write/Edit/MultiEdit | Scans **new text only** (content / new_string), reuses check.py SKIP list. **Block:** email addresses, secret-shaped tokens; log path/name `docs/log/YYYY/YYYY-MM-DD_<id>.md`; writes to users/ when user unknown. **Warn:** $ amounts, IPs, the word password/비밀번호 | per rule |
| English nudge | Warn only, never block, once per file per session. New text ≥ 200 letters, Hangul/(Hangul+Latin) > 30%, excluding code spans, parenthesized names, find.py keywords (확인일·기한). Paths: docs/{log,kb,requests}, decisions.md, .claude/skills | warn |
| PostToolUse | `check.py --file`: unregistered tags, char budgets (ratchet) | warn → feedback |
| Stop (narrow) | Only for files touched this turn: CURRENT_STATE over budget, new #open not in section C. **Exit 0 when stop_hook_active.** No "uncommitted" check (session-end skill does it) | block once |
| permissions.deny | `git push --force*`, `git push -f*`, `--force-with-lease`, `+` refspecs, `rm -rf docs*` (soft net; test matching) | deny |
| git pre-commit | check.py on staged files incl. hub-missing; backstop for sed/redirect/Python writes and teammates | block |

Common rules for all hooks: one launcher (`python3` if it works, else `py`; Windows shell verified in step 0); read stdin as UTF-8 bytes, reconfigure stdout/stderr UTF-8, normalize backslashes; wrap in try/except and **fail open**; exit 2 = block (map check.py's 1 → 2); block message = rule ID + offending line + fix; after a sensitive-value block Claude **asks the user**, no retry loop; per-rule mode (off/warn/block) in one config `tools/hooks/config.json`; warn mode returns additionalContext (exit-0 stderr is not shown); hits go to gitignored `tools/hooks/hits.log` (no secret values).

## 4. Working-context rules (into skills, not CLAUDE.md)
Browser: summarize in page JS (~1k chars per call, batch calls); scroll by JS, not `computer scroll` (returns a screenshot); screenshots only when text fails, scale ≤ 0.6. Bulk reads → subagent, table back; results to files, chat gets the conclusion. Read files by section; todo.md "Now" only unless syncing. CURRENT_STATE overwritten, closed items leave same day.

## 5. Steps
| # | Step | Size |
|---|---|---|
| 0 | Verify hook shell on Windows + cloud; Stop on interrupt; deny matching. Write launcher + config.json | light |
| 1 | Browser/context rules into start-day, mail-triage, drive-index skills | light |
| 2 | Cut project_instructions.md to repo-relevant parts | light |
| 3 | digest.py + SessionStart (incl. user ID resolution) | medium |
| 4 | check.py `--file`/`--new-text` + PreToolUse (warn) + pre-commit + test_hooks.py fixtures | heavy |
| 5 | Narrow Stop hook; shorten session-end | medium |
| 6 | Trim CLAUDE.md to ~3,000 chars (move question table) | light |
| 7 | Flip rules to block one by one, only when test_hooks.py green and hits.log shows no false positives | light, ongoing |

## 6. Open
- Who approves shared hook changes — hook scripts run on teammates' PCs, so changes = reviewed code (Q2).
- Hook changes need Claude Code restart or hooks review; document in onboarding.
- Settle by test in step 0: Stop on user interrupt, Windows hook shell, deny matching.
