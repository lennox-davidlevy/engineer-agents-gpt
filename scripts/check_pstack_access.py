#!/usr/bin/env python3
"""Check pstack registration and permissions using the installed OpenCode API.

Run from a fresh validation project containing this setup as .opencode.
Creates local test sessions, but makes no model requests and executes no skills.
"""

import json
from pathlib import Path
import subprocess
import time
from urllib.parse import urlencode


def api(method, path, body=None):
    command = ["opencode2", "api", method, path]
    if body is not None:
        command.extend(["--data", json.dumps(body)])
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)["data"] if result.stdout.strip() else None


def main():
    location = {"directory": str(Path.cwd())}
    query = urlencode({"location[directory]": location["directory"]})
    sources = Path(__file__).resolve().parents[1] / "vendor/pstack/skills"
    expected = {f"pstack-{p.parent.name}" for p in sources.glob("*/SKILL.md")}
    if not expected:
        raise RuntimeError("Missing pstack snapshot")
    agents = ("poteto", "engineer", "design", "explore", "researcher", "reviewer", "general")
    sessions = {
        agent: api("post", "/api/session", {
            "title": f"pstack access check: {agent}", "agent": agent, "location": location,
        })
        for agent in agents
    }
    deadline = time.monotonic() + 15
    while True:
        registered = api("get", f"/api/skill?{query}")
        if expected <= {s["id"] for s in registered} or time.monotonic() >= deadline:
            break
        time.sleep(0.1)
    skills = {s["id"]: s for s in registered if s["id"].startswith("pstack-")}
    if set(skills) != expected:
        raise RuntimeError(f"Registration mismatch: missing={expected - skills.keys()}, extra={skills.keys() - expected}")
    for name, skill in skills.items():
        if not skill.get("description") or skill.get("autoinvoke") is False:
            raise RuntimeError(f"Skill not advertised when permitted: {name}")
        if Path(skill["path"]).resolve() != sources.parents[2] / "skills" / name / "SKILL.md":
            raise RuntimeError(f"Skill loaded from the wrong installation: {name}: {skill['path']}")
    for agent, session in sessions.items():
        expected_effect = "allow" if agent == "poteto" else "deny"
        for name in sorted(expected):
            result = api("post", f"/api/session/{session['id']}/permission", {
                "agent": agent, "action": "skill", "resources": [name],
            })
            if result["effect"] == "ask":
                api("post", f"/api/session/{session['id']}/permission/{result['id']}/reply", {
                    "decision": "reject",
                })
            if result["effect"] != expected_effect:
                raise RuntimeError(f"{agent}: {name}: expected {expected_effect}, got {result['effect']}")
        print(f"PASS {agent}: all {len(expected)} pstack skills {expected_effect}", flush=True)
    print(f"PASS {len(skills)} advertised wrappers and {len(agents) * len(expected)} runtime permission decisions")


if __name__ == "__main__":
    main()
