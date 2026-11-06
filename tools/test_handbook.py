#!/usr/bin/env python3
"""Tests for tools/handbook.py: each check must actually fire (D-20261106-6 review).

Each test copies what the generator reads (tools/, .claude/skills/, docs/rules/, docs/handbook/) into a temp
folder, breaks one thing, runs `handbook.py --check` there and expects exit 1 with a specific message.
Run: py tools/test_handbook.py   (pre-commit runs it when tools/handbook.py or this file changes)
"""
import json, pathlib, shutil, subprocess, sys, tempfile, unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
COPY = ["tools", ".claude/skills", "docs/rules", "docs/handbook"]


class Handbook(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        for rel in COPY:
            shutil.copytree(REPO / rel, self.tmp / rel, ignore=shutil.ignore_patterns("__pycache__", "*.log"))
        self.hb = self.tmp / "docs/handbook"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_gen(self, *args):
        r = subprocess.run([sys.executable, "-I", str(self.tmp / "tools/handbook.py"), *args],
                           capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr

    def meta(self, change):
        p = self.hb / "meta.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        change(d)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

    def append(self, rel, text):
        p = self.tmp / rel
        p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")

    def expect_fail(self, needle):
        rc, out = self.run_gen("--check")
        self.assertEqual(rc, 1, out)
        self.assertIn(needle, out)

    def test_clean_copy_passes(self):
        rc, out = self.run_gen("--check")
        self.assertEqual(rc, 0, out)

    def test_new_function_without_meaning(self):
        self.append("tools/find.py", "\n\ndef zz_new():\n    return 1\n")
        self.expect_fail("tools/find.py#zz_new has no 'ko' meaning")

    def test_new_module_without_meaning(self):
        (self.tmp / "tools/zz_tool.py").write_text('"""Does a thing."""\n', encoding="utf-8")
        self.expect_fail("module tools/zz_tool.py has no 'ko' meaning")

    def test_new_skill_without_meaning(self):
        d = self.tmp / ".claude/skills/zz-skill"
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: zz-skill\ndescription: test\n---\n", encoding="utf-8")
        self.expect_fail("skill zz-skill has no 'en' meaning")

    def test_orphan_function_key(self):
        self.meta(lambda d: d["functions"].__setitem__("tools/find.py#gone", {"en": "x", "ko": "x"}))
        self.expect_fail("function tools/find.py#gone no longer exists")

    def test_deleted_module_leaves_orphan(self):
        (self.tmp / "tools/repo_map.py").unlink()
        self.expect_fail("module tools/repo_map.py no longer exists")

    def test_generated_page_edited(self):
        self.append("docs/handbook/code-map.md", "\nhand edit\n")
        self.expect_fail("code-map.md is stale")

    def test_email_in_readme(self):
        self.append("docs/handbook/README.md", "\nmail someone" + "@" + "example.com\n")
        self.expect_fail("email address")

    def test_host_in_meta(self):
        self.meta(lambda d: d["modules"]["tools/find.py"].__setitem__("en", "talks to db.example.net"))
        self.expect_fail("host name")

    def test_comment_mention_is_not_a_run(self):
        # a script named only in a comment must not appear as "runs"
        self.append("tools/find.py", "\n# see prune.py for archiving\n")
        self.run_gen()
        text = (self.hb / "code-map.md").read_text(encoding="utf-8")
        block = text.split("### `tools/find.py`", 1)[1].split("###", 1)[0]
        self.assertNotIn("tools/prune.py", block)


if __name__ == "__main__":
    unittest.main(verbosity=1)
