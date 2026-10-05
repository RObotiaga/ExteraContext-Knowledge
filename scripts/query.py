#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
WIKI = Path(os.environ.get("EXTERACONTEXT_WIKI", SKILL_ROOT / "data" / "wiki"))
DB = Path(os.environ.get("EXTERACONTEXT_DB", SKILL_ROOT / "data" / "exteracontext.sqlite"))

STATUS_SCORE = {
    "runtime-verified": 8.0,
    "code": 4.0,
    "docs": 3.0,
    "inference": 1.5,
    "secondary": 0.5,
    "unavailable": -4.0,
}

DIRECT_SOURCES = {
    "official-sdk", "exteragram-docs", "exteragram-utils", "exteragram-mcp",
    "exteragram-mcp-npm", "for-vibecoders", "extcli", "altylib", "catalib",
    "gradle-plugin", "template-n08", "template-robotiaga", "plugins-store",
    "plugins-store-codeberg", "plugins-store-gitverse", "vestr-plugins",
}
DONOR_PREFIXES = (
    "ayugram", "nagram", "nekogram", "nekox", "niagram", "novagram", "nullgram",
    "nullcoregram", "octogram", "cherrygram", "mercurygram", "miogram", "amegram",
    "vibogram", "reqgram", "opexgram", "televip",
)
OFFICIAL_SOURCES = {"official-sdk", "exteragram-docs", "exteragram-utils"}

COMMON_CROSS_CLIENT_IDENTIFIERS = {
    "messageobject", "tlobject", "notificationcenter", "chatactivity", "launchactivity",
    "sendmessageshelper", "tlrpc", "android", "telegram", "java", "python",
}

STOP = {
    "как", "что", "для", "или", "это", "при", "над", "под", "мне", "нужно", "сделать",
    "the", "and", "for", "with", "from", "into", "how", "use", "using", "plugin", "плагин",
    "exteragram", "exteragramm", "exteragram", "ayugram",
}

ALIASES = {
    "исход": ["outgoing", "send", "message"],
    "отправ": ["send", "outgoing", "request"],
    "сообщ": ["message", "MessageObject"],
    "контекст": ["context", "menu"],
    "меню": ["menu", "action"],
    "перехват": ["hook", "intercept"],
    "хук": ["hook", "xposed"],
    "hook": ["xposed", "callback"],
    "аккаунт": ["account", "multi-account"],
    "поток": ["thread", "ui", "background"],
    "интерфейс": ["ui", "view"],
    "настрой": ["settings", "preferences"],
    "медиа": ["media", "document", "photo"],
    "файл": ["file", "document"],
    "скач": ["download", "file"],
    "загруз": ["load", "download", "upload"],
    "выгруз": ["unload", "cleanup", "lifecycle"],
    "перезагруз": ["reload", "unload", "load"],
    "рефлек": ["reflection", "java", "xposed"],
    "java": ["reflection", "xposed", "Member"],
    "dex": ["dex", "jvm", "classloader"],
    "запрос": ["request", "send_request", "TLRPC"],
    "сеть": ["network", "request"],
    "хранил": ["storage", "cache"],
    "кэш": ["cache", "ttl"],
    "кеш": ["cache", "ttl"],
    "ошиб": ["debug", "error", "exception"],
    "сбор": ["build", "package", "elyx"],
    "elyx": ["archive", "entry", "builder"],
    "фон": ["background", "queue", "run_on_queue"],
    "обнов": ["ui", "run_on_ui_thread"],
    "измен": ["modify", "HookResult", "HookStrategy"],
    "импорт": ["import", "import_module"],
    "обработ": ["handler", "callback"],
    "расшир": ["extension", "FileInfo", "FilesController"],
    "metadata": ["метадан", "__id__", "__name__"],
    "метадан": ["metadata", "__id__", "__name__"],
    "permission": ["permissions", "разреш"],
    "разреш": ["permission", "permissions"],
    "intent": ["IntentsManager", "handler", "path"],
    "reload": ["lifecycle", "unload", "cleanup"],
    "приостан": ["pause", "AppEvent"],
    "возобнов": ["resume", "AppEvent"],
    "background": ["background", "pause", "queue"],
    "live": ["sync", "reload", "elyx_changes"],
}


