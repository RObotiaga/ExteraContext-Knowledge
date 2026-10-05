from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "scripts" / "lint_knowledge.py"

class TestKnowledgeQualityGate(unittest.TestCase):
    def test_quality_gate(self):
        res = subprocess.run(
            [sys.executable, str(LINTER)],
            capture_output=True, text=True
        )
        self.assertEqual(res.returncode, 0, f"Quality gate failed:\n{res.stdout}\n{res.stderr}")
        self.assertIn("ALL STRICT QUALITY GATES PASSED (100% Verified)!", res.stdout)

if __name__ == "__main__":
    unittest.main()
