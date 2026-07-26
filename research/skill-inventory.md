# OpenCode skill inventory — 2026-07-26

## Decision

**Measure first; do not prune or consolidate now.** The reported 23 skills are not a 23-skill prompt for every agent: the current allowlists make the largest list 13, and the two overlapping grill wrappers are visible together only to `design`. There is no observed failure, so deleting or merging workflows would trade away explicit user choices for a speculative benefit, while denying more skills would trade away autonomous routing. The obsolete `disable-model-invocation` advice in `writing-great-skills` has been corrected. The remaining low-risk decision is whether the three identical communication paragraphs in `engineer` and `design` are intentionally duplicated. Do **not** extract them into a shared project instruction: that would apply to unrelated agents too.

## Verified OpenCode behavior

- Discovery is broader than this checkout: OpenCode scans config `skill(s)/**/SKILL.md`, `.claude/skills`, `.agents/skills`, configured paths, and configured remote URLs; project-compatible directories are walked upward to the worktree. Thus this inventory is the repository contribution, not necessarily the complete installed-session inventory. [Official skills docs](https://opencode.ai/docs/skills/#understand-discovery); [current source, discovery](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/skill/index.ts#L116-L175)
- On every model turn, unless the `skill` tool is disabled, OpenCode adds `<available_skills>` to the system prompt. Entries are **name, description, and location**, not `SKILL.md` bodies. It filters out skills whose evaluated `permission.skill` action is `deny`; `ask` remains listed. [Current source, system prompt](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/session/system.ts#L83-L98); [current source, filtering/formatting](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/skill/index.ts#L239-L277); [official docs](https://opencode.ai/docs/skills/#configure-permissions)
- In the model-initiated path, the full body loads only when the model calls `skill(name)`; the tool returns the body plus a base directory and up to ten sibling-file paths. A direct slash command uses the separate path below and injects the body as its command template. The body is the meaningful runtime-token cost, distinct from the small per-turn metadata cost. [Current source, skill tool](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/tool/skill.ts#L8-L58)
- A direct `/name` is a different path: the pinned current source makes **all** discovered skills commands from `Skill.all()`, injects the skill content as the command template, and does not filter that construction through the invoking agent's `permission.skill`. This corroborates the repository's OpenCode 1.18.1 observation. In those versions, allowlists control model-tool discovery and loading but do not prevent explicit user slash invocation; recheck this behavior after upgrades rather than treating it as a permanent security guarantee. [Current source, command creation](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/command/index.ts#L93-L110); [repository README](../README.md#L44-L48)
- The official docs say `name` and `description` are required, but the pinned current source accepts a skill with no description and omits such a skill from `available_skills`; it still includes it in slash-command construction. This is a real documentation/source conflict, so do not rely on description omission as a portable “user-only” feature without testing the installed OpenCode version. [Docs](https://opencode.ai/docs/skills/#write-frontmatter); [current source, optional description and formatter](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/skill/index.ts#L42-L51) [and](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/skill/index.ts#L263-L277)
- There *are* shared-instruction mechanisms, but not a per-agent include/composition mechanism in the documented Markdown-agent format: an agent file's Markdown body is its prompt; `AGENTS.md` and `opencode.json.instructions` are combined project/global instructions. Using either to deduplicate the `engineer`/`design` wording would also affect other agents. [Agents docs](https://opencode.ai/docs/agents/#markdown) [and](https://opencode.ai/docs/agents/#prompt); [Rules docs](https://opencode.ai/docs/rules/#custom-instructions)

## Repository exposure and cost

All 23 `skills/*/SKILL.md` files have the documented description metadata. Whether each is model-visible or user-invoked depends on the active agent's evaluated permission, not on that metadata. The descriptions total approximately **3.15k characters** (about 0.8k tokens before XML/name/location framing) if all are visible. Exact prompt tokens vary by tokenizer and external/global skills. Current source also discovers a built-in `customize-opencode` skill, so the installed inventory may be one higher, but the agents configured here deny or disable it, so it does not increase the table's prompt-visible counts. [Inventory frontmatter](../skills/); [built-in source](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/skill/index.ts#L29-L40) [and](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/skill/index.ts#L208-L220)

| Agent | Model-visible skills (configured count) | Description characters, approx. | Finding |
|---|---:|---:|---|
| `engineer` | 13 | 2.4k | Largest, purposeful engineering set. |
| `design` | 10 | 1.5k | Only list containing all three grill variants. |
| `all-purpose` | 4 | 0.4k | Small router/research/conversation set. |
| `worker` | 1 | 0.1k | `tdd`. |
| `modularizer` | 2 | 0.4k | `codebase-design`, `modularize`. |
| `simplifier` | 3 | 0.5k | Design/simplify/TDD. |
| `researcher` | 1 | 0.2k | `research`. |
| `debugger` | 2 | 0.3k | Diagnosis/TDD. |
| `reviewer` | 1 | 0.4k | `code-review`. |
| `explore`, `review-spec`, `review-standards` | tool disabled | 0 | No `<available_skills>` section, not merely an empty list. |

Counts are from each agent's `permission.skill` rules; root config supplies no competing skill rule. [Agent configurations](../agents/); [root config](../opencode.json#L1-L16). These are **runtime context/routing** costs only. They do not grant filesystem, shell, edit, or task authority: those permissions are separately evaluated. In the repository's tested 1.18.1 behavior and the pinned source inspected here, they also do not prevent a user slash command; recheck after upgrades. [Permissions docs](https://opencode.ai/docs/permissions/#available-permissions)

## All 23 skills, reviewed

| Area | Skills | Exposure / overlap assessment |
|---|---|---|
| Design interview | `grilling`, `grill-me`, `grill-with-docs` | `grill-me` and `grill-with-docs` are thin wrappers around `grilling`; their near-identical “relentless interview” descriptions compete in `design`'s list. They preserve meaningful direct-command choices (stateless vs domain-doc-writing), so do not merge without usage evidence. [Wrappers](../skills/grill-me/SKILL.md#L1-L6) [and](../skills/grill-with-docs/SKILL.md#L1-L6) |
| Delivery flow | `to-prd`, `to-issues`, `implement`, `tdd`, `code-review`, `triage`, `setup-matt-pocock-skills` | Coherent staged flow, but several bodies tell the model to “run `/...`”; that assumes model invocation even though the named skill may be denied to the current agent. The configured principal flows currently have the required links, but this is maintenance coupling, not a permission guarantee. [Flow router](../skills/ask-matt/SKILL.md#L12-L25); [engineer allowlist](../agents/engineer.md#L37-L51); [design allowlist](../agents/design.md#L32-L43) |
| Architecture/refactoring | `codebase-design`, `domain-modeling`, `improve-codebase-architecture`, `modularize`, `simplify`, `prototype` | Complementary scopes (vocabulary, domain decisions, survey, mechanical split, shrinking, throwaway experiment). Shared terms are deliberate, not duplicate workflows. [Descriptions](../skills/codebase-design/SKILL.md#L1-L8) [and](../skills/modularize/SKILL.md#L1-L10) |
| Investigation/context | `diagnosing-bugs`, `research`, `handoff` | Distinct diagnosis, external evidence, and session-transfer jobs. |
| Standalone/help | `ask-matt`, `teach`, `writing-great-skills`, `bro` | Human-facing utilities; `all-purpose` sees two of these (`ask-matt` and `teach`). `ask-matt` is useful as a human router rather than evidence that every skill must be model-visible. |

## Conflicts and drift

1. **Stale local doctrine (resolved):** `writing-great-skills` said `disable-model-invocation: true` made a skill invisible. Current OpenCode source does not inspect that field, so the guidance now uses per-agent `permission.skill` rules and documents the version-specific slash-command bypass instead. No repository skill used the unsupported field, so this was maintenance drift rather than a runtime defect. [Corrected guidance](../skills/writing-great-skills/SKILL.md#L10-L20); [current source](https://github.com/anomalyco/opencode/blob/7534d23551f665e65080809975b4ca5c7d63807b/packages/opencode/src/skill/index.ts#L42-L51)
2. **Duplicate doctrine (verified):** `engineer` and `design` repeat the same three user-facing communication paragraphs verbatim. This costs no cross-agent runtime duplication (only the selected agent prompt is sent), but creates maintenance drift. Because global instructions would alter every agent, retain the duplication unless a future supported per-agent prompt-composition feature is adopted. [Engineer](../agents/engineer.md#L63-L69); [design](../agents/design.md#L53-L59)
3. **Soft workflow tension (not a proven defect):** `to-prd` says “Do NOT interview” yet later requires checking test seams with the user; `grilling` forbids acting before confirmation. These can be reconciled as different phases, but are risky if loaded together. No observed failure supports a rewrite. [PRD](../skills/to-prd/SKILL.md#L6-L18); [grilling](../skills/grilling/SKILL.md#L6-L10)

## Small next steps

1. Capture one real system prompt per primary agent (and record `opencode --version` plus global/external skill roots). Verify the actual available-skill count and provider-token accounting; this resolves the installed-version and external-discovery uncertainty.
2. Decide whether to choose one owner for the three shared `engineer`/`design` paragraphs or explicitly accept the duplication.
3. Revisit the three grill descriptions only if capture/telemetry shows misrouting. A low-risk experiment is to deny the two wrappers to **model** invocation for `design`; under the tested behavior their direct slash commands remain available, but confirm that on the installed release first.

### Remaining uncertainty

- This checkout has no pinned OpenCode package/version. The local binary reported OpenCode 1.18.5 on 2026-07-26, while the README's recorded slash-command test used 1.18.1; runtime behavior beyond that test should still be checked against 1.18.5 before relying on it.
- Home/global `.claude`, `.agents`, and configured path/URL skills were not inspectable from this repository, so they may add skills, descriptions, or duplicate names in a real session.
- No usage telemetry or model-routing failure data exists here; overlap is a plausible attention cost, not evidence that consolidation improves outcomes.
