---
type: source
source_id: plugins-store-air-raid-alert
title: "Источник: Air Raid Alert"
source_type: eaf
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: e30c41d0c01b8a3e417f933a6e5426e749092d46
path: "Plugins/air_raid_alert.eaf"
artifact_sha256: 6ca1da132020a54c1a7c51cd1e86b40546347fd5db7f78f9b67e4775844c85c2
plugin_id: "air_raid_alert"
plugin_version: "1.2.1"
author: "@cobra_S0FT | @excess_plugins"
min_version: ">=12.9.0"
app_version: ">=12.9.0"
sdk_version: ">=1.4.5.0"
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-air-raid-alert.md
date: "2026-10-05"
---

# Источник: Air Raid Alert

- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Файл: `Plugins/air_raid_alert.eaf`
- Версия: `1.2.1`
- Commit: `e30c41d0c01b8a3e417f933a6e5426e749092d46`
- Проверенный файл: [air_raid_alert.eaf](https://github.com/Kangel-Plugins/Plugins-Store/blob/e30c41d0c01b8a3e417f933a6e5426e749092d46/Plugins/air_raid_alert.eaf)
- Идентификаторы артефакта: git blob `ff27849f6fa0cd75a3bc01cdb066a85ecb35a9a1`; SHA-256 `6ca1da132020a54c1a7c51cd1e86b40546347fd5db7f78f9b67e4775844c85c2`; размер `26895` байт.
- Состав архива (ZIP, 14 записей): `refmap.yml`, `metainfo.yml`, `main.py`, `src/` (`alerts_api.py`, `i18n.py`, `monitor.py`, `notifier.py`, `regions.py`, `telegram_client.py`), `strings/` (`strings_en.yml`, `strings_ru.yml`, `strings_uk.yml`).

## Проверенные факты

1. Пакет — Elyx-архив с `refmap.yml` в корне (`metainfo: metainfo.yml`, `main: main.py`, `strings: strings`), `metainfo.yml` и точкой входа `main.py` с классом `AirRaidAlertPlugin(BasePlugin)`; код вынесен в `src/`, строки — в `strings/`. [refmap.yml:1-3, main.py:1-28](https://github.com/Kangel-Plugins/Plugins-Store/blob/e30c41d0c01b8a3e417f933a6e5426e749092d46/Plugins/air_raid_alert.eaf).
2. `metainfo.yml`: `id: air_raid_alert`, `version: 1.2.1`, `author: '@cobra_S0FT | @excess_plugins'`, `app_version: '>=12.9.0'`, `sdk_version: '>=1.4.5.0'`, `requirements: requests>=2.31`. [metainfo.yml:1-9](https://github.com/Kangel-Plugins/Plugins-Store/blob/e30c41d0c01b8a3e417f933a6e5426e749092d46/Plugins/air_raid_alert.eaf).
3. Фоновый мониторинг: `AlertMonitor` запускает `threading.Thread(..., name="AirRaidAlertMonitor", daemon=True)`, цикл опрашивает с `POLL_SECONDS = 15` через `self._stop.wait(POLL_SECONDS)`, повторный вход отбрасывается неблокирующим `self._lock.acquire(False)`. [src/monitor.py:11,61-62,76-81,157](https://github.com/Kangel-Plugins/Plugins-Store/blob/e30c41d0c01b8a3e417f933a6e5426e749092d46/Plugins/air_raid_alert.eaf).
4. Оповещения: Android-канал `NotificationManager.IMPORTANCE_HIGH` и `Notification.CATEGORY_ALARM`; внутриприложенные баннеры `bulletin()` показываются через `BulletinHelper` внутри `run_on_ui_thread(show)`. [src/notifier.py:26,33,40,57-65](https://github.com/Kangel-Plugins/Plugins-Store/blob/e30c41d0c01b8a3e417f933a6e5426e749092d46/Plugins/air_raid_alert.eaf).
5. Жизненный цикл: `on_plugin_load()` создаёт `AlertMonitor` и запускает его при `settings.get("enabled", False)`; `on_plugin_unload()` вызывает `monitor.stop()` (`Event.set`, `join(timeout=1)`); `on_app_event(AppEvent.RESUME)` при включённой настройке вызывает `monitor.check_now(False)` и обновляет сохранённый статус. [main.py:29-46, src/monitor.py:65-71](https://github.com/Kangel-Plugins/Plugins-Store/blob/e30c41d0c01b8a3e417f933a6e5426e749092d46/Plugins/air_raid_alert.eaf).

## Отклонение от закреплённого SHA

В задании был указан commit `e30c41d143c68ce5976eaef13ec3ca5078a94770`. Такого объекта в `Kangel-Plugins/Plugins-Store` нет: `git cat-file` отвечает `bad object`, GitHub API — HTTP 422, а `raw.githubusercontent.com` и `github.com/.../blob/` по этому SHA — HTTP 404. Фактический commit с префиксом `e30c41d` и сообщением `Update plugin: air_raid_alert v1.2.1` — `e30c41d0c01b8a3e417f933a6e5426e749092d46` (2026-10-03T20:00:27Z), и он разрешается HTTP 200. Локальный файл `Plugins-Store/Plugins/air_raid_alert.eaf` побайтово совпадает с этим commit: `git hash-object` рабочей копии = `ff27849f6fa0cd75a3bc01cdb066a85ecb35a9a1` = `git rev-parse e30c41d0...:Plugins/air_raid_alert.eaf`. Во всех фактах используется исправленный SHA.

## Ограничения

Проверка статическая по закреплённому исходнику: она подтверждает состав архива, метаданные и наличие указанных вызовов в коде, но не доказывает установку, запуск и фактическое поведение плагина на устройстве с клиентом `>=12.9.0` и SDK `>=1.4.5.0`. `alerts_api.py`, `regions.py` и `telegram_client.py` не разбирались по существу, так как в проверяемые утверждения не входили.
