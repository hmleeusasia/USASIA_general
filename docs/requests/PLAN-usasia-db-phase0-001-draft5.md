# PLAN usasia-db-phase0-001 draft5 — phase 0 + access layers stage 1 + migration readiness
Status: draft5 (2026-11-06), agreed after 2 fresh-Sonnet rounds (round 1: 3 blockers, 7 majors; round 2: no blockers, 2 majors fixed; record in section 8); approved by the user → D-20261106-7. Base: draft3 (D-20261105-5) sections 1-8 apply **except section 0 below**; this file wins on any conflict. Implements stage 1-2 of PLAN-access-layers-001-draft3 (D-20261106-5) and the handbook rule (D-20261106-6). App: usasia_db (Rails 8.1, SQLite, 1 GB VM).

## 0. Overrides of draft3
| draft3 item | Now |
|---|---|
| §3 export "all todos + versions"; R8 | `GET /api/v1/export` returns only the caller's visible rows, versions only for rows the caller owns |
| §3 GET /todos/:code "code or previous_code" | Looked up inside `Visible.for(caller)`; foreign rows → 404 |
| §5 / R9 nightly `sqlite3 -json` | **Dropped.** `.sqlite3.gz` stays the only nightly copy. JSON exists only through a Rails export task that goes through Visible (§2.5) |
| R6 versions append-only | Append-only, except one admin **purge** task for "report wrong" (§1.8) |
| S3 token field limits | Tokens cannot set owner, layer, code, created_by_kind |
| S9 identity by email/profile | users table keyed by (provider, subject) (§1.1) |
| `code` unique globally | Unique per owner: `(owner_id, code)` (§1.2) |
| §1 "owner must still be in ALLOWED_EMAILS at request time" | Session and token checks use `users.active`; ALLOWED_EMAILS only gates the first sign-in (§1.1) |

## 1. Access layers, stage 1-2 (D-20261106-5)
1. **users**: id, uuid, provider, subject (nullable until first login; unique (provider, subject)), email (display, lowercased), name, `admin` bool, `editor` bool, `active` bool, timestamps. ALLOWED_EMAILS only gates sign-in and creates the user row on first login; after that `users.active` is authoritative (leaver → inactive; tokens die). The shared "team" user (D-20261105-6) has no Google subject and is seeded by hand.
2. **todos**: `owner_id` NOT NULL → users; `layer` NOT NULL default 'L2', check constraint `layer IN ('L2','L4')` (L3 added with the grants table; until then fail closed); unique index `(owner_id, code)`; `parent_code` resolved within the same owner. `candidate` is **not** a layer: phase 1 adds a separate `promotion` column (null / candidate / promoted / reverted).
3. **`Visible.for(user)`**: L2 → owner only; L4 → all active users. Every read path (web pages, API, export, versions, search, dropdowns) uses it. Foreign rows → 404.
4. **Writes**: only the owner writes their rows (web or own token). **No direct L4 writes in phase 0** — L4 arrives only through the owner's digest promotion in phase 1; owner of an L4 row stays the original owner, displayed as "team". Editor edits of L4 = phase 1 decision.
5. **Versions** store `owner_id` and `layer` as they were at write time and are visible **to the row owner only**; non-owners see no history, actor or created_at for L4 rows.
6. **Admin** has no content access in the app. Raw server access is a **detective** control: SSH-login alert (PAM exec → healthchecks/mail to a second person) plus a heartbeat, so a disabled hook shows as a missing heartbeat (a root user can switch the hook off; the handbook says so). Wrapper scripts deferred to the server move (server-move-checklist).
7. **Deny list** (whole words, short lists, real-title tests from the current board, e.g. "health check", "HR kiosk", "payroll terminal" must pass): on a web L2 write → warning, owner confirms; on token writes and on promotion to L4 → hard reject with "write this to your own Drive (P layer)". Existing sensitive-value guard extended to every text column.
8. **Purge task** (admin, SSH alert applies): removes one row's L4 text from versions and the next exports after "report wrong"; logs the purge (id + reason code, no content). Older `.sqlite3.gz` keep it until retention ends (stated in the handbook).
9. **Logging**: filter_parameter_logging covers all content params; no request-body logging.
10. **Tests**: (a) route-enumerating contract test — user B gets 404 for user A's L2 row on every route and verb (web + API + export); (b) grep allow-list test for unscoped finders, `unscoped`, `find_by_sql`, raw SQL strings outside `Visible`, migrations and import.
11. **Gates before any non-hmlee user** (checklist): shared "team" Claude account retired for real work (access-layers §5); GitHub branch protection with James Yoo approval, admins included (user sets it); SSH-login alert live.

