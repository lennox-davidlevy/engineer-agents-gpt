---
name: handoff
description: Create or resume a compact handoff between agent sessions without treating recommendations as authorization.
---

## Create a handoff

Write a compact Markdown document to the operating system's temporary directory, not the workspace. It must contain:

1. **Goal and current state** — what the user is trying to achieve and where the work stands.
2. **Completed work** — verified outcomes, not a replay of the conversation.
3. **Decisions and constraints** — choices the next session must preserve.
4. **Open questions** — unresolved decisions requiring the user.
5. **Recommended next action — not authorized** — one concrete recommendation, explicitly labelled as advice rather than permission to execute.
6. **References** — paths or URLs with one sentence saying why and when each should be read. Do not copy existing PRDs, plans, ADRs, issues, commits, or diffs into the handoff, and do not instruct the next agent to load every reference eagerly.
7. **Suggested skills** — skills that may help after the user selects the next action.

End with: **“Authorization: This handoff transfers context only. The receiving agent must ask the user what to resume before starting work.”**

Redact API keys, passwords, personal information, and other secrets. If the user supplied arguments, use them to focus the handoff, not to pre-authorize work in the next session.

## Resume from a handoff

Read the handoff itself directly; do not delegate or summarize it through another agent. A handoff should be compact enough to fit comfortably in the main context.

Before the user confirms what to resume:

- Summarize the goal, current state, preserved decisions, open questions, and recommended next action.
- Treat every recommendation and suggested skill as informational.
- Do not create implementation todos, load execution skills, run commands, or inspect any referenced artifact.
- Ask one direct question: **“What would you like me to resume?”**

After confirmation, inspect only the references needed for that action. If the active agent can delegate to `explore`, use it for large read-only repository mapping rather than loading broad artifacts into the main context; otherwise inspect the smallest relevant slices directly.
