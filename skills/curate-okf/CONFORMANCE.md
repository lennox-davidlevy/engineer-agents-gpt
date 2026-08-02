# OKF v0.2 conformance

Read this reference before writing or auditing a bundle. It is a working checklist for [the official OKF v0.2 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md), not a substitute version of the standard. Recheck the official specification before targeting another version.

## Hard requirements

A bundle is conformant only when all of these hold:

1. Every non-reserved `.md` file is UTF-8 Markdown beginning with a parseable YAML frontmatter block delimited by `---` lines.
2. Every such frontmatter block has a non-empty `type` string.
3. Every `index.md` and `log.md` follows its reserved structure.

Do not promote optional guidance into a hard failure. Unknown types and keys, absent optional fields, broken links, and missing indexes are conformant. Preserve unknown fields when improving a bundle.

## Reserved files

`index.md` and `log.md` are reserved at every directory level and are never concepts.

- An `index.md` normally has no frontmatter. Only the bundle-root index may have frontmatter, and only to declare `okf_version: "0.2"`. Its body groups links under headings; entries should carry the linked concept's description.
- A `log.md` groups prose entries under `YYYY-MM-DD` headings in newest-first order.

All other `.md` files below the bundle root are concepts. A directory name such as `references/`, `archive/`, or `sources/` does not exempt Markdown files from conformance.

## Concept fields

`type` is required. `title`, `description`, `resource`, and `tags` are recommended when meaningful. Types are producer-defined: use descriptive values consistently and never claim they come from a registry.

Bodies have no mandatory sections. Prefer structural Markdown. `# Schema`, `# Examples`, and `# Computation` carry conventional meanings when applicable.

Use bundle-relative links beginning with `/` when stability across moves matters. Relative links are also valid. The prose around a link must explain its relationship; the link itself is untyped.

## Provenance, trust, and lifecycle

When `sources` is present, every entry requires `resource`. Use a stable `id` when a body claim cites that source, and join the claim to the entry with a footnote carrying the same label. `title`, `author`, `usage_count`, and `last_modified` are optional credibility signals; do not infer or fabricate them. A shared `usage_window` frames usage counts unless an entry overrides it.

When `generated` is present, `by` is required and `at` records the last meaningful content change. `verified` is either a list of `{ by, at }` events or one bare event mapping. Generation is not verification.

Actor strings use `<producer>/<version>` for tools, `human:<id>` for people, and `process:<id>` for automation. Do not emit a human actor for agent-generated or merely user-supplied material.

`status`, when present, is `draft`, `stable`, or `deprecated`; absence means stable. `stale_after` is an absolute `YYYY-MM-DD` date and becomes stale on that date.

## Attested computations

For `type: Attested Computation`, `runtime` is required. Supply the computation either as one fenced block under `# Computation` or through the `computation` path, not both. Every parameter entry contains `name`, `type`, and a boolean `required`; an agent may bind declared parameter values but must not rewrite the sanctioned computation. `executor` declares how to run it and the receipt shape; `attester` points to deterministic, non-LLM verification.

Do not invent an attested computation merely because source material contains code. Use this type only when the material actually defines a sanctioned computation and its execution contract.

## v0.1 input

When improving or converting v0.1 material, migrate legacy `timestamp` to `generated.at` only when the producer identity is known; otherwise preserve the timestamp without fabricating `generated.by`. Move a legacy `# Citations` list into `sources` only when each resource and claim relationship can be represented faithfully.

## Validation claim

The official project does not provide a standalone bundle-validator command. Report this work as an exhaustive audit against the specification, not as certification by official tooling.