## 2. Migration readiness (DB will move: company server, likely PostgreSQL)
1. CI runs the suite on **SQLite and PostgreSQL** (service container); Postgres failure blocks merge.
2. Portable SQL only: no triggers, SQLite JSON/FTS5; ordering via `nulls_last`; search via Arel `matches` with `sanitize_sql_like` (case-insensitive on both, % and _ literal); `code`, `previous_code`, `parent_code` normalised to one spelling before save **and on every lookup** (web, API, CLI): prefix T-/M- upper case, rest lower case (amended at build, D-20261106-7 note: M-names are lower case across the repos and find.py).
3. Timestamps UTC; business dates as `date` (America/Los_Angeles); emails lowercased; enum-like strings with check constraints.
4. No internal id outside the app: API/CLI/links use `code` (todos) or `uuid` (users now; each new table gets its own uuid when created). UUIDv7 via `SecureRandom.uuid_v7` (Ruby ≥ 3.3, check .ruby-version), string(36), unique index.
5. **Export/import rake tasks** = migration format (schema-versioned JSON, every table, through Visible for API callers; full export only as an admin rake task on the server under the SSH alert). Round-trip into fresh SQLite and fresh PostgreSQL with counts + per-row checksums: once at phase-0 exit and before any cut-over (not monthly).
6. Connection only via `DATABASE_URL`. Files never in the DB.
7. **Read-only mode**: env var or file flag → `while_preventing_writes` around every action → 503; auth_events / last_used_at writes skipped while on; CLI treats 503 like unreachable (exit 3, fail open).
8. `/api/v1` additive only; breaking → `/api/v2`; CLI ignores unknown fields.
9. Schema-change rules (handbook 06): expand-then-contract for renames; NOT NULL after backfill in a separate migration; SQLite snapshot before every migration on deploy. Cut-over runbook in usasia_db docs/server-move-checklist.md.

## 3. AI-written data
1. **Provenance** on todos: `source_kind` (mail/stws/chat/manual/import), `source_ref` (ticket no. or link ID, never content), `created_by_kind` (person/claude, set server-side from web session vs token).
2. **Idempotency**: no general mechanism in phase 0. Create is idempotent by `(owner_id, code)`: same client-writable fields (not created_by_kind, source_*, timestamps) → 200 with the existing row; different → 409. Two concurrent creates: rescue the unique-index error, re-read, compare, answer 200 or 409. Key-based idempotency added later for tables without a natural key.
3. **lock_version** on todos (not api_tokens). CLI GETs, sends lock_version; StaleObjectError → 409 with the current row; CLI shows the conflict.
4. System of record per field documented in the data dictionary `why` (STWS owns ticket status/assignee — mirror in phase 1; Drive owns originals).
5. **Stores deferred** to phase 2 step 1 (D-20261105-11). `todos.store` stays free text; the store dropdown reads only the user's visible rows until the stores table exists.
6. No delete; correct by status cancelled + note. Retention per layer: user decision later, not blocking.

