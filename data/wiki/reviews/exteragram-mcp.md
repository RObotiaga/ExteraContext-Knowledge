# Независимая проверка exteragram-mcp

## Область и снимок

- Проверен именно `cataIystdev/exteragram-mcp`, canonical slug `exteragram-mcp`, ветка `main`, SHA `ad824092ae60d785d0f0f21f1897b74118a186b1` (snapshot date 2026-09-27). В `raw/exteragram-mcp/tree.json` 71 запись, 59 файловых blobs, `truncated: false`.
- Сверены raw `radar-context.md`/`radar-urls.json` и source page: радар описывает MCP-сервер для разработки плагинов, пакет 1.0.0, заявленные 76 инструментов и основные workflow; эти описательные claims перепроверялись по pinned source, а не принимались за API.
- В первоначальном `file-manifest.json` отсутствовал `package-lock.json`, хотя он был в pinned tree. Файл получен через предусмотренный `work/acquire.py` для того же SHA. После получения все 59 blobs из manifest совпали с локальными файлами по SHA-256.
- Проверены README и `docs/README.md`, architecture/deployment docs, обзор и справка групп A–R; инвентарь регистраций всех 18 `src/tools/*.ts` и реализации, относящиеся к claims про `src/index.ts`, `src/server.ts`, `src/types.ts`, `src/state/plugin-context.ts` и оба codegen-модуля; также package/build config и семь test-файлов. Исходники читались как данные. MCP server, ADB, Python snippets, сборка и тесты не запускались.

## Результат

Вердикт: **accepted-with-gaps**. Source page и machine facts сверены с указанным SHA и обновлены. Проверка подтверждает статически объявленные возможности этого MCP-сервера, но не совместимость его generated client calls с конкретной установленной сборкой exteraGram.

Основные исправления и уточнения:

1. Факты расширены с 31 до 37 уникальных утверждений. Уточнено покрытие Client Utils, ADB destructive operations, шаблонов, статического количества тестов, locked direct dependency versions, VS Code/debugpy инструкции и ограничений Python requirements.
2. Добавлена генераторная оговорка: `pyString` экранирует обратный слэш и двойную кавычку, но оставляет line breaks/control characters необработанными; произвольная многострочная строка может стать синтаксически неверным Python-литералом.
3. Отдельно зафиксирован риск построения shell-команд: `ADB_PATH`, serial и некоторые пути конкатенируются без shell-escaping и передаются строкой в `execSync`. Это статический вывод о непроверенных входных значениях; ADB-вызовы не выполнялись.
4. Уточнены расхождения документации с реализацией: Q docs указывает для `adb_shell` 10 секунд и обещает exit code, тогда как код использует 15 секунд и отдаёт статус успеха/ошибки и текст вывода; `adb_get_logs` фильтрует строки локально и поддерживает отсутствующий в docs `no_filter`. В M docs описан `generate_jmethod`/`@jmethod`, но в группе кода этого SHA регистрируется `generate_jmvel_method`, а отдельной регистрации `generate_jmethod` нет.
5. Уточнено, что docs R неполон для шаблонов: и registry, и input schema сервера принимают четыре значения (`minimal`, `hello_world`, `settings_demo`, `xposed_demo`), хотя prose справочника называет два.
6. Архитектура документации заявляет 101 unit test; статический подсчёт test declarations тоже дал 101 `it(...)`. Это подтверждает число объявлений, но не запуск, прохождение или runtime coverage тестов.

В `work/exteragram-mcp-facts.json` проверены ID, claims и ссылки на evidence: повторяющихся ID и дословных дублирующих claims нет. Общие знания о hook registration, HookResult, UI thread, очередях и Bulletin уже представлены в существующем API index/других source pages; эти повторы оставлены как независимое provenance. Для последующего объединения подходят существующие canonical API topics hooks, threading, UI и portability; отдельные ADB security/build/debug claims сохраняют source-specific контракт.

## Остаточные gaps

- Не проверялись реальные вызовы MCP-клиента, работа ADB на устройстве, деплой/удаление/перезапуск плагина, debugpy attach, generated Python snippets или совместимость API с конкретной версией exteraGram.
- `npm build`, Vitest, lint и prepublish lifecycle не запускались. Не подтверждены статус passing тестов, опубликованная npm-упаковка или её точное соответствие этому source tree.
- Из lockfile извлечены direct pins, но транзитивный dependency/security audit не проводился.
- README/docs содержат собственные заявления о целевых версиях клиента и SDK; эта проверка сверяла внутреннюю согласованность одного MCP SHA, а не актуальность справочника относительно последующих сборок клиента.

Статус source page: `accepted-with-gaps`.
