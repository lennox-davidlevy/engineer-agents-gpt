### Shipping

Green checks are not independent proof. Shipping is a separately authorized
external action. Read [bounded local runs](../references/local-runs.md).

1. Identify the explicit shipping request, repository, PRs, base relationships, and exact heads. Without specific authorization, provide a readiness report only.
2. Inspect checks, review approvals, unresolved discussions, and conflicts with the available read-only forge tools. Work from the bottom of a dependency stack.
3. Obtain an independent read-only review of each relevant diff at its exact head. Poteto runs the real user-facing verification when delegates lack the driver. Use [verification](../references/verification.md) and report the loss of independent runtime verification honestly. Cloud-required checks remain blocked.
4. Record a verdict for each head with its evidence. CI green, a bot approval, or a prior agent's success report is not enough. A changed head or changed dependency invalidates affected evidence; inspect the difference and rerun the necessary checks.
5. Only the contiguous verified portion from the root is eligible. Do not arm a child before its parent lands or alter stack topology to make a gate pass. Re-read current state immediately before any separately authorized operation.
6. Never commit or push, including through merge commands or tools that would bypass that restriction. When the available shipping operation would do so, hand the eligible PRs and evidence to the human rather than execute it. Deployment and production access also need their own confirmation.
7. If the human or another authorized actor lands work, read back the resulting state and exact revisions before reporting it merged. Do not promise to watch beyond the bounded active session.

**Reply:** per-head verdicts, verified prefix, blocked gates, actual observed
shipping state, and the next human action. Do not claim a merge you did not observe.
