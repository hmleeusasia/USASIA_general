# PLAN data-migration-001 draft2 — moving work data from this repo to usasia_db
Status: draft2 (2026-11-05), approved by the user → D-20261105-3. draft1 written by Sonnet A; reviewed by a fresh Sonnet B in 2 rounds (objections accepted except "logs and drive index stay in git", settled as below). Owner: hmlee + Claude. Follows D-20261104-5, D-20261105-1, D-20261105-2. Sections 1-3 and 6 are the draft1 survey (inventory, dependency map, entities, risks); the section "Agreed scope" below overrides draft1 sections 4 and 5.
Sensitive-value scan of all tracked files: no email addresses, phone numbers or IP addresses found (emails were redacted by D-34). See "Findings" at the end.

## Agreed scope (draft2, overrides sections 4 and 5)
Committed now: phase 0 and phase 1 only. Later phases are separate PLANs, each approved on its own after phase 1 has run about 4 weeks.

| Phase | Work | Exit criteria |
|---|---|---|
| 0 | (1) Cloud-session reach test of usasia-it.duckdns.org (HTTPS + auth from a cloud sandbox) = go/no-go, done first; no-go → this PLAN is re-reviewed. (2) Per-user API token: create/update only, no delete (D-20261104-5), revocable without redeploy. (3) Versions table (who changed what, when) for every write. (4) Server-side sensitive-value guard on every text field (same as todos). (5) Python CLI in this repo, tools/ (list/find/add/update/export). (6) Rate limit / CLI batching (1 GB VM, WEB_CONCURRENCY 1, RAILS_MAX_THREADS 3). (7) Nightly JSON export to Drive. | JSON export restored into a fresh DB and compared; developer (James Yoo) reviewed app/API/auth code |
| 1 | Import todo.md (sections 1, 2, 3, 3a; section 4 sync notes stay) and archive files, guard run over every row with a hit report; add fields kind, STWS mirror (status, url, last_seen); switch todo, todo-sync, start-day, weekly-meeting, session-end, prune.py, stop.py, digest.py, check.py, test_hooks.py and kb pointers; CURRENT_STATE section C only moves to todos | Counts equal, user spot-checks 10 rows, each switched skill ran once in a real session, backup restore after import. Cut-over day: git tag pre-migrate-p1; todo.md becomes a read-only file generated from the DB (never hand-edited); first week Claude's token is read-only |
| Later | Reference data (stores, organizations, tags), drive index, logs, rest of CURRENT_STATE, questions list | Each needs its own PLAN that names the concrete problem git cannot solve (e.g. search fails, two users conflict on log files, guard needed on DB writes) and lists which hooks, R-LOG rules and find.py features it replaces |
| End | Restart the 2-week freeze (D-20261105-2) | — |

Rules for all phases: hooks and digest fail open (warn, never block session start/end) when the DB is unreachable; the DB holds secondary docs only (R-SEC-01), is_private rows hold summaries, originals stay in Drive; Q7 visibility is fixed before a second user is added (ALLOWED_EMAILS + token + docs/users/INDEX.md onboarding step).

| Q | Answer |
|---|---|
| Q1 | (a) Code, skills, rules, hooks, kb notes and decisions stay in GitHub; moving decisions is dropped |
| Q2 | Order (a), only phases 0-1 committed |
| Q3 | Deferred to the logs PLAN |
| Q4 | (b) No people table; names (with titles) stay in organization notes |
| Q5 | (a) CLI in this repo, tools/ |
| Q6 | Fail open with a message; for cloud sessions an on-demand export in the user's Drive (a gitignored cache is empty in a fresh clone) |
| Q7 | (a) All rows visible to signed-in teammates except is_private; decide before a second user |
| Q8 | (a) STWS mirror columns on todos incl. last_seen |
| Q9 | (a) Pointer stub 30 days, then delete |
| Q10 | (a) Create/update only, versions are a phase-0 gate, first week read-only |
| Q11 | (c) Developer reviews app/API/auth code; review-loop + user approval for repo changes |


