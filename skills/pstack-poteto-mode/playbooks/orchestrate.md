### Orchestrate

Coordinate a multi-unit program locally. This installation has one writer,
poteto, and read-only delegates. It has no cloud workers or durable scheduler.
Read [bounded local runs](../references/local-runs.md) and
[delegation](../references/delegation.md).

1. State the program goal, definition of done, scope, dependency graph, and active-session budget. A multi-day request needs explicit checkpoints rather than a promise of unattended persistence.
2. Write the ordered units and their acceptance predicates in an agreed project-local plan. Each unit names its files, prerequisites, real verification command or action, and evidence path. Keep a decision trail through `pstack-show-me-your-work`.
3. Put blocking discovery and shared-state decisions first. Poteto implements one coherent unit at a time. Fan out only independent read-only source mapping, research, or review, with task-specific briefs and no restricted skill files.
4. Each brief names the scope, artifact revision, evidence criteria, and expected report. Delegates return PASS, ISSUES, or BLOCKED with citations. An unavailable permission or tool stays blocked.
5. Verify each unit on the real artifact before starting its dependents. Keep unit state as planned, active, verified, or blocked, with evidence and outstanding decisions. A subagent's completion is not verification.
6. Review each completed unit independently. Poteto applies accepted in-scope fixes and reruns affected checks. Do not create recursive coordinators or another CLI implementation worker.
7. At each unit boundary, reconcile the plan against files and actual results. Record dropped assumptions and scope changes. Ask for authorization before expanding scope, external writes, destructive actions, or production access. Never commit or push.
8. Stop at the budget, an unmet gate, or completion. Follow [pause safely](pause-safely.md) for remaining work. On resume, use [session pickup](session-pickup.md) and recheck current state.

**Reply:** completed units with evidence, active and blocked units, current
dependencies, decision-trail path, and the next concrete action.
