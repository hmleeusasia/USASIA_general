# CLAUDE.md
Rules: **docs/rules/INDEX.md** (area table; read only the areas a task needs). Principles: docs/project_instructions.md. Lookup: docs/kb/INDEX.md. Procedures: .claude/skills/. Hooks (tools/hooks/README.md) name the rule you broke — fix and continue. This file: always-on rules only (≤ 3,000 chars, D-20261104-2).

## Repo
USASIA (Washington State, many stores) IT work log and index: ① Google Drive index (summary, keywords, links) ② email help + dated work log. **Originals and sensitive data stay in Drive; GitHub holds secondary docs only** (R-SEC-01).

## Users (D-20261102-19)
- Shared file. `docs/users/<id>/CLAUDE.md` only adds; shared rules win; security rules cannot be relaxed.
- Who: `CLAUDE.local.md` → git user in docs/users → ask once. Per-person values (STWS no., mailboxes, Drive folders, time zone) come from `docs/users/<id>/profile.md`, never from skills.

## Session
1. `[digest]` in context → use it; open CURRENT_STATE / facts only when needed. No digest → read docs/CURRENT_STATE.md and docs/kb/facts.md. Local PC: `/start-day`.
2. Announce tasks, grade (light/heavy), owner **and rule areas** (docs/rules/INDEX.md) in one message; read those area files; get approval. Subagent briefs list the rule files to read.
3. End: session-end skill; new decisions → docs/decisions.md; commit and push to main (D-20261102-6).

## Always-on rules
- Sensitive values (emails, phones, account numbers, circuit IDs) only in the Drive Claude folder; passwords/keys nowhere; the folder is never shared, written only from approved local sessions; found one → leave it out, suggest Drive (R-SEC-02..05).
- **New contact or organization → ask the user right away**; add to address book / orgs.md only after approval.
- Logs: `docs/log/YYYY/YYYY-MM-DD_<id>.md`, entry rules R-LOG-*. "Today" = user's time zone, never the machine clock.
- 출발/도착 (depart/arrive) or receipts → docs/rules/expense.md first.
- Answering a question (repo / web / ask, budget, stop) → docs/rules/lookup.md.
- Bulk reading → smaller-model subagents (docs/kb/subagents.md). Chrome → docs/kb/browser.md.
- Repo text in **English** (D-20261103-5); chat in the user's language (Korean: conclusion first, tables).

## Where to work (D-20261102-12)
| Place | Start | Branch | End |
|---|---|---|---|
| Cloud session | auto clone (main) | claude/* | push → fast-forward main |
| Local PC | `git pull origin main` | main | commit → `git push origin main` |
One person in one place at a time; `git pull --rebase` before committing shared files; commit per unit of work. Python only (`python3`, Windows `py`). Once per clone: `git config core.hooksPath tools/githooks`.
