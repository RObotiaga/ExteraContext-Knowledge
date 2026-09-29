# ExteraContext Knowledge

Source-of-truth knowledge repository for ExteraContext.

This repository contains the curated ExteraGram/AyuGram plugin-development knowledge base, source/reviewer provenance, recipes/topics, compatibility notes, and the compiler that turns those sources into the SQLite/FTS5 index consumed by ExteraContext MCP.

## Repository boundary

This repository owns **knowledge content** and its provenance. It does not own the MCP server, agent write-back runtime, or DeepSeek Harness integration; those live in `RObotiaga/ExteraContext-MCP`.

Key paths:

- `data/wiki/` — reviewed facts, sources, recipes, topics, rules, gaps and compatibility material.
- `data/sdk-snapshots/` — pinned metadata for official Android PySDK release/build artifacts.
- `data/legacy-source-runs.json` — provenance reconstructed from the original collector/reviewer prompt archive.
- `scripts/build_index.py` — deterministic SQLite/FTS5 compiler.
- `scripts/import_legacy_prompts.py` — legacy provenance importer.
- `benchmark/` — retrieval evaluation inputs and reports tied to the knowledge corpus.

## Build the knowledge index

```bash
mkdir -p dist
python scripts/build_index.py \
  --wiki data/wiki \
  --provenance data/legacy-source-runs.json \
  --db dist/exteracontext.sqlite
```

`dist/exteracontext.sqlite` is a generated artifact and is intentionally not committed to source control. The MCP repository can build/sync this database from this repository.

## Evidence model

Static evidence keeps its original status (`docs`, `code`, `inference`, `secondary`, `unavailable`). Legacy source review provenance is recorded as `independent-source-reread-nonblind`; it must not be upgraded to runtime verification.

## Planned release contract

The stable integration boundary with `ExteraContext-MCP` will be a versioned Knowledge Bundle containing the compiled SQLite database plus manifest, provenance and checksums. Until that release pipeline is enabled, the MCP repository can shallow-clone this repository and build the database locally.
