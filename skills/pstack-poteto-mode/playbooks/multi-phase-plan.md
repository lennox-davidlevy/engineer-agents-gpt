### Multi-phase or multi-PR plan

The deliverable is a plan, not implementation.

1. If the change has an obvious one-step approach, say a formal plan adds no value and give the concrete next step.
2. Ground the scope with `pstack-how` and existing repository conventions. Use read-only delegates for independent discovery. Do not create a prototype or edit product code under a read-only planning request; identify experiments that need separate authorization.
3. Define the target data shape, boundaries, dependencies, risks, and observable acceptance predicates. Separate factual unknowns from product decisions.
4. Write the plan to a user-requested path or an agreed local artifact. Order units so each ends in a verifiable state. Every unit names files, build work, user-visible results, checks, evidence paths, and prerequisites.
5. Include a real user-path check for each behavioral change. Add focused tests and a performance check when relevant. When the baseline lacks the feature, record that and use an absolute acceptance budget rather than an invalid before/after ratio.
6. Identify review gates and human delivery steps. Poteto implements directly in bounded sessions. Read-only delegates can review. Do not prescribe cloud workers, automatic commits or pushes, unattended scheduling, or unavailable tools.
7. Validate each path, command, dependency, and proof claim against the actual repository. Mark unrun experiments and missing drivers as unverified. Apply `pstack-technical-writing` and `pstack-unslop`.
8. Return the plan and stop. Execution requires the user's explicit go.

Use this shape for each unit:

```markdown
## <Task>

- Depends on. <Units or none.>
- Files. <Exact paths.>
- Build. <One coherent change.>
- User result. <Observable end state.>
- Verify. <Real commands or actions and literal expected results.>
- Evidence. <Paths where results will be saved.>
- Review gate. <Required review or reason none is needed.>
- Delivery. <Human actions and separately authorized external operations.>
```

**Reply:** plan path, units and dependencies, review gates, evidence already
available, unresolved questions, and blocked prerequisites.
