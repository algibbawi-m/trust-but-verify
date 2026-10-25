# Project card

Add this section only to the instruction file your tool reads: CLAUDE.md for Claude Code,
AGENTS.md for Codex. If the project has both, write the card in one and point to it from the
other. Never add it to a file the product ships or its users read. Fill each line from what the project
already has; ask the user only for what the files cannot tell you.

```markdown
## Project card

- **What it is, and who uses it:** <one sentence>
- **Run it:** <exact command>
- **See it work:** <start command> · <where to go: URL or screen> · <one thing to try, and what you should see> · <where screenshots go> · <how to stop it>
- **Checks:** <lint command> · <test command, with today's count, or "no tests here"> · <build command, if any>
- **Heavy here:** <folders, files or kinds of change where any edit is Heavy>
- **Off-limits:** <data, files and secrets that are never read, printed or committed>
- **Merge:** <who merges, and on which branch work happens>
- **Deploy:** <how, and who decides to deploy>
```
