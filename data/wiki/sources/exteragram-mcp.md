---
type: source
source_id: exteragram-mcp
platform: Android / tool
review_status: accepted-with-gaps
review: ../reviews/exteragram-mcp.md
date: 2026-09-28
---

# CatalystDev exteraGram MCP

Источник: [cataIystdev/exteragram-mcp](https://github.com/cataIystdev/exteragram-mcp), лицензия MIT. Снимок default branch `main`, commit [`ad824092ae60d785d0f0f21f1897b74118a186b1`](https://github.com/cataIystdev/exteragram-mcp/tree/ad824092ae60d785d0f0f21f1897b74118a186b1), получен 2026-09-27. `package.json` указывает `@catalystdev/exteragram-mcp` 1.0.0 и Node.js >=20.

## Роль источника

Это TypeScript MCP-сервер, который предоставляет агенту инструменты для генерации Python-сниппетов плагинов, справочные сведения об SDK, состояние текущего проекта и операции ADB. Это не реализация SDK ExteraGram. Большинство инструментов возвращает код и не подтверждает его совместимость с установленным клиентом; только группа ADB выполняет внешние команды. Источник полезен для воспроизводимых шаблонов и workflow, но его справочники привязаны к снимку и требуют сверки с фактической версией клиента.

## Покрытие

| Область и прочитанные пути | Извлечено | Граница/пропуск |
|---|---|---|
| README, `docs/README.md`, `docs/tools/overview.md`, `docs/api/architecture.md`, `docs/deployment/client-config.md`, `LICENSE`, `package.json`, `tsconfig.json`, `vitest.config.ts` | Назначение, инструменты, архитектура, клиентская конфигурация, лицензия, зависимости и команды сборки/тестов | Команды не запускались; готовый npm-артефакт отдельно не сравнивался с исходниками |
| `src/index.ts`, `src/server.ts`, `src/types.ts`, `src/state/plugin-context.ts` | stdio lifecycle, регистрация A–R, типы и in-memory PluginContext/валидация | Runtime MCP-клиента и поведение ExteraGram не проверялись |
| Все `src/tools/*.ts`: `context`, `scaffold`, `lifecycle`, `settings`, `menu`, `request-hooks`, `message-hook`, `client-utils`, `android-utils`, `hook-utils`, `file-utils`, `text-formatting`, `class-proxy`, `xposed-hooking`, `alert-dialog`, `bulletin`, `adb`, `reference` | Объявления и схемы инструментов, генерируемые сниппеты, отдельные реализации и call-sites | Описываемые Java/Python API клиента здесь не реализуются и не проверялись на устройстве |
| `src/codegen/python-builder.ts`, `src/codegen/templates.ts` | Общие генераторы Python-кода и встроенные шаблоны | Сгенерированный результат не запускался в целевом приложении |
| `docs/tools/A-context.md` — `R-reference.md`, включая `docs/tools/overview.md` | Документация всех групп инструментов, примеры, ограничения и объявленные сигнатуры | Документация местами противоречит коду и сама по себе не является контрактом SDK |
| `tests/codegen/python-builder.test.ts`, `tests/codegen/templates.test.ts`, `tests/state/plugin-context.test.ts`, `tests/tools/adb.test.ts`, `tests/tools/hooks.test.ts`, `tests/tools/scaffold.test.ts`, `tests/tools/settings.test.ts` | Статический обзор охваченных тестами областей и package scripts; в семи файлах насчитан 101 вызов `it(...)`, совпадающий с числом в architecture docs | Ни один тест не запускался; статический подсчёт объявлений не подтверждает их успешное выполнение |
| `package-lock.json` | Зафиксированный lockfile присутствует в дереве | Полный анализ всех транзитивных зависимостей и публикации npm не входил в задачу |

В `tree.json` нет других путей, требующих обзора: снимок не усечён. Всего прочитаны 18 tool-модулей и 7 test-файлов, перечисленных в дереве; чужие программы, сборка и установка не запускались.

## Архитектура и runtime границы

`src/index.ts` создаёт `McpServer` с именем `@catalystdev/exteragram-mcp`, версией 1.0.0 и capability `tools`, вызывает `registerAllTools`, подключает `StdioServerTransport`, пишет статус в stderr. `src/server.ts` централизует регистрацию 18 независимых групп A–R. В `package.json` указаны MCP SDK `^1.12.0`, Zod `^3.24.0`, TypeScript `^5.8.0`, Vitest `^3.0.0`, `build: tsc`, `test: vitest run`, `test:coverage` и `prepublishOnly: npm run build && npm test`.

Подсчёт `server.registerTool(...)` в 18 сохранённых `src/tools/*.ts` даёт **81 объявление**. README и `docs/tools/overview.md` называют набор «76 инструментов в 18 группах». Фактические группы подтверждаются `registerAllTools`, но описательное число 76 в этом SHA расходится со статическим подсчётом. Архитектурная документация сообщает 101 unit-тест; статический подсчёт семи файлов подтверждает 101 вызов `it(...)`, однако выполнение и результат тестов не проверялись.

Документация архитектуры определяет общий результат инструмента как MCP text content и говорит, что генераторы возвращают Python-код строкой для последующей вставки через IDE. Сервер сам не редактирует плагинные файлы генераторами. Исключение по характеру эффекта — ADB-модуль, который вызывает `child_process.execSync`.

## Состояние и валидация контекста

`src/state/plugin-context.ts` хранит один `currentContext` в памяти процесса. Контекст включает `plugin_id`, `plugin_name`, локальный `file_path`, optional `device_serial`, `registered_hooks: Set<string>` и метаданные. `setPluginContext(pluginId, pluginName, filePath, deviceSerial?)` отказывает при ошибках валидации и начинает новый `Set`; `clearPluginContext()` обнуляет контекст. Сериализация превращает Set в массив. Перезапуск MCP-процесса сбрасывает всё состояние, durable storage отсутствует.

Фактическая проверка ID — `/^[a-z][a-z0-9_-]{1,31}$/` (2–32 символа, только нижний регистр). `__version__` проверяется semver-подобным regexp, `app_version` и `sdk_version` — оператором сравнения и числовыми частями версии. Существенное расхождение: комментарий реализации прямо указывает, что синтаксис PEP 508 для requirements **не** проверяется, а цикл валидатора отбрасывает только пустые строки. Документация `A-context.md` утверждает обратное. Не трактовать успешную валидацию requirements как валидацию спецификаторов.

`registerHook` добавляет имя в набор контекста, а отсутствие контекста вызывает ошибку. Это bookkeeping для подсказок агенту: он не доказывает, что сгенерированный код действительно вставлен и hook зарегистрирован в клиенте.

## Группы и практические вызовы

| Группа / модуль | Сигнатура или вызов | Назначение и замечания |
|---|---|---|
| A `src/tools/context.ts` | `set_plugin_context(plugin_id, plugin_name, file_path, device_serial?)`; `get_plugin_context`; `clear_plugin_context`; `validate_plugin_metadata` | Задать единственный контекст, получить/сбросить его, отдельно проверить metadata. Учитывать расхождение PEP 508 выше. |
| B `src/tools/scaffold.ts` | `generate_plugin_file`; `generate_metadata_block`; `generate_import_block` | Генерирует строку полного `.py`, metadata или imports. Документация требует прямые metadata literals, поскольку клиент парсит их через AST; requirements добавляются при непустом списке. |
| C `src/tools/lifecycle.ts` | `generate_on_plugin_load(body?)`; `generate_on_plugin_unload(body?)`; `generate_on_app_event(events)` | Каркасы lifecycle; документированные `AppEvent`: START, STOP, PAUSE, RESUME. Setup хуков и listeners помещать в load, очистку — в unload. |
| D `src/tools/settings.ts` | `generate_settings_ui(components)`; `generate_settings_component(spec)`; `generate_get_setting`; `generate_set_setting`; `generate_export_import_settings`; `generate_simple_setting_factory` | Компоненты Header, Divider, Switch, Selector, Input, EditText, Text, Custom; callbacks и типы значений описаны в `D-settings.md`. Строковые поля некоторых specs являются Python-выражениями. |
| E `src/tools/menu.ts` | `generate_menu_item(...)` | Код для `add_menu_item(MenuItemData)` и callback; типы: сообщение context menu, drawer, chat action, profile action. |
| F `src/tools/request-hooks.ts` | `pre_request_hook(request_name, account, request)`; `post_request_hook(request_name, account, response, error)`; `on_update_hook(update_name, account, update)`; `on_updates_hook(container_name, account, updates)` | Инструменты генерируют пару: регистрацию `self.add_hook(...)` и метод. Без регистрации в `on_plugin_load` метод не включается в обработку. Результат использует DEFAULT/CANCEL/MODIFY/MODIFY_FINAL и payload соответствующего типа. |
| G `src/tools/message-hook.ts` | `on_send_message_hook(self, account, params) -> HookResult`; `self.add_on_send_message_hook(priority=...)` | Hook исходящего сообщения требует точного имени и вызова регистрации в load. Документация рекомендует проверить `params.message` как `str`; описанные поля включают `peer`, `replyToMsg`. |
| H `src/tools/client-utils.ts` | Высоко- и низкоуровневая отправка текста/медиа; `edit_message`; `send_request`; `run_on_queue`; `NotificationCenterDelegate`; справочники controller/queue | Генерирует call-sites для клиентских утилит и справочные списки controller/queue. Это примеры API, не код этих утилит. `PLUGINS_QUEUE` описана как предпочтительная для plugin background work. |
| I `src/tools/android-utils.ts` | `run_on_ui_thread(fn, delay=0)`; `OnClickListener`; `OnLongClickListener`; `R(callable)`; clipboard/log snippets | Помощники UI-thread, Android listener/Runnable, clipboard и logging. `on_long_click` должен вернуть boolean о поглощении события. |
| J `src/tools/hook-utils.ts` | `find_class`; `get/set_private_field`; `get/set_static_private_field` | Сниппеты Java reflection с обработкой ошибок/None; документация предупреждает о хрупкости при обновлениях приложения. |
| K `src/tools/file-utils.ts` | `read_file`; `write_file`; `delete_file`; `ensure_dir_exists`; `list_dir`; `list_standard_dirs` | Генерация файловых call-sites и известных каталогов. `write_file` не создаёт parent dir; генератор по умолчанию добавляет `ensure_dir_exists`. |
| L `src/tools/text-formatting.ts` | `parse_text(text, parse_mode, is_caption=False)`; `list_html_tags` | Документация описывает преобразование HTML/Markdown в plain text плюс TL entities; при caption используется ключ `caption`, иначе `message`. |
| M `src/tools/class-proxy.ts` | Java subclass/override, MVEL, fields, Java helper `J`, создание/оборачивание экземпляров, `from_java`, `PyObj`, `jclassbuilder` | Генератор DSL Java-подклассов через DexMaker. Ограничения документации: base class не final; перегрузки требуют явных типов; сложные overload — Java reflection. `M-class-proxy.md` дополнительно описывает `generate_jmethod`/`@jmethod`, но реализация этого SHA не регистрирует такой инструмент, а вместо него регистрирует `generate_jmvel_method`. |
| N `src/tools/xposed-hooking.ts` | `self.hook_method(method, handler, priority=10)`; `hook_all_methods`; `hook_all_constructors`; `unhook_method` | Сниппеты Xposed-style hook для метода/конструктора и filters. В примере используется `find_class(...).getDeclaredMethod(...)`; документация запрещает вызывать `getClass()` на самом Class и рекомендует хранить unhook handles. |
| O `src/tools/alert-dialog.ts` | `AlertDialogBuilder(context, progress_style).show()` | Каркас message/loading/spinner dialogs, callbacks, items и custom view. Для loading документация указывает `set_progress(0..100)` и `dismiss()`. |
| P `src/tools/bulletin.ts` | `BulletinHelper.show_*` | 11 описанных видов bulletin; docs заявляет UI-thread выполнение и константы 1500/2750/5000 мс для SHORT/LONG/PROLONG. |
| Q `src/tools/adb.ts` | `adb_check_devices`, deploy/list/remove plugin, get logs (`clear`, `no_filter`), restart, push/pull, `adb_shell(command, timeout_ms?)` | Реальные ADB-вызовы. Путь плагинов — `/data/user/0/com.exteragram.messenger/files/plugins/<id>.py`, package — `com.exteragram.messenger`. Выбор serial: аргумент > PluginContext > `ADB_SERIAL`. `adb_shell` принимает произвольную shell-команду; реализация использует execSync и timeout, default 15000 мс. Формирование команд конкатенацией не экранирует shell-ввод. В документации default timeout указан как 10000 мс и обещан exit code; фактический handler сообщает общий успех/ошибку и вывод, без exit code. `adb_get_logs` фильтрует logcat локально; параметр `no_filter` есть в коде, но отсутствует в Q docs. |
| R `src/tools/reference.ts` | `list_hook_strategies`; `list_app_events`; `list_menu_types`; `list_settings_components`; `list_available_libraries`; `list_common_classes`; `get_plugin_template`; `explain_pitfalls`; `list_hook_filters` | Справочная база, шаблоны и pitfalls. `get_plugin_template` schema принимает четыре ключа из `templates.ts`; R-reference prose документирует только два. Это сведения самого MCP-сервера и его версии, не гарантия текущего SDK. |

### Общие техники

- Сначала задавать PluginContext, затем генерировать файл и функциональные блоки. Само состояние не синхронизируется с файлом автоматически.
- Для request/update хуков помещать и метод, и регистрационный `add_hook` в плагин; для outbound message hook использовать точный метод `on_send_message_hook` и `add_on_send_message_hook`.
- Выполнять UI-изменения через UI thread. Для блокирующей работы использовать соответствующую queue; документация рекомендует `PLUGINS_QUEUE`.
- Java reflection/Xposed-код ограничивать try/except и сохранять возвращённые handles для отписки при unload.
- Перед `write_file` создавать директорию; перед изменениями `params.message` проверять тип.
- Сверять Python imports, class names и client API с реальным SDK целевой сборки: MCP генерирует текст, а не проверяет его на устройстве.
- Общий `pyString` экранирует только обратный слэш и двойную кавычку; он не преобразует переводы строк и другие управляющие символы в escape-последовательности, поэтому произвольный многострочный ввод не становится корректным Python-литералом автоматически.
- ADB-команды собираются конкатенацией в shell-строку для `execSync`; кроме преднамеренно произвольного `adb_shell`, необработанные `ADB_PATH`/serial и аргументы-пути тоже нельзя считать безопасными для недоверенного ввода.

## Build, тесты и конфигурация

`package.json` объявляет `build` (TypeScript compiler), `start`, `dev`, `test`, `test:watch`, `test:coverage`, `lint` и `prepublishOnly`. Lockfile данного SHA фиксирует прямые версии MCP SDK 1.29.0, Zod 3.25.76, TypeScript 5.9.3 и Vitest 3.2.4 в рамках диапазонов package manifest. В дереве есть семь test-файлов по codegen/templates, context, ADB, hooks, scaffold и settings. Результаты их исполнения отсутствуют: сборка, тесты и приложение не запускались.

`docs/deployment/client-config.md` приводит stdio-конфиги для Claude Code и Cursor/Windsurf с `npx -y @catalystdev/exteragram-mcp`, `ADB_PATH` и необязательным `ADB_SERIAL`; локальная конфигурация запускает `dist/index.js`. В таблице окружения `MCP_PORT` помечен как не реализованный в v1. Отдельно документ приводит VS Code debugpy attach на localhost:5678, path mapping и `adb forward tcp:5678 tcp:5678`; это описательная инструкция и не проверялась на устройстве. Справочник R описывает предварительно установленные библиотеки, ограничение requirements pure-Python wheels и риск конфликтов, поскольку окружение общее для плагинов.

## Несогласованности и ограничения

1. **Число инструментов:** README и overview заявляют 76, статический подсчёт регистраций в коде снимка — 81.
2. **PEP 508:** A-context docs утверждает проверку синтаксиса требований; реализация только запрещает пустую строку.
3. **Шаблоны:** реестр `templates.ts` и schema `get_plugin_template` принимают `minimal`, `hello_world`, `settings_demo`, `xposed_demo`; R-reference prose документирует только первые два и неполон.
4. **Class Proxy docs/code:** `M-class-proxy.md` описывает `generate_jmethod`/`@jmethod`, которого нет среди регистраций кода; кодовая группа вместо этого предоставляет `generate_jmvel_method`.
5. **ADB docs/code:** документация Q расходится с реализацией по таймауту и exit code для `adb_shell`, описывает `grep` для logcat вместо локальной фильтрации и не перечисляет кодовый параметр `no_filter`.
6. **Тесты:** в снимке есть 101 статическое объявление `it(...)`, совпадающее с architecture docs, но тесты не запускались и passing-статус не известен.
7. **Эксплуатация и безопасность:** `adb_shell` предоставляет произвольный shell через ADB. Формирование команд через `execSync` также включает необработанные значения окружения, serial и путей; это заслуживает отдельного исправления/проверки границ доверия upstream.
8. **Генерация строк:** `pyString` не экранирует переводы строк и управляющие символы; многострочные или управляющие данные могут дать некорректный Python-код.
9. **Совместимость:** данные о классах, путях, callback-сигнатурах и API взяты из документации/генераторов CatalystDev. Эквивалентность текущему SDK ExteraGram, поведение на устройстве, npm опубликованная сборка и изменения после SHA не проверялись.
10. **Отладка и зависимости:** VS Code/debugpy процедура приведена только в документации; runtime-совместимость отладки и фактическая поддержка перечисленных Python-библиотек на целевой сборке не подтверждены.

Машинный набор из 37 уникальных утверждений находится в `work/exteragram-mcp-facts.json`.
