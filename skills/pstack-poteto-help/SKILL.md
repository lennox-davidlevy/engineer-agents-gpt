---
name: pstack-poteto-help
description: Guides users through pstack setup, @pstack-poteto-mode, and picking the skill, playbook, or principle for a task. Type @pstack-poteto-help with a question.
---

# Poteto help

Answer the user's question about pstack and cite the local file that owns the
answer. A help question does not authorize implementation. Read the relevant
skill through its `pstack-<name>` ID before recommending its workflow.

## Installation and loading

This repository is cloned as the consuming project's `.opencode/` directory.
Select the `poteto` primary agent. Its skills are normal OpenCode skills under
`skills/pstack-*/`, with complete bodies and supporting files beside them.
The skill tool loads the instructions directly. There is no vendor dependency,
wrapper generator, Cursor plugin, Custom Mode, or separate setup command.

Permissions hide and deny `pstack-*` skill calls for the other configured agents.
This is not a filesystem sandbox. Do not bypass a denial through file reads.

Poteto loads `pstack-poteto-mode` before task work. The user can also mention a
skill as `@pstack-how`, for example. Skill IDs come from directory names.
Each advertised description says when the agent should load that skill.

## Models and verification

Models inherit the session configuration unless the user chooses otherwise.
`pstack-setup-pstack` discovers available OpenCode models and records approved
project-local role choices. It does not rewrite global configuration or run
paid model probes. A same-model review is not a multi-model panel.

When the project has no scripted way to exercise real behavior, recommend
`pstack-create-verification-skill`. Browser checks use Playwright through Code
Mode. Native desktop and interactive TUI checks need an existing driver.

## Pick a skill

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`@pstack-poteto-mode`](../pstack-poteto-mode/SKILL.md) |
| Know how code works now, or where new code should live | [`@pstack-how`](../pstack-how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`@pstack-why`](../pstack-why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`@pstack-teach`](../pstack-teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`@pstack-recall`](../pstack-recall/SKILL.md) |
| Know what a small diff could break outside itself | [`@pstack-blast-radius`](../pstack-blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`@pstack-architect`](../pstack-architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`@pstack-arena`](../pstack-arena/SKILL.md) |
| Run parallel read-only checks over slices | [`@pstack-swarm`](../pstack-swarm/SKILL.md) |
| Have independent reviewers challenge a diff | [`@pstack-interrogate`](../pstack-interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`@pstack-tdd`](../pstack-tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`@pstack-typescript-best-practices`](../pstack-typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`@pstack-no-comments`](../pstack-no-comments/SKILL.md) |
| Clean AI tells out of prose | [`@pstack-unslop`](../pstack-unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`@pstack-technical-writing`](../pstack-technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`@pstack-bro`](../pstack-bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`@pstack-create-verification-skill`](../pstack-create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`@pstack-maintain-verification-skill`](../pstack-maintain-verification-skill/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`@pstack-benchmark-checklist`](../pstack-benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`@pstack-figure-it-out`](../pstack-figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`@pstack-show-me-your-work`](../pstack-show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`@pstack-setup-pstack`](../pstack-setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`@pstack-automate-me`](../pstack-automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`@pstack-reflect`](../pstack-reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`@pstack-correct`](../pstack-correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`@pstack-make-bot-ui`](../pstack-make-bot-ui/SKILL.md) |
| Find their way around pstack | `@pstack-poteto-help` |


Principles are the `pstack-principle-*` skills. Playbooks are supporting files
under `pstack-poteto-mode/playbooks/`, not separately registered skills.
Read that skill's playbook index for the task-to-playbook mapping.

## Execution limits

Poteto performs implementation directly. Other agents provide read-only
exploration, research, and review. Local worktrees do not provide cloud or
credential isolation. Bounded runs end with the active session; there is no
overnight scheduler. The automation UI skill requires an external webhook
service that this setup does not provide.

Never commit or push. External writes, destructive actions, production access,
and material scope expansion need specific confirmation.

## Troubleshooting

- Missing skill. Check its path-derived ID, description, and skill permissions.
- Wrong skill body. Check for another installation overriding the same ID.
- Model choice ignored. Check approval and availability of its exact provider/model ID.
- Run stopped. Check its iteration budget, authority gates, and missing prerequisites.
- Verification claimed from a build. Ask for the actual user action and result.

## Reply

Lead with the answer. Give at most one example prompt and cite the relevant
local skill or supporting file. Keep the answer scoped to the question.
