### Worktree and simulator cleanup

Audit first. Deletion always needs specific confirmation.

1. Record disk usage and `git worktree list --porcelain`. Take worktree paths from git rather than constructing them from a naming convention.
2. For each candidate, inspect its branch, working-tree status, untracked files, and reachability of its commits from the intended retained branch. Read available PR state when relevant. An old timestamp or merged PR alone does not prove there is no unique work.
3. Use the scoped [history procedure](../references/history.md) only when the user authorizes session-history inspection for these directories. Missing history is unknown, not permission to delete.
4. Classify candidates as keep, inspect, or eligible for removal, with the concrete evidence and estimated reclaimable space. Preserve dirty, active, or uniquely committed work.
5. Present the exact paths and actions for confirmation. Do not force-remove a worktree, discard files, or delete a branch as an incidental cleanup step. Use supported git worktree commands only for the specifically approved candidates.
6. For simulators and caches, first establish the platform and ownership. Inspect available simulator tooling rather than guessing commands. Include exact targets in a separate confirmation. Do not clear application databases, credentials, or unrelated caches.
7. Read back the worktree list and disk state after authorized cleanup. Report what was actually removed and what remains unresolved.

**Reply:** candidate table, confirmed actions, observed results, and preserved work.
