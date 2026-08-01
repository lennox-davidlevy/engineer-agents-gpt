---
name: okf
description: Read and traverse an OKF knowledge bundle. Use when the user points at an OKF bundle, knowledge bundle, or a documentation directory written in the Open Knowledge Format.
---

An OKF bundle is a directory of markdown files. Each file is one concept, carries YAML frontmatter, and links to other concepts with normal markdown links. Read it by navigation, not by bulk.

## Traverse

1. Read `index.md` at the bundle root. It lists every concept with a one-line description, grouped into sections. If it is missing, list the directory and read frontmatter only.
2. Choose the concepts that match the question from those descriptions. Do not open a concept because it might be relevant.
3. Read the chosen concepts. Follow their in-body links only when the current concept does not answer the question.
4. Descend into a subdirectory by reading its own `index.md` first.
5. Stop when the question is answered. Report which concepts you read.

Never glob or read the whole bundle. The index exists so you do not have to. If you find yourself opening more than five or six concepts for one question, say so — either the question is too broad or the bundle needs a better index.

## Frontmatter

`type` is the only field guaranteed to be present. Use it to route: a `Configuration` concept answers "how do I set this up", a `Concept` answers "how does this work", a `Reference` answers "what are the valid values".

Tolerate anything unexpected. Unknown types, unknown keys, missing optional fields, and broken links are all valid. Never reject or flag a concept for them.

## Trust

These fields are optional and their absence is meaningful. Read them before you rely on a concept.

| Field | Meaning |
|---|---|
| `generated: { by, at }` | Who wrote the content and when it last changed. |
| `verified: [{ by, at }]` | Who confirmed it. May be a bare mapping; treat it as a one-element list. |
| `status` | `draft`, `stable`, or `deprecated`. Absent means `stable`. |
| `stale_after` | A date. The concept is stale when today is on or after it. |
| `sources` | What the content was derived from, each with an optional `id`. |

Derive a trust tier from `verified`:

- No `verified` key — **unverified**
- `verified` by non-`human:` actors only — **machine-confirmed**
- `verified` by a `human:<id>` actor — **human-reviewed**

Actors read as `human:<id>` for a person, `process:<id>` for an automated process, and `<producer>/<version>` for an agent or tool.

## Report trust with the answer

When an answer rests on a concept that is unverified, `draft`, `deprecated`, or past its `stale_after`, say so in one line next to the claim it supports. Name the concept and the reason.

> Custom subagents live in `.bob/agents/*.md`. — from `custom-subagents.md`, draft and unverified, derived from the product source rather than published documentation.

Do not bury this in a footer, and do not withhold the answer over it. It is a caveat on a claim, not a refusal.

Prefer a human-reviewed concept over an unverified one when they conflict. When a stale concept contradicts a fresh one, follow the fresh one and report the contradiction — a stale page that disagrees with a current page is a finding worth surfacing to the user.

## Attributed claims

A markdown footnote whose label matches a `sources[].id` attributes that specific claim to that source:

```markdown
The `events_` table is sharded daily.[^ga4-schema]
```

Resolve attribution through the matching `sources` entry, not by reading the footnote text. When a claim carries a footnote, cite the underlying source rather than the concept.

## Reserved files

`index.md` is a directory listing and `log.md` is a change history. Neither is a concept. Read `log.md` when you need to know what recently changed or what the bundle's authors know is missing; skip it otherwise.

## Do not write

This skill reads. Do not add frontmatter, create index files, or edit concepts unless the user asks for that separately.