## 4. Existing todos rows (no data loss)
1. Migration A: users table; seed the hmlee user from ALLOWED_EMAILS (subject null until first login, bound then); then create a user row for **every distinct non-null `owner_email` in todos** (active if on ALLOWED_EMAILS, else inactive). The migration prints the distinct owner list and fails loudly if any value is unexpected.
2. Migration B: `owner_id` nullable; backfill by lowercased `owner_email` match; **only NULL** owner_email → hmlee; `layer` 'L2' with check constraint; provenance columns (existing rows: source_kind 'import', created_by_kind 'person'); `lock_version` 0.
3. Separate data migration (own snapshot): upper-case `code`, `previous_code`, `parent_code`; fails if that creates a duplicate.
4. Snapshot, then Migration C: `owner_id` NOT NULL + foreign key; unique `(owner_id, code)` replaces unique `code`.
5. Keep `is_private` and `owner_email` one release (read by nothing), then drop. Note in the log: rows that were visible to teammates become private (intended by D-20261106-5).

## 5. Handbook (D-20261106-6)
Every step updates meta.json (EN + KO) and the generated pages; new page 04-access-control (Visible, roles, write rules, purge, SSH alert) with Korean twin. Migration runbook and schema-change rules go into server-move-checklist.md and 06-schema-change-guide (short).

**Build journal (user 2026-11-06):** every build step also writes a Korean study note in usasia_db `docs/build-journal/` (template `_template.ko.md`): goal, files changed and why, commands, problems and fixes, review findings, how to verify, what to learn, questions to ask. CI fails if a migration file is not named in any journal note.

## 6. Build order (each step: tests, handbook, CI on both DBs, review)
1. Postgres CI job + portable ordering/search + code upper-casing on save/lookup (data change in its own migration and snapshot, §4.3).
2. users + migrations A-C (incl. provenance columns with defaults and lock_version) + Visible + 404 + contract test + allow-list test + owner-only writes (web).
3. Provenance set on writes, lock_version checks, deny list, guard on all text, logging filter, read-only mode.
4. API tokens + auth_events + rate limits (draft3 §1, R1-R5, S1-S2, S5-S6).
5. API + versions (owner-only) + CLI (draft3 §3-4, R7-R8, S4) + CLI checksum pin (access-layers §4).
6. Export/import tasks + purge task + round-trip test (SQLite + Postgres) + SSH-login alert and heartbeat on the server.
7. Exit: draft3 §6 + round-trip passes + James Yoo review of auth/scope/API code + section 1.11 gates checked before onboarding.

## 7. Deferred (cheap to add later)
General idempotency keys; verified_by_human (derive from versions); uuid on tables not yet created; monthly round-trip; admin wrapper scripts; retention config; per-user time zone; L3 + grants; stores/aliases/store_id.

## 8. Review record (fresh Sonnet, round 1 on draft4)
Accepted: B1 versions owner-only; B2 no direct L4 in phase 0; B3 purge task; M1 per-owner code; M2 SSH alert instead of wrappers; M3 warn-then-confirm deny list on L2; M4 idempotency cut (natural key); M5 nightly JSON dropped; M6 stores deferred; M7 users.active authoritative; feasibility notes (uuid_v7, nulls_last, matches, upper-case code, while_preventing_writes, contract test); cut list; migration steps; re-added CLI checksum and the team-account gate; candidate as a separate column; roles as two booleans.

### Round 2 (same reviewer, on draft5): no blockers
Accepted: §0 row for users.active vs ALLOWED_EMAILS; owner backfill creates users for every distinct owner_email (only NULL → hmlee) with a loud check; upper-case on lookup and for previous/parent code in its own migration; sanitize_sql_like; idempotency field set + concurrent create; provenance columns in step 2; SSH alert build step + heartbeat; hand-seeded "team" user.
**Deliberate deviation from D-20261106-5 (access-layers §3.6):** people/HR wording on the owner's own L2 web write warns and asks the owner to confirm instead of rejecting (false positives in an IT log: "health check", "HR kiosk"); token writes and promotion to L4 still reject.
