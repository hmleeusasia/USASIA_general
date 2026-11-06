# PLAN onboarding-001 draft2 — guided tutorial for a new teammate
Status: draft2 (2026-11-05). draft1 (Opus) reviewed by a fresh Sonnet in 2 rounds; all must-fix accepted, account detection replaced by Opus proposal (agreed). **Account detection built but switched off (D-20261105-12); the rest not approved yet.** Owner: hmlee (requirements) + Claude. Builds on D-20261102-19, D-20261105-6, D-20261105-7, ai-system-questions Q13/Q15/Q16. draft1: docs/requests/archive/.

## Goal
A newcomer signs in and Claude walks them through the system, one short module per message: what it can do, what is ready, what Claude needs. Day 1 is a short core (target ≤ 45 min); the rest unlocks on first use.

## Principles
- Value first: show what the system does, then the rule that matters at that moment. Explain → ask → save → confirm.
- Resumable: progress in `docs/users/<id>/onboarding.md` (checklist, dates, skips, hmlee interventions). "Later" always allowed.
- Collect only what a skill reads. Non-sensitive → `users/<id>/profile.md`. **No emails, phones, account numbers or keys are collected in chat at all.** If a typed value looks like one, Claude stops and applies R-SEC-05. Passwords never (R-SEC-04).
- During onboarding the newcomer writes only `docs/users/<id>/` and their own log file; `git pull --rebase` before each commit. Shared files (ai-system-questions, docs/team) are updated by hmlee from the queue in onboarding.md.
- Module texts live in `docs/onboarding/<n>.md`, read one at a time (lean context).

## Who the user is (account detection, fixes the shared-PC gap of D-20261105-6)
1. Hook reads `~/.claude.json` → `oauthAccount.accountUuid` and maps it through the git-excluded `.claude/accounts.local.json` (uuid → id), written by onboarding. The uuid is treated like an account number: never in the repo, log, digest output or chat; the digest prints only the id.
2. The hook injects the personal `docs/users/<id>/CLAUDE.md` content as context itself; the static `@` import in CLAUDE.local.md is retired (a printed "load X" is not reliable).
3. Unknown uuid → digest line "new user? /onboarding". No file / no oauthAccount (cloud, other versions) → fall back: CLAUDE.local.md → git user → ask once, and only then the line "treating you as <id>, say otherwise". Fail open.
4. Test: the team account no longer sees hmlee's personal file.

## Tools: who has what (user 2026-11-05; re-reviewed with a fresh Sonnet, 2 rounds, 2026-11-06)
Not everyone has the same tools (Notion is hmlee-only today). Guide each person only within the tools they have. Two separate questions per tool: **have** (the person has the account) and **path** (how Claude reaches it this session: connector / Chrome / none).
| Tier | Tools | Recorded by |
|---|---|---|
| Admin-provided | Claude Code, repo access, Google Workspace account, STWS, usasia_db access | admin, "Before you arrive" list (not a Tools row) |
| Common (account; path varies) | Gmail, Outlook, intranet mail, Drive, Google Sheets (expense baseline), Chrome extension (only path to Outlook, intranet, STWS), M365 connector | person's accounts in profile.md; path checked per session |
| Optional (personal) | Notion, OT Tracer sheet | profile.md row if they have it |
Add a tool row only when a skill uses it (no RustDesk or Slack rows today).

