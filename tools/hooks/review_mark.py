"""Mark this session's heavy work as reviewed (review-loop skill, last step). D-20261104-2 decision i.
Usage: py tools/hooks/review_mark.py [session_id]
Without an ID it marks the session whose heavy-state file changed last (the current session in practice)."""
import glob
import os
import sys
import tempfile

if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else None
    if not sid:
        files = [f for f in glob.glob(os.path.join(tempfile.gettempdir(), "usasia_heavy_*.json"))
                 if "test" not in os.path.basename(f)]  # test_hooks.py sessions are named test-*/stoptest-*
        if not files:
            sys.exit("No heavy-state file found: nothing to mark (no repo writes this session?)")
        sid = os.path.basename(max(files, key=os.path.getmtime))[len("usasia_heavy_"):-len(".json")]
    open(os.path.join(tempfile.gettempdir(), f"usasia_review_{sid}"), "w").write("reviewed\n")
    print(f"Review marked for session {sid}")
