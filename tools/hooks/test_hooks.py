"""Fixture tests for guard.py / digest.py. Run: py tools/hooks/test_hooks.py
Forces every rule to 'block' via a temp config so each fixture shows hit / no hit.
Each "should hit" case has a "should not hit" twin (no empty passes)."""
import json
import os
import shutil
import subprocess
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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


def area_tests():
    """area.py: keyword pointer once, read clears path warning, unread write warns once; heavy-review."""
    import tempfile
    root = os.path.dirname(os.path.dirname(HERE)).replace("\\", "/")
    env = dict(os.environ, HOOKS_TEST="1")
    sid = f"test-area-{os.getpid()}"

    def area(inp):
        r = subprocess.run([sys.executable, os.path.join(HERE, "area.py")],
                           input=json.dumps(dict(inp, session_id=sid)).encode("utf-8"), capture_output=True, env=env, timeout=20)
        return r.stdout.decode("utf-8", "replace")

    bad = 0
    checks = [
        ("keyword 출발 → expense", {"hook_event_name": "UserPromptSubmit", "prompt": "출발"}, "expense.md"),
        ("keyword again → silent", {"hook_event_name": "UserPromptSubmit", "prompt": "도착"}, ""),
        ("no keyword → silent", {"hook_event_name": "UserPromptSubmit", "prompt": "BV 프린터 로그인 확인"}, ""),
        ("unread log write → warn", {"hook_event_name": "PreToolUse", "tool_name": "Write",
                                    "tool_input": {"file_path": root + "/docs/log/2026/2026-11-04_hmlee.md"}}, "log.md"),
        ("second log write → silent", {"hook_event_name": "PreToolUse", "tool_name": "Write",
                                      "tool_input": {"file_path": root + "/docs/log/2026/2026-11-05_hmlee.md"}}, ""),
    ]
    for name, inp, want in checks:
        out = area(inp)
        ok = (want in out) if want else (out.strip() == "")
        bad += not ok
        print(f"{'ok ' if ok else 'FAIL'} area {name}")
    sid2 = sid + "b"
    sid_save = sid
    sid = sid2
    area({"hook_event_name": "PostToolUse", "tool_name": "Read", "tool_input": {"file_path": root + "/docs/rules/log.md"}})
    out = area({"hook_event_name": "PreToolUse", "tool_name": "Edit",
                "tool_input": {"file_path": root + "/docs/stores/bv.md"}})
    ok = out.strip() == ""
    bad += not ok
    print(f"{'ok ' if ok else 'FAIL'} area read via Read → no warn")
    for s in (sid_save, sid2):
        try:
            os.remove(os.path.join(tempfile.gettempdir(), f"usasia_area_{s}.json"))
        except OSError:
            pass

    # heavy-review: hooks edit without marker → block once; decisions.md only → pass; with marker → pass
    def stop_run(s, files):
        json.dump({"files": files, "warned": False}, open(os.path.join(tempfile.gettempdir(), f"usasia_heavy_{s}.json"), "w"))
        r = subprocess.run([sys.executable, os.path.join(HERE, "stop.py")],
                           input=json.dumps({"session_id": s}).encode("utf-8"), capture_output=True, env=env, timeout=20)
        return r.stdout.decode("utf-8", "replace")
    hs = f"test-heavy-{os.getpid()}"
    cases = [("heavy hooks edit → block", hs + "1", ["tools/hooks/x.py"], None, True),
             ("decisions only → pass", hs + "2", ["docs/decisions.md"], None, False),
             ("heavy with marker → pass", hs + "3", ["CLAUDE.md"], True, False),
             ("skill edit → block", hs + "4", [".claude/skills/mail-triage/SKILL.md"], None, True),
             ("6 docs files → pass", hs + "5", [f"docs/team/{i}.md" for i in range(6)], None, False),
             ("tools/check.py → block", hs + "6", ["tools/check.py"], None, True)]
    for name, s, files, marker, want in cases:
        mk = os.path.join(tempfile.gettempdir(), f"usasia_review_{s}")
        if marker:
            open(mk, "w").write("x")
        out = stop_run(s, files)
        ok = ("heavy-review" in out) == want
        bad += not ok
        print(f"{'ok ' if ok else 'FAIL'} {name}")
        for f in (mk, os.path.join(tempfile.gettempdir(), f"usasia_heavy_{s}.json")):
            try:
                os.remove(f)
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
    bad += area_tests()
    import glob, tempfile
    for f in glob.glob(os.path.join(tempfile.gettempdir(), "usasia_*test*")):  # no test state left behind
        try:
            os.remove(f)
        except OSError:
            pass
    dg = subprocess.run([sys.executable, os.path.join(HERE, "digest.py"), "--print"], capture_output=True, timeout=60)
    dok = dg.returncode == 0 and dg.stdout.decode("utf-8", "replace").startswith("[digest]")
    print(f"{'ok ' if dok else 'FAIL'} digest --print")
    bad += not dok
    fp = os.path.join(HERE, "..", "find.py")  # R-LOOK-03: AND hit / partial OR / no match (exit 1)
    for name, args, want, code in [("find AND hit", ["Granite", "demarc"], os.path.join("kb", "INDEX.md:"), 0),
                                   ("find single no match", ["zzqqxx"], "NO INTERNAL MATCH", 1),
                                   ("find OR fallback", ["Granite", "zzqqxx"], "PARTIAL matches", 0),
                                   ("find no match", ["zzqqxx", "yyqqww"], "NO INTERNAL MATCH", 1)]:
        r = subprocess.run([sys.executable, fp] + args, capture_output=True, timeout=60)
        fok = r.returncode == code and want in r.stdout.decode("utf-8", "replace")
        print(f"{'ok ' if fok else 'FAIL'} {name}")
        bad += not fok
    total = len(CASES) + 1 + 4 + 6 + 6 + 4  # guard cases + digest + stop + area + heavy + find
    print(f"\n{total - bad}/{total} passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
