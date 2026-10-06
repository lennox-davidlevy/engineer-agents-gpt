# Bundled pstack

Private skill library for the single [poteto agent](../../agents/poteto.md).

## Provenance

- Author: Lauren Tan (poteto).
- Source: <https://github.com/cursor/plugins/tree/main/pstack>.
- Snapshot: `e5a8186d7b43be8d6ac4452440fbead5f1a51c70`, plugin version `0.15.13`.
- License: [MIT](LICENSE), including the upstream copyright notice.
- Imported: the complete `skills/` and `agents/` trees from the local upstream
  checkout. They are preserved unchanged, including script tests and fixtures.
  Plugin assets, guides, and the separate dormant automation pack are not imported.

The maintained OpenCode adaptation is [OPENCODE.md](OPENCODE.md), not a claim
that upstream Cursor infrastructure is available here. Keep adaptation changes
outside the snapshot so future updates can be compared with upstream.

## Install and share

Clone this repository as a project's `.opencode` directory, as described in the
root README. Keep `opencode.json`, `agents/`, `skills/pstack-*/`, and
`vendor/pstack/`, and `pstack-opencode/` together. No external pstack checkout, absolute developer path,
plugin installation, or additional skill-source registration is required.
For a global installation, preserve that layout in the OpenCode config directory
or symlink the config, agents, and skills to this repository. Wrappers resolve
the bundle relative to their real directory, so symlinked skills work too.

Select `poteto` as the session agent. The default remains `engineer`. Poteto
inherits the selected model. Tell it the task normally; its prompt loads the
adapter and routes through the bundled `poteto-mode` workflow.

The `vendor` snapshot stays outside discovery. Generated `pstack-*` wrappers
advertise each original skill to poteto and require loading its full text.
Namespaced IDs avoid collisions with this repository's normal skills.
Permissions hide and deny these wrappers for the other configured agents.
The global default denial must travel with the wrappers. Later agent-specific
allowances can override it, so retain a final `pstack-*` denial when adding a
broad skill allowance to another agent. This is skill-tool isolation, not a
filesystem sandbox. Do not configure `vendor/pstack/skills` as a skill source.

After updating the upstream snapshot, regenerate and check the wrappers:

```sh
python3 scripts/sync_pstack_wrappers.py
python3 scripts/sync_pstack_wrappers.py --check
```

The generator copies each skill's description and enables OpenCode discovery.
It never modifies upstream files or deletes stale wrappers automatically.
It also loads the local port map from `pstack-opencode/ports.json` and rejects
missing or out-of-bundle references before writing any wrapper.

Run the generator's disposable-installation tests with:

```sh
python3 scripts/test_pstack_wrappers.py
```

To check registration and isolation against the installed OpenCode runtime,
run from a fresh validation project containing this setup as `.opencode`:

```sh
python3 .opencode/scripts/check_pstack_access.py
```

This creates local test sessions and evaluates every pstack skill permission
for poteto and the six other tested agents. It makes no model requests and
executes no skills. A real poteto loading check and an engineer denial check
should also be run after changing the wrappers or adapter.

## Compatibility limits

The [local OpenCode ports](../../pstack-opencode/README.md) provide scoped session
history/export, model-role setup, existing read-only delegation, verification,
and bounded runs. They replace the corresponding Cursor steps without editing
the snapshot. Poteto remains the single implementation owner and primary agent.
Cloud workers, unattended scheduling, automation webhooks, and native desktop
drivers are not provided. Optional CLI/MCP integrations need their own setup and
authorization. Availability of 51 skill files is not an end-to-end certification
of all 51 workflows.
