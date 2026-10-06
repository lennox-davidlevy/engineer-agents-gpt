---
name: pstack-architect
description: "Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape."
metadata:
  opencode/autoinvoke: true
---

Resolve this skill's base directory through symlinks with `realpath` if needed.
From that resolved directory, the pstack root is `../../vendor/pstack`.
Read `OPENCODE.md` at that root first. It overrides Cursor-specific instructions.
Read `../../pstack-opencode/models.md` from this resolved wrapper directory.
Read `../../pstack-opencode/delegation.md` from this resolved wrapper directory.
Then read `skills/architect/SKILL.md` at that root in full. Follow it subject to
the OpenCode adapter and native port instructions above, which take precedence.
Resolve the original skill's references and scripts relative to its directory,
not this wrapper. Load other pstack skills through their `pstack-<name>` IDs.
Do not replace the original instructions with this entry point. If the bundle
is missing, report the installation problem instead of using another skill.
