---
type: source
source_id: exteragram-utils
platform: Android
review_status: accepted-with-gaps
review: ../reviews/exteragram-utils.md
date: 2026-09-28
---

# exteragram-utils 0.1.3 — SDK stubs и CLI разработки

Источник: [релиз PyPI exteragram-utils 0.1.3](https://pypi.org/project/exteragram-utils/0.1.3/), опубликованный 2025-11-18. Архив wheel SHA-256 `6f245c56e0209538047cc03cf396328e3842dfe784f0744eea46755f918533fb`; PyPI JSON snapshot SHA-256 `8aa523ffc3f6018f6c35ff07849fe71f46064109b44c7cca76a732a278d98c24`. Sdist SHA-256 `28ecfccc03053b213d40855890995fb0046156e291f63e852affea0e8529eed4`. PyPI не сообщает лицензию, автора в metadata тоже нет. Пакет не устанавливался; исходники анализировались как данные. Никакие ADB-команды, сокеты к клиенту и плагины не запускались, тесты и сборка не выполнялись.

Роль источника — типовые объявления SDK для плагинов exteraGram плюс отдельный рабочий desktop CLI для загрузки файлов и отладки через ADB. Не считать SDK-facing `.py`-модули в wheel реализациями SDK: кроме `dev_client.py`, они состоят из сигнатур с `...` или package version literal; одноимённые `.pyi` в sdist также являются typing stubs. Полноценное приложение-кодовое тело в поставке есть у CLI `exteragram_utils/dev_client.py`; ни `markdown_utils.py`, ни `utils/metadata_parser.py` не реализуют парсеры — их функции тоже stubs. Остальные API ниже подтверждены только как заявленная форма интерфейса.

## Покрытие

| Материал | Что извлечено | Граница |
|---|---|---|
| Все 21 файла из `raw/exteragram-utils/files/` (16 Python files и 5 dist-info metadata files; пустые `__init__.py` также просмотрены) | полные объявления модулей, класс/метод/функции, stubs против тел, wheel metadata/RECORD/entry point | wheel — опубликованная версия 0.1.3; поведение Android-клиента и совместимость не запускались |
| `exteragram_utils/dev_client.py:1-557` | CLI, ADB forwarding, TCP/JSON протокол, pending requests, timeout, ping, metadata parser, мониторинг, загрузка и reload | реализован только клиентская сторона; серверный протокол и действия клиента exteraGram здесь не представлены |
| `markdown_utils.py:1-34` | типы Markdown entities и сигнатура parse_markdown | весь модуль декларативный; `parse_markdown` и `to_tlrpc_object` — заглушки |
| `base_plugin.py`, `client_utils.py`, `dev_server.py`, `android_utils.py`, `file_utils.py`, `hook_utils.py`, `plugin_settings.py`, `ui/*.py`, `utils/metadata_parser.py` | публичные сигнатуры и ожидаемые Java/Android типы | тела — `...`, поэтому алгоритмы, ошибки, lifecycle и фактические вызовы не подтверждаются |
| Sdist `exteragram_utils-0.1.3.tar.gz` | README, `pyproject.toml`, `setup.py`, `MANIFEST.in`, дублирование `typings/*.pyi` и `py_stubs/*.py` | SHA-256 сверена с PyPI JSON; список членов tar проверен без извлечения, абсолютных и `..` путей нет; setup/build/install не запускались |
| `METADATA`, `entry_points.txt`, `WHEEL`, `top_level.txt`, `RECORD` | версия, зависимости, Python floor, console script, верхнеуровневые модули и содержимое wheel | PyPI metadata не задаёт license/homepage/docs URL; SDK/client version отсутствует |

## Установленные факты

### Как пакет распространяется

PyPI metadata фиксирует `Requires-Python: >=3.8`, зависимости `watchdog`, `aiofiles`, `black`, `beautifulsoup4`, `lxml`, `pillow`, `requests`, `pyyaml` с указанными в METADATA минимальными версиями. Единственный console entry point — `extera = exteragram_utils.dev_client:main`. README описывает запуск `extera [plugin_files...]`, а импорт типов напрямую (`from base_plugin import BasePlugin`, `from ui.settings import Switch`), без префикса `exteragram_utils`. `pyproject.toml` включает пакет `exteragram_utils*` и package-data `*.pyi`; `setup.py` копирует `.pyi` в дерево `py_stubs/*.py` и при установке копирует их в корень install library. Это объясняет несоответствие между namespace исполняемого CLI и root-level namespace type stubs. Наличие typing-пути не доказывает импортируемую Android-реализацию этих модулей вне runtime клиента.

### Совместимость заявленного Python floor

`METADATA` и `pyproject.toml` объявляют `>=3.8`, но SDK stub modules используют аннотации `str | None`/`list[str]` без `from __future__ import annotations`. Статически это означает, что такие модули не импортируются на Python 3.8; PEP 604 union syntax требует Python 3.10+. Это касается SDK declarations, а не обязательно `exteragram_utils.dev_client`, чей код пользуется `typing`-формами. Официальная документация SDK отдельно указывает plugin runtime Python 3.11 ([сводка совместимости](../compatibility.md)); это контекст запуска плагина, но не отменяет несовпадение заявленного wheel floor с синтаксисом root-level stubs. Совместимость не запускалась.

### Реализованный development client

`AdbManager` вызывает установленную снаружи команду `adb` через `subprocess.run`, с `check=True`, захватом stdout/stderr и текстовым режимом. `setup_device()` запускает ADB server, выполняет `wait-for-device`, затем делает `adb forward tcp:42690 tcp:42690`; при `--debug` добавляет `tcp:5678`. Здесь нет перебора `adb devices`, выбора serial или подтверждения конкретного устройства. `run_command()` ловит только `CalledProcessError`, но не ошибку отсутствующего `adb`; `start_server()` и `wait_for_device()` игнорируют возвращаемые ошибки, а subprocess и `wait-for-device` не имеют timeout. Метод `reverse_port()` реализован, но `setup_device()` его не вызывает.

`DeviceConnection` по умолчанию подключается к `127.0.0.1:42690`, ждёт повторно бесконечно с `retry_delay=2`, и использует TCP socket с `settimeout(1.0)` для чтения. Это относится к начальному connect при `running=True`; общий `disconnect()` навсегда устанавливает `running=False` для данного объекта. Отдельный daemon thread читает блоки до 4096 байт. JSON разбирается через `JSONDecoder.raw_decode`, поддерживаются несколько соседних JSON-объектов и сохранение хвоста после `JSONDecodeError`. Reader декодирует каждый TCP chunk через UTF-8 `errors="replace"`; разделение многобайтового символа между `recv` может повредить текст. Некорректный остаток сохраняется без лимита/recovery, поэтому source не доказывает устойчивый framing на произвольном повреждённом потоке. Запрос имеет поля `@` (action), `#` (монотонный integer ID), затем поля arguments; request сериализуется в UTF-8 и отправляется `sendall()` без явного разделителя. Ответ связывается по `#` с `PendingRequest` из словаря под `Lock`, а `Event.wait()` ждёт `response_timeout=30`. Timeout удаляет ID и возвращает `None`; disconnect помечает все pending как `Connection closed`, сигналит их Event и очищает словарь.

Keepalive использует `ping` каждые 10 секунд в daemon thread. `get_plugins()` удаляет поле `#` из полученного объекта; действия `write_plugin(plugin_id, content)`, `reload_plugin(plugin_id)`, `start_debugger(...)`, `stop_debugger(...)` отправляются тем же JSON RPC. В этом client code нет `enable_plugin`, `disable_plugin`, `remove_plugin` или Elyx actions, которые перечислены в документации SDK; версия server-side протокола не указана, поэтому совместимость списка команд неизвестна. При исключении отправки код удаляет текущий request и вызывает `disconnect()`, которая устанавливает `running=False`. Поэтому следующий `connect()` не входит в `while self.running`, и повторной отправки фактически не происходит. Есть и отдельный сбой восстановления: если server EOF завершил reader loop, `running` остаётся true, но `response_thread` может ещё считаться живым, поэтому `connect()` не создаёт нового reader; запросы после восстановления сокета могут ждать timeout. Это выводы из статического контроля потока, runtime-поведение не проверялось.

Флаг CLI называется `--debug`, но help говорит “Enable PyCharm debugger”, тогда как клиент при `debug_enabled` отправляет `platform: "vscode"`. Это внутреннее несоответствие опубликованной реализации. Сопутствующий `dev_server.py` описывает `DebuggerPlatform.PyCharm/VSCode` и start/stop remote debugging, однако весь этот модуль — stubs и не даёт реализации сервера или подтверждения поддержки любой из платформ.

### Загрузка и мониторинг файлов

`parse_metadata(content)` разбирает AST только верхнеуровневые `Assign`, берёт присваивания строковым `ast.Constant` dunder-полям и требует непустые `__id__` и `__name__`; остальные поля могут остаться `None`. Он не исполняет файл. `FileMonitor.add_files()` пропускает отсутствующие файлы и исходники без допустимого id, сохраняет `(mtime, PluginMetadata)` и сразу загружает содержимое.

Загрузка выполняется через `write_plugin`, затем ждёт 0,3 секунды и вызывает `reload_plugin`; успешность операции сводится к наличию любого ответа, а прикладное поле success не проверяется. Мониторинг раз в секунду сравнивает `mtime`, повторно парсит файл и загружает изменившийся файл. При изменённом файле с некорректным metadata он обновляет сохранённый mtime и не повторит попытку, пока файл снова не поменяется. Удалённый файл только логируется и остаётся в таблице наблюдения; удаление плагина/отписка не реализованы.

CLI принимает один или более positional `files`, `--debug`, `--log-level` с DEBUG/INFO/WARNING/ERROR/CRITICAL (default INFO). Перед ADB выбирает существующие файлы, но затем передаёт `args.files`, а не `valid_files`, в `add_files`. Обработчик KeyboardInterrupt останавливает debugger и соединение из `start_monitoring()`.

### SDK surface: объявления, не исполнение

`base_plugin.py` определяет описания `PluginMetadata`, `HookStrategy` (CANCEL/MODIFY/DEFAULT/MODIFY_FINAL), `HookResult`, `PluginError`, `AppEvent`, `MenuItemType`, `MenuItemData`, `HookFilterData`, `HookFilter`, `hook_filters()` и `BasePlugin`. Заявлены plugin lifecycle (`on_plugin_load/unload`, `on_app_event`), pre/post request, single/multiple update, send-message callbacks; Xposed-style method/constructor hooks; setting import/export и menu item add/remove. Все тела — заглушки; фактическая схема Java bridge, приоритетов, return semantics и очистки hooks из wheel неизвестна.

`client_utils.py` объявляет очереди клиента (`STAGE_QUEUE`, `GLOBAL_QUEUE`, `CACHE_CLEAR_QUEUE`, `SEARCH_QUEUE`, `PHONE_BOOK_QUEUE`, `THEME_QUEUE`, `EXTERNAL_NETWORK_QUEUE`, `PLUGINS_QUEUE`), `run_on_queue(fn, queue_name, delay)`, callback и `send_request(request, fn)`, getters контроллеров/хранилищ текущего клиента, send helpers (`send_message`, `send_text`, photo/document/video/audio) и `edit_message`. Это список заявленных helpers, не гарантия параметров или конкретного аккаунтного маршрута: bodies отсутствуют.

`android_utils.py` объявляет `OnClickListener`, `OnLongClickListener`, `run_on_ui_thread(func, delay)`, `log`, `copy_to_clipboard`, `R`; реализации Android thread dispatch/listeners не включены. `hook_utils.py` заявляет class lookup и чтение/запись instance/static private fields через Java reflection, но их поведение не задано. `file_utils.py` объявляет plugin/cache/files/image/video/audio/document paths и read/write/delete/ensure/list directory helpers. `plugin_settings.py` объявляет init и get/set/clear/all settings с передачей пути plugin dir и `all_shared_prefs`; реализация отсутствует.

`ui.settings` предоставляет только схемы dataclass-пунктов `Switch`, `Selector`, `Input`, `Text`, `Header`, `Divider`, `EditText` с ключами, значениями по умолчанию, callback-ами, иконкой/subtext, long-click и alias полями. `ui.alert.AlertDialogBuilder` описывает fluent builder с title/message/buttons/items/custom View, dismiss/cancel, image/drawable/animation, dim/blur, `create/show/dismiss` и доступом к dialog/button/progress. `ui.bulletin.BulletinHelper` заявляет info/error/success/simple/two-line/button/undo и системные уведомления о копировании/сохранении. Все реализации UI отсутствуют.

### SDK parsing helpers — только объявления

`markdown_utils.py` экспортирует только имя `parse_markdown`; enum типов Telegram entities (code, pre, strikethrough, text link, bold, italic, underline, spoiler, custom emoji) и dataclass-схемы `RawEntity(type, offset, length, language, url, document_id)` / `ParsedMessage(text, entities)` являются декларациями. И `parse_markdown(markdown)`, и `RawEntity.to_tlrpc_object()` имеют тело `...`. `utils/metadata_parser.py:get_metadata(file_path)` также только заглушка. Нельзя приписывать этим модулям алгоритм обработки Markdown или metadata.

`utils/metadata_parser.py:get_metadata(file_path)` — только объявление с `...`; нельзя отождествлять его с реализованной в dev client функцией `parse_metadata(content)`.

## Таблица интерфейсов и вызовов

| Модуль/класс | Сигнатуры или call-site | Назначение и lifecycle/thread/account | Доказательство |
|---|---|---|---|
| `exteragram_utils.dev_client:main` | `main()`; console script `extera` | desktop development CLI; ADB и долгоживущий мониторинг | [PyPI release](https://pypi.org/project/exteragram-utils/0.1.3/), `files/exteragram_utils/dev_client.py:501-557`, `dist-info/entry_points.txt` |
| `AdbManager` | `setup_device(debug_mode=False)`, `forward_port(local,remote)`, `reverse_port(local,remote)` | ADB server/device wait и host→device forwarding; reverse объявлен, но не используется | тот же релиз, `dev_client.py:36-86` |
| `DeviceConnection` | `connect()`, `disconnect()`, `send_message(action, arguments=None)`, `get_plugins()`, `write_plugin(plugin_id,content)`, `reload_plugin(plugin_id)`, `setup_debugger()`, `stop_debugger()` | TCP клиент на host:42690, concurrent response/ping threads, ID-correlated JSON RPC; account/device selection нет | тот же релиз, `dev_client.py:88-348` |
| `PendingRequest` | `request_id`, `action`, `event`, `response=None`, `error=None` | межпоточная корреляция request/response | тот же релиз, `dev_client.py:27-34`, `205-241` |
| `FileMonitor` | `add_files(filenames)`, `_check_for_changes()`, `start_monitoring()` | polling по mtime и write/reload plugin; shutdown на KeyboardInterrupt | тот же релиз, `dev_client.py:393-499` |
| `parse_metadata` | `parse_metadata(content) -> Optional[PluginMetadata]` | безопасный AST scan plugin metadata; обязательные `__id__`, `__name__` | тот же релиз, `dev_client.py:351-391` |
| `BasePlugin` | lifecycle/hooks/settings/menu signatures в `base_plugin.py:123-157` | заявленная plugin API surface, тела отсутствуют | тот же релиз, `files/base_plugin.py:12-157` |
| `HookFilter` / `HookFilterData` | фильтры результата/аргумента, `Condition`, `Or`, `to_java_filter` | заявленная сборка hook predicates, тело отсутствует | тот же релиз, `files/base_plugin.py:78-121` |
| `client_utils` | `run_on_queue`, `send_request`, controller getters, send/edit helpers | заявленные клиентские очереди и Telegram helpers; threading/account semantics не видны | тот же релиз, `files/client_utils.py:9-53` |
| `markdown_utils` | `parse_markdown(markdown) -> ParsedMessage`; `RawEntity.to_tlrpc_object()` | типы и сигнатуры объявлены, обе функции — заглушки | тот же релиз, `files/markdown_utils.py:4-34` |
| `android_utils`, `hook_utils`, `file_utils`, `plugin_settings` | сигнатуры в соответствующих root modules | Android dispatch/reflection/files/preferences declarations only | тот же релиз, соответствующие файлы `files/*.py` |
| `ui.settings`, `ui.alert`, `ui.bulletin` | settings row dataclasses, `AlertDialogBuilder`, `BulletinHelper` | описания UI API; callback thread и fragment lifecycle не реализованы в пакете | тот же релиз, `files/ui/*.py` |
| `DebuggerEventListener`, `DevServer` | `start_server`, `stop_server`, `setup_remote_debugging`, `stop_remote_debugging` | ожидаемый debug server API только в stub | тот же релиз, `files/dev_server.py:8-40` |

## Практические выводы и пределы

- Заявка на `>=3.8` расходится с синтаксисом аннотаций SDK stubs (PEP 604 `|` требует 3.10; `list[...]` — 3.9). Для downstream проектов, где package floor практически важен, отдельно ограничивать версию для типовых imports; это статический вывод, не runtime-проверка.

- Для локальной разработки пакет показывает протокол-клиентский workflow: обеспечить ADB port forward, читать plugin literal metadata без выполнения исходника, затем передавать `write_plugin` и `reload_plugin`. Это рецепт, извлечённый из desktop CLI; необходимую серверную реализацию на устройстве нужно брать из другого источника.
- Pending requests требуют reader thread отдельно от синхронного caller: иначе caller, ожидающий Event, не сможет получить ответ. Из кода видны общий lock, response buffer lock и конечный timeout; при этом reconnect lifecycle имеет статически видимые дефекты, перечисленные выше.
- Нет версии SDK в metadata и нет minimum-client version. `PluginMetadata.min_version` — только поле модели; это не сообщает, какая версия exteraGram API реализует объявленные методы.
- `base_plugin.py` импортирует Java/Xposed/ExteraGram-типы и поэтому сами declarations нацелены на среду с Chaquopy/Java interop в Android app; package metadata `py3-none-any` отражает переносимость архива, но не делает stub APIs реализованными на desktop.
- `setup.py` содержит custom install/develop копирование, но wheel уже содержит root-level stub-модули; анализ не устанавливал пакет и не проверял фактическое поведение pip installer.
- Открытые пробелы: отсутствуют runtime-реализации большинства SDK-модулей, серверная часть JSON протокола, серверный `dev_server`, Android client version mapping, фактические классы/сигнатуры SDK, UI/main thread и account semantics, тесты и runtime/device verification. Пакет не содержит релевантных тестов. PyPI и sdist не публикуют лицензию, репозиторий URL, homepage или документацию. README описывает `extera [plugin_files...]` и прямые imports; это docs, не доказательство работоспособности installation workflow.

Все утверждения о доступных SDK методах на этой странице имеют статус объявления из кода/stub, а не `runtime-verified`. Единственная существенная исполняемая реализация, установленная статически, — development CLI; вспомогательные SDK-модули в поставке — заглушки.
