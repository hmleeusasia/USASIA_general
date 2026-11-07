# ai-system-questions_closed (moved by tools/prune.py)

## 2026-11-04
| # | 고민 | 나온 날 | 지금 상태·제안 |
|---|---|---|---|
| Q3 | CURRENT_STATE를 공용(저장소 작업)과 개인(`users/<id>/state.md`)으로 나눌까? | 2026-11-03 | → D-20261103-8 (personal tasks moved to todo.md) |
| Q4 | 로컬도 main 직접 대신 브랜치에서 작업할까? (D-12 개정) | 2026-11-03 | → D-33 (main kept) |
| Q5 | git 이력의 예전 이메일 주소 정리(filter-repo + 강제 push + 재클론) | 2026-11-02 | → D-34 (done 11/03) |
| Q12 | Existing Korean docs → English: bulk convert now, or convert as each file is edited? Which first (skills, kb, CLAUDE.md)? Keep Korean synonyms in keywords.md for search? | 2026-11-03 | → D-33 (convert on edit) |

## 2026-11-06
| # | 고민 | 나온 날 | 지금 상태·제안 |
|---|---|---|---|
| Q19 | GLPI + master tables (usasia_db stores master, GLPI assets master, CSV import, STWS only tickets). Agreed Opus+Sonnet: docs/requests/PLAN-master-data-glpi-001-draft1.md | 2026-11-05 | Approved → D-20261105-11. Next: share with the team developer; GLPI details from the team |

## 2026-11-06
| # | 고민 | 나온 날 | 지금 상태·제안 |
|---|---|---|---|
| Q19 | **Per-account isolation when the repo is shared** (user concern 2026-11-06): no account may expose another person's private info, work or confidential items; one DB, but each account runs on its own. Draft plan (Opus, reviewed by Sonnet): (A) shared repo = team-public only (rules, skills, tools, general kb, orgs, shared decisions); shared docs never link into personal space; server-side check (CI), since local hooks don't run everywhere. (B) Personal space = **own Google Drive, synced folder via Drive for Desktop**, never shared, separate from the Claude folder (R-SEC-03); holds logs, todo, mail-triage results, notes about others. Company Workspace admins can still read it. Hooks/skills/CLAUDE.md log paths change in one place. (C) usasia_db is **SQLite** → no RLS: keep SQLite, owner_id + visibility (default private, explicit share) enforced in one Rails layer, per-user API token, no shared admin key, no direct DB file access; manager sees only rows shared to manager; limit sharing of the Drive backup folder. Audit log and confidential tags later. Order: (1) confirm DB engine choice (2) check GitHub repo visibility/collaborators (3) stop D-20261105-7 (docs/team work context) and move its rows (4) move personal files out, then **rewrite git history** (filter-repo, everyone re-clones) — before inviting anyone (5) update hook/skill paths (6) retire the shared Claude account for real work, turn on account detection (7) onboard teammates. Open: cloud sessions reach the personal space only via the Drive connector | 2026-11-06 | → D-20261106-5 (PLAN-access-layers-001-draft3) |
