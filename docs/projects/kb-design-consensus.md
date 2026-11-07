# Knowledge / project framework — consensus draft (Q21, Q22)

2026-11-07 brainstorm, reviewed by a Sonnet critic (one round). Status: **draft, not adopted**; apply later in one batch (user). Sources: dev-knowledge-research.md, knowledge-fields-research.md.

## Storage principle (user 2026-11-07, supersedes the Markdown-import compromise below)
| Place | Holds |
|---|---|
| GitHub wiki repo | Rules, skills, hooks, templates, principles, design docs, procedures |
| GitHub code repos | Code, tests, migrations, build journal |
| **usasia_db (SQL, source of truth)** | **All records**: work log, todos, project status/milestones, lessons, risks, decisions, KB, org/contact index (no sensitive values) |
| GLPI | Raw data: assets, tickets |
| Drive | Original documents, sensitive values |

- Decisions: the decision record lives in the DB; only the resulting rule text goes into md.
- Current Markdown records (log, todo, projects, kb) move to the DB in phases; this solves most of Q20.
- Claude reads and writes records through the DB API; `kb-find` = SQL search.
- R-SEC applies to the DB the same way (no passwords, accounts, circuit IDs).
- Open: fallback when the DB is down (read-only export snapshot? write queue?).

## Accepted from review
| # | Change | Severity |
|---|---|---|
| 1 | One home per record: every record (project status, lessons, risks, ADR, KB) only in usasia_db; the wiki keeps no record copies (lessons.md/risks.md dropped) | high |
| 3 | Collision-free IDs across repos and sessions (Q20): `<prefix>-<yyyymmdd>-<user>-<n>` or script-generated; duplicate check in CI | high |
| 4 | Define the read path first: generated INDEX (id, title, type, scope, state, keywords), store hub pages that only link, skill `kb-find` (validated first); task announcement step "search KB for scope + keywords" | high |
| 5 | Security in code repos is enforced by repo mechanisms, not CLAUDE.md text: secret scan (pre-commit + CI), push protection, CODEOWNERS, main protection. repo-onboard installs these | high |
| 6 | New R-SEC rule: knowledge records follow R-SEC-01/02; `restricted` records hold only a Drive link; POS/payment and PCI evidence stay in Drive; ingest uses read-only, scoped tokens; sens-* hooks extended to usasia_db | high |
| 7 | Required fields only: id, type, scope, state, owner, last_verified, sources. Others optional. reuse_count derived by script from log/commit references | med |
| 9 | No call-graph generation at first; docstrings + ARCHITECTURE + lockfiles. Add an ast index when a repo grows past ~5k lines | med |
| 10 | GLPI link = GLPI ID + stable human key (store code + asset tag); monthly read-only API check for dangling IDs; GLPI KB module unused | med |
| 11 | Validation: draft → validated after a field use or a second person; session-end proposes, user approves; weekly review lists ≤ 5 overdue | med |
| 12 | usasia_db unavailable → never blocks work: log entry tagged `#kb-pending`, synced later; reads fall back to the INDEX cached in the wiki | med |
| 13 | Migration of pos_tips.md / kb: subagent pass, each tip → draft record; old file becomes a stub for one month | med |
| 14 | One developer onboarding page + `kb new lesson` helper | low |
| 15 | Commit trailers optional (warn, never block); lesson links to commit hash | low |

## Adjusted (Claude rebuttal)
- **#2 "wiki-only knowledge folder first"** — rejected: all records live in usasia_db (SQL), see Storage principle. (An earlier Markdown-import compromise was withdrawn.)
- **#8 "types are only tags"** — kept the user's 5 types, but one README template with optional sections switched on by type, not 5 templates.
- **#5 correction to the earlier chat answer**: a sibling repo's CLAUDE.md loads only when it is the working directory or added to a cloud session via add_repo (local `--add-dir` does not load it by default). So the "secondary repo" header is a convenience, not a safety control.

## Rollout
1. Phase 1: ID scheme (Q20), project README template + todo-vs-project rule, migrate granite-dia / ai-system, minimal record template, INDEX + kb-find, R-SEC additions.
2. Phase 2: KB schema in usasia_db + Markdown import, pos_tips migration, session-end drafts, validation and stale review, GLPI ID check, start-day milestones.
3. Phase 3 (when a dev repo is active): repo-onboard with secret-scan hooks and CI, ADR in code repos, optional trailers, scoped-token ingest, ast index if needed.

## Open for the user
- **On hold**: network field design from real Drive docs (network tables, ISP sheets, Tacoma request form, survey sample). Cloud session 2026-11-07 could not open work Drive files (connector account has no access, even by direct link) → retry from a local PC session; read structure (tabs, headers) only, no values (R-SEC)
- DB-down fallback method
- Migration order of existing Markdown records
- Who may set `validated` besides the owner?
- Phase 1 start date.
