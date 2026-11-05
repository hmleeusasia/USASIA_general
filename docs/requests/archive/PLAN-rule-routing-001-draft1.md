# PLAN-rule-routing-001-draft1 (Opus + Sonnet 2 rounds, 2026-11-04 — awaiting review and user approval)
Related: PLAN-lean-context-001-draft2 (layers, hooks), D-20261103-6/7, ai-system-questions Q2, Q8, Q17(2).

## 1. Request (user, 2026-11-04)
Rules grow without bloating always-loaded md. Before work, only the rules the task needs are read. A supervisor makes sure the needed rules reach the executor; after work a reviewer checks the result critically; executor accepts or rebuts; unresolved points go to the user.

## 2. Decisions (agreed in chat 2026-11-04)
| # | Decision | Why |
|---|---|---|
| a | Rules live in `docs/rules/<area>.md` (1–3k chars each) + one `docs/rules/INDEX.md` area table (≤ 3k chars). Not one big file | No line-number pointers, fewer git conflicts, one folder = one source |
| b | One heading per rule with a stable ID: `## R-<AREA>-NN`. IDs never reused. Hook rule names map to IDs in config.json (one namespace) | Logs, reviews and hooks cite IDs |
| c | **Opus (main session) is the conductor.** At the task announcement (CLAUDE.md Session 2) it reads INDEX, names the areas, reads those area files. No separate conductor agent | Opus has the conversation context; a fresh agent does not (Sonnet r2 #5) |
| d | Opus passes rule file paths in every subagent brief ("read docs/rules/log.md, security.md") | Subagents know only the brief |
| e | Supervisor = hooks + reviewer, not a model. Path hook: file written → area; if that area file was not read this session, warn once | Catches skipped reads (Q17(2) type miss) |
| f | Procedures stay in skills and cite IDs. Only cross-skill or hook-enforced rules move to docs/rules. Skill-local rules stay in the skill. Personal rules stay in docs/users/<id>/ | Avoid splitting rules from their steps (Sonnet r2 #4) |
| g | Always-loaded CLAUDE.md keeps: session flow + announce/approve, security/storage, new contact → ask now, language, pointer to docs/rules/INDEX.md. Irreversible-action rules never depend on a lookup | Sonnet r2 #7 |
| h | Heavy work only: post-build review by fresh Sonnet. Input = diff (scratchpad file) + the area files used. Each objection cites an ID or `skill:<name> step N`; otherwise non-blocking. Executor accepts or rebuts. Max 2 rounds, then one batched question to the user (2–4 options) | Grade per project_instructions §2 |
| i | Heavy is derived from touched paths (touch.py): `.claude/skills/**`, `tools/hooks/**`, `CLAUDE.md`, `docs/decisions.md`, `docs/rules/**`, or > 5 repo files. Stop hook warns once if heavy and no review note in scratchpad | Grade is only in chat (Sonnet r1 #7) |
| j | Accepted rebuttals = unclear rule → one friction line in ai-system-questions.md, reworded at weekly session-end | Reuse existing loop |
| k | Migration is incremental with a deadline: new rules go straight to docs/rules; an old rule moves when its file is edited; all remaining moved by 2026-12-31 | No big-bang loss; no endless dual system |

## 3. Files
| File | Change |
|---|---|
| docs/rules/INDEX.md (new) | Area table: area, file, one-line scope, trigger paths/keywords, ID range |
| docs/rules/<area>.md (new) | Start set (temporary): security, storage, log, contacts, git, messages, browser, mileage |
| CLAUDE.md | Replace moved judgment rules with IDs; add "read docs/rules/INDEX.md at task announcement"; stay ≤ 3,000 chars |
| docs/project_instructions.md | Rules part → docs/rules; keep principles only |
| .claude/skills/*/SKILL.md | When edited: cite IDs instead of restating cross-skill rules |
| tools/hooks/config.json | Add `area-read` (warn), `heavy-review` (warn); map hook rule names → IDs |
| tools/hooks/area.py (new) | PostToolUse Read: record area files read this session. PreToolUse Write/Edit: path → area; warn once if area file not read |
| tools/hooks/stop.py | heavy-review check (decision i) |
| tools/check.py | Every `R-*` cited in skills/CLAUDE.md/hooks exists; IDs unique; INDEX lists every area file; INDEX ≤ 3k, area file ≤ 3k |
| .claude/skills/review-loop/SKILL.md (new) | Steps of decision h: write diff to scratchpad, brief fresh Sonnet with rule paths, collect objections, accept/rebut, max 2 rounds, batch question |
| docs/kb/subagents.md | Brief template line: "rules to read: <paths>" |

## 4. Steps
| # | Step | Size |
|---|---|---|
| 1 | docs/rules/INDEX.md + 3 first area files (security, log, mileage) from existing text; CLAUDE.md points to them; mapping table old location → ID in this PLAN's appendix | heavy |
| 2 | check.py ID checks + test fixtures | light |
| 3 | area.py hook in warn, local settings only; 1 week of hits.log | light |
| 4 | review-loop skill; try on one real heavy task | light |
| 5 | stop.py heavy-review warn | light |
| 6 | Move remaining rules as files are edited; deadline 2026-12-31 | ongoing |
| 7 | Evaluate (~2 weeks after step 3): misses, false warnings, chars read per task | light |

## 5. How to check
- test_hooks.py: hit/no-hit twins for area-read and heavy-review.
- check.py passes on the whole repo after step 1.
- Mapping table: every moved rule line appears once in docs/rules, and its old location keeps only the ID.
- Measure: chars read at task start before/after on 3 typical tasks (log entry, mail triage, skill edit). Target: always-loaded ≤ 5k; per task INDEX + 1–2 area files ≈ 6k.

## 6. Risks and questions
| Risk / question | Note |
|---|---|
| D-20261103-7 freeze on new skills/decisions until ~11/17 | Step 1 fixes real friction (Q17(2) mileage rule missed); steps 3–5 after 11/17 unless the user says otherwise |
| Hooks still in settings.local.json; who approves shared hooks (Q2) | Unchanged by this PLAN; area.py follows the same path |
| Opus skips reading INDEX | area.py warns on write; reviewer checks omitted areas on heavy work. Read-only answers are not covered |
| Context compaction drops rules read earlier | Re-read the area file per task (small) |
| Two ID namespaces (hook names vs R-*) | Mapping in config.json; check.py verifies |
| Personal rules (mail_triage §0, Q8) | Stay in docs/users/<id>/; not in docs/rules |

## Appendix A. Mapping table (filled in step 1)
| Old location | Rule (short) | New ID |
|---|---|---|
