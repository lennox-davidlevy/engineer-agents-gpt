---
name: excalidraw
description: Draw, explain, compare, or refine ideas with editable Excalidraw diagrams using the local MCP canvas. Save the diagram and open the populated editor for the user.
---

# Excalidraw diagrams

Turn the user's idea into an editable diagram, not a software project. Use the
configured `excalidraw` MCP tools; do not clone Excalidraw, build a custom viewer,
or install a second diagram framework. The package includes the local web editor.
This is open-ended: architecture, flows, alternatives, sketches, and revisions
are all valid. Do not force a fixed architecture template or elaborate ceremony.

## Required style: Camenae

Before creating, restyling, or rendering a diagram, read
`references/camenae-theme.md`. Use Camenae for all generated diagrams and exports
unless the user explicitly requests another theme. Its styling rules override
the upstream diagram guide's aesthetic defaults. Default to Light mode on the
Stone `#e6dfd2` canvas, not a black background; use the reference's semantic
palette, fonts, sharp corners, and restrained emphasis.

Follow the reference's native-file and browser-render delivery path: the current
MCP does not preserve all scene settings/fonts through ordinary export/import.
Verify the live editor, editable file, and final image agree. Do not claim theme
fidelity merely because shape colors were set, or silently approximate unsupported
settings. No additional theme framework or renderer patch is needed.

## Connect and preserve existing work

- Use the configured launcher (`scripts/start.mjs` beside this skill). It installs
  a pinned project-local package and patches verified upstream bytes to enforce
  local Host/Origin checks for HTTP and WebSockets. Never bypass it with a direct
  `npx` launch: the unpatched 2.1.2 server lacks these protections. The checks
  isolate browser origins, not other programs running on the user's machine.
- Discover the `excalidraw` tools through Code Mode `search`, then use their exact
  schemas. Read `read_diagram_guide` once when beginning a drawing task.
- The repository configuration uses `mcp-excalidraw-server@2.1.2`, Node >=20,
  and `http://127.0.0.1:3210`. The MCP process auto-starts a local canvas server.
  No account, API key, global install, or Excalidraw clone is required.
- Check the configured URL rather than assuming the default if it was overridden.
  Use `http://127.0.0.1:<port>`; it has no authentication against local processes.
  Report a port conflict or an unprotected pre-existing canvas;
  do not kill an unrelated process or connect to an unverified service.
- Run `describe_scene` before changing anything. The canvas is shared by all
  clients on that URL, not isolated by OpenCode session or repository. Never clear,
  replace, or repurpose an unfamiliar populated canvas without confirmation.
  For a new drawing on an occupied canvas, ask whether to reuse it or use a
  separately configured port. Do not mix unrelated diagrams by default.
- For an existing file, import the requested `.excalidraw` scene only after checking
  the live canvas. Preserve current work before a user-approved replacement.
  Do not overwrite unrelated files or undo manual edits from another client.

## Draw what helps

Understand the question the diagram should answer. Read relevant code or supplied
facts for technical diagrams; distinguish existing behavior, proposals, and unknowns.
Ask only when ambiguity materially changes the drawing. A request to discuss an
idea alone is not authorization to mutate a canvas.

Choose a simple composition: clear labels, generous spacing, a consistent reading
direction, and a small color palette. Label important connections with their
meaning or direction; show ownership/trust boundaries when relevant, not merely
boxes connected by unexplained arrows. Keep large topics in separate views rather
than shrinking text until it becomes unreadable.

Prefer a batch of labeled shapes and bound arrows using `batch_create_elements`.
Use explicit stable IDs for later revisions. The toolkit accepts `text` on shapes
and `startElementId` / `endElementId` on arrows; consult the discovered schema and
guide for exact fields. Use element updates and layout tools for refinements,
not whole-canvas regeneration. Do not run mutating calls concurrently against
the same elements.

Mermaid conversion is optional, not the default: it needs a connected browser tab.
Ordinary element creation, screenshots, and file export do not. Do not introduce
browser automation just to draw shapes.

## Look, save, and open

1. Use `describe_scene` to check labels and relationships, then
   `get_canvas_screenshot` or `export_to_image` to inspect the actual result.
   If Code Mode does not expose the image visually, export a PNG inside the active
   repository and read it with the image tool. Fix clipping, overlaps, illegible
   text, and misleading arrows. Stop once the diagram communicates the requested
   idea; do not pursue decorative perfection. Headless previews are preliminary;
   use the theme reference's browser-render path for faithful final images.
2. Export an editable scene with `export_scene` to
   `docs/diagrams/<descriptive-name>.excalidraw` in the active repository, unless
   the user specifies another destination. Create parent directories first.
   Use a fresh filename for new diagrams, or update a file only when requested.
   Verify the exported file exists, parses as Excalidraw JSON, and contains the
   expected elements. Finalize its Camenae styling and scene state as described
   in the reference before loading it into the native editor. A PNG alone is not
   the editable deliverable.
3. Diagram files are ordinary documentation; do not automatically gitignore them.
   Respect the user's tracking preference. Runtime downloads, logs, and state go
   under `.cache/excalidraw/`; ensure that directory is ignored in the consuming
   repository without overwriting existing ignore rules. Never commit or push.
4. On macOS, run `open "http://127.0.0.1:3210"` (or the actual configured local
   canvas URL) to open the **populated** editor in the user's normal browser.
   Opening the completed diagram is part of a diagram-creation request unless
   the user opts out. Do not open an empty excalidraw.com page instead. If asked
   only to open an existing diagram, load it safely first; do not redraw it.
   For Camenae delivery, verify Light mode and the Stone background in that editor;
   a browser preference can differ from the file or automated preview.
5. Provide the editable file path and local canvas URL. State accurately whether
   opening succeeded. Leave the canvas server running for the user to edit.

The live canvas is in memory: server restart loses it. Exported files are the
durable copy. Browser edits do **not** automatically update that file; tell the
user to save from Excalidraw or ask for another export after editing. Snapshots
are not a substitute for file export.

## Privacy, authority, and failures

Drawing and headless exports run locally. The browser editor loads fonts from a
CDN; optional `export_to_excalidraw_url` uploads an encrypted scene to an external
service. Never upload/share a diagram without specific permission, even when the
tool is available. Do not include secrets in diagrams or external documentation
queries. A local browser opening does not authorize external writes.

Both primary agents may draw when requested; subagents remain read-only and do
not get these tools. Tool availability does not expand the user's task authority.

If MCP is unavailable, check `/mcps` and report the connection/dependency error.
Do not silently switch to another installation or remote service. A fresh OpenCode
session may be needed after installing this configuration. For CLI diagnostics,
invoke this skill's `scripts/start.mjs` by absolute path from the active project:
`node <skill-directory>/scripts/start.mjs status`. It also accepts `start` and
`stop`; stop only a canvas you own, after saving its work. Preserve the configured
`EXPRESS_SERVER_URL` environment when overriding the default. Unknown source-byte
errors require a reviewed patch update, not deletion of the checks. Use the
original launcher to stop an old unprotected server, with the user's permission,
or select a separately configured port. Never silently kill an existing server.

Upstream reference: https://github.com/yctimlin/mcp_excalidraw
