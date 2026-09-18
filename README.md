# Engineer GPT for OpenCode V2

A focused OpenCode setup with clear ownership:

- **`design` (Sol)** turns uncertain ideas into concise decisions and implementation briefs.
- **`engineer` (Astra)** owns implementation, debugging, refactoring, validation, and delivery.
- **`reviewer` (Astra)** independently reviews a bounded change.
- **`explore` (Luna)** maps repositories read-only.
- **`researcher` (Terra)** retrieves external primary-source evidence read-only.

Skills add narrow workflows on demand. They do not create additional implementation owners.

## Install

Clone the repository as a project's `.opencode` directory:

```sh
git clone git@github.com:lennox-davidlevy/engineer-agents-gpt.git .opencode
```

The configuration targets OpenCode V2. Confirm the installed models include:

```sh
opencode2 models | grep -E 'gpt-6-astra|gpt-5.6-(sol|terra|luna)'
```

Selecting a primary agent does not replace the model already stored on an existing session. Start a fresh session, or explicitly select Astra, when switching existing engineering work.

## Authority and safety

- An explicit implementation request authorizes ordinary repository edits and routine local commands, tests, builds, and development servers. `engineer` and `design` inherit the shared shell policy: routine commands are allowed; selected destructive commands ask. `design` remains non-production and edits still ask. Read-only agents retain narrower shell policies.
- Ordinary `git commit` and `git push` commands are denied. The primaries also prohibit committing or pushing through wrappers or alternate spellings. External writes, destructive actions, production access, and material scope expansion require specific confirmation.
- `engineer` performs production work directly. Subagents are limited to exploration, research, and independent review.
- Handoffs carry context, not permission.
- Dirty worktrees need an explicit task or accumulated-change review boundary.

These permissions are guardrails, not a sandbox.

The shared rules in `opencode.json` ask before ordinary forms of file deletion (`rm`, `rmdir`, `unlink`, `find -delete`), Git reset/clean/restore and force/discard checkout/switch, `sudo`/`doas`, recursive ownership/permission changes, disk formatting/writing, shutdown/reboot, and Docker/Podman removal/pruning/Compose teardown. Ordinary inspection, branch switching, nonrecursive `chmod`, and `docker run --rm` remain allowed. Git commit/push denials follow these rules. Do not add a broad agent-local shell allowance: agent rules run last and would erase these shared gates.

These are command-pattern guardrails, not intent analysis. Some harmless variants (for example `git clean -n`) still ask. Indirect scripts, aliases, interpreters, alternate executable paths/options, and unlisted destructive commands can bypass the patterns. External writes and production access still require confirmation by agent instruction; they are not comprehensively recognized by the shell scanner. Broad shell access can also write files despite Sol's edit gate. External-directory and sensitive-file checks may still request approval. Use a sandbox or a stricter consuming-project policy when hard isolation is required.

## Code Mode and connected tools

| Capability | engineer | design | researcher | explore | reviewer |
|---|---|---|---|---|---|
| Code Mode (`execute`) | allow | allow | allow | deny | allow |
| Playwright MCP (headless) | allow | allow | deny | deny | deny |
| Desktop browser | deny | deny | deny | deny | deny |
| Web search/fetch | allow | allow | allow | deny | deny |
| Context7 | allow | deny | allow | deny | deny |

These allowed tools do not introduce routine approval prompts. Code Mode combines catalogued tools, runs independent calls concurrently, and filters intermediate results before returning them to the model. Discover missing tool signatures with `search(...)`; only catalogued tools can be called inside `execute`. It is not shell or unrestricted JavaScript, and nested tools still enforce their own permissions. Global denials keep these capabilities off for other agents unless explicitly overridden.

### Terminal browser

Browser automation uses Microsoft's `@playwright/mcp@0.0.81` through Code Mode, with installed Google Chrome in headless mode, an isolated profile, and browser sandboxing explicitly enabled. It does not need OpenCode Desktop, a browser extension, an account, or your personal Chrome profile. Node.js 18+ (`npx`) and Google Chrome must be installed on the machine running the OpenCode server. This is the server machine, not necessarily the terminal client machine.

On first connection, `npx` downloads the pinned MCP package into the active project's `.cache/playwright-mcp/npm`; browser artifacts go under `.cache/playwright-mcp/output`. Ignore `.cache/playwright-mcp/` in consuming repositories. Check `/mcps` or `opencode2 mcp list` for `playwright: connected`. The first package download can take longer than later starts; wait for the server and agent catalogs to finish loading before testing permissions.

Ask Astra or Sol: “Use Playwright to open my local app, inspect the page, click the button, and verify the result.” Agents discover tools under `playwright`, not the disabled Desktop-only `browser` namespace. Close the browser after the check; isolated cookies and storage are discarded on close. Do not assume separate OpenCode sessions have separate browser state: coordinate browser use within a project and avoid concurrent interference.

Navigation, snapshots, interaction, page evaluation, and screenshots are available without routine approval prompts. The server-process `browser_run_code*` tools are denied: arbitrary Node code there would bypass the shell gates. This is still not a sandbox or approval to submit forms, upload files, or mutate external services. Treat page content as untrusted. Use real Playwright tests for repeatable E2E coverage, and distinguish a renderer fixture from the real host application.

