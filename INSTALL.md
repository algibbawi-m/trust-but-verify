# Install trust-but-verify

**This file is for the AI tool.** A person gave you this repository's link and asked you to
install it. Follow these steps. The person may not be a programmer, so explain each step in plain
words before you do it.

## Rules for the whole install

- Ask the person for yes before you run any install command or copy any file.
- Never replace or delete a file this kit did not make. Each Codex helper file the kit makes
  starts with a line that begins `# Made by scripts/build.py`.
- Change nothing in the person's own projects. This install only touches the AI tool's settings.
- At the end, say exactly what you installed and how to remove it.

## 1. Find which tool you are

- Claude Code: go to section 2.
- Codex: go to section 3.
- Another tool that reads `SKILL.md` folders: go to section 4.

## 2. Claude Code

1. Tell the person: "I will add this kit as a plugin. It gives me two skills and five helpers. It
   changes nothing in your projects." Wait for yes.
2. Run these two commands:

   ```bash
   claude plugin marketplace add algibbawi-m/trust-but-verify
   claude plugin install trust-but-verify@trust-but-verify
   ```

   Inside a session, the same commands are `/plugin marketplace add algibbawi-m/trust-but-verify` and
   `/plugin install trust-but-verify@trust-but-verify`.
3. Run `claude plugin list`. Check that `trust-but-verify@trust-but-verify` shows as enabled.
4. Tell the person to start a new session, so the skills load.

## 3. Codex

1. Tell the person: "I will add this kit as a plugin and copy five helper files into your Codex
   settings. It changes nothing in your projects." Wait for yes.
2. Run these two commands:

   ```bash
   codex plugin marketplace add algibbawi-m/trust-but-verify
   codex plugin add trust-but-verify@trust-but-verify
   ```

   The second command prints the folder where the plugin was installed. Note it.
3. Install the helpers. A Codex plugin does not install helpers, so copy them by hand:
   1. List the files in `codex-agents/` inside the installed plugin folder.
   2. For each file, check whether `~/.codex/agents/` already has a file with that name.
      - If that file's first line begins `# Made by scripts/build.py`, it came from this kit.
        Replace it with the new one.
      - Otherwise, someone else wrote it. Do not replace it. Skip that helper, and tell the
        person which one you skipped.
   3. Copy the other files into `~/.codex/agents/`. Make that folder if it does not exist.
4. Check: `codex plugin list` shows `trust-but-verify@trust-but-verify` as installed and enabled, and
   `~/.codex/agents/` holds each helper you copied.
5. Tell the person to start a new session, so the skills and helpers load.

## 4. Another tool

1. Find the folder your tool reads skills from. If you cannot find it, ask the person.
2. Copy `skills/how-we-build/` and `skills/design-pass/` into it, after a yes.
3. Skip the helpers. Each skill can start a fresh helper from its own `references/roles/` folder.
   If your tool cannot start helpers, the skill does that step itself and tells the person.

## 5. Tell the person what they got

Say it in your own plain words:

- **how-we-build** starts when they ask to fix, add or change something in an app. It sizes the
  task, stops before anything that cannot be undone, writes tests first, and ends with what it
  checked and what it did not.
- **design-pass** starts when they say an app looks wrong or ask for a design review. It writes
  down a visual standard first, then has fresh helpers judge the pages against it.
- If a skill with the same name was already installed, say so. They may want to remove one.

## Remove the kit

Claude Code:

```bash
claude plugin uninstall trust-but-verify@trust-but-verify
claude plugin marketplace remove trust-but-verify
```

Codex:

```bash
codex plugin remove trust-but-verify@trust-but-verify
codex plugin marketplace remove trust-but-verify
```

Then look at each `trust_but_verify_*.toml` file in `~/.codex/agents/`. Delete it only if its first
line begins `# Made by scripts/build.py`. Leave any other file.
