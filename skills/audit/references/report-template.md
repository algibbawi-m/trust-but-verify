# Report template

Write every section. Plain words, short sentences. Never a secret's value, never a real person's
data: file, line and kind only. Each finding says how it was confirmed.

```markdown
# Audit: <app name> — <YYYY-MM-DD>

**Verdict:** <one sentence: "Safe to use and build on." / "Usable, but fix 1 and 2 before
anyone else uses it." / "Not safe to use until 1–3 are fixed.">

**Scope:** <what was read>. **Not read:** <areas or files no reviewer read, or "none">.
<If needed: "Not a fresh review: <reason>.">

## 1. What this app is

- **For:** <who uses it, to do what>
- **Run it:** `<command>` — <worked / failed: one line / not run: why>
- **Checks:** <lint> · <tests: n passed, n failed> · <build> — or "no tests here"
- **Data:** <where it is stored; what comes in from outside; sign-in; payments; outside services>
- **Secrets:** <how the app gets them; `.gitignore` covers them: yes / no>
- **Dependencies:** <n> for running, <n> for building and testing
- **Load assumed:** <one person / a team / the public>

| Area | Files | Lines | High risk? | Reviewer |
|---|---|---|---|---|
| <name> | <n> | <n> | <sign-in / money / personal data / writes, or no> | <1> |

## 2. Findings

### Fix now

1. **<What goes wrong, in a few words>** — `path:line`
   - **What goes wrong:** <the concrete case, as the person using the app meets it>
   - **Fix:** <the smallest fix; prefer deleting code>
   - **If we skip it:** <the cost>
   - **Confirmed by:** <reading the code / a whole-tree search / a break run in a copy / the check
     output / the secret scan>

### Fix before you build more

2. ...

### Note for later

3. ...

## 3. What could be cut

| What | Where | Why it can go (the rung) | Saves |
|---|---|---|---|
| <thing> | `path` | <not needed / already in the project at `path` / the platform does it / <package> does it / bigger than needed> | <~n lines, or 1 dependency> |

Total: about <n> lines and <n> dependencies.

## 4. Checks I ran

- `<command>` → <one result line>

## 5. Dropped findings

- <what a reviewer said> — dropped: <what the code shows>

## 6. Not checked

- <what, and why>

## Next steps

1. <the first fix, as its own task>
2. ...
```
