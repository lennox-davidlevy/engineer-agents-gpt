---
name: code-review
description: Independently review changes since a fixed point for requirement fidelity, correctness, and repository standards.
---

Route the review through `reviewer`; the implementing agent must not grade its own work.

Before delegation:

1. Require a fixed point such as a commit, branch, tag, or merge-base. Ask if it is missing.
2. Require an explicit review boundary:
   - **Task review** — only the complete change made from a clean starting point.
   - **Integration review** — the complete accumulated diff, including earlier uncommitted work.
   Do not infer the boundary from `HEAD` when the checkout is dirty.
3. Confirm the fixed point resolves and the intended diff is non-empty.
4. Locate the originating issue, PRD, or specification. If none is found, ask the user whether there is one; proceed without it only when the user confirms there is no specification.
5. Locate repository standards such as `AGENTS.md`, `CONTRIBUTING.md`, and coding guidelines.

Give `reviewer` the fixed point, explicit review boundary, commit list, original requirement or specification, standards sources, and validation already run. Findings must stay inside the selected boundary. The reviewer may inspect surrounding or external code when needed as evidence, but must not report unrelated changes.

If findings are corrected, continue the same reviewer session and ask it to verify those corrections. Start a new full review only when the review boundary itself materially changed.

Report the findings without weakening or silently discarding them. If the user confirmed there is no specification, say so; if there are no findings, report `No findings`.
