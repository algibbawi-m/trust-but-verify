# trust-but-verify

Four skills for people who build software by directing an AI coding tool, but who do not read the
code. They work in **Claude Code** and in **Codex**.

You judge your app by what it does for the people who use it. These skills make the AI work in a
way you can judge the same way: it says how big a task is, stops before anything that cannot be
undone, proves its work with checks it ran, and tells you what it did not check.

## Install

**The easy way.** Paste this into Claude Code or Codex:

> Install the kit at https://github.com/algibbawi-m/trust-but-verify. Follow its INSTALL.md.

The AI reads [INSTALL.md](INSTALL.md), asks you before it changes anything, and tells you what
it installed.

**From the command line.**

| Tool | Commands |
|---|---|
| Claude Code | `claude plugin marketplace add algibbawi-m/trust-but-verify`<br>`claude plugin install trust-but-verify@trust-but-verify` |
| Codex | `codex plugin marketplace add algibbawi-m/trust-but-verify`<br>`codex plugin add trust-but-verify@trust-but-verify`<br>then copy `codex-agents/*.toml` to `~/.codex/agents/` |

Start a new session after you install.

## What you get

### how-we-build

It starts when you ask the AI to fix, add or change something in a software project.

- **It sizes the task** as Quick, Standard or Heavy, and tells you in one line. Bigger tasks get a
  written plan, tests first, and a fresh reviewer.
- **It stops before anything git cannot undo**: deploying, changing stored data, adding a
  secret, spending money. It tells you what will change and how to undo it, then waits for yes.
- **It keeps secrets and real people's data out** of code, tests, commits and chat.
- **It proves the work.** It runs the project's checks and quotes the result. It never writes
  "should work".
- **It stops guessing.** After two failed fixes that rest on the same belief, it tests that
  belief before it tries again.

### verify

It starts when you ask the AI to check work before it ships: "review my changes", "is this safe to
merge".

- **Whoever built the change never judges it.** A fresh reviewer gets the goal and the changes,
  never the story of how they were built.
- **It runs the checks itself**, and scans the changes for keys and passwords without printing
  them.
- **Every finding is checked in the code** before you see it. Wrong findings are dropped, with
  the reason.
- **It proves fake tests.** It breaks the behaviour in a throwaway copy. If the test still
  passes, the test guards nothing.
- **It changes nothing until you pick** which findings to fix.

### audit

It starts when you take over an app that an AI or someone else built: "audit this app", "what is
wrong with it", "what can I delete".

- **It maps the app first**: what it is for, how it runs, where its data and secrets live.
- **It splits the app into areas**, and a fresh reviewer reads each one. It tells you the count
  before it starts more than one.
- **It scans the whole history for secrets.** A key that was committed once is exposed, even if
  a later commit deleted it.
- **It ranks findings by what a person using the app would feel**, and lists code and
  dependencies that could be cut.
- **It changes no code.** You get one report, and each fix becomes its own task.
- **Run it again** when a more capable model comes out, or as the app grows. It compares with
  the last report: what was fixed, what is still open, and what is new.

### design-pass

It starts when you say the app looks wrong, or ask for a design review.

- **It writes the standard first**: type sizes, spacing, colours and the top of each page, as
  numbers a reviewer can measure.
- **The builder never judges its own page.** A fresh verifier compares each page with the
  standard at four screen sizes, in light and dark.
- **A two-person red team** uses the app: a senior product designer, and someone who has never
  seen it and tries real tasks.
- **Findings become build instructions**, ranked by what a person using the app would feel.

## How it fits together

```
skills/how-we-build ──► planner, builder, reviewer     (Heavy tasks; review runs through verify)
skills/verify       ──► reviewer
skills/audit        ──► reviewer, one per area
skills/design-pass  ──► design-lead, reviewer, red-team, builder

roles/*.md  ── the one place each helper is written
   │  scripts/build.py makes:
   ├──► agents/*.md                         Claude Code helpers (ship in the plugin)
   ├──► codex-agents/*.toml                 Codex helpers (copied to ~/.codex/agents/)
   └──► skills/*/references/roles/*.md      used when no helper is installed
```

The skills work without the helpers. If a helper is missing, the skill starts a fresh subagent
from its `references/roles/` file. If the tool cannot start one, the skill does the step itself
and tells you that nobody fresh checked the work.

Your project's own rules always win. If your project's instruction file (CLAUDE.md, AGENTS.md or
similar) sets its own steps or checks, the skills follow those.

## Change the kit

1. Edit the skill in `skills/`, or the helper in `roles/`. Do not edit the made files in
   `agents/`, `codex-agents/` or `skills/*/references/roles/`.
2. Run `python3 scripts/build.py`.
3. Run `python3 scripts/check.py`. It fails if a made file is out of date, if the skills' copies
   of a shared script differ, or if a file or commit holds an email address, a home-folder path,
   or a key.
4. Run `python3 -m unittest scripts/test_check.py`.

To keep your own private words out of the repo, list them one per line in
`.git/info/private-terms`. Git never pushes that folder. `check.py` then fails on any of those
words.

## Credit

This kit adapts ideas and some wording from two MIT-licensed skill kits. Their license notices
are in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

- [ponytail](https://github.com/DietrichGebert/ponytail) by Dietrich Gebert: the "question the
  need" steps and the "never cut" list in how-we-build, and the review and audit methods in
  verify and audit.
- [superpowers](https://github.com/obra/superpowers) by Jesse Vincent: in how-we-build, writing
  the test first and watching it fail, no "should work" without a check, no performative
  agreement with a review, stopping after repeated failed fixes, and the four things that stop
  an autonomous run.

## License

MIT. See [LICENSE](LICENSE).
