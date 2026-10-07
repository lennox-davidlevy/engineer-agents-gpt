#!/usr/bin/env python3
"""Check pstack registration and permissions using the installed OpenCode API.

Run from a fresh validation project containing this setup as .opencode.
Creates local test sessions and activates two skills with resume=false.
Makes no model requests and executes no workflows.
"""

import json
from pathlib import Path
import subprocess
import tempfile
import time
from urllib.parse import urlencode


def api(method, path, body=None):
    command = ["opencode2", "api", method, path]
    if body is not None:
        command.extend(["--data", json.dumps(body)])
    # V2.0.23 can exit before large piped stdout finishes flushing.
    with tempfile.TemporaryFile(mode="w+") as output:
        subprocess.run(command, check=True, stdout=output, stderr=subprocess.PIPE, text=True, timeout=30)
        output.seek(0)
        text = output.read()
    return json.loads(text)["data"] if text.strip() else None


def main():
    location = {"directory": str(Path.cwd())}
    query = urlencode({"location[directory]": location["directory"]})
    sources = Path(__file__).resolve().parents[1] / "skills"
    expected = {p.parent.name for p in sources.glob("pstack-*/SKILL.md")}
    if not expected:
        raise RuntimeError("Missing native pstack skills")
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
        if Path(skill["path"]).resolve() != sources / name / "SKILL.md":
            raise RuntimeError(f"Skill loaded from the wrong installation: {name}: {skill['path']}")
        body = (sources / name / "SKILL.md").read_text().split("---", 2)[2].strip()
        if skill["content"].strip() != body:
            raise RuntimeError(f"Registered body does not match the native skill: {name}")
    for agent, session in sessions.items():
        expected_effect = "allow" if agent == "poteto" else "deny"
        for name in sorted(expected):
            result = api("post", f"/api/session/{session['id']}/permission", {
                "agent": agent, "action": "skill", "resources": [name],
            })
            if result["effect"] == "ask":
                api("post", f"/api/session/{session['id']}/permission/{result['id']}/reply", {
                    "reply": "reject",
                })
            if result["effect"] != expected_effect:
                raise RuntimeError(f"{agent}: {name}: expected {expected_effect}, got {result['effect']}")
        print(f"PASS {agent}: all {len(expected)} pstack skills {expected_effect}", flush=True)
    session_id = sessions["poteto"]["id"]
    for name in ("pstack-poteto-mode", "pstack-how"):
        api("post", f"/api/experimental/session/{session_id}/skill", {"id": name, "resume": False})
    messages = api("get", f"/api/session/{session_id}/message")
    loaded = {message["skill"]: message["text"] for message in messages if message["type"] == "skill"}
    for name, marker in (("pstack-poteto-mode", "## Principles"), ("pstack-how", "## Step 1. Assess Complexity")):
        if marker not in loaded.get(name, "") or "vendor/pstack" in loaded[name]:
            raise RuntimeError(f"Skill activation did not load the native workflow: {name}")
    print("PASS native mode and how skill activation; no model requests")
    print(f"PASS {len(skills)} advertised native skills and {len(agents) * len(expected)} runtime permission decisions")


if __name__ == "__main__":
    main()
