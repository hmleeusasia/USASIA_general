# PLAN-rule-routing-001-draft2 (Opus + Sonnet, 2026-11-04 — approved by user 2026-11-04, D-20261104-2)
draft1 → docs/requests/archive/ (fresh-Sonnet review: 7 must, 9 should, all taken here). Related: PLAN-lean-context-001-draft2, D-20261103-6/7, ai-system-questions Q2, Q8, Q17(2).

## 1. Request (user, 2026-11-04)
Rules grow without bloating always-loaded md. Before work, only the rules the task needs are read. A supervisor makes sure the needed rules reach the executor; after heavy work a reviewer checks the result critically; executor accepts or rebuts; unresolved points go to the user.

## 2. Decisions (chosen by the user in chat 2026-11-04)
| # | Decision | Why |
|---|---|---|
| a | Rules live in `docs/rules/<area>.md` (≤ 3k chars each) + `docs/rules/INDEX.md` area table (≤ 3k chars). No line-number pointers | Fewer git conflicts; one folder = one source |
| b | One heading per rule, stable ID `## R-<AREA>-NN`, never reused. Hook rule names map to IDs under a separate `"ids"` key in tools/hooks/config.json (not inside `"rules"`, which test_hooks.py forces to block) | Logs, reviews, hooks cite IDs |
| c | **Opus (main session) is the conductor**: at the task announcement (CLAUDE.md Session 2) it reads INDEX, names the areas, reads those area files. No separate conductor agent | Opus has the conversation; a fresh agent does not |
| d | Every subagent brief lists "rules to read: <paths>". subagents.md "read CLAUDE.md and storage_rules.md first" becomes "read the listed rule files" | Subagents know only the brief |
| e | Supervisor = hooks + reviewer. Two triggers: (1) **keyword** — UserPromptSubmit matches INDEX trigger words (e.g. 출발/도착 → mileage) and points to the area file, once per area per session; (2) **path** — a repo write whose path maps to an area whose file was not read this session → warn once. Connector-only work (Notion, Sheets, mail) is covered only by (1) | Path hooks never see connector writes (mileage, Q17(2)) |
| f | Procedures stay in skills and cite IDs. Only cross-skill or hook-enforced rules move. Skill-local rules stay. Personal rules stay in docs/users/<id>/ | Keep rules next to their steps |
| g | CLAUDE.md keeps: session flow + announce/approve, security/storage, new contact → ask now, language, pointer to docs/rules/INDEX.md. Irreversible-action rules never depend on a lookup | Safety |
| h | Heavy work: post-build review by fresh Sonnet (separate gate from the pre-build PLAN review in subagents.md §3). Input = diff file + the area files used. Each objection cites an ID or `skill:<name> step N`, else non-blocking. Accept or rebut; max 2 rounds; then one batched question (2–4 options) | Grade per project_instructions §2 |
| i | Heavy (mechanical): this session touched `tools/hooks/**`, `CLAUDE.md`, `docs/rules/**`, `.claude/skills/review-loop/**`, or > 5 repo files in total. decisions.md and a single SKILL.md edit do **not** count (session-end touches them every session). Stop **blocks once** (stop_hook_active prevents loops) if heavy and no review marker | Stop "warn" only logs; Claude never sees it |
| j | Accepted rebuttals → one friction line in ai-system-questions.md; reworded at weekly session-end | Reuse existing loop |
| k | Incremental migration: new rules go straight to docs/rules; an old rule moves when its file is edited; the rest by 2026-12-31. `storage` area **replaces** docs/storage_rules.md (old file → pointer, then removed) | No big-bang loss; no dual source |

## 3. Files
| File | Change |
|---|---|
| docs/rules/INDEX.md (new) | Columns: area, file, scope (1 line), trigger words, trigger paths, ID range |
| docs/rules/{security,log,mileage}.md (new, step 1) | First three areas; more as files are edited |
| CLAUDE.md | Now 3,183 chars (over the 3,000 cap). Moved rules → IDs; add INDEX pointer; end ≤ 3,000 |
| docs/kb/subagents.md | Brief line "rules to read"; replace the storage_rules.md line; note the two review gates |
| docs/decisions.md | One `D-YYYYMMDD-N` entry for this PLAN |
| tools/hooks/guard.py, tools/check.py | Add `docs/rules/` to the sensitive-scan SKIP lists (security.md describes emails/secrets) |
| tools/check.py | (1) every `R-*` cited in CLAUDE.md, skills, hooks, docs/rules exists (docs/requests excluded); (2) IDs unique; (3) every ID listed in INDEX's range; (4) INDEX lists every area file; (5) **char** budget: INDEX, area files ≤ 3k, CLAUDE.md ≤ 3k; (6) Appendix A fingerprints appear once under docs/rules and not in the old file. New messages in English |
| tools/hooks/area.py (new) | PostToolUse Read: if path under docs/rules/ (fast exit otherwise) record it in `usasia_area_<session>.json` (tempdir, per session, not cleared by stop.py; reset on SessionStart compact). PreToolUse Write/Edit: path → area, warn once if unread. UserPromptSubmit: trigger words → pointer once per area |
| tools/hooks/stop.py | heavy-review (decision i) using its own per-session state `usasia_heavy_<session>.json` (touch.py state is per turn and is deleted each Stop) |
| tools/hooks/review_mark.py (new) | Writes `usasia_review_<session>` marker; the skill calls it (session_id read from the latest hook state file) |
| tools/hooks/config.json | Rules `area-read`, `area-keyword`, `heavy-review`; separate `"ids"` map |
| .claude/skills/review-loop/SKILL.md (new) | Decision h steps: `git diff > <tempdir>/review.diff`, brief fresh Sonnet with rule paths + diff path, collect, accept/rebut, max 2 rounds, batch question, run review_mark.py |

