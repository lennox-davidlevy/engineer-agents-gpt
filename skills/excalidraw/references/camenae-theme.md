# Camenae theme

Required styling for all diagrams, flowcharts, sketches, and renders made with
this skill, unless the user explicitly requests a different theme. These rules
override the upstream diagram guide's aesthetic defaults, not its API guidance.
Preserve meaning, content, IDs, and bindings when restyling an existing diagram.

## Palette

Use the exact values, not approximate named colors or Excalidraw's default swatches.

| Token | Color | Use |
| --- | --- | --- |
| Stone | `#e6dfd2` | Canvas, storage, alternating lanes |
| Surface | `#fbf8f2` | Ordinary cards and steps |
| Ink | `#23201b` | Default strokes and text |
| Deep | `#1f1c18` | Core runtime, dark tags, legend |
| On-dark | `#f8f3ea` | Text on Deep or Accent fills |
| Muted | `#6b6255` | Secondary text, external boundaries, return arrows |
| Faint | `#cfc6b5` | Subgroups, deprecated strokes, planned fill |
| Accent | `#b4412c` | Primary emphasis, failures, denied paths, trust boundaries |
| Healthy | `#3f7a66` | Allowed/healthy status only |
| Warning | `#c08a2e` | Warning/degraded status only |
| Approval | `#2c4a9e` | Approval/human decision emphasis only |

## Global defaults

- **Light theme; Stone canvas.** Never default to a black canvas or dark-mode
  color inversion. Deep is an element fill, not the canvas background.
- Grid off. If specifically requested, use a faint ink grid (design target:
  `rgba(35,32,27,.08)`); do not invent a grid-color API if the editor lacks one.
- Architect sloppiness: `roughness: 0`.
- Sharp corners: `roundness: null`. No rounded cards; decorative arches/ovals are
  exceptions only when intentional. Semantic diamonds remain diamonds.
- Thin strokes: `strokeWidth: 1`; use `2` for a focal element or specified status.
- Solid fills: `fillStyle: "solid"`; hachure only for planned/not-built areas.
- Full element opacity: `opacity: 100`. Mute with Muted/Faint colors, not fading.
  An explicitly unfilled shape uses `backgroundColor: "transparent"`; that is
  different from reducing the whole element's opacity.
- No gradients, shadows, arbitrary fills, or decorative status colors.

## Typography

- Labels: **Nunito**, Ink. Native Excalidraw font ID: `6`.
- Tags, IDs, protocols, connector labels, and annotations: **Code/Cascadia**,
  native font ID `3`. Tags and protocols are UPPERCASE, Muted, small (typically
  16 px). Use actual text such as `HTTPS`, `GRPC`, `SSE`, `YES`, `NO`.
- Title: Nunito, Ink, largest size (typically 32–40 px). Body labels are typically
  20–24 px. Establish hierarchy with size and spacing, not a substituted serif.
- Text on Deep or Accent fills: On-dark, explicitly set on the text element.
  Shape stroke color and label color are independent; do not inherit dark-on-dark.
- Put a small numbered tag above component boxes, e.g. `S·01`, `DB·02`, `Q·03`.
  Keep IDs stable across revisions. Do not number every arrow or annotation.
- Fit boxes to readable text; remeasure/reflow text after font, size, or content
  changes. Do not shrink a crowded diagram into illegibility.

## Components

All unspecified text is Ink; unfilled means transparent fill at full opacity.

| Component | Stroke | Fill / text | Details |
| --- | --- | --- | --- |
| Service / app | Ink | Surface | Width 1 |
| Primary / entry point | Accent | Accent / On-dark | Reserve for the main focus |
| Core runtime / engine / worker | Deep | Deep / On-dark | At most 2–3 deep focal elements |
| Database / storage | Ink | Stone | Rectangle with double top line; cylinder only if supported |
| Queue / stream / bus | Ink | Unfilled | Long thin rectangle with thin dividers |
| External system / third party | Muted | Unfilled | Dashed border |
| Client / user / browser | Ink | Unfilled | UPPERCASE code tag above |
| Planned / future / not built | Muted | Faint, hachure | Dashed border |
| Deprecated / removed | Faint | Unfilled / Muted | Dotted border |
| Error / failure | Accent | Surface | Width 2 |
| Approval / human-in-the-loop | Approval | Surface | Width 2 |
| Healthy / allowed | Healthy | Healthy | Small solid square beside the label |
| Warning / degraded | Warning | Warning | Small solid square beside the label |
| Note / annotation | Muted | No box / Muted code text | Thin muted leader line if needed |
| Legend | Deep | Deep / On-dark | Bottom corner, only when it explains notation |

## Groups and boundaries

| Boundary | Style |
| --- | --- |
| System / VPC / environment | Ink, width 1, unfilled; Deep tag with On-dark text at top-left edge |
| Trust zone / security | Accent, dashed, unfilled |
| Subgroup / module | Faint, solid, unfilled |
| Zones / lanes | Alternate Stone and Surface, no enclosing stroke; thin Ink separators |

## Connectors

