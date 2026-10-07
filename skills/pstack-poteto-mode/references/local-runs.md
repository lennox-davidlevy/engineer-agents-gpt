# Bounded local runs, pause, and eval

Use this procedure for autonomous-run, orchestrate, autopilot, session pickup,
pause-safely, eval, and shipping. Apply engineering checks within the current
scope and the bounds below. There is no unattended scheduler.

## Run contract

Before work, state the checkable exit condition, scope, and iteration budget.
Use three iterations when the user has not supplied a budget. An iteration is
one hypothesis, one bounded change, and its verification. Each shell check gets
a finite timeout. This is a workflow budget, not an enforceable billing cap.

Run each iteration in the current session. Start a background shell task only
for an owned long-running check, and consume its completion notification rather
than polling. A returned background ID means started, not successful. Never
launch `nohup`, cron, a service, or recursive OpenCode sessions to simulate a
missing wake mechanism. Stop at the budget, an unmet permission gate, a missing
prerequisite, or the exit condition. Report VERIFIED, NOT VERIFIED, or
INCONCLUSIVE with evidence. A plateau does not authorize infinite retries.

Use `pstack-show-me-your-work` for the decision trail. Its bundled `log.sh`
helper works locally after inspection. Keep the log and evidence under an
agreed local task directory such as `/tmp/opencode/<task>/`. Use the history
port for a transcript audit. Do not auto-commit, discard unrelated changes,
open PRs, or expand to adjacent bugs. List out-of-scope findings separately.

## Pause and resume

Finish an atomic step and start no new work. If an owned background task or
delegate is still running, stop it only through an available supported control
or record its ID and actual status. Do not fabricate a cancel tool. Leave
uncommitted edits intact; never create the upstream `wip:` commit.

Write a checkpoint with the task, exact directory and branch, changed files,
checks and evidence paths, active process/session IDs, blockers, and next action.
Distinguish scratch evidence from durable project files. Do not claim a file
under `/tmp` survives reboot. On pickup, use the history port and recheck the
checkout and process state before acting. A checkpoint transfers context, not
authorization. Current user instructions remain controlling.

## Local eval

Keep one explicit question and fixed input. Run baseline and candidate in fresh
local contexts, with the same selected model and task budget unless model choice
is the variable the user asked to test. Use read-only delegates for read-only
tasks. Poteto owns write tasks; do not bypass the primary-only restriction by
spawning another CLI instance for implementation. Use separate scratch copies
for candidate artifacts when needed. Ask reviewer to compare anonymized outputs
against the rubric, and disclose any loss of blinding or independent execution.

Count actual tool results and observed behavior, not only final self-reports.
If only one candidate or one judge ran, report that. A local comparison is not
a cloud-isolation test, and a smoke check is not a quality benchmark.

## PR status and shipping handoff

Use existing authenticated `gh` read-only commands for an explicitly named PR
when available. Limit status checks to the agreed budget; do not start the
upstream Bun watcher or orchestration daemon automatically. If `gh` or its auth
is absent, report that prerequisite instead of installing it. Verification may
finish with a local handoff. Merging, deployment, team messages, ticket updates,
and PR creation each need specific authorization. Commit and push stay forbidden.

Cloud-required shipping gates and unattended webhook workflows remain blocked.
Do not relabel a local worker as cloud verification to make the playbook pass.
