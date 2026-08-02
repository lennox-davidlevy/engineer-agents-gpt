---
name: curate-okf
description: Curate an OKF bundle from raw Markdown, or improve an existing bundle.
---

Curate for lossless retrieval: turn scattered documents into durable concepts that an unfamiliar agent can find, trust, and trace. Target OKF v0.2. Do not mistake smaller files for better knowledge.

## Branches

- **Convert** raw notes, a large Markdown file, or an irregular documentation tree into a new bundle. Source material is evidence: never edit, move, rename, or delete it. Create the bundle at a collision-free sibling path unless the user chooses another destination; source and bundle trees must remain disjoint.
- **Improve** a confirmed OKF bundle in place. Preserve valid knowledge, concept IDs, source attribution, and unknown frontmatter unless changing one is necessary to correct a demonstrated defect.

A mixed or malformed directory is raw source unless the user explicitly identifies it as a bundle to repair. There is no ignored directory inside OKF: every non-reserved `.md` file below the bundle root is a concept.

Run end-to-end without a routine approval gate. Pause only when a material decision cannot be inferred safely, including suspected secrets, conflicting authoritative claims, multiple plausible audiences, an ambiguous bundle boundary, or a destination collision.

## Process

1. **Establish the boundary.** Identify the source root, bundle root, intended audience, and the questions the material appears meant to answer. On the convert branch, resolve both roots and reject either tree containing the other; inventory every source file and record its resolved path and SHA-256 digest in a temporary manifest outside both trees. Mark non-Markdown files as unsupported input rather than extracting knowledge from them. For large Markdown files, inventory substantive sections as well. On the improve branch, inventory every existing file and inspect indexes and frontmatter before reading concept bodies.

   Complete when every input is listed and any material ambiguity has been resolved; conversion additionally requires disjoint trees and a complete pre-write source manifest.

2. **Build the coverage map.** On the convert branch, map every useful claim in every Markdown source file and substantive section to one or more target concept IDs. Map duplicates to the shared concept and retain conflicts as attributed claims. Exclude only empty, structural, or boilerplate Markdown that carries no knowledge, with a concrete reason; stale, unsupported, contradictory, or out-of-scope knowledge is not excludable. List non-Markdown files separately as unconverted. On the improve branch, assign every existing concept a disposition such as keep, split, merge, relink, or deprecate. Decompose by durable meaning—an asset, idea, decision, procedure, contract, or computation—not mechanically by heading or length. A concept may combine related passages from several sources, and one source may feed several concepts.

   Complete when conversion maps every useful claim and permits only demonstrably non-knowledge exclusions, improvement accounts for every existing concept without losing valid knowledge, and every proposed concept has a distinct purpose.

3. **Design the wayfinding.** Choose a small, self-explanatory type vocabulary suited to the domain. Plan shallow directories, a root index, an index for each directory, concise titles and descriptions, and prose links whose surrounding text names the relationship. Derive representative questions from the corpus and ensure the index descriptions route each question toward its answer.

   Complete when every concept is reachable from the root, sibling concepts are distinguishable from their descriptions, and each representative question has a short planned route.

4. **Write the bundle.** Before writing, read [`CONFORMANCE.md`](CONFORMANCE.md) and apply every applicable v0.2 rule. Normally give each concept `type`, `title`, and `description`; add `resource`, tags, provenance, trust, and lifecycle metadata only when the source supports them. Never invent verification, freshness, authority, or source credibility. Preserve disagreements and superseded material with attribution instead of synthesizing false consensus.

   On the convert branch, create `provenance/source-map.md` as a conformant `Source Map` concept containing the coverage map, source paths, and pre-write digests, then link it from the root index. Point each concept's `sources` entries to the precise original files or external sources it derives from. The originals remain outside the bundle.

   On the improve branch, make the smallest coherent changes that fix coverage, decomposition, wayfinding, provenance, or lifecycle defects. Do not churn paths or metadata merely for uniformity.

   Complete when the planned concepts, indexes, links, and conversion provenance exist and every generated claim remains traceable to source material.

5. **Audit exhaustively.** Inspect every bundle file; sampling is not validation. Separate hard conformance failures from quality defects:

   - **Conformance:** every non-reserved `.md` has parseable YAML frontmatter and a non-empty `type`; every `index.md` and `log.md` follows its reserved structure.
   - **Field contracts:** every optional family that is present follows its specified shape, and an Attested Computation carries its required runtime contract. Record these separately from structural conformance.
   - **Coverage:** every source disposition appears in the bundle or source map, with exclusions and conflicts explicit.
   - **Wayfinding:** every concept is indexed, descriptions discriminate, directories disclose their contents, and internal links resolve. Broken links are conformant but remain quality defects when the target should exist.
   - **Integrity:** on conversion, recompute every source digest against the pre-write manifest, require the same paths and bytes, and confirm no source path entered the bundle. On both branches, check for invented claims, fabricated trust signals, accidental secrets, or lost unknown metadata.
   - **Retrieval:** load `query-okf` and answer the representative questions index-first. Improve the bundle when an answer needs broad searching, excessive concept reads, or source guesswork.

   Complete when there are zero conformance failures, zero unresolved field-contract defects, zero unaccounted useful claims, zero orphan concepts, conversion sources are byte-for-byte unchanged, and each representative question is answered by a short, source-backed route or recorded as a genuine knowledge gap.

6. **Report the result.** Give the source and bundle paths, concept and Markdown-source counts, unconverted non-Markdown files, exclusions and unresolved conflicts, conformance result, quality defects intentionally left open, and retrieval questions tested. On conversion, state explicitly that the original sources were unchanged and verified against the manifest.

   Complete when the user can locate the bundle, understand its trust limits, and reproduce the audit.
