# Merge Readiness Report: feat/plugins-store-verified-catalog

**Date:** 2026-10-03  
**Target Repository:** `RObotiaga/ExteraContext-Knowledge`  
**Branch:** `feat/plugins-store-verified-catalog`  
**Base Branch:** `main`  
**Overall Verdict:** **READY WITH NON-BLOCKING GAPS**

---

## 1. Summary

This report assesses the merge-readiness of the `feat/plugins-store-verified-catalog` branch into `main`. The branch introduces structured, independently verified technical knowledge for 30 individual plugins from the [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store) repository, repairs provenance schema incompatibilities, resolves commit pin authenticity issues, and establishes machine-readable coverage models.

---

## 2. What Improved

1. **New Knowledge Assets:**
   - **30 New Individual Plugin Sources:** 30 standalone source markdown pages, 30 independent review pages, and 30 fact JSON bundles.
   - **150 High-Value Facts:** Every fact is anchored to exact source lines and immutable commit SHAs with actionable developer recipes.
   - **Total Fact Corpus:** Expanded from **2,453 to 2,603 verified facts** (+150 facts).
2. **Provenance Schema v2:**
   - Introduced `schema_version: 2` with explicit separation between legacy prompt archive runs, verified catalog runs, and direct API captures.
   - Fixed SQLite `source_runs` primary key to use stable `run_id`, preventing data loss on null `call_id`.
   - Populated true `collector_runs = 1` and `reviewer_runs = 1` for all individual sources, eliminating `0` counters in SQLite.
3. **Commit Pin Repair:**
   - Repaired 19 previously truncated/misidentified commit SHAs with exact, content-verified git commit hashes and blobs.
   - All 30 individual plugin sources now link to 100% resolvable (HTTP 200) immutable commit objects.
4. **Coverage Models:**
   - Added 30 machine-readable coverage JSON files in `data/wiki/coverage/` tracking 15 architectural areas and documented gaps.
5. **Quality Gate & CI:**
   - Enhanced `scripts/lint_knowledge.py` to enforce cross-document consistency, 40-hex commit SHA validation, global fact ID uniqueness, and duplicate claim prevention.
   - All unit tests (`test_knowledge_quality_gate`, `test_legacy_provenance`, `test_sdk_release_inventory`) pass 100%.

---

## 3. Provenance Migration

- **Schema Contract:** `data/legacy-source-runs.json` migrated from unversioned/v1 to `schema_version: 2`.
- **Honest Nulls Policy:** Unknown fields (e.g., `call_id`, `started_at`, `prompt_archive`, `reasoning`, `fork_turns` for post-legacy runs) are preserved as `null` rather than populated with synthetic placeholders.
- **Categorization of Runs:**
  - `legacy-agent-run`: 190 runs (84 sources)
  - `verified-catalog-collector`: 30 runs (30 sources)
  - `verified-catalog-reviewer`: 30 runs (30 sources)
  - `direct-capture`: 1 run (`official-sdk-builds`)
  - `direct-capture-review`: 1 run (`official-sdk-builds`)
  - **Total Runs:** **252 runs** across **115 unique sources**.
- **Review Mode:** Explicitly documented as `independent-source-reread-nonblind` for all plugin reviews where reviewers inspected collector output.

---

## 4. Quality Gate Results

### Strict Quality Linter (`scripts/lint_knowledge.py`):
```
=== Running ExteraContext-Knowledge Strict Quality Gate ===
Quality Gate Completed. Total errors: 0, warnings: 0
SUCCESS: ALL STRICT QUALITY GATES PASSED (100% Verified)!
```

### Invariant Checks:
- `index.md` source count (`115`) = `source-registry.md` source count (`115`) = `legacy-source-runs.json` summary count (`115`) = SQLite `source_provenance` count (`115`).
- Total facts in `index.md` header (`2603`) = master `facts.json` length (`2603`) = sum of all per-file facts (`2603`).
- Global duplicate fact IDs: `0`.
- Global exact duplicate claims: `0`.
- Unpinned `blob/main` or `branch/main` references: `0`.

