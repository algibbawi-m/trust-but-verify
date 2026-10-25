---
name: how-we-build
description: Use for any task that changes a software project's code or configuration, or that deploys, migrates, installs, deletes, or changes stored data, secrets or servers — a fix, a feature, a refactor — and for any bug, failed test or odd behaviour in a software project. Not for documents, slides or notes, nor for questions answered in chat.
---

# How we build

The person you work with is not a programmer. They rely on this method to build well, and they
judge the work by what the product does for its user.

**The project's own rules win.** Where the project defines its own sizes, steps, helpers, checks,
review chain, merge rule, records or brief format, use those in full. Its rules live in its
instruction file (CLAUDE.md, AGENTS.md or similar). This skill fills only what the project leaves
unsaid. Never use it to skip a step the project requires. A session that resumes from a project
log follows that project's protocol and does not stop for the approvals here. The project's brief
format, records and branch rule also win: put this skill's size line and closing lines inside
them. Where the project names no branch rule, branch first when you are on the default branch.
Change project files only in a git repository; if the folder is not one, find the repository its
rules point to, or say so before you edit. Work outside a repository, such as on a server or a
setting, follows the "git cannot undo" rule below: make the undo first.

## Always, whatever the size

**Before anything git cannot undo**, stop. This means: deploying or pushing; a database migration
or any change to stored data; deleting files or data outside git; adding, changing or rotating a
secret; adding or upgrading a dependency; changing who can sign in; spending money or calling a
paid service; changing a server, domain or scheduled job. Tell the user in one line what will
change and how to undo it. Make that undo exist first (a dump, a copy, a tag, the current
version; for a secret, where the old value is kept). Wait for yes. A plan's yes covers such a step
only when the plan names it and its undo. If there is no undo, say so in those words. Use a dry
run or a copy first where one exists.

**Secrets and personal data.**
- Never print, paste or commit a secret, key or password. If the user types one into chat, do
  not repeat it. A live key (not a test key) shown in chat counts as exposed: tell them to replace
  it.
- Before a task puts a secret in a file, make sure `.gitignore` covers that file.
- Before each commit, run `git diff --cached --name-only`. Stop if it lists a `.env`, key or
  token file.
- No real person's data (customers, staff, users) in code, tests, fixtures, commits or chat.
  Use made-up names. If the user gives real data, stop and say so first.
- A secret that was committed is exposed: tell the user it must be replaced, not only deleted.
- A new project gets a `.gitignore` for env files and keys before its first commit.

**Other people's work.** Record `git status` before you start. Never revert, stash, reset or
delete changes you did not make. When a file mixes the user's work and yours, stage only yours
with `git add -p`.

## 0. Check the fit, then size the task

First check that the request fits this project: the page, file or feature it names exists, and
this is the project it belongs to. If not, ask one question before anything else.

If the user asks why something happens and not for a change, go to "When something breaks",
report the cause, and stop. Size the fix only when they ask for one.

Answer in order; the first yes decides.

1. **Heavy** — the project card's "Heavy here" list names it. With no card: a wrong result could
   change the product's main output, sign-in or security, stored personal or health data, or
   payments and billing. Or the user asks for the full path.
2. **Standard** — it touches more than a couple of files, the approach is a judgment call, or it
   is on the "git cannot undo" list above.
3. **Quick** — everything else: clear, small, one place.

Say the size in one line before you start ("Standard: it touches three files"), inside the opening
brief where the user's rules ask for one. The user can change it in one word. When you cannot
tell, take the larger size and say why. If the task grows, stop, say so, and move up one size. For
Heavy, also say the rough cost: how many helper runs.

| Step | Quick | Standard | Heavy |
|---|---|---|---|
| 1 Understand | read the ask | the goal opens the plan | short written design, user approves |
| 2 Question the need | rungs 1–2 | all rungs | all rungs |
| 3 Plan | — | written plan, one yes | `planner` writes it; shown, not waited on |
| 4 Build test-first | if behaviour changes | yes | yes, by `builder` |
| 5 Run the checks | yes | yes | yes |
| 6 Review | — | re-read the diff once | fresh `reviewer`, one fix round |
| 7 Finish | commit + brief | commit + brief | merge decision + brief |

