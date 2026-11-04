// Outlook web: collect message-list rows down to a cutoff date, without opening mail (no read-status change).
// Usage: set CUTOFF below, paste into javascript_tool, wait (browser_batch of wait 10),
// check `window._olDone`, then read `window._ol.slice(i, i+8).join('\n')` in slices (~1k chars per call).
// Rows: "Unread? | sender | subject | date | preview" with emails/phones/URLs masked.
window._olDone = false; window._ol = [];
(async () => {
  const CUTOFF = new Date('2026-10-01');            // stop when a row is older than this
  const clean = s => s.replace(/https?:\S+/g, '').replace(/\S+@\S+/g, '<e>')
    .replace(/\+?\d[\d\-\.\(\) ]{8,}\d/g, '<n>').replace(/[A-Za-z0-9%_\-]{25,}/g, '').replace(/[=&?]/g, ' ')
    .replace(/\s+/g, ' ').trim();
  let sc = document.querySelector('[role=listbox] [role=option]');
  while (sc && !(getComputedStyle(sc).overflowY == 'auto' && sc.scrollHeight > sc.clientHeight + 5)) sc = sc.parentElement;
  if (!sc) { window._olDone = 'no list'; return; }
  sc.scrollTop = 0; await new Promise(r => setTimeout(r, 1500));
  const seen = new Set(); let stop = false;
  for (let k = 0; k < 60 && !stop; k++) {
    for (const o of document.querySelectorAll('[role=listbox] [role=option]')) {
      const lab = clean(o.getAttribute('aria-label') || o.innerText);
      const key = lab.slice(0, 90); if (seen.has(key)) continue; seen.add(key);
      // Dates: "9/22/2026" (older) or "Tue 10/13" (recent, no year -> this year, or last year if in the future)
      const m = lab.match(/\b(\d{1,2})\/(\d{1,2})(?:\/(\d{4}))?\b/);
      if (m) {
        const now = new Date(); let d = new Date(m[3] ? +m[3] : now.getFullYear(), m[1] - 1, +m[2]);
        if (!m[3] && d > now) d.setFullYear(d.getFullYear() - 1);
        if (d < CUTOFF) { stop = true; break; }
      }
      window._ol.push(lab.slice(0, 160));
    }
    const before = sc.scrollTop; sc.scrollTop += sc.clientHeight * 0.8;
    await new Promise(r => setTimeout(r, 1200));
    if (sc.scrollTop === before) break;             // end of list
  }
  window._olDone = true;
})();
'started';
