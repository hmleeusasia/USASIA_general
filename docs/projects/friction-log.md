# Friction log — inefficiencies found in sessions  #proj-ai-system
<!-- D-20261106-8. Every session end appends its lines here (session-end A.3), from every account.
     Teammate accounts only record; the admin (hmlee) patches them in the weekly review (session-end B.5)
     and moves handled lines to docs/archive/<YYYY>/friction-log_done.md with the fix (commit or decision ID).
     Append only at the bottom; never edit or delete another person's line (only the admin moves handled lines, in B.5, right after a pull). No sensitive values (R-SEC-02..05). -->

Format: `- YYYY-MM-DD · <user id> · <where: local/cloud> · <what was slow or wasted> · <cause> · <candidate fix>`
Keep Open short: the weekly review empties it. A session with nothing found adds: `- YYYY-MM-DD · <user id> · <where> · none found`

## Open
- 2026-11-05 · hmlee · local · STWS ticket creation takes ~10–12 browser calls per ticket (10 tickets that day) · manual click path · one browser script like tools/browser/outlook_list.js; needs live testing (deferred in D-20261105-8)
- 2026-11-06 · hmlee · local · usasia_db tests only run in CI (5–6 min per try); db/schema.rb written by hand · no Ruby on the PC · run tests in a cloud session or a container on the server; or let CI commit the regenerated schema.rb
- 2026-11-06 · hmlee · local · Python heredoc edits of Ruby files broke on regex escapes; Edit refused files not Read first → extra round trips · shell-scripted multi-file edits · use Read + Edit for code with regexes; reserve heredoc scripts for plain text
- 2026-11-06 · hmlee · local · tools/hooks/review_mark.py without a session ID marked the newest state file, maybe another session's · no session ID passed · pass the session ID from the review-loop skill, or have the hook mark by current session automatically
- 2026-11-06 · hmlee · local · production deploy after "오케이" was blocked by the auto-mode safety check, one extra question · approval was not explicit · ask with an explicit deploy button (as done after) and wait for it before merging to main
- 2026-11-06 · hmlee · local · inefficiency notes were not written at session end · session-end A.3 only said "note friction" and the weekly table was the only fixed place · this file + D-20261106-8
- 2026-11-06 · hmlee · local · usasia_db tools/docs/gen_handbook.py --help regenerated the pages instead of printing help · the script has no help flag and treats unknown args as a normal run · add argparse with --help, or refuse unknown args
- 2026-11-06 · hmlee · local · PowerShell [IO.File] calls used the process cwd (USASIA_general), not the repo cd'd into, and inline python -c with nested quotes failed → 3 retries · shell quoting across PowerShell/Python · use Edit for code, Bash heredoc + script file for bulk text edits
- 2026-11-06 · hmlee · local · background "wait for CI" commands reported failed twice although CI passed (gh run watch got split args) · PowerShell quoting of the run ID · use Bash for gh polling one-liners
- 2026-11-06 · hmlee · local · no Ruby on the local PC, so 2 test bugs surfaced only on the first CI run (one extra push and wait) · tests run only in CI · consider Ruby (or a container) locally for usasia_db, or accept CI as the test runner
- 2026-11-06 · hmlee · local · Python string edits wrote a token path with "\t" as a real tab in the study note → 2 extra fix commits · backslashes in non-raw Python strings inside heredocs · use Edit for lines with Windows paths or regexes
- 2026-11-06 · hmlee · local · a long Bash heredoc with mixed quotes failed (unexpected EOF) → rewrote it as a scratchpad script · heredoc quoting in Git Bash · write multi-line scripts to the scratchpad with Write, then run them
- 2026-11-06 · hmlee · local · gave the user a Git Bash curl command; in Windows PowerShell curl is an Invoke-WebRequest alias → error, one extra round trip · user shell not checked · give PowerShell commands (curl.exe) to this user by default
- 2026-11-06 · hmlee · local · usasia_db page text "your own todos. Keep" failed the query allow-list scan → one extra CI cycle · the scan reads view prose as code · avoid "todos." in view text, or have the scan skip ERB text outside tags
- 2026-11-06 · hmlee · local · test helpers took keyword args next to a token: keyword → 13 CI errors and one extra CI cycle (~5 min) · no local Ruby, Ruby 3 keyword rules missed · same as earlier line: local Ruby/container or a quick syntax/test run before push
- 2026-11-06 · hmlee · local · wrote 2026-11-07 (UTC from CI logs) as today in the study note and CURRENT_STATE; caught only at session end · machine/UTC dates leaked in · take "today" from the digest line before writing any date
- 2026-11-06 · hmlee · local · USASIA_general handbook pre-commit (meta.json for new tools/*.py) found only at commit time → second pass of docstrings + re-pin · check not run before commit · run py tools/handbook.py right after adding a tools/ file
- 2026-11-06 · hmlee · local · a Python heredoc replace failed silently-matched on "
" text and stopped the whole patch → redone with Edit · backslash escapes in heredoc replacements (repeat of an earlier line) · use Edit for lines containing 
 or regexes
- 2026-11-06 · hmlee · local · usasia_db step 6 pushed straight to main; Deploy runs on green main CI, so it deployed without the chat approval used in steps 4-5 · deploy gate lives only in habit, not in the workflow · push to a claude/* branch first, ask, then fast-forward main (or add a protected environment)
- 2026-11-07 · hmlee · local · review_mark.py with no session id marked another session (784ba25a) as reviewed · it picks the newest heavy-state file · require the id when more than one heavy-state file is open
- 2026-11-07 · hmlee · local · step 6 journal gave a server round-trip recipe (DATABASE_URL + db:schema:load) that could overwrite the production DB; caught only when about to run it · recipes for the live server were written without checking how the app runs there (Kamal container, multi-DB) · journal/handbook server commands get the same review as code; prefer a throwaway container
- 2026-11-07 · hmlee · local · server docker exec (export) was blocked by the auto-mode permission check, so the user ran 4 commands by hand with extra round trips · no allow rule for read-mostly ssh HML commands · decide whether to allow a narrow ssh HML rule or keep server runs with the user
- 2026-11-07 · hmlee · local · Python edits inside a bash heredoc turned \n into real newlines and broke a YAML line and a shell printf; Edit failed twice on files not Read first · escaping through two layers · use Edit for multi-line or escaped text; Read before Edit
