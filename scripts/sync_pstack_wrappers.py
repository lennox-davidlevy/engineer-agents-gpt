#!/usr/bin/env python3
"""Generate OpenCode entry points without changing the upstream snapshot."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def render(source, ports):
    lines = source.read_text().splitlines()
    if lines[0] != "---":
        raise ValueError(f"Missing frontmatter: {source}")
    frontmatter = lines[1:lines.index("---", 1)]
    start = next(i for i, line in enumerate(frontmatter) if line.startswith("description:"))
    end = start + 1
    while end < len(frontmatter) and (
        not frontmatter[end].strip() or frontmatter[end][0].isspace()
    ):
        end += 1
    description = "\n".join(frontmatter[start:end]).rstrip()
    name = source.parent.name
    native = "".join(
        f"Read `../../pstack-opencode/{path}` from this resolved wrapper directory.\n"
        for path in ports.get(name, [])
    )
    return f"""---
name: pstack-{name}
{description}
metadata:
  opencode/autoinvoke: true
---

Resolve this skill's base directory through symlinks with `realpath` if needed.
From that resolved directory, the pstack root is `../../vendor/pstack`.
Read `OPENCODE.md` at that root first. It overrides Cursor-specific instructions.
{native}Then read `skills/{name}/SKILL.md` at that root in full. Follow it subject to
the OpenCode adapter and native port instructions above, which take precedence.
Resolve the original skill's references and scripts relative to its directory,
not this wrapper. Load other pstack skills through their `pstack-<name>` IDs.
Do not replace the original instructions with this entry point. If the bundle
is missing, report the installation problem instead of using another skill.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report drift without writing files")
    args = parser.parse_args()
    sources = sorted((ROOT / "vendor/pstack/skills").glob("*/SKILL.md"))
    if not sources:
        raise SystemExit("Missing pstack snapshot")
    port_root = ROOT / "pstack-opencode"
    ports = json.loads((port_root / "ports.json").read_text())
    if not isinstance(ports, dict) or set(ports) - {p.parent.name for p in sources}:
        raise SystemExit("Port map must contain only existing upstream skill IDs")
    for paths in ports.values():
        if not isinstance(paths, list) or not paths:
            raise SystemExit("Each port entry must be a nonempty list of Markdown paths")
        for path in paths:
            if not isinstance(path, str) or Path(path).suffix != ".md":
                raise SystemExit(f"Invalid port path: {path!r}")
            target = (port_root / path).resolve()
            if not target.is_relative_to(port_root.resolve()) or not target.is_file():
                raise SystemExit(f"Missing or out-of-bundle port: {path}")
    expected = {ROOT / "skills" / f"pstack-{p.parent.name}" / "SKILL.md": render(p, ports) for p in sources}
    stale = set((ROOT / "skills").glob("pstack-*/SKILL.md")) - expected.keys()
    if stale:
        raise SystemExit("Stale wrappers require review: " + ", ".join(str(p) for p in sorted(stale)))
    changed = [p for p, text in expected.items() if not p.exists() or p.read_text() != text]
    if args.check and changed:
        raise SystemExit("Wrapper drift: " + ", ".join(str(p.relative_to(ROOT)) for p in changed))
    for path in changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected[path])
    print(f"{len(expected)} pstack wrappers checked; {len(changed)} written")


if __name__ == "__main__":
    main()
