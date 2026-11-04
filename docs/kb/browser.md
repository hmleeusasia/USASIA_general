# Browser use with small context (Claude in Chrome)
Read before any Chrome task. Tested 2026-11-03 (Outlook sent mail, 3 months).

## Rules
1. **Text before pictures.** Order: `javascript_tool` (summarize in the page) → `find` + `read_page(ref)` → `get_page_text` → screenshot (last, scale ≤ 0.6).
2. **Do not scroll with `computer scroll`** — each scroll returns a full screenshot. Scroll the list container in JS (`el.scrollTop += el.clientHeight*0.8`).
3. **`javascript_tool` output is cut at ~1,000 chars.** Store results in `window._x`, then read in slices; put several slice reads in one `browser_batch`.
4. **Long loops (> ~40 s) time out.** Start them async (`(async()=>{…; window._done=true})()`), then `browser_batch` of `wait 10` ×N + one status check.
5. **Output with URLs / `?=&` / long tokens is blocked** ("Cookie/query string data"). Strip them in JS before returning: `s.replace(/https?:\S+/g,'').replace(/[A-Za-z0-9%_\-]{25,}/g,'').replace(/[=&?]/g,' ')`.
6. **Mask in the page, not after:** replace emails and phone numbers in JS (`/\S+@\S+/g`, `/\+?\d[\d\-\.\(\) ]{8,}\d/g`) so they never enter context.
7. `read_page` of a whole reading pane is verbose (UI tree); prefer `innerText` of the pane via JS, cut to what you need (e.g. my own message's first 260 chars).
8. Bulk reading of many pages → one pass with a JS loop, return a table; or a subagent if no browser is needed. Results go to a file; chat gets the conclusion.

## Ready scripts
- Outlook list (no clicks, does not mark read): `tools/browser/outlook_list.js` — paste into `javascript_tool`, then read `window._ol` in slices.
