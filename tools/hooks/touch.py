"""PostToolUse recorder: remembers which repo files were written this turn (temp state, not in repo).
stop.py reads and clears it. Never blocks."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_input, norm_path  # noqa: E402

ROOT = norm_path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def state_file(session):
    return os.path.join(tempfile.gettempdir(), f"usasia_touch_{session or 'x'}.json")


def heavy_file(session):
    """Cumulative per-session list (heavy-review in stop.py); never cleared by stop.py."""
    return os.path.join(tempfile.gettempdir(), f"usasia_heavy_{session or 'x'}.json")


def load_heavy(session):
    try:
        return json.load(open(heavy_file(session), encoding="utf-8"))
    except Exception:
        return {"files": [], "warned": False}


def load(session):
    try:
        return json.load(open(state_file(session), encoding="utf-8"))
    except Exception:
        return []


if __name__ == "__main__":
    try:
        d = read_input()
        p = norm_path((d.get("tool_input") or {}).get("file_path", ""))
        if p.lower().startswith(ROOT.lower() + "/"):
            p = p[len(ROOT) + 1:]
            s = d.get("session_id")
            files = load(s)
            if p not in files:
                files.append(p)
                json.dump(files, open(state_file(s), "w", encoding="utf-8"))
            h = load_heavy(s)
            if p not in h["files"]:
                h["files"].append(p)
                json.dump(h, open(heavy_file(s), "w", encoding="utf-8"))
    except Exception:
        pass
    sys.exit(0)
