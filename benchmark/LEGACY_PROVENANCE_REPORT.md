# Legacy wiki provenance import

The supplied `agent-prompts.zip` was parsed as provenance for the original wiki build.

## Observed run structure

- 174 recorded subagent runs.
- 76 source slugs.
- 90 collector runs.
- 84 reviewer runs.
- Every one of the 76 source slugs has at least one collector and at least one reviewer.
- All recorded runs requested `gpt-6-luna` with `reasoning=high`.
- All recorded runs have `fork_turns=none`.
- 19 source slugs had a retry or additional collector/reviewer run.
- Prompt bodies are explicitly marked as reconstructed from saved templates where applicable, rather than verbatim transcripts.

## Trust interpretation

The original reviewer instruction required the reviewer to re-read primary snapshots, verify coverage, signatures, paths/permalinks, evidence status, duplicates, contradictions, and version differences, and to fix the collector output rather than merely report issues.

However, the reviewer could inspect and edit the collector's `wiki/sources/<slug>.md` and `work/<slug>-facts.json`. The historical review is therefore classified as:

`independent-source-reread-nonblind`

It is stronger provenance than an unreviewed collection pass, but it is not equivalent to the new write-back protocol's blind Phase-A verifier. It also never upgrades static `docs` or `code` evidence to `runtime-verified`.

## Integration

`data/legacy-source-runs.json` stores the parsed run provenance. `scripts/build_index.py` imports it into:

- `source_runs`
- `source_provenance`

`python scripts/query.py evidence <legacy-fact-id>` now returns the original collector/reviewer run trail alongside the fact.

`python scripts/query.py doctor` reports:

- `legacy_source_runs = 174`
- `legacy_sources_with_reviewers = 76`

## Regression checks

The provenance integration does not change ranking scores. Retrieval remained:

- Hit@1: 80.0%
- Hit@3: 80.0%
- Hit@5: 100.0%
- Hit@10: 100.0%
- Expected recall@10: 91.1%
- MRR@10: 0.8433

Additional holdout sets remained at 100% Hit@10 with 95.8% expected recall. Donor named-symbol checks remained 6/6 Top-1 with donor warnings 6/6.
