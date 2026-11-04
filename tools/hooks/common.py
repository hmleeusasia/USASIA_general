"""Shared helpers for hooks. Rules: read stdin as UTF-8 bytes, write UTF-8, fail open."""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def read_input():
    try:
        raw = sys.stdin.buffer.read()
        return json.loads(raw.decode("utf-8")) if raw.strip() else {}
    except Exception:
        return {}


def mode(rule):
    try:
        with open(os.path.join(HERE, "config.json"), encoding="utf-8") as f:
            return json.load(f)["rules"].get(rule, "off")
    except Exception:
        return "off"


def norm_path(p):
    return (p or "").replace("\\", "/")


def log(rule, msg):
    """Local, gitignored (*.log). Never pass secret values here."""
    try:
        with open(os.path.join(HERE, "hits.log"), "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\t{rule}\t{msg}\n")
    except Exception:
        pass


def context(event, text):
    """Show text to Claude without blocking (works for warn mode)."""
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}, ensure_ascii=False))


def block(rule, line, fix):
    """Exit 2: stderr goes to Claude. Message = rule ID + offending line + fix."""
    sys.stderr.write(f"[{rule}] {line}\nFix: {fix}\n")
    sys.exit(2)
