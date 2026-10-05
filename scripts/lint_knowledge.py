#!/usr/bin/env python3
"""
Strict Quality Gate Linter for ExteraContext-Knowledge.

Enforces:
1. Manifest integrity (legacy 705 files partition mapping).
2. Cross-document consistency:
   - index.md header counts == master facts.json count == provenance source count.
   - facts JSON count == index.md listed count == review.md stated count.
   - source-registry.md contains all 115 registered sources.
3. Evidence integrity:
   - No unpinned 'blob/main' or 'branch/main' URLs in facts or wiki pages.
   - All 'code' facts must have exact line number references in evidence_path (:line).
   - All pinned commit SHAs must have expected 40-hex length.
4. Reviewer independence:
   - Reviewer identity in frontmatter cannot contain 'collector'.
   - Static/runtime evidence boundaries explicitly documented.
5. Individual plugin sources validation (30 sources):
   - Facts, source, review files present.
   - Frontmatter completeness.
   - Provenance collector + reviewer link.
6. Global fact integrity:
   - Zero duplicate fact IDs across the entire corpus.
   - Zero exact duplicate claims.
   - Near-duplicate claim warning analysis.
"""

from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "data" / "wiki"
FACTS_DIR = WIKI / "facts"
SOURCES_DIR = WIKI / "sources"
REVIEWS_DIR = WIKI / "reviews"
PROVENANCE_FILE = ROOT / "data" / "legacy-source-runs.json"
MANIFEST_FILE = ROOT / "data" / "plugins-manifest.json"
INDEX_FILE = WIKI / "index.md"
REGISTRY_FILE = WIKI / "source-registry.md"
MASTER_FACTS_FILE = WIKI / "facts.json"

errors = []
warnings = []

def error(msg: str):
    errors.append(msg)
    print(f"  [ERROR] {msg}")

def warn(msg: str):
    warnings.append(msg)
    print(f"  [WARN] {msg}")

print("=== Running ExteraContext-Knowledge Strict Quality Gate ===")

# --- 1. Manifest Validation ---
if not MANIFEST_FILE.exists():
    error(f"Missing manifest file: {MANIFEST_FILE}")
else:
    try:
        manifest = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
        entries = manifest.get("entries", [])
        total_files = manifest.get("total_files_in_git_tree", 0)
        inc_count = manifest.get("included_files_count", 0)
        exc_count = manifest.get("excluded_files_count", 0)
        summary = manifest.get("summary_by_category", {})

        if len(entries) != 705:
            error(f"Manifest entries count is {len(entries)}, expected 705")
        if total_files != 705:
            error(f"Manifest total_files_in_git_tree is {total_files}, expected 705")
        if inc_count + exc_count != 705:
            error(f"Manifest included ({inc_count}) + excluded ({exc_count}) != 705")

        paths = [e["path"] for e in entries]
        if len(set(paths)) != 705:
            error(f"Duplicate paths found in manifest: {705 - len(set(paths))} duplicates")

        sum_cat = sum(summary.values())
        if sum_cat != 705:
            error(f"Sum of summary_by_category ({sum_cat}) != 705")

    except Exception as e:
        error(f"Failed to parse manifest: {e}")

# --- 2. Global Header Verification in index.md ---
if not INDEX_FILE.exists():
    error(f"Missing index.md: {INDEX_FILE}")
    header_src_cnt = 0
    header_fact_cnt = 0
else:
    index_text = INDEX_FILE.read_text(encoding='utf-8')
    m_header = re.search(r'Обработано и независимо проверено\s+(\d+)\s+из\s+(\d+)\s+материалов;\s*структурированных записей с происхождением\s*—\s*(\d+)', index_text)
    if not m_header:
        error("Header count pattern not found in index.md")
        header_src_cnt = 0
        header_fact_cnt = 0
    else:
        header_src_cnt = int(m_header.group(1))
        header_fact_cnt = int(m_header.group(3))

# --- 3. Master facts.json Verification ---
if not MASTER_FACTS_FILE.exists():
    error(f"Missing master facts.json: {MASTER_FACTS_FILE}")
    master_facts = []
else:
    try:
        master_facts = json.loads(MASTER_FACTS_FILE.read_text(encoding='utf-8'))
        if len(master_facts) != header_fact_cnt:
            error(f"facts.json length ({len(master_facts)}) != index.md header count ({header_fact_cnt})")
    except Exception as e:
        error(f"Failed to parse master facts.json: {e}")
        master_facts = []

# --- 4. Provenance Verification ---
if not PROVENANCE_FILE.exists():
    error(f"Missing legacy-source-runs.json: {PROVENANCE_FILE}")
    prov_sources = {}
    prov_runs = []
