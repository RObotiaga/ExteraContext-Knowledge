---
type: skill
source_id: skill-foss
platform: Android / tool
review_status: accepted-with-gaps
review: ../reviews/skill-foss.md
date: 2026-09-28
---

# fossSquad/exteraSkill

Источник: [fossSquad/exteraSkill](https://github.com/fossSquad/exteraSkill), снимок `main` с SHA `0f5bde5296ba06a3fce4751228d26acd112d51bb` от 2026-09-27. Репозиторий заявляет GPL-3.0. Это агентский skill, документация и два вспомогательных Python-скрипта; реализация SDK, клиент exteraGram, примеры отдельными файлами и CI/build-конфигурация отсутствуют. Все содержимое рассматривается как материал исследования. Выполнения кода и проверки на устройстве не было.

## Назначение и выбор проекта

`SKILL.md` задаёт разработчику/агенту маршрут: сначала определить, разрабатывается Python-плагин или DEX-плагин, затем использовать соответствующие справочные страницы. Python-раздел объединяет обычный `BasePlugin`, Elyx и API-справку Telegram/Android; DEX-раздел отводит Java/Xposed-реализацию и Python-загрузчик для DEX. Это схема навигации самого skill, а не доказательство фактической поддержки конкретной установленной сборкой.

Документация предлагает одиночный Python-файл, когда проект мал и не использует ресурсы; Elyx предлагается при разрастании кода на несколько модулей, наличии UI-ресурсов/конфигурации, локализаций, локальных библиотек, повторяемой сборки, совместной работе или потребности в быстрой синхронизации. Это практическая рекомендация источника, не формальное ограничение SDK.

README предлагает установить skill через `npx skills add fossSquad/exteraSkill`. Это команда установки самого skill, а не ExteraGram SDK или плагина.

## Границы покрытия

Приобретённое дерево снимка полное: 48 из 48 blob-файлов совпадают с `tree.json` и `file-manifest.json`; SHA и SHA-256 файлов проверяются по этим сохранённым манифестам. Просмотрены README, skill-манифест и все справочные Markdown-файлы, включая встраиваемые примеры; оба Python-файла прочитаны статически как данные. У репозитория нет отдельного каталога examples, тестов, build-файлов или CI-конфигурации.

| Пути снимка | Извлечено | Пробелы |
|---|---|---|
| `README.md`, `SKILL.md`, `LICENSE` | Установка skill, триггеры и маршрутизация Python/DEX, карта документов, лицензия | Не выполнялась установка skill; лицензионные выводы ограничены метаданными и файлом LICENSE |
| `references/first-plugin.md`, `plugin-class.md`, `multi-account.md`, `python_plugins.md`, `setup.md` | Форма плагина, metadata, lifecycle, app events, hook регистрации/результаты, multi-account и стартовая среда | Утверждения не сверялись с живым SDK или приложением |
| `references/plugin-settings.md`, `ui_settings.md`, `alert-dialog-builder.md`, `bulletin-helper.md`, `android-utils.md`, `text-formatting.md` | Настройки, кастомные строки, dialogs/bulletins, Java callback wrappers, UI thread, форматирование текста | Примеры не запускались; конкретная доступность зависит от SDK/клиента |
| `references/client-utils.md`, `hook-utils.md`, `xposed-hooking.md`, `class-proxy.md`, `intents.md`, `file-utils.md`, `dev-server.md` | Очереди, Telegram requests, сообщения/media, reflection/hooks/proxies, intents, file handlers и dev-протокол | Нет реализации API; протокол не проверялся в рантайме, его auth/ACL в документе не описаны |
| `references/elyx.md`, `references/elyx/*.md` (10 файлов) | Выбор Elyx, refmap/archive, metadata, imports, assets/localization/settings, dependencies, public facade, development/build/reload | Elyx runtime, ElyxBuilder и внешний dev client не включены и не проверялись |
| `references/ChatActivity.md`, `LaunchActivity.md`, `MessageObject.md`, `MessagesController.md`, `SendMessagesHelper.md`, `TLRPC.md`, `common-source-classes.md`, `components-index.md` | Индексы классов, полей, методов и Telegram request-моделей, полезных при поиске точек интеграции | Это созданные на 30.07.2026 сводки; upstream Telegram URL в генераторе указывает на подвижный `master`, не зафиксированный SHA клиента exteraGram |
| `references/dex_plugins.md`, `available-libraries.md`, `pip.md`, `debugging.md` | Заявленные DEX prerequisites/build steps, ограничения pip, список библиотек, отладка и установка | Не представлены Gradle-проект, loader/build implementation или runtime test |
| `scripts/java2md.py`, `scripts/push_plugin.py` | Сопоставлены источники, парсеры/команды и расхождения README↔код | Скрипты намеренно не запускались; сетевые/устройственные эффекты не проверялись |

В основном дереве 45 Markdown-файлов, 2 Python-файла и LICENSE. Большие Telegram reference-файлы также просмотрены как generated inventories; они не дают закреплённого API-контракта конкретной сборки приложения.

## Документированные контракты и примеры

### Python plugin: metadata, lifecycle, hooks

Документация описывает Python-файл с top-level константами metadata и одним классом `BasePlugin`. Loader, согласно справке, извлекает metadata статическим AST-разбором, поэтому вычисляемые при импорте значения для `__id__`, `__name__`, версии и остальных полей не подходят. `__id__` и `__name__` названы обязательными; для `__id__` указаны 2–32 символа, латинская буква в начале и латинские буквы/цифры/`_`/`-` далее. Примеры задают `__app_version__ >=12.5.1` и `__sdk_version__ >=1.4.4.3` как baseline этого набора справки.

`on_plugin_load()` предназначен для регистрации hooks/listeners и фоновой работы; `on_plugin_unload()` — для очистки собственных ресурсов. Документация перечисляет `AppEvent.START`, `STOP`, `PAUSE`, `RESUME`. Объявление callback само по себе не регистрирует событие: вызовите `add_hook(name, match_substring=False, priority=0)` или `add_on_send_message_hook(priority=0)` во время загрузки. Для send hook отдельно отмечено, что медиа-сообщение может не иметь строкового `params.message`; пример сначала проверяет его наличие и тип.

Hook callbacks для запросов, ответов, updates и исходящих message params получают `account`. `HookResult` сочетается со стратегиями `DEFAULT`, `CANCEL`, `MODIFY` и `MODIFY_FINAL`; изменяемое значение возвращается в подходящем поле (`request`, `response`, `update`, `updates` или `params`). Пример `.hello Alice` меняет `params.message` и возвращает `MODIFY`; неизвестную команду оставляет без изменений. Сам skill рекомендует не выполнять долгую сеть/работу с файлами непосредственно в UI-hook.

Есть явное расхождение версий: основной пример и практический baseline в `plugin-class.md` — SDK `1.4.4.3`, тогда как `multi-account.md` требует SDK `>=1.4.5.0` для `account`-параметров, `AccountClient`, `get_client`, `get_hook_account` и `get_selected_account`; Elyx metadata/quick-start задают `sdk_version >=1.4.5.3`. Следовательно, цифра 1.4.4.3 в skill не подтверждает все описанные на дочерних страницах API.

### Учетные записи и выполнение

`multi-account.md` говорит, что залогиненные аккаунты остаются подключёнными и могут вызывать hooks, даже если они не выбраны в UI. Вызовы account-scoped helpers без явного account обращаются к выбранному UI аккаунту; ответ на hook следует привязать к account callback через `self.client(account)`, `get_client(account)` или `account=`. Для `NotificationCenterDelegate.didReceivedNotification(id, account, args)` account передаётся явно, автоматический hook scope не заявлен. `get_media_controller()` указан как глобальный исключительный singleton без account-параметра.

Для сетевой/файловой работы справка предлагает `run_on_queue(func, queue=PLUGINS_QUEUE, delay=0)`; задержка измеряется миллисекундами. Перечислены очереди `STAGE_QUEUE`, `GLOBAL_QUEUE`, `CACHE_CLEAR_QUEUE`, `SEARCH_QUEUE`, `PHONE_BOOK_QUEUE`, `THEME_QUEUE`, `EXTERNAL_NETWORK_QUEUE`, `PLUGINS_QUEUE`. Для UI предназначен `run_on_ui_thread(func, delay=0)`. `R(fn)` создаёт Java `Runnable`, когда принимающий API требует именно этот объект; `OnClickListener(fn)` и `OnLongClickListener(fn)` оборачивают обработчики Android, причём long-click callback возвращает bool.

### Requests, media, UI и файлы

`send_request(request, callback, account=...)` описан как обёртка над отправкой TLObject через `ConnectionsManager`; callback получает `(response, error)`, а результат вызова — request ID. `send_text`, `send_photo`, `send_document`, `send_video` и `send_audio` автоматически готовят типичные параметры; `parse_mode` принимает HTML или Markdown. Низкоуровневый `send_message(params, parse_mode=None)` принимает словарь полей `SendMessagesHelper.SendMessageParams`. `edit_message(message_obj, ...)` рассчитан на настоящий Java `MessageObject`, может менять текст и/или заменять медиа; неизвестный `parse_mode` документирован как `ValueError`.

`create_settings() -> List[Any]` возвращает строки из `ui.settings`: `Header`, `Divider`, `Switch`, `Selector`, `Input`, `Text`, `EditText`, `Custom`. Для персистентности класс плагина предоставляет `get_setting`, `set_setting`, `export_settings`, `import_settings`; `reload_settings=True` предлагается при изменении структуры отображаемых настроек. Для кастомных строк `SimpleSettingFactory` разделяет `create_view(...)` и `bind_view(...)`, с необязательными `create_item`, click/long-click, attached-view и equality callbacks.

`AlertDialogBuilder` документирует message, loading и spinner dialogs, списки, кнопки, custom views, lifecycle и listeners; справка предупреждает использовать действующий Android `Context` и работать с диалогом на UI thread. `BulletinHelper` включает standard/simple/two-line, action/undo и contextual bulletins, с duration constants 1500/2750/5000 ms. Это SDK документация, а не подтверждение доступности каждого helper в произвольной сборке.

`hook_utils` документирует поиск Java-класса по полному имени и доступ к instance/static private fields. В Xposed-разделе перечислены `MethodHook` (before/after), `MethodReplacement` (полная замена), функциональные `before=`/`after=` callbacks и фильтры аргументов/результатов. `param.args` можно менять; вызов `param.setResult(...)` из before-hook пропускает исходный Java method. `class-proxy.md` описывает генерацию Java subclass через `java_subclass`, точечные `joverride`/`joverload`, поля и pre/post constructors; `new_instance()` возвращает Python peer, а `.java` — исходный Java объект. Это сложные документированные API, а не подтверждённые возможности любого клиентского билда.

Файловые helpers перечисляют app/cache/media directories и чтение/запись текста/bytes, листинг и удаление. `FilesController.register(file_info)` связывает extension и callback, опционально ограничивает места через whitelist/blacklist и иконки при `SUPPORT_ICONS`; для unregister нужен возвращённый secret. `intents` описывает глобальные before/after handlers, фильтры по scheme/host/path/action/type/categories/flags, callback-параметры, handle и `unhandle`. По этому же документу before-handler может вернуть `True`, чтобы остановить остальные Python handlers и исходную Java intent обработку; after-handler не блокирует исходный поток.

### Elyx: структура, публичный фасад, сборка

Elyx рекомендован для многомодульного плагина или проекта с ресурсами, переводами, библиотеками и repeatable build. Это формат, сохраняющий `BasePlugin`, а не отдельный runtime API плагина. Архив ZIP-совместимый (`.elyx`, `.eaf` и описанные варианты `.zip`); `refmap.yml`/`.yaml`/`.json` должен находиться в корне архива. Нельзя упаковывать внешний каталог-обёртку вместо содержимого проекта. `refmap.main` выбирает entry module; если опущен, документ по умолчанию ищет корневой `main.py`. Инстанцируется первый найденный в entry module подкласс `BasePlugin`, поэтому helper-классы предлагается импортировать из других файлов.

Документация просит импортировать из стабильного фасада `elyx`; внутренние физические модули движка/importer/installer считаются private. Локальные модули namespaced по ID плагина; для computed import рекомендуется `elyx.import_module`, поскольку обычный `importlib.import_module` может не получить plugin context. Описаны plugin-bound `assets`, `metainfo`, `refmap`, `settings`, `strings`, asset readers/renderers, localization lookup, SettingsController, callback proxies, `gen`/`gen2`, `mvel_execute` и `LazyDict`.

Зависимости могут быть PIP requirements, локальными wheel-файлами или объявлениями `requires` других плагинов. Для PIP описана установка pure-Python `none-any` wheels, общий набор библиотек между плагинами и возможные version conflicts. `available-libraries.md` заявляет Python 3.11 и перечисляет beautifulsoup4, debugpy, lxml, packaging, pillow, requests и PyYAML. Локальный/Android native wheel нельзя считать переносимым по этой справке; dependency install зависит от сети. Для Elyx документация требует Python 3.11-bytecode при компиляции `.pyc`.

Development guide описывает разовую начальную установку/включение Elyx archive перед live reload и ADB port forwarding к `127.0.0.1:42690`. DevServer обменивается последовательными UTF-8 JSON объектами; `@` — имя команды, `#` — request ID. Базовые команды включают ping, list, enable/disable/reload, write/remove plugin и start/stop debugger. Elyx передаёт zlib-compressed JSON в base64 поле `data` для сравнения/применения изменений. Справка называет `ElyxBuilder` и внешний `elyx_dev_client.py`, но они не содержатся в снимке и их CLI не часть runtime API.

DEX guide документирует типичный Android library проект с `build.gradle`, `libs/exteragram.jar` как compileOnly stubs, Java entry point и Python loader. Он предлагает получить stubs из APK через exteralib, собирать с Java 17/Android SDK 35/build-tools 36.0.0, затем прогонять D8 и получить `classes.dex`; отдельного проекта или Gradle task в снимке нет, поэтому версия toolchain и steps не подтверждены сборкой. Loader example использует `DexClassLoader` (текст также упоминает `InMemoryDexClassLoader`), читает DEX с `/storage/emulated/0/Android/media/com.exteragram.messenger/classes.dex`, загружает класс и reflection вызывает `initAndStart()`. Debugging guide даёт ADB push в этот путь, затем app `Install from file` и in-app restart; она специально говорит, что `am stop` не выполняет корректный reload. Это описанный workflow, не результат установки или запуска.

## API-указатель

Все строки ниже имеют статус `docs` и указывают раздел документации; они не являются утверждением об успешном вызове в runtime.

| Модуль/класс | Документированные вызовы | Назначение и контекст | Источник |
|---|---|---|---|
| `BasePlugin` | `on_plugin_load()`, `on_plugin_unload()`, `on_app_event(event_type)`, `create_settings()` | Жизненный цикл, события приложения, страница настроек | [plugin-class](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/plugin-class.md#L90) |
| `BasePlugin` hooks | `add_hook(name, match_substring=False, priority=0)`, `add_on_send_message_hook(priority=0)`, `pre_request_hook(...)`, `post_request_hook(...)`, `on_update_hook(...)`, `on_updates_hook(...)`, `on_send_message_hook(...)` | Подписки и interception запросов, updates и исходящих сообщений; callback получает account | [plugin-class](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/plugin-class.md#L261) |
| `client_utils` | `run_on_queue(func, queue, delay)`, `send_request(request, fn)`, `send_text(...)`, `send_photo(...)`, `send_document(...)`, `send_video(...)`, `send_audio(...)`, `send_message(params, parse_mode=None)`, `edit_message(message_obj, ...)` | Background jobs, TL requests, send/edit flows | [client-utils](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/client-utils.md#L15) |
| account helpers | `self.client(account)`, `get_client(account)`, account-scoped getters, `get_hook_account()`, `get_selected_account()` | Вызовы в контексте account, который породил hook; API перечислены для SDK ≥1.4.5.0 | [multi-account](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/multi-account.md#L9) |
| `android_utils` | `run_on_ui_thread(func, delay=0)`, `R(fn)`, `OnClickListener(fn)`, `OnLongClickListener(fn)`, `log(data)`, `copy_to_clipboard(text)` | UI scheduling, Java callbacks, logging и clipboard | [android-utils](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/android-utils.md#L15) |
| dialogs / bulletins | `AlertDialogBuilder(...)`, `set_title(...)`, `set_message(...)`, `set_items(...)`, button/listener methods, `show()`/`dismiss()`; `BulletinHelper.show_*` | Message/progress dialogs, contextual and actionable bulletins; dialog work is documented for UI thread | [alert-dialog-builder](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/alert-dialog-builder.md#L48), [bulletin-helper](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/bulletin-helper.md#L31) |
| settings | `get_setting`, `set_setting`, `export_settings`, `import_settings`, `SimpleSettingFactory(...)` | Значения плагина и built-in/custom settings rows | [plugin-settings](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/plugin-settings.md#L150) |
| Xposed/reflection | `find_class(...)`, `get_private_field(...)`, `set_private_field(...)`, `hook_method(...)`, `param.getResult()`, `param.setResult(value)` | Java reflection, hook/replacement и изменение результата | [hook-utils](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/hook-utils.md#L14), [xposed-hooking](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/xposed-hooking.md#L11) |
| class proxy | `java_subclass`, `joverride`, `joverload`, `jfield`, `new_instance()`, `.java` | Java subclasses, перегрузки и мост к исходному Java object | [class-proxy](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/class-proxy.md#L1) |
| file handlers | `FilesController.register(file_info)`, `unregister(extension, secret)` | Перехват открытия файлов и необязательные custom icons | [file-utils](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/file-utils.md#L190) |
| intents | `new_global_before_handler(...)`, `new_global_after_handler(...)`, `HandlerHandle`, `unhandle(handler_id)`, `parse(url)` | Фильтрация/реакция на обработку ссылок; отличие блокирующего before от after | [intents](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/intents.md#L1) |
| Elyx facade | `get_environment()`, `import_module(...)`, `Assets(...)`, `Asset(...)`, `SettingsController(...)`, `gen(...)`, `gen2(...)`, `mvel_execute(...)` | Описанный публичный Elyx API; import только через `elyx` | [Elyx public API](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/elyx/public-api.md#L7) |
| DevServer | `ping`, `get_plugins`, `enable_plugin`, `disable_plugin`, `reload_plugin`, `write_plugin`, `remove_plugin`, `start_debugger`, `stop_debugger`; Elyx `elyx_ping`, `get_elyx_plugins`, `elyx_compare_folder`, `elyx_changes` | Документированный TCP JSON протокол для dev tooling | [dev-server](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/references/dev-server.md#L28) |

## Проблемы происхождения и точности

1. **Skill README ссылается на отсутствующий путь скрипта.** `SKILL.md` называет `scripts/adb_push_py.py`, но дерево содержит `scripts/push_plugin.py`. У скрипта `push_plugin.py` и его usage-строки встречается старое имя `adb_push_py.py`.
2. **Push-скрипт сообщает успех без подтверждения сервера.** По статическому чтению он делает ADB forward и отправляет `write_plugin` и `reload_plugin` по двум TCP-соединениям, но не читает/проверяет ответы; печать «successfully» не является подтверждением доставки/перезагрузки.
3. **Reference generator неприкреплён к версии Telegram.** `java2md.py` скачивает `DrKLO/Telegram/refs/heads/master` для шести файлов. Парсер нормальных классов описан как базовый и не полностью поддерживающий многострочные declarations; TLRPC parser тоже извлекает только совпавшие строки полей. Значит generated Markdown — неполный индекс, не неизменная спецификация exteraGram API.
4. **Справки содержат конкурирующие baseline.** 1.4.4.3 для общего skill соседствует с multi-account 1.4.5.0 и Elyx 1.4.5.3. Для конкретного API следует брать отдельную минимальную версию документа и подтверждать на целевой сборке.
5. **Нет независимого runtime evidence.** Команды тестирования приведены справочно; никаких результатов устройства, версии клиента, logs или CI данный снимок не содержит.

## Источники

- [README](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/README.md)
- [SKILL.md](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/SKILL.md)
- [tree snapshot](../../raw/skill-foss/tree.json), [file manifest and SHA-256](../../raw/skill-foss/file-manifest.json)
- [java2md.py](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/scripts/java2md.py), [push_plugin.py](https://github.com/fossSquad/exteraSkill/blob/0f5bde5296ba06a3fce4751228d26acd112d51bb/scripts/push_plugin.py)
