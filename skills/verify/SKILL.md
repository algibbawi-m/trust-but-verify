---
name: verify
description: Reviews the current code changes before they ship. It collects the uncommitted edits and the branch's commits, sends them with the goal to a fresh reviewer who did not build them, runs the project's checks, checks every finding in the code, and reports in plain words what to fix now, before merge, or later. Read-only until the user says yes. Use when the user says "check what you just did before I ship it", "review my changes", "is this safe to merge", "verify this", "look over this branch or PR", "did you break anything", "second opinion on this change", "double check the work on this branch", or wants work they did not watch checked before it ships or before they show it to someone. Not for building or fixing (that is how-we-build), not for reviewing a whole app (that is audit), and not for documents.
---

# Verify

You are the ORCHESTRATOR of a review on demand. A fresh reviewer helper judges the change; you collect
what it needs, run the checks, confirm every finding in the code, and report to the user.

The person you work with is not a programmer. They ask for this before they ship work they did
not watch being built, so the report must tell them, in plain words, what a person using the app
would hit. Three stances govern everything below:

- **Whoever built the change never judges it.** The reviewer gets the goal, the plan and the
  diff — never the story of how the work was built. That includes you if you built it.
- **A finding is a claim until you see it in the code.** You open every line the reviewer names
  before it goes in the report. Wrong findings are dropped with a reason.
- **Read-only until the user says yes.** You change nothing in the project. Fixes start only
  after the user picks them, and then follow `how-we-build` at their size.

The project's own rules (its instruction file, such as CLAUDE.md or AGENTS.md; its review
chain, helpers and checks) win where they differ. `how-we-build`'s rules on secrets and personal
data apply here in full.

## 1. Collect the change

Record `git status` first. If the folder is not a git repository, say so and stop: there is no
change to compare.

Pick what to compare, in this order:

1. **The user names it** — a branch, a PR (`gh pr diff <n>`), a commit range, or files. Use that.
2. **On a branch that is not the default branch** — everything since it left the default branch:
   `git merge-base HEAD <default>`, then `git diff <base>` (this covers its commits and all
   uncommitted edits to tracked files). Find the default branch with
   `git symbolic-ref --short refs/remotes/origin/HEAD`; if that fails, use `main` or `master`.
3. **On the default branch** — commits not yet pushed (`git diff @{upstream}`), or only the
   uncommitted edits (`git diff HEAD`) when there is no upstream.
4. **Nothing changed** — the last commit, and say so.

Always add **new files git does not track yet** (`git ls-files --others --exclude-standard`),
in full. They are the part of a change most often missed.

Write the diff and the new files to one file **outside the project** (a temporary folder from
`mktemp -d`), through the secret mask, so no key value reaches the reviewer:

```
{ git diff <base>; for f in <new files>; do echo "=== NEW FILE: $f"; cat "$f"; done; } \
  | python3 <this skill's folder>/scripts/find_secrets.py redact > <folder>/change.diff
```

Leave lockfiles and generated files out of it, and list their names instead. Delete the file
when the review ends.

