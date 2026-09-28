---
type: source
source_id: vestr-plugins
platform: Android (Python plugins for ExteraGram/AyuGram ecosystem)
review_status: accepted-with-gaps
review: ../reviews/vestr-plugins.md
date: 2026-09-28
---

# mr-Vestr/plugins: три Python-плагина и практические интеграции с клиентом

- Источник: [mr-Vestr/plugins](https://github.com/mr-Vestr/plugins), ветка `main`, pinned SHA [`c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c`](https://github.com/mr-Vestr/plugins/tree/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c), зафиксирован 2026-09-27 15:53 UTC. GitHub commit API повторно подтвердил SHA, дату `2026-08-31T16:18:35Z`, сообщение `Update ADB Lite link to English documentation` и дерево `c1f4671ffdbb19d7c392355cae7a16193c684cec`; commit signature API отмечает как verified. Ссылки на исходники ниже закреплены за SHA снимка.
- Роль: коллекция автора из трёх Android Python-плагинов: Templates (шаблоны сообщений), Plugin creator (создание файлов из текста) и ADB Lite (передача и установка плагинов с ПК через Wi-Fi). Это примеры интеграции с `BasePlugin`, `ui.settings`, `client_utils`, `hook_utils` и внутренними Java-классами Telegram/ExteraGram, а не SDK или независимая спецификация API.
- Метаданные снимка: Templates `4.2`, `__min_version__ = "12.1.1"`; Plugin creator `3.1`, ADB Lite `1.0`, оба с `__min_version__ = "12.5.0"`. Это требования, записанные в конкретных исходниках, а не подтверждённая совместимость с актуальными сборками.
- Лицензия: GitHub `repository.json` сообщает `license: null`, а pinned tree не содержит отдельного файла лицензии. Наличие приветственного комментария с просьбой отметить автора не устанавливает юридическую лицензию на повторное использование.
- Граница доказательств: код, metadata/config JSON и документация прочитаны как данные; плагины, клиент, Desktop-компаньон и сетевой протокол не запускались. Результатов установки или проверки на устройстве нет; все поведенческие утверждения остаются `code` (статический исходник) либо `docs`. Внешние обращения конкретной установленной версии к mutable `main` могут получить конфигурацию, отличную от pinned `config.json`.

## Покрытие

| Пути снимка и материалы | Извлечено | Пропуски и граница покрытия |
|---|---|---|
| `snapshot.json`, `tree.json`, `repository.json`, `file-manifest.json`, `radar-context.md`, `radar-urls.json` | Идентичность и SHA, список файлов/контрольные суммы, метаданные GitHub, контекст радара | `radar-urls.json` пуст; дополнительных исторических commit URL не задано. GitHub не указывает лицензию |
| [`README.md`](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/README.md), [`README_EN.md`](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/README_EN.md), root `config.json` | Каталог трёх плагинов, заявленный путь установки, badges и deeplink-конфигурация | Скриншоты и внешние Telegram-ссылки не исследовались как поведение клиента |
| `Templates/TEMPLATES_RU.md`, `Templates/TEMPLATES_EN.md`, `Templates/config.json`, `Templates/templates.py` | Обе версии руководства, сценарии, редакторы настроек, локализационное расхождение, metadata, message hook, Markdown/entity conversion, topic-send, import/export, lifecycle, update/config calls и выделенные UI/reflection hooks | Implementation (7 798 строк) выборочно сверен по metadata и центральным сохранению/отправке/импорту/lifecycle/update/UI методам, не построчно; реализация всего UI и все import/export error paths не инвентаризованы |
| `Plugin creator/PLUGIN_CREATOR_RU.md`, `Plugin creator/PLUGIN_CREATOR_EN.md`, `Plugin creator/config.json`, `Plugin creator/plugin_creator.py` | Обе версии руководства; способы создания файлов, настройки редактора, metadata, command/send-button hooks, temp-file/document sender, direct save/install | Implementation (5 517 строк) выборочно сверен по metadata и центральным hooks/file/send/install/settings paths, не построчно; все editor actions, Java overloads и error paths не инвентаризованы |
| `ADB Lite/ADB_LITE_RU.md`, `ADB Lite/ADB_LITE_EN.md`, `ADB Lite/config.json`, `ADB Lite/adb_lite.plugin` | Обе версии руководства; TCP HTTP-like routing, pairing/token flow, mDNS discovery, saved-device preferences, auto-install, lifecycle и remote update/config paths | Implementation (4 451 строка) выборочно сверен по metadata, HTTP parser/routes, pairing/install, NSD/storage/lifecycle/update paths, не построчно; отдельный репозиторий Desktop companion здесь не изучен |

Полный манифест путей и SHA-256: [file-manifest.json](../../raw/vestr-plugins/file-manifest.json); pinned tree: [tree.json](../../raw/vestr-plugins/tree.json). Независимо прочитаны обе языковые версии руководств каждого плагина, оба README, все четыре config JSON и выбранные центральные участки трёх реализаций. Основные сценарии и contract-like детали из руководств сверены с указанными code paths, но большие реализации не прочитаны построчно. В полном tree нет отдельных build-файлов, CI workflow или тестовой suite; плагины, host client, Desktop companion и сетевой протокол не запускались, не собирались и не устанавливались.

Контекст радара этого source snapshot не содержит прямого упоминания `mr-Vestr/plugins` и описывает другие проекты; `radar-urls.json` пуст. Поэтому для данного репозитория нельзя сопоставить отдельную исходную формулировку радара или исторический commit.

## Подтверждённые технические факты

### Общая структура и metadata

Все три реализации наследуют `BasePlugin` и используют доступные в Android host Python модули и Java bridge. Примеры импортируют такие host API как `MenuItemData`, `HookResult`, `HookStrategy`, `MethodHook`, `ui.settings`, `client_utils`, `hook_utils`, `android_utils` и Telegram/ExteraGram Java-классы. Конкретный runtime contract этих импортов этим репозиторием не определяется; для него нужны документация SDK и совместимая сборка клиента.

В исходниках заданы стандартные поля плагинов (`__id__`, `__name__`, `__description__`, `__author__`, `__version__`, `__min_version__`, `__icon__`). Снимок фиксирует три самостоятельные metadata версии и два разных минимума клиента. Их нельзя сводить к одной общей версии репозитория.

### Templates

`TemplatesPlugin` сохраняет массив шаблонов через `get_setting`/`set_setting`; при создании объекта приводит отсутствующие поля `enabled`, `name`, `text` к значениям по умолчанию. В коде ограничение `TEMPLATE_COUNT = 30`. Запись формы `имя: текст` разделяется только по первому двоеточию; шаблон включён, если заданы и имя, и текст.

Руководство Templates описывает отправку из settings, командой и двумя chat menus; конфигурация `show_chat_menu`, `show_chat_plugins_menu`, `show_drawer_menu` и `settings_menu_button` управляет точками входа. Это документированный plugin workflow, а не независимое описание host menu API.

Отправка через команду в `on_send_message_hook(account, params)` использует настраиваемый prefix, по умолчанию `//`. При точном совпадении имени плагин заменяет `params.message`, сбрасывает/создаёт `params.entities`, конвертирует разметку в Telegram entities и возвращает `HookResult(MODIFY, params=...)`; пустая команда и префиксный поиск переводят пользователя в меню и отменяют исходную отправку. Суффиксное совпадение ищет имя без учёта регистра; частичные совпадения начинаются с prefix query.

Для прямой отправки в forum topic `_send_template_to_peer(..., topic_id, account)` формирует `message_data` с peer, текстом и entities; если topic найден, добавляет тот же topic message как `replyToMsg` и `replyToTopMsg`, затем вызывает `send_message(message_data)`. Источник доказывает этот call-site, но не гарантирует account routing, сетевую доставку или совместимость всех topic-типов.

Текстовая разметка перед `parse_markdown` заменяет `--...--` на italic-маркеры `_..._`, `~~...~~` на `~...~`, `**...**` на `*...*`; остальные виды форматирования зависят от host `markdown_utils.parse_markdown`. Синтаксис из README подтверждается для этих трёх случаев, но не является полной спецификацией парсера.

Импорт перехватывает `AndroidUtilities.openForView` с ожидаемой точной Java-сигнатурой; только имя расширения `.templates` ведёт к чтению UTF-8 JSON, отмене стандартного открытия (`setResult(False)`) и показу sheet импорта. Экспорт/импорт документирован как функция, а implementation path показывает лимит выбора до 30 элементов; полный JSON schema и все ошибки импорта в этой статье не специфицированы.

Оба `Templates` руководства (RU и EN) утверждают поддержку двух языков; корневые README утверждают 16. Pinned implementation содержит 17 записей `PLUGIN_LANG_CODES`, включая `system` и 16 locale codes. Это документальное расхождение с кодом снимка; наличие и полнота переведённых строк не проверялись.

Англоязычные руководства добавляют отдельные пользовательские/интеграционные детали: Templates предоставляет четыре documented send paths и описывает formatting markers; Plugin creator документирует configurable editor actions (send, share, save to Downloads, install) и toolbar/info-block controls; ADB Lite перечисляет auto-approve, auto-install, notification/language controls и последовательность сопряжения с Desktop companion. Это `docs`-утверждения, а не runtime-проверка; конкретные source-backed code paths выше имеют приоритет при расхождениях.

### Plugin creator

`PluginCreatorPlugin` metadata в этом снимке указывает минимум клиента `12.5.0`. Плагин принимает исходный текст из команды `.file` (настройка изменяема): `on_send_message_hook` берёт хвост после команды, при пустом хвосте открывает редактор/меню, а при непустом запускает `_send_plugin_file` и возвращает `HookResult(CANCEL)`, чтобы исходный текст команды не ушёл как сообщение.

Также имеется hook на Java `MessageSendPreview.setItemOptions(ItemOptions)`: когда включена настройка и поле ввода не пусто, long-press menu получает пункт отправки как файл. Выбор закрывает меню, очищает composer и передаёт сохранённый текст в `_send_plugin_file`. Это отражает текущую внутреннюю сигнатуру класса клиента и уязвимо к изменению UI-кода; SDK-контракт не заявлен.

`_send_plugin_file` UTF-8-кодирует текст во временный файл с настраиваемым именем, берёт активный `dialog_id`, рефлексией ищет `SendMessagesHelper.prepareSendingDocumentInternal` и готовит вызов с MIME `text/plain`; в соседних строках аргументы адаптируются к вариантам сигнатуры с `Uri` и типами массивов. Отдельные действия пишут `.plugin` в Downloads либо создают файл в cache и открывают штатный `PluginsController.showInstallDialog`. Код не проверялся в клиенте; отражённые сигнатуры могут отличаться между версиями.

Руководство Plugin creator документирует editor actions `Send to chat`, `Share file`, `Save to downloads`, `Install plugin`, настройки набора/вида toolbar controls, размера шрифта и показателей chars/lines/bytes. Это claims документации; обзор кода здесь подтверждает только file send, direct save и install call-sites, а не каждую UI-настройку.

### ADB Lite

Документация описывает передачу файлов с Desktop-компаньона по локальной Wi-Fi сети без root/ADB, pairing по mDNS, список доверенных устройств, auto-approve и optional auto-install. Implementation создаёт TCP listener на `0.0.0.0`; по умолчанию ищет свободный порт в диапазоне 1500–1520 и поднимает daemon accept loop с отдельным daemon handler на соединение.

Внутренний HTTP-like routing реализован вручную и обслуживает `GET /test`, `GET /`, `POST /connect`, `POST /check`, `POST /install`, `OPTIONS`; неизвестный метод/путь получает 405/404. В ответах добавляются `Access-Control-Allow-Origin: *` и разрешение заголовков `Content-Type`, `X-Filename`, `X-Device-Token`. Транспорт создаёт обычный `socket.SOCK_STREAM`; в описанном серверном пути нет TLS-слоя. Это статическое наблюдение, не полноценная проверка сетевой безопасности.

HTTP-like parser ждёт `CRLF CRLF` до 65 536 bytes, затем читает заявленный `Content-Length`; у соединения установлен socket timeout 10 секунд, а при нулевом/отсутствующем length путь пытается дочитать до закрытия с коротким timeout 0.5 секунды. В просмотренном parser path нет ветки `Transfer-Encoding`; поддержка chunked requests из снимка не следует. В этом кодовом пути не найден отдельный верхний предел тела после заголовков; это наблюдение исходника, не runtime security finding.

Pairing endpoint разбирает newline-delimited body с сигнатурой `adb_lite_s`, именем устройства, ОС, токеном, адресом ПК и строкой desktop-support. Токен используется для поиска сохранённого устройства на `/check` и `/install`; заблокированный или неизвестный токен отклоняется. В настройках можно подтверждать только ранее сохранённое устройство автоматически; новый pairing проходит UI confirmation, сохраняет token, имена, URL, время и ОС.

Для обнаружения сервер публикует Android NSD/DNS-SD сервис `_adblite._tcp` с версией, device/manufacturer/app и устройственным key; сервис снимается при остановке. В implementation default Elyx extensions — `.eaf`, `.elyx`, `.crul`; auto-install `.elyx`-ветки пробует ElyxEngine, обычной plugin-ветки — `PluginsController` validation/load callbacks. Если auto-install выключен, UI вызывает install dialog; это разделяет silent install и подтверждаемый host flow.

Saved devices хранятся JSON-строкой в Android `SharedPreferences`; загрузчик нормализует записи и мигрирует legacy setting `saved_devices`. Настройки состояния UI (`expanded_devices`) также читаются из preferences с fallback на legacy plugin setting. Жизненный цикл при загрузке поднимает сохранённый включённый сервер, а при unload снимает NSD service и останавливает server thread.

## Вызовы и hooks

| Модуль/класс | Объявление или call-site | Назначение | Lifecycle / поток / аккаунт | Ссылка на pinned исходник |
|---|---|---|---|---|
| `TemplatesPlugin(BasePlugin)` | `on_plugin_load()` / `on_plugin_unload()` | Регистрация message/input/document/UI hooks, обновления и меню; очистка delegate refs и ряда hook handles | Host plugin lifecycle; загрузка конфигурации запускается в daemon thread, UI переносится на UI thread; unload очищает перечисленные handles | [`Templates/templates.py`, L3096-L3164](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Templates/templates.py#L3096-L3164) |
| `TemplatesPlugin` | `on_send_message_hook(account, params) -> HookResult(...)` | Подмена исходящего текста/entities для шаблона, остановка отправки при поиске | Вызывается send-message hook host; callback принимает account, но routing по нему в данном методе не показан | [`Templates/templates.py`, L5476-L5545](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Templates/templates.py#L5476-L5545) |
| `TemplatesPlugin` | `_send_template_to_peer(dialog_id, template_text, topic_id=0, account=None)` → `send_message(message_data)` | Формирует peer/text/entities и опциональные topic reply references | UI/picker call path; account используется при поиске topic message, однако сам `send_message` получает только data dictionary | [`Templates/templates.py`, L5693-L5724](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Templates/templates.py#L5693-L5724) |
| `TemplatesPlugin` / `DocumentHandler(MethodHook)` | `AndroidUtilities.openForView(File, String, String, Activity, Theme.ResourcesProvider, boolean)` | Перехват `.templates`, чтение JSON и запуск sheet импорта | UI/view hook, при успешном распознавании подавляет штатное открытие; сигнатура подбирается по `repr(method)` | [`Templates/templates.py`, L3578-L3611](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Templates/templates.py#L3578-L3611) |
| `PluginCreatorPlugin(BasePlugin)` | `on_send_message_hook(account, params)` → `_send_plugin_file(code)` | Парсит configurable command и создаёт отправляемый файл из остатка сообщения | Send-message hook; callback берёт текущий fragment/dialog, тяжёлая UI работа переносится через `run_on_ui_thread`; account аргумент отдельно не маршрутизирует вызов | [`Plugin creator/plugin_creator.py`, L3386-L3429](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Plugin%20creator/plugin_creator.py#L3386-L3429) |
| `PluginCreatorPlugin` / `_SendMenuHook(MethodHook)` | `MessageSendPreview.setItemOptions(ItemOptions)` | Добавляет в long-press send preview действие «отправить как plugin» | UI hook; читает active chat input, чистит его и вызывает генератор file send; callback отражён из Java | [`Plugin creator/plugin_creator.py`, L3260-L3384](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Plugin%20creator/plugin_creator.py#L3260-L3384) |
| `PluginCreatorPlugin` | `_send_plugin_file(plugin_code, sheet=None)` → `SendMessagesHelper.prepareSendingDocumentInternal(...)` | Запись временного UTF-8 файла и вызов внутреннего document sender | Текущий chat и активный account instance; ищет Java overload reflection; совместимость зависит от host signature | [`Plugin creator/plugin_creator.py`, L3523-L3605](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Plugin%20creator/plugin_creator.py#L3523-L3605) |
| `PluginCreatorPlugin` | `_save_plugin_file_direct(...)` / `_install_plugin_file_direct(...)` | Сохранение в Downloads либо запуск штатного Install dialog из cache file | UI действий editor; install делегируется `PluginsController` | [`Plugin creator/plugin_creator.py`, L4803-L4837](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/Plugin%20creator/plugin_creator.py#L4803-L4837) |
| `ADBLiteServer` | `start()` → `_serve_loop()` → `_handle_client()` → `_process_request(method, path, ...)` | TCP accept, разбор HTTP-like request, dispatch routes и CORS responses | Daemon server thread и отдельный daemon thread для каждого клиента | [`ADB Lite/adb_lite.plugin`, L422-L586](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/ADB%20Lite/adb_lite.plugin#L422-L586) |
| `ADBLiteServer` | `_handle_connect`, `_handle_check`, `_handle_install` | Pairing handshake, token health check, file install request | Серверный handler thread ждёт UI confirmation/установочный callback; route принимает device token в теле или заголовке | [`ADB Lite/adb_lite.plugin`, L588-L658](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/ADB%20Lite/adb_lite.plugin#L588-L658) |
| `ADBLitePlugin` | `_register_nsd_service()` / `_unregister_nsd_service()` | Публикация и снятие `_adblite._tcp` с метаданными устройства | Android NSD lifecycle управляется плагином | [`ADB Lite/adb_lite.plugin`, L2130-L2187](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/ADB%20Lite/adb_lite.plugin#L2130-L2187) |
| `ADBLitePlugin` | `on_plugin_load()` / `on_plugin_unload()` | Восстановление устройств и enabled state; старт сервера и последующая остановка/NSD cleanup | Host plugin lifecycle; server start асинхронен | [`ADB Lite/adb_lite.plugin`, L2864-L2909](https://github.com/mr-Vestr/plugins/blob/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c/ADB%20Lite/adb_lite.plugin#L2864-L2909) |

## Ограничения и противоречия

- README называет все три проекта плагинами ExteraGram/AyuGram; конкретные compatibility claims — заявления автора, статические исходники и идентифицированные Java классы. Установка на обоих клиентах не проверялась.
- Языковое расхождение Templates описано один раз выше; обе подробные manuals говорят RU/EN, а code содержит 16 locale codes плюс `system`. Не установлены полнота перевода и фактическая доступность локализаций в runtime.
- Некоторые hooks выбирают внутренний Java overload по имени/`repr` или отражённым parameter types (`openForView`, `setItemOptions`, `prepareSendingDocumentInternal`, SettingsActivity). Это примеры точек вмешательства из одного снимка, не стабильный публичный API.
- ADB Lite guide говорит, что данные идут по Wi-Fi. Код показывает IPv4 socket, wildcard bind, открытые CORS headers и token-gated handlers; в этом server path не найден TLS. Реальные сетевые ограничения задаются окружением/роутером и в снимке не подтверждены.
- Templates и Plugin creator проверяют обновления по mutable `refs/heads/main` config JSON и затем скачивают URL из ответа; ADB Lite аналогично получает mutable update config. Эти ответы и загружаемые artifacts не являются частью pinned SHA и в этом обзоре не запрашивались.
- В Templates `_download_and_install_update()` содержит два последовательных запуска одного `download_thread`, тогда как Plugin creator и ADB Lite в соответствующих путях запускают по одному. Статически оба потока могут обращаться к одному update temp path и запускать reload; фактическую гонку без runtime проверки утверждать нельзя.
- Здесь нет build/tests/CI/runtime evidence, и standalone Desktop companion `mr-Vestr/adb-lite-desktop` не входит в покрытие. Подтверждения для Android client internals, thread affinity, HTTP interoperability, data migrations и install behavior требуют отдельной проверки.
