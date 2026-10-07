### Feature

**You own the design and implementation. Plan, review, verify.**

1. `how` over the affected subsystem.
2. `architect` for parallel design exploration.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (the **separate-before-serializing-shared-state** principle skill). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Poteto implements directly within named file boundaries and success criteria. Choose the organizing data shape before logic, per **principle-model-the-domain**. Use a state machine, table, or typed model when it removes scattered assumptions. For competing shapes, use **arena** with read-only design proposals and primary-owned implementation. Keep edits surgical, migrate affected callers, and verify each. Obtain independent read-only review rather than delegating writes.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
6. Use **sequence-verifiable-units** to build and verify each small unit before the next. Keep changes local; never commit or push.
7. If the design is contested, `interrogate` before shipping.
8. Run **Opening a PR**.

Poteto owns code-coupled work. Fan out only independent read-only audits,
investigations, and design critiques. Rewrite the checkpoint at phase boundaries.

**Reply:** what you built, what you chose and why, the throughput checkpoint, open decisions. Tables for design alternatives.
