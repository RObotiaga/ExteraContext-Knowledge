---
type: review
source_id: air-raid-alert
reviewer: /root/review_air_raid_alert
collector: /root/collect_air_raid_alert
model: gpt-6-luna
verdict: unavailable-verified
date: 2026-09-28
accepted_facts: 4
---

# Независимая проверка air-raid-alert

## Область проверки

Целевой репозиторий по-прежнему не имеет URL или `owner/repo`, поэтому для него нет локального каталога `raw/air-raid-alert/`, `tree.json`, commit SHA или файлового snapshot. Проверены source page, все четыре записи `work/air-raid-alert-facts.json`, соответствующая запись `work/radar-source-candidates.json` (кандидат `unresolved:exteragram-air-raid-alert`, строки 662–677) и первичный текст радара `outputs/plugin-wiki/raw/radar.md:3643–3655`. Кандидат в реестре указывает `explicit_url: null`, `owner_repo: null`, `missing_url: true` и `unresolved_repository_identity`. В радаре приведены дата 16 сентября 2026, описание `Plugin exteraGram`, README и `air_raid_alert.elyx` около 21 КБ; без первичной ссылки эти сведения остаются `secondary`.

## Независимый поиск и исправления

На дату проверки GitHub REST Search Repositories повторён с точными запросами `exteraGram-air-raid-alert in:name`, `"exteraGram-air-raid-alert"`, `exteragram in:name created:2026-09-16` и `air_raid_alert.elyx`; каждый вернул `total_count: 0`. Запрос `air_raid_alert.elyx in:readme` вернул только `MightyM17/CSI_Task_App_22`; это не подтверждает целевой плагин. Общий `air-raid-alert` дал посторонние проекты без установленной связи с ExteraGram. GitHub Code Search для `air_raid_alert.elyx` вернул HTTP 401.

GitLab project search по точному имени и имени файла, а также Codeberg repository search по тем же строкам вернули пустые ответы HTTP 200. Wayback CDX для wildcard URL GitHub по имени репозитория снова вернул 503; ранее записанный запрос по имени файла также завершился недоступностью. В source page сохранён ранее выполненный Sourcegraph global поиск имени файла с `archived:yes fork:yes` (`matchCount: 0`); поиск репозитория был ограничен shard match limit. Эти результаты ограничены публичной индексацией и не исключают приватные, удалённые, переименованные или неиндексированные источники.

Проверен отдельный первичный каталог `Kangel-Plugins/Plugins-Store` на SHA `513e29a07858e5dec3a8dcdc6a860fe4296f1d43`. Его `store.json:472–505` содержит `air_raid_alert`, название `Air Raid Alert – alerts.in.ua`, версию `1.2.0`, авторов `@cobra_S0FT | @excess_plugins` и URL на `Plugins/air_raid_alert.eaf`. SHA-256 локального файла `outputs/plugin-wiki/raw/plugins-store/files/store.json` равен `f155aff2470dba54ebb2584c93646330e5ec0bbf80447719e292214e7cd7d79d` и совпадает с записью `file-manifest.json`. Это подтверждает содержимое snapshot каталога, но не связывает этот `.eaf` с неидентифицированным `.elyx` из радара. Исправлена ошибочная строка coverage в source page, где говорилось, что каталог заново не проверялся. Portable-ссылка на facts оставлена в требуемом виде `../facts/air-raid-alert.json`; сгенерированная страница facts на момент review отсутствует.

## Проверка фактов и повторов

Все четыре ID уникальны; записи описывают разные виды доказательств и дублирующихся утверждений не содержат:

- `air-raid-alert-001` — live REST-поиск по точному имени и отсутствие owner/repo в candidate registry (`unavailable`). URL поискового запроса соответствует зафиксированному запросу.
- `air-raid-alert-002` — только вторичный пересказ радара о дате, описании и файлах (`secondary`); путь `raw/radar.md:3643–3655` соответствует source excerpt. У репозитория и `.elyx` нет подтверждённого SHA или локального hash.
- `air-raid-alert-003` — поиск имени файла, нерелевантное совпадение README и недоступный Code Search (`unavailable`). Endpoint URLs соответствуют проверенным API-запросам; Code Search 401 является неразрешённым пробелом, а не отрицательным результатом.
- `air-raid-alert-004` — catalog snapshot факт о похожем `.eaf` и вывод о неустановленной связи (`inference`). Permalink на `store.json` закреплён на snapshot SHA и lines 472–505; локальный path/hash подтверждены manifest.

Итог: **4 уникальных факта** (`001`–`004`). В source page обновлены review status/link, статус завершённой проверки, ложное утверждение coverage о непроверенном KPM каталоге и оговорка о ещё не собранной facts page. Смешения KPM `.eaf` с неизвестным `.elyx` нет.

## Остаточные пробелы и вердикт

Нет первичного URL/namespace, README, manifest, commit SHA, tree, байтов `.elyx` или его hash; поэтому нельзя проверить функции, API, lifecycle, сборку, ограничения, содержимое и runtime исходного плагина. Не удалось получить архивное подтверждение из Wayback, а GitHub Code Search закрыт авторизацией. Негативные поисковые результаты показывают только текущее состояние доступных индексов: они не доказывают, что репозитория никогда не существовало.

**Вердикт: `unavailable-verified`.** Подтверждены отсутствие разрешённой identity и недоступность первичного материала по проверенным каналам; содержимое `.elyx` осталось непроверенным.
