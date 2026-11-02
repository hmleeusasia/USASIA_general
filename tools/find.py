#!/usr/bin/env python3
"""기록 검색. 사용:
  python3 tools/find.py <단어|#태그> [...]   모두 포함한 건만 (AND, 대소문자 무시)
  python3 tools/find.py --open               열린 건(#open/#waiting)
동의어는 docs/keywords.md 표에서 자동 확장. 3자 이하 영문은 단어 단위로 찾는다."""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = [ROOT/"docs/log", ROOT/"docs/archive"]

def synonyms():
    groups = []
    for line in (ROOT/"docs/keywords.md").read_text().splitlines():
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
            head = None
            for i, line in enumerate(f.read_text().splitlines() + ["### "], 1):
                if line.startswith("### "):
                    if head: yield f.relative_to(ROOT), *head, "\n".join(body)
                    head, body = (i, line), [line]
                elif head: body.append(line)

def main(args):
    if not args: print(__doc__); return 1
    if args == ["--open"]:
        pats = [re.compile(r"#(open|waiting)\b")]
    else:
        g = synonyms(); pats = [pattern(a, g) for a in args]
    hits = [(f, n, h) for f, n, h, b in entries() if all(p.search(b) for p in pats)]
    for f, n, h in hits: print(f"{f}:{n}: {h[4:]}")
    if args != ["--open"]:
        for line in (ROOT/"docs/decisions.md").read_text().splitlines():
            if line.startswith("- D-") and all(p.search(line) for p in pats):
                hits.append(1); print(("[대체됨] " if "대체: D-" in line else "") + "결정 " + line[2:])
    if not hits: print("결과 없음")

sys.exit(main(sys.argv[1:]))
