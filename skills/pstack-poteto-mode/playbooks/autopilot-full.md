### Autopilot-full

Process a queue of independent changes. The cloud-owner and automatic-merge
lifecycle is unavailable in this installation. Use a bounded local run and
state this limit before beginning. Never promise automatic delivery.

1. Confirm the queue, scopes, acceptance predicates, and iteration budget under [bounded local runs](../references/local-runs.md). Keep the decision trail through `pstack-show-me-your-work`.
2. Check that queue items are independent. Use [orchestrate](orchestrate.md) when dependencies make this a program. Poteto implements directly; read-only delegates may investigate or review independent slices.
3. For each item, run the matching feature, bug-fix, or refactoring playbook. Verify real behavior, inspect the diff, and obtain an independent review. Keep results tied to exact artifact states.
4. Fix accepted in-scope findings, rerun affected checks, and record the verdict. Unavailable cloud-isolation gates remain blocked rather than silently weakened.
5. Hand back verified local changes. Never commit or push. Existing PR status uses [babysit](babysit.md). An explicit shipping request uses [shipping](shipping.md) and its authority gates.
6. Stop on the budget or missing prerequisite. Save a checkpoint instead of creating cron jobs, hidden sessions, or recurring monitor processes.

**Reply:** queue results, evidence, blocked lifecycle steps, decision trail,
and the next human action.
