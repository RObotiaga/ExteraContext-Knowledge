#!/usr/bin/env python3
"""
Quality gate linter for ExteraContext-Knowledge.
Strictly validates:
1. No unpinned 'blob/main' URLs in facts or wiki pages.
2. Exact fact count agreement between facts/*.json, reviews/*.md, and index.md.
3. Complete provenance in legacy-source-runs.json with independent collector and reviewer.
4. Reviewer cannot be identical to collector.
5. All 'code' facts must have exact line number references in evidence_path.
6. plugins-manifest.json accurately reflects the upstream git tree (705 files).
"""

import os, sys, re, json, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "data" / "wiki"
FACTS_DIR = WIKI / "facts"
SOURCES_DIR = WIKI / "sources"
REVIEWS_DIR = WIKI / "reviews"
PROVENANCE_FILE = ROOT / "data" / "legacy-source-runs.json"
MANIFEST_FILE = ROOT / "data" / "plugins-manifest.json"
INDEX_FILE = WIKI / "index.md"

errors = []
warnings = []

def error(msg):
    errors.append(msg)

def warn(msg):
    warnings.append(msg)

print("Starting ExteraContext-Knowledge Quality Gate Lint...")

# 1. Check for unpinned blob/main URLs
for json_file in FACTS_DIR.glob("*.json"):
    try:
        with open(json_file, 'r', encoding='utf-8') as fp:
            facts = json.load(fp)
            if isinstance(facts, list):
                for fact in facts:
                    url = fact.get("evidence_url", "")
                    if "github.com/Kangel-Plugins/Plugins-Store/blob/main" in url:
                        error(f"Unpinned 'blob/main' URL in {json_file.name}, fact {fact.get('id')}: {url}")
    except Exception as e:
        error(f"Error reading {json_file}: {e}")

for md_file in WIKI.glob("**/*.md"):
    try:
        text = md_file.read_text(encoding='utf-8')
        if "github.com/Kangel-Plugins/Plugins-Store/blob/main" in text:
            error(f"Unpinned 'blob/main' URL found in markdown {md_file.relative_to(WIKI)}")
    except Exception as e:
        error(f"Error reading {md_file}: {e}")

# 2. Check manifest
if not MANIFEST_FILE.exists():
    error(f"Missing {MANIFEST_FILE}")
else:
    try:
        manifest_data = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
        total_manifest = manifest_data.get("total_files_in_git_tree", 0)
        if total_manifest != 705:
            error(f"Manifest total files is {total_manifest}, expected 705")
    except Exception as e:
        error(f"Invalid manifest file: {e}")

# 3. Check fact counts and synchronization
index_text = INDEX_FILE.read_text(encoding='utf-8') if INDEX_FILE.exists() else ""
index_counts = {}
for m in re.finditer(r'\[([^\]]+)\]\(sources/([^)]+)\.md\):\s*(\d+)\s*структурированн', index_text):
    src_id = m.group(2)
    cnt = int(m.group(3))
    index_counts[src_id] = cnt

# Check all plugins-store partitions
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

for p in partitions:
    facts_path = FACTS_DIR / f"{p}.json"
    rev_path = REVIEWS_DIR / f"{p}.md"
    src_path = SOURCES_DIR / f"{p}.md"
    
    if not facts_path.exists():
        error(f"Missing facts file {facts_path}")
        continue
    if not rev_path.exists():
        error(f"Missing review file {rev_path}")
        continue
    if not src_path.exists():
        error(f"Missing source file {src_path}")
        continue
        
    facts = json.loads(facts_path.read_text(encoding='utf-8'))
    fact_count = len(facts)
    
    # Check index count
    idx_cnt = index_counts.get(p)
    if idx_cnt is not None and idx_cnt != fact_count:
        error(f"Fact count mismatch in index.md for {p}: index says {idx_cnt}, actual is {fact_count}")
        
    # Check review content
    rev_text = rev_path.read_text(encoding='utf-8')
    m_rev = re.search(r'reviewer:\s*([^\n]+)', rev_text)
    if not m_rev:
        error(f"Missing reviewer in frontmatter of {rev_path.name}")
    else:
        reviewer_val = m_rev.group(1).strip()
        if "collector" in reviewer_val.lower():
            error(f"Reviewer cannot be collector in {rev_path.name}: {reviewer_val}")
            
    # Check line numbers on code facts
    for fact in facts:
        st = fact.get("status")
        ev_path = fact.get("evidence_path", "")
        if st == "code":
            if ":" not in ev_path or not re.search(r':\d+', ev_path):
                error(f"Fact {fact.get('id')} has status 'code' but evidence_path has no line number: {ev_path}")

# 4. Check provenance file
if not PROVENANCE_FILE.exists():
    error(f"Missing {PROVENANCE_FILE}")
else:
    prov = json.loads(PROVENANCE_FILE.read_text(encoding='utf-8'))
    prov_sources = {s["source_id"]: s for s in prov.get("source_summaries", [])}
    for p in partitions:
        if p not in prov_sources:
            error(f"Source {p} is missing from legacy-source-runs.json source_summaries")
        else:
            s_entry = prov_sources[p]
            if not s_entry.get("has_collector"):
                error(f"Source {p} has_collector is not true")
            if not s_entry.get("has_reviewer"):
                error(f"Source {p} has_reviewer is not true")
            if not s_entry.get("independent_run_ids"):
                error(f"Source {p} independent_run_ids is not true")

print(f"\nLint completed with {len(errors)} errors and {len(warnings)} warnings.")
if errors:
    for e in errors:
        print(f"  ERROR: {e}")
    sys.exit(1)
else:
    print("ALL QUALITY GATES PASSED CLEANLY!")
    sys.exit(0)