## 4. Steps
| # | Step | Size | When |
|---|---|---|---|
| 1 | INDEX + security, log, expense (incl. mileage) area files from existing text; CLAUDE.md trim + pointer; guard/check SKIP for docs/rules; Appendix A filled with fingerprints. **Reviewed by fresh Sonnet manually** (subagents.md §3), since review-loop does not exist yet | heavy | done 2026-11-04 (freeze exception approved for the whole PLAN) |
| 2 | check.py checks (1)–(5) done 11/04 (fingerprint check (6) still manual) | light | done 2026-11-04 |
| 3 | review-loop skill + review_mark.py | light | done 2026-11-04 |
| 4 | area.py (keyword + path) warn, local settings only; 1 week hits.log | light | done 2026-11-04 (measure until ~11/11) |
| 5 | stop.py heavy-review (block once) | light | done 2026-11-04 |
| 6 | Move remaining rules as files are edited | ongoing | by 2026-12-31 |
| 7 | Evaluate: misses, false warnings, chars read per task | light | ~2 weeks after 4 |

## 5. How to check
- test_hooks.py twins: area-read (read then write = no warn; write unread = warn), area-keyword (출발 = hit; 출발점 in a sentence about something else = judge), heavy-review (hooks edit without marker = block; with marker = pass; decisions.md only = pass).
- check.py passes on the whole repo after step 1 and 2.
- Measure chars at task start on 3 tasks (log entry, mail triage, skill edit). Always-loaded counts CLAUDE.md + CLAUDE.local.md chain + MEMORY.md + digest; target ≤ 5k. Per task INDEX + 1–2 area files ≈ 6k.

## 6. Risks and limits
| Item | Note |
|---|---|
| Freeze D-20261103-7 (to ~11/17) | Step 1 only, with user OK; steps 3–5 after 11/17 |
| Hooks are local only (settings.local.json); cloud sessions get no area hooks until shared settings (Q2) | Cloud relies on CLAUDE.md pointer + INDEX |
| Read tracking gaps: `cat` via Bash not recorded; partial read counts as read; subagent Reads' session_id not checked | Warn only; reviewer is the second net |
| Opus skips INDEX on read-only answers | Not covered (no write, no keyword) |
| Two ID namespaces | `"ids"` map + check.py |
| Personal rules (mail_triage §0, Q8) | Stay in docs/users/<id>/ |

## Appendix A. Mapping (filled in step 1)
| Old location | Rule (short) | Fingerprint phrase | New ID |
|---|---|---|---|
| CLAUDE.md judgment rules; docs/storage_rules.md | Repo = secondary docs only | "GitHub holds secondary docs only: index" | R-SEC-01 |
| docs/storage_rules.md table | What never goes in the repo | "IP ranges, firewall settings, network diagrams" | R-SEC-02 |
| CLAUDE.md; D-20261102-16 | Sensitive values → Drive Claude folder | "inherited sharing off" | R-SEC-03 |
| CLAUDE.md; D-20261102-16 | Passwords stored nowhere | "stored nowhere: not in the repo" | R-SEC-04 |
| CLAUDE.md; storage_rules.md last line | Found one → leave out, suggest Drive | "recommend keeping this in Drive" | R-SEC-05 |
| CLAUDE.md Where things go; template | Log path, one person per file | "One file per person per day" | R-LOG-01 |
| CLAUDE.md; template | Entry heading + tags | "Each entry starts `### Title" | R-LOG-02 |
| template comment | Entry self-contained | "no \"that case\"" | R-LOG-03 |
| CLAUDE.md; template | Decisions only in decisions.md | "the log carries the decision ID" | R-LOG-04 |
| CLAUDE.md; D-20261102-11; D-20261105-1 | Dates in body; time zone | "never the machine clock" | R-LOG-05 |
| template comment | No sensitive values in logs | "No amounts, accounts, keys, IPs, serial numbers" | R-LOG-06 |
| CLAUDE.md | Hub on first entry; no history tables | "No hand-written history tables in hubs" | R-LOG-07 |
| template tip comment | Search before writing a tip | "Before writing a tip" | R-LOG-08 |
| D-20261104-1; Q17(2) | depart/arrive logged live | "are mileage events" | R-EXP-01 |
| reimbursement.md | Notion UTC → PT | "Notion stores UTC" | R-EXP-02 |
| reimbursement.md | Read Sheet row back first | "read the target row back" | R-EXP-03 |
| reimbursement.md | Empty miles | "No record for that route" | R-EXP-04 |
| reimbursement.md | Tabs, codes, lunch cap | "Lunch claim cap" | R-EXP-05 |
| reimbursement.md | Receipt intake | "file names are unreliable" | R-EXP-06 |
| reimbursement.md | Photo in chat | "connector upload needs inline base64" | R-EXP-07 |

## 7. Added 2026-11-04: docs that only grow (D-20261104-3)
| Kind | Docs | Fix | Done |
|---|---|---|---|
| State (open → closed) | todo.md, ai-system-questions.md | tools/prune.py moves closed rows to docs/archive/YYYY/ (session-end, todo-sync) | ✔ 11/04 (first run: 1 todo row, 4 past Now rows, 4 questions) |
| Record (append is right) | decisions.md, ARCHITECTURE.md | Never read whole: grep ID / last 5 lines; git diff | ✔ session-end edited |
| Reference (growth is normal) | orgs.md, facts.md | grep names; facts ≤ 3k | ✔ mail-triage edited |
| All always/daily-read | see check.py BUDGET | Soft char budgets in check.py; rule-ID checks (step 2) | ✔ 11/04 |
todo.md is still over budget (11.0k > 8k) because 끝 rows wait for STWS Closed; it shrinks after the next todo-sync.
