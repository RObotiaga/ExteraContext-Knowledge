# Preflight Baseline Report: feat/plugins-store-verified-catalog

**Date:** 2026-10-03  
**Target Repository:** `RObotiaga/ExteraContext-Knowledge`  
**Target Branch:** `feat/plugins-store-verified-catalog`  
**Base Comparison Branch:** `main`  

---

## 1. Commit SHAs

- **`main`:** `a229c986bdbe209282a46826cce48cb4b41df27c`
- **`feat/plugins-store-knowledge`:** `5f4784149683bff40c02c43c084e58ab105882f3`
- **`feat/plugins-store-verified-catalog`:** `cf2b09f31b10d7cdcc5928fb5ed967949cc4a7b5`

---

## 2. Current Branch Inventory and Counts

- **Total unique sources:** `114` (84 legacy/thematic sources + 30 new individual Plugins-Store sources)
- **Total facts:** `2603` (2453 baseline + 150 new facts)
- **New individual plugin sources:** `30`
- **New facts:** `150` (exactly 5 facts per individual source)
- **Collector / Reviewer pairs:** Present for all 30 sources (total 250 runs in `data/legacy-source-runs.json`)
- **Strict Linter Status:** `scripts/lint_knowledge.py` passes with 0 errors (`SUCCESS: ALL STRICT QUALITY GATES PASSED (100% Verified)!`).

---

## 3. Baseline Test Failures & Structural Deficiencies

### A. Test Failures
- **`tests/test_legacy_provenance.py`:** **FAILED**
  - Failure: `assert manifest["unique_sources"] == 84` raises `AssertionError` because `unique_sources` is now 114.
  - Reason: Hardcoded legacy constants (`prompt_count == 190`, `unique_sources == 84`, `len(runs) == 190`) do not distinguish legacy prompt archive runs from post-legacy verified catalog runs.

### B. Provenance Schema & SQLite Incompatibilities
- **`data/legacy-source-runs.json`:**
  - Lacks an explicit `schema_version` (currently unversioned / v1).
  - The 60 new runs (30 collector + 30 reviewer) lack `call_id`, `provenance_kind`, and other metadata.
  - In `scripts/build_index.py`, `source_runs` defines `call_id TEXT PRIMARY KEY`. Without `call_id`, new runs insert with `call_id = NULL`, causing primary key collisions or loss of run identity.
  - In `source_summaries`, the new sources lack `collector_runs` and `reviewer_runs` integer counters, causing SQLite `source_provenance` to have `has_collector = 1` and `has_reviewer = 1`, but `collector_runs = 0` and `reviewer_runs = 0`.
  - Missing field values should be cleanly `null` rather than fabricated with fake data.

### C. Source Registry (`data/wiki/source-registry.md`)
- Line 3 contains an inaccurate global claim: `Модель всех пар: gpt-6-luna.`, whereas new collectors used `google-antigravity/gemini-3.8-flash` and reviewers used `gpt-6-luna` or `deepseek-v4.1-flash`.
- The registry table only lists up to 91 sources and does not yet contain the 30 new individual plugin sources.

---

## 4. Baseline Retrieval Benchmark Metrics

### Standard Evaluation (`evaluate_retrieval.py` on 15 core cases):
- **Cases:** 15
- **Hit@1:** 0.7333 (73.3%)
- **Hit@3:** 0.8000 (80.0%)
- **Hit@5:** 1.0000 (100.0%)
- **Hit@10:** 1.0000 (100.0%)
- **Expected Recall@10:** 0.8778 (87.8%)
- **MRR@10:** 0.8056
- **Average Direct Evidence in Top 10:** 9.6 / 10
- **Average Donor Evidence in Top 10:** 0.067 / 10
- **Average Packet Size:** 14,594.2 chars

### Control Evaluation (`evaluate_control.py` on 15 control cases):
- **Cases:** 15
- **Top 1:** 0.4000 (40.0%)
- **Top 3:** 0.5333 (53.3%)
- **Top 5:** 0.6000 (60.0%)
- **Top 10:** 0.6667 (66.7%)
- **Recall:** 0.5333 (53.3%)

---

## 5. Required Action Plan

1. **Stage 1 (Provenance Schema):** Upgrade `data/legacy-source-runs.json` to `schema_version: 2`, introduce `provenance_kind`, add stable `run_id` as primary identifier, support both legacy and post-legacy runs cleanly in `build_index.py`.
2. **Stage 2 (Source Summaries):** Ensure `collector_runs = 1`, `reviewer_runs = 1`, `has_collector = true`, `has_reviewer = true`, `review_mode = "independent-source-reread-nonblind"`, accurate `models` array and `facts_count = 5`.
3. **Stage 3 (Tests):** Rewrite `test_legacy_provenance.py` around structural invariants and separate counters (`legacy_prompt_count`, `legacy_unique_sources`, `post_legacy_runs`, `total_unique_sources`), check SQLite integrity and concrete source rows (`official-sdk` vs `plugins-store-searchid`).
4. **Stage 4 (Source Registry):** Update `source-registry.md` with model columns, remove false global statements, and include all 30 new sources.
5. **Stage 5 (Quality Linter):** Extend `scripts/lint_knowledge.py` to validate each individual plugin source (facts, source, review, line ranges, pinned URLs, duplicate fact IDs, near-duplicate claims).
6. **Stage 6 (Coverage Model):** Add `data/wiki/coverage/plugins-store-<id>.json` for individual plugins with structured areas and known gaps.
7. **Stage 7 (Quality Audit):** Conduct sample audit across small, medium, and large plugins; create `benchmark/plugins-store-verified-catalog-audit.md`.
8. **Stage 8 (Holdout & A/B Benchmark):** Create `benchmark/plugins-store-holdout.json` (20+ queries across 10 categories), run retrieval A/B and generate `benchmark/PLUGINS_STORE_VERIFIED_CATALOG_REPORT.md`.
9. **Stage 9 (CI):** Run full test suite.
10. **Stage 10 (Merge Readiness):** Produce `benchmark/PLUGINS_STORE_VERIFIED_CATALOG_MERGE_READINESS.md`.
