#!/usr/bin/env python3
"""문서 점검 (Windows·Mac·Linux 공통): python3 tools/check.py
미등록 태그, 허브 없는 대상 태그, 민감 정보 의심, CURRENT_STATE·facts 줄 수."""
import re, sys, pathlib
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "docs"
HUB = {"vendor": "vendors", "store": "stores", "asset": "assets", "proj": "projects"}
SENS = re.compile(r"\$ ?\d|\b\d{1,3}(\.\d{1,3}){3}\b|([0-9A-Fa-f]{2}:){5}|password|passwd|비밀번호|api[_-]?key", re.I)
SKIP = ("storage_rules.md", "templates", "keywords.md", "requests", "session_review.md")
problems = []

logs = [f for d in ("log", "archive") for f in (D / d).rglob("*.md")]
known = set(re.findall(r"#[a-z][a-z0-9-]*", (D / "keywords.md").read_text(encoding="utf-8")))
tags = {t for f in logs for t in re.findall(r"(?<![\w#])#[a-z][a-z0-9-]*", f.read_text(encoding="utf-8"))}
for t in sorted(tags):
    m = re.match(r"#(vendor|store|asset|proj)-(.+)", t)
    if m and t not in ("#store-ops", "#vendor-mgmt"):
        hub = D / HUB[m[1]] / f"{m[2]}.md"
        if not hub.exists(): problems.append(f"허브 없음: {t} → {hub.relative_to(ROOT)}")
    elif t not in known:
        problems.append(f"미등록 태그: {t}")

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
for f in D.rglob("*.md"):
    if any(s in f.parts or f.name == s for s in SKIP): continue
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if SENS.search(line): problems.append(f"민감 정보 의심: {f.relative_to(ROOT)}:{i}: {line.strip()[:60]}")
        if EMAIL.search(line): problems.append(f"이메일 주소: {f.relative_to(ROOT)}:{i}: {EMAIL.search(line).group()} → 드라이브 Claude 폴더로 (D-20261102-16)")

for sub in ("kb", "drive-index"):
    idx = (D / sub / "INDEX.md").read_text(encoding="utf-8")
    for f in (D / sub).glob("*.md"):
        if f.name != "INDEX.md" and f.name not in idx: problems.append(f"INDEX 누락: docs/{sub}/{f.name}")

for name, limit in (("CURRENT_STATE.md", 80), ("kb/facts.md", 50)):
    n = len((D / name).read_text(encoding="utf-8").splitlines())
    if n > limit: problems.append(f"{name} {n}줄 > {limit}")

print("\n".join(problems) if problems else f"점검 통과 (기록 파일 {len(logs)}개)")
sys.exit(1 if problems else 0)
