# PLAN onboarding-001 draft1 — guided tutorial for a new teammate
Status: draft1 (2026-11-05), Opus. Not reviewed, not approved. Owner: hmlee (requirements) + Claude. Builds on D-20261102-19 (multi-user), D-20261105-6 (team account = beta tester), D-20261105-7 (docs/team context files), ai-system-questions Q13/Q15/Q16.

## Goal
A newcomer signs in and Claude walks them through the system one module at a time: what it can do, what is already set up, and what Claude needs from them. Each module = explain briefly → ask → save → confirm. The newcomer ends day 1 with a working profile, a first start-day, a first log entry and a session end.

## Principles
- One module per message, short (Korean or English, newcomer's choice). Never a wall of rules: show, then try.
- Resumable: progress in `docs/users/<id>/onboarding.md` (checklist + date per module). "Skip / later" is always allowed and recorded.
- Collect only what a skill reads. Each answer goes to its one home: non-sensitive → `docs/users/<id>/profile.md`; emails, phones, account numbers → their Drive Claude folder `00_profile` (R-SEC-03). Passwords never asked, never stored (R-SEC-04).
- Shared rules win; the newcomer's file only adds (D-20261102-19).
- New contacts or organizations named during onboarding → ask before adding (CLAUDE.md).

## Trigger
skill `onboarding`: runs when the user is unknown (no CLAUDE.local.md, git user not in docs/users) or the user says "온보딩", "처음", "onboarding", or `/onboarding`. Resumes at the first unchecked module. Open: detecting the signed-in Claude account when two accounts share one PC (D-20261105-6) — until solved, the first module asks "who are you?" and checks git user.

## Modules
| # | Module | Explain (what exists) | Ask / collect | Saved to | Done when |
|---|---|---|---|---|---|
| 0 | Welcome | 3-line map: repo (records, rules), Drive (originals, sensitive), STWS (tickets), usasia_db (todo board). How long it takes; can stop anytime | Language; name; preferred id | onboarding.md | id chosen, folder created |
| 1 | Security first | R-SEC in 5 lines: what never goes in the repo, the Drive Claude folder, passwords nowhere | Confirm understood | onboarding.md | confirmed |
| 2 | Who you are | docs/team/<name>.md if it exists: "here is the context we gathered; is it right?" + its "ask when they join" questions | Role, areas, stores covered, boss, time zone (required, D-20261105-1) | profile.md; team file answers | profile rows filled |
| 3 | Setup | CLAUDE.local.md line, git hooksPath, git user, cloud allowed domain (users/INDEX steps 2, 5, 6) | Local PC / cloud / both; Claude account type | profile.md; CLAUDE.local.md | `check.py` passes, digest shows the user |
| 4 | Connections | Which connectors and Chrome the session really has (test, do not trust profile, Q15) | Mailboxes used (Gmail / Outlook / intranet), Drive yes/no | profile.md (types only) | each source tested once or marked "none" |
| 5 | Drive Claude folder | Why it exists; create private folder, inheritance off; 00_profile sheet | Folder ID; sensitive values typed by them into the sheet, not chat | profile.md (folder ID only) | folder shared with 0 people (get_file_permissions) |
| 6 | Tickets (STWS) | todo board ↔ STWS, reporting duty; permission differences (Q16) | STWS assignee number, permission level | profile.md | first todo-sync dry run lists their tickets |
| 7 | Mail scope | mail-triage: list preview only, triage classes | What mail is theirs; senders to skip | users/<id>/mail_rules.md (stage 2 of H-multi) | 1 triage run on 5 mails |
| 8 | Expenses | kb/reimbursement.md daily intake (Q13) | Where receipts are stored; where expenses are recorded (if none: Notion DB + Sheet from template); existing method | profile.md | one test receipt flow or "skipped" |
| 9 | Tour of skills | start-day, todo / todo-sync, mail-triage, session-end, weekly-meeting, find.py + lookup rules; one line each + "try:" example | Which to use daily | onboarding.md | they ran 2 skills |
| 10 | First day | Real start-day → one log entry → session-end with commit | — | log file | first commit pushed |
| 11 | Feedback | What was confusing | Friction lines | ai-system-questions.md | module list closed; hmlee told |

## Files to build
- `.claude/skills/onboarding/SKILL.md` (procedure, ≤ 3,000 chars; module text lives in docs/onboarding.md)
- `docs/onboarding.md` (module texts, shared; replaces the short list in docs/users/INDEX.md)
- `docs/templates/user_profile.md`, `docs/templates/user_onboarding.md` (checklist)
- digest.py: unknown user → one line "new user? run /onboarding"

## Test
Beta tester = the "team" Claude account (D-20261105-6), walked by hmlee as a real newcomer. Pass = modules 0–10 done without hmlee typing repo commands; friction lines collected; second run resumes correctly after a stop.

## Open questions for the user
1. Who approves a new member's access (repo collaborator, usasia_db ALLOWED_EMAILS, STWS)? Onboarding can only list these as requests.
2. Should the tutorial also teach each person's own area (e.g. POS tips for Help Desk), or system use only?
3. Personal todo board: todo.md or usasia_db todos from day 1 (D-20261105-3 phase 1)?
