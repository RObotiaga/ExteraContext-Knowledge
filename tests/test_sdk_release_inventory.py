from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "data" / "sdk-snapshots" / "release-inventory.json"
FACTS = ROOT / "data" / "wiki" / "facts" / "official-sdk-builds.json"

inv = json.loads(INV.read_text("utf-8"))
releases = inv["releases"]
facts = json.loads(FACTS.read_text("utf-8"))

assert inv["source_id"] == "official-sdk-builds"
assert len(releases) >= 14
assert len({r["tag"] for r in releases}) == len(releases)
assert all(r["sdk_version"] and r["channel"] and r["build"] and r["commit"] for r in releases)
assert all(r["stubs"] and r["stubs"]["digest"].startswith("sha256:") for r in releases)
identity = [(r["sdk_version"], r["channel"], r["build"], r["tag"], r["commit"]) for r in releases]
assert len(identity) == len(set(identity))
counts = Counter(r["sdk_version"] for r in releases)
for version in ["1.4.3.9", "1.4.4.1", "1.4.5.0"]:
    assert counts[version] >= 2
    xs = [r for r in releases if r["sdk_version"] == version]
    assert len({r["stubs"]["digest"] for r in xs}) >= 2
assert any(r["channel"] == "beta" and r["github_prerelease"] is False for r in releases)
ids = {f["id"] for f in facts}
assert "official-sdk-builds:snapshot-identity" in ids
assert "official-sdk-builds:stubs-symbol-diff-pending" in ids
print({"sdk_releases": len(releases), "sdk_facts": len(facts)})
