---
name: pstack-principle-encode-lessons-in-structure
description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
metadata:
  opencode/autoinvoke: true
---

Resolve this skill's base directory through symlinks with `realpath` if needed.
From that resolved directory, the pstack root is `../../vendor/pstack`.
Read `OPENCODE.md` at that root first. It overrides Cursor-specific instructions.
Then read `skills/principle-encode-lessons-in-structure/SKILL.md` at that root in full. Follow it subject to
the OpenCode adapter and native port instructions above, which take precedence.
Resolve the original skill's references and scripts relative to its directory,
not this wrapper. Load other pstack skills through their `pstack-<name>` IDs.
Do not replace the original instructions with this entry point. If the bundle
is missing, report the installation problem instead of using another skill.
