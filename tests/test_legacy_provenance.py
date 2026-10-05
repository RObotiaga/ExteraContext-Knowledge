from __future__ import annotations

import json
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "exteracontext.sqlite"
MANIFEST = ROOT / "data" / "legacy-source-runs.json"

class TestLegacyProvenance(unittest.TestCase):
    def test_provenance_invariants(self):
        manifest = json.loads(MANIFEST.read_text("utf-8"))

        # Invariant 1: Schema version 2 with separated legacy & post-legacy counters
        self.assertEqual(manifest.get("schema_version"), 2)
        self.assertEqual(manifest.get("legacy_prompt_count"), 190)
        self.assertEqual(manifest.get("legacy_unique_sources"), 84)
        self.assertEqual(manifest.get("total_unique_sources"), 115)

        # Invariant 2: Total unique sources == len(source_summaries)
        summaries = manifest["source_summaries"]
        self.assertEqual(manifest["unique_sources"], len(summaries))
        self.assertEqual(manifest["total_unique_sources"], len(summaries))
        self.assertEqual(len(manifest["runs"]), 252)

        # Invariant 3: All source_ids are unique
        source_ids = [s["source_id"] for s in summaries]
        self.assertEqual(len(source_ids), len(set(source_ids)))

        # Invariant 4: Every source with collector/reviewer provenance has valid runs and distinct IDs
        for s in summaries:
            self.assertTrue(s["has_collector"])
            self.assertTrue(s["has_reviewer"])
            self.assertGreaterEqual(s["collector_runs"], 1)
            self.assertGreaterEqual(s["reviewer_runs"], 1)
            
            indep = s["independent_run_ids"]
            if isinstance(indep, list):
                self.assertGreaterEqual(len(indep), 2)
                self.assertEqual(len(set(indep)), len(indep))
            else:
                self.assertTrue(indep)

        # Invariant 5: SQLite source_runs and source_provenance integrity
        self.assertTrue(DB.exists(), f"Database not found at {DB}")
        con = sqlite3.connect(DB)
        try:
            self.assertEqual(con.execute("pragma integrity_check").fetchone()[0], "ok")
            
            # 252 source runs (190 legacy + 62 post-legacy/direct-capture)
            self.assertEqual(con.execute("select count(*) from source_runs").fetchone()[0], 252)
            # 115 source provenance entries
            self.assertEqual(con.execute("select count(*) from source_provenance").fetchone()[0], 115)
            self.assertEqual(con.execute("select count(*) from source_provenance where has_reviewer=1").fetchone()[0], 115)
            self.assertEqual(con.execute("select count(*) from source_provenance where collector_runs >= 1 and reviewer_runs >= 1").fetchone()[0], 115)

            # Check realistic fields for sample legacy source ('official-sdk')
            row_legacy = con.execute(
                "select collector_runs, reviewer_runs, review_mode, all_fork_turns_none, has_collector, has_reviewer "
                "from source_provenance where source_id='official-sdk'"
            ).fetchone()
            self.assertEqual(row_legacy, (1, 1, "independent-source-reread-nonblind", 1, 1, 1))

            leg_run = con.execute(
                "select run_id, call_id, source_id, role, provenance_kind, model "
                "from source_runs where source_id='official-sdk' and role='collector'"
            ).fetchone()
            self.assertIsNotNone(leg_run[1])  # call_id exists for legacy run
            self.assertEqual(leg_run[4], "legacy-agent-run")

            # Check realistic fields for sample new verified-catalog source ('plugins-store-searchid')
            # all_fork_turns_none is None because fork_turns is not applicable/recorded for verified-catalog runs
            row_new = con.execute(
                "select collector_runs, reviewer_runs, review_mode, all_fork_turns_none, has_collector, has_reviewer, facts_count "
                "from source_provenance where source_id='plugins-store-searchid'"
            ).fetchone()
            self.assertEqual(row_new, (1, 1, "independent-source-reread-nonblind", None, 1, 1, 5))

            new_run_collector = con.execute(
                "select run_id, call_id, source_id, role, provenance_kind, model "
                "from source_runs where source_id='plugins-store-searchid' and role='collector'"
            ).fetchone()
            self.assertEqual(new_run_collector[0], "run_collect_plugins-store-searchid")
            self.assertIsNone(new_run_collector[1])  # no fake call_id
            self.assertEqual(new_run_collector[4], "verified-catalog-collector")
            self.assertEqual(new_run_collector[5], "google-antigravity/gemini-3.8-flash")

            new_run_reviewer = con.execute(
                "select run_id, call_id, source_id, role, provenance_kind, model "
                "from source_runs where source_id='plugins-store-searchid' and role='reviewer'"
            ).fetchone()
            self.assertEqual(new_run_reviewer[0], "run_review_plugins-store-searchid")
            self.assertIsNone(new_run_reviewer[1])  # no fake call_id
            self.assertEqual(new_run_reviewer[4], "verified-catalog-reviewer")
            self.assertEqual(new_run_reviewer[5], "gpt-6-luna")

        finally:
            con.close()

if __name__ == "__main__":
    unittest.main()
