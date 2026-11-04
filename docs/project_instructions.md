# Working principles (this repo)
Cut to repo-relevant parts 2026-11-03 (PLAN-lean-context-001 step 2; generic version in git history, D-20261102-1). Repo settings: CLAUDE.md.

## 1. State lives in files, not chat
| File | Rule |
|---|---|
| docs/CURRENT_STATE.md | Handover, ≤ 80 lines, fixed sections A–H, overwrite changed sections only |
| docs/decisions.md | Append only, `D-YYYYMMDD-N`, one line each |
Start: CLAUDE.md → CURRENT_STATE → announce tasks, grade and owner in one message, get approval → afterwards stop only for exceptions. End: session-end skill.

## 2. Grade the work
| Grade | Example | Process |
|---|---|---|
| Light | one log entry, one file fix, small skill edit | do it → check → commit |
| Heavy | framework/structure change, many files | PLAN → fresh-agent review → user approval → build → check |
Same kind of work under the same rules → one PLAN. Unsure → ask the user.

## 3. Subagents
Models, prompts, checks: docs/kb/subagents.md. Main session judges, reviews, commits; tell the user which model before delegating; give paths in the prompt; never commit agent output unreviewed; agents must not commit.

## 4. PLAN format
`docs/requests/PLAN-<topic>-001-draftN.md`: request / decisions / files to change / how to check / risks and questions. Old drafts → `docs/requests/archive/`. Review asks: missing paths, conflicts, checks that pass for the wrong reason; results as must / should / fine with line refs.

## 5. Checks and research
- Say "not checked" for anything not verified; keep inference and fact apart.
- Knowledge order: docs/kb/INDEX.md → topic file → raw files. Search counts first, then narrow; never conclude "none" from cut output; read only needed line ranges.
- Repeated manual work → a script in tools/.

## 6. Communication
Conclusion first, tables, the user's language. Mark undecided values as "temporary". Ask with 2–4 options, recommendation first. End of session: inefficiency table (waste → fix), apply usage-saving fixes right away.
