---
name: code-review
description: Review a branch, PR, or worktree in parallel for specification fidelity and repository standards.
---

Review one explicit change boundary through two fresh `reviewer` contexts:

- **Spec** — does the change implement the requested behavior correctly and completely?
- **Standards** — does the change follow documented repository rules and remain maintainable?

The implementing context coordinates the review but does not grade its own work.

## 1. Establish the boundary

Require a fixed point such as a commit, branch, tag, or merge-base. Confirm it resolves and determine what belongs to the review:

- **Committed branch:** compare the merge-base with `HEAD`.
- **Task worktree:** include the task's committed, staged, unstaged, and relevant untracked files.
- **Dirty shared worktree:** ask whether the review covers all accumulated changes or an identifiable subset. A three-dot diff does not include uncommitted work or separate overlapping edits.

Stop on an invalid fixed point or empty selected boundary.

## 2. Gather the two sources of truth

For **Spec**, use the user's request plus any linked issue, PRD, acceptance criteria, or supplied specification. The conversation is a valid specification; an issue tracker is optional. If no requirement source exists, say so, but still review observable correctness and regressions without inventing requirements.

For **Standards**, locate applicable `AGENTS.md`, contribution guides, coding standards, and local conventions. Repository rules override generic advice; skip formatting or checks already enforced mechanically.

Use these smells only as prompts to investigate: unclear names, duplicated policy, feature envy, data clumps, primitive obsession, repeated conditionals, shotgun surgery, divergent responsibilities, speculative generality, message chains, middle men, and inheritance that does not fit. A smell is a judgment call, not a finding by itself. Report it only with concrete evidence, practical consequence, and a justified correction; do not prescribe Fowler's stock refactoring automatically.

## 3. Review in parallel

Launch two `reviewer` assignments concurrently. Give both the fixed point, exact boundary, commit list, and validation already run.

**Spec assignment:** include the complete requirement source. Ask for missing or partial requirements, incorrect behavior, regressions, unrequested scope, and validation gaps. Require a quoted requirement when one exists.

**Standards assignment:** include the standards sources and the smell cues above. Ask for documented-rule violations and maintainability defects introduced by the change. Require the cited rule for hard violations; label heuristic concerns as judgment calls.

Both assignments report only actionable findings inside the selected boundary, with severity, exact location, evidence, practical consequence, and required correction. `No findings` is valid.

## 4. Report separately

Present the results under `## Spec` and `## Standards`. Do not rank one axis against the other. Preserve supported findings; if a reviewer claim is unsupported or duplicates the other axis exactly, say why rather than silently dropping it.

End with finding counts and the highest severity within each axis. If corrections are made, continue the same reviewer sessions to verify them; start over only when the review boundary materially changes.
