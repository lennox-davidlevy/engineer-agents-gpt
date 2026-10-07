---
name: pstack-how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

# How

For the relevant task, read [delegation](../pstack-poteto-mode/references/delegation.md). These procedures define the OpenCode execution steps.


Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Use available read-only agents. Omit `model` unless the user explicitly chose another under the model procedure. A missing model is a blocker for that comparison, not permission to choose another paid provider.

## Step 1. Assess Complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

## Step 2a. Explore (complex questions only)

Decompose the question into 2 to 4 exploration angles, each a distinct slice of the subsystem. Spawn all explorers in a single message:

- `agent`: `explore`
- Respect the selected agent's read-only permissions.

Read `references/explorer-prompt.md` in the primary session, then give each explorer bounded task-specific questions for its angle. Then go to Step 3.

## Step 2b. Direct Explain (simple questions)

For a narrow question, explain directly. If an independent trace would add evidence, use one read-only explorer:

- `agent`: `explore`
- Respect the selected agent's read-only permissions.

Read `references/explainer-prompt.md` for the output contract. If delegating, translate it into task-specific questions rather than handing over a restricted skill file. Go to Step 4.

## Step 3. Synthesize (complex questions only)

Once all explorers return, check their citations and synthesize in the primary
session using `references/explainer-prompt.md`. Do not launch a second agent just
to restate findings. Report any unverified paths.

## Step 4. Present

Present the explainer's output to the user. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output Format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
