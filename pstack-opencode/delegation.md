# Local delegation

Poteto is primary-only in this installation. Replace upstream Task,
poteto-agent, cloud workers, and Comment Sicko spawning with the following
procedure. Do not change agent modes or permissions to make a playbook run.

1. Read the skill and its rubric in the primary poteto session. Decide whether
   delegation would add independent evidence or merely repeat your own work.
2. Discover the available `subagent` targets from the tool catalog. Prefer
   `explore` for local read-only mapping, `researcher` for public-source research,
   and `reviewer` for independent review. Inspect their known capability limits.
   Do not assign shell/API work to a delegate whose shell permission is denied.
3. Give a bounded task, user intent, relevant code/artifact paths, and concrete
   acceptance criteria. Do not tell delegates to load `pstack-*`, read the
   pstack skill files, or recover the workflow from the vendor directory.
   Their skill denial remains intact. Translate the applicable rubric into
   task-specific review questions yourself. Do not paste the full skill to
   circumvent the restriction.
4. Omit `model` unless the user selected another one under the models port.
   Use `background: true` only for independent work with a clear owner. Wait
   for the tool's completion notification; do not poll child-session status.
5. Inspect the returned evidence. Poteto applies accepted implementation changes
   itself and runs the checks. Delegation does not establish correctness.

## Arena and architecture

Read-only delegates may propose distinct designs or critique artifacts. Poteto
implements candidates sequentially in separate scratch directories when needed,
then runs the same checks against each. Preserve base-selection and synthesis
reasoning. Report sequential implementation honestly; it is not a concurrent
code race. Do not invoke `opencode run`, spawn a hidden general-purpose worker,
or create another agent to bypass the primary-only restriction.

## Swarm and review

Split read-only coverage across the available delegates. For implementation
sweeps, keep one writer, poteto, and distribute only investigation or review.
For `no-comments`, poteto reads the Comment Sicko rubric and asks reviewer
specific questions about non-obvious rationale, obsolete comments, and claims
that should be enforced structurally. Reviewer returns findings, never edits.

Use fresh child sessions for independent judgments. If no permitted delegate
can perform a required check, do it directly and mark the independence gate
unmet. A local worktree does not isolate credentials, processes, or machines.
Cloud-required verification remains blocked, not silently weakened.
