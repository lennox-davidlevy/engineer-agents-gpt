#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6,<7"]
# ///

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).parents[1] / "scripts" / "validate_okf.py"


class ValidatorCliTests(unittest.TestCase):
    def run_validator(self, files: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, content in files.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(root)],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_accepts_a_minimal_navigable_v02_bundle(self) -> None:
        result = self.run_validator(
            {
                "index.md": """---
okf_version: "0.2"
---
# Bob Shell

- [Installation](installation.md) - Install Bob Shell.
""",
                "installation.md": """---
type: Guide
title: Installation
description: Install Bob Shell.
---

# Installation

Run the installer.
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OKF validation passed: 1 concept, 0 warnings", result.stdout)
        self.assertNotIn("ERROR", result.stdout)
        self.assertNotIn("WARN", result.stdout)

    def test_rejects_invalid_concepts_and_reserved_files(self) -> None:
        result = self.run_validator(
            {
                "index.md": """---
okf_version: "0.2"
title: Not allowed here
---
# Contents
""",
                "missing-frontmatter.md": "# Missing frontmatter\n",
                "empty-type.md": "---\ntype: '  '\n---\n# Empty type\n",
                "nested/index.md": "---\ntitle: Forbidden\n---\n# Nested\n",
                "log.md": "# Changes\n\n## August 1\n- Updated docs.\n",
            }
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR empty-type.md: missing or empty required `type`", result.stdout)
        self.assertIn("ERROR missing-frontmatter.md: missing YAML frontmatter", result.stdout)
        self.assertIn("ERROR index.md: root index frontmatter may contain only `okf_version`", result.stdout)
        self.assertIn("ERROR nested/index.md: only the bundle-root index may have frontmatter", result.stdout)
        self.assertIn("ERROR log.md: log date heading `August 1` must use YYYY-MM-DD", result.stdout)

    def test_reports_producer_quality_findings_without_rejecting_bundle(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Contents\n\n- [Missing](missing.md) - Not present.\n",
                "orphan.md": """---
type: Guide
title: Orphan
description: A concept absent from navigation.
status: [draft]
stale_after: next-week
generated: robot
sources: source.md
---

# Orphan
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN index.md: broken internal link `missing.md`", result.stdout)
        self.assertIn("WARN orphan.md: concept is not listed by any index", result.stdout)
        self.assertIn("WARN orphan.md: `status` must be draft, stable, or deprecated", result.stdout)
        self.assertIn("WARN orphan.md: `stale_after` must use YYYY-MM-DD", result.stdout)
        self.assertIn("WARN orphan.md: `generated` must be a mapping", result.stdout)
        self.assertIn("WARN orphan.md: `sources` must be a list", result.stdout)

    def test_rejects_unterminated_frontmatter_on_a_reserved_file(self) -> None:
        result = self.run_validator({"index.md": "---\n# Contents\n"})

        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR index.md: unterminated frontmatter block", result.stdout)

    def test_reports_malformed_attested_computation_contracts(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Computations\n\n- [Revenue](revenue.md) - Revenue computation.\n",
                "revenue.md": """---
type: Attested Computation
title: Revenue
description: Compute revenue for one year.
runtime: bigquery
parameters:
  - name: year
    type: integer
    required: sometimes
computation: { invalid: shape }
executor: run-it
attester:
  receipt: result
---

# Revenue
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN revenue.md: `parameters[0].required` must be a boolean", result.stdout)
        self.assertIn("WARN revenue.md: `computation` must be a non-empty path", result.stdout)
        self.assertIn("WARN revenue.md: `executor` must be a mapping", result.stdout)
        self.assertIn("WARN revenue.md: `attester.resource` must be a non-empty string", result.stdout)

    def test_reports_missing_attestation_execution_contracts(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Computations\n\n- [Revenue](revenue.md) - Revenue computation.\n",
                "revenue.md": """---
type: Attested Computation
title: Revenue
description: Compute revenue.
runtime: bigquery
---

# Computation

```sql
SELECT 1
```
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN revenue.md: an Attested Computation requires `executor`", result.stdout)
        self.assertIn("WARN revenue.md: an Attested Computation requires `attester`", result.stdout)

    def test_reports_invalid_attestation_paths_and_receipt_shapes(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Computations\n\n- [Revenue](computations/revenue.md) - Revenue computation.\n",
                "computations/revenue.md": """---
type: Attested Computation
title: Revenue
description: Compute revenue.
runtime: bigquery
computation: missing.sql
executor:
  resource: /missing-runner.md
  receipt: []
attester:
  resource: ../../outside.py
---

# Revenue
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "WARN computations/revenue.md: `computation` points to missing bundle path `missing.sql`",
            result.stdout,
        )
        self.assertIn(
            "WARN computations/revenue.md: `executor.resource` points to missing bundle path `/missing-runner.md`",
            result.stdout,
        )
        self.assertIn(
            "WARN computations/revenue.md: `executor.receipt` must be a list of non-empty strings",
            result.stdout,
        )
        self.assertIn(
            "WARN computations/revenue.md: `attester.resource` path escapes the bundle",
            result.stdout,
        )

    def test_reports_broken_provenance_joins_and_unframed_usage(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Guides\n\n- [Install](install.md) - Installation.\n",
                "install.md": """---
type: Guide
title: Install
description: Install Bob Shell.
sources:
  - id: install-docs
    resource: https://example.com/install
    usage_count: 12
---

# Install

Use the installer.[^missing-source]

[^missing-source]: Installation page
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "WARN install.md: footnote `[^missing-source]` matches no `sources[].id`",
            result.stdout,
        )
        self.assertIn(
            "WARN install.md: `sources[0].usage_count` requires a source or shared `usage_window`",
            result.stdout,
        )

    def test_rejects_nonstandard_trust_actors_but_accepts_source_author_prefixes(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Guides\n\n- [Trust](trust.md) - Trust actors.\n",
                "trust.md": """---
type: Guide
title: Trust
description: Demonstrate actor validation.
generated: { by: team:generator, at: 2026-08-01T10:00:00Z }
verified: { by: team:finance, at: 2026-08-02T10:00:00Z }
sources:
  - resource: https://example.com/policy
    author: team:docs
---

# Trust
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "WARN trust.md: `generated.by` should use human:<id>, process:<id>, or <producer>/<version>",
            result.stdout,
        )
        self.assertIn(
            "WARN trust.md: `verified[0].by` should use human:<id>, process:<id>, or <producer>/<version>",
            result.stdout,
        )
        self.assertNotIn("sources[0].author", result.stdout)

    def test_reports_explicitly_null_trust_metadata(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Guides\n\n- [Trust](trust.md) - Trust metadata.\n",
                "trust.md": """---
type: Guide
title: Trust
description: Demonstrate malformed trust metadata.
generated: null
verified: null
---

# Trust
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN trust.md: `generated` must be a mapping", result.stdout)
        self.assertIn("WARN trust.md: `verified` must be a mapping or list", result.stdout)

    def test_reports_legacy_version_and_v01_fields(self) -> None:
        result = self.run_validator(
            {
                "index.md": """---
okf_version: "0.1"
---
# Legacy

- [Legacy](legacy.md) - Legacy concept.
""",
                "legacy.md": """---
type: Guide
title: Legacy
description: A legacy concept.
timestamp: 2026-01-01T10:00:00Z
---

# Legacy

# Citations

- [Source](https://example.com)
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "WARN index.md: bundle targets OKF 0.1; this validator checks v0.2",
            result.stdout,
        )
        self.assertIn("WARN legacy.md: legacy `timestamp` should migrate to `generated.at`", result.stdout)
        self.assertIn("WARN legacy.md: legacy `# Citations` should migrate to `sources`", result.stdout)

    def test_ignores_link_examples_in_inline_code_and_html_comments(self) -> None:
        result = self.run_validator(
            {
                "index.md": "# Examples\n\n- [Examples](examples.md) - Link examples.\n",
                "examples.md": """---
type: Guide
title: Examples
description: Demonstrate links as text.
---

# Examples

The literal syntax is `[label](missing.md)`.

<!-- [unpublished](also-missing.md) -->

    - [list example](list-missing.md)

- List item
      [nested code example](nested-list-code.md)

```markdown
# Citations
```
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OKF validation passed: 1 concept, 0 warnings", result.stdout)

    def test_handles_reference_links_and_ignores_indented_code(self) -> None:
        result = self.run_validator(
            {
                "index.md": """# Examples

- [Examples][examples] - Link examples.

[examples]: examples.md
""",
                "examples.md": """---
type: Guide
title: Examples
description: Demonstrate reference links.
---

# Examples

    [literal](missing.md)

See [an unavailable concept][missing-ref].
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN examples.md: undefined reference link `[missing-ref]`", result.stdout)
        self.assertNotIn("broken internal link `missing.md`", result.stdout)
        self.assertNotIn("concept is not listed by any index", result.stdout)

    def test_handles_collapsed_and_shortcut_links_in_nested_lists(self) -> None:
        result = self.run_validator(
            {
                "index.md": """# Guides

- Commands
    - [Install][] - Installation.
    - [configure] - Configuration.

[install]: install.md
[configure]: configure.md
""",
                "install.md": """---
type: Guide
title: Install
description: Install Bob Shell.
---

# Install

See [missing collapsed][].

[missing collapsed]: missing-collapsed.md
""",
                "configure.md": """---
type: Guide
title: Configure
description: Configure Bob Shell.
---

# Configure

See [missing shortcut].

[missing shortcut]: missing-shortcut.md
""",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("concept is not listed by any index", result.stdout)
        self.assertIn("WARN install.md: broken internal link `missing-collapsed.md`", result.stdout)
        self.assertIn("WARN configure.md: broken internal link `missing-shortcut.md`", result.stdout)

    def test_rejects_a_missing_bundle_directory(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "/definitely/not/an/okf/bundle"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("not a directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
