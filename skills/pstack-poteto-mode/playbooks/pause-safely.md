### Pause safely

**You own a clean stop. Leave a checkpoint a cold-start agent can resume from.** This is explicit only. On "keep going", "going to bed, keep going", or "don't stop", do not pause.

1. Stop at a safe boundary. Finish the current atomic step and start nothing new. Stop owned background work only through an available supported control. Otherwise record its ID and actual status; do not invent cancellation.
2. Take no irreversible action to pause. Never commit or push. Do not discard uncommitted work.
3. Preserve the working tree and record the exact directory, branch, changed files, checks, evidence, active process or delegate IDs, and blockers. State whether the tree is runnable. A scratch file is not guaranteed to survive reboot.
4. Write the resume note off-context. Capture intent, what you were doing, progress and what's verified, current state, next steps, key files, and gotchas. For the compaction trigger write it to a file like `/tmp/opencode/<slug>-resume.md`. If a show-me-your-work trail exists, point at it instead of duplicating it.

**Reply:** where you stopped, checkpoint path, working-tree state, active work,
and the first action on resume. This is a pause, not a final report.