## 1. Understand

- One question per message, in plain words.
- Before you ask, check whether running something can answer the question. If a quick throwaway
  sketch outside the project settles a technical choice, build it, show what it did, and mark the
  choice "my call". Ask the user only what the product should do, what they prefer, or what only
  they know.
- Quick: if one detail is unclear, ask it, or make an assumption that is easy to undo and say so.
- Standard has one stop: the plan opens with the goal in the user's words, and their yes covers
  both. If the request is already clear, say so and offer to start.
- Heavy: write a short design as the first section of the plan file — the goal, what it will not
  do, constraints, open questions. The user approves the design; the plan after it is shown, not
  waited on.
- Mark your own choices as "my call". Never present them as something the user agreed to.

## 2. Question the need

Before you write code, stop at the first rung that solves it:

1. Does this need to exist at all?
2. Does the project already have it?
3. Does the language or platform already do it?
4. Does an installed dependency already do it?
5. Only then: the smallest version that works.

A new dependency is at least Standard. Name the package, where it comes from, its last release
date, and why nothing installed does the job. Open its page before you install it; never install
from a name typed from memory. Pin it in the lockfile.

Never cut: validation of outside input, error handling that prevents data loss, security,
accessibility, anything the user asked for, and the tests the project requires.

Be minimal about the solution, never about the change. Before you change anything, list every
place the change must reach (callers, tests, configuration, documentation) and what it could
break for users, including data it could destroy or expose.

## 3. Plan

- Standard: if you can enter your tool's plan mode yourself, use it. Otherwise post the plan in
  chat and wait for yes. Name the files, the order, and the checks that prove it done. Walk the user through it in
  plain words.
- Heavy: have the `planner` helper write the plan file. Unless the project names a place, the
  file is `docs/plans/<date>-<topic>.md`, committed with the work.
- Every plan has a "what could go wrong" list: the likely real failures, and the test for each.
- No line that decides nothing ("handle edge cases", "add validation", "TBD").

## 4. Build test-first

- When behaviour changes, write the test first. Run it and see it fail for the right reason.
  Then make the change.
- If the code came first, take the change out, show that the test fails, then put it back.
- Every guard or validation gets a test that fails when that guard is deleted.
- Judge each test you write or keep by two imagined edits. Break the behaviour: the test must
  fail. Change only the inside of the code, with the same result for the user: the test must
  still pass. Rewrite a test that fails either edit.
- Take each expected value from the requirement, never from a run of the code under test.
- Test a range at its first and last edge, never the middle only.
- Changes that alter no behaviour (wording, comments, renames) need no new test.
- For a change to how a screen looks, use the project's screen tests if it has them; otherwise
  a screenshot at the failing size, before and after, is the test.
- If the project has no test setup, do not add one inside another task. Show the behaviour
  before and after instead, write "no tests here" in the brief, and offer test setup as its own
  Standard task.
- Heavy: give the plan to the `builder` helper. Tell it to write the failing test first and
  report the failing run. Single attempt; if the plan cannot be built as written, it stops and
  says which line and why.

## 5. Run the checks

- Run the project's named checks yourself (lint, tests, build) and quote the result in the same
  message that says the work is done. A helper's "it passes" is a claim, not a check.
- Run every documented command the change relies on, exactly as written.
- Your change adds only the files it meant to touch.
- For a change the user can see, show it: a screenshot, or the exact steps to see it. For a bug,
  rerun the original failing steps and show the result.
- Use the project card's "See it work" line to start and drive the app. If the project has no
  such line, write one the first time you drive the app, and run it once from start to end
  before you trust it. Offer it to the user as its own commit.
- Never write "should work", "probably" or "seems fixed". Say what you ran and what it showed,
  or say "not checked".
