---
name: prototype
description: Build a disposable artifact to answer one uncertain design question.
---

A prototype buys evidence, not production code.

1. State the question and the observation that would answer it. If the question can be settled cheaply from existing evidence, do that instead of building.
2. Choose the smallest artifact that exposes the uncertainty. For state or interaction logic, read [LOGIC.md](LOGIC.md). For visual hierarchy or workflow alternatives, read [UI.md](UI.md). Neither branch is mandatory when a smaller script, sketch, or spike suffices.
3. Mark the artifact as temporary, keep it inside the active repository, avoid production data and external side effects, and provide one clear way to run or view it.
4. Skip production hardening that does not affect the question. Add tests only when repeatability is necessary to trust the experiment.
5. Record what was learned. Delete the artifact or deliberately rebuild the chosen behavior to production standards; do not silently promote prototype code.
