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

- An explicit implementation request authorizes ordinary repository edits for that task. Shell commands remain permission-controlled; consuming repositories can allow known-safe local checks.
- Commits are denied. External writes, destructive actions, pushes, production access, and material scope expansion require specific approval.
- `engineer` performs production work directly. Subagents are limited to exploration, research, and independent review.
- Handoffs carry context, not permission.
- Dirty worktrees need an explicit task or accumulated-change review boundary.

These permissions are guardrails, not a sandbox.

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
)
git diff --check
```

There are no committed build, lint, or application test scripts.
