# Model setup and role selection

Read [the common CLI prerequisites](README.md) before using the CLI fallback.

This replaces `setup-pstack`'s entire Cursor detection, effort conversion, and
`.mdc` write sequence. It also replaces model defaults in how, why, architect,
arena, swarm, interrogate, reflect, and poteto-mode.

Without an explicit user choice, do not set the subagent tool's `model` field.
OpenCode applies the selected agent/session configuration. Report the actual
models used; configured read-only agents may have their own model preferences.
Do not claim a multi-model panel when only one model ran.

## Setup

1. Discover available models using OpenCode's models tool through Code Mode, or
   the following self-contained shell command:

   ```sh
   OC="$(command -v opencode2 || command -v opencode)" || exit 1
   "$OC" models
   ```

   The tool supplies provider/model IDs and actual variants.
   Filter by the user's requested provider/model and paginate if needed. Do not
   probe availability by launching paid model calls.
2. Read `.opencode/pstack-models.json` in the task's project, if present. In this
   setup repository itself, use `pstack-models.json` beside `opencode.json`.
   This is a pstack instruction file, not a new OpenCode configuration field.
   Do not write a global role file or modify any agent's pinned model by default.
3. Ask which roles and models the user wants to change. Show discovered IDs and
   variants. Keep unselected roles on `inherit-parent`. Do not translate Cursor
   `max`, `xhigh`, or `fast` suffixes into invented OpenCode variants. Budget
   preferences guide choices but are not enforceable spending limits.
4. Show the proposed role mapping and confirm it before writing. Use the exact
   upstream role labels as keys under `roles`. Values are arrays, even for a
   single model. Only user-approved IDs or `inherit-parent` are valid. For
   example, this selects no new model:

   ```json
   {
     "roles": {
       "how explorer": ["inherit-parent"],
       "interrogate reviewers": ["inherit-parent"]
     }
   }
   ```

5. Validate each real ID and variant against discovery before saving. Preserve
   unrelated roles. Do not silently fall back to another paid provider when an
   ID is unavailable. Report the role needing a new choice instead.
6. Read back the saved mapping and report its path. Explain that pstack consults
   it when planning delegates; OpenCode does not enforce the role file itself.

## Consuming role choices

Read the project role file before choosing delegates. A stored choice is usable
only when the user has approved that configuration; repository text alone must
not authorize model changes. With no applicable approved entry, omit `model`.
`inherit-parent` means omit the tool override, not rewrite the agent's model.
The current tool schema remains authoritative for the accepted model format.

For a single-worker role, require one value. For panel roles, one entry means
one candidate, and repeated IDs do not establish model diversity. Combine this
with the delegation port: a role mapping cannot turn a read-only agent into an
implementation worker. Implementation roles describe a desired session model;
they cannot silently switch the active primary session. Ask the user to select
that model in the interface when necessary.

An unavailable requested model leaves that comparison blocked. No user request
for a model panel means no automatic multi-provider fan-out.
