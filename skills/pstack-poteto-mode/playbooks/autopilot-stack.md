### Autopilot-stack

Prepare dependent changes in reviewable order without landing them.
Use [bounded local runs](../references/local-runs.md).

1. Record the requested dependency chain, each unit's scope, and its acceptance predicate. Do not infer authorization to create branches, PRs, commits, pushes, or merges from the word "autopilot".
2. Poteto implements each unit directly after its prerequisites are verified. Read-only delegates may explore and review. Preserve the existing worktree and unrelated changes.
3. Verify every unit on the real artifact before proceeding. Record evidence and decisions through `pstack-show-me-your-work`. A later change that invalidates an earlier result requires a recheck.
4. Obtain independent review of the combined result and dependency boundaries. Fix accepted in-scope findings and rerun affected checks. Do not claim cloud isolation or multi-model diversity that did not occur.
5. Return the local diff with the proposed unit ordering and dependency graph. Never commit or push. The human controls commit and PR creation. A separately requested PR operation follows [opening a PR](opening-a-pr.md).
6. Stop at the iteration budget or any unmet gate. Use [pause safely](pause-safely.md) if work remains.

Choose this playbook for dependent units intended for ordered human delivery.
Choose [autopilot-full](autopilot-full.md) for independent queue items.

**Reply:** verified units in order, dependencies, review findings, evidence,
blocked work, and human delivery steps. Do not call local edits STACK-READY PRs.
