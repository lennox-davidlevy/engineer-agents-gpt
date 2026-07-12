---
name: simplify
description: Grind a piece of code down until the same behaviour survives in half the code — repeated shrinking passes under a test harness.
disable-model-invocation: true
---

# Simplify

Generated code is reliably overbuilt: speculative abstraction, defensive branches for impossible states, indirection with one caller. The job here is to **grind** it — repeated shrinking passes that preserve behaviour while the code gets smaller.

This is expensive attention. It's only worth spending in **critical areas** — hot paths, public interfaces, code humans will re-read for years. If the user points you at something peripheral, say so before starting.

Use the `/codebase-design` vocabulary (**module**, **interface**, **depth**, the **deletion test**) throughout.

## Process

### 1. Pin the target

The user names the files, module, or diff to grind. If they didn't, ask — never pick your own target. Note the starting line count.

### 2. Rig the harness

Grinding without a harness is just rewriting. Establish, in order of preference:

1. Existing tests that exercise the target **through its interface**.
2. If none exist, offer to write characterization tests first (via `/tdd`) — tests that pin current behaviour, not desired behaviour.
3. If the user declines tests, fall back to typecheck + a manual verification step they agree to run.

The harness must be green before the first pass. Record the exact commands.

### 3. Grind

Run passes. Each pass: hunt one round of targets, apply the cuts, run the harness, stay green. If a cut breaks the harness, revert the cut — don't adjust the tests to fit. Hunt for:

- **Speculative generality** — abstraction, parameters, or hooks serving needs that don't exist. Apply the deletion test; if complexity vanishes rather than reappearing at callers, delete it.
- **Single-use indirection** — a function, class, or layer with exactly one caller that adds no name worth keeping. Inline it.
- **Defensive code for impossible states** — validation and fallbacks for inputs the types or call sites already rule out. Delete; let the types carry it.
- **Duplicated shapes** — the same logic written twice with different variable names. Collapse to one.
- **Config that never varies** — options, flags, and injected dependencies with a single value across the codebase. Hard-code them.
- **Cleverness** — code that is short but opaque. Rewrite plain. Shrinking measured in *concepts a reader must hold*, not characters.

After each pass, report: lines before → after, what was cut, harness status.

### 4. Stop

Stop when a full pass yields no cuts — that's the completion criterion, not a target line count. Report final numbers against the step-1 baseline, and anything you chose *not* to cut with a one-line reason each.

## Guardrails

- **The interface holds** unless the user explicitly approves changing it. Shrinking the implementation is free; shrinking the interface is a design decision.
- **Not code golf.** Fewer lines is the usual outcome, not the goal. When brevity and readability conflict, readability wins.
- **No feature loss disguised as simplification.** If a branch looks dead but you can't prove it, ask before cutting.