## 1. Inventory and proposed home
"DB" = usasia_db. "Stays" = GitHub, because it is code or instructions for Claude, not work data. "Drive" = Drive Claude folder / company Drive (R-SEC-01..03).
| Item | What it is | Size | Written by | Proposed home | Reason |
|---|---|---|---|---|---|
| docs/users/hmlee/todo.md | Personal board: Now plan (8 rows), main list (45 rows), no-ticket follow-ups (11 rows, section 3), others' tickets (1), sync notes | 13.7 KB | todo, todo-sync, weekly-meeting, start-day (read), session-end/prune.py | DB (todos, exists) | Work data; D-20261104-5 first table. Sections 3 and 4 need new fields (§3) |
| docs/archive/2026/todo_hmlee_closed.md, ai-system-questions_closed.md | Rows pruned from boards | 2 small files | prune.py | DB, then delete | History is done rows (status done/cancelled) |
| docs/log/2026/*.md | Daily work log, one file per person per day, entries `### title #tags` | 4 files, 66 entries, 29 KB | every skill that records work (todo, mail-triage, weekly-meeting, start-day) | DB (log_entries) | Core work data. Biggest cut-over (find.py, hooks, check.py read it) |
| docs/CURRENT_STATE.md | Handover A–H: C = repo/framework tasks (9 rows), B handoff notes, F traps, H last start-day / last monthly check | 5 KB | session-end, start-day, drive-check, humans | Split: C and B tasks → DB todos (kind=project); H dates → DB settings; A/E/F/G → stay or move to facts | Mixed file. digest.py parses sections by letter |
| docs/decisions.md | Append-only decision lines, 40 entries, IDs cited everywhere | 17 KB | humans/Claude at session-end | OPEN QUESTION Q1. Proposal: stays until phase 5, then DB (decisions) | It is governance, cited by rules and hooks; moving gives search but loses git diff review |
| docs/kb/orgs.md | Affiliates, vendors, partners with contact NAMES and titles | ~38 rows, 6.5 KB | mail-triage, todo, humans | DB (organizations + people name/title only) | Structured reference; R-SEC-02 allows name+title only |
| docs/kb/store_codes.md | Store/org abbreviations and aliases (used by find.py synonyms) | 20 rows | humans | DB (stores) | Reference table; todos.store is free text today |
| docs/vendors/*, stores/, assets/, projects/ (INDEX + hubs) | Hubs: itsolution.md, granite-dia.md, ai-system.md; stores/assets INDEX empty | 3 hubs + 4 INDEX | humans when first entry appears (R-LOG-07) | DB (organizations notes, projects) | Hubs only exist to anchor tags; DB relations replace them |
| docs/keywords.md | Tag whitelist + synonym table | ~20 tags, 8 synonyms | humans; check.py/find.py read | DB (tags, tag_synonyms) | Becomes validation data for log_entries and todos |
| docs/calendar.md | Recurring dates | 2 rows | humans | DB (recurring_events) or drop | Tiny; weekly meeting + monthly check could be settings |
| docs/drive-index/*.md | One line per Drive doc (name, summary, keywords, link), 6 files | ~270 rows, 66 KB | drive-index, drive-check, start-day | DB (drive_docs) | Index of Drive, not originals; ⚠ marks → is_private/sensitive flag; fits search and monthly status check |
| docs/drive-index/claude-folder.md | IDs + column names of the sensitive Drive folder | 15 rows | humans | Stays in GitHub for now (or DB settings) | R-SEC-03 says repo keeps IDs only; moving adds nothing and hooks/skills read it |
| docs/users/hmlee/profile.md | Per-person values: STWS no., time zone, git user, Drive folder ID | 12 rows | humans (copy of Drive 00_profile) | DB (users) with Drive 00_profile still the original (D-20261103-3) | digest.py/prune.py need it offline → keep cached copy (Q6) |
| docs/users/INDEX.md, users/hmlee/CLAUDE.md | User list, onboarding steps; personal instruction file | 2 files | humans | Stays | CLAUDE.md-type instructions; onboarding is a procedure |
| docs/kb/facts.md, mail_triage.md, pos_tips.md, reimbursement.md, work_overview.md, subagents.md, browser.md, INDEX.md | Knowledge/instruction notes read by Claude | 8 files, 36 KB | humans, Claude | Stays (Q1); work_overview.md (work-stream table from sent mail) is data → DB candidate later | Instructions for Claude behave like code; pos_tips/work_overview could later be knowledge_notes |
| docs/projects/ai-system-questions.md | Framework questions list (~20 rows) | 3.8 KB | Claude at session-end | DB todos kind=question, then delete | Questions are tasks with a decision outcome |
| docs/requests/PLAN-*.md (+ archive) | Design plans | 8 files | Claude | Stays (project design docs, finite) | Not operational data; dev docs for the repo |
| docs/rules/*, project_instructions.md, CLAUDE.md, .claude/skills/*, .claude/settings.json | Rules and procedures | 14 files | humans | Stays | Code/instructions |
| docs/templates/* | Entry/hub templates | 6 | humans | Stays until phases 3/5, then delete daily_log, store, vendor, asset, project, drive_index templates | Replaced by DB forms and validations |
| docs/ARCHITECTURE.md | Principles, diagrams, generated snapshot | 16 KB | repo_map.py, session-end | Stays; repo_map.py counts must change | Documentation of code |
| docs/storage_rules.md | Pointer to rules/security.md | 152 B | — | Delete (already planned in file) | Dead pointer |
| tools/*.py, tools/hooks/*, tools/githooks/*, tools/browser/* | Scripts and hooks | 20 files | humans | Stays | Code (D-20261104-5: existing hooks stay) |

## 2. Dependency map (what reads/writes each DB-bound item, and the change)
### 2.1 todo.md / archive
| File:line | Use | Change |
|---|---|---|
| CLAUDE.md:12 (digest/CURRENT_STATE), :14 | Session start reads state; end writes | Digest takes counts from the API |
| .claude/skills/todo/SKILL.md:17,21,23,34,39 | Search board, append M- row, log entry, "yesterday's requests" | Search and create through CLI (`todo add/find`); keep log-entry step until phase 3 |
| .claude/skills/todo-sync/SKILL.md:8,18,27,32,34 | Source = todo.md; add/update rows; update header; write sync notes | Read/write via CLI; header line and §4 notes disappear (DB keeps updated_at, add sync log) |
| .claude/skills/start-day/SKILL.md:12,34 | Reads "Now" and yesterday's M- rows | `todo list --planned-for today`, `--created-since` |
| .claude/skills/weekly-meeting/SKILL.md:15,16,23 | Done rows, Now rows, new To-dos with owner/due | CLI queries and `todo add --assignee --due` |
| .claude/skills/session-end/SKILL.md:9,10 | prune.py, "open items → todo.md" | Drop prune step for todos; open items via CLI |
| tools/prune.py:9-13,39,125-136 | Archives closed rows, past Now rows, old sync notes | Todo part deleted (status done is enough); questions part deleted at phase 5 |
| tools/hooks/stop.py:60-72 | stop-open: every T-ID in an #open log entry must be on the board (reads todo.md) | Ask the API `GET /todos?code=` (offline → skip with warn) |
| tools/hooks/digest.py:92 (+ :62 section H/F) | Pointer text "Open on demand: users/<id>/todo.md" | Update text; counts from CLI |
| tools/check.py:67 | todo.md 8k budget | Remove budget |
| tools/hooks/test_hooks.py:33-34,74-76 | Test paths docs/users/*/todo.md | Replace tests with API-mocked cases |
| docs/kb/INDEX.md:6, kb/facts.md:20, kb/mail_triage.md (todo refs) | Lookup table/fact text | Reword to "todo board in usasia_db" |
| docs/users/hmlee/CLAUDE.md (todo link) | Link to todo.md | Replace by app URL |

