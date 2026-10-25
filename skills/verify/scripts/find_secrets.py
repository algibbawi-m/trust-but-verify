#!/usr/bin/env python3
"""Find likely secrets and print where they are, never what they are.

Usage (run from inside the repository):
  find_secrets.py files PATH...   scan these files
  find_secrets.py tree            scan every file git tracks, plus untracked files not ignored
  find_secrets.py history         scan every line ever added in any commit on any branch
  find_secrets.py redact          copy standard input to standard output, with each secret value
                                  replaced by [REDACTED <kind>]

The scan modes print one line per hit: "path:line  kind" (history: "commit path  kind"), then a
count. The matched value is never printed, so the output is safe to show and to paste into a report.
"""
import re
import subprocess
import sys

PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{40,}")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("Stripe live key", re.compile(r"\b(sk|rk)_live_[A-Za-z0-9]{10,}")),
    ("Stripe test key", re.compile(r"\b(sk|rk)_test_[A-Za-z0-9]{10,}")),
    ("Anthropic or OpenAI key", re.compile(r"\bsk-(ant-|proj-)?[A-Za-z0-9_-]{20,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("JSON web token", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("password in a connection URL", re.compile(r"\b[a-z][a-z0-9+.-]*://[^/\s:@'\"]+:[^/\s:@'\"]{3,}@")),
    ("hard-coded secret", re.compile(
        r"(?i)\b[A-Za-z0-9_]*(api[_-]?key|secret|token|passw(or)?d|pwd|auth)[A-Za-z0-9_]*\b\s*[:=]\s*['\"]([^'\"\s]{8,})['\"]")),
]
PLACEHOLDER = re.compile(r"(?i)^(x+|\*+|changeme|change[_-]?me|your[_-].*|example.*|dummy.*|placeholder.*|<.*>|\$\{.*\}|test|password|secret)$")
SECRET_FILES = re.compile(r"(^|/)(\.env(\.[^/]*)?|id_rsa|id_ed25519|credentials\.json|service[-_]account.*\.json|[^/]*\.(pem|key|p12|pfx))$")
SAFE_ENV = re.compile(r"\.env\.(example|sample|template|dist)$")


def kinds(line):
    found = []
    for kind, pattern in PATTERNS:
        m = pattern.search(line)
        if not m:
            continue
        if kind == "hard-coded secret" and (PLACEHOLDER.match(m.group(3)) or found):
            continue
        found.append(kind)
    return found


def redact(line):
    for kind, pattern in PATTERNS:
        if kind == "hard-coded secret":
            line = pattern.sub(lambda m: m.group(0) if PLACEHOLDER.match(m.group(3)) else
                               m.group(0).replace(m.group(3), f"[REDACTED {kind}]"), line)
        else:
            line = pattern.sub(f"[REDACTED {kind}]", line)
    return line


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, errors="replace").stdout


def scan_files(paths):
    hits = 0
    for path in paths:
        if SECRET_FILES.search(path) and not SAFE_ENV.search(path):
            print(f"{path}  secret-looking file")
            hits += 1
        try:
            with open(path, encoding="utf-8", errors="strict") as f:
                lines = f.readlines()
        except (OSError, UnicodeDecodeError):
            continue  # unreadable or binary
        for n, line in enumerate(lines, 1):
            for kind in kinds(line):
                print(f"{path}:{n}  {kind}")
                hits += 1
    return hits


def scan_history():
    hits, seen, commit, path = 0, set(), "", ""
    for line in git("log", "-p", "--all", "--no-color", "-U0", "--format=commit %h").splitlines():
        if line.startswith("commit "):
            commit = line.split()[1]
        elif line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("+") and not line.startswith("+++"):
            for kind in kinds(line):
                if (commit, path, kind) not in seen:
                    seen.add((commit, path, kind))
                    print(f"{commit} {path}  {kind}")
                    hits += 1
    return hits


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "files":
        hits = scan_files(sys.argv[2:])
    elif mode == "tree":
        listed = git("ls-files", "--cached", "--others", "--exclude-standard").splitlines()
        hits = scan_files(listed)
    elif mode == "history":
        hits = scan_history()
    elif mode == "redact":
        for line in sys.stdin:
            sys.stdout.write(redact(line))
        return
    else:
        print(__doc__)
        sys.exit(2)
    print(f"{hits} possible secret(s) found. Values are not shown.")


if __name__ == "__main__":
    main()
