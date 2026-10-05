#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WIKI = SKILL_ROOT / "data" / "wiki"
DEFAULT_DB = SKILL_ROOT / "data" / "exteracontext.sqlite"
DEFAULT_PROVENANCE = SKILL_ROOT / "data" / "legacy-source-runs.json"
SUPPORTED_PROVENANCE_SCHEMAS = {1, 2}

DOC_KINDS = {
    "recipes": "recipe",
    "topics": "topic",
    "sources": "source",
    "reviews": "review",
    "entities": "entity",
    "apis": "api-index",
}


def title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def kind_for(path: Path, wiki: Path) -> str:
    rel = path.relative_to(wiki)
    if len(rel.parts) > 1 and rel.parts[0] in DOC_KINDS:
        return DOC_KINDS[rel.parts[0]]
    return "core"


def _normalize_v1_provenance(data: dict[str, Any]) -> dict[str, Any]:
    """Adapt legacy schema v1 in memory without fabricating call IDs or provenance."""
    runs = []
    for original in data.get("runs", []):
        r = dict(original)
        call_id = r.get("call_id")
        r["run_id"] = r.get("run_id") or call_id
        if not r["run_id"]:
            raise ValueError("schema v1 run has no call_id; cannot construct a truthful run identity")
        r["provenance_kind"] = r.get("provenance_kind") or "legacy-agent-run"
        r.setdefault("date", None)
        r.setdefault("prompt_archive", None)
        r.setdefault("produced_facts_count", None)
        r.setdefault("reviewed_facts_count", None)
        runs.append(r)

    summaries = []
    by_source: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        by_source.setdefault(run["source_id"], []).append(run)
    for old in data.get("source_summaries", []):
        s = dict(old)
        src_runs = by_source.get(s["source_id"], [])
        ids = [r["run_id"] for r in src_runs]
        # The legacy v1 boolean only said that IDs were distinct; v1 call IDs are the
        # actual available identifiers, so use them only when all are present/distinct.
        if not isinstance(s.get("independent_run_ids"), list):
            if ids and len(ids) == len(set(ids)):
                s["independent_run_ids"] = ids
            else:
                s["independent_run_ids"] = None
        s.setdefault("facts_count", None)
        s.setdefault("review_status", None)
        s.setdefault("provenance_kinds", sorted({r["provenance_kind"] for r in src_runs}))
        summaries.append(s)
    return {**data, "schema_version": 2, "runs": runs, "source_summaries": summaries}


