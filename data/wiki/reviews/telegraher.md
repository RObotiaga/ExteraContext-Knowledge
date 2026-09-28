---
type: review
source_id: telegraher
reviewer: /root/review_telegraher
collector: /root/collect_telegraher
model: gpt-6-luna
verdict: unavailable-verified
date: 2026-09-28
accepted_facts: 3
---

# Независимая проверка Telegraher

## Scope и evidence

Назначенная цель — строго `phxc/telegraher`. Снимок кода/SHA отсутствует, поэтому проверены GitHub identity/API, весь относящийся к цели локальный raw-набор (`acquisition-error.json`, `radar-context.md`, пустой `radar-urls.json`) и три machine facts. `tree.json` отсутствует, что согласуется с пустым repository. API-запросы выполнены 2026-09-28 10:35 UTC.

[`GET /repos/phxc/telegraher`](https://api.github.com/repos/phxc/telegraher) вернул HTTP 200: `id=552598807`, `node_id=R_kgDOIO_9Fw`, `full_name=phxc/telegraher`, public, `fork=false`, `created_at=2022-10-16T23:33:52Z`, `updated_at=2023-03-22T11:59:23Z`, `pushed_at=2022-10-16T23:33:53Z`, `size=0`, `default_branch=main`. Это подтверждает точную идентичность записи, но не наличие исходников.

Независимо проверены GitHub REST endpoints: [`/commits`](https://api.github.com/repos/phxc/telegraher/commits) — HTTP 409 `Git Repository is empty`; [`/branches`](https://api.github.com/repos/phxc/telegraher/branches) и [`/tags`](https://api.github.com/repos/phxc/telegraher/tags) — HTTP 200 `[]`; [`/git/refs`](https://api.github.com/repos/phxc/telegraher/git/refs), [`/git/matching-refs/heads/`](https://api.github.com/repos/phxc/telegraher/git/matching-refs/heads/) и [`/git/matching-refs/tags/`](https://api.github.com/repos/phxc/telegraher/git/matching-refs/tags/) — HTTP 409 empty repository; [`/contents/`](https://api.github.com/repos/phxc/telegraher/contents/) — HTTP 404 `This repository is empty`. Совпадает с acquisition record от 2026-09-27, который сохраняет только 409.

Одноимённые [`nikitasius/Telegraher`](https://api.github.com/repos/nikitasius/Telegraher) (ID `436203627`) и [`pegioner/Telegraher`](https://api.github.com/repos/pegioner/Telegraher) (ID `477550587`), упомянутые на source page, отдельно проверены только по repository metadata: их fork lineage — `DrKLO/Telegram` → `nikitasius/Telegraher` → `pegioner/Telegraher`; `phxc/telegraher` имеет отдельный ID и `fork=false`. Оснований приписать их код цели нет; их код не использован. Search API не считается исчерпывающим списком проектов. У `nikitasius/Telegraher` metadata показывает push 2026-09-17, поэтому радарная общая характеристика «старые направления не развивались» остаётся вторичной и не должна считаться текущим фактом для каждого одноимённого проекта.

## Facts, coverage и verdict

- `telegraher-001`: identity/metadata подтверждены прямым repository API; `unavailable` относится к отсутствию code content, не является `code` evidence.
- `telegraher-002`: статусы commits, refs, branches/tags и contents подтверждены перечисленными endpoints; SHA/tree получить нельзя. Это evidence недоступности, не утверждение о поведении кода.
- `telegraher-003`: корректно помечен `secondary`, основан на `raw/telegraher/radar-context.md:10,35` и пустом `radar-urls.json`; конкретных API/functions для цели радар не задаёт.

ID и claims трёх фактов уникальны, дублирования нет. Статусов `code` и `runtime-verified` нет. Не установлены commits/SHA, исходники, README, лицензия, tests, build или feature/API contracts; runtime не проверялся. Упомянутая acquisition-попытка Wayback/CDX отдельно не перепроверялась. Полнота по недоступному коду не заявляется.

**Verdict: `unavailable-verified`.** Публичная запись `phxc/telegraher` точно идентифицирована и независимо подтверждена пустой. Фактов: **3** (2 `unavailable`, 1 `secondary`, 0 `code`).