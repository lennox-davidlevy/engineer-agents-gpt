---
name: modularize
description: Split a monolithic file into concept-sized modules in separate files — mapped, planned, then moved mechanically with no rewrites.
disable-model-invocation: true
---

# Modularize

Take a monolithic file — the 1400-line file with 20 components in it — and split it into modules a human can read, understand, and change one at a time. This is a **mechanical move, not a rewrite**: code changes address, not behaviour or shape.

Use the `/codebase-design` vocabulary: each new file should be a **module** with a small **interface**, grouped by concept. The failure mode on both sides: one giant file is unreadable, but 40 one-export files are dust — shallow modules. Aim for files a human can read in one sitting, each owning one concept.

## Process

### 1. Map

The user names the file (or files). Inventory it:

- Every top-level declaration — components, functions, types, constants — and roughly how many lines each occupies.
- The internal dependency sketch: which declarations use which. This decides what can move together and what must move first.
- What's exported today — that's the file's current interface, and it must survive the split unchanged (re-exports are fine).

### 2. Plan the layout

Propose a file layout, grouping declarations **by concept, not by kind** — `invoice-table.tsx` holding the table, its row, and its private helpers beats `components.ts` / `helpers.ts` / `types.ts` buckets. Name files using the domain language in `CONTEXT.md` where it exists.

Present the plan as a table: new file → declarations it receives → what it exports. Flag anything shared by several groups (candidates for a small shared module) and anything that looks dead (candidate for deletion — but ask, don't decide).

Get the user's approval before moving anything.

### 3. Move mechanically

One module at a time:

1. Create the new file, move the declarations, fix imports at every call site.
2. Keep the original file re-exporting moved names if external callers import from it — killing those re-exports is a follow-up, not part of this job.
3. Run typecheck (and tests, if present) after **each** move — stay green between moves, so any breakage points at exactly one move.

Move, don't improve. If you spot code begging to be simplified or redesigned, note it for the report and suggest the user run `/simplify` after — changing it mid-move hides which change broke what.

### 4. Finish

Done when every planned move has landed, the original file either is gone or holds exactly one remaining concern, and typecheck/tests pass. Report the final layout, the re-exports left behind for compatibility, and the improvement notes you deferred.
