### Autonomous run

Define done, then work toward it within the active session.
Read [bounded local runs](../references/local-runs.md).

1. State the exit predicate, scope, and iteration budget. Default to three iterations.
2. Identify the real command or user action that proves the predicate. Capture the baseline before changing anything.
3. Each iteration tests one hypothesis with the smallest justified change. Poteto implements directly. Delegate only independent read-only investigation or review.
4. Verify each unit before the next. Retain only changes supported by evidence. Preserve unrelated work and do not discard files without authorization.
5. Log each decision and result through `pstack-show-me-your-work`. Report adjacent bugs separately rather than expanding scope.
6. Stop at the predicate, budget, permission gate, or missing prerequisite. Report VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Do not promise monitoring after the session ends.

**Reply:** exit condition, iterations run, retained changes, rejected hypotheses,
evidence, and final predicate state.
