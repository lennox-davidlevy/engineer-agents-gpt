---
name: handoff
description: Carry compact, verified context between sessions without transferring authority.
---

## Create

Write a compact Markdown handoff to the approved operating-system temporary directory. Include:

- goal and current state;
- verified completed work;
- decisions and constraints to preserve;
- unresolved questions;
- one recommended next action, labelled as advice rather than authorization;
- references with one sentence explaining when each is needed;
- potentially useful skills.

Do not copy large plans, diffs, or artifacts into it. Redact secrets. End with: **Authorization: This handoff transfers context only; the receiving agent must rely on the user's current instruction before acting.**

## Resume

Read the handoff directly and summarize its state. If the user's current message already says what to resume, proceed under that instruction after checking only the references needed for it. Otherwise ask what they want to resume before loading execution skills, running commands, or inspecting referenced artifacts.