def validate_provenance(data: dict[str, Any], facts: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("provenance manifest must be a JSON object")
    schema_version = data.get("schema_version")
    if schema_version not in SUPPORTED_PROVENANCE_SCHEMAS:
        raise ValueError(f"unsupported provenance schema_version: {schema_version!r}")
    if schema_version == 1:
        data = _normalize_v1_provenance(data)
    elif schema_version != 2:
        raise ValueError(f"unsupported provenance schema_version: {schema_version!r}")

    runs = data.get("runs")
    summaries = data.get("source_summaries")
    if not isinstance(runs, list) or not isinstance(summaries, list):
        raise ValueError("schema v2 requires runs and source_summaries arrays")

    run_ids: list[str] = []
    by_source: dict[str, list[dict[str, Any]]] = {}
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            raise ValueError(f"run {index} must be an object")
        run_id, source_id, role, kind = (run.get("run_id"), run.get("source_id"), run.get("role"), run.get("provenance_kind"))
        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError(f"run {index} missing stable run_id")
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError(f"run {run_id} missing source_id")
        if role not in {"collector", "reviewer"}:
            raise ValueError(f"run {run_id} has invalid role {role!r}")
        if not isinstance(kind, str) or not kind.strip():
            raise ValueError(f"run {run_id} missing provenance_kind")
        run_ids.append(run_id)
        by_source.setdefault(source_id, []).append(run)
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("duplicate run_id in provenance manifest")

    summary_ids = [s.get("source_id") for s in summaries if isinstance(s, dict)]
    if len(summary_ids) != len(summaries) or any(not sid for sid in summary_ids):
        raise ValueError("each source summary must be an object with source_id")
    if len(summary_ids) != len(set(summary_ids)):
        raise ValueError("duplicate source_id in source_summaries")

    fact_counts: dict[str, int] = {}
    for fact in facts:
        sid = fact.get("source_id")
        if sid:
            fact_counts[sid] = fact_counts.get(sid, 0) + 1

    summary_set = set(summary_ids)
    run_source_set = set(by_source)
    if run_source_set - summary_set:
        raise ValueError(f"runs have sources without summaries: {sorted(run_source_set - summary_set)}")
    if summary_set - run_source_set:
        raise ValueError(f"source summaries have no run records: {sorted(summary_set - run_source_set)}")

    for summary in summaries:
        sid = summary["source_id"]
        source_runs = by_source.get(sid, [])
        c_runs = [r for r in source_runs if r["role"] == "collector"]
        r_runs = [r for r in source_runs if r["role"] == "reviewer"]
        expected_c, expected_r = len(c_runs), len(r_runs)
        if summary.get("collector_runs") != expected_c or summary.get("reviewer_runs") != expected_r:
            raise ValueError(f"{sid}: summary collector/reviewer counts do not match run rows ({expected_c}/{expected_r})")
        if summary.get("has_collector") is not (expected_c > 0):
            raise ValueError(f"{sid}: has_collector conflicts with collector run count")
        if summary.get("has_reviewer") is not (expected_r > 0):
            raise ValueError(f"{sid}: has_reviewer conflicts with reviewer run count")
        ids = summary.get("independent_run_ids")
        if ids is not None:
            if not isinstance(ids, list) or len(ids) != len(set(ids)):
                raise ValueError(f"{sid}: independent_run_ids must be a unique list or null")
            actual = {r["run_id"] for r in source_runs}
            if not set(ids).issubset(actual):
                raise ValueError(f"{sid}: independent_run_ids reference other sources or missing runs")
            if expected_c and expected_r:
                cids = {r["run_id"] for r in c_runs}
                rids = {r["run_id"] for r in r_runs}
                if not (set(ids) & cids) or not (set(ids) & rids):
                    raise ValueError(f"{sid}: independent_run_ids do not include collector and reviewer")
                if not (set(ids) & cids).isdisjoint(set(ids) & rids):
                    raise ValueError(f"{sid}: collector and reviewer run identities overlap")
        fork_value = summary.get("all_fork_turns_none")
        if fork_value is not None and not isinstance(fork_value, bool):
            raise ValueError(f"{sid}: all_fork_turns_none must be bool or null")
        if any(r.get("fork_turns") is None for r in source_runs) and fork_value is True:
            raise ValueError(f"{sid}: cannot assert all_fork_turns_none when a run's fork_turns is unknown")
        actual_fact_count = fact_counts.get(sid, 0)
        if summary.get("facts_count") is not None and summary["facts_count"] != actual_fact_count:
            raise ValueError(f"{sid}: facts_count {summary['facts_count']} != indexed fact count {actual_fact_count}")

    return data


def build(wiki: Path, db: Path, provenance: Path | None = None) -> None:
    facts_path = wiki / "facts.json"
    if not facts_path.exists():
        raise SystemExit(f"facts.json not found: {facts_path}")
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    if not isinstance(facts, list):
        raise SystemExit("wiki/facts.json must contain a list")
    fact_ids = [f.get("id") for f in facts]
    if any(not isinstance(fid, str) or not fid.strip() for fid in fact_ids):
        raise SystemExit("wiki/facts.json contains missing/empty fact id")
    if len(fact_ids) != len(set(fact_ids)):
        raise SystemExit("wiki/facts.json contains duplicate fact ids")

    provenance_path = provenance or DEFAULT_PROVENANCE
    if provenance_path is None or not provenance_path.exists():
        raise SystemExit(f"provenance manifest not found: {provenance_path}")
    try:
        provenance_data = validate_provenance(json.loads(provenance_path.read_text(encoding="utf-8")), facts)
    except (ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"invalid provenance manifest: {exc}") from exc

    db.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{db.name}.", suffix=".tmp", dir=str(db.parent))
    os.close(fd)
    tmp_db = Path(tmp_name)
    con: sqlite3.Connection | None = None
    try:
        con = sqlite3.connect(tmp_db)
        con.execute("PRAGMA journal_mode=DELETE")
        con.execute("PRAGMA synchronous=FULL")
        con.execute("PRAGMA foreign_keys=ON")
        con.executescript(
            """
            CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE facts(
                id TEXT PRIMARY KEY,
                topic TEXT,
                claim TEXT,
                api TEXT,
                evidence_url TEXT,
                evidence_path TEXT,
                version TEXT,
                status TEXT,
                recipe TEXT,
                source_id TEXT,
                source_fact_id TEXT,
                original_status TEXT,
                canonical_topic TEXT,
                review_status TEXT,
                platform TEXT
            );
            CREATE VIRTUAL TABLE facts_fts USING fts5(
                id UNINDEXED, claim, api, recipe, topic, canonical_topic, source_id, version, platform,
                tokenize='unicode61 remove_diacritics 2'
            );
            CREATE TABLE docs(path TEXT PRIMARY KEY,title TEXT,kind TEXT,content TEXT);
            CREATE VIRTUAL TABLE docs_fts USING fts5(path UNINDEXED,title,content,kind,tokenize='unicode61 remove_diacritics 2');
            CREATE TABLE source_runs(
                run_id TEXT PRIMARY KEY,
                call_id TEXT,
                source_id TEXT NOT NULL,
                source_title TEXT,
                role TEXT NOT NULL CHECK(role IN ('collector','reviewer')),
                provenance_kind TEXT NOT NULL,
                task_name TEXT,
                agent_path TEXT,
                started_at TEXT,
                date TEXT,
                model TEXT,
                reasoning TEXT,
                fork_turns TEXT,
                role_attempt TEXT,
                repository TEXT,
                raw_materials TEXT,
                raw_materials_status TEXT,
                wiki_source_page TEXT,
                task_name_matched INTEGER,
                prompt_reconstructed INTEGER,
                prompt_file TEXT,
                prompt_archive TEXT,
                run_order INTEGER,
                produced_facts_count INTEGER,
                reviewed_facts_count INTEGER
            );
            CREATE INDEX source_runs_source_idx ON source_runs(source_id,role);
            CREATE TABLE source_provenance(
                source_id TEXT PRIMARY KEY,
                collector_runs INTEGER NOT NULL,
                reviewer_runs INTEGER NOT NULL,
                has_collector INTEGER NOT NULL,
                has_reviewer INTEGER NOT NULL,
                independent_run_ids INTEGER,
                independent_run_ids_json TEXT,
                review_mode TEXT,
                all_fork_turns_none INTEGER,
                models_json TEXT,
                reasoning_levels_json TEXT,
                provenance_kinds_json TEXT,
                facts_count INTEGER,
                review_status TEXT
            );
            CREATE INDEX facts_api_idx ON facts(api);
            CREATE INDEX facts_source_idx ON facts(source_id);
            CREATE INDEX facts_status_idx ON facts(status);
            CREATE INDEX docs_kind_idx ON docs(kind);
            """
        )

        fact_cols = [
            "id", "topic", "claim", "api", "evidence_url", "evidence_path", "version", "status", "recipe",
            "source_id", "source_fact_id", "original_status", "canonical_topic", "review_status", "platform"
        ]
        for fact in facts:
            row = [fact.get(col) for col in fact_cols]
            con.execute(f"INSERT INTO facts({','.join(fact_cols)}) VALUES ({','.join('?' for _ in fact_cols)})", row)
            con.execute(
                "INSERT INTO facts_fts(id,claim,api,recipe,topic,canonical_topic,source_id,version,platform) VALUES (?,?,?,?,?,?,?,?,?)",
                tuple(fact.get(col) for col in ["id", "claim", "api", "recipe", "topic", "canonical_topic", "source_id", "version", "platform"]),
            )

        runs = provenance_data["runs"]
        summaries = provenance_data["source_summaries"]
        for run in runs:
            columns = [
                "run_id", "call_id", "source_id", "source_title", "role", "provenance_kind", "task_name", "agent_path",
                "started_at", "date", "model", "reasoning", "fork_turns", "role_attempt", "repository", "raw_materials",
                "raw_materials_status", "wiki_source_page", "task_name_matched", "prompt_reconstructed", "prompt_file",
                "prompt_archive", "order", "produced_facts_count", "reviewed_facts_count"
            ]
            row = [run.get(col) for col in columns]
            row[18] = None if row[18] is None else int(bool(row[18]))
            row[19] = None if row[19] is None else int(bool(row[19]))
            con.execute(f"INSERT INTO source_runs({','.join('run_order' if c == 'order' else c for c in columns)}) VALUES ({','.join('?' for _ in columns)})", row)

        for summary in summaries:
            ids = summary.get("independent_run_ids")
            fork = summary.get("all_fork_turns_none")
            models = summary.get("models")
            reasoning = summary.get("reasoning_levels")
            kinds = summary.get("provenance_kinds")
            values = (
                summary["source_id"], summary["collector_runs"], summary["reviewer_runs"],
                int(summary["has_collector"]), int(summary["has_reviewer"]),
                None if ids is None else int(bool(ids)),
                None if ids is None else json.dumps(ids, ensure_ascii=False),
                summary.get("review_mode"), None if fork is None else int(fork),
                None if models is None else json.dumps(models, ensure_ascii=False),
                None if reasoning is None else json.dumps(reasoning, ensure_ascii=False),
                None if kinds is None else json.dumps(kinds, ensure_ascii=False),
                summary.get("facts_count"), summary.get("review_status"),
            )
            con.execute(
                "INSERT INTO source_provenance(source_id,collector_runs,reviewer_runs,has_collector,has_reviewer,independent_run_ids,independent_run_ids_json,review_mode,all_fork_turns_none,models_json,reasoning_levels_json,provenance_kinds_json,facts_count,review_status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                values,
            )

        doc_count = 0
        for path in sorted(wiki.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(wiki).as_posix()
            title = title_from_markdown(text, path.stem)
            kind = kind_for(path, wiki)
            con.execute("INSERT INTO docs(path,title,kind,content) VALUES (?,?,?,?)", (rel, title, kind, text))
            con.execute("INSERT INTO docs_fts(path,title,content,kind) VALUES (?,?,?,?)", (rel, title, text, kind))
            doc_count += 1

        status_counts: dict[str, int] = {}
        for fact in facts:
            status = fact.get("status")
            key = status if status is not None else "unknown"
            status_counts[key] = status_counts.get(key, 0) + 1

        try:
            wiki_root = wiki.resolve().relative_to(SKILL_ROOT.resolve()).as_posix()
        except ValueError:
            wiki_root = "external"
        meta = {
            "facts": len(facts),
            "docs": doc_count,
            "status_counts": status_counts,
            "wiki_root": wiki_root,
            "source_runs": len(runs),
            "source_provenance": len(summaries),
            "provenance_schema_version": provenance_data["schema_version"],
            "legacy_prompt_count": provenance_data.get("legacy_prompt_count"),
            "legacy_unique_sources": provenance_data.get("legacy_unique_sources"),
            "post_legacy_runs": provenance_data.get("post_legacy_runs"),
            "direct_capture_runs": provenance_data.get("direct_capture_runs"),
        }
        for key, value in meta.items():
            con.execute("INSERT INTO meta(key,value) VALUES (?,?)", (key, json.dumps(value, ensure_ascii=False)))
        con.commit()
        integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity_check failed: {integrity}")
        con.close()
        con = None
        os.replace(tmp_db, db)
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    except Exception:
        if con is not None:
            con.rollback()
            con.close()
        for suffix in ("", "-wal", "-shm"):
            candidate = Path(str(tmp_db) + suffix)
            try:
                candidate.unlink(missing_ok=True)
            except Exception:
                pass
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the local ExteraContext SQLite/FTS5 index")
    parser.add_argument("--wiki", type=Path, default=DEFAULT_WIKI)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    args = parser.parse_args()
    build(args.wiki.resolve(), args.db.resolve(), args.provenance.resolve() if args.provenance else None)

if __name__ == "__main__":
    main()
