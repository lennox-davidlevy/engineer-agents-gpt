#!/usr/bin/env python3
"""Exercise the bundle validator through its CLI on disposable native installs."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class NativeBundleValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pstack-native-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills/pstack-example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        (self.root / "skills/PSTACK-LICENSE").write_text("Fixture license\n")
        self.skill.write_text("---\nname: pstack-example\ndescription: Example workflow\n---\n# Example\n\nRead [details](references/details.md).\n")
        self.reference = self.skill.parent / "references/details.md"
        self.reference.parent.mkdir()
        self.reference.write_text("Use the real public interface.\n")

    def run_check(self):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("check_pstack_skills.py")), str(self.root)],
            capture_output=True, text=True, timeout=10,
        )

    def test_native_install_needs_no_vendor_or_generator(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "PASS 1 native skills and bundled references\n")

    def test_missing_resource_reports_the_broken_link(self):
        self.reference.unlink()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved bundled link references/details.md", result.stderr)

    def test_pointer_wrapper_is_rejected(self):
        self.skill.write_text("---\nname: pstack-example\ndescription: Example\n---\nRead ../../vendor/pstack/skills/example/SKILL.md\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("obsolete runtime dependency vendor/pstack", result.stderr)

    def test_hidden_skill_is_rejected(self):
        self.skill.write_text(self.skill.read_text().replace("description: Example workflow", "description: Example workflow\ndisable-model-invocation: true"))
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("skill hidden from discovery", result.stderr)


if __name__ == "__main__":
    unittest.main()
