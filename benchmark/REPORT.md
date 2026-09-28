# ExteraContext prototype benchmark report

Date: 2026-09-28

## What was actually tested

This report measures the deterministic retrieval layer bundled with ExteraContext. It does **not** claim an end-to-end LLM A/B/C result: this execution environment has no independent Codex/Claude/model runner, so it cannot create clean fresh agent sessions for baseline/raw-wiki/skill runs.

The retrieval benchmark still tests the critical mechanism that the skill adds: given a natural-language development task, does it surface the expected evidence, prioritize target/official sources, avoid donor contamination, and keep provenance warnings visible?

Control = naive lexical overlap over the same 2,167 facts, with no evidence-status/source ranking and no domain query expansion.

Metrics:

- Hit@K: at least one expected fact appears in the first K facts.
- Expected recall@10: share of all expected facts present in the first 10.
- MRR: mean reciprocal rank of the first expected fact.

## Main development set — 15 cases

Covers outgoing hooks, multi-account, background/UI work, TL requests, editing, reflection, Xposed, settings, lifecycle, Elyx, file handlers, intents, metadata, and an unsupported permissions query.

| Retriever | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Expected recall@10 |
|---|---:|---:|---:|---:|---:|
| Naive control | 40.0% | 60.0% | 60.0% | 73.3% | 55.6% |
| Original prototype v0.1 | 60.0% | 60.0% | 66.7% | 86.7% | 72.2% |
| Current v0.5 | 80.0% | 80.0% | 100.0% | 100.0% | 91.1% |

Current v0.5 MRR@10: 0.843.

The first benchmark exposed missing Russian/English domain expansions and excessive weight on semantically adjacent implementation facts. Those general retrieval issues were fixed; therefore this set is now a regression set, not an unbiased holdout.

## First holdout — 12 cases

This set was created after the first tuning pass and tested v0.2 before its two observed misses were used for later fixes.

| Retriever | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Expected recall@10 |
|---|---:|---:|---:|---:|---:|
| Naive control | 41.7% | 50.0% | 58.3% | 83.3% | 79.2% |
| ExteraContext v0.2, before holdout fixes | 58.3% | 83.3% | 83.3% | 91.7% | 91.7% |

This is the cleanest evidence in this prototype that evidence-aware/domain-aware retrieval improves natural-language lookup rather than only memorizing the development set.

## Exact-term holdout — 12 cases

A later set intentionally contains many exact API/class terms. Both naive control and the current retriever achieve 100% Hit@10 and 95.8% expected recall@10; Hit@3 is 91.7% for both.

Interpretation: when the developer already knows the exact identifier, plain lexical retrieval is already strong. ExteraContext's primary value is ambiguous natural-language tasks, evidence ranking, provenance and donor/compatibility guardrails—not replacing exact symbol lookup.

## Donor-symbol holdout — 6 fresh cases

Created after the donor-ranking fix and not used for another tuning pass. Named donor symbols include ObserversGroup, AyuConfig, CloudStorageHelper, TranslationCache, NetworkLoggingInterceptor and AyuFilter.

- Correct donor family in top 1: 6/6 (100%)
- Correct donor family in top 3: 6/6 (100%)
- Donor warning emitted: 6/6 (100%)

This matters because an earlier implementation over-penalized donor sources and could hide an explicitly named AyuGram/Nagram symbol behind unrelated ExteraGram facts. The current version surfaces the exact donor symbol while keeping it labeled donor-only.

## Context size

Bundled derived wiki: 9,921,410 bytes total (4,672,754 bytes Markdown + 5,241,727 bytes structured JSON).

Average task packet on the 15-case set: about 14,404 characters. That is roughly 690x smaller than injecting the entire derived wiki by byte/character magnitude. This is not a tokenizer-accurate token ratio, but it demonstrates the intended progressive-disclosure effect.

## Important limitations

1. No runtime-verified facts exist yet. The benchmark validates retrieval, not whether an API works on a device.
2. Client/SDK version filtering remains heuristic, not a strict compatibility solver.
3. The benchmark ground truth is based on the current wiki, so errors in the wiki can become errors in the benchmark.
4. This is not yet a clean end-to-end model comparison. Independent model sessions are required to measure code success, hallucinated API rate, repair iterations and token usage with and without ExteraContext.
5. Exact-term cases show little retrieval advantage; this is expected and should not be hidden by averaging only ambiguous cases.

## Reproduce

From the skill root:

```bash
python tests/smoke.py
python benchmark/evaluate_retrieval.py
python benchmark/eval_set.py benchmark/holdout2.json
```

The frozen raw result files are in this directory.

## End-to-end A/B/C protocol

Use fresh model sessions for every run:

A. Baseline: project repository only; no plugin wiki and no ExteraContext.
B. Raw wiki: project repository + derived wiki, but no ExteraContext query tool/ranking instructions.
C. ExteraContext: project repository + skill; agent must retrieve task packets and resolve non-local symbols.

Run the same tasks at least twice per mode and preferably three times. Do not continue between modes in one chat/session.

Primary outcome:

> percentage of tasks completed with working code and zero unverified external API symbols.

Also record build/load/runtime success, wrong-client API count, unsupported-case honesty, number of repair iterations, tool calls and token usage.