| Meaning | Color / width | Line / head |
| --- | --- | --- |
| Call / request | Ink / 1 | Solid, filled triangle head, orthogonal routing |
| Async / event / pub-sub | Ink / 1 | Dashed, open arrowhead |
| Response / return | Muted / 1 | Dashed, open arrowhead |
| Primary / critical path | Accent / 2 | Solid |
| Replication / sync | Ink / 1 | Dotted, heads on both ends |
| Blocked / denied | Accent / 1 | Dashed, bar at destination |
| Loop-back | Muted / 1 | Dashed |

Native arrowhead values include `triangle`, `arrow` (open), and `bar`. Use explicit
orthogonal points with sharp joints where needed; binding endpoints does not
automatically guarantee the requested route. Keep labels Muted, small Code,
UPPERCASE, independent of arrow stroke color. Avoid crossings through text/boxes.

## Flowcharts

| Element | Style |
| --- | --- |
| Start / end | Deep fill, On-dark text; sharp rectangle by default |
| Process | Ink stroke, Surface fill |
| Decision | Diamond, Ink stroke, Stone fill; outgoing `YES` / `NO` labels |
| Input / output | Parallelogram, Ink stroke, unfilled |
| Approval gate | Diamond, Approval stroke, width 2, Surface fill |

Do not send invented `cylinder` or `parallelogram` types to MCP. Use supported
geometry (e.g. grouped line segments and text for a parallelogram), or explain a
limitation rather than silently changing notation.

## Emphasis rules

- Limit decorative red emphasis to one or two focal items. Red required to convey
  failures, denial, or trust boundaries is exempt; do not hide meaning to meet a
  color quota. Red must not become the dominant background color.
- Green, gold, and blue communicate status or meaning, never decoration. Pair
  color with a label/shape so color alone does not carry the distinction.
- Keep Deep fills selective. Boundary tags and a compact legend do not justify
  turning every component dark.

## Apply and preserve the theme with the current MCP

The installed community package is **2.1.2**, not the official Excalidraw CLI.
Check discovered tool schemas before passing fields. Its convenience tools do
not expose every native Excalidraw property. In particular:

- `export_scene` writes a white `appState.viewBackgroundColor`; MCP `import_scene`
  imports elements/files but ignores `appState`.
- Export expansion can replace `roundness: null` with rounded defaults.
- Convenience shape labels inherit stroke color; arrow labels get their own
  default ink/size. Use explicit bound text in the native file for independent
  On-dark labels and Code connector labels. Preserve both `containerId` and the
  container's `boundElements`; don't create a duplicate label.
- Headless rendering substitutes some fonts, including Nunito, and the CLI's
  offline `render` path ignores scene `appState`. It is not proof of exact Camenae
  typography/background. Do not label that output as a faithful final render.

**Use this delivery path instead of adding another server patch:**

1. Build/edit the diagram through MCP using explicit supported style fields.
2. Export to the requested native `.excalidraw` file. Finalize its element styles,
   bound text colors/fonts, sharp corners, and scene state according to this
   reference. Keep content, geometry, files, and bindings intact. Set:

   ```json
   {
     "appState": {
       "viewBackgroundColor": "#e6dfd2",
       "theme": "light",
       "gridSize": null,
       "exportBackground": true,
       "exportWithDarkMode": false
     }
   }
   ```

   Merge these settings into existing `appState`, not over the whole document.
   Do not overwrite this finalized file with an uncorrected MCP export later.
3. Open/drop the finalized file into the **local editor**, not through MCP
   `import_scene`, so native scene settings and corners are applied. This is a
   replacement of the canvas: only do it for the user's current diagram, after
   checking no unrelated/manual work will be lost. Check the editor is in Light
   mode, Stone background, grid off, with Nunito loaded. A browser's saved theme
   preference can override expectations; file metadata alone is not sufficient.
4. Let the browser sync finish (or use **Sync to Backend**) before exporting an
   image. Use MCP `export_to_image` with `renderer: "browser"`, `background: true`,
   and `dark: false`, with this editor tab connected. Inspect the resulting PNG
   or SVG. Browser export uses the live scene background and browser fonts.
   The guarded CLI equivalent is `node <skill>/scripts/start.mjs screenshot
   --renderer browser --out <absolute-output.png>`; do not pass `--dark` or
   `--no-background`. Preserve the configured canvas URL.
5. Recheck the final editable file and final image after every revision/export.
   Native editor saves may omit session-only preferences; explicitly selecting
   Light mode remains necessary. When opening the user's normal browser, don't
   assume it shares the automated browser's saved theme or background state.

Use Playwright tools for automated local-editor interactions. Native file pickers
may not work under automation; a native file drop exercises the same import path.
If automation or browser fonts are unavailable, retain the finalized editable
file and explain the remaining opening/rendering step. Do not silently substitute
a black/white background, another font, an image of the diagram, or an oversized
background rectangle to conceal a scene-state limitation.

## Delivery check

- Stone background, light colors, no dark-mode inversion or transparent export.
- Exact palette; no accidental default pastel colors, default black labels on
  dark fills, hachure on completed work, or rounded cards.
- Nunito body/title; small Code tags and connector labels; readable contrast.
- Expected semantic emphasis, solid status squares, labeled arrows.
- Editable native file retains the intended style; browser-rendered image matches
  the populated editor. Inspect the actual image, not just the JSON values.
