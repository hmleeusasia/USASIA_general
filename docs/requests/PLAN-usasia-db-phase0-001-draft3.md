# PLAN usasia-db-phase0-001 draft3 — API token, change history, API, CLI, JSON export
Status: draft3 (2026-11-05), approved → D-20261105-5. draft1 reviewed by a fresh Sonnet (section 7), draft2 by an Opus security review (section 8). Later sections override earlier ones. Implements phase 0 of PLAN-data-migration-001-draft2 / D-20261105-3 (step 1, cloud reach test, passed). App: C:\USASIA Claude\usasia_db (Rails 8.1, SQLite, 1 GB VM, WEB_CONCURRENCY 1, RAILS_MAX_THREADS 3). Todos: D-20261105-4.

## 1. API tokens
- New page /tokens (Google login): a signed-in user creates a token with a name and a scope `read` or `write`; value shown once.
- Table api_tokens: owner_email, name, scope, token_digest (SHA-256 of a 32-byte random value, unique), last_used_at, revoked_at, timestamps. Lookup by digest (secure compare not needed after hashing). Prefix `usdb_` on values so leaks are recognisable.
- No delete scope exists. Revoke = button, sets revoked_at; no redeploy. First week only `read` tokens are created for Claude (D-20261105-3 Q10).
- Owner must still be in ALLOWED_EMAILS at request time (removing a person from the secret also kills their tokens).
- Where tokens live: this PC = a file in the user's home (e.g. ~/.usasia/token, outside the repo); cloud sessions = an environment variable set in the cloud environment. Never in the repo, Drive Claude folder or memory (R-SEC-04).

## 2. Change history
- Table versions: item_type, item_id, item_code, event (create/update), changes (JSON {field: [before, after]}), actor_email, api_token_id (null for web), created_at.
- Written by a model concern (after_create / after_update), actor taken from Current attributes set in the controller (web session or token). Own small table, no paper_trail gem.
- Edit page shows the item's history.

## 3. JSON API under /api/v1 (Authorization: Bearer <token>)
| Request | Does | Scope |
|---|---|---|
| GET /api/v1/todos | list; filters status (open/all/each), store, code, planned_for, due_before, updated_since | read |
| GET /api/v1/todos/:code | one item (code or previous_code) | read |
| POST /api/v1/todos | create | write |
| PATCH /api/v1/todos/:code | update | write |
| GET /api/v1/export | all todos + versions as JSON | read |
- No DELETE route. CSRF skipped for API (token auth, no cookies). Errors as JSON {errors: {...}} with 401/403/404/422/429.
- Rate limit: Rails 8 `rate_limit to: 60, within: 1.minute, by: token` on API controllers.
- Sensitive-value guard: already in the Todo model, so web and API share it; extract to a concern for future tables.

## 4. Python CLI tools/usasia.py (this repo)
- Standard library only (urllib); honours HTTPS_PROXY (cloud sessions resolve names through the proxy).
- Commands: `todo list [--status --store --planned-for]`, `todo get CODE`, `todo add --code --title ...`, `todo update CODE --field value`, `export [--out file]`.
- Token from env USASIA_DB_TOKEN, else ~/.usasia/token. Base URL from env or default https://usasia-it.duckdns.org.
- Unreachable / 5xx → one-line message, exit code 3 (callers such as hooks treat 3 as "skip, warn" = fail open).
- Tests: tools/test_usasia.py with a local fake server (http.server) — no network.

## 5. Nightly JSON export + restore test
- backup.sh also runs `sqlite3 -json` (todos, versions) → usasia_db_<date>.json.gz next to the .sqlite3.gz, uploaded to the same Drive folder, same retention.
- Restore test (phase-0 exit): load the JSON into a fresh SQLite with the schema, compare counts and every row with production.

## 6. Exit criteria for phase 0
JSON restore test passes; API works from this PC and from a cloud session with a read token; fresh-Sonnet review of the built code; developer (James Yoo) reviews app/API/auth code (user sends the request).

