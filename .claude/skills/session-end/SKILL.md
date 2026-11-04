---
name: session-end
description: Session wrap-up and handoff. Every session — check.py, open items to the todo board, new facts/decisions, commit and push. Weekly (Monday meeting day, or when asked) — full review incl. framework-change and inefficiency tables. Use for "마무리", "인계", "세션 종료", "세션 닫기", "주간 점검".
---

# Session end (session-end)

## A. Every session (light — keep it short)
1. `python3 tools/repo_map.py` (refreshes docs/ARCHITECTURE.md snapshot), then `python3 tools/check.py` passes (Stop hook already blocks: CURRENT_STATE > 80 lines, open T-IDs missing from the board — tools/hooks/stop.py)
2. Open items (#open/#waiting) → docs/users/<id>/todo.md (personal work); CURRENT_STATE C holds repo/framework items only, changed sections only. New lasting fact → kb/facts.md (with date); new hard-to-reverse decision → decisions.md; new org → kb/orgs.md
3. Report in a few lines: what was done, what is left or unverified. **No framework-change or inefficiency tables here** — note friction as one line in docs/projects/ai-system-questions.md instead
4. Commit → push by work place: local `git pull --rebase origin main` then `git push origin main`; cloud: push the claude/* branch, then `git fetch origin main && git checkout -B main origin/main && git merge --ff-only <branch> && git push origin main` (stop and tell the user if not fast-forward)

## B. Weekly (Monday, with weekly-meeting, or when the user asks)
1. `python3 tools/find.py --open` (overdue) and `--due` (30 days); CURRENT_STATE ≤ 80 lines, kb/facts.md ≤ 50 lines
2. If structure, data flow or principles changed this week: update the hand-written diagrams in docs/ARCHITECTURE.md. INDEX files match real files (missing entries, dead links); kb docs and skills created this week are in kb/INDEX.md
3. Tags outside keywords.md or duplicate meanings; anything that must not be in GitHub (storage_rules.md)
4. Local session only: Drive Claude folder shared with 0 people — get_file_permissions (folder ID: docs/drive-index/claude-folder.md)
   - Cloud session with Sheets connector: apply rows of 90_변경대기_* batch files without the `완료_` prefix to target sheets → copy to 90_변경대기 with status '완료' and date → rename batch with `완료_` → update CURRENT_STATE H-sheet (D-20261102-17)
5. Review ai-system-questions.md friction lines from the week, then report (one message):
   - Framework-change table (what · why · files) — evidence such as repeated tag combos, a target with no hub mentioned twice or more, ambiguous classifications, an oversized file. "None" if none. Change nothing before approval
   - Inefficiency table: | waste | cause | fix | where | status (committed / needs approval) | — look at repeated manual work, model choice for subagents, question round-trips, large reads
   - Ask about each "needs approval" item one at a time; apply only approved ones
6. Quarterly: remind the user to delete leftover claude/* remote branches in GitHub web (D-20261102-7). Only when docs/log has 60+ files: monthly summaries (docs/log/YYYY/YYYY-MM-summary.md, 10–20 lines, one "### title  #tags" line per item + decision IDs, no #open/#waiting) → move originals to docs/archive/YYYY/
