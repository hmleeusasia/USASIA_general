#!/usr/bin/env python3
"""Move closed rows out of state docs so always-read files do not grow (D-20261104-3).

  py tools/prune.py            # dry run: show what would move
  py tools/prune.py --apply    # move rows
  options: --user <id> (default from CLAUDE.local.md), --today YYYY-MM-DD, --days N (default 2)

Rules
- todo.md section 2: status 끝/취소/Done/Cancelled (STWS Resolved or Cancelled; STWS "Closed" is not tracked) and last
  move >= N days ago -> docs/archive/YYYY/todo_<id>_closed.md
- todo.md section 1 "Now": rows whose day (M/D) is before today -> archive file (Dec run: January rows count as next year)
- todo.md section 4 sync notes: keep the newest 5 lines, older -> archive file
- docs/projects/ai-system-questions.md: rows whose last cell has "→ D-" and no "open" -> archive file
"""
import re, sys, pathlib, datetime
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "docs"
CLOSED = {"끝", "취소", "done", "cancelled", "closed"}
KEEP_SYNC = 5


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def user_id():
    u = arg("--user")
    if u: return u
    p = ROOT / "CLAUDE.local.md"
    m = re.search(r"docs/users/([^/]+)/CLAUDE\.md", p.read_text(encoding="utf-8")) if p.exists() else None
    if not m: sys.exit("No user: pass --user <id>")
    return m.group(1)


def today(uid):
    t = arg("--today")
    if t: return datetime.date.fromisoformat(t)
    prof = D / "users" / uid / "profile.md"
    m = re.search(r"(America|Asia|Europe)/[A-Za-z_]+", prof.read_text(encoding="utf-8")) if prof.exists() else None
    if m:
        try:
            from zoneinfo import ZoneInfo
            return datetime.datetime.now(ZoneInfo(m.group(0))).date()
        except Exception:
            pass  # no tz database (Windows without tzdata): local clock; the local PC is in the user's zone
    return datetime.date.today()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def sections(lines):
    """Yield (heading, start, end) for each '## ' section."""
    idx = [i for i, l in enumerate(lines) if l.startswith("## ")] + [len(lines)]
    for a, b in zip(idx, idx[1:]):
        yield lines[a], a, b


def prune_todo(path, now, days):
    lines = path.read_text(encoding="utf-8").splitlines()
    out, moved, dropped, sync_old = [], [], [], []
    drop = set()
    for head, a, b in sections(lines):
        if head.startswith("## 1."):
            for i in range(a, b):
                c = cells(lines[i]) if lines[i].startswith("|") else []
                m = re.search(r"\b(\d{1,2})/(\d{1,2})\b", c[0]) if c else None
                if m:
                    try:
                        d = datetime.date(now.year, int(m[1]), int(m[2]))
                    except ValueError:
                        continue
                    if (now - d).days > 180:  # late-December run, January row → next year
                        d = d.replace(year=now.year + 1)
                    if d < now:
                        drop.add(i); dropped.append(lines[i])
        elif head.startswith("## 2."):
            for i in range(a, b):
                c = cells(lines[i]) if lines[i].startswith("| ") else []
                if len(c) < 7 or not re.match(r"[A-Z]+-", c[0]): continue
                st = c[4].split("(")[0].strip().lower()
                m = re.search(r"\d{4}-\d{2}-\d{2}", c[5])
                # 끝/Done counts only once STWS says Closed (Resolved still waits for the user); 취소 is final
                # STWS Resolved/Cancelled is final; closing in STWS is not tracked (user, 2026-11-04)
                if st in CLOSED and m:
                    if (now - datetime.date.fromisoformat(m[0])).days >= days:
                        drop.add(i); moved.append(lines[i])
        elif head.startswith("## 4."):
            notes = [i for i in range(a, b) if lines[i].startswith("- ")]
            for i in notes[:-KEEP_SYNC] if len(notes) > KEEP_SYNC else []:
                drop.add(i); sync_old.append(lines[i])
    out = [l for i, l in enumerate(lines) if i not in drop]
    return out, moved, dropped, sync_old


def prune_questions(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    moved, keep = [], []
    for l in lines:
        c = cells(l) if l.startswith("| Q") else []
        if c and "→ D-" in c[-1] and not re.search(r"\bopen\b|미정|pending", c[-1], re.I):
            moved.append(l)
        else:
            keep.append(l)
    return keep, moved


def archive(name, header, rows, now, apply):
    p = D / "archive" / str(now.year) / name
    if apply and rows:
        p.parent.mkdir(parents=True, exist_ok=True)
        new = not p.exists()
        with p.open("a", encoding="utf-8", newline="\n") as f:
            if new: f.write(f"# {name[:-3]} (moved by tools/prune.py)\n")
            f.write(f"\n## {now.isoformat()}\n{header}\n" + "\n".join(rows) + "\n")
    return p.relative_to(ROOT)


def main():
    apply = "--apply" in sys.argv
    uid = user_id(); now = today(uid); days = int(arg("--days", 2))
    report = []
    todo = D / "users" / uid / "todo.md"
    if todo.exists():
        before = len(todo.read_text(encoding="utf-8"))
        out, moved, dropped, sync_old = prune_todo(todo, now, days)
        hdr = "| ID | 할 일 | 매장 | 분야 | 상태 | 움직임 | 다음 |\n|---|---|---|---|---|---|---|"
        a = archive(f"todo_{uid}_closed.md", hdr, moved, now, apply)
        archive(f"todo_{uid}_closed.md", "Past Now rows (dropped from section 1):", dropped, now, apply)
        archive(f"todo_{uid}_closed.md", "Sync notes:", sync_old, now, apply)
        if apply and (moved or dropped or sync_old):
            todo.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
        after = len("\n".join(out)) + 1
        report.append(f"todo.md: {len(moved)} closed rows → {a}; {len(dropped)} past Now rows dropped; "
                      f"{len(sync_old)} old sync notes archived; {before} → {after} chars")
        report += [f"  move: {r[:90]}" for r in moved] + [f"  drop: {r[:90]}" for r in dropped]
    q = D / "projects" / "ai-system-questions.md"
    if q.exists():
        keep, moved = prune_questions(q)
        a = archive("ai-system-questions_closed.md", "| # | 고민 | 나온 날 | 지금 상태·제안 |\n|---|---|---|---|", moved, now, apply)
        if apply and moved:
            q.write_text("\n".join(keep) + "\n", encoding="utf-8", newline="\n")
        report.append(f"ai-system-questions.md: {len(moved)} closed questions → {a}")
        report += [f"  move: {r[:90]}" for r in moved]
    print(("APPLIED" if apply else "DRY RUN (use --apply)") + f" · user {uid} · today {now}")
    print("\n".join(report))


if __name__ == "__main__":
    main()
