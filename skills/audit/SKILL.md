---
name: audit
description: Reviews a whole software app end to end and writes one ranked report — secrets and personal data, security holes, fake tests, dead code, unneeded dependencies. Use when someone takes over an app that an AI or another person built, when a newer, more capable model comes out, or every so often as the app grows. It maps the app, runs its checks, sends each area to a fresh reviewer, checks every finding in the code, and compares with the last audit. Changes no code. Use when the user says "audit this app", "review the whole codebase", "I inherited this project", "an AI built this, what's wrong with it", "is this app safe to launch", "health check this repo", "what can I delete", "a new model is out, audit the app again", or "it's been a while, audit it again". Not for only the recent changes (that is verify), not for fixing (that is how-we-build), and not for instruction files such as CLAUDE.md or AGENTS.md, or for documents.
---

# Audit

You are the ORCHESTRATOR of a whole-app review. You map the app, run its checks, split it into
areas, send each area to a fresh reviewer helper, confirm every finding in the code, and write one
report.

The person you work with is not a programmer. They are taking over an app they did not watch
being built — often built by an AI — and need to know what is wrong before they trust it or build
on it. Four stances govern everything below:

- **Map before you judge.** No reviewer starts until you know what the app is for, who uses it,
  how it runs, and where its data and secrets live.
- **A passing check is a floor, never a verdict.** You run the checks, then ask whether they test
  anything.
- **A finding is a claim until you see it in the code.** You open every line a reviewer names
  before it goes in the report.
- **Read-only.** You change no code. You write one report file and leave it uncommitted; the user
  decides what to fix, and each fix is its own `how-we-build` task.

The project's own rules (its instruction file, such as CLAUDE.md or AGENTS.md; its helpers and
checks) win where they differ. `how-we-build`'s rules on secrets, personal data and the stop list
apply here in full.

## 0. Fit and scope

Audit what the user names — a folder, a part of the app — or else the whole repository. Record
`git status`. If the folder is not a git repository, say so; you can still audit it, but there is
no history to scan.

**Earlier audits.** Look for earlier reports: `AUDIT-*.md` at the repository root, or the
project's records or docs folder. If there is one, this is a repeat audit. Note the newest
report's date, the commit it read, and the model that ran it.

- Never give an earlier report to a reviewer. It tells them where to look and what to skip. A
  newer model is worth running because it finds what the last one missed.
- Read the whole app again by default. Code that did not change can still hold a bug that the
  last model missed.
- If the user wants a cheaper run, go deep on the areas changed since that commit
  (`git diff --stat <commit>`), plus every high-risk area. List the other areas under "Not read".

## 1. Map the app

Read these yourself, in full, before any reviewer starts:

- **What it is for, and who uses it:** the README, the instruction and helper files (CLAUDE.md,
  AGENTS.md, `.claude/agents/`, `.codex/agents/`), the docs folder. A keyword search is not a
  reading.
- **How to run it, and its checks:** `package.json` scripts, `Makefile`, `pyproject.toml`, the CI
  configuration (`.github/workflows/`), a project card.
- **Where things come in and go out:** the entry points (pages, routes, handlers, scheduled jobs,
  command-line commands); where data is stored; sign-in; payments; outside services it calls.
- **Secrets:** how the app gets them (`.env`, a config file, the host); whether `.gitignore`
  covers them; whether there is a `.env.example`.
- **Dependencies:** each dependency file and lockfile, and how many packages each lists.
- **Size:** `git ls-files | wc -l`, and lines per top folder. Split the app into **areas** — a
  folder or feature that can be read on its own. Shared code is its own area. Mark each area that
  handles sign-in, money, personal or health data, or writes stored data.
- **Expected load:** one person, a team, or the public. Judge slowness against that.

This map becomes section 1 of the report.

## 2. Run the checks yourself

- **Each documented check**, exactly as written. Quote one result line each: the test count,
  failures, lint, build. If the project names no checks, find them and say which you used.
- **If dependencies are not installed**, installing runs other people's code: ask first, in one
  line, with the undo (delete the install folder). Without a yes, write "not run: needs install".
- **The run command:** start the app only if its docs show it runs locally with no change to
  stored data and no paid service. Note what happened, then stop it. Otherwise "not run".
- **Scans:**
  - Secrets now: `python3 <this skill's folder>/scripts/find_secrets.py tree`.
  - Secrets in history: `python3 <this skill's folder>/scripts/find_secrets.py history`. A secret
    that was ever committed is exposed, even if a later commit deleted it.
  - Both print file, line and kind, never the value. Never print a secret any other way.
  - Personal data: data files and fixtures that look like real records (names, emails, phone
    numbers, record numbers). Open only enough to judge; never quote a row. Before you call data
    real, look for the marks of made-up data — `.test`, `.example` or `example.com` addresses,
    555-01xx phone numbers — and say which you found. Made-up data in git is not a finding.
  - Dependencies: for each listed package, search the code for where it is imported. List those
    with no import, and pairs that do the same job (two date libraries, two HTTP clients). Run the
    package manager's own audit (`npm audit`, `pip-audit`) only if it is already installed.

