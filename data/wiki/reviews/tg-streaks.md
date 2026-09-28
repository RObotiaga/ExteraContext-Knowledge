---
type: review
source_id: tg-streaks
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: n08i40k/tg-streaks

- Вердикт: **accepted-with-gaps**.
- Проверенный snapshot: `n08i40k/tg-streaks`, SHA `e9fa83619480964ccd3b8565af8c1301318ac7ad` (`master`), по `raw/tg-streaks/snapshot.json`, `tree.json`, `file-manifest.json` и сохранённым исходникам. Идентификатор источника и назначение сверены с `radar-context.md`/`radar-urls.json`: крупный ExteraGram/AyuGram Kotlin/DEX-плагин со streak/pet UI и собственной базой. Радарная версия `2.20.0` отличается от entrypoint и `pyproject.toml` snapshot `2.20.1`; это различие уже явно отражено на source page. Короткие hash-ы упомянутых в радаре коммитов отдельно не подтверждены.
- Проверка статическая: приложение, клиент, тесты, сборка, workflow и внешние API не запускались. Source inspection не является runtime evidence.

## Независимое покрытие

По `tree.json` подтверждены 134 Kotlin-файла. Независимо сверены `Plugin.kt`, Python entrypoint `tg-streaks.py`, `SettingsMenuActions.kt`, ключевые файлы `hook/**`, controllers, account/task queue, entities/DAOs/converters/migrations/Room, history fetchers, backup/sync, UI и WebView/resources, Gradle/Just/Python конфигурации, release workflow и user-guide разделы `settings.mdx`, `control-panel.mdx`, `features/streak-pet.mdx`. Остальные `docs/content/**/*.mdx` присутствуют в снимке и перечислены в source page collector coverage, но здесь не заявляется независимое повторное чтение каждого документа или скриншота. Проверка соответствует тематической области этого крупного приложения, но не означает построчный аудит каждой реализации из 134 файлов.

Отдельно прослежены Python↔Kotlin reflection contract, settings callback/defaults/application, пять hook bundles и unhook lifecycle, selected-account task queues, relation keys и schema migration chain, sync/backup flows, chat/pet UI и WebView bridge, а также release workflow inputs/artifacts/permissions. Snapshot включает все заявленные Kotlin-файлы и перечисленные источники пользовательской документации. Корневого README в дереве нет; `src/test`, `src/androidTest` и `tests/` не найдены, а repository metadata содержит `license: null` и manifest фиксирует 404 для двух проверенных путей LICENSE.

## Найденное и исправленное

- Сверены метаданные plugin entrypoint (`tg-streaks`, `Streaks`, `2.20.1`, min version `12.1.1`) с `pyproject.toml`; значение радара `2.20.0` относится к более раннему срезу.
- Подтверждён порядок успешной загрузки: подготовка embedded assets → Kotlin `inject` → Python settings/menu registration → Kotlin `finalizeInject`; lifecycle и host integration описаны как source-level contracts. Таблица hooks не превращает внутренние Telegram методы в обещание публичного SDK.
- Подробности settings из пользовательского руководства ранее не имели отдельного структурированного факта. Добавлен факт о defaults (update-check и auto-create включены; FAB 64/80/96/112/128 dp, default 80), persistence и Kotlin setter bridge, с кодовыми ссылками. Settings actions связаны с rebuild-all, backup export и emoji-pack management.
- Удалено дублирование: прежний отдельный fact `tg-streaks-027` повторял три типа/веса pet tasks из `tg-streaks-014`; пользовательское описание и вызов rebuild объединены в fact 014, а освободившийся ID 027 использован для settings.
- Release workflow описание сверено с сохранённым YAML: manual input version, предварительная проверка `Telegram.jar`, сборка и embedding `.plugin`, отдельный `classes.dex`, provenance attestations, metadata commit/tag/publish и Telegram `editMessageMedia`/`sendMessage`. Указано, что это конфигурация workflow, не факт успешного запуска.
- Проверены точные SHA permalinks в facts и source page. После правок facts JSON содержит **27 уникальных фактов с уникальными ID**; внутренний повтор task weights устранён. Пересекающиеся с другими sources темы (`build`, plugin lifecycle/hooks/settings, account queues, Room/storage, history/RPC, sync/backup, UI/WebView) следует синтезировать по canonical topic, сохраняя source и commit provenance; контракты fork-ов и различия версий не сливать как один API.

## Остаточные gaps

- Нет статического доказательства, что embedded `.plugin` из GitHub Release совпадает с исходниками на данном SHA: в отслеживаемом `tg-streaks.py` области DEX/resources пусты.
- Не проверены runtime hook/reflection compatibility с конкретными ExteraGram/AyuGram APK, фактическая отработка settings/menus/UI и WebView-поведение устройства, Telegram RPC limits, Android storage/document picker, Room codegen и upgrade реальных БД.
- Не выполнялся threat audit входящего sync SQLite snapshot, всей WebView resource surface или release credentials/workflow execution; source inspection подтверждает лишь описанные call-sites/config.
- Радарные короткие commit hashes не идентифицируются из `radar-urls.json`; по этому snapshot проверен только базовый SHA.
- 134 Kotlin-файла сохранены и охвачены выбранными подсистемами и call-sites; абсолютная полнота всех периферийных UI/utility implementation details не заявляется.

Остаточные ограничения оставлены как gaps, поэтому оценка — **accepted-with-gaps**, без гарантии runtime-работоспособности или абсолютной полноты.
