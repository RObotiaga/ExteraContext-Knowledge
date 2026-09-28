#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

PROMPT_GLOB = "*.md"

def _m(pattern: str, text: str):
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else None

def parse_prompt(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    source_m = re.search(r"- Источник: `([^`]+)` — (.+)", text)
    role = "collector" if "- Роль: сборщик" in text else "reviewer" if "- Роль: независимый проверяющий" in text else None
    sub = re.search(r"- Субагент: `([^`]+)` \(`([^`]+)`\)", text)
    model = re.search(r"- Запрошенная модель: `([^`]+)`; reasoning: `([^`]+)`; `fork_turns`: `([^`]+)`", text)
    order = re.search(r"- Порядок запуска: `(\d+)` из `(\d+)`", text)
    raw = re.search(r"- Сохраненные входные материалы: `([^`]+)` — (.+)", text)
    task_match = re.search(r"- Назначение совпадает с финальным task name в pipeline: \*\*(.+?)\*\*", text)
    return {
        "order": int(order.group(1)) if order else None,
        "source_id": source_m.group(1) if source_m else None,
        "source_title": source_m.group(2).strip() if source_m else None,
        "role": role,
        "task_name": sub.group(1) if sub else None,
        "agent_path": sub.group(2) if sub else None,
        "call_id": _m(r"- Идентификатор вызова: `([^`]+)`", text),
        "started_at": _m(r"- UTC: `([^`]+)`", text),
        "model": model.group(1) if model else None,
        "reasoning": model.group(2) if model else None,
        "fork_turns": model.group(3) if model else None,
        "role_attempt": _m(r"- Номер запуска этой роли для источника: `([^`]+)`", text),
        "repository": _m(r"- Репозиторий/пакет: `([^`]+)`", text),
        "raw_materials": raw.group(1) if raw else None,
        "raw_materials_status": raw.group(2).strip() if raw else None,
        "wiki_source_page": _m(r"- Страница базы: `([^`]+)`", text),
        "task_name_matched": (task_match.group(1).strip().lower() == "да") if task_match else None,
        "prompt_reconstructed": "Реконструкция, не дословная стенограмма" in text,
        "prompt_file": path.name,
    }

def prompt_files(path: Path):
    if path.is_file() and path.suffix.lower() == ".zip":
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        with zipfile.ZipFile(path) as z:
            z.extractall(root)
        files = sorted(root.rglob("prompts/*.md"))
        return files, td
    files = sorted(path.rglob("prompts/*.md")) if path.is_dir() else []
    return files, None

def build_manifest(path: Path) -> dict:
    files, tmp = prompt_files(path)
    try:
        runs = [parse_prompt(p) for p in files]
        runs = [r for r in runs if r.get("source_id") and r.get("role")]
        runs.sort(key=lambda r: r.get("order") or 10**9)
        by_source = defaultdict(list)
        for r in runs:
            by_source[r["source_id"]].append(r)
        summaries = []
        for source_id, rs in sorted(by_source.items()):
            collectors = [r for r in rs if r["role"] == "collector"]
            reviewers = [r for r in rs if r["role"] == "reviewer"]
            ids = [r["call_id"] for r in rs if r.get("call_id")]
            summaries.append({
                "source_id": source_id,
                "collector_runs": len(collectors),
                "reviewer_runs": len(reviewers),
                "has_collector": bool(collectors),
                "has_reviewer": bool(reviewers),
                "independent_run_ids": bool(ids) and len(ids) == len(set(ids)) == len(rs),
                "review_mode": "independent-source-reread-nonblind",
                "all_fork_turns_none": all(r.get("fork_turns") == "none" for r in rs),
                "models": sorted({r["model"] for r in rs if r.get("model")}),
                "reasoning_levels": sorted({r["reasoning"] for r in rs if r.get("reasoning")}),
            })
        return {
            "schema_version": 1,
            "generated_from": path.name,
            "prompt_count": len(runs),
            "unique_sources": len(by_source),
            "notes": [
                "Prompt bodies are reconstructed from saved templates where indicated, not verbatim transcripts.",
                "Collector and reviewer runs are separate and fork_turns=none when recorded, but legacy reviewers were non-blind: they could inspect and edit collector outputs.",
                "Legacy review provenance does not imply runtime verification.",
            ],
            "runs": runs,
            "source_summaries": summaries,
        }
    finally:
        if tmp:
            tmp.cleanup()

def main():
    p = argparse.ArgumentParser(description="Parse legacy wiki collector/reviewer prompt logs into provenance JSON")
    p.add_argument("input", type=Path, help="agent-prompts.zip or extracted directory")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    manifest = build_manifest(args.input)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "out": str(args.out),
        "prompt_count": manifest["prompt_count"],
        "unique_sources": manifest["unique_sources"],
        "sources_with_reviewer": sum(1 for x in manifest["source_summaries"] if x["has_reviewer"]),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
