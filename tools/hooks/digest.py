"""SessionStart digest (PLAN-lean-context-001-draft2 step 3).
~10 lines injected at startup/resume/compact so Claude does not read full CURRENT_STATE + facts.
Manual run: py tools/hooks/digest.py --print   (prints the plain text)
Fails open: any error -> short note, exit 0."""
import datetime
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_input, mode, context  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TODAY = datetime.date.today()


def rd(rel):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def run(cmd):
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=20)
        return r.stdout.decode("utf-8", "replace")
    except Exception:
        return ""


_TEST = os.environ.get("HOOKS_TEST") == "1"  # path overrides only in tests: the real map stays git-ignored
ACCOUNTS = (_TEST and os.environ.get("USASIA_ACCOUNTS")) or os.path.join(ROOT, ".claude", "accounts.local.json")
CLAUDE_JSON = (_TEST and os.environ.get("USASIA_CLAUDE_JSON")) or os.path.expanduser("~/.claude.json")
ID_RE = re.compile(r"[a-z0-9_-]+")


def account_uuid():
    """Signed-in Claude account id from ~/.claude.json, or None. Treated like an account number:
    never printed, logged or written to the repo (PLAN-onboarding-001-draft2, D-20261105-12)."""
    try:
        with open(CLAUDE_JSON, encoding="utf-8") as f:
            u = (json.load(f).get("oauthAccount") or {}).get("accountUuid")
        return u if isinstance(u, str) and u else None
    except Exception:
        return None


def account_user(force=False):
    """(id, how) from the account map, (None, how) for an unknown account, or None to fall back.
    Rule account-detect (config.json) is off until the user turns it on; force=True for tests."""
    if not force and mode("account-detect") == "off":
        return None
    u = account_uuid()
    if not u:
        return None
    try:
        with open(ACCOUNTS, encoding="utf-8") as f:
            uid = json.load(f).get(u)
    except Exception:
        uid = None
    if isinstance(uid, str) and ID_RE.fullmatch(uid) and os.path.isdir(os.path.join(ROOT, "docs", "users", uid)):
        return uid, "Claude account"
    return None, "new Claude account → run /onboarding"


def register(uid):
    """Map the signed-in account to <uid> in the git-excluded accounts file (used by onboarding)."""
    u = account_uuid()
    if not u or not ID_RE.fullmatch(uid or "") or not os.path.isdir(os.path.join(ROOT, "docs", "users", uid)):
        return "not registered (no account, bad id, or docs/users/<id> missing)"
    m = {}
    if os.path.exists(ACCOUNTS):
        try:
            with open(ACCOUNTS, encoding="utf-8") as f:
                m = json.load(f)
            assert isinstance(m, dict)
        except Exception:
            return "not registered: accounts file unreadable; fix or remove it first (other mappings kept)"
    m[u] = uid
    tmp = ACCOUNTS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=1)
    os.replace(tmp, ACCOUNTS)
    return f"registered this Claude account as {uid}"


def personal_rules(uid):
    """Personal CLAUDE.md text to inject when the account was detected (replaces the static @ import later)."""
    t = rd(f"docs/users/{uid}/CLAUDE.md").strip()
    return f"[personal rules: docs/users/{uid}/CLAUDE.md]\n{t}" if t else ""


def user_id():
    acc = account_user()
    if acc:
        return acc
    m = re.search(r"@docs/users/([^/]+)/CLAUDE\.md", rd("CLAUDE.local.md"))
    if m:
        return m.group(1), "CLAUDE.local.md"
    name = run(["git", "config", "user.name"]).strip()
    users = os.path.join(ROOT, "docs", "users")
    for uid in sorted(os.listdir(users)) if os.path.isdir(users) else []:
        if name and re.search(r"git 사용자\s*\|\s*" + re.escape(name) + r"\s*\|", rd(f"docs/users/{uid}/profile.md")):
            return uid, "git user"
    return None, f"git user '{name}' not in docs/users → ask once"


