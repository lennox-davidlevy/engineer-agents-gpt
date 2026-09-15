---
name: diagnosing-bugs
description: Diagnose a reproducible bug or performance regression from evidence to verified fix.
---

Start from the reported consequence and build the fastest reliable feedback loop that can distinguish broken from fixed. Existing reasoning may guide where to look, but do not present a hypothesis as the cause until evidence supports it.

## Diagnose

1. **Define the symptom.** Capture expected versus actual behavior, environment, and the narrowest known trigger. Read only the code and decisions relevant to that path.
2. **Reproduce or instrument.** Prefer an existing test, focused command, request, browser action, trace replay, benchmark, or small harness. For intermittent failures, improve the reproduction rate rather than demanding perfect determinism. If the environment cannot reproduce it, request the smallest useful artifact or safe instrumentation instead of guessing.
3. **Reduce uncertainty.** Minimize the case when that materially shrinks the search space. Form one or more falsifiable hypotheses and test the cheapest discriminating prediction first. Add targeted instrumentation; tag temporary probes so they can be removed.
4. **Fix the owning layer.** Add a regression test before the fix when a stable interface can express the real failure. If no such interface exists, say so rather than adding a misleading test. Make the smallest correction that addresses the cause, not the symptom.
5. **Verify and clean up.** Re-run the original path and affected checks, remove temporary instrumentation and throwaway artifacts, and report the evidence tying cause to fix.

For performance regressions, establish a repeatable baseline and use profiling or query plans rather than log volume. The optional human-in-the-loop template at `scripts/hitl-loop.template.sh` is a last resort when automation cannot drive the trigger.
