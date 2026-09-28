# Независимая проверка: `skill-makarworld`

- **Источник:** `makarworld/exteragram-plugin-skill`
- **Commit:** `b6fdffaf017e416eab1fb4bd3aaa984325a2f23e` (`main` в снимке от 2026-09-27)
- **Радарный контекст:** строки 1493–1502 `raw/skill-makarworld/radar-context.md` называет этот материал дополнительным/проверочным skill для ExteraGram/AyuGram; `radar-urls.json` пуст.
- **Вердикт:** `accepted-with-gaps`.
- **Результат:** `work/skill-makarworld-facts.json` содержит **39 уникальных фактов** с уникальными ID и claims. Исходные файлы не менялись; дополнены facts/source page и сохранённый manifest.

## Независимое покрытие

Сверены `tree.json`, `file-manifest.json`, `snapshot.json`, `repository.json`, source page и все 39 facts. У дерева 24 blob-файла, snapshot не truncated. Все 24 файла присутствуют в manifest; повторный SHA-256 расчёт по каждому сохранённому файлу дал 0 расхождений. При первичной проверке обнаружены два не попавших в выборку корневых файла — `.gitattributes` и `.gitignore`; они получены read-only acquisition по тому же commit SHA и прочитаны. Содержимое обоих относится к line-ending normalization/бинарным расширениям и editor/OS/Python noise, а не меняет описанную SDK поверхность.

Полностью просмотрены `README.md`, `SKILL.md`, все 15 `reference/*.md`, все 4 `examples/*.py`, `LICENSE`, `.gitattributes`, `.gitignore`. Reference inventory: `android-utils.md`, `class-proxy.md`, `client-utils.md`, `dev-workflow.md`, `elyx.md`, `file-utils.md`, `hook-utils.md`, `intents.md`, `multi-account.md`, `plugin-class.md`, `repo-conventions.md`, `settings.md`, `text-formatting.md`, `ui-helpers.md`, `xposed-hooking.md`. Примеры: `custom_setting.py`, `ghost_mode.py`, `hello_command.py`, `minimal.py`.

Проверено покрытие метаданных и AST loader, lifecycle/app events, settings/menu items, SDK hooks и HookResult, аккаунтов/очередей/клиентских helpers, Android UI, reflection/Xposed/class proxy, intents, файлов, Elyx metadata/imports/assets/locales/settings/dependencies, ElyxBuilder и reload, DevServer/debugger, PIP/предустановленных библиотек, `awesome-plugins` edit/release conventions и лицензии. Ни один файл исходника не исполнялся и ничего не устанавливалось.

## Исправления

1. Уточнено важное правило Elyx archive: reference принимает корневой `refmap.yaml`, `refmap.yml` или `refmap.json` и рекомендует YAML. Изначальный fact `skill-makarworld-022` чрезмерно требовал именно `refmap.yml`; claim, API и recipe исправлены. В тексте также уточнено, что рекомендация иметь один plugin class в entry module связана с документированным поведением loader (создаётся первый найденный subclass), а не с запретом дополнительных классов в проекте.
2. Добавлены пропущенные детали установки самого skill, включения developer mode, отдельного debugger port и IDE path mappings, JSON/request-ID протокола DevServer и Elyx base64 payload, рекомендаций к custom DevServer client, перечня pre-installed libraries/PIP limits, Elyx Java callback proxies (`gen`, `gen2`, `mvel_execute`) и Elyx reload troubleshooting.
3. Дополнена API-карта файловых helpers, `NotificationCenterDelegate`/controllers, Android listeners/logging/clipboard и `AlertDialogBuilder`. Уточнена оговорка `hook_utils`: `find_class` уже возвращает `Class`, поэтому `getClass()` перед Java reflection вызывать нельзя.
4. Добавлены facts `skill-makarworld-033`–`039`; исправлены темы claims `003`, `018`, `024`. Текущий machine layer проверен: **39 facts, 39 уникальных ID, 39 уникальных claims**, каждый evidence path существует и его конечная строка входит в файл; SHA paths указывают на commit снимка. Статусы остаются документационными, кроме fact о содержимом примера, помеченного `code`; runtime claims не добавлялись.

## Дубликаты и различия provenance

Внутри facts-файла повторов нет. Поиск по принятым facts `official-sdk` подтвердил повторяющиеся знания: baseline/metadata (`sdk-baseline`, `metadata-ast`, `plugin-id-single`), lifecycle (`lifecycle`), outgoing hook/HookResult и Xposed (`hook-registration`, `hook-signatures`, `outgoing-hook`, `hook-strategies`, `xposed-hooks`, `xposed-param`, `java-reflection-find`, `class-proxy-dsl`), account callbacks/helpers (`account-scope`, `account-client`, `notification-account`), очереди/UI thread (`queue-api`, `queue-names`, `ui-thread`), request/send/formatting (`send-request`, `send-helpers`, `low-level-send`, `edit-message`, `text-formatting`), settings/UI (`settings-row-types`, `dialogs`, `bulletins`), Android listeners/log/clipboard (`android-listeners`, `android-log-clipboard`), file handlers (`file-controller`), intents (`intents`), Elyx archive/assets/localization/dependencies/build/reload (`elyx-archive`, `elyx-assets`, `elyx-localization`, `elyx-settings`, `elyx-requirements`, `preinstalled-libs`, `elyxbuilder-cli`, `elyx-dev-reload`, `elyx-troubleshooting`) и DevServer (`devserver-security`). Эти записи оставлены как самостоятельные provenance для этого commit; при тематическом синтезе они относятся к canonical topics `portability`, `build`, `lifecycle`, `hooks`, `accounts`, `threading`, `requests`, `ui`, `storage`, `debug` и `distribution` соответственно. Версионные условия остаются раздельными: baseline skill 1.4.4.3; multi-account 1.4.5.0+; Elyx 1.4.5.3+; intents app build 66999 / 12.6.4+; custom generated class name app code 66690+. Репозиторный workflow `awesome-plugins` не объединён с общими SDK правилами.

## Остаточные пробелы

- README говорит, что skill собран из 32 страниц официальных docs, но снимок содержит только сам skill/reference, не эти 32 исходные страницы и не точный scrape commit. Утверждение сохранено как заявление README. Skill сам отдаёт live docs приоритет по SDK behavior.
- Нет исходника SDK, клиента, ElyxBuilder или `elyx_dev_client.py` для проверки реализаций. Сигнатуры, versions, DevServer permissions/auth/ACL, package-resolution semantics и release instructions подтверждены только документами этого commit; runtime, build и release-процедуры не запускались.
- API-карта суммирует ряд длинных справочников, а не воспроизводит каждый параметр каждого UI/settings/file helper. Для точной сигнатуры следует открыть связанную reference страницу и перепроверить применимость к живым docs/target app.
- В repo-specific release guidance есть конкретные Pluggy env var names и запреты внешней публикации; их наличие в документации не доказывает состояние секретов/доступа или фактические результаты Pluggy.

Страница принята с этими границами; вердикт означает проверенную полноту/точность относительно сохранённого skill snapshot, а не подтверждение текущего SDK runtime.
