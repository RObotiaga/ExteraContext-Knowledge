---
type: review
source_id: exteragram-docs
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: yearningss/exteraGram-docs

- **Вердикт:** `accepted-with-gaps`.
- **Scope:** репозиторий `yearningss/exteraGram-docs`, branch `main`, pinned SHA `341db43686bfb3212e1ecf3cddcc8b8fcfd885f3` (снимок от 2026-09-27). Источник — reverse-engineering документация конкретной сборки exteraGram `12.10.1 / 70389 Full Beta Universal`; SDK обозначен автором как Elyx `1.4.5.5`.
- **Назначение:** `raw/exteragram-docs/radar-context.md` выделяет repository как документационную/reverse-engineering находку и особенно рекомендует `plugins-and-sdk.md` и `exterahook.md`; исходные ссылки радара перечислены в `radar-urls.json`, который пуст.
- **Предел evidence:** source содержит документационные заявления и inline-примеры, но не APK, manifest клиента, исходники, тесты, сборку или runtime-логи. Все claims о внутренностях приложения/SDK оставлены в статусе `docs`; cross-source выводы обозначены как сравнения, а не runtime findings.

## Независимое покрытие

По непорезанному `tree.json` проверены README и все девять документов `docs/`: `ai-integration.md`, `architecture.md`, `backend-and-sync.md`, `dialogs-and-features.md`, `exterahook.md`, `plugins-and-sdk.md`, `settings-reference.md`, `steganography-and-backup.md`, `ui-screens.md`. Все десять Markdown-файлов прочитаны целиком, включая полный каталог настроек и полный каталог экранов. В покрытие вошли сборочный паспорт, Python/Elyx formats и facades, callback lifecycle, hook declarations, thread/account claims, настройки и host plugin UI, debug/dependencies, сети и client-side storage, а также связанные limitations.

Tree содержит 11 blobs (README, 9 docs и `.gitignore`) и одну директорию `docs/`. Первичный `file-manifest.json` не включал `.gitignore`; он был отдельно получен штатным read-only `work/acquire.py` для того же pinned SHA и сохранён в manifest. Его SHA-256 равен `f76c2318f999e35b2251db041d40e6e7143e46f80765320c62a49396b7e659f2`. `.gitignore` проверен как вспомогательный файл и не содержит developer API. Девять относящихся к предмету docs плюс README доступны локально и их SHA-256 совпадают с manifest. Исследуемый контент не исполнялся и не устанавливался.

## Точность и выполненные исправления

- Поправлен охват lifecycle: `on_load()` есть и в single-file, и в archive inline-примерах; single-file пример также показывает `on_unload()`, а таблица SDK перечисляет ещё `on_stop()`. Ранее второй пример не был отмечен.
- Отделены два документационных источника от runtime: stub `BasePlugin` из `exteragram-utils` 0.1.3 объявляет `on_plugin_load()`/`on_plugin_unload()`, а отдельно захваченный официальный SDK reference показывает эту же пару. Они расходятся с названиями в рассматриваемой странице, но не доказывают контракт клиента 12.10.1; этот конфликт оставлен нерешённым.
- Уточнено расхождение metadata/version: источник называет SDK 1.4.5.5, показывает YAML `min_sdk: 1.4.5.5` и Python `__min_sdk__ = "1.4.0"`; отдельно захваченная официальная документация описывает SDK surface 1.4.4.3, `__sdk_version__`/`__app_version__` и legacy `__min_version__`. Совместимость и принятие ключей фактическим loader неизвестны, поэтому ни один контракт не выбран как подтверждённый.
- Добавлено фактическое содержание документации об инициализации ExteraHook через `ExteraHookInitProvider` до `Application.onCreate()`, `unsealHiddenApi()` и `disableArtProfileSaver()`. Эти детали помечены как непроверенные claims снимка: манифеста/JNI/ART реализации нет.
- Расширен список developer-настроек до всех десяти entries в секции Plugins Engine: `pluginsEngine`, `pluginsSafeMode`, `pluginsUnknownSources`, `pluginsDevMode`, `pluginsCompactView`, `pluginsDisableArtOpts`, `pluginsPySdkAutoUpdate`, `pluginsPySdkBetaVersions`, `pinnedPlugins`, `sdkUpdateScheduleTimestamp`. Факт не представляет их как доступный API плагина.
- Добавлен отдельный факт о host plugin UI: закрепление, переход к настройкам/сведениям, source viewer, принудительный Hot Reload и удаление. Это действия интерфейса, не публичные вызовы SDK.
- В coverage note исправлен подсчёт snapshot: полный набор документации — 10 Markdown-файлов, а не все blobs репозитория; дополнительный `.gitignore` теперь также учтён.
- Проверены primary evidence paths/permalinks: ссылки source page и facts указывают на SHA `341db43686bfb3212e1ecf3cddcc8b8fcfd885f3`; cited paths присутствуют в manifest/raw capture, line anchors соответствуют просмотренным текстовым разделам. Claim о поддержке функций, исходящих только из README/документации, остаётся `docs`.

## Повторы и canonical topics

В `work/exteragram-docs-facts.json` **27 уникальных фактов с 27 уникальными ID**; точных повторов claims не выявлено. Lifecycle facts пересекаются тематически с `exteragram-utils` и `official-sdk`, а SDK settings/UI/hooks встречаются и в других SDK/plugin sources. Эти записи оставлены как отдельная provenance для данного SHA; для последующего synthesis использовать canonical topics `lifecycle`, `build`, `hooks`, `threading`, `accounts`, `ui`, `storage` и сохранять различия версий. Внутри source page повторное изложение тех же контрактов в пояснительном тексте, таблице и практических выводах — навигационное повторение, не дополнительные facts.

## Остаточные gaps

- Не доступны APK, Android manifest, SDK loader/runtime, Java/Kotlin/Python implementation ExteraGram, native `dev.exterahook`, binaries, tests, build/CI, changelog и device logs; ранняя инициализация, bypass, hook ordering и значения настроек не подтверждены независимо.
- Нет точных signature/contract для `hook_utils`, `client_utils`, `file_utils`, `plugin_settings`, UI facades, `PipController` и `dev_server`; lifecycle/thread safety, cleanup, account routing, current-chat/forum-thread context и plugin storage contract остаются открытыми.
- Backend auth/серверная схема, Room DAO, и crypto/KDF/nonce параметры не опубликованы в этом snapshot. Список AI-моделей и endpoints датирован не независимо и может устареть.
- Пустой `radar-urls.json` не позволяет независимо сверить исторические URL-упоминания радара. License не указана в repository metadata.
- Runtime checks не проводились; абсолютная полнота относительно недоступного APK/runtime не утверждается.

Источник принят как аккуратно ограниченная карта документационных утверждений по данному snapshot, с указанными пробелами по implementation и runtime.
