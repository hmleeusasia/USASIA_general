"""PreToolUse guard (PLAN-lean-context-001-draft2 step 4).
Write/Edit/MultiEdit: scans NEW text only. Bash: force push / rm -rf docs.
Per-rule mode in config.json: off | warn (context to Claude, no block) | block (exit 2).
Fails open on any internal error."""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_input, mode, norm_path, log  # noqa: E402

ROOT = norm_path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
SKIP = ("docs/storage_rules.md", "docs/templates/", "docs/keywords.md", "docs/session_review.md",
        "tools/", "docs/requests/")                     # rule docs and code talk ABOUT sensitive values
SCAN = ("docs/", ".claude/skills/", "CLAUDE.md", "README.md")

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}")
SECRET = re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|gh[pous]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|xox[abp]-[A-Za-z0-9-]{20,})"
                    r"|(password|passwd|pwd|비밀번호|암호)\s*[:=]\s*\S{4,}", re.I)
SOFT = re.compile(r"\$ ?\d|\b\d{1,3}(\.\d{1,3}){3}\b|([0-9A-Fa-f]{2}:){5}|\bpassword\b|비밀번호", re.I)
LOG_OK = re.compile(r"^docs/log/(\d{4})/(\d{4})-\d{2}-\d{2}_[a-z0-9]+\.md$")
FORCE = re.compile(r"\bgit\s+push\b[^\n;&|]*?(\s(-f|--force|--force-with-lease)\b|\s\+[\w/.-]+)")
RMDOCS = re.compile(r"\brm\s+-[a-z]*r[a-z]*f?\b[^\n;&|]*\bdocs\b|\brm\s+-[a-z]*f[a-z]*r\b[^\n;&|]*\bdocs\b")
HANGUL = re.compile(r"[가-힣]")
LATIN = re.compile(r"[A-Za-z]")
ENG_PATHS = ("docs/log/", "docs/kb/", "docs/requests/", "docs/decisions.md", ".claude/skills/")

hits = []  # (rule, line, fix)


def rel(p):
    p = norm_path(p)
    return p[len(ROOT) + 1:] if p.lower().startswith(ROOT.lower() + "/") else p.lstrip("./")


def new_text(tool, ti):
    if tool == "Write":
        return ti.get("content", "")
    if tool == "Edit":
        return ti.get("new_string", "")
    if tool == "MultiEdit":
        return "\n".join(e.get("new_string", "") for e in ti.get("edits", []))
    return ""


def first_line(rx, text):
    for line in text.splitlines():
        m = rx.search(line)
        if m:
            return line.strip()[:100], m
    return None, None


def mask(s):
    return EMAIL.sub("<email>", SECRET.sub("<secret>", s))


def seen_once(session, key):
    """English nudge: once per file per session (state in temp dir, not in repo)."""
    f = os.path.join(tempfile.gettempdir(), f"usasia_hooks_{session or 'x'}.json")
    try:
        data = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []
    except Exception:
        data = []
    if key in data:
        return True
    data.append(key)
    try:
        json.dump(data, open(f, "w", encoding="utf-8"))
    except Exception:
        pass
    return False


def check_file(path, text, session):
    scan = path.startswith(SCAN) and not path.startswith(SKIP)
    if scan:
        line, m = first_line(EMAIL, text)
        if line:
            hits.append(("sens-email", mask(line),
                         "Remove the address; emails live only in the Drive Claude folder (D-20261102-16). "
                         "If the user explicitly wants it here, ask the user — do not retry with variations."))
        line, m = first_line(SECRET, text)
        if line:
            hits.append(("sens-secret", mask(line),
                         "Passwords/keys are never stored anywhere (storage_rules.md). Remove it and tell the user."))
        line, m = first_line(SOFT, text)
        if line:
            hits.append(("sens-soft", mask(line),
                         "Amount/IP/MAC/'password' word: keep only if it is not a real value (Drive for real values)."))
    if path.startswith("docs/log/"):
        m = LOG_OK.match(path)
        if not m or m.group(1) != m.group(2):
            hits.append(("log-path", path, "Log files: docs/log/YYYY/YYYY-MM-DD_<id>.md (one file per person, year folder = file year)."))
    if path.startswith("docs/users/"):
        try:
            from digest import user_id
            uid, _ = user_id()
        except Exception:
            uid = "?"
        owner = path.split("/")[2] if path.count("/") >= 2 else ""
        if uid is None:
            hits.append(("users-unknown", path, "User unknown: ask the user who they are before writing personal files (CLAUDE.md)."))
        elif uid != "?" and owner and owner != uid and owner != "INDEX.md":
            hits.append(("users-unknown", path, f"This is {owner}'s folder, current user is {uid}. Ask before writing."))
    if path.startswith(ENG_PATHS):
        plain = re.sub(r"`[^`]*`|\([^)]*\)", "", text)
        h, l = len(HANGUL.findall(plain)), len(LATIN.findall(plain))
        if h + l >= 200 and h / (h + l) > 0.30 and not seen_once(session, path):
            hits.append(("english-nudge", f"{path}: {h}/{h + l} Hangul letters",
                         "New repo text is English (D-20261103-5). Korean names/quotes are fine. No need to retry."))


def check_bash(cmd):
    m = FORCE.search(cmd)
    if m:
        hits.append(("git-force", cmd.strip()[:100], "Force push / + refspec rewrites history. Only if the user asked for it in chat."))
    if RMDOCS.search(cmd):
        hits.append(("rm-docs", cmd.strip()[:100], "Recursive delete of docs/. Ask the user first."))


def main():
    d = read_input()
    tool, ti = d.get("tool_name", ""), d.get("tool_input", {}) or {}
    if tool in ("Write", "Edit", "MultiEdit"):
        check_file(rel(ti.get("file_path", "")), new_text(tool, ti), d.get("session_id"))
    elif tool == "Bash":
        check_bash(ti.get("command", ""))
    blocks, warns = [], []
    for rule, line, fix in hits:
        md = mode(rule)
        if md == "off":
            continue
        log(rule, f"{md}\t{tool}\t{line[:80]}")
        (blocks if md == "block" else warns).append(f"[{rule}] {line}\n  Fix: {fix}")
    if blocks:
        sys.stderr.write("Supervisor blocked this action:\n" + "\n".join(blocks + warns) + "\n")
        sys.exit(2)
    if warns:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                          "additionalContext": "Supervisor warnings (not blocked):\n" + "\n".join(warns)}},
                         ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail open
        log("guard-error", type(e).__name__)
        sys.exit(0)
