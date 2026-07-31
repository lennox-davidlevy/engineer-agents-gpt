---
name: code-review
description: Independently review changes since a fixed point for requirement fidelity, correctness, and repository standards.
---

Route the review through `reviewer`; the implementing agent must not grade its own work.

Before delegation:

1. Require a fixed point such as a commit, branch, tag, or merge-base. Ask if it is missing.
2. Confirm the fixed point resolves and the diff is non-empty.
3. Locate the originating issue, PRD, or specification. If none is found, ask the user whether there is one; proceed without it only when the user confirms there is no specification.
4. Locate repository standards such as `AGENTS.md`, `CONTRIBUTING.md`, and coding guidelines.

Give `reviewer` the fixed point, commit list, original requirement or specification, standards sources, and any validation already run. The reviewer inspects the complete diff and returns only actionable, change-introduced findings with file-and-line evidence.

Report the findings without weakening or silently discarding them. If the user confirmed there is no specification, say so; if there are no findings, report `No findings`.
