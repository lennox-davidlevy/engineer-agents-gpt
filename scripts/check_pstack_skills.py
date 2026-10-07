#!/usr/bin/env python3
"""Validate the native pstack bundle without a vendor tree or OpenCode service."""

import argparse
from pathlib import Path
import re
import sys


def check(root):
    errors = []
    entries = sorted((root / "skills").glob("pstack-*/SKILL.md"))
    if not entries:
        return ["No native pstack skills found"]
    if not (root / "skills/PSTACK-LICENSE").is_file():
        errors.append("Missing skills/PSTACK-LICENSE")
    for entry in entries:
        text = entry.read_text()
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f"{entry.relative_to(root)}: missing frontmatter")
            continue
        metadata, body = parts[1:]
        if not re.search(rf"^name: {re.escape(entry.parent.name)}\s*$", metadata, re.M):
            errors.append(f"{entry.relative_to(root)}: name must match the skill ID")
        if not re.search(r"^description: \S", metadata, re.M):
            errors.append(f"{entry.relative_to(root)}: missing description")
        if re.search(r"disable-model-invocation:\s*true|opencode/autoinvoke:\s*false", metadata):
            errors.append(f"{entry.relative_to(root)}: skill hidden from discovery")
        if not body.strip():
            errors.append(f"{entry.relative_to(root)}: empty skill body")
        for path in entry.parent.rglob("*.md"):
            text = path.read_text()
            label = path.relative_to(root)
            for obsolete in ("vendor/pstack", "pstack-opencode/", "sync_pstack_wrappers", "Then read `skills/"):
                if obsolete in text:
                    errors.append(f"{label}: obsolete runtime dependency {obsolete}")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                target = target.split("#", 1)[0]
                if any(char in target for char in "<>*"):
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to((root / "skills").resolve()) or not resolved.exists():
                    errors.append(f"{label}: unresolved bundled link {target}")
            for target in re.findall(r"`((?:references|playbooks|scripts)/[^`\s]+)`", text):
                if any(char in target for char in "<>*"):
                    continue
                if not (entry.parent / target).exists():
                    errors.append(f"{label}: missing skill resource {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    errors = check(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS {len(list((root / 'skills').glob('pstack-*/SKILL.md')))} native skills and bundled references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
