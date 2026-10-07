### Bug fix

**You own this task. Plan, implement, review, verify.** Delegate only read-only investigation and review.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself on the matching surface using the verification procedure in the Non-negotiables, even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Form hypotheses and rule them out with runtime evidence. Seed them with `how` over the subsystem and `why` for regression history. Use instrumentation when state is unclear. For a stubborn hunt, follow [bounded local runs](../references/local-runs.md), not an unattended loop. Confirm the surviving mechanism before planning the fix.
3. Plan the fix. If it crosses a function boundary, use `architect` first. Poteto implements the smallest in-scope root-cause repair directly.
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Capture the failing repro before the fix, then rerun it after. Never commit or push. See the **tdd** skill for the failing-test-first cadence when the bug has a cheap local test path. Skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical **sequence-verifiable-units** principle skill, the failing test first and the fix on top.
6. Run **Opening a PR**.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
