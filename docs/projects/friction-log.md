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