---

## 5. Sample Audit Results

A blind sample audit was conducted by independent subagents on 75 facts (50% sample) across 15 plugins (including mandatory targets `SearchID`, `Profile_Plugin`, `Link Guard`, and `Air Raid Alert`):

- **Sampled Facts:** 75 / 150
- **Accuracy:** 68 fully verified, 7 scope/citation corrections applied, 0 rejected.
- **Evidence Link Validity:** 100% (75/75 URLs resolve with HTTP 200).
- **Overclaim Rate:** 1.3% (all identified overclaims softened to best-effort/observed scope).
- **Runtime Overclaim Rate:** 0.0% (strict `code` status maintained across all records).

---

## 6. Retrieval Benchmark: main vs. Branch

| Metric | main (Baseline, 2453 facts) | Branch (Verified Catalog, 2603 facts) | Delta | Assessment |
|---|---|---|---|---|
| **Core Cases Hit@1** | 0.7333 (73.3%) | 0.7333 (73.3%) | 0.0000 | **Zero regression** |
| **Core Cases MRR@10** | 0.8056 | 0.8056 | 0.0000 | **Zero regression** |
| **Core Cases Recall@10** | 0.8778 (87.8%) | 0.8778 (87.8%) | 0.0000 | **Zero regression** |
| **Donor Contamination (Core)** | 0.0667 | 0.0667 | 0.0000 | **Zero increase (safe)** |
| **General Holdout Hit@1** | 0.4000 (40.0%) | 0.4000 (40.0%) | 0.0000 | **Zero regression** |
| **Plugins-Store Holdout Hit@1** | 0.0000 (0.0%) | **0.4545 (45.5%)** | **+0.4545** | **Substantial gain** |
| **Plugins-Store Holdout Hit@5** | 0.0000 (0.0%) | **0.5455 (54.5%)** | **+0.5455** | **Substantial gain** |
| **Plugins-Store Holdout Recall**| 0.0000 (0.0%) | **0.6439 (64.4%)** | **+0.6439** | **Substantial gain** |

---

## 7. Known Remaining Gaps (Non-Blocking)

1. **Partitioned Plugins Granularity:** The 686 legacy plugins in Plugins-Store remain categorized under 8 comprehensive thematic partitions (`ui-customization`, `messages-chat`, `hooks-reflection`, `media-files`, `network-async`, `dex-native`, `accounts-storage`, `automation-tools`). Breaking these down into individual 1-plugin-1-file records can proceed incrementally in subsequent maintenance PRs.
2. **Offline Binary Validation:** EAF/ZIP internal member paths (e.g. `air_raid_alert.eaf!/src/monitor.py`) are content-addressed by the outer archive SHA-256 and member byte counts, but are not individual Git blobs.
3. **Hardware / Vendor API Testing:** Features relying on device-specific hardware (Samsung S-Pen stylus action codes, Google Play Services MLKit face models, Android 12+ RenderEffect) are documented from static code analysis (`status: code`); live device validation requires target device execution.

---

## 8. Runtime Evidence Status

- **Status:** All 150 new facts carry `status: "code"`.
- **Target Target Compatibility:** Static call-site observation in a plugin does not imply forward compatibility across all ExteraGram/AyuGram versions.
- **Index Runtime Status:** The index reports `runtime_verified: 0`. No static fact has been promoted to runtime-verified status.

---

## 9. Merge Recommendation

### Recommendation: **READY WITH NON-BLOCKING GAPS**

The branch `feat/plugins-store-verified-catalog` satisfies all mandatory merge requirements:
- Provenance database preserves full integrity under Schema v2 without synthetic data.
- All cross-document and SQLite counts match exactly at 115 sources and 2,603 facts.
- CI and local test suites pass 100%.
- All evidence links resolve to verified commit objects.
- Retrieval benchmark proves zero regression on legacy cases and dramatic improvements (+45.5% Hit@1, +64.4% Recall) on Plugins-Store queries.
- Evidence boundaries between static code observation and official target API support are strictly maintained.
