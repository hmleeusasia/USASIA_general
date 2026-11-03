#!/usr/bin/env python3
"""기록 검색. 사용:
  python3 tools/find.py <단어|#태그> [...]   모두 포함한 건만 (AND, 대소문자 무시). 결정 기록도 함께 검색
  python3 tools/find.py --open               열린 건(#open/#waiting) + 확인일, 지난 것은 [기한초과]
  python3 tools/find.py --due                앞으로 30일 안의 날짜(확인일·다음·기한) + calendar.md
동의어는 docs/keywords.md 표에서 자동 확장. 3자 이하 영문은 단어 단위로 찾는다.
### 없는 파일(월별 요약 등)은 파일 전체를 한 건으로 본다."""
import re, sys, pathlib, datetime
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = [ROOT/"docs/log", ROOT/"docs/archive"]
TODAY = datetime.date.today()
DATE = re.compile(r"(확인일|다음)[^\n]*?(\d{4}-\d{2}-\d{2})")

def synonyms():
    groups = []
    for line in (ROOT/"docs/keywords.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(#[\w-]+)\s*\|(.*)\|", line)
        if m:
            groups.append([m[1]] + [a.strip() for a in m[2].split(",") if a.strip()])
    return groups

def pattern(word, groups):
    w = word.lstrip("#").lower()
    alts = next((g for g in groups if any(a.lstrip("#").lower() == w for a in g)), [word])
    parts = []
    for a in alts:
        e = re.escape(a)
        parts.append(rf"(?<![A-Za-z0-9-]){e}(?![A-Za-z0-9-])" if re.fullmatch(r"[A-Za-z0-9]{1,3}", a) else e)
    return re.compile("|".join(parts), re.I)

def entries():
    for d in DIRS:
        for f in sorted(d.rglob("*.md")):
            lines = f.read_text(encoding="utf-8").splitlines()
            rel = f.relative_to(ROOT)
            if not any(l.startswith("### ") for l in lines):
                if lines: yield rel, 1, "#"*3 + " " + lines[0].lstrip("# "), "\n".join(lines)
                continue
            head = None
            for i, line in enumerate(lines + ["### "], 1):
                if line.startswith("### "):
                    if head: yield rel, *head, "\n".join(body)
                    head, body = (i, line), [line]
                elif head: body.append(line)

def dates(body):
    return [(k, datetime.date.fromisoformat(d)) for k, d in DATE.findall(body)]

def main(args):
    if not args: print(__doc__); return 1
    if args == ["--open"]:
        n = 0
        for f, i, h, b in entries():
            if "summary" in f.name or not re.search(r"#(open|waiting)\b", h): continue
            ds = dates(b); late = any(d < TODAY for k, d in ds if k in ("확인일", "기한"))
            print(f"{'[기한초과] ' if late else ''}{f}:{i}: {h[4:]}" + "".join(f"  ({k} {d})" for k, d in ds)); n += 1
        if not n: print("열린 건 없음")
        return
    if args == ["--due"]:
        end = TODAY + datetime.timedelta(days=30); out = []
        for f, i, h, b in entries():
            if not re.search(r"#done\b", h):
                out += [(d, f"{k}: {h[4:]}  ({f}:{i})") for k, d in dates(b) if d <= end]
        for line in (ROOT/"docs/calendar.md").read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)", line)
            if m and datetime.date.fromisoformat(m[1]) <= end: out.append((datetime.date.fromisoformat(m[1]), "calendar:" + m[2]))
        for d, t in sorted(out): print(f"{'[지남] ' if d < TODAY else ''}{d} {t}")
        if not out: print("30일 안 일정 없음")
        return
    g = synonyms(); pats = [pattern(a, g) for a in args]
    hits = [(f, n, h) for f, n, h, b in entries() if all(p.search(b) for p in pats)]
    for f, n, h in hits: print(f"{f}:{n}: {h[4:]}")
    for line in (ROOT/"docs/decisions.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("- D-") and all(p.search(line) for p in pats):
            hits.append(1)
            print(("[대체됨] " if re.search(r"→ 대체: D-\d{8}-\d+\s*$", line) else "") + "결정 " + line[2:])
    if not hits: print("결과 없음")

sys.exit(main(sys.argv[1:]))
