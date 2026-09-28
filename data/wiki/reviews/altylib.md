---
type: review
source_id: altylib
review_status: accepted-with-gaps
date: 2026-09-27
---

# Независимая проверка: Altuskhins/AltyLib

- Вердикт: **accepted-with-gaps**.
- Snapshot: `f2674328a24fd24ebc01683f2f84b92ed8470630` (`main`); SHA исходного plugin: `5f34f5420dd5795ce088dff2cde8660d221b8e2954af7bc9eccb480c93f64bda`; README: `f0c62fd14ee1e1e999b13c84d94651f095e91c3e8b28b10c54e2e7d4ce8bf983`; LICENSE: `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986`.
- Полностью сверены единственные три tracked-файла в `tree.json`: `Altylib.plugin` (2868 строк), `README.md` (376 строк), `LICENSE` (674 строки). Дополнительно проверены `snapshot.json`, `repository.json`, `file-manifest.json`, `tree.json`, `radar-context.md` и пустой `radar-urls.json`. Все три raw file hashes соответствуют локальному snapshot. Исходник не запускался; результаты являются static source review, не runtime evidence.
- README заявляет библиотеку для ExteraGram и версию 1.0.4. Code metadata задаёт `__id__=altylib`, `__version__=1.0.4`, `__min_version__=11.9.1`; `__all__` содержит 75 именованных экспортов. Сверены публичные exports, классы, методы и релевантные внутренние участки; покрыты storage/settings, EventBus, commands, scheduler/RPC, hook lifecycle, Telegram requests/peer, formatting, threading, media/UI, NotificationCenter, auto-updater, CLI/debug, feature helpers и cookbook.
- В radar-context источник отнесён к библиотеке/SDK, шаблону, документации и инструменту; названы EventBus/RPC, команды, scheduler, safe_hook, Telegram helpers, UTF-16 formatting, media/UI, rate limiting, diagnostics/hot reload и CLI. Утверждения радара сверены как вторичные: межплагенная семантика и автоматический hook cleanup кодом не подтверждаются. README и tree не содержат отдельного package/CLI launcher.
- Исходный набор из 55 facts имел 55 уникальных ID. После независимого аудита исправлены заметные расхождения и добавлены недостающие факты об auto-updater/message helpers, UI/media exports, cookbook и неверных README примерах. Итоговый JSON содержит **61 факт с 61 уникальным ID**; `claim` и `recipe` на русском, статусы соответствуют схеме (`code`, `docs`, `inference`). Файл для итогового handoff: `C:\Users\sofar\Documents\Codex\2026-09-27\g\work\altylib-facts.json`; синхронная копия остаётся в `outputs/plugin-wiki/work/altylib-facts.json`.

## Найденные расхождения и правки

- Уточнено, что TTL fixed-expiry: чтение не продлевает срок, нулевой/ложный TTL трактуется как отсутствие истечения; cache in-memory, а eviction не LRU по последнему чтению.
- Подтверждено, что EventBus и RPC используют module-global in-process registries. README/радар не доказывают IPC между изолированными runtime/plugin instances.
- Hook cleanup доступен только через явные `HookLifecycle.cancel_all()`, `HookGroup.cancel_all()`, `HookRegistration.cancel()` или `safe_unhook_all()`. `AltyLib.on_plugin_unload()` кеширует updater tasks и выставляет stop flag, но не вызывает hook cleanup или очистку других глобальных реестров.
- `send_request` импортируется из `client_utils`, не является wrapper AltyLib и отсутствует в `__all__`. `split_text` использует Python `len()`, тогда как `md` конвертирует entity offsets в UTF-16.
- В tree нет `altylib_cli.py`/packaging entrypoint. `validate_plugin_manifest` проверяет только вхождение трёх имен metadata полей, не парсит файл и не сверяет значения/версии.
- Исправлено покрытие auto-updater, помощников получения/установки plugin, save-to-gallery, snackbar/clipboard и статических cookbook entries. Отмечено, что updater stop не join-ит поток; в helper-загрузке файла нет callback, который после завершения сам вызывает установку.
- Расширено сравнение README и implementation: неверный пример `TTLCache(ttl=30)`/`.has()`, сигнатура `safe_hook`/default `once`, неблокирующий `RateLimiter.acquire`, observer cleanup только при `atexit`, фактический порядок clipboard аргументов, поведение media без blocking, отсутствие crash notification и двух заявленных cookbook entries.
- README содержит скопированные примеры KVStore в Event Bus/Scheduler, помещает Telegram peer/send helpers в RPC раздел, обещает automagic unload cleanup и описывает validator как schema/version checker. Эти claims квалифицированы по implementation, без распространения README statements на проверенное runtime поведение.
- LICENSE и GitHub metadata указывают GPL-3.0; формулировка source page исправлена с `GPL-3.0-or-later` на `GPL-3.0`.

## Дубликаты и остаточные границы

В JSON нет повторяющихся fact IDs; внутри страницы близкие TTL/EventBus/RPC/lifecycle детали сгруппированы по разным контрактам, а docs-vs-code расхождения сохранены отдельно от code behavior. Пересекающиеся темы следует далее объединять в канонических topic/API страницах с отдельным provenance, не сливая различия контрактов. Другие source pages и общие index/topics не менялись.

Остаточные gaps относятся к runtime: не проверялись реальные ExteraGram/AyuGram версии, reflection и Java method resolution, очереди/потоки, callback behavior, UI availability, работа media/FileLoader, установка updater plugin, hot reload и CLI distribution. Минимальная версия metadata `11.9.1` не доказывает совместимость с текущей сборкой. Независимая проверка ограничена зафиксированным tree/SHA и не гарантирует поведение внешних зависимостей или других версий.
