---
type: source
source_id: official-sdk-builds
date: 2026-09-29
review_status: accepted-with-gaps
---

# Официальные Android PySDK builds: plugins-pysdk-builds

Первичный источник: <https://github.com/exteraSquad/plugins-pysdk-builds/releases>.

Это отдельный первичный источник **release metadata реальных Android PySDK artifacts**, а не HTML-документация API. Capture выполнен через официальный GitHub Releases API 2026-09-29. В inventory сохранены tag, channel, build number, полный commit SHA из release body, publication date и metadata всех assets.

## Каноническая identity snapshot

`sdk_version + channel + build + tag + commit`

Один `sdk_version` недостаточен: release stream содержит несколько builds для 1.4.3.9, 1.4.4.1 и 1.4.5.0.

## Captured releases

| Роль | SDK | Канал | Build | Commit | Published | stubs.zip bytes | stubs SHA-256 |
|---|---:|---|---:|---|---|---:|---|
| candidate | `1.4.3.8` | stable | #13 | `731bc0d` | 2026-04-27 | 11752 | `d521ce8ae490807e…` |
| anchor | `1.4.3.9` | stable | #14 | `ed745e9` | 2026-04-28 | 11752 | `8fb7e2ba255475f1…` |
| anchor | `1.4.3.9` | stable | #16 | `818ff5b` | 2026-05-01 | 12436 | `228262d3e1a44068…` |
| candidate | `1.4.4.1` | beta | #18 | `9ebfdce` | 2026-05-03 | 13219 | `497e6008b034ff5e…` |
| candidate | `1.4.4.1` | beta | #19 | `07279b0` | 2026-05-10 | 13219 | `6c3dc1aa92935107…` |
| anchor | `1.4.3.10` | stable | #20 | `69c7cb5` | 2026-06-22 | 11804 | `8b026a427b184a30…` |
| candidate | `1.4.4.2` | beta | #21 | `9e77645` | 2026-06-22 | 13219 | `f6940e9bd5a8c42b…` |
| anchor | `1.4.4.3` | beta | #23 | `ad8ef19` | 2026-07-16 | 13230 | `29a60f83cf5e5e60…` |
| candidate | `1.4.5.0` | beta | #24 | `9374712` | 2026-07-25 | 13553 | `b4391a7ab1147888…` |
| anchor | `1.4.5.1` | stable | #35 | `88b7f57` | 2026-07-30 | 22038 | `078262ded8197945…` |
| anchor | `1.4.5.0` | beta | #36 | `e1e5506` | 2026-08-07 | 13553 | `933b3c7703e07022…` |
| candidate | `1.4.5.3` | beta | #39 | `f931e00` | 2026-08-13 | 21637 | `dfcde58c25aeb627…` |
| candidate | `1.4.5.4` | beta | #40 | `f449c63` | 2026-08-13 | 21637 | `6d110efef1a1e035…` |
| anchor | `1.4.5.5` | beta | #41 | `20ef655` | 2026-08-28 | 21637 | `68b6e3a4aca60197…` |

Полная машинная запись: `data/sdk-snapshots/release-inventory.json`.

## Same-version drift

- `1.4.3.9 stable`: build #14 и #16 — разные commits и stubs digests.
- `1.4.4.1 beta`: build #18 и #19 — разные commits и stubs digests.
- `1.4.5.0 beta`: build #24 и #36 — разные commits и stubs digests.

Разный SHA-256 доказывает различие bytes artifacts. Он **не доказывает**, что изменился конкретный API symbol.

## Каналы

Captured beta releases имеют GitHub `prerelease=false`, поэтому channel определяется по official tag/name/body metadata, а не по GitHub prerelease boolean.

На дату capture:
- latest beta: `1.4.5.5` build #41, commit `20ef655470d64e8bf195e3f5a9973485d1b0be19`;
- latest stable: `1.4.5.1` build #35, commit `88b7f5713c982e1e07c9bbfdc33835d1b2116495`.

## Anchor snapshots

Для первого symbol-level pass выбраны: 1.4.5.5 beta #41, 1.4.5.1 stable #35, 1.4.5.0 beta #36, 1.4.4.3 beta #23, 1.4.3.10 stable #20, 1.4.3.9 stable #14 и #16.

## Evidence boundary

В этом обновлении сохранены release metadata, sizes и cryptographic digests. Содержимое `stubs.zip` через доступный GitHub connector не было получено как текстовый resource, поэтому symbol presence/signatures/version boundaries пока не извлечены. Нельзя выводить API changes только из размера ZIP или digest.

Это static release evidence, не runtime verification.
