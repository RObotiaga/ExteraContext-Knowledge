# Независимая проверка: `exteragram-utils`

- **Источник:** PyPI `exteragram-utils` 0.1.3, опубликованный 2025-11-18.
- **Артефакт:** wheel SHA-256 `6f245c56e0209538047cc03cf396328e3842dfe784f0744eea46755f918533fb`; PyPI JSON snapshot SHA-256 `8aa523ffc3f6018f6c35ff07849fe71f46064109b44c7cca76a732a278d98c24`. Git commit у бинарного package release отсутствует; версия и digest задают проверенный scope.
- **Sdist:** `work/exteragram_utils-0.1.3.tar.gz`, SHA-256 `28ecfccc03053b213d40855890995fb0046156e291f63e852affea0e8529eed4`.
- **Область:** независимо прочитаны все 21 файла wheel snapshot из `raw/exteragram-utils/files/` (16 `.py`, включая пустые `__init__.py`, и 5 `.dist-info` файлов); просмотрены tree, manifest, PyPI metadata, полный `dev_client.py`, все SDK declaration modules, README/`pyproject.toml`/`setup.py`/`MANIFEST.in` sdist и член-лист архива. Исходные `.pyi` в sdist сверены с wheel root-level stub modules. `radar-context.md` и `radar-urls.json` для данного slug отсутствуют; идентификация как developer package подтверждается PyPI summary и README.
- **Вердикт:** `accepted-with-gaps`.

## Независимое покрытие

Проверены публикация и packaging (Python requirement, dependencies, entry point, top-level namespace, README imports, custom setup commands), все Android SDK stub surfaces и CLI implementation. Покрыты ADB setup/forwarding и ошибки/неограниченные ожидания команд, TCP connect/retry lifecycle, reader/ping threads, JSON request/response correlation, timeout/disconnect, plugin calls/debugger calls, metadata AST parser, file polling/upload/reload, CLI argument flow и logging. Просмотрены module stubs для hooks/base plugin, queues/account helpers, Android helpers, reflection, storage/settings, Markdown, alert/bulletin/settings UI и metadata helper. Все методы этих SDK modules подтверждены как declarations/stubs, не runtime behavior.

Sdist прочитан без установки и распаковки. Все member paths проверены на абсолютные пути и `..`; опасных путей не найдено. SHA-256 совпал с pinned PyPI JSON. Все 21 wheel entries и размеры соответствуют tree; каждый сохранённый raw-файл побайтно совпал с записью wheel. Все 14 Python files из `py_stubs/` sdist совпали с соответствующими root-level wheel modules. Setup/build/install, import, tests, ADB, sockets и Android client не запускались.

## Исправления и точность

- Исправлено утверждение о retry в `send_message`: исключение вызывает `disconnect()`, а тот навсегда устанавливает `running=False`; последующий `connect()` не выполняет свой `while self.running`. Следовательно, код не повторяет запрос после этого пути. Также зафиксирован отдельный recovery edge case: при server EOF старый response thread может оставаться живым в момент reconnect и помешать запуску нового reader.
- Уточнена трактовка `Requires-Python: >=3.8`: SDK root `.py` declarations используют `str | None` без future annotations, поэтому PEP 604 требует Python 3.10+ и несовместима с заявленным floor. Официальная SDK документация отдельно описывает plugin runtime Python 3.11; это не является подтверждением совместимости package imports с Python 3.8.
- Добавлено замечание о stream parser: UTF-8 decode каждого отдельного `recv()` с `errors="replace"` может испортить символ, если байты многобайтового символа разделены между chunks. Ошибка `raw_decode` оставляет хвост без ограниченного buffer/recovery.
- Сопоставлены действия этого CLI и action set в документации официального DevServer: pinned client содержит ping/get/write/reload/debugger operations, тогда как SDK docs также перечисляют enable/disable/remove и Elyx actions. Server implementation или protocol version mapping в package отсутствует; контракты не объединены как будто они подтверждённо эквивалентны.
- Уточнены metadata claims: PyPI owner account не является полем author; PyPI и sdist не задают license или project/home/docs URL и не указывают client/SDK compatibility version.
- Обновлены source coverage, Python compatibility discussion, protocol limitations, facts и frontmatter review link/status.

## Повторы и canonical topics

Подготовленное множество содержит **41 уникальный fact ID**, дубликатов ID нет. Схожие утверждения о thread dispatch, hook declarations, UI helpers и TCP DevServer уже встречаются в документации официального SDK и других источниках; по правилам базы они сохраняются как отдельные provenance. Для последующего синтеза подходят `network.md`/`workflow.md`/`debug.md` (CLI и JSON transport), `portability.md` (Python floor и environment), а также `hooks.md`, `threading.md`, `accounts.md`, `storage.md` и `ui.md` для stub-only surfaces. Действия протокола и SDK signatures должны сохранять source/version distinction. Source page и facts JSON внутри себя повторно описывают отдельные API в coverage prose, интерфейсной таблице и отдельном SDK разделе; это навигационные повторы, не дополнительные facts, и при будущей редактуре их можно сократить.

## Остаточные пробелы

- Wheel содержит заглушки вместо runtime SDK bodies; недоступны фактические Java bridge semantics, hook priority/cleanup, callback threading, account routing, filesystem/settings behavior и UI lifecycle.
- В пакете отсутствуют peer/server code и mapping к конкретной версии клиента; не установлено, соответствует ли TCP protocol конкретной версии exteraGram.
- Не подтверждались runtime compatibility Python, работа CLI, ADB forwarding, поведение на устройстве или integration behavior; статический просмотр не заменяет эти проверки.
- В артефактах нет релевантного набора тестов. Для PyPI release нет repository/commit permalink, так что точные API claims ссылаются на pinned release и локальные archive paths, а не на VCS line links.
- Лицензия из доступных PyPI metadata/sdist не устанавливается.

Источник принят как точное статическое описание pinned release, с явно указанными пробелами по SDK implementation, protocol peer и runtime/client compatibility. Гарантия абсолютной полноты для недоступного кода не даётся.
