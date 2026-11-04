"""Step-0 probe: records which shell/Python runs hooks and what each event sends. Never blocks."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_input, mode, log, context  # noqa: E402

try:
    d = read_input()
    if mode("probe") != "off":
        ev = d.get("hook_event_name", "?")
        info = (f"event={ev} source={d.get('source', '')} stop_hook_active={d.get('stop_hook_active', '')} "
                f"tool={d.get('tool_name', '')} py={sys.executable} MSYSTEM={os.environ.get('MSYSTEM', '')} "
                f"SHELL={os.environ.get('SHELL', '')} keys={','.join(sorted(d))}")
        log("probe", info)
        if ev == "SessionStart":
            context(ev, "[probe] SessionStart hook ran: " + info)
except Exception:
    pass
sys.exit(0)
