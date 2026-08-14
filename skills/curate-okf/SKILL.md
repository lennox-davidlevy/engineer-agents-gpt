---
name: curate-okf
description: Create or update an OKF v0.2 bundle in place from a directory of Markdown documentation.
---

Turn a current, possibly messy Markdown corpus into durable concepts that an unfamiliar agent can find, trust, and use. Target OKF v0.2. The bundle is malleable: organize it for retrieval rather than preserving the source layout mechanically.

## Modes

- **Create** when the target directory contains raw or irregular Markdown rather than a usable bundle. Curate that directory in place unless the user names another destination.
- **Update** when the target is already an OKF bundle and its Markdown has been added, replaced, or deleted to reflect newer documentation. Reconcile the current corpus with the existing organization.

A mixed or temporarily malformed directory is valid input. Do not require a second untouched source tree, a digest manifest, or a permanent source map. The current Markdown is the evidence to curate. Every non-reserved `.md` file below the bundle root becomes a concept; non-Markdown files are outside this skill's input contract.

Follow the host's write and command authorization rules. Pause when a material decision cannot be inferred safely, including suspected secrets, conflicting authoritative claims, an ambiguous bundle boundary, or multiple plausible audiences.

## Process

1. **Establish the current corpus.** Confirm the bundle root, intended audience, and the questions the documentation should answer. Inventory every Markdown file and substantive section. Inspect existing indexes and frontmatter before reading bodies; when Git history is available, use the current diff as evidence of additions, replacements, deletions, and renames, but do not require Git. List non-Markdown files as unsupported rather than silently extracting from them.

   Complete when every input is accounted for and material ambiguity is resolved.

2. **Build the coverage map.** Map every substantive source section to one or more target concepts. Consolidate repetition, preserve contradictory or version-specific guidance with attribution, and exclude only empty, purely navigational, redundant, or boilerplate material with a concrete reason. Generated documentation is evidence when it contains unique knowledge; never exclude it merely because a tool produced it. For an update, give each existing concept a disposition such as keep, revise, split, merge, move, or remove. Decompose by durable meaning—an asset, idea, decision, procedure, contract, or computation—not mechanically by heading or length.

   Complete when every substantive section is represented, every exclusion is justified, and every proposed concept has a distinct purpose.

3. **Design for retrieval.** Derive representative user questions from the corpus. Choose a small, self-explanatory type vocabulary; plan shallow directories, concise titles and descriptions, useful indexes, and prose links whose surrounding text names the relationship. Preserve an existing concept ID—the file path without `.md`—when the concept still means substantially the same thing. Rename, split, or merge only when the old organization materially harms retrieval, then repair every affected link.

   Complete when every concept is discoverable, sibling descriptions are distinguishable, stable IDs are preserved where useful, and each representative question has a short planned route.

4. **Curate in place.** Before writing, read [`CONFORMANCE.md`](CONFORMANCE.md) and apply every applicable v0.2 rule. Normally give each concept `type`, `title`, and `description`; add `resource`, tags, provenance, trust, and lifecycle metadata only when the evidence supports them. Never invent verification, freshness, authority, source identity, or credibility. Preserve unknown frontmatter on retained concepts. If content changes materially, refresh truthful generation metadata and remove verification that no longer covers the current text.

   Keep paths stable by default. New or replacement raw Markdown may be rewritten, moved, split, or merged when needed for coherent concepts. Update root and directory indexes, repair internal links, and update `log.md` when one exists. Do not create bookkeeping concepts that do not help a future consumer answer questions.

   Complete when the planned concepts, indexes, and links exist; every retained claim is supported by the current corpus; and no path or metadata changed merely for uniformity.

5. **Validate mechanically.** Locate `scripts/validate_okf.py` beside this skill and run:

   ```sh
   uv run <skill-dir>/scripts/validate_okf.py <bundle-dir>
   ```

   Fix every conformance error. Resolve quality warnings when they identify a real producer defect; OKF consumers tolerate missing indexes and broken links, but a bundle curated for retrieval should not leave its own concepts unreachable. The validator checks structure, not coverage or truth.

   Complete when the validator reports zero errors and every remaining warning is understood and justified.

6. **Test retrieval.** Load `query-okf` and answer the representative questions index-first. Improve the bundle when answers require broad searching, ambiguous index entries, unnecessary concept reads, or unsupported inference.

   Complete when each representative question has a short, source-backed route or exposes a genuine knowledge gap.

7. **Report the result.** Give the bundle path, mode, concept count, unsupported files, exclusions, conflicts, preserved and changed concept IDs, validator result, remaining quality warnings, and retrieval questions tested.

   Complete when the user can locate the bundle, understand what changed and its trust limits, and reproduce the validation.
