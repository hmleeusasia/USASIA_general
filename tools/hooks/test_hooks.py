"""Fixture tests for guard.py / digest.py. Run: py tools/hooks/test_hooks.py
Forces every rule to 'block' via a temp config so each fixture shows hit / no hit.
Each "should hit" case has a "should not hit" twin (no empty passes)."""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(HERE, "config.json")
E = "hm" + "@" + "example.com"  # built at runtime so this file holds no literal address

W = lambda path, text: {"tool_name": "Write", "tool_input": {"file_path": path, "content": text}}
ED = lambda path, text: {"tool_name": "Edit", "tool_input": {"file_path": path, "old_string": "x", "new_string": text}}
B = lambda cmd: {"tool_name": "Bash", "tool_input": {"command": cmd}}
KO = "한국어로만 길게 쓴 문장입니다 " * 20

CASES = [  # (name, input, expected rule or None)
    ("email in log", ED("docs/log/2026/2026-11-03_hmlee.md", f"contact {E}"), "sens-email"),
    ("no email", ED("docs/log/2026/2026-11-03_hmlee.md", "contact via Drive address book"), None),
    ("email in tools ok", W("tools/x.py", f"# {E}"), None),
    ("password value", ED("docs/kb/x.md", "password: Hmart2026!"), "sens-secret"),
    ("password word only", ED("docs/kb/x.md", "ask for the password in person"), "sens-soft"),
    ("api key", ED("docs/kb/x.md", "key sk-abcdefghijklmnopqrstuvwxyz123"), "sens-secret"),
    ("drive id ok", ED("docs/kb/x.md", "folder 1g9q_Povbwi0-7HH2dPqh6zWeMOyz7Fwf"), None),
    ("amount soft", ED("docs/kb/x.md", "cost $250"), "sens-soft"),
    ("bad log name", W("docs/log/2026/2026-11-03.md", "x"), "log-path"),
    ("bad log year", W("docs/log/2025/2026-11-03_hmlee.md", "x"), "log-path"),
    ("good log name", W("docs/log/2026/2026-11-03_hmlee.md", "x"), None),
    ("other user folder", W("docs/users/kim/todo.md", "x"), "users-unknown"),
    ("own user folder", W("docs/users/hmlee/todo.md", "x"), None),
    ("korean long kb", W("docs/kb/ko.md", KO), "english-nudge"),
    ("korean short", W("docs/kb/ko2.md", "확인일 2026-11-03"), None),
    ("korean names in parens", W("docs/kb/en.md", "Dan Choi (최철룡) approved. " * 20), None),
    ("force push", B("git push --dry-run --force origin main"), "git-force"),
    ("plus refspec", B("git push origin +main"), "git-force"),
    ("force-with-lease", B("git push --force-with-lease"), "git-force"),
    ("normal push", B("git push -q origin main"), None),
    ("rm docs", B("rm -rf docs/kb"), "rm-docs"),
    ("rm tmp", B("rm -rf /tmp/x"), None),
    ("garbage input", {"tool_name": "Write"}, None),
]


def run(inp):
    inp = dict(inp, session_id=f"test-{os.getpid()}")  # fresh "once per session" state each run
    env = dict(os.environ, HOOKS_TEST="1", CLAUDE_PROJECT_DIR=os.path.dirname(os.path.dirname(HERE)))
    r = subprocess.run([sys.executable, os.path.join(HERE, "guard.py")], input=json.dumps(inp).encode("utf-8"),
                       capture_output=True, env=env, timeout=20)
    return r.returncode, r.stderr.decode("utf-8", "replace")


def stop_tests():
    """touch.py records files, stop.py blocks only on real gaps and never when stop_hook_active."""
    root = os.path.dirname(os.path.dirname(HERE))
    tmp_log = os.path.join(root, "docs", "log", "2099", "2099-01-01_test.md")
    os.makedirs(os.path.dirname(tmp_log), exist_ok=True)
    open(tmp_log, "w", encoding="utf-8").write("### Fake open item T-99999  #pos #support #open\n")
    env = dict(os.environ, HOOKS_TEST="1")
    sid = f"stoptest-{os.getpid()}"
    py = lambda script, inp: subprocess.run([sys.executable, os.path.join(HERE, script)], env=env, timeout=20,
                                            input=json.dumps(inp).encode("utf-8"), capture_output=True)
    touch = lambda rel: py("touch.py", {"session_id": sid, "tool_input": {"file_path": os.path.join(root, rel)}})
    cfg_txt = open(CFG, encoding="utf-8").read()
    bad = 0
    try:
        cfg = json.loads(cfg_txt); cfg["rules"].update({"stop-state": "block", "stop-open": "block"})
        json.dump(cfg, open(CFG, "w", encoding="utf-8"))
        cases = [
            ("stop: state ok, no log", ["docs/CURRENT_STATE.md"], False, False),
            ("stop: open T-ID missing from board", ["docs/log/2099/2099-01-01_test.md"], False, True),
            ("stop: same but stop_hook_active", ["docs/log/2099/2099-01-01_test.md"], True, False),
            ("stop: real log, all T-IDs on board", ["docs/log/2026/2026-11-03_hmlee.md"], False, False),
        ]
        for name, files, active, want_block in cases:
            for f in files:
                touch(f)
            r = py("stop.py", {"session_id": sid, "stop_hook_active": active})
            out = r.stdout.decode("utf-8", "replace")
            blocked = '"decision": "block"' in out
            ok = r.returncode == 0 and blocked == want_block
            bad += not ok
            print(f"{'ok ' if ok else 'FAIL'} {name}: block={blocked}")
    finally:
        open(CFG, "w", encoding="utf-8").write(cfg_txt)
        os.remove(tmp_log)
        try:
            os.rmdir(os.path.dirname(tmp_log))
        except OSError:
            pass
    return bad


def main():
    shutil.copy(CFG, CFG + ".bak")
    try:
        cfg = json.load(open(CFG, encoding="utf-8"))
        cfg["rules"] = {k: "block" for k in list(cfg["rules"]) + ["git-force", "rm-docs"]}
        json.dump(cfg, open(CFG, "w", encoding="utf-8"))
        bad = 0
        for name, inp, want in CASES:
            code, err = run(inp)
            got = err.split("[", 1)[1].split("]")[0] if code == 2 and "[" in err else None
            ok = (want is None and code == 0) or (want is not None and code == 2 and f"[{want}]" in err)
            bad += not ok
            print(f"{'ok ' if ok else 'FAIL'} {name}: want {want}, got {got} (exit {code})")
    finally:
        shutil.move(CFG + ".bak", CFG)
    bad += stop_tests()
    dg = subprocess.run([sys.executable, os.path.join(HERE, "digest.py"), "--print"], capture_output=True, timeout=60)
    dok = dg.returncode == 0 and dg.stdout.decode("utf-8", "replace").startswith("[digest]")
    print(f"{'ok ' if dok else 'FAIL'} digest --print")
    bad += not dok
    total = len(CASES) + 1 + 4  # guard cases + digest + stop cases
    print(f"\n{total - bad}/{total} passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
