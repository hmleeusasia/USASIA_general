"""Rule-area supervisor (PLAN-rule-routing-001-draft2 decision e, D-20261104-2). Never blocks.

Events (one script, picked by hook_event_name):
  UserPromptSubmit      trigger words from docs/rules/INDEX.md -> "read docs/rules/<area>.md" once per area per session
  PostToolUse Read      a docs/rules/<area>.md read -> record area as read (Bash is not hooked: a spawn per
                        Bash call is too slow, ~0.9 s; reading rules with cat is not recorded — warn only)
  PreToolUse Write|Edit a repo write whose path matches an area's trigger paths, area not read -> warn once
  SessionStart compact  forget what was read (the content left the context)
Rules: area-keyword, area-read (config.json, off|warn). State: <tempdir>/usasia_area_<session>.json."""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_input, mode, log, context, norm_path  # noqa: E402

ROOT = norm_path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
RULE_RE = re.compile(r"docs/rules/([a-z0-9_-]+)\.md")


def state_file(s):
    return os.path.join(tempfile.gettempdir(), f"usasia_area_{s or 'x'}.json")


def load(s):
    try:
        return json.load(open(state_file(s), encoding="utf-8"))
    except Exception:
        return {"read": [], "warned": [], "pointed": []}


def save(s, st):
    try:
        json.dump(st, open(state_file(s), "w", encoding="utf-8"))
    except Exception:
        pass


def areas():
    """[(area, file, [words], [path regex])] from the INDEX table."""
    out = []
    try:
        txt = open(os.path.join(ROOT, "docs", "rules", "INDEX.md"), encoding="utf-8").read()
    except Exception:
        return out
    for line in txt.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 6 or not c[1].endswith(".md") or c[0] in ("Area", "---"):
            continue
        words = [w.strip() for w in c[3].split(",") if w.strip()]
        paths = []
        for p in re.findall(r"[\w./{},*-]+/\*\*|[\w./-]+\.md", c[4]):
            m = re.match(r"(.*)\{([^}]*)\}(.*)", p)
            for q in ([m[1] + x + m[3] for x in m[2].split(",")] if m else [p]):
                paths.append(re.compile("^" + re.escape(q).replace(r"\*\*", ".*") + "$"))
        out.append((c[0], c[1], words, paths))
    return out


def word_hit(word, text):
    if re.fullmatch(r"[A-Za-z][A-Za-z ]*", word):
        return re.search(r"\b" + re.escape(word) + r"\b", text, re.I) is not None
    return word in text


def rel(p):
    p = norm_path(p)
    if p.lower().startswith(ROOT.lower() + "/"):
        return p[len(ROOT) + 1:]
    return p


def main():
    d = read_input()
    ev = d.get("hook_event_name", "")
    s = d.get("session_id")
    st = load(s)
    ti = d.get("tool_input") or {}

    if ev == "SessionStart":
        if d.get("source") == "compact":  # content left the context: point and warn again
            st = {"read": [], "warned": [], "pointed": []}
            save(s, st)
        return

    if ev == "PostToolUse":
        text = ti.get("file_path", "") if d.get("tool_name") == "Read" else ti.get("command", "")
        found = RULE_RE.findall(norm_path(text))
        if found:
            st["read"] = sorted(set(st["read"]) | {f + ".md" for f in found})
            save(s, st)
        return

    if ev == "UserPromptSubmit":
        md = mode("area-keyword")
        if md == "off":
            return
        prompt = d.get("prompt", "")
        if "<agent-message" in prompt or "[Subagent hand-back]" in prompt or "<task-notification>" in prompt:
            return  # subagent reports and system notices are not user requests (seen 2026-11-04)
        msgs = []
        for area, f, words, _ in areas():
            if f in st["read"] or area in st["pointed"]:
                continue
            hit = next((w for w in words if word_hit(w, prompt)), None)
            if hit:
                st["pointed"].append(area)
                msgs.append(f"docs/rules/{f} (matched '{hit}')")
                log("area-keyword", f"{area}\t{hit}")
        if msgs:
            save(s, st)
            context("UserPromptSubmit", "Rule areas for this request — read before acting: " + "; ".join(msgs))
        return

    if ev == "PreToolUse":
        md = mode("area-read")
        if md == "off":
            return
        path = rel(ti.get("file_path", ""))
        msgs = []
        for area, f, _, paths in areas():
            if f in st["read"] or area in st["warned"]:
                continue
            if any(rx.match(path) for rx in paths):
                st["warned"].append(area)
                msgs.append(f"docs/rules/{f}")
                log("area-read", f"{area}\t{path}")
        if msgs:
            save(s, st)
            context("PreToolUse", f"[area-read] Writing {path}: rule file(s) not read this session: "
                    + ", ".join(msgs) + ". Read them and check this edit (shown once).")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail open
        log("area-error", type(e).__name__)
    sys.exit(0)
