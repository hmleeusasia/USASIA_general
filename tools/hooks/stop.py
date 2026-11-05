"""Stop hook, narrow (PLAN-lean-context-001-draft2 step 5).
Only looks at files written this turn (touch.py). Checks:
  stop-state: CURRENT_STATE.md over 80 lines
  stop-open : a #open/#waiting log heading with a T-ID that is not on any todo board (D-20261103-8)
  heavy-review: this session touched heavy paths (or > 15 repo files, backstop) and no review marker exists
                (review-loop skill -> review_mark.py). Blocks once per session (D-20261104-2 decision i)
Exit 0 when stop_hook_active (never loops). Does NOT check uncommitted work (session-end skill does).
Does not run when the user interrupts (tested step 0) — pre-commit is the backstop."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_input, mode, log  # noqa: E402
from touch import load, state_file, load_heavy, heavy_file  # noqa: E402
import tempfile  # noqa: E402

HEAVY = re.compile(r"^(tools/|docs/rules/|\.claude/skills/|\.claude/settings|CLAUDE\.md$|docs/users/[^/]+/CLAUDE\.md$)")  # by risk (2026-11-05)


def review_marker(session):
    return os.path.join(tempfile.gettempdir(), f"usasia_review_{session or 'x'}")


def heavy_problem(session):
    h = load_heavy(session)
    files = h.get("files", [])
    hits = [f for f in files if HEAVY.match(f)]
    if mode("heavy-review") != "block" or h.get("warned") or not (hits or len(files) > 15)             or os.path.exists(review_marker(session)):
        return None
    h["warned"] = True
    try:
        json.dump(h, open(heavy_file(session), "w", encoding="utf-8"))
    except Exception:
        pass
    why = ", ".join(hits[:4]) if hits else f"{len(files)} repo files"
    return ("heavy-review", f"Heavy work this session without a post-build review ({why})",
            "If the heavy work is finished, run the review-loop skill (fresh Sonnet, diff + rule files). "
            "If it is still in progress, continue; this reminder is shown once per session.")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def rd(rel):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def problems(files):
    out = []
    if "docs/CURRENT_STATE.md" in files:
        n = len(rd("docs/CURRENT_STATE.md").splitlines())
        if n > 80:
            out.append(("stop-state", f"docs/CURRENT_STATE.md has {n} lines (> 80)",
                        "Shorten: overwrite sections, drop closed items, move history to the log."))
    logs = [f for f in files if f.startswith("docs/log/") and f.endswith(".md")]
    if logs:
        board = ""
        users = os.path.join(ROOT, "docs", "users")
        for uid in os.listdir(users) if os.path.isdir(users) else []:
            board += rd(f"docs/users/{uid}/todo.md")
        for f in logs:
            for line in rd(f).splitlines():
                if line.startswith("### ") and re.search(r"#(open|waiting)\b", line):
                    miss = [t for t in re.findall(r"\bT-\d+\b", line) if t not in board]
                    if miss:
                        out.append(("stop-open", f"{f}: {line[4:90]}",
                                    f"Add {', '.join(miss)} to the todo board docs/users/<id>/todo.md (todo skill)."))
    return out


if __name__ == "__main__":
    try:
        d = read_input()
        s = d.get("session_id")
        files = load(s)
        try:
            os.remove(state_file(s))  # next turn starts clean
        except Exception:
            pass
        if d.get("stop_hook_active"):
            sys.exit(0)
        msgs = []
        hp = heavy_problem(s)
        for rule, line, fix in problems(files) + ([hp] if hp else []):
            md = mode(rule)
            if md == "off":
                continue
            log(rule, f"{md}\t{line[:80]}")
            if md == "block":
                msgs.append(f"[{rule}] {line}\n  Fix: {fix}")
        if msgs:
            print(json.dumps({"decision": "block", "reason": "Supervisor: fix before ending the turn:\n" + "\n".join(msgs)},
                             ensure_ascii=False))
    except Exception as e:  # fail open
        log("stop-error", type(e).__name__)
    sys.exit(0)
