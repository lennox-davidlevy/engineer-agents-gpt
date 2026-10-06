---
name: pstack-poteto-mode
description: poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /poteto-mode, or requests to work in this style.
metadata:
  opencode/autoinvoke: true
---

Resolve this skill's base directory through symlinks with `realpath` if needed.
From that resolved directory, the pstack root is `../../vendor/pstack`.
Read `OPENCODE.md` at that root first. It overrides Cursor-specific instructions.
Read `../../pstack-opencode/README.md` from this resolved wrapper directory.
Read `../../pstack-opencode/history.md` from this resolved wrapper directory.
Read `../../pstack-opencode/models.md` from this resolved wrapper directory.
Read `../../pstack-opencode/delegation.md` from this resolved wrapper directory.
Read `../../pstack-opencode/verification.md` from this resolved wrapper directory.
Read `../../pstack-opencode/local-runs.md` from this resolved wrapper directory.
Then read `skills/poteto-mode/SKILL.md` at that root in full. Follow it subject to
the OpenCode adapter and native port instructions above, which take precedence.
Resolve the original skill's references and scripts relative to its directory,
not this wrapper. Load other pstack skills through their `pstack-<name>` IDs.
Do not replace the original instructions with this entry point. If the bundle
is missing, report the installation problem instead of using another skill.
