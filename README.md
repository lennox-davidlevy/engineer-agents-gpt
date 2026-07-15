# Engineer GPT for OpenCode

This repository installs a small engineering agent team for OpenCode. The default `engineer` can inspect and review freely, asks before direct edits or general shell commands, and asks before handing mutating work to a specialist. Read-only exploration, research, and review stay approval-free.

## Install

OpenCode must recognize the repository root as a configuration directory. Cloning it into an arbitrary project directory is not enough.

The following installation modes were verified with OpenCode 1.18.1.

### Install in project
Clone anywhere and point OpenCode at the clone:

```sh
git clone git@github.com:lennox-davidlevy/engineer-agents-gpt.git .opencode
```

## What approval means

- `engineer` reads, searches, and runs read-only Git inspection commands without prompting.
- Direct edits and general shell commands require approval.
- Read-only specialists (`explore`, `researcher`, and `reviewer`) launch without approval. Research artifacts still require edit approval.
- Mutating specialists (`worker`, `debugger`, `modularizer`, and `simplifier`) require approval before launch. Approval trusts that specialist to complete the bounded assignment without prompting for every routine edit or test command.
- Common destructive or external-write commands are explicitly denied to mutating specialists, including direct `git commit`, `git push`, `git reset --hard`, `git clean`, `rm -rf`, and `gh pr create`/`gh pr merge` attempts.

Those shell denials are defense in depth, not a sandbox. A specialist with general shell access is trusted for the approved assignment. Use an agent with `bash: ask` if a workflow needs approval for each command.

The hidden Standards and Spec review lanes are internal to `reviewer`; primary agents cannot launch them directly.

## Agents and models

The setup expects an OpenCode provider that exposes the configured OpenAI model IDs:

- Sol for engineering, design, difficult diagnosis, transformations, and review
- Terra for cost-efficient implementation, research, and general conversation
- Luna for fast repository exploration

Model binding and provider-option propagation could not be validated without loading the machine's real provider configuration, which was intentionally kept out of the isolated tests. For the same reason, the planned lightweight system-model override remains unset rather than assuming `openai/gpt-5.6-luna-fast` is available. Verify the configured model IDs with `opencode models` in each installed environment.

`engineer` is the default primary agent. `design` is the high-effort architecture partner, and `all-purpose` is a cost-efficient conversational alternative that does not delegate work.

OpenCode's built-in LSP support is enabled. In isolated portability checks, a repository with `gopls` produced diagnostics, while a repository without its expected PHP server stayed quiet and returned no diagnostics. Consuming projects can override LSP settings if their language-server setup behaves differently.

## Skills

Skills are available both through OpenCode's `skill` tool and as direct slash commands. Agent `permission.skill` allowlists constrain model-initiated skill loading; they do **not** create a separate “user-only” channel. In OpenCode 1.18.1, direct `/tdd` invocation succeeded from an agent whose skill allowlist denied `tdd`, without an approval prompt.

Use an agent's allowlist to define what it may load autonomously. Treat a slash command you invoke yourself as explicit user direction.

No custom commands, tools, plugins, hooks, or MCP servers are installed by this repository.
