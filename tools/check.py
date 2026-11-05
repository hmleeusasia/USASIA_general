#!/usr/bin/env python3
"""문서 점검 (Windows·Mac·Linux 공통): python3 tools/check.py
미등록 태그, 허브 없는 대상 태그, 민감 정보 의심, CURRENT_STATE·facts 줄 수."""
import re, sys, pathlib
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "docs"
HUB = {"vendor": "vendors", "store": "stores", "asset": "assets", "proj": "projects"}
SENS = re.compile(r"\b\d{1,3}(\.\d{1,3}){3}\b|([0-9A-Fa-f]{2}:){5}|(password|passwd|비밀번호|api[_-]?key)\s*[:=]\s*\S+", re.I)  # words only next to a value (2026-11-05)
SKIP = ("storage_rules.md", "rules", "templates", "keywords.md", "requests")
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

# Rule IDs (D-20261104-2): defined once in docs/rules, cited IDs exist, INDEX ranges match.
RID = re.compile(r"\bR-([A-Z]+)-(\d{2})\b")
RULES = D / "rules"
defined = {}
if RULES.exists():
    for f in RULES.glob("*.md"):
        if f.name == "INDEX.md": continue
        for m in re.finditer(r"^## (R-[A-Z]+-\d{2})\s*$", f.read_text(encoding="utf-8"), re.M):
            if m[1] in defined: problems.append(f"Rule ID defined twice: {m[1]} in docs/rules/{f.name} and {defined[m[1]]}")
            defined[m[1]] = f"docs/rules/{f.name}"
    idx = (RULES / "INDEX.md").read_text(encoding="utf-8")
    for f in RULES.glob("*.md"):
        if f.name != "INDEX.md" and f.name not in idx: problems.append(f"Rule file not in docs/rules/INDEX.md: {f.name}")
    for area, a, b in re.findall(r"\bR-([A-Z]+)-(\d{2})\.\.(\d{2})\b", idx):
        want = {f"R-{area}-{n:02d}" for n in range(int(a), int(b) + 1)}
        have = {k for k in defined if k.startswith(f"R-{area}-")}
        if want != have: problems.append(f"docs/rules/INDEX.md range R-{area}-{a}..{b} does not match defined {sorted(have)}")
    cite_files = [ROOT / "CLAUDE.md", *ROOT.glob(".claude/skills/*/SKILL.md"), *(ROOT / "tools" / "hooks").glob("*.py"),
                  *RULES.glob("*.md"), *(D / "kb").glob("*.md"), *(D / "templates").glob("*.md"), *(D / "users").rglob("*.md")]
    for f in cite_files:
        txt = f.read_text(encoding="utf-8")
        for m in RID.finditer(txt):
            rid = f"R-{m[1]}-{m[2]}"
            if rid not in defined and not txt[m.end():m.end() + 2] == "..":
                problems.append(f"Unknown rule ID: {rid} in {f.relative_to(ROOT)}")

# Char budgets for always/daily-read docs (D-20261104-3). Soft: shown as (warn), never blocks.
BUDGET = {"CLAUDE.md": 3000, "docs/rules/*.md": 3000, "docs/users/*/CLAUDE.md": 1000, "docs/users/*/todo.md": 8000,
          "docs/kb/facts.md": 3000, "docs/kb/INDEX.md": 3000, "docs/CURRENT_STATE.md": 5000,
          "docs/projects/ai-system-questions.md": 4000}
for pat, limit in BUDGET.items():
    for f in ROOT.glob(pat):
        n = len(f.read_text(encoding="utf-8"))
        if n > limit: problems.append(f"Over char budget: {f.relative_to(ROOT)} {n} > {limit} (prune closed items: tools/prune.py; shorten long rows)")
for f in ROOT.glob("docs/users/*/todo.md"):  # long open rows grow the board; prune never touches them (2026-11-05)
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and len(line) > 400:
            problems.append(f"Over char budget: long todo row {f.relative_to(ROOT)} {line.split('|')[1].strip()} {len(line)} chars > 400 → one line, details to the log")

# --files a b c : only problems about these files (pre-commit). Soft "민감 정보 의심" is shown, not counted.
if "--files" in sys.argv:
    files = [a.replace("\\", "/") for a in sys.argv[sys.argv.index("--files") + 1:]]
    ftags = set()
    for a in files:
        p = ROOT / a
        if p.suffix == ".md" and p.exists():
            ftags |= set(re.findall(r"(?<![\w#])#[a-z][a-z0-9-]*", p.read_text(encoding="utf-8")))
    def mine(pr):
        if pr.startswith(("허브 없음", "미등록 태그")):
            return pr.split(": ")[1].split(" ")[0] in ftags
        return any(a in pr.replace("\\", "/") or a.endswith(pr.split(" ")[0]) for a in files)
    problems = [pr for pr in problems if mine(pr)]
    soft = [pr for pr in problems if pr.startswith(("민감 정보 의심", "Over char budget"))]
    hard = [pr for pr in problems if pr not in soft]
    if soft: print("(warn) " + "\n(warn) ".join(soft))
    if hard: print("\n".join(hard))
    sys.exit(1 if hard else 0)

soft = [pr for pr in problems if pr.startswith("Over char budget")]  # budgets never fail (D-20261104-3)
hard = [pr for pr in problems if pr not in soft]
if soft: print("(warn) " + "\n(warn) ".join(soft))
print("\n".join(hard) if hard else f"점검 통과 (기록 파일 {len(logs)}개)")
sys.exit(1 if hard else 0)
