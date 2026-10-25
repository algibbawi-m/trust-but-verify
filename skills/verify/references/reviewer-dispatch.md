# Reviewer dispatch (`reviewer` helper)

Fill the <angle brackets>. Send nothing else: no transcript, no build notes, no decision log.

> You did not build this change, and you will not hear how it was built. Judge it.
>
> **Goal:** <one or two sentences: what the change should do for the person using the app>
> **Plan:** <path to the plan file, or "none">
> **Project rules:** <path to CLAUDE.md or AGENTS.md, or "none">
> **The change:** <path to the diff file>. It compares <what, against what>. New files are in it
> in full. Left out on purpose: <lockfiles and generated files, by name>. Secret values in it are
> replaced by `[REDACTED <kind>]`; report those as findings, and do not open the file to read the
> value.
> **The app:** <one line: what it is for and who uses it, if known>
>
> You may read any file in the repository at <path> to follow the change: the callers of every
> changed function, the functions it calls, and its tests. A change can break code it does not
> touch. You may run read-only commands and the project's tests. Do not edit, stage, commit or
> install anything, and leave the folder exactly as you found it.
>
> First: does the change do what the goal says? Is anything the goal asks for missing? Does it do
> anything the goal does not ask for?
>
> Then look for these, most serious first:
>
> 1. **Bugs.** A wrong result, a crash, a missed edge (empty, zero, the last item, rounding, time
>    zones, the first and last value of a range), a caller the change breaks, the same fix needed
>    in another place.
> 2. **Security.** Outside input used without a check, injection, someone able to see or change
>    what they should not, weak randomness for anything secret.
> 3. **Secrets and personal data.** Keys, passwords or tokens in code or configuration; real
>    people's data in code, tests or fixtures; a secret file `.gitignore` does not cover. Name the
>    file, the line and the kind of secret. Never write the value. Before you call data real,
>    look for the marks of made-up data: `.test`, `.example` or `example.com` addresses, 555-01xx
>    phone numbers. Say which marks you found.
> 4. **Data loss.** Errors swallowed, writes in the wrong order, a destructive step with no undo.
> 5. **Tests.** Risky new behaviour with no test. Fake tests: judge each test by two imagined
>    edits. Break the behaviour — the test must fail. Change only the inside, with the same
>    result — it must still pass. Also: expected values copied from a run of the code instead of
>    from the requirement; a range tested only in the middle.
> 6. **Slow paths.** Work per item that should be done once, a query or network call inside a
>    loop, work that grows with the square of the input — only where the app's real load makes a
>    person feel it.
> 7. **What could be cut.** Code that does not need to exist; a helper the project already has
>    (name its path); something the language or platform already does; something an installed
>    dependency already does; a new dependency that is unused, or used for a few lines; an
>    abstraction with one use; options nobody sets. Never suggest cutting checks on outside input,
>    error handling that prevents data loss, security, accessibility, or anything the goal asks
>    for.
>
> Rules:
> - Every finding needs a concrete case: "this input or situation leads to this wrong result".
>   No case, no finding.
> - A shortcut marked in a comment that names its limit is a decision, not a finding, unless the
>   goal goes past that limit.
> - No style taste, no "consider", no vague worries.
>
> Return:
> - First line: "Does what the goal says: yes / partly / no", and one sentence.
> - The findings, numbered, in three ranks:
>   - **Fix now:** a person using the app loses data, money, access or privacy; the main job
>     gives a wrong answer; a secret is exposed; the app no longer starts.
>   - **Fix before merge:** a bug in a less-used path; a fake or missing test over risky
>     behaviour; an unused new dependency; a real slowdown.
>   - **Note for later:** code that could be cut, small speed-ups, wording.
> - Each finding: a short title; where (`path:line`); what goes wrong for the person using the
>   app (the concrete case); the smallest fix (prefer deleting code); and the cost of skipping it.
> - Last: what you could not check, and why.
