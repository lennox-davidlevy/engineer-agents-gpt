---
name: pstack-reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

For the relevant task, read [history](../pstack-poteto-mode/references/history.md), [delegation](../pstack-poteto-mode/references/delegation.md). These procedures define the OpenCode execution steps.


Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "@pstack-reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

Use the visible conversation or a scoped OpenCode session export under the
history procedure linked above. If the current session ID or export is
unavailable, give a concise evidence-backed digest and report that limit.

### 2. Spawn three reviewers in parallel

Use fresh read-only `reviewer` sessions for judgment, tooling, and divergent
perspectives. Omit `model` unless the user selected another through the model
procedure. Inspect these templates in the primary session:

- `references/judgment-reviewer.md`
- `references/tooling-reviewer.md`
- `references/divergent-reviewer.md`

Translate the lenses into bounded questions about the supplied transcript or
digest. Do not give delegates restricted skill paths or ask them to edit.
Obtain external evidence in the primary or through a permitted researcher.

### 3. Synthesize

Read `references/synthesizer.md` and combine the findings in the primary session.
Verify citations. Return Accepted, Rejected, and Backlog lists with concrete
target files and reasons. Do not describe three lenses as three models.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Keep backlog items local. Filing them in an external tracker requires specific authorization.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the available `skill-creator` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
