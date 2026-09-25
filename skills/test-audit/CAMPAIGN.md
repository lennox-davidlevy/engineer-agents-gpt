# Test-pruning campaign

Campaign mode prunes one subsystem's whole test surface in one coherent PR-sized
change: a plugin such as `extensions/telegram`, or one core area. The value bar,
retention bar, candidate evidence, and validation in [SKILL.md](SKILL.md) apply
to every lane. This file adds the order of work for a full campaign.
Each step ends on its completion criterion; do not start the next step early.
An entire redundant test layer is a valid deletion target; do not reduce a
campaign to scattered cosmetic cleanup. Optimize for confidence, not deletion
count, and stay within the authorized subsystem and edit scope.

## 1. Baseline

Record the subsystem's test and support line counts and every test file's
pass/fail state at a pinned baseline SHA, normally current `main` or the default
branch. Record any task-local changes separately; do not overwrite them to
establish a baseline. Keep baseline failures in their own list: they may be real
product bugs, not stale tests. Identify required live/QA environments without
accessing production or external services without authorization.

Done when every in-scope test file has a recorded baseline result. If an
environment is unavailable, report the blocked files; do not claim a complete
baseline or silently shrink the campaign.

## 2. Lanes and inventory

Split the surface into **lanes** along production owner boundaries, not file
prefixes. Examples include accounts, commands, context, dispatch, inbound,
outbound, persistence, transport, shared, harness, and live/QA scenarios.
Include the subsystem's cases at shared core boundaries and its QA and
live-proof harness tests.

Done when every test file and QA scenario the subsystem owns belongs to exactly
one lane.

## 3. Read-only ledger per lane

The primary gives each lane to its own read-only `explore` context. The agent
reads every assigned test in full, including parameter tables. It also reads
the production owners and their entry points, callers, history, and CI routing.
Each test declaration goes into a written **ledger** with one mark. An
`it.each` (or equivalent parameterized test) is one declaration unless its rows
need different marks; then mark each row. Include the candidate evidence
required by [SKILL.md](SKILL.md), not merely a deletion recommendation.

- `R`: retain, naming the contract and the bug it catches; a retained test that
  only moves to a better-named file stays `R` with the move noted;
- `F`: retain the contract but repair the assertion, such as a vacuous negative
  that passes when only one of several items is missing;
- `C`: consolidate, naming the owner that absorbs the assertion first: a sibling
  table case, a stronger boundary suite, or the shared owner in another package;
- `D`: delete, naming the proof that remains, or why no contract exists.

Judge a test by its assertions, not its name. A test named for retiring a
progress window may only assert that the window was not cleared.

Done when every declaration in the lane has a mark and an evidence line.

## 4. Layer plan per lane

Treat the per-test ledger as input, not as the edit list. A second read-only
pass, starting from the ledger, looks for the redundant **layer**. Several
dispatch suites may replay the same shared compositor through one mocked
preview, around stronger real-stream and HTTP-fixture suites. Name the
**keeper** suite for each contract. Prefer the real transport boundary with a
fake network over a mocked collaborator. Correct any ledger errors this pass
finds. Report the evidence and layer plan before editing.

Done when each lane plan names its retired files, its keeper per contract, the
assertions to carry into keepers, and the test-only production seams unlocked.

## 5. Cutover

Engineer edits lane by lane, including shared harnesses and support files;
there are no mutating workers. With each lane, remove the test-only production
seams it unlocks: injection parameters, getters, reset exports, and indirection
layers. Register moved suites in CI routing and test inventories. Update
shrink-only line-cap baselines where they exist. Put durable test-ownership
rules in the subsystem's `AGENTS.md`, drawn from mistakes this campaign actually
found. Do not introduce a new line-cap mechanism merely for this campaign.

Done when every lane plan is applied, its keepers have no new failures, and any
remaining failures are verified against the recorded baseline with the same
failure reason. Carry those unchanged baseline failures into Step 7; they do
not authorize weakening tests or skipping new failures.

## 6. Preservation review

Before claiming completion, the primary dispatches independent `reviewer`
contexts to compare deleted coverage against the keepers, one per boundary
group. They look for contracts that lost their only proof and new assertions
that cannot fail, such as a rejection row the production code never reaches.
Supply the fixed baseline, full task diff including relevant untracked files,
ledgers, layer plans, and validation evidence. Reviewers do not delegate or edit.

For each restored contract, Engineer makes one deliberate **mutation** of the
production owner and confirms the keeper goes red for the intended reason.
Then restore the source byte for byte and rerun the keeper. Save the exact
pre-mutation contents and preserve all existing task and user changes; do not
use a blanket Git restore/reset. Stop editing while each test run is active.

Done when every reported gap is restored or rejected with source evidence, and
every restored contract has a caught mutation and a passing restored run.
This coverage-preservation review complements the mandatory final `code-review`
in [SKILL.md](SKILL.md); it does not replace its Spec and Standards axes.

## 7. Product defects

A baseline failure that survives into a keeper is a bug report. Do not delete
or weaken it to make the campaign green. If repairing it is within the
authorized task, fix it at its owner as a separately documented change and
prove it through the real user flow, with a **control** run that removes only
the fix and shows the old behavior. Preserve and restore exact contents as in
the mutation step. Otherwise report the defect and request a scope decision.
Record unrelated product discrepancies as follow-ups instead of fixing them
in the campaign. Never create commits as part of this workflow.

Done when each repaired defect has a failing control and a passing candidate
on the same harness, and each unrepaired defect is explicitly reported.

## 8. Reconcile and hand off

Campaigns may outlive many default-branch commits. Hand off branch integration
to the user; recommend merging rather than rebasing a long, many-commit
campaign, subject to repository policy. When upstream modified a file the
campaign deleted, preserve its new contracts in the keeper rather than blindly
discarding either side. Re-evaluate whether the deletion is still justified.
Confirm every new upstream regression has a home. After integration, rerun the
whole subsystem suite and repeat authorized live proof on the integrated head.
Until then, report the tested SHA and outstanding integration proof accurately.

Expect review tooling to truncate large diffs. Split review by boundary and
read complete files rather than accepting truncated coverage. Record maintainer
decisions in the handoff or authorized PR evidence instead of weakening gates.

Hand off with the [SKILL.md](SKILL.md) report, plus:

- baseline and final test/support line counts, with production counted separately;
- lanes, retired layers, and keepers;
- preservation gaps found and their mutations;
- product defects with control and candidate proof;
- outstanding environment, scope, or integration blockers.
