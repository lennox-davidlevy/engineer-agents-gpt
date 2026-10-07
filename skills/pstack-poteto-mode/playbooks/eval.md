### Eval

**You own the experiment design. Plan, blind, run, synthesize.**

**Non-negotiables for blinding:**

- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in any directory, file, or prompt the candidate sees.
- The candidate prompt looks like an organic user request. State the goal, not the meta.
- No chain-eliciting cues. Don't ask the candidate to list which skills, principles, or files they applied. Ask for design notes generally and grade chain-following from code shape, not self-report.
- Sanitize directory and slug names. Use project-shaped names a user might pick.
- Don't tell the candidate other candidates exist.
- The judge can know it's judging but sees outputs by sanitized label only, never by model name.
- Comparing two variants: one judge scores both sets in a single pass on one scale, blind to which set each came from.

**Steps:**

1. **Frame.** State what variant is under test and what behavior counts as success. Write the rubric (3-6 concrete criteria) for the judge only. Hold it back from candidates.
2. **Set up sanitized environments.** Per-candidate working dir with the variant in place. Plant any context an organic task would have: a project skeleton, the skills the candidate would naturally read.
3. **Author one organic prompt.** What a user would type. No leakage of what's being measured.
4. **Run candidates within available permissions.** Read-only tasks may use fresh permitted delegates. Poteto performs implementation candidates sequentially in isolated scratch copies. Never give delegates restricted pstack skills or start another CLI worker to bypass the primary-only rule. Report losses of independence or blinding. Follow [bounded local eval](../references/local-runs.md).
5. **Ask a fresh read-only judge** to compare artifact paths by sanitized label against the rubric. Omit `model` unless the user selected another. Do not claim cross-model review without it.
6. **Verify from actual tool evidence.** Use this conversation and named exports obtained through the [history procedure](../references/history.md). Inspect what was actually loaded or run. If an export is unavailable, state that the chain audit is incomplete. Do not grade from candidate self-reports.
7. **Read every candidate output yourself** end to end. Compare to the judge's verdict. Disagreement means a model is biased or the rubric is ambiguous. Synthesize.

**Reply:** variant under test, rubric, per-candidate notes, judge's verdict, your synthesis, and a recommendation for whether to promote the variant.