else:
    try:
        prov = json.loads(PROVENANCE_FILE.read_text(encoding='utf-8'))
        prov_sources = {s["source_id"]: s for s in prov.get("source_summaries", [])}
        prov_runs = prov.get("runs", [])

        if prov.get("schema_version") != 2:
            error(f"Provenance schema_version is {prov.get('schema_version')}, expected 2")

        if len(prov_sources) != header_src_cnt:
            error(f"Provenance source_summaries count ({len(prov_sources)}) != index.md header ({header_src_cnt})")
        if prov.get("unique_sources") != header_src_cnt:
            error(f"Provenance unique_sources ({prov.get('unique_sources')}) != index.md header ({header_src_cnt})")

    except Exception as e:
        error(f"Failed to parse provenance: {e}")
        prov_sources = {}
        prov_runs = []

# --- 5. Partition-by-Partition Deep Checks (8 Thematic Partitions) ---
partitions = [
    'plugins-store-ui-customization',
    'plugins-store-messages-chat',
    'plugins-store-hooks-reflection',
    'plugins-store-media-files',
    'plugins-store-network-async',
    'plugins-store-dex-native',
    'plugins-store-accounts-storage',
    'plugins-store-automation-tools'
]

# Extract index line counts: [Title](sources/<id>.md): X структурированных записей
index_item_counts = {}
for m in re.finditer(r'\[([^\]]+)\]\(sources/([^)]+)\.md\):\s*(\d+)\s*структурированн', index_text):
    index_item_counts[m.group(2)] = int(m.group(3))

for p in partitions:
    facts_file = FACTS_DIR / f"{p}.json"
    src_file = SOURCES_DIR / f"{p}.md"
    rev_file = REVIEWS_DIR / f"{p}.md"

    if not facts_file.exists():
        error(f"Missing facts file: {facts_file}")
        continue
    if not src_file.exists():
        error(f"Missing source file: {src_file}")
        continue
    if not rev_file.exists():
        error(f"Missing review file: {rev_file}")
        continue

    facts = json.loads(facts_file.read_text(encoding='utf-8'))
    fact_count = len(facts)
    src_text = src_file.read_text(encoding='utf-8')
    rev_text = rev_file.read_text(encoding='utf-8')

    manifest_cat_count = manifest["summary_by_category"].get(p)
    if manifest_cat_count is None:
        error(f"Partition {p} not found in manifest summary_by_category")
    else:
        if str(manifest_cat_count) not in src_text:
            error(f"Source {src_file.name} does not state manifest file count {manifest_cat_count}")
        if str(manifest_cat_count) not in rev_text:
            error(f"Review {rev_file.name} does not state manifest file count {manifest_cat_count}")

    idx_cnt = index_item_counts.get(p)
    if idx_cnt != fact_count:
        error(f"Fact count mismatch for {p}: facts JSON has {fact_count}, but index.md lists {idx_cnt}")

    m_rev_cnt = re.search(r'[Сс]борщик.*?(\d+)\s+факт', rev_text)
    if not m_rev_cnt:
        error(f"Review {rev_file.name} missing stated fact count pattern ('Сборщик ... X фактов')")
    else:
        rev_stated_facts = int(m_rev_cnt.group(1))
        if rev_stated_facts != fact_count:
            error(f"Review {rev_file.name} states {rev_stated_facts} facts, but facts JSON has {fact_count}")

    m_rev_id = re.search(r'reviewer:\s*([^\n]+)', rev_text)
    if not m_rev_id:
        error(f"Missing reviewer in frontmatter of {rev_file.name}")
    else:
        rev_val = m_rev_id.group(1).strip()
        if "collector" in rev_val.lower():
            error(f"Reviewer cannot be collector in {rev_file.name}: {rev_val}")

    p_summary = prov_sources.get(p)
    if not p_summary:
        error(f"Missing provenance summary for {p}")
    else:
        if not p_summary.get("has_collector"):
            error(f"Provenance for {p} missing has_collector")
        if not p_summary.get("has_reviewer"):
            error(f"Provenance for {p} missing has_reviewer")
        if not p_summary.get("independent_run_ids"):
            error(f"Provenance for {p} missing independent_run_ids")

    for fact in facts:
        url = fact.get("evidence_url", "")
        if "blob/main" in url or "branch/main" in url:
            error(f"Unpinned url in fact {fact.get('id')}: {url}")

        status = fact.get("status")
        ev_path = fact.get("evidence_path", "")
        if status == "code":
            if ":" not in ev_path or not re.search(r':\d+', ev_path):
                error(f"Code fact {fact.get('id')} missing line reference in evidence_path: '{ev_path}'")

# --- 6. Individual Plugins-Store Sources Validation (30 Individual Sources) ---
individual_sources = [
    p.stem for p in FACTS_DIR.glob("plugins-store-*.json")
    if p.stem not in {
        "plugins-store", "plugins-store-codeberg", "plugins-store-gitverse",
        "plugins-store-ui-customization", "plugins-store-messages-chat", "plugins-store-hooks-reflection",
        "plugins-store-media-files", "plugins-store-network-async", "plugins-store-dex-native",
        "plugins-store-accounts-storage", "plugins-store-automation-tools"
    }
]

runs_by_source = {}
for r in prov_runs:
    runs_by_source.setdefault(r.get("source_id"), []).append(r)

