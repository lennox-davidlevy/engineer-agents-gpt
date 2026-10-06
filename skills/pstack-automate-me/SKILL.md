---
name: pstack-automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via create-skill + unslop, optionally pulling fresh evidence from recent transcripts."
metadata:
  opencode/autoinvoke: true
---

Resolve this skill's base directory through symlinks with `realpath` if needed.
From that resolved directory, the pstack root is `../../vendor/pstack`.
Read `OPENCODE.md` at that root first. It overrides Cursor-specific instructions.
Read `../../pstack-opencode/README.md` from this resolved wrapper directory.
Read `../../pstack-opencode/history.md` from this resolved wrapper directory.
Read `../../pstack-opencode/verification.md` from this resolved wrapper directory.
Then read `skills/automate-me/SKILL.md` at that root in full. Follow it subject to
the OpenCode adapter and native port instructions above, which take precedence.
Resolve the original skill's references and scripts relative to its directory,
not this wrapper. Load other pstack skills through their `pstack-<name>` IDs.
Do not replace the original instructions with this entry point. If the bundle
is missing, report the installation problem instead of using another skill.
