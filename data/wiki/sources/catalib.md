---
type: source
source_id: catalib
platform: tool / Android (Chaquopy plugin runtime)
review_status: accepted-with-gaps
review: ../reviews/catalib.md
date: 2026-09-27
---

# catalib — модульная разработка exteraGram-плагинов с однофайловой сборкой

- Репозиторий: [cataIystdev/catalib](https://github.com/cataIystdev/catalib), снимок `5c9871245d77494f33b7e81b1050d29478dcbaa8` (ветка `main`, получен 2026-09-27).
- Лицензия: MIT. PyPI-пакет в `pyproject.toml` — `catalib` 0.3.3; минимальная версия среды инструмента — Python 3.11.
- Роль: отдельный инструмент сборки и runtime-загрузчик для разработки exteraGram-плагина из дерева Python-модулей и выпуска единственного файла, который принимает штатный загрузчик приложения. Это не API самого клиента и не замена SDK.
- Состояние проекта требует оговорки: в README написано, что поддержка прекращена в связи с ElyxCore; метаданные репозитория в полученном snapshot сообщают `archived: true`. При этом код и книга описывают завершённую реализацию 0.3.3 и не содержат миграционного перехода на ElyxCore. Реализованные возможности ниже — описание снимка, а не рекомендация начинать новый проект на неподдерживаемом инструменте.

## Покрытие и источники

Проверены README, `pyproject.toml`, changelog, относящиеся к сборке и разработке главы книги (`getting-started`, `guide`, `cli`, `deployment`, `internals`, `reference`, troubleshooting), архитектурные решения и component docs, а также implementation-код и целевые тесты перечисленных ниже областей. Примеры и contributing-документы не проходили построчную проверку. Чтение исходников и тестов было статическим; тесты/чужие команды не запускались.

| Область | Что прочитано | Результат и границы |
|---|---|---|
| Модель сборки и импорты | `book/guide/project-structure.md`, `book/internals/how-it-works.md`, `docs/architecture/decisions/ADR-0002-bundler-meta-path.md`, `src/catalib/bundler/{discovery,model,compiler,sourcemap}.py`, `src/catalib/runtime/bootstrap.py`, `tests/unit/bundler/`, `tests/unit/runtime/test_bootstrap.py`, `tests/integration/test_bundle_roundtrip.py` | Сверены реализация и целевые тестовые случаи от `src/` до встроенных модулей, импортов, перезагрузки и traceback; тесты не запускались. |
| Каталог SDK внутрь bundle | `src/catalib/bundler/{vendor,treeshake}.py`, `book/guide/manifest.md`, `book/troubleshooting.md`, ADR-0008, тесты `tests/unit/bundler/test_treeshake.py` | Разобраны AST-анализ, транзитивный граф, fallback и динамические импорты. |
| CLI, манифест и recipe | `book/getting-started/quickstart.md`, `book/cli/build.md`, `src/catalib/cli/{app,build_command,_pipeline}.py`, `src/catalib/manifest/{loader,model}.py` | Проверены фактические флаги и назначение двух файлов результата. |
| Зависимости / версии | `pyproject.toml`, `src/catalib/bundler/requirements.py`, `book/guide/dependencies.md`, `docs/architecture/overview.md`, ADR-0011 | Python 3.11+, целевой Chaquopy 3.11; поддерживаются объявленные pure-Python wheels, но совместимость каждой внешней библиотеки отдельно не тестируется. |
| Тестовая база / устройство | `tests/integration/test_bundle_roundtrip.py`, `tests/unit/runtime/test_bootstrap.py`, `docs/architecture/evidence/T-011-probe-result.json` | В репозитории описан отдельный тестовый roundtrip и записан результат пробника на Chaquopy 3.11.10; данное исследование runtime не повторяло. |
| CI и качество выпуска | `pyproject.toml`, `book/contributing/publishing.md`, дерево snapshot, GitHub status/check-runs API для exact SHA | В дереве нет workflow CI; live commit status имеет два успешных GitBook context и check-runs API возвращает 0. Это не подтверждает build/test CI. |
| Support SDK и plugin lifecycle | `book/reference/api.md`, `book/guide/{hooks,settings,plugin-class,sdk-access}.md`, `docs/components/support.md`, ADR-0003/0006/0007, `src/catalib/support/`, tests `test_public_api.py`, `test_plugin.py`, `test_xposed.py` | Проверен фасад `catalib.support`, декларативная регистрация хуков/меню/Xposed и основные группы SDK helper API. Полный паритет заявлен авторами; он не перепроверялся против каждой версии официального SDK. |
| Локальная разработка и отладка | `book/cli/*.md`, `book/guide/testing.md`, `book/deployment/*.md`, `docs/guides/device-workflow.md`, `src/catalib/{watching,diagnostics,devicelogs,testing}.py`, `src/catalib/deploy/`, соответствующие unit tests | Проверены scaffold, watcher fallback, preflight, device logs, dev-server deploy protocol и host-side plugin harness. Запуски команд/тестов не выполнялись. |
| Assets, wheels и obfuscation | README, книга, манифест, bundler и доступные планы/ADR | Bundler читает только `*.py` под `src/`; отдельного копирования assets или обфускации в CLI/манифесте не найдено. Это граница изученного snapshot, не утверждение обо всех внешних инструментах. |

## Как получается один самодостаточный файл

`catalib.toml` задаёт идентификатор, метаданные и `[build] src/entry/out/vendor`. По умолчанию `src` — входное дерево; каждый `*.py` включается в bundle, а не только импортируемые модули плагина. `discovery` преобразует `src/pkg/sub.py` в имя `<plugin_id>.pkg.sub`, а `src/pkg/__init__.py` — в пакет. `src/__init__.py` необязателен и, если присутствует, становится телом верхнего модуля. Скрытые каталоги и `__pycache__` пропускаются; каталог с модулями без `__init__.py`, отсутствующая entry-точка, пустой `src` и symlink/path traversal завершают сборку ошибкой.

Компилятор формирует последовательность из строковых литералов метаданных, необязательного `__requirements__`, полного исходника встроенного загрузчика, словаря `_CATALIB_SOURCES` и вызова `catalib_install(plugin_id, globals(), ..., entry)`. Исходники не сплющиваются в одно пространство имён: они сохраняют отдельные module/package identity и исполняются при первом импорте. Основной результат — `dist/<id>.py`; рядом записывается побайтно идентичный `<id>.plugin` для установки. Оба — один и тот же текстовый Python bundle, а не исполняемый бинарный архив.

Загрузчик добавляет finder в начало `sys.meta_path`. Для каждого полного имени в таблице finder возвращает import spec, а loader компилирует сохранённый исходник с исходным origin. Верхний модуль временно сделан пакетом (`__package__`, `__path__`, согласованный `__spec__`), поэтому работают относительные импорты и абсолютные импорты через `<plugin_id>.*`. Имя модуля плагина уникально для его внутренних модулей. При активации удаляются старые finder и `sys.modules`-подмодули этого плагина, а также помеченные/с синтетическим origin старые вендоренные `catalib.*`; настоящий установленный `catalib` с файловым origin не удаляется.

После загрузки entry-модуля загрузчик ищет определённый именно в нём подкласс SDK `BasePlugin` (либо class hierarchy с `BasePlugin`/`CatalibPlugin` при отсутствии SDK) и поднимает класс в namespace верхнего файла, чтобы движок exteraGram мог его обнаружить. Поэтому `entry` должен указывать на модуль с классом плагина. В документации рекомендуют ровно один такой класс.

`linecache` получает исходный текст по origin вида `<plugin_id>/pkg/sub.py`; код компилируется с тем же origin. Документированный результат — traceback со строкой и именем исходного файла, хотя физические файлы после сборки не нужны.

## Импорты, динамика и циклы

- Внутри проекта можно сохранять обычные relative imports, например `from .core.parser import parse`, `from . import config`. Абсолютные `import <plugin_id>...` тоже представлены в таблице. Условие — запуск цельного bundle с активированным загрузчиком; книга предупреждает, что копирование/исполнение модулей по частям теряет настроенную package-среду.
- Все файлы плагина включаются в таблицу вне зависимости от статических связей, поэтому механизм `vendor="auto"` **не удаляет** неиспользуемые модули самого плагина. В том числе строковый `importlib.import_module(f"{__name__}.feature")` может обратиться к модулю плагина, если он включён и имя вычислено в корректное полное имя. Пример с таким динамическим импортом отдельно не закреплён тестом; это вывод из статической таблицы и finder.
- `vendor="auto"` относится только к вендоренным модулям `catalib`, которые нужны потому, что на устройстве пакет catalib не установлен. AST-анализ видит обычные `import`/`from ... import ...`, включая импорты внутри функций; строит транзитивное замыкание и генерирует уменьшенный `catalib.support.__init__`. Он не интерпретирует `importlib.import_module`, `__import__` и строковые имена. Если такие динамические обращения касаются `catalib.support`, задать `[build] vendor = "full"` либо добавить явный импорт. Для неоднозначных форм (пакет как объект, `import *`, неизвестный ре-экспорт, импорт `catalib` вне support, синтаксическая ошибка) реализация тоже выбирает полный vendor и печатает причину.
- Tree-shaking — только по модулям catalib, не по отдельным символам и не по модулям плагина. Вырезание функций/классов отвергнуто авторами как ненадёжное при рефлексии, proxy и динамических обращениях.
- Циклические импорты модулей плагина не названы отдельной поддерживаемой возможностью и тестами не покрыты. Реализация делегирует разрешение импорта стандартному `importlib`/`sys.modules` и исполняет каждый модуль при запросе. Следовательно, циклы должны подчиняться обычной семантике Python с частично инициализированными модулями: чтение ещё не присвоенного атрибута может завершиться ошибкой. Это вывод по реализации, а не установленное ограничение catalib или runtime-проверка.
- Namespace packages не поддерживаются discovery: любой подкаталог `src`, содержащий `.py`, обязан иметь `__init__.py`.

## SDK facade и lifecycle плагина

В snapshot есть не только инструмент сборки, но и вендорируемый facade `catalib.support`. Он реэкспортирует базовые `CatalibPlugin`, hook/menu/settings/Xposed API и тематические модули для Android utilities, client queues/requests/controllers, файлов, reflection, форматирования, dialogs, bulletins, Java class proxy и FQN-констант. ADR-0007 описывает цель как паритет с публичным SDK; это позиция документации проекта, а совместимость каждой сигнатуры с каждой сборкой ExteraGram отдельно здесь не проверялась. Вне Android SDK слой использует функциональные stubs для offline работы. [API reference](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/reference/api.md#L74-L110), [support exports](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/support/__init__.py#L10-L84), [ADR-0007](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/docs/architecture/decisions/ADR-0007-polnyj-paritet-sdk.md#L22-L54).

`CatalibPlugin.on_plugin_load()` регистрирует декорированные handlers, menu items и Xposed hooks, затем вызывает `on_load()`. `on_plugin_unload()` снимает зарегистрированные Xposed hooks и вызывает `on_unload()`. Поддерживаются исходящие сообщения, request lifecycle (`pre_request`/`post_request`), update callbacks (`on_update`/`on_updates`), app events и menu handlers; callbacks request/update получают account id. Обработчик phase hook может фильтровать имя точным сравнением или подстрокой. Декоратор `@xposed` включает целевой Java class/method, фазу и фильтры; ошибки разрешения/регистрации отражаются в логах и не должны обрушать загрузку по реализации. [Hooks](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/guide/hooks.md#L31-L106), [plugin implementation](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/support/plugin.py#L168-L286), [Xposed implementation](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/support/xposed.py#L60-L205).

Настройки строятся как `SettingItem` декларативными фабриками (`header`, `divider`, `switch`, `selector`, `text_input`, `edit_text`, `text`, `custom`); опциональные параметры callbacks/icon/link и поведения UI добавлены keyword-only для совместимости. `CatalibPlugin.settings()` возвращает эти элементы, `get_setting`/`set_setting` работают с настройками SDK. `catalib.support.files` оборачивает plugin/cache/files/images/video/audio/document directories и file helpers; `client` — очереди, отправку запросов/сообщений и controller getters. Это конкретные integration points, а не отдельный runtime SDK клиента. [Settings API](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/reference/api.md#L56-L89), [SDK access guide](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/guide/sdk-access.md#L58-L96).

## Локальные workflow, диагностика и деплой

`catalib init` генерирует `hook` (default), `minimal`, `menu` или `settings` шаблон с `catalib.toml`, пакетным `src` и offline tests; непустая целевая директория отклоняется. `catalib.testing.PluginHarness` помогает host-side тестировать message hooks и menu handlers на offline stubs, включая начальные settings и logs. Эти tests не заменяют проверку в приложении. [init](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/cli/init.md#L1-L94), [testing helper](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/testing.py#L24-L142).

`catalib watch` пересобирает при изменении `src` или манифеста. При наличии использует `watchfiles`, иначе применяет stdlib polling (по умолчанию 1 секунда). `catalib doctor` сообщает о Python, среде, манифесте и deploy prerequisites; старый Python/битый manifest дают fail, отсутствие adb/device/dev server обычно warn. `catalib logs` читает logcat, обычно фильтруя по `plugin_id`; на Android доступ к чужим логам ExteraGram может требовать `READ_LOGS`/root/Shizuku/adb grant, а в некоторых сборках plugin logs вообще не попадают в logcat. [watch](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/cli/watch.md#L1-L64), [doctor](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/cli/doctor.md#L1-L64), [logs](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/cli/logs.md#L1-L84).

Доставка идет через встроенный JSON/TCP dev server exteraGram: `ping`, `write_plugin`, `reload_plugin`, `set_plugin_enabled`; напрямую `adb push` в приватную папку не работает без root. На ПК используется `adb forward`, Termux/Pydroid подключаются к localhost напрямую. Реализация `deploy_plugin(..., enable=True)` вызывает `set_plugin_enabled(true)` на каждом обычном deploy, хотя некоторые docs описывают это как действие первого деплоя; в T-081 отдельно сообщается, что на одном app build UI экрана plugins требовался, чтобы команда включения вступила в силу. `get_plugins.error == null` — записанный проектом критерий успешного импорта, а не проверка, выполненная этим review. [deploy implementation](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/deploy/reload.py#L40-L92), [device workflow record](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/docs/guides/device-workflow.md#L17-L55).

## Зависимости, ресурсы и ограничения сборки

Зависимости плагина объявляются `requirements = [...]` в `[plugin]` и/или литеральным `__requirements__ = [...]` в каждом исходном модуле. Слияние идёт в порядке: сначала манифест, затем модули в порядке обнаружения; точные дубликаты удаляются. Пустая строка и известные пакеты с бинарными расширениями отклоняются. Список blocklist: `numpy`, `pandas`, `scipy`, `cryptography`, `opencv-python`, `opencv-python-headless`, `opencv-contrib-python` (нормализация имён по PEP 503). Документация утверждает, что exteraGram устанавливает универсальные pure-Python wheels. Это не автоматическая проверка всего PyPI: незанесённый бинарный пакет может пройти локальную проверку, но не стать совместимым.

Репозиторий не описывает в bundler механизм вшивания произвольных файлов/asset data: discovery перебирает `*.py` под `src`, compiler сериализует исходники модулей и source origins. Отдельного `assets` поля или опции обфускации в известном build CLI/манифесте нет. Поэтому считать bundle упаковщиком ресурсов или обфускатором нельзя; внешняя доставка файлов и защита исходников этим snapshot не решены.

## Версии и статус поддержки

- Для запуска инструмента метаданные PyPI-проекта задают `requires-python = ">=3.11"`; classifiers заявляют Python 3.11, 3.12, 3.13. Зависимость runtime code boundary — stdlib и SDK, без Typer/watchfiles; это позволяет не переносить CLI-зависимости внутрь плагина.
- Документы по приложению описывают целевую встроенную среду как Chaquopy CPython 3.11. В `T-011-probe-result.json` записан эксперимент на устройстве с Chaquopy Python 3.11.10: собственный finder, synthetic package и relative import сработали, traceback указывает на синтетический origin; ошибок пробника нет. Это конкретное документированное подтверждение 3.11.10, не гарантия для каждой версии exteraGram/Chaquopy или для Python 3.12/3.13 на устройстве.
- В project `0.3.3` — версия самого catalib, не минимальная версия exteraGram или SDK. `plugin.min_version` экспортируется как `__app_version__`, `sdk_version` — как `__sdk_version__`; второй является жёстким ограничением установки. Это иная семантика, чем Python compatibility.
- README объявляет прекращение поддержки; API snapshot репозитория также помечает репозиторий archived. При этом pyproject/changelog/book описывают последнюю версию 0.3.3 и не предлагают официальную альтернативу или план миграции на ElyxCore. Не трактовать код как поддерживаемую интеграцию ElyxCore.

## Методы, вызовы и команды

| Модуль / вызов | Назначение и важные условия | Источник |
|---|---|---|
| `catalib build [--project DIR] [--check]` | Собрать из `catalib.toml`; `--check` проходит тот же pipeline без записи. CLI `build()` использует `build_bundle(project.resolve(), write=not check)`. | [CLI build](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/book/cli/build.md#L1-L25), [build_command.py](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/cli/build_command.py#L13-L49) |
| `discover_sources(src_dir: Path, entry: str) -> SourceTree` | Собрать детерминированное дерево модулей, проверить entry, `__init__.py`, скрытые каталоги и traversal. | [discovery.py](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/bundler/discovery.py#L34-L94) |
| `merge_requirements(manifest_requirements, modules)` | Слить PEP 508 strings из манифеста и `__requirements__`, отклонить пустые и blocklist binary deps. | [requirements.py](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/bundler/requirements.py#L44-L83) |
| `plan_vendor(tree, mode="auto")` | Включить транзитивно требуемые модули `catalib`; `full` включает весь набор, `auto` анализирует статические импорты. | [treeshake.py](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/bundler/treeshake.py#L218-L319) |
| `compile_plugin(manifest, tree) -> BundleResult` | Вставить метаданные, bootstrap, module source table и vendor; проверяет синтаксис результата и AST метаданных. | [compiler.py](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/bundler/compiler.py#L86-L131) |
| `_CatalibFinder.find_spec(fullname, path=None, target=None)` / `_CatalibLoader.exec_module(module)` | Вернуть spec для модуля из таблицы и исполнить встроенный текст с origin/linecache. Приватные детали сгенерированного runtime. | [bootstrap.py](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/runtime/bootstrap.py#L24-L69) |
| `catalib_install(module_name, module_globals, sources, entry_fullname)` | Установить finder, очистить состояние reload, восстановить пакетную идентичность, исполнить корень, импортировать entry и поднять класс плагина в верхний namespace. | [bootstrap.py](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/runtime/bootstrap.py#L108-L176) |

## Практические recipes

**Обычная однофайловая сборка:**

```bash
pip install catalib
catalib init "Hello Plugin" --id hello --dir hello
cd hello
catalib build --check
catalib build
```

Указать в `catalib.toml` `[build] entry = "plugin"`, если класс находится в `src/plugin.py`; пакетные директории снабжать `__init__.py`. Разрабатывать с относительными импортами. Положить в exteraGram `dist/hello.plugin` либо файл `.py`; документация также допускает `.py` для установки. При прямом переносе bundle каталог ресурсов не появится автоматически.

**Подключить SDK helper из catalib:**

```toml
[build]
vendor = "auto"
```

Импортировать helper явной формой `from catalib.support import CatalibPlugin, hook` либо `from catalib.support.files import get_plugins_dir`. После build проверить строку vendor-summary. Для динамических `catalib` импортов выставить `vendor = "full"` и удостовериться, что набор требований устройства доступен.

**Проверить/протестировать проект:**

`catalib build --check` проверяет манифест, discovery, requirements, синтаксис и литералы metadata без записи файлов; это не запуск кода плагина на устройстве. В дополнение к host-side roundtrip в документах snapshot есть исторический T-081: шаблонный bundle доставили на NX789J 2026-05-17, `get_plugins` вернул `error: null`. Это документированное подтверждение для того app/Chaquopy build, не текущий повторный запуск и не гарантия другой версии. В этом review команды, сборка и тесты не запускались. [T-081 record](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/docs/guides/device-workflow.md#L47-L55).

## Расхождения и открытые пробелы

1. **README о прекращении поддержки против возможностей книги.** README прямо сообщает, что catalib прекращает поддержку после ElyxCore. Исходники, книга и changelog одновременно документируют CLI/поддержку SDK и выпуск 0.3.3 (19 мая 2026), но не описывают замену/совместимость с ElyxCore. Архивированное состояние snapshot подтверждает скорее статус проекта, чем активную поддержку.
2. **Преувеличение «самодостаточности».** Выход содержит код runtime и исходники Python-модулей плюс декларацию `__requirements__`. Пакеты не копируются в bundle: exteraGram отдельно устанавливает поддерживаемые зависимости; бинарные wheels исключены. Ресурсные файлы и произвольные assets не включены показанным pipeline.
3. **Не всякое «обычное import» покрывается auto vendor.** Обычные импорты модулей проекта поддерживаются общим finder. Но `vendor="auto"` статически анализирует лишь синтаксис импортов catalib и пропустит динамический вызов/имя; документация рекомендует full mode или явный import.
4. **Циклические импорты не специфицированы.** Нет документации или теста на взаимный import двух модулей проекта; ожидается стандартная семантика импортов Python по реализации. Корректность конкретного графа надо проверять отдельным bundle roundtrip.
5. **CI и выпуск.** В этом snapshot отсутствует `.github/workflows`/CI-конфигурация. Для exact SHA GitHub API возвращает общий status `success` из двух контекстов GitBook (preview/editor) и ноль check-runs; build/test CI этим не подтверждается. `pyproject.toml` описывает pytest и coverage, документация описывает публикацию.
6. **Непроверенная область платформ.** Поддержка runtime эмпирически задокументирована для одного устройства/Chaquopy 3.11.10. Устройство и приложение в рамках этого ingest не запускались; версии за пределами записанного эксперимента не подтверждены.

## Вывод для выбора

catalib технически решает задачу многофайлового Python-плагина при ограничении загрузчика «один верхнеуровневый `.py`»: встроенная таблица исходников и `sys.meta_path` сохраняют пакетную структуру без распаковки на диск. Полезные идеи реализации — детерминированное discovery, literal metadata validation, диагностический source origin и консервативный fallback vendor-анализатора. Практический минус решения сейчас — явное прекращение поддержки/архивный статус. Его допустимо использовать как исторический технический reference; совместимость с ElyxCore и дальнейшая поддержка не доказаны.
