---
name: design-pass
description: Runs a design pass on any app with a UI — writes (or reads) the project's visual direction, builds pages to it, and judges them with a fresh design verifier and a two-seat red team (a senior product designer and someone who has never seen the app) instead of trusting passing checks. Use when the user wants the app's look reviewed, polished, redesigned or brought to a standard; says pages look clumsy, misaligned, mangled or "not clean"; asks for a design review, design red team or design polish; or starts UI work on a project that has no design direction yet.
---

# Design pass

You are the ORCHESTRATOR of a design pass. Helpers draw, build, verify and attack; you choose the
size, turn findings into build instructions, look at every page yourself, and make the work ready
to merge. Merge only when the project's rules or the user say so.

This skill exists because pages were once called "clean" because they had no sideways scroll and
nothing overlapped, while the owner saw mangled tabs, no alignment and no sense of smoothness.
Four stances govern everything below:

- **A passing check is a floor, never a verdict.** A page is done when it matches the direction and
  a fresh designer cannot find it clumsy.
- **The standard is written before anyone builds.** No direction file, no building.
- **Whoever built a page never judges it.** The verifier and the red team are fresh helpers.
- **Findings become build instructions,** ranked by what a person using the app would feel —
  never opinions left for the builder to interpret.

The project's own rules (its instruction file such as CLAUDE.md or AGENTS.md, its test gate,
merge process and records) override anything procedural here. This skill decides how the design is
judged, not how the project commits.

## 0. Choose the size — tell the user, ask only on a conflict

Check two facts yourself:

1. **Is there a written direction?** Look for a design direction file (`design/DIRECTION.md` by
   default; also search the project's docs and instruction files for one). A direction counts only
   if it fixes type sizes, spacing, colour meanings and the top of the page at each width.
2. **How much is touched?** Count the screens the request changes.

| Situation | Path |
|---|---|
| No direction exists | **Direction first** (§1), whatever the size, then light or full |
| Direction exists; 1–3 screens | **Light**: build → verifier → one red team at the end → you look |
| Direction exists; most of the app, or before a launch | **Full**: mockups → per page build and verifier → red team every 2–3 pages and at the end → you look |
| The user says something that passed its checks looks wrong | **Full** on those screens |

State the path in your opening message in one line ("No direction yet, so I'll write one first,
then a light pass over the two screens"). The user can overrule in one word. Ask only when the facts
disagree — a direction exists but the running app plainly contradicts it, or the scope is unclear.
Full passes are expensive (a whole-app pass ran thousands of messages); never default to full when
light fits.

## 1. Direction first (only when none exists)

1. **Walk what is there.** A design lead (§6) opens every screen at the four sizes (§4), light and
   dark, and lists what feels clumsy *with measurements* — "the app's name is the smallest text
   on the bar (11.5px)", "the selected tab turns bold and shifts its neighbours". If there is no
   running app yet, it works from what the app is for and who uses it.
2. **Offer two or three contrasting directions** as small HTML mockups filled with the app's real
   (or realistic placeholder) content, each named by a one-line feeling ("a well-kept notebook",
   "a bright dashboard"). The user picks. **This choice is always the user's** — the one question
   the skill must ask.
3. **Write the chosen direction** to `design/DIRECTION.md` (or where the project keeps design docs),
   with every section in `references/direction-template.md`. Mockups go beside it.

For a tiny app the direction may be one page; it is still written. Later passes then run light
against it.

## 2. Build

Per page, in the direction's order (the shell — header and page head — first, since every page
sits in it):

- **Full path:** if the page is not in the mockups, the design lead draws its phone and laptop frames
  first, from real content.
- One builder per page, in its own git worktree where the project allows, one commit per page.
- Tests assert structure and data attributes, never wording.
- The builder runs the project's whole test gate, not only the UI tests — page text is often asserted
  elsewhere.

## 3. Verifier

A fresh helper that did not build the page serves it, opens it in a browser it can drive, and
compares it against the direction and mockup at the four sizes, light and dark. It returns
**MATCH** or a numbered **DIVERGE** list, each item with the size, the screenshot, and what the
direction says. DIVERGE items go to one fixer round; the verifier then looks again. An item that
diverges twice comes to you to rule on — fix, or amend the direction and say so.

## 4. The four sizes, and the browser

375×812 (phone), 768×1024 (tablet), 1280×800 (laptop), 1440×900 (wide), each in light and dark.
Set the browser back to desktop size when done.

**No browser.** Every check in this skill needs a browser you can drive. Some tools have none (for
example, Codex CLI and its IDE extension). Then use the project's own browser tests, such as
Playwright, if it has them. If it has none, stop and tell the user that a visual check needs a
browser. Never call a page done without one.

## 5. Red team

Two fresh helpers, started together, over the merged or merge-ready app:

- **A senior product designer** hunting what is still clumsy, inconsistent or ugly: alignment to one
  left edge, the type scale, spacing rhythm, one word per state, controls that look alike behaving
  alike, what happens when you scroll, select, go back.
- **Someone who has never seen this app**, doing the three to five real tasks the app exists for
  (you name them from its purpose — "book a table for four on Friday"), reporting where they got
  lost, what they misread, and what made them hesitate.

**Light:** once, at the end. **Full:** every two or three pages, and once at the end. A later round
opens by confirming the earlier round's fixes held.

You turn their reports into a red-team record (`design/RED-TEAM-<n>-<date>.md`, or the project's
records folder):

- **What both liked, and must not be broken.**
- **Rulings**, grouped by who builds them, each: the finding's tag (D3 for the designer, S5 for the
  newcomer), then **Build:** one concrete instruction ("the question at the answer's size, weight 400").
- **Not built, and why** — each routed: not a design issue (to whoever owns it), a choice only the
  user can make (to their decision list with a recommendation), or kept because the direction chose
  it.

The rulings go to builders exactly as written, then through the verifier.

## 6. Seats and helpers

- **A design skill first.** Every design seat — design lead, verifier, both red-teamers, and you
  before judging — loads a frontend design skill first if one is installed (in Claude Code,
  Anthropic's `frontend-design` plugin). Its report says which skill it loaded, or that none was
  installed. A seat whose report does not say is run again.
- **Which helper for which seat.** Design lead → `design-lead`; verifier → `reviewer`; both
  red-team seats → `red-team`; builders and fixers → `builder`.
- **Finding the helpers.** Use the project's own helpers where it has them. Otherwise use this
  kit's: in Claude Code, `trust-but-verify:design-lead`, `trust-but-verify:reviewer`, `trust-but-verify:red-team`
  and `trust-but-verify:builder`; in Codex, `trust_but_verify_design_lead`, `trust_but_verify_reviewer`,
  `trust_but_verify_red_team` and `trust_but_verify_builder`. If a helper is not installed, start a fresh
  subagent with the matching file in `references/roles/`, then the task.
- **No subagents at all.** If your tool cannot start a fresh helper, the verifier and red team
  cannot be fresh. Do those steps yourself, and tell the user in the closing brief that nobody
  fresh judged the pages.
- The kit's helpers set their effort in their files. A fresh subagent without a file uses whatever
  effort your tool gives it.
- Prompts for each seat: `references/dispatch-templates.md`.
- Each seat that uses a browser works in its own tab or window, and changes no data except on a
  throwaway copy.

## 7. You look, then close

Before any merge, open every changed page yourself at phone and laptop size. "Nothing overlaps" is a
floor, not a verdict.

Close by showing the user the pages — screenshots at phone and laptop, or a live page they can click —
with what changed that they will see, what waits on their decision, and what is next. Ask nothing
mid-way unless only they can decide it. Short progress notes are fine.
