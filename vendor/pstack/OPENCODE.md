# OpenCode adapter

Read this before the upstream skills. These rules override their Cursor-specific
instructions. Preserve the engineering workflows, not unavailable host APIs.

Local implementations live in `../../pstack-opencode/` relative to this bundle.
Read the native files named by the loaded wrapper before following upstream
steps. Their executable local procedures supersede the general fallbacks below.

## Loading and isolation

This directory preserves the upstream files, outside OpenCode skill discovery.
Do not register it directly or copy its skills into discovery directories.
Registered wrappers in the installation's `skills/pstack-*/` directories provide
native discovery and loading for poteto. Load `pstack-<id>` with the `skill` tool,
then read the original file in full as the wrapper directs. Upstream `/how`, for
example, means `pstack-how`, not a Cursor command or the unprefixed `how` ID.
Resolve relative links from the original file containing them. Cursor modes,
reminders, and icons have no runtime effect here. Wrapper metadata enables
advertising without changing upstream `disable-model-invocation` fields.

All 51 skills and their supporting files are included. The two files under
`agents/` are prompt resources, not additional registered OpenCode agents.
The configuration denies `pstack-*` skill access by default and allows it for
poteto. Engineer and design retain an explicit denial after their broad skill
allowance. A denial hides the wrappers from an agent's catalog and blocks skill
loading. This is not a filesystem sandbox. Other agents with filesystem access
can still read the files. Do not bypass a skill denial using direct file reads.

## Tools and delegation

| Upstream concept | OpenCode behavior |
| --- | --- |
| Read, Glob, Grep, Shell, edits | Use `read`, `glob`, `grep`, `shell`, and `patch`. |
| AskQuestion | Use `question` for actual product choices or permission gates. |
| TodoWrite | Use an available todo tool, otherwise maintain a brief checklist. |
| Task | Use `subagent` with `agent`, `prompt`, and optional `background`. |
| poteto-agent | Poteto is primary-only. The primary performs implementation directly. |
| generalPurpose, reviewers, investigators | Choose an available read-only agent whose permissions fit. Supply code/artifact paths and task-specific criteria, not skill-loading instructions. |
| Comment Sicko | Read `agents/comment-sicko.md` and give its rubric to `reviewer`; do not register another agent. |
| control-ui | Discover Playwright Code Mode tools for web UI checks. Electron/native control requires a separately available harness. |
| control-cli | Use shell commands and existing project CLI tests. Report interactive TUI verification as blocked without a suitable harness. |
| create-skill | Use the available `skill-creator` workflow, if present. |
| deslop | Perform the requested cleanup directly using the bundled principles and code-quality rubric; disclose this substitution. |

A read-only delegate cannot edit code, spawn workers, or call unavailable MCPs.
Do not use it for implementation or ask it to read denied skill files. Poteto
owns implementation and applies accepted findings directly. A leaf delegate
must not recursively launch the entire parent playbook. Do not launch duplicate
panels from every worker. If delegation
is unavailable, work directly and report the missing independent check.

Do not copy Cursor model slugs into OpenCode tool calls. Inherit the session
model by default. Only select another model when the user requests it, discover
the actual provider/model ID first, and report the models actually used. A
single-model review is not a multi-model review. The `setup-pstack` skill's
Cursor model probing and `~/.cursor/rules/pstack-models.mdc` writes do not apply;
use `pstack-opencode/models.md` for discovery and approved local role choices.
Never change global model configuration
as an incidental setup step.

## Host-specific workflows

- **History and recall.** Do not inspect `~/.cursor/projects` or guess an
  OpenCode database layout. Use the current conversation, supplied transcripts,
  and the native history port's scoped session-list/export procedure. If history
  is inaccessible, say so.
  This applies to recall, automate-me, correct, reflect, session pickup, and
  transcript-based evaluation. Do not execute Cursor transcript audit commands.
- **Generated skills.** Write authorized project-local verification skills
  under `.opencode/skills/`, not `.cursor/skills/`. Creating a personal mode or
  additional agent is a separate user request, not part of installing poteto.
- **Cloud isolation.** Cursor cloud workers are unavailable. Local worktrees
  isolate files but not machines, credentials, processes, or network. Do not
  label them cloud workers or claim equivalent independent verification. Stop
  any step that requires cloud isolation and report the missing prerequisite.
- **Loops.** Use the native bounded-run procedure, not an implied `/loop`
  service. Work within the active session and actual background tool lifecycle.
  Do not promise overnight persistence or monitoring after the session ends.
- **Automation UI.** `make-bot-ui` depends on Cursor automation webhooks and
  Grok Bot infrastructure. It is included for reference, not an OpenCode-native
  automation service. Explain that prerequisite before implementing it.
- **External integrations.** Discover available MCP tools rather than guessing
  names. GitHub CLI, Bun, Origin, observability services, and project verification
  harnesses are optional prerequisites, not installed by this bundle. Inspect
  scripts before executing them; inclusion is not permission to run them.
- **Shipping.** Opening PRs, team messages, ticket updates, deployments, and
  merges require specific authorization. Never commit or push. Skip upstream
  automatic PR-opening steps and hand the result back locally. A user's request
  for an investigation does not authorize code edits.

## Verification

Use the actual application or public interface to verify changes. Do not call
configuration parsing, a worker's report, or model consensus proof of runtime
behavior. Label substitutions and blocked steps. All skills are readable; that
does not mean every Cursor-dependent workflow is executable on OpenCode.
