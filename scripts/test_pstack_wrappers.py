#!/usr/bin/env python3
"""Exercise wrapper generation as a CLI against disposable installation trees."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class WrapperGeneration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pstack-wrapper-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        shutil.copy2(Path(__file__).with_name("sync_pstack_wrappers.py"), self.root / "scripts")
        self.source = self.root / "vendor/pstack/skills/recall/SKILL.md"
        self.source.parent.mkdir(parents=True)
        self.original = "---\nname: recall\ndescription: >-\n  Recall previous\n  work.\ndisable-model-invocation: true\n---\nOriginal workflow.\n"
        self.source.write_text(self.original)
        (self.root / "pstack-opencode").mkdir()
        (self.root / "pstack-opencode/history.md").write_text("Native history procedure.\n")
        self.mapping = self.root / "pstack-opencode/ports.json"
        self.mapping.write_text(json.dumps({"recall": ["history.md"]}))
        self.wrapper = self.root / "skills/pstack-recall/SKILL.md"

    def run_generator(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/sync_pstack_wrappers.py"), *args],
            capture_output=True, text=True, timeout=10,
        )

    def test_ported_entry_point_preserves_source_and_checks_drift(self):
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.wrapper.read_text()
        self.assertIn("name: pstack-recall", text)
        self.assertIn("opencode/autoinvoke: true", text)
        self.assertIn("description: >-\n  Recall previous\n  work.", text)
        self.assertIn("../../pstack-opencode/history.md", text)
        self.assertIn("skills/recall/SKILL.md", text)
        self.assertIn("native port instructions above, which take precedence", text)
        self.assertEqual(self.source.read_text(), self.original)
        self.assertEqual(self.run_generator("--check").returncode, 0)
        self.wrapper.write_text("stale entry point\n")
        self.assertNotEqual(self.run_generator("--check").returncode, 0)
        self.assertEqual(self.wrapper.read_text(), "stale entry point\n")

    def test_invalid_port_references_fail_before_writing(self):
        outside = self.root / "outside.md"
        outside.write_text("Not a port.\n")
        for mapping in (
            {"recall": ["missing.md"]},
            {"recall": ["../outside.md"]},
            {"unknown-skill": ["history.md"]},
        ):
            with self.subTest(mapping=mapping):
                self.mapping.write_text(json.dumps(mapping))
                result = self.run_generator()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.wrapper.exists())
                self.assertEqual(self.source.read_text(), self.original)

    def test_unported_skill_still_loads_original(self):
        self.mapping.write_text("{}")
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.wrapper.read_text()
        self.assertIn("skills/recall/SKILL.md", text)
        self.assertNotIn("pstack-opencode/history.md", text)


if __name__ == "__main__":
    unittest.main()
