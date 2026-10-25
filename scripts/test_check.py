"""Tests for scripts/check.py. Run: python3 -m unittest scripts/test_check.py

Each test copies the repo to a temp folder, breaks one thing there, and runs check.py on the copy.
The real repo is never changed.
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Sample private words, built from parts so this file never holds them whole.
WORD = "zeb" + "rafruit"
SHORT = "zeb" + "ra"
PHRASE = "blue" + " door"


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repo"
        shutil.copytree(REPO, self.repo)
        terms = self.repo / ".git" / "info" / "private-terms"
        terms.parent.mkdir(parents=True, exist_ok=True)
        terms.write_text("\n".join(["# test list", WORD, SHORT, PHRASE]) + "\n")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def check(self):
        return run([sys.executable, "scripts/check.py"], self.repo)

    def plant(self, text, name="planted.md"):
        (self.repo / name).write_text(text)
        run(["git", "add", name], self.repo)

    def test_clean_repo_passes(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_private_term_fails(self):
        self.plant(f"Built for the {WORD.title()} team.\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("planted.md:1", result.stdout)
        self.assertIn(WORD, result.stdout)

    def test_private_phrase_fails(self):
        self.plant("Meet me at the " + PHRASE.title().replace(" ", "  ") + ".\n")
        self.assertEqual(self.check().returncode, 1)

    def test_term_inside_a_longer_word_passes(self):
        self.plant(f"Two {SHORT}s and a {WORD}y smoothie.\n")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_untracked_new_file_is_scanned(self):
        (self.repo / "draft.md").write_text(WORD + "\n")
        self.assertEqual(self.check().returncode, 1)

    def test_email_fails(self):
        self.plant("Write to someone@example.org for help.\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("email", result.stdout)

    def test_home_folder_path_fails(self):
        self.plant("Copy it from /Users/alex/Code/app.\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("home folder", result.stdout)

    def test_key_like_string_fails(self):
        self.plant("token = ghp_" + "a" * 36 + "\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("key", result.stdout)

    def test_hand_edited_made_file_fails(self):
        made = self.repo / "agents" / "reviewer.md"
        made.write_text(made.read_text() + "\nA hand edit.\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("agents/reviewer.md", result.stdout)
        self.assertIn("scripts/build.py", result.stdout)

    def test_missing_made_file_fails(self):
        (self.repo / "codex-agents" / "trust_but_verify_reviewer.toml").unlink()
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("trust_but_verify_reviewer.toml", result.stdout)

    def test_personal_email_in_commit_fails(self):
        self.plant("Nothing private here.\n")
        run(["git", "-c", "user.name=Alex", "-c", "user.email=alex@example.org",
             "commit", "-q", "-m", "test"], self.repo)
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("commit", result.stdout)

    def test_real_private_list_catches_its_first_term(self):
        real = REPO / ".git" / "info" / "private-terms"
        if not real.exists():
            self.skipTest("no private word list in this clone")
        first = next(line.strip() for line in real.read_text().splitlines()
                     if line.strip() and not line.startswith("#"))
        shutil.copy(real, self.repo / ".git" / "info" / "private-terms")
        self.plant(f"Made for {first.upper()}.\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("planted.md:1", result.stdout)


if __name__ == "__main__":
    unittest.main()