def section(text, letter):
    m = re.search(rf"^## {letter}\..*?$(.*?)(?=^## [A-Z]\.|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def short(s, n=70):
    s = re.sub(r"\*\*|`", "", s).strip(" -")
    return s if len(s) <= n else s[: n - 1] + "…"


def build():
    out = []
    uid, how = user_id()
    where = "cloud" if os.environ.get("CLAUDE_CODE_REMOTE") else "local"
    out.append(f"User: {uid or 'UNKNOWN'} ({how}) · {where} · today {TODAY}")
    if how == "Claude account" and uid:
        local = re.search(r"@docs/users/([^/]+)/CLAUDE\.md", rd("CLAUDE.local.md"))
        if local and local.group(1) != uid:
            out.append(f"CLAUDE.local.md loads {local.group(1)}'s personal file: ignore it; this session is {uid}")
        pr = personal_rules(uid)
        if pr:
            out.append(pr)
    if where == "cloud":
        out.append("Cloud: no Drive, no Chrome - do not try them; note 'needs local check' (R-LOOK-03)")

    st = rd("docs/CURRENT_STATE.md")
    h = section(st, "H").splitlines()
    out.append("Last start-day: " + short(h[0] if h else "?", 90))
    sheet = re.search(r"^\| H-sheet \|.*?\| ([^|]+) \| [^|]+ \|\s*$", st, re.M)
    if sheet:
        out.append("H-sheet: " + sheet.group(1).strip())

    py = sys.executable
    opens = [l for l in run([py, "tools/find.py", "--open"]).splitlines() if l.strip()]
    late = [l for l in opens if "[기한초과]" in l]
    soon = []
    for l in run([py, "tools/find.py", "--due"]).splitlines():
        m = re.match(r"(\d{4}-\d{2}-\d{2})", l)
        if m and (datetime.date.fromisoformat(m.group(1)) - TODAY).days <= 7:
            ids = re.findall(r"\bT-\d+\b", l)
            title = re.sub(r"^\S+ \S+: ", "", l).split("  #")[0]
            soon.append(f"{m.group(1)[5:]} {ids[0] if ids else short(title, 40)}")
    ids_late = [", ".join(re.findall(r"\bT-\d+\b", l)) or short(l.split(": ", 1)[-1], 40) for l in late]
    out.append(f"Open: {len(opens)} · overdue: {', '.join(ids_late) or 'none'} · due ≤7d: {'; '.join(soon) or 'none'}")

    traps = [short(l) for l in section(st, "F").splitlines() if l.startswith("-")]
    if traps:
        out.append("Traps: " + " | ".join(traps))

    br = run(["git", "branch", "--show-current"]).strip()
    dirty = len([l for l in run(["git", "status", "--porcelain"]).splitlines() if l.strip()])
    ab = run(["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"]).split()
    ab_s = f"ahead {ab[0]} / behind {ab[1]} vs origin/main (no fetch)" if len(ab) == 2 else ""
    out.append(f"Git: {br} · uncommitted {dirty} · {ab_s}")

    out.append("Open on demand: users/<id>/todo.md (tasks), CURRENT_STATE C (repo work), kb/INDEX.md, kb/browser.md (Chrome). "
               "Run /start-day for mail/STWS/Drive.")
    return "[digest] " + "\n".join(out)


if __name__ == "__main__":
    if "--register" in sys.argv:
        i = sys.argv.index("--register")
        print(register(sys.argv[i + 1] if len(sys.argv) > i + 1 else ""))
        sys.exit(0)
    if "--print" in sys.argv:
        print(build())
        sys.exit(0)
    d = read_input()
    try:
        if mode("digest") != "off":
            context("SessionStart", build())
    except Exception as e:  # fail open
        context("SessionStart", f"[digest] failed ({type(e).__name__}); read docs/CURRENT_STATE.md")
    sys.exit(0)