### 2.2 Log entries
| File:line | Use | Change |
|---|---|---|
| tools/find.py:12,60-100 | Searches log+archive; `--open`, `--due` parse `#open/#waiting`, dates (확인일/기한/다음), tags, synonyms | Replace by `search`, `open`, `due` server endpoints; synonyms from DB |
| tools/check.py:14-31,84 | Tag whitelist, hub-exists check, sensitive scan, INDEX gaps | Move to app validations; keep a thin check for remaining files |
| tools/hooks/guard.py:23,28,93-96 | log-path rule (name/year), ENG_PATHS english-nudge, sens-email/sens-secret on writes to docs/log | These fire only on file writes. DB writes bypass them → server-side sensitive guard (like todos) is mandatory before phase 3 |
| tools/hooks/area.py + docs/rules/INDEX.md:7 | Trigger path docs/log/** warns on unread write | Trigger words stay; path trigger dropped |
| tools/hooks/stop.py:60 | Looks at touched log files | Rewritten to API check (see 2.1) |
| tools/repo_map.py:39 | Counts log files | Count from API or drop |
| .claude/skills/mail-triage/SKILL.md:45; weekly-meeting:22,26; start-day (log lines); todo:23 | Append entries to docs/log | `log add --title --tags --body`; "commit and push" steps removed for logs |
| docs/rules/log.md (R-LOG-01..08), docs/templates/daily_log.md, CLAUDE.md:5,19 | File naming, entry format, hubs, tips | Rewrite rules: one-file-per-day rules (01) end; 02–06 become field/validation rules; 07 hubs end; 08 tip promotion stays |
| docs/kb/mail_triage.md:9 | "daily_log mail-check line" | Reword |
| tools/hooks/test_hooks.py:22-23,30-32,115-117 | Log path/sensitive tests | Rework |

### 2.3 Reference data (orgs, stores, tags, hubs, calendar)
| File:line | Use | Change |
|---|---|---|
| tools/find.py:18,22,74 | Reads keywords.md, store_codes.md, calendar.md for synonyms and due dates | Server-side; or cached JSON export in gitignored cache |
| tools/check.py:14,19 | Tag whitelist, hub check | App validations |
| tools/repo_map.py:11,42,43 | Counts decisions and store rows | Adjust |
| .claude/skills/mail-triage/SKILL.md:8,40 | Reads orgs.md; appends org line after approval | `org find/add` (new org still asks the user first, CLAUDE.md:18) |
| .claude/skills/todo/SKILL.md:11,12; weekly-meeting:31 | store_codes.md abbreviations; "ask to add contact" | Store list from API; todos.store becomes a FK/validated code |
| .claude/skills/todo-sync/SKILL.md:~20 | Hard-coded store abbreviation list inside the skill | Replace by API list (duplicate source today) |
| docs/kb/INDEX.md:8 (vendors), docs/kb/facts.md:14,17, kb/store_codes.md:20,27 | Pointers | Reword |
| docs/rules/log.md R-LOG-07, docs/rules/INDEX.md:7 | Hubs `docs/{vendors,stores,assets,projects}/**` | Drop |
| CLAUDE.md:18 | New contact/org → ask, add to "address book / orgs.md" | Wording → "address book / organizations" |

### 2.4 Drive index
| File:line | Use | Change |
|---|---|---|
| .claude/skills/drive-index/SKILL.md:18 | Writes docs/drive-index/<topic>.md rows, updates INDEX | Writes via `drive-doc upsert`; INDEX.md gone |
| .claude/skills/drive-check/SKILL.md:11,29 | Extract IDs from all index files; mark 🗑; update CURRENT_STATE H | `drive-doc list` / `set-status`; last check date into settings |
| .claude/skills/start-day/SKILL.md:45 | "not in docs/drive-index" new/changed docs | Query by ID/modified time |
| .claude/skills/session-end/SKILL.md:19 | Reads claude-folder.md for the folder ID | Unchanged while claude-folder.md stays |
| docs/kb/reimbursement.md:12, kb/subagents.md:53 | Point to drive-index rows/template | Reword; subagent brief uses CLI upsert |
| tools/check.py:31 (INDEX gaps for kb, drive-index) | Index completeness check | Drop for drive-index |
| docs/kb/INDEX.md:12,14 | Lookup rows | Reword |

### 2.5 State, users, decisions, questions
| File:line | Use | Change |
|---|---|---|
| tools/hooks/digest.py:41,62-90 | User detection (profile.md git user), section H/F parsing, H-sheet, counts | users + settings from API with offline cache (Q6) |
| tools/prune.py:39 | Reads profile.md for user | API |
| .claude/skills/start-day/SKILL.md:23,24,41,62; drive-check:29 | "Last start-day", "last monthly check" in CURRENT_STATE H | `settings get/set` |
| docs/project_instructions.md:7-8, CLAUDE.md:12,14 | Describe CURRENT_STATE and decisions.md | Reword at each cut-over |
| tools/hooks/stop.py:55-58; tools/check.py:36,68 | CURRENT_STATE 80-line/5k limits | Keep until CURRENT_STATE is removed |
| tools/find.py:83; tools/repo_map.py:42 | Decision search/count | Only if decisions move (Q1) |
| .claude/skills/review-loop/SKILL.md:24, session-end:12 | Friction lines → ai-system-questions.md | `todo add --kind question` |
| docs/users/INDEX.md (profile.md steps) | Onboarding steps create profile.md | Add "create user in app" step |

## 3. Proposed entities
| Entity | Key fields | Relations | Replaces |
|---|---|---|---|
| users | name, login email (identity only), git user, stws_id, time_zone, drive_folder_id, role | has many todos, log_entries | profile.md |
| stores | code, name, aliases, region, active (BV legacy vs new, TC=Lakewood) | todos, log_entries | store_codes.md, store hubs |
| organizations | name, kind (affiliate/vendor/partner/building owner), notes, status (confirmed/presumed) | people, log_entries, todos.waiting_on | orgs.md, vendor hubs |
| people | name, title, organization_id. NO email/phone (stay in Drive 10_address book, R-SEC-02/03) | org | names inside orgs.md/todo |
| todos | exists (see below) | store, assignee user, parent | todo.md, archive, ai-system-questions, CURRENT_STATE C |
| log_entries | date, user, title, fields/kinds/targets as tags, status (open/waiting/done), body text, due/check dates, ticket codes, decision ids | stores, orgs, projects, todos (by code) | docs/log |
| tags, tag_synonyms | name, group (field/kind/state), synonym | tagging on log_entries, todos | keywords.md |
| projects | name, tag, summary, status | log_entries, todos | docs/projects hubs |
| drive_docs | name, summary, keywords, targets, url, drive_id, folder, sensitive flag, status (ok/trashed/renamed), checked_on | store, org | docs/drive-index |
| settings / events | key/value (last start-day, last monthly check), recurring events | — | CURRENT_STATE H, calendar.md |
| decisions (optional, Q1) | code D-…, date, text, replaced_by | — | decisions.md |
### What todos covers now and what it gets wrong
| Covered | Gap or mismatch |
|---|---|
| code, parent_code, previous_code, status enum, waiting_on, next_step, due_on, planned_for, moved_on, assignee, is_private | store and tags are free strings: no store registry, "DH·MW", "BV(구)", "?" and "본부" are not validated or searchable by alias |
| Sensitive-value guard on free text | Status text like "기다림(매장 구매)" and "기다림(?)" loses the reason unless it goes to waiting_on (import rule needed) |
| Combined IDs split into rows | Section "Now" has rows without a day ("next FW visit", "Any") and multi-ID rows; planned_for date alone cannot hold them |
| No delete route, cancel instead | No change history; a token that can edit can silently rewrite a row (needs versions/audit before Claude gets write access) |
| owner_email | No users table: assignee is a name, owner is an email; no link to stws_id; no per-user visibility rule (PLAN out of scope) |
| — | No kind field: tickets (T-), no-ticket follow-ups (M-), others' tickets (section 3a), repo/framework tasks (CURRENT_STATE C), questions all look alike |
| — | No ticket mirror fields (STWS status, URL, last sync); todo-sync compares STWS vs board and today only has the board |
| — | Section 3 "Who" values (user/local/cloud) and long narrative notes (M-contact, M-names) are not rows; contact batches must stay in the Drive pending sheet (D-20261102-17) |
| — | Links to log entries/ticket mentions are not stored (log_entries.todo_code needed in phase 3) |

## 4. Migration order, cut-over and rollback (draft1, superseded by Agreed scope)
Order follows risk and dependency: fewest readers first, log last.
| Phase | Scope | Prerequisites | Cut-over rule (repo file after the DB is source) | Rollback |
|---|---|---|---|---|
| 0 | API token without delete, per-user; Python CLI (list/find/add/update/export); server-side guard on every text field; row versions; nightly JSON export already on Drive backup; test cloud-session reachability | todos table live (done), Q5, Q6, Q7 | — | Nothing moves |
| 1 | todos: import todo.md (45+11+8+1 rows) and archive files; add fields (kind, ticket mirror, store FK later); switch todo, todo-sync, start-day, weekly-meeting, session-end, stop.py, digest.py | Phase 0; import script with row-by-row report; user checks 10 rows | After counts match and one week of parallel use (both written by CLI, file generated read-only): todo.md replaced by a 5-line pointer; archive files deleted. Git tag `pre-migrate-p1` | Re-run `export --md` to regenerate todo.md from DB; restore from tag; delta since cut-over exported from DB |
| 2 | Reference: users, stores, organizations, people (name/title), tags/synonyms, projects; todos.store/waiting_on validated against them; find.py reads the API | Phase 1; Q4 | orgs.md, store_codes.md, keywords.md, hubs → pointer stubs 30 days, then deleted; check.py tag/hub checks removed | Same: export regenerates md; tag `pre-migrate-p2` |
| 3 | drive_docs (≈270 rows) and the three Drive skills; claude-folder.md stays | Phase 2 (stores, orgs) | drive-index/*.md deleted after row count + sample check (⚠ flags preserved) | Export to md; Drive links are unchanged anyway |
| 4 | log_entries: import 4 files/66 entries, then CLI-only writes; replace find.py, check.py log parts, log-path/stop-open/sens hooks; rewrite R-LOG rules, templates | Phases 1–3; server guard proven on todos; search parity test (same 10 queries old vs new) | Logs frozen at a named date; docs/log/ removed from main after parity test; git history keeps old text | Export `log --md` per day regenerates files; tag `pre-migrate-p4`; restore hooks from tag |
| 5 | State and records: CURRENT_STATE C/B → todos, H → settings; ai-system-questions → todos; decisions → DB only if Q1 says so; calendar.md; kb data (work_overview, pos_tips) if wanted | Phase 4 | CURRENT_STATE reduced to a short generated pointer or deleted; digest fully API | Same export/restore |
| 6 | Cleanup: delete stubs and templates, shrink CLAUDE.md (still ≤ 3,000 chars) and rules INDEX, update ARCHITECTURE/repo_map, test_hooks | All | — | Git tags |
Cut-over rule for all items: DB becomes source only when (a) import report shows counts equal, (b) user spot-checks, (c) the replacement skill/hook ran once in a real session, (d) a restore from the daily Drive backup was tested after the import. Freeze = file is replaced by a pointer or deleted, never edited in parallel after cut-over. Two-writer period is not allowed (one writer: CLI); the old file is read-only after the freeze date.
Global rollback: each phase is a git tag + DB export; the DB export can regenerate the markdown, so rolling back = tag restore + `export --md` of rows changed after cut-over.

## 5. Questions for the user (draft1 options; answers in Agreed scope)
| # | Question | Options | Recommendation |
|---|---|---|---|
| Q1 | Which docs stay in GitHub as "instructions for Claude" (D-20261104-5 says code only)? | (a) Only code/skills/rules/hooks; kb notes and decisions stay too. (b) Same, but decisions.md moves to the DB at phase 5. (c) Everything incl. kb moves | (a) now, revisit decisions at phase 5. Decisions are reviewed by diff and cited by rules; kb notes are loaded as context |
| Q2 | Phase order | (a) todos → reference → Drive index → log → state. (b) log first because it is the largest. (c) reference first | (a). Log has the most readers (find.py, 5 hooks, 4 skills) and needs the server guard proven first |
| Q3 | Log entries after migration: where is the readable record? | (a) DB only. (b) DB + monthly Markdown export to Drive (not GitHub). (c) keep files in GitHub too | (b): backup you can read without the app; GitHub stays code-only |
| Q4 | Contacts/people in the DB | (a) Name + title + org only (as orgs.md today); emails/phones only in Drive address book. (b) No people table; keep names in text. (c) Full contacts in DB | (a). Matches R-SEC-02/03; (c) would put sensitive values on the VM |
| Q5 | Where does the CLI live | (a) this repo, tools/ (hooks and skills already live here; team clones it). (b) usasia_db repo, installed on each PC | (a): one clone per teammate; usasia_db stays the server |
| Q6 | If the DB is unreachable (VM down, cloud sandbox cannot reach it) | (a) Read-only cache of todos/users in a gitignored file; writes wait. (b) Hard fail with message. (c) Queue writes locally and sync later | (a) for session start; check cloud reach in phase 0 before anything is cut over |
| Q7 | Visibility between teammates for todos and log entries | (a) All visible except is_private rows. (b) Private by default, share per row. (c) Per-user only | (a): users/ is already team-visible (D-20261102-19); decide before phase 4 |
| Q8 | STWS tickets | (a) Add ticket mirror columns on todos (stws_status, url, last_seen). (b) Separate tickets table. (c) Keep STWS only in the browser as now | (a): todo.md already treats T- rows as the mirror; (b) adds joins for ~45 rows |
| Q9 | Old files after cut-over | (a) Pointer stub 30 days, then delete (history in git). (b) Delete immediately. (c) Keep frozen in archive/ | (a). Git history already redacted by D-34; do not keep a second copy of work data in main |
| Q10 | Claude's write permission | (a) Create/update, never delete (D-20261104-5), plus row versions. (b) Read-only until phase 2. (c) Full write | (a) with versions. Read-only first for 1 week during phase 1 is acceptable |
| Q11 | Who reviews phases | (a) Fresh-Sonnet review per phase (review-loop) + hmlee approval. (b) Developer (James Yoo) reviews app code only. (c) Both | (c) as D-20261104-5: developer reviews app code, review-loop covers repo changes |

## 6. Risks
1. Availability and reach: one 1 GB VM and a free domain become a dependency for start-day, todo, stop hook, digest. Cloud-session network access to the DB is not checked. Mitigation: phase 0 reach test, cache (Q6), daily backup restore test.
2. Guard coverage: sens-email/sens-secret hooks only see file writes; DB writes bypass them. The todos guard is pattern-based (emails, phones, keys) and cannot detect account numbers, circuit IDs or serials. Mitigation: same guard on every text field server-side and in the CLI; keep the "write only summaries" rule.
3. Fidelity of log search: find.py relies on regexes over free text (tags, dates, #open/#waiting, synonyms, line refs like file:line used in reports). Import may lose structure; mitigation: parity test of 10 real queries before phase 4.
4. Process drag: ~12 skills/tools/hooks and 6 rule/kb files change; D-20261103-7 freeze (to 11/17) and the 3,000-char CLAUDE.md limit apply; hooks tests (test_hooks.py) must be rewritten.
5. Two-writer drift during parallel weeks (CLI vs hand-edit); mitigated by read-only old files and one writer.

## Findings (sensitive-value scan, locations only)
| Where | What |
|---|---|
| docs/kb/orgs.md (STI row), docs/kb/work_overview.md | A business street address of a warehouse site (not personal; R-SEC-02 lists network details, not business addresses) — suggest user decides if it stays |
| docs/users/hmlee/todo.md (M-share row) | Describes a document shared with personal accounts and that it contains passwords (no values written). This is a security-map item that D-20261102-19 sends to Drive 30_sharing review |
| docs/users/hmlee/profile.md, docs/drive-index/claude-folder.md, kb/reimbursement.md | Drive/Notion/Sheet IDs and the STWS assignee number — allowed (IDs), but they become DB rows; keep out of any public export |
| Whole repo | About 60 staff/contact names with titles (kb/orgs.md, todo.md M-contact) — allowed (name and title), but the DB makes them searchable by anyone with login |
| Whole repo | No emails, phone numbers, IPs, account numbers or passwords found by pattern scan |