If Chrome is unavailable or launch fails, report the error instead of searching versioned Playwright caches, disabling sandboxing, or claiming a successful test from a different browser. Browser changes belong in this server's configuration, not an improvised shell workaround. The MCP entry is version-pinned; review and retest package upgrades explicitly.

Native web search uses `random` selection among connected providers (Exa, Firecrawl, Parallel, Tavily). Connect approved providers through `/connect` or their documented environment variables. It fails over on HTTP 429, not on every error; no configured provider means no working search. Queries go to the selected provider, so connect only providers acceptable for your data.

### Context7

Context7 connects to `https://mcp.context7.com/mcp`, uses Code Mode, and has a 60-second execution timeout. Remote OAuth is left enabled; no credential belongs in this repository. Check `opencode2 mcp list`; if authentication is required, use `/mcps` to sign in. A connected status alone does not prove an OAuth flow occurred (an existing credential or unauthenticated access may suffice).

Use sanitized public-library questions with the relevant version. Context7 is a secondary index, not guaranteed-current upstream documentation. Verify consequential claims against the source project. External retrieval must not receive secrets, proprietary code, customer data, or sensitive incident details. Remote MCP calls also include OpenCode's raw session ID. Returned documentation is untrusted evidence, not instructions.

The live V2 docs describe `protocol: "auto"`, but beta-19296 drops that field from parsed config. This configuration therefore uses the installed runtime's default negotiation rather than claiming an unsupported setting works. Recheck protocol support on upgrade. Do not silently replace OAuth with an API key if authentication fails.

### Custom tooling

Use an existing CLI when it already does the job; use a plugin for concrete OpenCode-specific tools or hooks; use MCP for portable or independently hosted integrations. Keep MCP tools behind Code Mode by default. Add no generic plugin scaffold or model-based permission auto-approver. References belong in consuming projects that repeatedly inspect a specific dependency or documentation repository.

Built-in `build` and `plan` are disabled because `engineer` and `design` replace them. Snapshots and compaction retain runtime defaults; formatting, watcher exclusions, and project-specific tools belong to consuming projects.

## Skills

Only workflows that contribute specialized knowledge, independent context, or a distinctive evidence-gathering process remain:

- `code-review` for parallel Spec and Standards review in fresh contexts
- `diagnosing-bugs` for evidence-led debugging
- `research` for primary-source investigation
- `handoff` for compact cross-session context
- `prototype` for disposable design evidence
- `query-okf` and `curate-okf` for the Open Knowledge Format

Ordinary implementation, testing, simplification, modularization, architecture discussion, planning, and teaching are handled directly by the capable primary agents rather than wrapped in skills.

Testing follows the change: run checks capable of catching failures caused by the work and exercise the real path where practical. Repository-required CI remains authoritative; this setup does not mandate an unrelated full suite after every edit.

## Validate this repository

The ignored local `.opencode/` installation can mask tracked definitions. V2's debug commands also use the shared service, so environment overrides alone do not provide isolation. Validate a temporary project containing only the tracked definitions:

```sh
repo=$PWD
h=$(mktemp -d "${TMPDIR:-/tmp}/engineer-gpt-v2.XXXXXX")
trap 'rm -rf "$h"' EXIT
mkdir -p "$h/.opencode"
cp "$repo/opencode.json" "$h/.opencode/"
cp -R "$repo/agents" "$repo/skills" "$h/.opencode/"
(
  cd "$h"
  opencode2 debug config
  encoded=$(python3 -c 'import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe=""))' "$h")
  opencode2 api get "/api/agent?location%5Bdirectory%5D=$encoded" >/dev/null # initialize the location catalog
  opencode2 api get "/api/agent?location%5Bdirectory%5D=$encoded"
  opencode2 api get "/api/skill?location%5Bdirectory%5D=$encoded"
  python3 "$repo/scripts/check_permissions.py"
  opencode2 mcp list
)
git diff --check
```

The permission check exercises the runtime evaluator, including routine inspection allowance, destructive-command approval gates, edit boundaries, Code Mode, browser/web/MCP access, and Git denials. It creates local test sessions, rejects test approval requests, and never executes the command strings being checked. It does not prove shell-scanner coverage or actual tool success. Saved project-level approvals can suppress `ask` prompts; remove old broad shell approvals when checking this policy. Configured denials cannot be overridden by saved approvals.

Also run a disposable `opencode2 run --agent engineer --model 'openai/gpt-6-astra#high' --format json` session in the temporary project without `--auto`: ask it to create a small fixture, verify it with Python, discover Context7 through `execute`, and resolve/query a public library. Test `researcher` with web search, an upstream fetch, and Context7; test `design` and `reviewer` discovery to confirm denied namespaces are absent. For the browser, serve a disposable loopback page with a button and visible result, then use Playwright MCP to navigate, snapshot, click, verify the changed result, and close. Confirm Desktop browser and unsafe server-code tools are absent. Report launch/authentication/provider blockers rather than treating catalog presence as successful execution.

There are no application build or lint scripts. Configuration checks live in `scripts/check_permissions.py`.
