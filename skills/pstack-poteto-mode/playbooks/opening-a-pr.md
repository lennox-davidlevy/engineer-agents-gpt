### Opening a PR or local handoff

Every implementation playbook ends with a local handoff. A read-only question
ends with its answer. Neither automatically creates a PR.

1. Inspect the actual diff and run the repository's focused checks. Preserve
   unrelated changes and existing worktrees. Never reset or discard them as a
   cleanup shortcut.
2. Review code quality directly. Use `pstack-no-comments` for comment review
   within the authorized edit scope and an independent read-only reviewer for
   the final diff. Poteto applies accepted fixes and reruns affected checks.
3. Never commit or push. Give the human the verified local diff and suggested
   unit ordering. Do not invoke a helper or external tool that commits or pushes.
4. Create or update a PR only with specific authorization, and only from an
   already published branch. If publishing would be required, hand that step
   to the human. Discover available forge tools and use their documented API.
5. Write any requested PR title and description using `pstack-technical-writing`
   and `pstack-unslop`. Do not invent a PR URL or status.

**Titles.** Use Conventional Commits in the form `type(scope): subject`. Use `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf` as the type. Use the changed area, such as `pstack` or `poteto-mode`, as the scope. Keep the subject short and imperative. Name a real symbol when one carries the change. For example, `fix(pstack): retarget opening-a-pr babysit trigger`. Do not add a trailing period.

**Descriptions.** The PR body is a briefing, not the lab notebook. A reviewer who has the diff should learn why the change exists, what it leaves out, what it could break, and how you proved it works, in under a minute. Write short, simple sentences with few identifiers. Do not write walls of text. The squash commit body is the PR body. If the body would make the squash commit longer than about 40 lines, cut the body.

Put each section under a `##` heading, not a bold lead-in, so the sections stand apart. Use these sections in order. Drop a section when it has nothing to say.

- `## Why` gives the problem and the approach in one to three short sentences. Do not list SHAs or rebase genealogy. Do not add a "based on main" preamble.
- `## What changed` has one to three short bullets. Name a real symbol or path only when it carries the change. Name both sides of a rename or retarget.
- `## Scope` always names what the PR covers and what it deliberately leaves out, for example a related follow-up or a known gap. Use one to three short items. Do not list symbols or paths, and do not write a file-by-file essay.
- `## Tradeoffs` names only rejected alternatives that a reviewer would otherwise ask about. Skip this section when there was no real choice.
- `## Blast Radius` gives one or two sentences on who or what the change touches and why that is safe or risky. If main is red, state the cost of leaving it red.
- `## Verification` has one to three bullets. Each bullet names a real run path and its outcome. For a performance change, report one primary number with its unit in `before → after` form. Link the arena or swarm directory for the remaining evidence. Do not include sample-size methodology, swarm recitals, or metric tables.

After these sections, attach videos or screenshots when they prove a claim. Do not paste full SHAs, swarm or arena lane recitals, lever-correction essays, file-by-file checklists, or "CLEAN" verdicts. Put these details in a linked artifact. A commit body does not restate its subject.

**Read back external state.** After an authorized PR operation, read the
actual PR and report its observed URL and status. Do not claim readiness from
a local build alone. Opening a PR does not start babysitting or authorize merge.

**Reply:** local changes, checks and evidence, open risks, and human delivery
steps. Include a PR link only if one actually exists.
