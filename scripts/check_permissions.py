#!/usr/bin/env python3
"""Check the installed V2 permission evaluator; no tested commands are executed.

Run from the temporary validation project, not the source checkout.
Creates one local test session per configured agent. Requires opencode2.
"""

import json
import pathlib
import subprocess


def api(method, path, body):
    result = subprocess.run(
        ["opencode2", "api", method, path, "--data", json.dumps(body)],
        check=True, capture_output=True, text=True, timeout=30,
    )
    return json.loads(result.stdout)["data"] if result.stdout.strip() else None


def main():
    count = 0
    for agent in ("engineer", "design", "researcher", "explore", "reviewer"):
        session = api("post", "/api/session", {
            "title": f"Permission smoke test: {agent}",
            "agent": agent,
            "location": {"directory": str(pathlib.Path.cwd())},
        })
        cases = [
            ("execute", "*", "deny" if agent == "explore" else "allow"),
            ("browser", "*", "allow" if agent in ("engineer", "design") else "deny"),
            ("websearch", "React useState official documentation", "allow" if agent in ("engineer", "design", "researcher") else "deny"),
            ("webfetch", "https://react.dev/reference/react/useState", "allow" if agent in ("engineer", "design", "researcher") else "deny"),
            ("context7_query-docs", "*", "allow" if agent in ("engineer", "researcher") else "deny"),
            ("context7_resolve-library-id", "*", "allow" if agent in ("engineer", "researcher") else "deny"),
            ("shell", "python3 -c 'print(1)'", "allow" if agent == "engineer" else "ask" if agent == "design" else "deny"),
            ("edit", "smoke-check.txt", "allow" if agent == "engineer" else "ask" if agent == "design" else "deny"),
            ("shell", "git status --short", "deny" if agent == "researcher" else "allow"),
            ("shell", "git commit", "deny"),
            ("shell", "git commit -m test", "deny"),
            ("shell", "git push", "deny"),
            ("shell", "git push origin HEAD", "deny"),
            ("subagent", "general", "deny"),
            ("skill", "unknown-skill", "deny"),
        ]
        for action, resource, expected in cases:
            result = api("post", f"/api/session/{session['id']}/permission", {
                "agent": agent, "action": action, "resources": [resource],
            })
            actual = result["effect"]
            if actual == "ask":
                api("post", f"/api/session/{session['id']}/permission/{result['id']}/reply", {"reply": "reject"})
            if actual != expected:
                raise RuntimeError(f"{agent}: {action} {resource!r}: expected {expected}, got {actual}")
            count += 1
        print(f"PASS {agent}: {len(cases)} runtime permission checks")
    print(f"PASS {count} checks; no shell, browser, web, or MCP action was executed")


if __name__ == "__main__":
    main()
