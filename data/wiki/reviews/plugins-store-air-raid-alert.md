---
type: review
source_id: plugins-store-air-raid-alert
title: "Источник: Air Raid Alert"
reviewer: independent-verifier
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: e30c41d0c01b8a3e417f933a6e5426e749092d46
artifact_sha256: 6ca1da132020a54c1a7c51cd1e86b40546347fd5db7f78f9b67e4775844c85c2
plugin_id: "air_raid_alert"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-05"
---

# Ревью: Air Raid Alert

Сборщик предоставил 5 фактов. Принято 5 фактов.

- Сверен исходник плагина `Plugins/air_raid_alert.eaf` версии 1.2.1 на commit `e30c41d0c01b8a3e417f933a6e5426e749092d46`.
- Архив распакован как ZIP: 14 записей (12 файлов и 2 каталога). Артефакт сверен по трём идентификаторам: git blob `ff27849f6fa0cd75a3bc01cdb066a85ecb35a9a1`, SHA-256 `6ca1da132020a54c1a7c51cd1e86b40546347fd5db7f78f9b67e4775844c85c2`, размер 26895 байт.
- Все пять утверждений подтверждаются указанными фрагментами исходника.
- Факт 1 подтверждает структуру Elyx-пакета. Уточнение: в перечне кандидата отсутствовал `src/i18n.py`, который реально входит в архив; имена файлов локализации — `strings_en.yml`, `strings_ru.yml`, `strings_uk.yml`, а не `en/ru/uk`. Утверждение принято с этим уточнением; ссылки внутри архива ведут на `refmap.yml:1-3` и `main.py:1-28`.
- Факт 2 подтверждает шесть заявленных значений `metainfo.yml` дословно (`id`, `version`, `author`, `app_version`, `sdk_version`, `requirements`); дополнительно в файле есть `name`, `description` и `icon`.
- Факт 3 подтверждает `POLL_SECONDS = 15`, daemon-поток `AirRaidAlertMonitor` и неблокирующий `self._lock.acquire(False)`, который именно отбрасывает наложившийся опрос, а не ждёт блокировку.
- Факт 4 подтверждает оба канала оповещения: `NotificationManager.IMPORTANCE_HIGH` и `Notification.CATEGORY_ALARM` для Android-уведомления, `BulletinHelper.show_error/show_success/show_info` внутри `run_on_ui_thread(show)` для внутриприложенных баннеров. Сам факт наличия кода не доказывает показ уведомления на конкретной сборке клиента.
- Факт 5 подтверждает жизненный цикл; уточнено, что `on_plugin_load()` запускает монитор условно — только при `settings.get("enabled", False)`, — а `on_app_event(AppEvent.RESUME)` вызывает `monitor.check_now(False)` тоже при включённой настройке. Формулировка кандидата «on_plugin_load запускает монитор» без условия принята только с этим уточнением.

## Отклонение от закреплённого SHA

Закреплённый в задании commit `e30c41d143c68ce5976eaef13ec3ca5078a94770` не существует. Проверено независимо: `git cat-file -t` в клоне `Kangel-Plugins/Plugins-Store` возвращает `bad object`; GitHub API отдаёт HTTP 422 (No commit found for SHA); `https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/e30c41d143c68ce5976eaef13ec3ca5078a94770/Plugins/air_raid_alert.eaf` и соответствующая blob-страница отдают HTTP 404. Фактический commit с тем же префиксом — `e30c41d0c01b8a3e417f933a6e5426e749092d46` (`Update plugin: air_raid_alert v1.2.1`, 2026-10-03T20:00:27Z); его API-ответ и обе ссылки возвращают HTTP 200. Локальный файл совпадает с этим commit побайтово (`git hash-object` рабочей копии = `git rev-parse e30c41d0...:Plugins/air_raid_alert.eaf` = `ff27849f6fa0cd75a3bc01cdb066a85ecb35a9a1`), поэтому проверка выполнена по фактическому содержимому закреплённой ревизии 1.2.1, а в фактах и карточке источника используется исправленный SHA. Публиковать URL с 404 в качестве citation нельзя.

## Проверка фактов и повторов

Все пять ID уникальны, записи описывают разные предметные области и дублирующихся утверждений не содержат:

- `air-raid-alert-001` — структура пакета и состав архива (`code`). Подтверждено перечислением ZIP; уточнён пропущенный `src/i18n.py`.
- `air-raid-alert-002` — метаданные `metainfo.yml` (`code`). Подтверждено построчно.
- `air-raid-alert-003` — фоновый поток, период 15 с и неблокирующая блокировка (`code`). Подтверждено `src/monitor.py`.
- `air-raid-alert-004` — Android-уведомление и баннеры на UI-потоке (`code`). Подтверждено `src/notifier.py`.
- `air-raid-alert-005` — `on_plugin_load` / `on_plugin_unload` / `on_app_event(RESUME)` (`code`). Подтверждено `main.py` с уточнением условия `enabled`.

Новых фактов сверх пяти не добавлено; уточнения к фактам 1 и 5 не меняют их предмет и не создают отдельных записей.

## Остаточные пробелы и вердикт

Проверка статическая: установка и запуск на устройстве с клиентом `>=12.9.0` и SDK `>=1.4.5.0` не выполнялись, runtime-подтверждений нет. Сетевой слой (`src/alerts_api.py`, `src/telegram_client.py`) и справочник регионов (`src/regions.py`) не разбирались, поскольку в проверяемые утверждения не входили. Как и у любого `.eaf`-архива, работоспособность зависит от версии загрузчика Elyx целевой сборки.

**Вердикт: `accepted`.** Пять фактов подтверждены закреплённым исходником; два уточнения внесены без отклонения фактов, закреплённый SHA исправлен на существующий.