def ensure_db() -> None:
    if DB.exists():
        return
    build_script = SKILL_ROOT / "scripts" / "build_index.py"
    if build_script.is_file() and WIKI.is_dir():
        subprocess.run(
            [sys.executable, str(build_script), "--wiki", str(WIKI), "--db", str(DB)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        return
    raise FileNotFoundError(f"Database not found at {DB}")


def con() -> sqlite3.Connection:
    ensure_db()
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def words(q: str) -> list[str]:
    raw = re.findall(r"[A-Za-zА-Яа-яЁё0-9_.$:@+-]+", q.lower())
    out: list[str] = []
    for w in raw:
        if len(w) < 2 or w in STOP:
            continue
        out.append(w)
        for stem, vals in ALIASES.items():
            if w.startswith(stem):
                out.extend(v.lower() for v in vals)
    seen = set()
    return [x for x in out if not (x in seen or seen.add(x))]


def fts_query(q: str) -> str:
    toks = words(q)
    if not toks:
        toks = [q.strip().lower()] if q.strip() else []
    safe = []
    for t in toks[:24]:
        t = re.sub(r"[^A-Za-zА-Яа-яЁё0-9_]", "", t)
        if len(t) >= 2:
            safe.append(f'"{t}"*')
    return " OR ".join(safe)


def source_bonus(source_id: str) -> float:
    s = (source_id or "").lower()
    if s in OFFICIAL_SOURCES:
        return 5.0
    if s in DIRECT_SOURCES or s.startswith("plugins-store-"):
        return 2.5
    if s.startswith(DONOR_PREFIXES):
        return -0.5
    return 0.5


def directness(source_id: str) -> str:
    s = (source_id or "").lower()
    if s in OFFICIAL_SOURCES:
        return "official"
    if s in DIRECT_SOURCES or s.startswith("plugins-store-"):
        return "target-ecosystem"
    if s.startswith(DONOR_PREFIXES):
        return "donor"
    return "other"


def row_dict(r: sqlite3.Row) -> dict[str, Any]:
    return {k: r[k] for k in r.keys()}


def search_facts(q: str, limit: int = 12) -> list[dict[str, Any]]:
    match = fts_query(q)
    if not match:
        return []
    c = con()
    rows = c.execute(
        """
        SELECT f.*, bm25(facts_fts, 4.0, 7.0, 3.0, 1.5, 1.5, 1.0, 1.0, 1.0) AS bm
        FROM facts_fts JOIN facts f ON f.id = facts_fts.id
        WHERE facts_fts MATCH ?
        ORDER BY bm LIMIT ?
        """,
        (match, max(limit * 8, 60)),
    ).fetchall()
    c.close()
    qlow = q.lower()
    toks = words(q)
    raw_identifiers = [x.lower() for x in re.findall(r"\b[A-Za-z_][A-Za-z0-9_.]*\b", q)
                       if len(x) >= 5 and ("_" in x or "." in x or any(ch.isupper() for ch in x[1:]))]
    out = []
    for r in rows:
        d = row_dict(r)
        hay = " ".join(str(d.get(k, "")) for k in ("claim", "api", "recipe", "topic", "canonical_topic", "source_id", "version", "platform")).lower()
        coverage = sum(1 for t in toks if t in hay)
        exact_api = 0.0
        api = (d.get("api") or "").lower()
        if api and (qlow in api or any(t in api for t in toks if len(t) >= 4)):
            exact_api = 2.0
        if api and any(ident in api and ident not in COMMON_CROSS_CLIENT_IDENTIFIERS for ident in raw_identifiers):
            exact_api += 8.0
        d["score"] = round(coverage * 0.65 + STATUS_SCORE.get(d.get("status", ""), 0) + source_bonus(d.get("source_id", "")) + exact_api, 3)
        d["directness"] = directness(d.get("source_id", ""))
        out.append(d)

    out.sort(key=lambda x: (x.get("score", 0), -(x.get("bm", 0) or 0)), reverse=True)
    return out[:limit]


def context_packet(q: str, target: str | None = None, client_version: str | None = None, sdk_version: str | None = None, limit: int = 10) -> dict[str, Any]:
    facts = search_facts(q, limit=limit)
    return {
        "query": q,
        "target": target or "ExteraGram Android",
        "client_version": client_version,
        "sdk_version": sdk_version,
        "facts": facts,
    }


def render_context_md(packet: dict[str, Any]) -> str:
    lines = [f"# Context Packet: {packet.get('query', '')}", ""]
    for f in packet.get("facts", []):
        lines.append(f"- **[{f.get('id')}]** ({f.get('directness')}) {f.get('claim')}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query facts from ExteraContext index")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    args = parser.parse_args()
    results = search_facts(args.query, limit=args.limit)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
