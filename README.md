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
| Excalidraw MCP (local canvas) | allow | allow | deny | deny | deny |


Built-in `build` and `plan` are disabled because `engineer` and `design` replace them. Snapshots and compaction retain runtime defaults; formatting, watcher exclusions, and project-specific tools belong to consuming projects.

### Editable diagrams

The bundled launcher applies a small browser-access patch to a private installation
of version 2.1.2: exact local Host/Origin checks for HTTP and WebSockets, rejection
of cross-site data requests, and no iframe embedding. Local MCP requests still
work. This protects against unrelated browser pages, not other local processes.
The launcher refuses unknown upstream bytes and unprotected existing canvases;
it never patches npm's download cache. Do not bypass it with a direct `npx` launch.

Ask either primary to use `excalidraw` to sketch, explain, compare, or revise an
idea. Node.js 20+ is required; no Excalidraw clone or desktop app is needed.
The pinned community MCP package includes the editor and starts a loopback canvas
at `http://127.0.0.1:3210`. First connection downloads the package into the project's
`.cache/excalidraw/`; the isolated HOME keeps package runtime state there too.
Ignore that cache in consuming repositories.

The command path assumes this repository is installed as the project's `.opencode`
directory, as described above. To run directly from this source checkout, use
`node skills/excalidraw/scripts/start.mjs start`. The same launcher accepts `status`
and `stop` (stop only your own canvas, after saving work). If an older unprotected
canvas occupies the port, save and stop it with its original launcher or choose a
different port; the patched launcher will not silently attach or kill it.

Run the HTTP/WebSocket regression after preparing the local package:

```sh
node skills/excalidraw/scripts/start.mjs --help
node --test skills/excalidraw/scripts/browser-access.test.mjs
```

`EXCALIDRAW_TEST_SERVER` can point the same test at a pristine 2.1.2 `dist/server.js`
to reproduce the failure. The test starts and stops its own canvas on a free port.

The skill saves editable files under `docs/diagrams/` and opens the populated
editor in your browser. Files are not automatically gitignored. The live canvas
is shared across sessions using that port and is lost when its server stops;
exported files persist. Manual browser edits need another save/export. Do not use
the same canvas concurrently for unrelated projects. A project-specific server
override can select another `EXPRESS_SERVER_URL` port (repeat the complete server
object because V2 replaces it; use `http://127.0.0.1:<port>`). Sharing externally requires explicit approval;
the local browser editor does fetch fonts from a CDN.

## Skills


Useful skills, some from [Matt Pocock](https://github.com/mattpocock/skills), [Kit Langton](https://github.com/kitlangton/skills), myself, twitter.  All of these I use regularly and only where I see good results relatively consistently:

- `code-review` for parallel Spec and Standards review in fresh contexts
- `diagnosing-bugs` for evidence-led debugging
- `effect` for Effect v4 TypeScript implementation patterns and reference guides
- `excalidraw` for editable diagrams on a local canvas, file export, and browser opening
- `research` for primary-source investigation
- `handoff` for compact cross-session context
- `prototype` for disposable design evidence
- `query-okf` and `curate-okf` for the Open Knowledge Format
- `test-audit` for test authoring gates, evidence-led deletion, and full subsystem test-pruning campaigns
