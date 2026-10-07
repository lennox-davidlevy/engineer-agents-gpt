# Engineer Agents for OpenCode

Work in progress. I've found less is more with modern frontier models: many skills I used to rely on are no longer beneficial or efficient. This is the setup I use daily.

A typical session:

1. Start from a template repository with the file structure I like and the dependencies I expect to use.
2. Build the foundation, by hand or with the harness.
3. Design new features with the `design` primary agent.
4. Hand off to `engineer` (the heavier model) for implementation.
5. Subagents handle research and exploration; Context7 MCP covers library docs, playwright for UIs.

- **`design` (Sol - Primary)** turns uncertain ideas into concise decisions and implementation briefs.
- **`engineer` (Astra - Primary)** owns implementation, debugging, refactoring, validation, and delivery.
- **`reviewer` (Astra - Subagent)** independently reviews a bounded change.
- **`explore` (Luna - Subagent)** maps repositories read-only.
- **`researcher` (Terra - Subagent)** retrieves external primary-source evidence read-only.

Skills add narrow workflows on demand.

### Optional poteto agent

Select `poteto` to use Lauren Tan's pstack workflows. This is one additional
agent; it does not replace the default.
Its 51 OpenCode-native skills live in `skills/pstack-*/`. Each `SKILL.md`
contains the actual instructions, with references and scripts alongside it.
OpenCode loads the body directly through the skill tool. There are no pointer
wrappers or generation step. Edit these files directly.

Permissions hide and deny `pstack-*` skills for the other configured agents.
This restricts skill discovery and calls, not filesystem reads.
The [poteto agent](agents/poteto.md) defines common tool and authority rules.
Specialized procedures for history, model roles, delegation, verification, and
bounded runs live under [poteto-mode references](skills/pstack-poteto-mode/references/).
No Cursor checkout, cloud worker service, or unattended scheduler is required
or provided. The skills derive from Lauren Tan's pstack and retain its
[MIT license](skills/PSTACK-LICENSE). The starting source was
[pstack 0.15.13](https://github.com/cursor/plugins/tree/e5a8186d7b43be8d6ac4452440fbead5f1a51c70/pstack).
These are maintained OpenCode adaptations, not a synced copy of that source.

The old `vendor/pstack/` snapshot is retained but unused. Removing it was blocked
by the active agent's snapshot-protection rule during this migration.

Validate the skill layout with `python3 scripts/check_pstack_skills.py`.
From a fresh project containing this repo as `.opencode`, run
`python3 .opencode/scripts/check_pstack_access.py` to check native registration
and poteto-only access using the installed OpenCode V2 service. This creates
local validation sessions but makes no model requests.

## Install

Clone the repository as a project's `.opencode` directory:

```sh
git clone git@github.com:lennox-davidlevy/opencode-engineer-agents.git .opencode
```

The configuration targets OpenCode V2. Confirm the installed models include:

```sh
opencode2 models
```

And choose the models that work for you.

## Authority and safety

- Ordinary `git commit` and `git push` commands are denied. Personal preference, I prefer to control the git worflow, even if it is a bit less efficient.
- Destructive commands (file deletion, git reset/clean, `sudo`, Docker pruning etc) asks for approval.
- `engineer` performs production work. Subagents are limited to exploration, research, and independent review.
- Handoffs carry context.

## Code Mode and connected tools

| Capability | engineer | design | researcher | explore | reviewer |
|---|---|---|---|---|---|
| Code Mode (`execute`) | allow | allow | allow | deny | allow |
| Playwright MCP (headless) | allow | allow | deny | deny | deny |
| Desktop browser | deny | deny | deny | deny | deny |
| Web search/fetch | allow | allow | allow | deny | deny |
| Context7 | allow | deny | allow | deny | deny |


Built-in `build` and `plan` are disabled because `engineer` and `design` replace them. Snapshots and compaction retain runtime defaults; formatting, watcher exclusions, and project-specific tools belong to consuming projects.

## Skills


Useful skills, some from [Matt Pocock](https://github.com/mattpocock/skills), [Kit Langton](https://github.com/kitlangton/skills), myself, twitter.  All of these I use regularly and only where I see good results relatively consistently:

- `code-review` for parallel Spec and Standards review in fresh contexts
- `diagnosing-bugs` for evidence-led debugging
- `effect` for Effect v4 TypeScript implementation patterns and reference guides
- `research` for primary-source investigation
- `handoff` for compact cross-session context
- `prototype` for disposable design evidence
- `query-okf` and `curate-okf` for the Open Knowledge Format
- `test-audit` for test authoring gates, evidence-led deletion, and full subsystem test-pruning campaigns
