# Local OpenCode ports

These instructions replace host-specific steps, not the upstream engineering
principles. The generated wrappers load them before the original skills.
They take precedence over Cursor paths, commands, model defaults, and automation
instructions. The agent's authority and permission rules still take precedence.

`ports.json` maps upstream skill IDs to the native instructions they need.
Keep this directory beside `skills/`, `agents/`, and `vendor/` when sharing the
setup. Regenerate wrappers with `python3 scripts/sync_pstack_wrappers.py` after
changing the mapping. Do not edit the snapshot under `vendor/pstack/skills/`.

| Workflow | Native implementation |
| --- | --- |
| Recall, reflection, pickup, transcript audits | [Scoped session listing and export](history.md) through the OpenCode CLI. |
| Setup and model roles | [User-selected OpenCode model IDs](models.md) in a project-local role file. |
| How, why, review, arena, swarm | [Existing local delegates](delegation.md), with poteto owning implementation. |
| UI, CLI, and generated verification skills | [Existing project checks and Playwright](verification.md). |
| Autonomous runs, pause, eval, shipping handoff | [Bounded local runs](local-runs.md), without automatic commits or remote writes. |

Use the installed V2 executable. In shell examples, `OC` means that executable.
Initialize it in every shell invocation that uses it. Variables do not persist
between tool calls. Run this prefix and the intended command in the same call:

```sh
OC="$(command -v opencode2 || command -v opencode)" || exit 1
"$OC" --version
```

Stop if neither exists or the installed version is not V2. Check the installed
command's `--help` when a flag is rejected. Do not install or upgrade anything
as a fallback. CLI/API operations must use the same server connection as the
session. If connected explicitly, use the corresponding `--server` option;
do not switch to a standalone server to sidestep a permission or connection issue.

## Still outside this port

There is no cloud worker provisioning, machine-level sandbox, unattended
scheduler, webhook receiver, or native desktop/TUI driver. `make-bot-ui` still
requires its external service. Local worktrees are not security isolation.
Do not replace missing infrastructure with `--auto`, elevated permissions,
unbounded processes, credential copying, or unsupported claims of persistence.

The command contracts were checked against OpenCode V2 documentation at
<https://opencode.ai/v2/docs/cli/commands> and the installed V2 CLI/API.
The ports are agent workflows, not a new background service.
