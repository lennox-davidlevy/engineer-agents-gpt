---
name: query-okf
description: Query an OKF knowledge bundle when the user asks a read-only question about its contents.
---

Query an OKF bundle by wayfinding, not bulk reading. A bundle is a directory tree of Markdown concepts connected by ordinary links; `type` is producer-defined, so route from titles, descriptions, and prose rather than assuming a taxonomy.

## Process

1. Locate the bundle root and read its `index.md` when present. A root index may declare `okf_version`; indexes elsewhere have no frontmatter. If no index exists, list the immediate tree and inspect concept frontmatter without reading every body.

   Complete when the bundle boundary and the smallest plausible entry points are known.

2. Follow the index descriptions into the concepts that directly match the question. Descend through a subdirectory's `index.md` before opening its concepts. When an index is absent, route from filenames and frontmatter. Do not open a concept merely because it might be relevant.

   Complete when the selected concepts have an explicit route from an index entry, filename, or frontmatter value.

3. Read the selected concepts and inspect their trust, lifecycle, and provenance fields. Follow an in-body link only when it resolves a remaining part of the question; surrounding prose defines the relationship. Resolve claim footnotes through the matching `sources[].id`.

   Complete when every part of the answer is supported, or the bundle's gap is established without speculative reading.

4. Answer naturally, citing the concept IDs used either inline or in a compact source list. Put a trust or lifecycle caveat beside the claim it affects. Report a wayfinding defect only when poor navigation materially obstructed the answer.

   Complete when the answer or documented absence is clear, attributed, and reproducible from the reported route.

When answering requires unexpectedly broad reading, reassess the route before opening more concepts. Broad questions may legitimately span many concepts; the signal of a defect is unnecessary or speculative reading, not a fixed count.

## Trust and lifecycle

All fields below are optional. Their absence never makes a concept malformed.

| Signal | Interpretation |
|---|---|
| no `verified` key | unverified |
| only non-`human:` verifiers | machine-confirmed |
| any `human:<id>` verifier | human-reviewed |
| `status: draft` | possibly incomplete and not yet reviewed |
| `status: deprecated` | retained for history, not current guidance |
| today on or after `stale_after` | stale |

`generated` identifies how the current content was produced and when it last changed; it is not verification. When `generated.at` is later than a verification event, that event does not confirm the current text even though the formal OKF trust tier still derives from the presence of `verified`. Prefer fresh, currently human-reviewed concepts when claims conflict, but report the contradiction rather than silently choosing. Do not withhold an answer solely because its support is unverified.

## Consumer tolerance

`type` is the only universally required concept field. Unknown types and keys, missing optional metadata, broken links, and missing indexes are all permitted by OKF v0.2. Treat them as generic or incomplete navigation, not conformance failures.

`index.md` and `log.md` are reserved at every directory level and are not concepts. Read `log.md` only when recent changes or known gaps bear on the question.
