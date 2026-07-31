# Design It Twice

When the user wants alternative interfaces for a chosen deepening candidate, draft several before choosing. Based on Ousterhout's “Design It Twice”: the first plausible idea is unlikely to be the best.

Use the vocabulary in [SKILL.md](SKILL.md): **module**, **interface**, **seam**, **adapter**, and **leverage**.

## Process

### 1. Frame the problem

State the constraints every interface must satisfy, the dependency categories from [DEEPENING.md](DEEPENING.md), and a small illustrative sketch. This frames the problem without proposing a solution.

### 2. Draft independent alternatives

Draft at least three materially different interfaces in separate passes. Do not compare or combine them until every draft exists:

1. Minimize the interface: one to three entry points with maximum leverage.
2. Maximize flexibility across the known use cases.
3. Optimize the common caller so the default case is trivial.
4. When cross-seam dependencies dominate, add a ports-and-adapters alternative.

For each alternative provide:

1. The complete interface, including invariants, ordering, and errors.
2. A caller example.
3. What the implementation hides.
4. The dependency and adapter strategy.
5. Its strongest and weakest leverage.

### 3. Compare and recommend

Compare the drafts by depth, locality, and seam placement. Recommend one design or a specific hybrid and explain why it best satisfies the original constraints.