Mechanics
- Record: one `Tools` table in `docs/users/<id>/profile.md` (tool · have y/n · note). Repo copy only (non-sensitive); the Drive 00_profile does not carry it (D-20261103-3 note). Connector or path state is never recorded: it belongs to the session, not the person (Q15).
- Surface: digest.py prints `[tools claimed] …` from the profile. It is a claim, not a check (hooks cannot see the session's tool list). Skills read that line, not the profile again.
- Truth: at first use of a tool, the session's tool list wins. If the tool is missing or a call fails, Claude says so in one line and proposes a profile fix; never a silent skip or workaround.
- Unknown tool → ask once, record in profile.md (local and cloud alike; pull before commit).
- Optional tools: people without it are told once, one line, no install push ("with Notion you could also …"), in onboarding or the first time the related skill runs; recorded as `told:` in onboarding.md. Missing or unreadable `told:` → do not repeat.

Fallbacks (wording goes into skills with the onboarding skill)
| Skill | Without | Fallback |
|---|---|---|
| Expenses | Notion | Sheet only |
| Expenses | Sheet | decide later (local list for month-end?) |
| mail-triage | some mailboxes | loop over the profile's mailbox list |
| mail-triage, STWS, Outlook, intranet | Chrome | skip with one line |
| start-day, drive-check | Drive connector | skip the Drive step with one line |
| todo-sync | Chrome / STWS | todo.md only |

Build now (small, review-loop because docs/rules and tools/ change): R-EXP-01/02/06 reworded to "the user's targets (profile)"; R-EXP-05 lunch cap and code marked "company policy, same for all" with a decision ID; hmlee values removed from todo/SKILL.md (default assignee) and todo-sync/SKILL.md (verified-as line → "verified: <id>, date"); Tools table in hmlee's profile and in the profile template; `[tools claimed]` digest line. Defer to the onboarding skill: docs/kb/tools.md catalog, per-skill fallback wording.

## Before you arrive (hmlee / admin, ~10 min) — not a module
Repo collaborator access; usasia_db ALLOWED_EMAILS + redeploy; STWS account and permission (Dan Choi approves); cloud environment allowed domain (if cloud); `git config core.hooksPath tools/githooks` on their PC; stub `docs/users/<id>/` from templates; pre-fill profile rows from docs/team/<name>.md. Claude drafts the request texts; people approve.

## Day-1 core
| # | Module | Explain | Ask / collect | Saved to | Done when |
|---|---|---|---|---|---|
| 0 | Welcome | Fixed 5-line tour (what the system does) + 3 security lines + "never paste emails, phones or keys here" | Language; id confirm | onboarding.md | id confirmed |
| 2 | Who you are | Confirm list pre-filled from docs/team/<name>.md (no raw source context, no third-party questions) | Role, stores, time zone (required, D-20261105-1); boss optional | profile.md | rows confirmed |
| 3 | Setup | Claude writes accounts.local.json and runs `git config user.name/email` itself; newcomer only approves | Local / cloud | profile.md (`git 사용자` = `git config user.name`) | digest shows their id; check.py passes |
| 5 | Drive Claude folder (+ security in practice) | Why the folder exists; newcomer creates it (private, inheritance off) | Folder ID only | profile.md | permissions = 0 people (get_file_permissions, or a screenshot of the sharing dialog if no connector) |
| 10 | First day | Real start-day → one log entry → session-end, commit, push | — | own log | first commit by the new id pushed |

## Unlocked on first use or day 2+
| Module | Trigger | Collect |
|---|---|---|
| Connections | first mail/Drive/Chrome task | one profile row `connectors: Drive y/n, Chrome y/n` (Q15) |
| Tickets (STWS) | first "ticket" / todo-sync | STWS assignee number; "verified: <id>, date" on skill steps (Q16) |
| Mail scope | first "mail" | users/<id>/mail_rules.md |
| Expenses / OT / mileage | first receipt, 출발/도착, OT | where receipts and expenses live, OT sheet (Q13). Creating Notion DB/Sheet = separate task |
| Skill tour | day 2 | which skills they use |
| Feedback | end of day 1 and week 1 | friction lines → onboarding.md queue |

## Answers adopted
Access: hmlee requests, Dan Choi approves STWS permissions (before-you-arrive list). Scope v1: system use only; area tips (e.g. POS for Help Desk) later as optional modules. Todo board: todo.md on day 1; moves with phase 1 migration (D-20261105-3) by script.

## Test (team account beta, D-20261105-6)
Pass = (a) artifacts exist: profile rows, onboarding.md core checked, one log file, one pushed commit by the new id, check.py passes; (b) core ≤ 45 min; (c) hmlee interventions counted in onboarding.md; (d) resume: stop after module 3, restart → resumes at 5 with no repeated questions; (e) team account sees no hmlee personal file. Modules needing connectors are marked "needs real account".

## Files
`.claude/skills/onboarding/SKILL.md` (≤ 3,000 chars), `docs/onboarding/0.md…` (one per module), `docs/templates/user_profile.md`, digest.py + a SessionStart change for detection and personal-file injection, `.gitignore` for accounts.local.json, test_hooks cases. docs/users/INDEX.md short list → pointer.

## Open for the user
1. Showing docs/team/<name>.md to its subject: default = confirm list only; hmlee approves once for all team files (user 2026-11-06: permissions are not being adjusted yet, hmlee handles it).
2. Build order: account detection first (also fixes today's shared-PC issue), then the skill and core modules?
