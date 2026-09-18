#!/usr/bin/env python3
"""Check the installed V2 permission evaluator; no tested commands are executed.

Run from the temporary validation project, not the source checkout.
Creates one local test session per configured agent. Requires opencode2.
"""

import json
import pathlib
import subprocess


# Permission resources only: these strings are never passed to a shell.
DESTRUCTIVE_COMMANDS = (
    "rm -rf scratch", "rm -fr scratch", "rm file.txt", "/bin/rm -rf scratch",
    "rmdir scratch", "/bin/rmdir scratch", "unlink file.txt",
    "find scratch -type f -delete",
    "git reset --hard HEAD", "git reset HEAD~1", "git clean -fd",
    "git restore file.txt", "git checkout -- file.txt", "git checkout HEAD -- file.txt",
    "git checkout -f main", "git checkout --force main",
    "git switch -f main", "git switch --discard-changes main",
    "git checkout main -f", "git checkout main --force",
    "git switch --force main", "git switch main -f", "git switch main --force",
    "sudo true", "doas true",
    "chmod -R 777 scratch", "chmod -vR 777 scratch", "chmod --recursive 777 scratch",
    "chown -R nobody scratch", "chown --recursive nobody scratch",
    "chgrp -R staff scratch", "chgrp --recursive staff scratch",
    "dd if=/dev/zero of=disk.img", "mkfs.ext4 disk.img",
    "diskutil eraseDisk APFS test disk9", "diskutil partitionDisk disk9 GPT APFS test 100%",
    "shutdown -h now", "reboot",
    "docker rm test", "docker rmi test", "docker volume rm data",
    "docker system prune", "docker compose down", "docker compose -p test down -v",
    "docker-compose down", "podman rm test", "podman rmi test",
    "podman volume rm data", "podman system prune", "podman compose down",
)

INSPECTION_COMMANDS = (
    "set -eu", "ls -l dev/bob", "readlink dev/bob", "realpath dev/bob",
    "dev/bob --version", "node -e \"console.log('metadata')\"",
    "find dev -maxdepth 3 -type f -o -type l", "sed -n '1,120p'",
    "git diff", "git log -1", "git checkout feature", "git switch feature",
    "git checkout bug-fix", "git switch feature/add-filter",
    "chmod +x script.sh", "docker ps", "docker run --rm example-test-image",
    "podman run --rm example-test-image",
)


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
            ("shell", "python3 -c 'print(1)'", "allow" if agent in ("engineer", "design") else "deny"),
            ("shell", "set -eu\nBOB='dev/bob/bin/bob'\nls -l \"$BOB\"; readlink \"$BOB\" || true; realpath \"$BOB\"; \"$BOB\" --version\nnode -e \"console.log('metadata')\"\nfind dev -maxdepth 3 -type f -o -type l | sed -n '1,120p'", "allow" if agent in ("engineer", "design") else "deny"),
            ("edit", "smoke-check.txt", "allow" if agent == "engineer" else "ask" if agent == "design" else "deny"),
            ("shell", "git status --short", "deny" if agent == "researcher" else "allow"),
            ("shell", "git commit", "deny"),
            ("shell", "git commit -m test", "deny"),
            ("shell", "git push", "deny"),
            ("shell", "git push origin HEAD", "deny"),
            ("subagent", "general", "deny"),
            ("skill", "unknown-skill", "deny"),
        ]
        cases.extend(("shell", command, "ask" if agent in ("engineer", "design") else "deny")
                     for command in DESTRUCTIVE_COMMANDS)
        if agent in ("engineer", "design"):
            cases.extend(("shell", command, "allow") for command in INSPECTION_COMMANDS)
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
