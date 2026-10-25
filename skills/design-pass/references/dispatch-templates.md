# Dispatch templates

Fill the <angle brackets>. Every judging template opens with the design-skill line; a report that
does not say which skill was loaded, or that none was, is run again. Send each prompt to the
matching helper (see §6 of SKILL.md for its name in your tool), or to a fresh subagent that first
reads the matching file in `references/roles/`.

## Design lead (`design-lead` helper)

> If a frontend design skill is installed, load it first. Say in your report which skill you
> loaded, or that none was installed.
>
> You are the design lead for <app>, used by <who> to <what>. Change nothing in the product.
> Serve the app with <how to run it>, open it in a browser you can drive, and walk every screen at 375×812,
> 768×1024, 1280×800 and 1440×900, light and dark.
>
> 1. List what feels clumsy, each with a measurement (sizes in px, what shifts, where two pages
>    disagree).
> 2. <If no direction:> Draw two or three contrasting directions as one HTML mockup file at
>    <path>, each titled by a one-line feeling, each showing <the two or three most-used screens>
>    at phone and laptop with the app's real content. Do not pick; the user picks.
>    <If a direction exists:> Draw <page> at phone and laptop in the direction's grammar, into
>    <path>, from real content.
> 3. <After the user picks:> Write the direction to <path> with every section of
>    <skill>/references/direction-template.md, numbers not adjectives, ending with the build order
>    and the one or two changes that matter most on each page.
>
> Set the browser back to desktop size at the end.

## Builder (`builder` helper)

> Build <page> to the direction at <path> and its mockup frames at <path>, in the worktree
> <path> on branch <branch>. One commit for the page. Tests assert structure and data attributes,
> never wording. Run <the project's lint> and <the project's whole test gate> and report the literal
> counts. Do not judge the look; a verifier will. If the direction cannot be built as written, stop
> and say which line and why rather than improvising.

## Design verifier (`reviewer` helper)

> If a frontend design skill is installed, load it first. Say in your report which skill you
> loaded, or that none was installed.
>
> You did not build this page. Serve <branch/worktree> with <how>, open a browser you can drive, and compare
> <page> against the direction at <path> and the mockup at <path> at 375×812, 768×1024, 1280×800
> and 1440×900, light and dark. Check: one left edge; every text size on the direction's scale;
> spacing on its steps; the top of the page at each width; hover, focus and selected states; empty
> and error states; text never cut; nothing floating; nothing moving under the reader when
> selecting or scrolling.
>
> Return MATCH, or DIVERGE with a numbered list: size and theme, what you see (measured), what the
> direction says, screenshot. No wording nits unless the direction fixes the word. Set the browser
> back to desktop size at the end.

## Red team — senior product designer (`red-team` helper)

> If a frontend design skill is installed, load it first. Say in your report which skill you
> loaded, or that none was installed.
>
> You are a senior product designer seeing <app> for review. Serve <main or branch> with <how>,
> open a browser you can drive, and use every page at phone and laptop, light and dark. Hunt what is still
> clumsy, inconsistent or ugly: edges that do not line up, sizes off the scale, uneven gaps, one
> state called several words, look-alike controls behaving differently, what happens when you scroll,
> select, go back, or land on a bad link. The direction is at <path>; where the direction itself
> looks wrong, say so.
>
> <If a later round:> First confirm each ruling in <previous red-team record> held.
>
> Return findings numbered D1, D2…, ranked by what a person using the app would feel, each with the
> page, the size, a measurement and a screenshot. Also list what works and must not be broken.

## Red team — someone who has never seen this app (`red-team` helper)

> If a frontend design skill is installed, load it first. Say in your report which skill you
> loaded, or that none was installed.
>
> You have never seen <app>. You are <the kind of person who uses it>, not a programmer, with a few
> minutes between other work. Serve it with <how>, open a browser you can drive at phone size (375×812) and
> then a laptop, and try to do these real tasks:
> 1. <task>
> 2. <task>
> 3. <task>
>
> Do not read the code or the design documents. Report, numbered S1, S2…, every place you got lost,
> misread something, hesitated, or were told something in words you would not use — quote what the
> screen said and say what you expected. Also say which moments felt right. Change no data except
> on the throwaway copy at <path>.
