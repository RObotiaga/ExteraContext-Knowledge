from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'exteracontext.sqlite'
MANIFEST = ROOT / 'data' / 'legacy-source-runs.json'

manifest = json.loads(MANIFEST.read_text('utf-8'))
assert manifest['prompt_count'] == 174
assert manifest['unique_sources'] == 76
assert len(manifest['runs']) == 174
assert all(s['has_collector'] and s['has_reviewer'] for s in manifest['source_summaries'])
assert all(s['review_mode'] == 'independent-source-reread-nonblind' for s in manifest['source_summaries'])

con = sqlite3.connect(DB)
assert con.execute('select count(*) from source_runs').fetchone()[0] == 174
assert con.execute('select count(*) from source_provenance').fetchone()[0] == 76
assert con.execute('select count(*) from source_provenance where has_reviewer=1').fetchone()[0] == 76
row = con.execute("select collector_runs, reviewer_runs, review_mode from source_provenance where source_id='official-sdk'").fetchone()
assert row == (1, 1, 'independent-source-reread-nonblind')
con.close()

out = subprocess.check_output([
    sys.executable, str(ROOT / 'scripts' / 'query.py'), 'evidence',
    'official-sdk:sdk-baseline', '--format', 'json'
], text=True)
data = json.loads(out)
prov = data[0]['source_provenance']
assert prov['collector_runs'] == 1
assert prov['reviewer_runs'] == 1
assert prov['all_fork_turns_none'] == 1
assert prov['review_mode'] == 'independent-source-reread-nonblind'
assert {r['role'] for r in prov['runs']} == {'collector', 'reviewer'}
print('legacy-provenance: ok')
