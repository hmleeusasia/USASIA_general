# PLAN access-layers-001 draft3 — personal vs team data, admin limits, auto-classification
Status: draft3 (2026-11-06), agreed with a fresh Sonnet after 2 rounds (round notes at the end); awaiting user approval. Owner: hmlee + Claude. Answers ai-system-questions Q19 (and Q1, Q2, Q6, Q9, Q16, Q20 in part). Overrides D-20261105-3 Q7 (default visibility: now private) and adds to PLAN-usasia-db-phase0-001-draft3 (D-20261105-5) before it is built.

## 1. Goals (user, 2026-11-06) and what this plan honestly delivers
| Goal | Delivered by |
|---|---|
| Users work independently | Row owner + layer on every row; one Visible scope (section 4) |
| Admin and user rights separate | Admin role = accounts, deploy, schema, backups; no content right in the app |
| Admin cannot read private data | **No normal path** gives the admin private content: truly private content is never stored on the admin's systems (minimization); app hides others' rows; admin raw access (console, sqlite3, restore) is notified to a second person. **Not claimed:** protection against an admin-developer who ships malicious code — that is covered by required review from a second developer, not by cryptography |
| Team and personal never mix, still a wiki | Layers L2/L4, derived work facts promoted only after owner confirmation |
| No manual entry | Claude classifies on save; promotion is a one-click daily batch |

Known residual: Google Workspace super-admins can read any Drive (incl. personal Drive and backups); Claude session transcripts hold what Claude read in that session.

## 2. Layers
| Layer | Content | Who sees | Where |
|---|---|---|---|
| L0 secret | passwords, keys | nobody | not stored (R-SEC-04) |
| L1 sensitive value | emails, phones, account / circuit IDs | owner; team copies in a shared Drive (Q6) | Drive (R-SEC-03) |
| P private | HR, evaluations, health, private life, notes about people | owner only | **owner's own Drive / local file only**; never usasia_db or GitHub; Claude writes there only in that owner's session |
| L2 personal work | own todos, mail-triage results, drafts — work summaries only (R-SEC-01) | owner only (app-enforced) | usasia_db |
| L3 shared-to | items shared with named people or a group | owner + grantees | usasia_db, `grants` table (stage 3) |
| L4 team wiki | stores, assets, vendors, procedures, tips, team decisions, work-history facts | all signed-in team | usasia_db (data), GitHub (rules, skills, code) |

Roles: admin, editor (approves team decisions/rules, Q2), user. Roles never widen content access.

## 3. Classification and promotion (goal 5)
1. Every row: `owner` NOT NULL, `layer` NOT NULL default L2. Unsure → L2 (or P).
2. Source default: personal mailbox/chat/notes → L2; STWS ticket, team mailbox → L4 candidate.
3. Claude splits a record: original stays L2; extracted **work facts** become a row with status `candidate`, linked to store/asset/vendor. Candidates are invisible to everyone but the owner.
4. Daily digest shows the owner each candidate's L4 text next to its source; per-row checkboxes; rows touching a person or a vendor contact are **unchecked by default**. Confirm → L4.
5. L4 rows: author shown as "team", date only; API does not return created_at, versions or derived_from for L4 to non-owners; derived_from lives in an owner-only table.
6. Never promoted: people facts, HR, money, complaints, private life (deny list enforced in the CLI **and server-side**). People/HR wording on an L2 write → rejected with "write this to your own Drive (P)".
7. "Report wrong" on any L4 row → revert to L2, purge from versions and the next export; older backups keep it until retention ends (stated).
8. Per-category auto-promotion (store/asset/vendor technical facts only) may be proposed after ≥ 4 weeks of digest data with zero reported-wrong promotions — separate decision.

## 4. Enforcement in usasia_db
- One scope `Visible.for(user)` on every read: web, API, search, versions, export. Foreign rows → 404.
- Build-failing test: no unscoped finders, raw SQL, Arel, `where` strings, or joins/includes bypassing the scope in controllers and models; export covered.
- Write tokens: may write only rows their owner owns; cannot create or set layer L4 (promotion only through the owner's digest confirmation in a web session).
- L3/L4 text from others = untrusted data for Claude (S4 envelope).
- filter_parameter_logging covers all content params; no request-body logging.
- Nightly JSON export: layer-filtered, L2 omitted; the `.sqlite3.gz` is the only full copy; backup folder shared with nobody.
- Admin raw access (rails console, sqlite3, restore) sends a notice to a second person (James Yoo or Dan Choi) through the healthchecks/mail channel, not a log the admin controls.
- Code review: branch protection on usasia_db main and this repo's tools/ requires James Yoo's approval, applies to admins (no bypass); tools/usasia.py checksum pinned in a file only the reviewer can change; CLI checks it at session start.

## 5. People and accounts
- Shared "team" Claude account retired for real work before any non-hmlee write — a hard gate in the build checklist.
- Leaver: removed from ALLOWED_EMAILS (tokens die); their L4 contributions stay; their L2 is exportable to them for N days, then deleted; the admin cannot read it.

## 6. GitHub repo
Shared repo = team-public only. Personal files (users/<id> todo, logs, docs/team notes) move to usasia_db (L2/L4) or the owner's Drive (P); then git history rewrite (filter-repo) before any teammate is invited.

## 7. Stages
1. This PLAN → decision.
2. Phase 0 draft4 = phase 0 + owner/layer NOT NULL, Visible scope, 404, scoped versions/export, write-token limits, server deny list, logging filter, layer-filtered export, admin-access notice, branch protection; James Yoo review.
3. Phase 1: todo import, classifier, candidates + digest promotion.
4. Retire shared Claude account for real work; move personal files out of GitHub, filter-repo; onboard teammates.
5. `grants` table when the first L3 share is needed.
Not taken: client-side encryption, blind indexes, KMS, OpenFGA server, paid DLP. Encryption revisited only for a concrete need, as Active Record Encryption on one opt-in column.

## 8. Debate record (fresh Sonnet, 2 rounds)
Round 1: client-side encryption rejected (admin ships the code; key handling; lost search/guard; plaintext in transcripts) → minimization + second reviewer. Derived-row leaks (metadata, versions) fixed. Shared account retirement moved earlier. Staged scope. Kept against the reviewer: promotion automation from day 1 as a digest batch (goal 5).
Round 2: no blockers. Added: unchecked-by-default rows touching people/contacts, report-wrong + purge, candidate status invisible to others, write tokens cannot create L4, server-side people/HR deny list, layer-filtered export, audit notice to a second person, branch protection without admin bypass, leaver L2 export-then-delete, honest goal-3 wording.
