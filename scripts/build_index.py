#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WIKI = SKILL_ROOT / "data" / "wiki"
DEFAULT_DB = SKILL_ROOT / "data" / "exteracontext.sqlite"
DEFAULT_PROVENANCE = SKILL_ROOT / "data" / "legacy-source-runs.json"

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


def build(wiki: Path, db: Path, provenance: Path | None = None) -> None:
    facts_path = wiki / "facts.json"
    if not facts_path.exists():
        raise SystemExit(f"facts.json not found: {facts_path}")
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    if not isinstance(facts, list):
        raise SystemExit("wiki/facts.json must contain a list")

    provenance_data = None
    provenance_path = provenance or DEFAULT_PROVENANCE
    if provenance_path and provenance_path.exists():
        provenance_data = json.loads(provenance_path.read_text(encoding="utf-8"))

    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()

    con = sqlite3.connect(db)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
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
            id UNINDEXED,
            claim,
            api,
            recipe,
            topic,
            canonical_topic,
            source_id,
            version,
            platform,
            tokenize='unicode61 remove_diacritics 2'
        );
        CREATE TABLE docs(
            path TEXT PRIMARY KEY,
            title TEXT,
            kind TEXT,
            content TEXT
        );
        CREATE VIRTUAL TABLE docs_fts USING fts5(
            path UNINDEXED,
            title,
            content,
            kind,
            tokenize='unicode61 remove_diacritics 2'
        );
        CREATE TABLE source_runs(
            call_id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            source_title TEXT,
            role TEXT NOT NULL CHECK(role IN ('collector','reviewer')),
            task_name TEXT,
            agent_path TEXT,
            started_at TEXT,
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
            run_order INTEGER
        );
        CREATE INDEX source_runs_source_idx ON source_runs(source_id, role);
        CREATE TABLE source_provenance(
            source_id TEXT PRIMARY KEY,
            collector_runs INTEGER NOT NULL DEFAULT 0,
            reviewer_runs INTEGER NOT NULL DEFAULT 0,
            has_collector INTEGER NOT NULL DEFAULT 0,
            has_reviewer INTEGER NOT NULL DEFAULT 0,
            independent_run_ids INTEGER NOT NULL DEFAULT 0,
            review_mode TEXT,
            all_fork_turns_none INTEGER NOT NULL DEFAULT 0,
            models_json TEXT NOT NULL DEFAULT '[]',
            reasoning_levels_json TEXT NOT NULL DEFAULT '[]'
        );
        CREATE INDEX facts_api_idx ON facts(api);
        CREATE INDEX facts_source_idx ON facts(source_id);
        CREATE INDEX facts_status_idx ON facts(status);
        CREATE INDEX docs_kind_idx ON docs(kind);
        """
    )

    fact_cols = [
        "id", "topic", "claim", "api", "evidence_url", "evidence_path", "version",
        "status", "recipe", "source_id", "source_fact_id", "original_status",
        "canonical_topic", "review_status", "platform"
    ]
    for fact in facts:
        row = [str(fact.get(c, "") or "") for c in fact_cols]
        con.execute(
            f"INSERT INTO facts({','.join(fact_cols)}) VALUES ({','.join('?' for _ in fact_cols)})",
            row,
        )
        con.execute(
            "INSERT INTO facts_fts(id,claim,api,recipe,topic,canonical_topic,source_id,version,platform) VALUES (?,?,?,?,?,?,?,?,?)",
            (
                fact.get("id", ""), fact.get("claim", ""), fact.get("api", ""),
                fact.get("recipe", ""), fact.get("topic", ""), fact.get("canonical_topic", ""),
                fact.get("source_id", ""), fact.get("version", ""), fact.get("platform", "")
            ),
        )

    source_run_count = 0
    source_provenance_count = 0
    if provenance_data:
        for run in provenance_data.get("runs", []):
            con.execute(
                """INSERT OR REPLACE INTO source_runs(
                    call_id,source_id,source_title,role,task_name,agent_path,started_at,model,reasoning,
                    fork_turns,role_attempt,repository,raw_materials,raw_materials_status,wiki_source_page,
                    task_name_matched,prompt_reconstructed,prompt_file,run_order
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    run.get("call_id"), run.get("source_id"), run.get("source_title"), run.get("role"),
                    run.get("task_name"), run.get("agent_path"), run.get("started_at"), run.get("model"),
                    run.get("reasoning"), run.get("fork_turns"), run.get("role_attempt"), run.get("repository"),
                    run.get("raw_materials"), run.get("raw_materials_status"), run.get("wiki_source_page"),
                    int(bool(run.get("task_name_matched"))) if run.get("task_name_matched") is not None else None,
                    int(bool(run.get("prompt_reconstructed"))), run.get("prompt_file"), run.get("order"),
                ),
            )
            source_run_count += 1
        for s in provenance_data.get("source_summaries", []):
            con.execute(
                """INSERT OR REPLACE INTO source_provenance(
                    source_id,collector_runs,reviewer_runs,has_collector,has_reviewer,independent_run_ids,
                    review_mode,all_fork_turns_none,models_json,reasoning_levels_json
                ) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    s.get("source_id"), int(s.get("collector_runs", 0)), int(s.get("reviewer_runs", 0)),
                    int(bool(s.get("has_collector"))), int(bool(s.get("has_reviewer"))),
                    int(bool(s.get("independent_run_ids"))), s.get("review_mode"),
                    int(bool(s.get("all_fork_turns_none"))),
                    json.dumps(s.get("models", []), ensure_ascii=False),
                    json.dumps(s.get("reasoning_levels", []), ensure_ascii=False),
                ),
            )
            source_provenance_count += 1

    doc_count = 0
    for path in sorted(wiki.rglob("*.md")):
        # The per-source fact JSON is indexed above; markdown is useful as synthesized context.
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(wiki).as_posix()
        title = title_from_markdown(text, path.stem)
        kind = kind_for(path, wiki)
        con.execute("INSERT INTO docs(path,title,kind,content) VALUES (?,?,?,?)", (rel, title, kind, text))
        con.execute("INSERT INTO docs_fts(path,title,content,kind) VALUES (?,?,?,?)", (rel, title, text, kind))
        doc_count += 1

    status_counts = {}
    for fact in facts:
        status_counts[fact.get("status", "unknown")] = status_counts.get(fact.get("status", "unknown"), 0) + 1
    meta = {
        "facts": len(facts),
        "docs": doc_count,
        "status_counts": status_counts,
        "wiki_root": str(wiki),
        "source_runs": source_run_count,
        "source_provenance": source_provenance_count,
    }
    for k, v in meta.items():
        con.execute("INSERT INTO meta(key,value) VALUES (?,?)", (k, json.dumps(v, ensure_ascii=False)))
    con.commit()
    con.close()
    print(json.dumps(meta, ensure_ascii=False, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description="Build the local ExteraContext SQLite/FTS5 index")
    p.add_argument("--wiki", type=Path, default=DEFAULT_WIKI)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    args = p.parse_args()
    build(args.wiki.resolve(), args.db.resolve(), args.provenance.resolve() if args.provenance else None)


if __name__ == "__main__":
    main()