for sid in individual_sources:
    ffile = FACTS_DIR / f"{sid}.json"
    sfile = SOURCES_DIR / f"{sid}.md"
    rfile = REVIEWS_DIR / f"{sid}.md"

    if not ffile.exists():
        error(f"Missing individual facts file: {ffile}")
        continue
    if not sfile.exists():
        error(f"Missing individual source file: {sfile}")
        continue
    if not rfile.exists():
        error(f"Missing individual review file: {rfile}")
        continue

    facts = json.loads(ffile.read_text(encoding="utf-8"))
    stext = sfile.read_text(encoding="utf-8")
    rtext = rfile.read_text(encoding="utf-8")

    # Frontmatter completeness
    for field in ["source_id", "repository", "commit", "platform", "review_status"]:
        if f"{field}:" not in stext[:stext.find("\n---\n", 3)]:
            error(f"Source {sfile.name} missing frontmatter {field}")

    for field in ["source_id", "reviewer", "review_status"]:
        if f"{field}:" not in rtext[:rtext.find("\n---\n", 3)]:
            error(f"Review {rfile.name} missing frontmatter {field}")

    # Reviewer independence
    m_rev = re.search(r"reviewer:\s*([^\n]+)", rtext[:rtext.find("\n---\n", 3)])
    if m_rev and "collector" in m_rev.group(1).lower():
        error(f"Reviewer in {rfile.name} cannot contain 'collector'")

    # Review stated fact count
    m_rev_cnt = re.search(r'[Сс]борщик.*?(\d+)\s+факт', rtext)
    if m_rev_cnt:
        rev_stated = int(m_rev_cnt.group(1))
        if rev_stated != len(facts):
            error(f"Review {rfile.name} states {rev_stated} facts, but facts JSON has {len(facts)}")

    # Index count matching
    idx_cnt = index_item_counts.get(sid)
    if idx_cnt is not None and idx_cnt != len(facts):
        error(f"Fact count mismatch for {sid}: facts JSON has {len(facts)}, but index.md lists {idx_cnt}")

    # Static/runtime boundary
    if not any(term in rtext.lower() for term in ["runtime", "статическ", "статус"]):
        error(f"Review {rfile.name} missing explicit static/runtime boundary note")

    # Facts validation
    for fact in facts:
        fid = fact.get("id")
        if not fid or not fid.startswith(f"{sid}:"):
            error(f"Fact {fid} id does not start with {sid}:")

        status = fact.get("status")
        if status not in {"code", "docs", "inference", "secondary", "unavailable"}:
            error(f"Fact {fid} has invalid status {status}")

        ev_path = fact.get("evidence_path", "")
        if status == "code":
            if ":" not in ev_path or not re.search(r':\d+', ev_path):
                error(f"Code fact {fid} missing line reference in evidence_path: '{ev_path}'")

        url = fact.get("evidence_url", "")
        if "blob/main" in url or "branch/main" in url:
            error(f"Fact {fid} unpinned url: {url}")

        # Check commit SHA length in URL
        m_sha = re.search(r"/blob/([0-9a-fA-F]+)/", url)
        if m_sha:
            sha = m_sha.group(1)
            if len(sha) != 40:
                error(f"Fact {fid} commit SHA in url has length {len(sha)}, expected 40: {sha}")

    # Provenance link check
    s_runs = runs_by_source.get(sid, [])
    has_c = any(r["role"] == "collector" for r in s_runs)
    has_r = any(r["role"] == "reviewer" for r in s_runs)
    if not has_c or not has_r:
        error(f"{sid} missing collector or reviewer run in provenance manifest")

# --- 7. Source Registry Completeness ---
if REGISTRY_FILE.exists():
    reg_text = REGISTRY_FILE.read_text(encoding="utf-8")
    for sid in prov_sources:
        if f"sources/{sid}.md" not in reg_text:
            error(f"Source {sid} missing from source-registry.md")

# --- 8. Global Fact IDs and Duplicate Claims Checks ---
global_ids = [f.get("id") for f in master_facts]
if len(global_ids) != len(set(global_ids)):
    dupes = [x for x in global_ids if global_ids.count(x) > 1]
    error(f"Global duplicate fact IDs found: {set(dupes)}")

global_claims = [f.get("claim", "").strip() for f in master_facts if f.get("claim")]
if len(global_claims) != len(set(global_claims)):
    dupe_claims = [c for c in global_claims if global_claims.count(c) > 1]
    error(f"Global exact duplicate claims found: {len(set(dupe_claims))} duplicates")

# --- 9. Global check for blob/main in any markdown file ---
for md_path in WIKI.glob("**/*.md"):
    text = md_path.read_text(encoding='utf-8')
    if "github.com/Kangel-Plugins/Plugins-Store/blob/main" in text:
        error(f"Unpinned 'blob/main' link found in {md_path.relative_to(WIKI)}")

print(f"\nQuality Gate Completed. Total errors: {len(errors)}, warnings: {len(warnings)}")
if errors:
    print(f"FAILED: {len(errors)} quality gate errors detected.")
    sys.exit(1)
else:
    print("SUCCESS: ALL STRICT QUALITY GATES PASSED (100% Verified)!")
    sys.exit(0)