## Questions for the reviewer
1. Token design safe enough (digest, scope, revoke, owner allow-list check)? Anything missing (expiry, IP)?
2. Versions via callbacks + Current attributes: gaps (e.g. update_all bypass, import path)?
3. Rate limit backed by Rails.cache (Solid Cache on SQLite) on a 1 GB VM: OK?
4. Is the JSON export enough as the rollback source for phase 1?

## 7. Review changes (accepted, override above)
| # | Change |
|---|---|
| R1 | API controllers get their own base class (ActionController::API): no allow_browser (application_controller.rb:3 would answer 406 to the CLI), no require_login redirect (JSON 401 instead), no cookies/session, no Set-Cookie. Reuses ApplicationController.allowed_email? for the owner check |
| R2 | CSRF: skipped only in the API base class; web /tokens pages keep CSRF (create/revoke are POST/DELETE forms) |
| R3 | Token only in the Authorization: Bearer header; `?token=` refused (proxy/Puma logs record URLs). Never logged: not in 401 handling, not in CLI errors. filter_parameter_logging already covers :token/:token_digest |
| R4 | Tokens: expires_at (write 90 days, read 180 days), max 5 active per user, list shows last 4 chars only, revoke writes an audit row |
| R5 | Rate limit: `store: ActiveSupport::Cache::MemoryStore.new` (one Puma process; Solid Cache would write SQLite per request), `by:` resolved token id; also rate limit failed auth by remote IP (check remote_ip behind kamal-proxy); 429 with Retry-After |
| R6 | Versions: after_save with saved_changes, inside the save transaction, updated_at excluded; actor "console" when none set; append-only (no update/delete); a test fails the build if app code uses update_all/update_column/insert_all/upsert_all on todos; the phase-1 import saves rows normally with actor "import" |
| R7 | CLI refuses non-https base URLs, keeps certificate verification on (SSL_CERT_FILE honoured for proxies), honours NO_PROXY, exit 3 = unreachable (fail open), exit 4 = 401/403 (warn: token revoked/expired), prints no token |
| R8 | API: params.expect (owner_email/actor never from the body), 400 on bad JSON, pagination (limit 200 + cursor), index on updated_at; export paginated, excludes api_tokens |
| R9 | Nightly JSON: `sqlite3 -json` on the .backup snapshot (not the live DB); retention also for *.json.gz. Rollback primary = .sqlite3.gz, JSON = readable secondary; after a restore all tokens are revoked |
| R10 | Tests: revoked, expired, wrong scope (read token POST → 403), owner removed from allow list, no Set-Cookie, query-string token refused, rate limit 429 |

## 8. Security review changes (Opus, threat model) — D-20261105-5
| # | Change |
|---|---|
| S1 | Scopes: `read`, `write`, `export` (separate). Claude tokens never get `export`; export = web session or an export token made by hand |
| S2 | Per-token daily write cap (default 100/day) on top of 60/min; more than 10 status changes to cancelled per hour → 429 |
| S3 | Field limits: tokens cannot set is_private, owner_email; code changes only via web (M- → T- rename by a person) |
| S4 | CLI prints todo text inside an "UNTRUSTED DATA" envelope; skills treat it as data, never instructions |
| S5 | auth_events table (event, token id, hashed IP, reason code; never the token) for every 401/403/429 and OAuth refusal/failure; token create/revoke rows; /tokens page + CLI `activity` show the last 24 h per token (start-day shows it) |
| S6 | Creating a token needs a Google sign-in within the last 15 minutes |
| S7 | Backup failure alert: backup.sh pings a free healthchecks.io check on success; a missed ping emails the user |
| S8 | GitHub: server host key stored as a repo variable and written to known_hosts (no ssh-keyscan); third-party actions pinned to commit SHAs; Dependabot PRs merged after CI. User: 2FA on both GitHub accounts, branch protection on main |
| S9 | Identities: owner/actor names "team" (shared Claude account) and "hmlee" (personal). Local CLI maps the signed-in Claude account (accountUuid in ~/.claude.json) to a profile via ~/.usasia/accounts.json and reads ~/.usasia/token-<profile>; unknown account → no token, fail open with a message. Cloud sessions run only on the hmlee account (token in that cloud environment's variables) |
| S10 | Server is temporary: no hardening now; usasia_db docs/server-move-checklist.md lists the review's server findings; DB holds summaries only until the move |
