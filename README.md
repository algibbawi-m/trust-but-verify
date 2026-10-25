# trust-but-verify

Two skills for people who build software by directing an AI coding tool, but who do not read the
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
skills/how-we-build ──► planner, builder, reviewer     (Heavy tasks)
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
3. Run `python3 scripts/check.py`. It fails if a made file is out of date, or if a file or commit
   holds an email address, a home-folder path, or a key.
4. Run `python3 -m unittest scripts/test_check.py`.

To keep your own private words out of the repo, list them one per line in
`.git/info/private-terms`. Git never pushes that folder. `check.py` then fails on any of those
words.

## License

MIT. See [LICENSE](LICENSE).