Then collect the **goal**: what this change should do for the person using the app. Take it from,
in order: the user's words in this conversation, the PR description, a plan file for this work
(one named in the conversation, or the project's plans folder), the commit messages. If none says
what the change is for, ask the user one question: "In one sentence, what should this change do
for the person using the app?"

Also note the project's rules file (CLAUDE.md, AGENTS.md) if there is one. The reviewer reads it.

Never give the reviewer the build story: no transcript, no "first I tried", no decision log, no
list of what was hard. Those make a reviewer agree with the builder.

**Size of the review.** Count the changed lines without lockfiles. Up to about 2,000 lines in one
area: one reviewer. Larger, or several unrelated areas (for example the sign-in code and a
report page): split by area, one reviewer each, at most three, sent together. Tell the user the
count first ("This change is large, so three reviewers, one per area").

## 2. Dispatch the reviewer, and run the checks yourself

Send the reviewer the dispatch in `references/reviewer-dispatch.md`, filled in. Choose the
helper in this order:

1. The project's own reviewer helper, if it has one.
2. This kit's reviewer helper, if it is installed: `trust-but-verify:reviewer` in Claude Code,
   `trust_but_verify_reviewer` in Codex. It sets its own effort in its file.
3. No reviewer helper installed: start a fresh subagent. Give it
   `references/roles/reviewer.md`, then the dispatch.
4. No subagent can be started: say so in one line, then do the review yourself in a separate
   pass that reads only the goal, the plan and the diff. Put "Not a fresh review: <reason>" at
   the top of the report, and tell the user that nobody fresh checked the work.

While it works, run these yourself. A helper's "the tests pass" is a claim, not a check.

- **The project's checks**, exactly as its rules name them; otherwise find them in
  `package.json`, `pyproject.toml`, `Makefile` or the CI configuration, and say which you used.
  Quote one result line for each. If a check needs an install that is not there, do not install:
  write "not run: needs install", since installing is on `how-we-build`'s stop list.
- **Secrets in the change.** From the project folder, run
  `python3 <this skill's folder>/scripts/find_secrets.py files <each changed and new file>`.
  It prints file, line and kind, never the value. Also stop on any changed `.env`, key or token
  file, and check that `.gitignore` covers the files that hold secrets.
- **New dependencies.** Compare the dependency files (`package.json`, `requirements*.txt`,
  `pyproject.toml`, `Gemfile`, `go.mod`, `Cargo.toml`) with the base. For each added package,
  search the code for where it is imported. None found is a finding.

## 3. Check every finding in the code

For each finding the reviewer returns:

- Open the file at the line. Confirm the concrete case: the caller exists, the value can really
  be empty, the code really is unused (search the whole project, including tests, configuration
  and strings).
- **A fake-test finding** (a test that passes even when the behaviour breaks): prove it when you
  can. Copy the project to a throwaway folder outside it (copy, not `git worktree`, which drops
  uncommitted edits; link big folders such as `node_modules` instead of copying them). Break the
  behaviour the test claims to guard, run only that test, then delete the copy. It still passes:
  confirmed. Also do this once for the test that guards the change's main behaviour, even when
  the reviewer did not flag it — reviewers miss fake tests that look busy.
- **A secret finding:** confirm it with `find_secrets.py`, never by printing the line. Check
  whether it was committed (`git log --oneline -- <file>`) and pushed
  (`git branch -r --contains <commit>`). A committed key counts as exposed: the fix is to
  replace it at the service, not only to delete it from the code.
- Keep, downgrade or drop it. Write one line for each dropped finding: what the reviewer said,
  and what the code shows. Push back with reasons; never "great point".

Add your own confirmed hits from step 2 (failed checks, secrets, unused dependencies) as findings.

## 4. Report

Plain words. Short sentences. Explain a technical term the first time you use it. Never print a
secret's value or a real person's data: name the file and line and the kind only.

```
**Verify: <branch or what was compared>**
Compared: <what> (<n> commits, uncommitted edits in <n> files, <n> new files).
Goal: <one sentence> (from <your words / the plan / commit messages>).
Verdict: <Ready to ship. | Fix 1 and 2 before you ship. | Not ready: <why>.>

Fix now
1. **<What goes wrong, in a few words>** — `path:line`
   - What goes wrong: <the concrete case, as the person using the app meets it>
   - Fix: <the smallest fix; prefer deleting code>
   - If we skip it: <the cost>

Fix before merge
2. ...

Note for later
3. ...

Checks I ran: <command> → <one result line>. <command> → <result>.
Dropped: <one line each, with the reason>.
Not checked: <what you could not check, and why>.
```

The ranks:
- **Fix now:** a person using the app loses data, money, access or privacy; the main job gives
  a wrong answer; a secret is exposed; the app no longer starts or the checks fail.
- **Fix before merge:** a bug in a less-used path; a fake test, or no test, over risky behaviour;
  a new dependency nobody uses; a real slowdown at the app's real load.
- **Note for later:** code that could be cut, small speed-ups, wording.

Number the findings across all ranks, so the user can say "fix 1 and 3". Nothing found: the
header, "Ready to ship. Nothing to fix.", the checks you ran, and what you did not check.

End with one question: which findings to fix now. Fix nothing before the user answers. Each fix
they pick is a `how-we-build` task at its own size.

## When `how-we-build` calls this

A Heavy task's review step uses this skill's steps 1–3, with the task's own goal and plan. The
fix round then follows `how-we-build`: the first two ranks go to one `builder` round, then the
checks run again, then stop.

---

Credit: some ideas come from the `/ponytail-review` command in ponytail by Dietrich Gebert
(github.com/DietrichGebert/ponytail, MIT license): read the callers of a change and not only the
diff; no concrete case, no finding; a shortcut marked in a comment that names its limit is a
decision, not a finding.