- If the project names no checks, find them (package.json, pyproject.toml, Makefile) and say
  which you used.

## 6. Review

- Standard: re-read your diff against the goal once before you commit.
- Heavy: run the review in the `verify` skill, steps 1–3. Without it, give the `reviewer`
  helper the goal, the plan and the diff — never the story of the build. Ask for findings in
  three ranks: fix now, fix before merge, note for later. Send the first two ranks to one
  `builder` fix round, run your checks, then stop. Wording-only findings never block.
- When you receive review, check each finding in the code before you act on it. Push back with
  reasons when it is wrong. No "great point".

## 7. Finish

- One task, one commit. The message says what the user gets, and why. Write the project's own
  records if it keeps them.
- Merging, pushing and deploying are the user's decision unless the project's rules hand them
  to you in writing.
- Never delete a branch, a commit or uncommitted work you did not create this session, unless
  the user types "discard" after you list what will be lost. Temporary files you made this
  session are yours to remove.
- End the closing brief with: the command you ran and one line of its result; what the user can
  click or run to see the change; what you did not check; any risk they must know; what you
  skipped on purpose, and when to come back to it.

## When something breaks

1. Reproduce it. Read the whole error. Check what changed recently. If you cannot reproduce it,
   ask where and how the user sees it; do not guess.
2. Find the root cause: trace the bad value back to where it starts.
3. Test one guess at a time, with the smallest change that tests it.
4. If the user only asked why, report the cause in plain words and stop here.
5. Write a failing test, then make one fix.
6. Before you fix shared code, find every place that uses it.
7. After two failed fixes that rest on the same belief, stop fixing. Write that belief as one
   sentence. Find one observation that would come out differently if the belief were false, and
   make it. Start the next fix only after that test.
8. After three failed fixes, stop. Tell the user in plain words that the design may be wrong.

## Project card

Offer a card only when the project has no instruction file that names its checks, or when the
user asks. If the project's rules already name its checks and merge rule, write nothing, except
the "See it work" line from step 5 when it is missing. Put a card only in the
instruction file your tool reads: CLAUDE.md for Claude Code, AGENTS.md for Codex. If the project
has both, write the card in one and point to it from the other. Never put it in a file the product
ships or its users read. Use `references/project-card.md`, show it to the user in plain words, and commit it on its
own.

## Helpers

Heavy tasks use three helpers: `planner`, `builder` and `reviewer`. Each one starts fresh, so it
judges the work and not the story of how it was made.

1. Use the project's own helpers where it has them.
2. Otherwise use this kit's helpers. In Claude Code they are `trust-but-verify:planner`,
   `trust-but-verify:builder` and `trust-but-verify:reviewer`. In Codex they are `trust_but_verify_planner`,
   `trust_but_verify_builder` and `trust_but_verify_reviewer`.
3. If a helper is not installed, start a fresh subagent. Give it the matching file in
   `references/roles/`, then the task.
4. If your tool cannot start a subagent, do the step yourself. Say in the closing brief that no
   fresh helper looked at the work.

The kit's helpers set their effort in their files. A fresh subagent without a file uses whatever
effort your tool gives it. Never start a helper to re-check routine work; your checks in step 5
do that. For how a UI looks, use the `design-pass` skill. To review changes on demand, before
they ship, use `verify`; to review a whole app, use `audit`. As a Claude Code plugin, each skill
name starts with `trust-but-verify:`, for example `trust-but-verify:verify`.

In an autonomous run, stop for only four things: a step git cannot undo, a security-sensitive
change, a side effect others will see (merge, push, publish, send), or a plan so broken that
every path is a guess.

---

Credit: some ideas come from two skill kits, both under the MIT license.
- ponytail by Dietrich Gebert (github.com/DietrichGebert/ponytail): the "question the need" steps
  and the "never cut" list.
- superpowers by Jesse Vincent (github.com/obra/superpowers): write the test first and watch it
  fail; no "should work" without a check; no performative agreement with a review; stop after
  repeated failed fixes; the four things that stop an autonomous run.
