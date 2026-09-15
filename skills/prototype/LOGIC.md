# Logic prototype

Use a logic prototype when behavior is hard to judge on paper: state transitions, ordering, data shape, concurrency, or an API's ergonomics.

- Keep the domain logic isolated enough to inspect, but do not pre-architect it for production reuse.
- Expose the important state and decisions. A small script, REPL, test harness, terminal UI, or local page is acceptable; choose the cheapest useful form.
- Drive representative happy paths and edge cases. Make assumptions visible.
- Use in-memory or disposable local data unless persistence itself is the question.
- Capture the answer and delete the harness. If some logic deserves production use, implement and test it under production constraints rather than copying it blindly.
