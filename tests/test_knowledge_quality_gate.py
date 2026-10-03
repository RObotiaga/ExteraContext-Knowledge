from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "scripts" / "lint_knowledge.py"

def test_quality_gate():
    res = subprocess.run(
        [sys.executable, str(LINTER)],
        capture_output=True, text=True
    )
    assert res.returncode == 0, f"Quality gate failed:\n{res.stdout}\n{res.stderr}"
    assert "ALL STRICT QUALITY GATES PASSED (100% Verified)!" in res.stdout

if __name__ == "__main__":
    test_quality_gate()
    print("test_knowledge_quality_gate: ok")
