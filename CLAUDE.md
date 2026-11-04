# CLAUDE.md
Principles: docs/project_instructions.md. Lookup table: docs/kb/INDEX.md "Where to look first". Procedures: .claude/skills/ (each skill's description says when to use it).
Supervisor hooks (tools/hooks/README.md) enforce checkable rules and say which rule you broke — fix and continue. This file keeps judgment rules only (budget ~3,000 chars, PLAN-lean-context-001).

## Repo
USASIA (Washington State, many stores) IT work log and index. ① Google Drive index (summary, keywords, links) ② email help + dated work log (vendors, decisions, dates, tips). **Originals and sensitive data stay in Google Drive; GitHub holds secondary docs only** (docs/storage_rules.md).

## Users (D-20261102-19)
- This file is shared. Personal settings `docs/users/<id>/CLAUDE.md` only add; shared rules win; security/storage rules cannot be relaxed.
- Who: `CLAUDE.local.md` → git user in docs/users → ask once. Per-person values (STWS no., mailboxes, Drive folders) come from `docs/users/<id>/profile.md`, never from skills.

## Session
1. `[digest]` in context (SessionStart hook) → use it; open CURRENT_STATE / facts only when needed. No digest → read docs/CURRENT_STATE.md and docs/kb/facts.md in full. Local PC: `/start-day` (D-20261102-13).
2. Announce tasks, grade (light/heavy) and owner in one message; get approval.
3. End: session-end skill; new decisions → docs/decisions.md; commit and push to main (D-20261102-6).

## Where things go
Logs `docs/log/YYYY/YYYY-MM-DD_<id>.md` (one person per file, template docs/templates/daily_log.md) · hubs `docs/{vendors,stores,assets,projects}/<name>.md` · recurring dates docs/calendar.md · Drive index docs/drive-index/ · keywords docs/keywords.md · old logs docs/archive/YYYY/.

## Judgment rules
- Each log entry: `### Title  #field #kind #target` (keywords.md). Create a hub when the first related entry appears; no hand-written history tables (use find.py).
- Decisions explained only in decisions.md, logs carry the ID. Dates live in the entry body; calendar.md only for recurring/long-term (D-20261102-11).
- Sensitive values (emails, phones, account numbers, circuit IDs) only in the Drive Claude folder; passwords/keys nowhere; the folder is never shared; writes only from approved local sessions (D-20261102-16). Found one → leave it out, suggest Drive.
- **New contact or organization → ask the user right away**, add to address book / orgs.md only after approval.
- Bulk reading → smaller-model subagents (docs/kb/subagents.md, D-20261102-20). Chrome → docs/kb/browser.md.
- Repo text in **English** (D-20261103-5); chat in the user's language (Korean: conclusion first, tables).

## Where to work (D-20261102-12)
| Place | Start | Branch | End |
|---|---|---|---|
| Cloud session | auto clone (main) | claude/* | push → fast-forward main |
| Local PC | `git pull origin main` | main | commit → `git push origin main` |
One person works in one place at a time; `git pull --rebase` before committing shared files; commit per unit of work. Tools need Python only (`python3`, on Windows `py`). Once per clone: `git config core.hooksPath tools/githooks`.