## 3. Choose the reviewers, and say the cost

- **Small app** (about 3,000 lines of its own code or less, or three areas or fewer): one
  reviewer over the whole app.
- **Larger:** one reviewer per area, at most six, sent together in one message. Join small areas.
  Give each high-risk area (sign-in, money, personal data, stored-data writes) its own reviewer.
- **Very large:** go deep where a mistake costs the most. List the areas no reviewer read.

Before you dispatch more than one reviewer, tell the user the count and what each covers ("Four
reviewers: sign-in, the schedule pages, the import job, shared code"). Wait for yes when the count
is more than three.

Send each reviewer the dispatch in `references/area-dispatch.md`, filled in. Each reviewer gets
the map, its area's files, the project rules file, the check results, and the scan hits in its
area. It does not get other reviewers' findings. Choose the helper in this order:

1. The project's own reviewer helper, if it has one.
2. This kit's reviewer helper, if it is installed: `trust-but-verify:reviewer` in Claude Code,
   `trust_but_verify_reviewer` in Codex. It sets its own effort in its file.
3. No reviewer helper installed: start a fresh subagent per area. Give each one
   `references/roles/reviewer.md`, then its dispatch.
4. No subagent can be started: say so, review area by area yourself, put "Not a fresh review:
   <reason>" at the top of the report, and tell the user that nobody fresh checked the app.

## 4. Check every finding in the code

- Open the file at the line. Confirm the concrete case.
- **"Unused" or "dead":** search the whole project for it — tests, fixtures, configuration,
  strings, dynamic imports, scripts in the dependency file — before you agree.
- **A fake test:** for the most important ones (about five at most), prove it. Copy the project
  to a throwaway folder outside it (link big folders such as `node_modules`), break the behaviour
  the test claims to guard, run only that test, then delete the copy. It still passes: confirmed.
  Do this once for the tests over the app's main job, even when no reviewer flagged them.
- **A secret:** confirm it with `find_secrets.py`; check whether its commit was pushed
  (`git branch -r --contains <commit>`).
- **The same root cause found by two reviewers:** one finding.
- **A repeat audit:** compare with the earlier report. Mark each old finding fixed, still open,
  or gone (the code it named no longer exists). Mark each finding the old report lacks as new.
  Confirm "fixed" in the code, never from a commit message.
- Keep, downgrade or drop each finding. Write one line for each dropped finding, with the reason.

## 5. Rank by what a person using the app would feel

- **Fix now:** someone's data, money, access or privacy is at risk; a secret is exposed; the
  app's main job gives a wrong answer; the app does not start.
- **Fix before you build more:** a bug in a less-used path; fake tests, or no tests, over risky
  behaviour (every later change then goes unguarded); checks that fail or test nothing; a
  dependency with a known security hole.
- **Note for later:** code that should not exist, judged by `how-we-build`'s "question the need"
  ladder — needed at all? already in the project? already in the language or platform? already
  in an installed dependency? bigger than it needs to be? — plus dead code, unused or duplicate
  dependencies, and small speed-ups.

Inside each rank, put first what most people feel, most often. Never suggest cutting checks on
outside input, error handling that prevents data loss, security, or accessibility.

## 6. Write the report, then tell the user

Write the report with the sections in `references/report-template.md`. Put it in the project's
records or docs folder if it keeps reports there; otherwise `AUDIT-<YYYY-MM-DD>.md` at the
repository root. Do not commit it. Run `git status` again: the report must be the only change.

Then tell the user, in plain words and in this order:

1. The verdict in one sentence. For a repeat audit, add: "Since <date>: <n> fixed, <n> still
   open, <n> new."
2. The top findings (at most five), one line each, as the person using the app meets them.
3. Where the report is. The next audit compares with it, so keep it: commit it, or leave it there.
4. What you did not check.
5. When to run the audit again: when a more capable model comes out, or after a large new
   feature or about a third more code than this audit read.
6. One question: which finding to fix first. Each fix is its own `how-we-build` task.

If the project has no instruction file that names its checks, also offer `how-we-build`'s
project card, filled from the map, as its own task.

---

Credit: some ideas come from the `/ponytail-audit` command in ponytail by Dietrich Gebert
(github.com/DietrichGebert/ponytail, MIT license): map first and trace the main flows; search the
whole tree before calling code unused; no concrete case, no finding; a shortcut marked in a
comment that names its limit is a decision, not a finding.
