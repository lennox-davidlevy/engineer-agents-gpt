# Engineer GPT for OpenCode

This repository installs a focused engineering setup for OpenCode. The Sol-backed `forge` is the default daily engineering agent: it inspects freely, carries explicit implementation requests through local edits and validation, and pauses for consequential side effects. `design` develops project ideas and implementation-ready plans; `engineer` remains the approval-first implementation alternative. These agents delegate only bounded read-only exploration, external research, and independent review. `all-purpose` is a non-delegating conversational alternative.

## Install

OpenCode must recognize the repository root as a configuration directory. Cloning it into an arbitrary project directory is not enough.

The following installation modes were verified with OpenCode 1.18.1.

### Install in project
Clone anywhere and point OpenCode at the clone:

```sh
git clone git@github.com:lennox-davidlevy/engineer-agents-gpt.git .opencode
```

## What approval means

- `forge` reads and inspects without prompting. An explicit implementation request authorizes workspace edits and ordinary local validation.
- Advice, review, diagnosis, and planning stay read-only unless the user separately requests implementation.
- Read-only subagents (`explore`, `researcher`, and `reviewer`) launch without approval. Research artifacts still require edit approval.
- Production implementation, edits, and validation remain in the main `forge` context. A session handoff may transfer approved design decisions, but it does not authorize implementation.
- Commits, pushes, external writes, destructive actions, and material scope expansion require specific approval.
- `engineer` remains available when approval before edits and general shell commands is preferred.

These permissions are guardrails, not a sandbox.

## Agents and models

The setup expects an OpenCode provider that exposes the configured OpenAI model IDs:

- Sol for design, engineering, and independent review
- Terra for external research
- Luna for fast repository exploration

Model binding and provider-option propagation could not be validated without loading the machine's real provider configuration, which was intentionally kept out of the isolated tests. For the same reason, the planned lightweight system-model override remains unset rather than assuming `openai/gpt-5.6-luna-fast` is available. Verify the configured model IDs with `opencode models` in each installed environment.

`forge` is the default primary agent. `design` is the high-effort thinking and planning primary used before a fresh engineering session. `engineer` offers the same focused engineering role with approval-first edits and shell commands. `all-purpose` is the terse conversational primary for work that does not need either workflow.

OpenCode's built-in LSP support is enabled. In isolated portability checks, a repository with `gopls` produced diagnostics, while a repository without its expected PHP server stayed quiet and returned no diagnostics. Consuming projects can override LSP settings if their language-server setup behaves differently.

## Skills

Skills are reusable procedures, not additional agents. The active primary loads the relevant procedure and performs it in the same context. Skills are also available as direct slash commands. Agent `permission.skill` allowlists constrain model-initiated loading; they do **not** create a separate “user-only” channel. In OpenCode 1.18.1, direct `/tdd` invocation succeeded from an agent whose skill allowlist denied `tdd`, without an approval prompt.

Use an agent's allowlist to define what it may load autonomously. Treat a slash command you invoke yourself as explicit user direction.

No custom commands, tools, plugins, hooks, or MCP servers are installed by this repository.
