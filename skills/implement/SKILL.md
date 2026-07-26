---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
---

Implement the work described by the user in the PRD or issues.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Address every actionable finding, rerun the relevant checks, and repeat /code-review. Continue until the final diff has no actionable findings and all required checks pass.

Report the work as tested, reviewed, and ready for the user to commit. Do not commit it yourself.
