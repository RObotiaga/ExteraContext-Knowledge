# Независимая проверка tayugram-mcp

**Вердикт: `accepted-with-gaps`.** Проверен снимок `MRsuperkosmos/tayugram-mcp` на commit [`78f3b08048424418b42338ec1ff2a65ec7b2671c`](https://github.com/MRsuperkosmos/tayugram-mcp/tree/78f3b08048424418b42338ec1ff2a65ec7b2671c). Проверка статическая; runtime-поведение не подтверждалось.

## Закрепление источника

- `snapshot.json` указывает тот же repo, SHA и ветку `main`; дерево полное: 54 entries, из них 49 файлов и 5 каталогов.
- Снимок расширен до всех 49 файловых blobs дерева. SHA-256 файлов совпадают с 49 записями manifest, а Git blob SHA-1 каждого файла совпадает с соответствующей записью закреплённого `tree.json`. Пропущенных blobs и несовпадений нет.
- URL в manifest указывают на закреплённый SHA. `radar-urls.json` пуст; назначение сверено с `raw/tayugram-mcp/radar-context.md` и срезом `wiki/sources/radar.md` на строках 3018–3044. Радар считает проект MCP-каталогом Telegram-сценариев, а не plugin API; исходная страница это разграничение сохраняет.

## Независимое покрытие

Сверены README, TOOLS, changelog, install/agent-install, security/contributing, tdata-import docs, package manifest и lockfile, CI, сервер, tool registry/dispatcher, queue, config/login/CLI/selftest, базовый GramJS wrapper и все доменные модули `src/tg-*.js`, AyuGram archive/power modules, генератор TOOLS, импортёр/конвертер сессий, все `test-*.mjs`, cleanup helper и PowerShell scripts. Проверялись их объявления, описания, ключевые call-sites и согласованность с каталогом.

`TOOLS.md` содержит 200 нумерованных имён с описаниями. Статическая сверка имени по имени дала точное совпадение с 200 уникальными регистрациями из core registry и доменных модулей; ещё два `name` в исходниках относятся к MCP server и selftest client, не к tools. Список маркирует 146 read/54 write. Это статический анализ файлов, не запущенный реестр. Generator печатает required args, но не полный JSON Schema. Полные схемы лежат в `src/tools.js` и в функциях `tools()` доменных модулей. `@modelcontextprotocol/sdk` реализует серверный MCP protocol (`tools/list`/`tools/call` over stdio); `telegram`/GramJS — отдельный клиент для Telegram MTProto. Их не следует смешивать с ExteraGram Android plugin SDK/API.

## Исправления и найденные расхождения

- Исправлена граница покрытия: в raw-снимок добавлены оставшиеся файлы тестов, генератора, session conversion, scripts и lockfile; список файлов и хеши повторно проверены. На source page теперь перечислены точные пробелы статической и runtime-проверки.
- Исправлено описание каталога: `TOOLS.md` не содержит полный набор optional параметров или полный JSON Schema; он показывает имена, descriptions и обязательные аргументы.
- Добавлено различие MCP protocol, server SDK и GramJS Telegram client SDK.
- Зафиксировано расхождение safety contract: README, SECURITY, AGENT-INSTALL и CONTRIBUTING говорят, что destructive account operations отсутствуют, однако `tg_delete_messages` принимает произвольные ID и передаёт их `c.deleteMessages` без проверки авторства в wrapper (`src/tools.js:145-149`, `src/tg.js:678-684`). Это не доказывает итоговые серверные permission rules Telegram, но обещание «нельзя удалить чужие сообщения» не следует из кода.
- Заявленный в README и AGENT-INSTALL backoff на `FLOOD_WAIT` не найден в коде: `rpcMessage` лишь форматирует ошибку, а `RateLimitedQueue` pacing не ждёт серверный timeout и не повторяет запрос.
- В `src/tg.js:321` для сброса pending login упомянут `tg_logout`, но такого зарегистрированного tool нет. `test-ayu.mjs:9` безусловно вызывает `callTool("tg_logout", ...)`; статически `callTool` выбрасывает `Unknown tool` до дальнейших AyuGram assertions. Тест не запускался.
- Описание тестовой безопасности в CONTRIBUTING шире кода. `test-mutating.mjs` меняет cloud folders/contacts/sticker-set state/emoji status/draft/pins; очистка не восстанавливает прежний emoji status, draft, список pins или состояние sticker set. Не запускать его, исходя из обещания, что он пишет только в Saved Messages и полностью откатывает изменения.
- Root metadata `package-lock.json` расходится с `package.json`: lockfile всё ещё говорит `0.1.0`, `MIT`, Node `>=22.5`, а manifest — `1.0.0`, `Apache-2.0`, Node `>=18`. Прямые зависимости совпадают. Указанный Node >=18 для Telegram layer и SQLite requirement для AyuGram также следует читать вместе с конкретной документацией и lock metadata.
- `system_prevent_sleep` порождает detached/unref PowerShell helper; серверные shutdown handlers отключают Telegram client, но не вызывают `allowSleep`. В репозитории нет явной очистки этого дочернего процесса при штатном завершении MCP. Самостоятельный `ayu-supervisor.ps1` тоже бесконечный цикл. Lifecycle claim оставлен как непроверенный риск, поскольку Windows process behavior не запускалось.

## Повторы и идентификаторы фактов

В `outputs/plugin-wiki/work/tayugram-mcp-facts.json` сейчас 34 факта с 34 уникальными ID. Повторяющихся идентификаторов и дословно повторённых claims не найдено. Смежные факты об изоляции аккаунтов и платформенной поддержке относятся к разным контрактам; safety claim об удалении оставлен как один факт с несколькими доказательствами, а не размножен по отдельным документам.

## Остаточные пробелы

- Не запускались генератор, selftest, npm/CI, live account tests, импорт tdata, Windows scripts, AyuGram desktop или Telegram API calls. Результаты `runtime-verified` отсутствуют.
- Не проверялись реальные Telegram permissions/FLOOD_WAIT, SQLite-схема в пользовательской базе и поведение зависимостей после установки из stale lockfile.
- Не сверялись все 200 инструментов с внешним Telegram API contract. Достаточно проверены разделы/регистрация и доменные сценарии для описания источника; переносимый код должен ссылаться на точную схему и конкретный source module.

Проверка завершена с ограничениями: источник доступен и целостен, но несколько документов/тестов противоречат реализации, а сетевые/desktop эффекты остаются непроверенными.
