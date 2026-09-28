---
type: source-review
source_id: ayugram-desktop-plus
reviewer: /root/review_ayugram_desktop_plus
model: gpt-6-luna
verdict: accepted-with-gaps
reviewed_at: 2026-09-28
---

# Независимая проверка AyuGram Desktop Plus

## Область и версия

Проверен `Kindness-Kismet/AyuGramDesktop-Plus` на закреплённом SHA [`b59475e090b64fd5c8bc4124535c515050b70ef0`](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/tree/b59475e090b64fd5c8bc4124535c515050b70ef0). `snapshot.json` совпадает с этим SHA, дерево помечено полным и содержит 7 355 blobs. `file-manifest.json` содержит 63 отобранных файла; для всех 63 локальные SHA-256 совпали с manifest. Сборщик: `/root/collect_ayugram_desktop_plus`; независимый проверяющий: `/root/review_ayugram_desktop_plus`, модель `gpt-6-luna`.

Сверены source page, все 24 исходных факта и их строки/сигнатуры в snapshot, README, AGENTS, `Telegram/CMakeLists.txt`, app-debug guides и выбранные Ayu lifecycle/settings/worker/data/feature/debug файлы. Также проверены `radar-context.md` и пустой `radar-urls.json`. Приложение и сборки не запускались; тесты не выполнялись.

## Полезность и граница API

Материал полезен разработчику, который изменяет сам Desktop fork: инструкции требуют добавлять исходники в `ayugram_files`, менять upstream UI/core файлы напрямую, регистрировать settings в JSON/UI и держать данные в `ayu/data`. Примеры settings, account/session worker, HistoryItem filtering/cache invalidation, Qt Network, debug loopback и ресурсного импорта дают переносимые инженерные паттерны.

Это не extension host contract. `AyuInfra`, `AyuSettings`, `AyuWorker`, `FiltersController` — внутренние C++/Telegram Desktop seams; `rpl`, `base::Timer`, `Core::App`, `Data::Session`, `HistoryItem` принадлежат Qt/reactive или Telegram Desktop implementation. `QNetworkAccessManager` — Qt transport, Google endpoint — внешний сервис. Debug TCP command server — debug-поверхность процесса. Ни один из этих интерфейсов не подтверждает Android hook/DEX/plugin API. Радар упоминает AyuGramDesktop-Plus среди Desktop/iOS форков и прямо характеризует такую группу как малорелевантную Android plugin-разработке; это верно отражено как secondary context, а не API.

## Найденные проблемы и исправления

- Факт 018 и source page ошибочно утверждали проверку ожидаемого размера emoji preset. В `emoji_packs.cpp` `preset.size` попадает только в progress callback как запасной total; downloader сравнивает SHA-256, сетевой статус и результат `QSaveFile::commit()`, но не число скачанных байт с `preset.size`. Исправлены claim, рецепт и описание. Импорт далее имеет общий верхний предел размера; это не проверка совпадения с manifest size.
- Факт 022 ссылался на unrelated README ranges. Перенесены ссылки на download table и release description: README 141–152 и 376–389.
- Факт 001 смешивал README claims с выводом «не Android plugin SDK». Claim сужен до явно описанного Desktop-клиента; отрицательный вывод оставлен отдельно в inference-факте 024.
- В факт 004 добавлена ссылка на декларации `rpl::variable` в заголовке, где хранение действительно видно.
- Покрытие не включало выбранный `AyuDatabase`. Добавлен факт 025 об относительной SQLite базе, schema sync, миграциях и поведении recovery; в source page добавлена соответствующая граница storage integration.

После исправлений машинный слой содержит **25 уникальных фактов**. Дубликатов, требующих удаления или слияния, не осталось: 012 и 013 описывают решение фильтрации и отдельную cache-инвалидацию; 018 и 019 — загрузку и публикацию импортированного ресурса; 014–017 — независимые части debug control surface. Пересечения 001/024 оставлены разделёнными: README identity vs scoped negative API inference. При последующем тематическом синтезе разумно канонизировать общие идеи под CMake/fork integration, reactive settings, message pipeline/cache invalidation, debug harness и safe resource import, не объединяя desktop контракт с Android plugin APIs.

## Остаточные пробелы

- Выборка составляет 63 файла из полного дерева на 7 355 blobs; Telegram Desktop upstream и все Ayu call-sites/feature directories не прочитаны. Feature/UI table не претендует на каталог всех функций клиента.
- В `filters` и message history просмотрены лишь отдельные реализации и выбранные внутренние call-sites; интеграция во все receive/send/edit/delete пути не прослежена.
- UI picker и platform emoji-font backend просмотрены частично. README описывает фичи, шестиплатформенные архивы и release provenance как документацию; ни работоспособность функций, ни build/release workflow здесь не подтверждались.
- Debug server/CLI не запускались. TCP protocol, synthetic UI helpers и fake state подтверждены чтением source/docs, не runtime.
- Исторических URL нет, поэтому сравнение с parent/upstream и version drift сверх зафиксированного SHA не оценивались.

## Вердикт

**`accepted-with-gaps`**: источник корректно представлен как набор нативных Desktop fork integration patterns, а ошибочная проверка размера исправлена. Для Android plugin разработки он даёт только переносимые идеи; доступного Android plugin API из него выводить нельзя. Ограничения перечислены выше.
