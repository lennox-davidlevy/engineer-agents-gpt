---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
---

Implement the work described by the user in the PRD or issues.

Before the first edit, capture the current `HEAD` as the fixed point for the final review.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

After validation, run `/code-review` from the captured fixed point so the completed diff goes through `reviewer`.

Address every actionable finding and rerun the relevant checks. Repeat review only when the corrections materially changed the implementation.

Report the work as tested, reviewed, and ready for the user to commit. Do not commit it yourself.
