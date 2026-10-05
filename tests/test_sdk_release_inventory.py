from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "data" / "sdk-snapshots" / "release-inventory.json"
FACTS = ROOT / "data" / "wiki" / "facts" / "official-sdk-builds.json"

class TestSdkReleaseInventory(unittest.TestCase):
    def test_release_inventory(self):
        inv = json.loads(INV.read_text("utf-8"))
        releases = inv["releases"]
        facts = json.loads(FACTS.read_text("utf-8"))

        self.assertEqual(inv["source_id"], "official-sdk-builds")
        self.assertGreaterEqual(len(releases), 14)
        self.assertEqual(len({r["tag"] for r in releases}), len(releases))
        self.assertTrue(all(r["sdk_version"] and r["channel"] and r["build"] and r["commit"] for r in releases))
        self.assertTrue(all(r["stubs"] and r["stubs"]["digest"].startswith("sha256:") for r in releases))
        identity = [(r["sdk_version"], r["channel"], r["build"], r["tag"], r["commit"]) for r in releases]
        self.assertEqual(len(identity), len(set(identity)))
        counts = Counter(r["sdk_version"] for r in releases)
        for version in ["1.4.3.9", "1.4.4.1", "1.4.5.0"]:
            self.assertGreaterEqual(counts[version], 2)
            xs = [r for r in releases if r["sdk_version"] == version]
            self.assertGreaterEqual(len({r["stubs"]["digest"] for r in xs}), 2)
        self.assertTrue(any(r["channel"] == "beta" and r["github_prerelease"] is False for r in releases))
        ids = {f["id"] for f in facts}
        self.assertIn("official-sdk-builds:snapshot-identity", ids)
        self.assertIn("official-sdk-builds:stubs-symbol-diff-pending", ids)

if __name__ == "__main__":
    unittest.main()
