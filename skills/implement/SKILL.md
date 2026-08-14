---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
---

Implement the work described by the user in the PRD or issues.

Before the first edit, inspect `git status` and establish the final review boundary:

- **Clean checkout:** capture the current `HEAD`. The final review covers the complete diff created by this task.
- **Dirty checkout:** stop and ask whether the existing changes belong to this implementation.
  - If they belong, ask the user to confirm the commit before those changes as the fixed point. The final review covers the complete accumulated diff.
  - If they are unrelated and the user wants a task-only review, ask them to checkpoint or commit the existing work first. Do not pretend a commit-only fixed point can separate overlapping uncommitted work reliably.

Do not edit until the user has selected the review boundary.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

After validation, run `/code-review` with the confirmed fixed point and review boundary so the completed diff goes through `reviewer`.

Address every actionable finding and rerun the relevant checks. When corrections need verification, continue the same reviewer session with the findings and resulting changes; do not start the full review again.

Report the work as tested, reviewed, and ready for the user to commit. Do not commit it yourself.
