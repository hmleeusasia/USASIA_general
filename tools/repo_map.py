#!/usr/bin/env python3
"""Rebuild the GENERATED section of docs/ARCHITECTURE.md: tree with sizes, content vs framework,
records, skills, hook rule modes. Usage: python tools/repo_map.py [--check]  (--check: exit 1 if stale)"""
import json, pathlib, re, sys, datetime
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = ROOT / "docs/ARCHITECTURE.md"
B, E = "<!-- GENERATED:BEGIN (tools/repo_map.py — do not edit by hand) -->", "<!-- GENERATED:END -->"
SKIP = {".git", "__pycache__", "node_modules"}
FRAME = ("CLAUDE.md", ".claude", "tools", "docs/templates", "docs/requests", "docs/ARCHITECTURE.md",
         "docs/project_instructions.md", "docs/storage_rules.md", "docs/keywords.md")

def files():
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if p.is_file() and not SKIP & set(rel.parts) and not p.name.endswith((".log", ".local.md")) \
           and p.name != "settings.local.json" and rel.as_posix() != "docs/ARCHITECTURE.md":
            yield rel, p.stat().st_size

def tree(fs, depth=3):
    agg = {}
    for rel, size in fs:
        for i in range(1, min(len(rel.parts), depth) + 1):
            key = rel.parts[:i]
            n, s, isdir = agg.get(key, (0, 0, i < len(rel.parts)))
            agg[key] = (n + 1, s + size, isdir)
    out = ["```", "."]
    for key in sorted(agg):
        n, s, isdir = agg[key]
        name = key[-1] + ("/" if isdir else "")
        info = f"{n} files, {s/1024:.1f} KB" if isdir else f"{s/1024:.1f} KB"
        out.append(f"{'│   ' * (len(key) - 1)}├── {name:<34} {info}")
    return out + ["```"]

def build():
    fs = list(files())
    fw = sum(s for r, s in fs if any(r.as_posix().startswith(x) for x in FRAME))
    tot = sum(s for _, s in fs)
    logs = sorted((ROOT / "docs/log").rglob("*.md"))
    entries = sum(p.read_text(encoding="utf-8").count("\n### ") for p in logs)
    users = sorted(p.name for p in (ROOT / "docs/users").iterdir() if p.is_dir())
    dec = sum(1 for l in (ROOT / "docs/decisions.md").read_text(encoding="utf-8").splitlines() if l.startswith("- D-"))
    stores = sum(1 for l in (ROOT / "docs/kb/store_codes.md").read_text(encoding="utf-8").splitlines()
                 if l.startswith("| ") and not l.startswith("| 약어"))
    out = [B, "## 8. Generated snapshot", f"_Rebuilt {datetime.date.today()} by tools/repo_map.py._", "",
           "| Metric | Value |", "|---|---|",
           f"| Files / size | {len(fs)} / {tot/1024:.0f} KB |",
           f"| Content vs framework | {(tot-fw)/1024:.0f} KB vs {fw/1024:.0f} KB ({fw*100//max(tot,1)}% framework) |",
           f"| Log files / entries | {len(logs)} / {entries} |",
           f"| Users | {', '.join(users)} |", f"| Decisions | {dec} |", f"| Store codes | {stores} |", "",
           "### Skills (.claude/skills)", "| Skill | When |", "|---|---|"]
    for sk in sorted((ROOT / ".claude/skills").glob("*/SKILL.md")):
        m = re.search(r"^description:\s*(.+)$", sk.read_text(encoding="utf-8"), re.M)
        out.append(f"| {sk.parent.name} | {(m[1] if m else '')[:110]} |")
    try:
        rules = json.loads((ROOT / "tools/hooks/config.json").read_text(encoding="utf-8"))["rules"]
        out += ["", "### Hook rule modes (tools/hooks/config.json)", "| Mode | Rules |", "|---|---|"]
        for md in ("block", "warn", "off"):
            out.append(f"| {md} | {', '.join(k for k, v in rules.items() if v == md) or '-'} |")
    except Exception:
        pass
    out += ["", "### Tree (depth 3)"] + tree(fs) + [E]
    return "\n".join(out)

def main():
    text = DOC.read_text(encoding="utf-8")
    i, j = text.index(B), text.index(E) + len(E)
    new = text[:i] + build() + text[j:]
    strip = lambda t: re.sub(r"_Rebuilt .*?_", "", t)
    if "--check" in sys.argv:
        stale = strip(new) != strip(text)
        print("ARCHITECTURE.md generated section is stale: run python tools/repo_map.py" if stale else "up to date")
        return 1 if stale else 0
    if new != text: DOC.write_text(new, encoding="utf-8", newline="\n")
    print("docs/ARCHITECTURE.md updated")
    return 0

sys.exit(main())
