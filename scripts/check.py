"""Check the repo before every commit and before publishing.

Run: python3 scripts/check.py

It fails when:
  - a made file differs from what scripts/build.py would make;
  - two skills ship a script with the same name, and the copies differ;
  - a file or a commit holds an email address, a home-folder path or a key-like string;
  - a file or a commit holds a word from the private list at .git/info/private-terms.
Git never pushes .git/info, so the private list stays on the machine that wrote it.
"""
import re
import subprocess
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

ROOT = build.ROOT
TERMS_FILE = ROOT / ".git" / "info" / "private-terms"
ALLOWED_EMAIL = re.compile(r"(@users\.noreply\.github\.com|^noreply@anthropic\.com|^noreply@github\.com)$")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PATTERNS = [
    ("home folder path", re.compile(r"/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\")),
    ("key-like string", re.compile(
        r"ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}"
        r"|xox[abprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]
# The checker and its tests hold these patterns and their test samples on purpose.
PATTERN_EXEMPT = {"scripts/check.py", "scripts/test_check.py"}


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def private_terms():
    if not TERMS_FILE.exists():
        return None
    terms = [line.strip() for line in TERMS_FILE.read_text().splitlines()
             if line.strip() and not line.startswith("#")]
    return [(t, re.compile(r"\b" + r"\s+".join(map(re.escape, t.split())) + r"\b", re.I))
            for t in terms]


def scan_text(text, terms, exempt=False):
    """Yield (line number, kind, match) for each problem in text."""
    for number, line in enumerate(text.splitlines(), 1):
        if not exempt:
            for found in EMAIL.findall(line):
                if not ALLOWED_EMAIL.search(found):
                    yield number, "email address", found
            for kind, pattern in PATTERNS:
                for found in pattern.findall(line):
                    yield number, kind, found
        for term, pattern in terms or []:
            if pattern.search(line):
                yield number, "private word", term


def check_made_files():
    problems = []
    expected = build.render()
    for rel, content in expected.items():
        path = ROOT / rel
        if not path.exists():
            problems.append(f"{rel}: missing. Run python3 scripts/build.py")
        elif path.read_text() != content:
            problems.append(f"{rel}: differs from roles/. Edit roles/, then run python3 scripts/build.py")
    for rel in sorted(build.made_files_on_disk() - set(expected)):
        problems.append(f"{rel}: no role makes this file. Run python3 scripts/build.py")
    for rel in expected:
        if rel.endswith(".toml"):
            try:
                tomllib.loads(expected[rel])
            except tomllib.TOMLDecodeError as error:
                problems.append(f"{rel}: not valid TOML ({error})")
    return problems


def check_shared_scripts():
    """Each skill carries its own copy of a shared script. The copies must stay the same."""
    problems = []
    copies = {}
    for path in sorted(ROOT.glob("skills/*/scripts/*")):
        copies.setdefault(path.name, []).append(path)
    for name, paths in copies.items():
        first = paths[0]
        for other in paths[1:]:
            if other.read_bytes() != first.read_bytes():
                problems.append(f"{other.relative_to(ROOT)}: differs from {first.relative_to(ROOT)}. "
                                "Make the copies the same")
    return problems


def check_files(terms):
    problems = []
    listed = git("ls-files", "--cached", "--others", "--exclude-standard").stdout.splitlines()
    for rel in listed:
        path = ROOT / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for number, kind, found in scan_text(text, terms, exempt=rel in PATTERN_EXEMPT):
            problems.append(f"{rel}:{number}: {kind}: {found}")
    return problems


def check_commits(terms):
    problems = []
    log = git("log", "--format=%h%x00%an%x00%ae%x00%cn%x00%ce%x00%B%x1e")
    if log.returncode != 0:
        return problems
    for record in log.stdout.split("\x1e"):
        if not record.strip():
            continue
        short, author, author_email, committer, committer_email, message = record.strip("\n").split("\x00")
        for email in {author_email, committer_email}:
            if not ALLOWED_EMAIL.search(email):
                problems.append(f"commit {short}: personal email address: {email}. "
                                "Use your GitHub no-reply address")
        for _, kind, found in scan_text("\n".join([author, committer, message]), terms):
            problems.append(f"commit {short}: {kind}: {found}")
    return problems


def main():
    terms = private_terms()
    if terms is None:
        print(f"Note: no private word list at .git/info/private-terms. Only general patterns checked.")
    problems = check_made_files() + check_shared_scripts() + check_files(terms) + check_commits(terms)
    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). Nothing is safe to commit or publish until they are fixed.")
        sys.exit(1)
    print("check passed: made files are current, and no leaks were found")


if __name__ == "__main__":
    main()
