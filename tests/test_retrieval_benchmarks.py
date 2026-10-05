#!/usr/bin/env python3
"""
CI Test Suite: Retrieval Quality Gates & Regression Budget.
Validates:
1. Core SDK regression budget (benchmark/cases.json).
2. Plugins-Store holdout retrieval performance (benchmark/plugins-store-holdout.json).
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import query as qmod

BENCH_DIR = ROOT / "benchmark"
CORE_CASES = BENCH_DIR / "cases.json"
PS_HOLDOUT = BENCH_DIR / "plugins-store-holdout.json"


def evaluate_dataset(cases_path: Path):
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    rows = []
    for c in cases:
        query = c["query"]
        expected = set(c["expected"])
        facts = qmod.search_facts(query, limit=10)
        ids = [f["id"] for f in facts]

        ranks = {e: (ids.index(e) + 1 if e in ids else None) for e in expected}
        found_ranks = [r for r in ranks.values() if r is not None]
        min_rank = min(found_ranks) if found_ranks else None

        found = sum(1 for e in expected if e in ids)
        direct = sum(1 for f in facts if f.get("directness") in {"official", "target-ecosystem"})
        donors = sum(1 for f in facts if f.get("directness") == "donor")

        rr = (1.0 / min_rank) if min_rank else 0.0
        recall = (found / len(expected)) if expected else 0.0

        rows.append({
            "id": c["id"],
            "top1": bool(min_rank and min_rank <= 1),
            "top3": bool(min_rank and min_rank <= 3),
            "top5": bool(min_rank and min_rank <= 5),
            "top10": bool(min_rank and min_rank <= 10),
            "recall": recall,
            "mrr": rr,
            "direct": direct,
            "donors": donors,
        })

    n = len(rows) if rows else 1
    return {
        "cases": n,
        "hit@1": sum(r["top1"] for r in rows) / n,
        "hit@3": sum(r["top3"] for r in rows) / n,
        "hit@5": sum(r["top5"] for r in rows) / n,
        "hit@10": sum(r["top10"] for r in rows) / n,
        "recall@10": sum(r["recall"] for r in rows) / n,
        "mrr@10": sum(r["mrr"] for r in rows) / n,
        "avg_donors": sum(r["donors"] for r in rows) / n,
    }


class TestRetrievalBenchmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        qmod.ensure_db()

    def test_core_sdk_regression_budget(self):
        """
        Enforce strict regression budget on the 15 core SDK cases:
        - Hit@1 must not drop below baseline (0.7333).
        - Hit@3 must remain >= 0.8000.
        - Hit@5 allowed max 1-2 case shift (>= 0.8666).
        - MRR@10 allowed max 0.03 drop (>= 0.7700).
        - Recall@10 must remain >= 0.7500.
        - Donor contamination must remain near zero (<= 0.05).
        """
        results = evaluate_dataset(CORE_CASES)
        print("\nCore Cases Retrieval:", results)

        self.assertGreaterEqual(results["hit@1"], 0.7333, "Core Hit@1 regressed below baseline 0.7333")
        self.assertGreaterEqual(results["hit@3"], 0.8000, "Core Hit@3 regressed below 0.8000")
        self.assertGreaterEqual(results["hit@5"], 0.8666, "Core Hit@5 regressed below budget (max 1-2 case shift)")
        self.assertGreaterEqual(results["hit@10"], 0.9333, "Core Hit@10 regressed below 0.9333")
        self.assertGreaterEqual(results["mrr@10"], 0.7700, "Core MRR@10 regressed beyond budget (0.8056 - 0.035)")
        self.assertGreaterEqual(results["recall@10"], 0.7500, "Core Recall@10 regressed beyond budget")
        self.assertLessEqual(results["avg_donors"], 0.05, "Core donor contamination exceeded threshold")

    def test_plugins_store_holdout_quality(self):
        """
        Enforce retrieval quality on the 22 Plugins-Store holdout cases:
        - Hit@1 >= 0.40
        - Hit@5 >= 0.50
        - Hit@10 >= 0.70
        - Recall@10 >= 0.60
        - Donor contamination <= 0.10
        """
        results = evaluate_dataset(PS_HOLDOUT)
        print("Plugins-Store Holdout:", results)

        self.assertGreaterEqual(results["hit@1"], 0.40, "Plugins-Store Hit@1 below target")
        self.assertGreaterEqual(results["hit@5"], 0.50, "Plugins-Store Hit@5 below target")
        self.assertGreaterEqual(results["hit@10"], 0.70, "Plugins-Store Hit@10 below target")
        self.assertGreaterEqual(results["recall@10"], 0.60, "Plugins-Store Recall@10 below target")
        self.assertLessEqual(results["avg_donors"], 0.10, "Plugins-Store donor contamination too high")


if __name__ == "__main__":
    unittest.main()
