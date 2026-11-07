---
name: review-loop
description: Post-build review of heavy work by a fresh Sonnet — diff + rule files in, objections citing rule IDs out, accept or rebut, max 2 rounds, then one batched question to the user. Use when the Stop hook says "heavy-review", before committing heavy work (tools/, CLAUDE.md, docs/rules, skills, settings, > 15 files), or when the user says "검토", "리뷰", "review".
---
# review-loop (D-20261104-2 decision h)
Pre-build review of a PLAN is a separate gate (docs/kb/subagents.md §3). This one checks what was actually built.

## 1. Prepare (main session)
1. List the rule files the work used (from the task announcement; docs/rules/INDEX.md). Add the PLAN path if there is one.
2. Write the diff for the reviewer: `git diff HEAD > <tempdir>/review.diff` and `git status --short >> <tempdir>/review.diff` (untracked files: name them in the brief). Windows temp: `py -c "import tempfile;print(tempfile.gettempdir())"`. Quote paths with spaces.
3. Do **not** send your own summary or reasoning — the reviewer judges the diff, not the narrative.

## 2. Brief (fresh Sonnet, general-purpose, new agent every review)
- Repo path; "do not edit or commit files"; rules to read: <rule file paths>; diff file: <path>; untracked files: <list>.
- Checks: rule violations, things lost or changed in meaning, checks that pass for the wrong reason, missing tests; run `py tools/check.py` and `py tools/hooks/test_hooks.py` if code changed.
- Every objection cites a rule ID (`R-…`), a decision ID, a PLAN decision/step, or `skill:<name> step N`. No citation → mark it "suggestion" (non-blocking).
- Output: must / should / fine with file:line, under 500 words.

## 3. Answer (main session)
- Verify each must/should yourself (open the file) before acting — the report is not proof.
- Accept → fix. Rebut → one line why, with evidence (file:line, test output).
- Round 2 only if something was rebutted or a fix was large: send the rebuttals and the new diff to the **same** reviewer (SendMessage). No round 3.
- Still disagreed after round 2 → one batched question to the user: a table (point, reviewer, me, options), 2–4 options, recommendation first.
- An accepted rebuttal means a rule is unclear → one friction line in docs/projects/friction-log.md (D-20261106-8).

## 4. Close
1. `py tools/hooks/review_mark.py [session_id]` (marks this session as reviewed; the Stop hook stops reminding). Without an ID it takes the newest heavy-state file — pass the ID when two sessions run at once.
2. Report to the user: table of objections → accepted / rebutted / asked; what was not checked.
3. Commit message names the review ("fresh-Sonnet review: …").
