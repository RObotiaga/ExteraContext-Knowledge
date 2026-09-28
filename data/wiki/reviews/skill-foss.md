# Независимая проверка: `skill-foss`

- **Источник:** `fossSquad/exteraSkill`
- **Commit:** `0f5bde5296ba06a3fce4751228d26acd112d51bb` (`main`, снимок от 2026-09-27)
- **Радарный контекст:** `raw/skill-foss/radar-context.md` указывает на строки 1495–1502 `raw/radar.md`: источник назван основным специализированным skill для ExteraGram/AyuGram-плагинов. `radar-urls.json` пуст; назначение сверено с `SKILL.md` и README.
- **Вердикт:** `accepted-with-gaps`.
- **Результат:** `work/skill-foss-facts.json` содержит **34 уникальных факта** с уникальными ID и claims.

## Независимое покрытие

Сверены `snapshot.json`, `tree.json`, `file-manifest.json`, все сохранённые файлы, source page и исходные 32 facts. Snapshot зафиксирован на требуемом commit и не помечен truncated. В tree, manifest и локальном `files/` ровно 48 blob-файлов; пересчёт SHA-256 дал 0 отсутствующих файлов и 0 расхождений. Папки исходников и примеры — данные; скрипты не запускались, ничего не устанавливалось и не собиралось.

Прочитаны `README.md`, `SKILL.md`, `LICENSE`, все 45 Markdown-файлов, включая все `references/elyx/*.md`, а также `scripts/push_plugin.py` и `scripts/java2md.py`. Полный перечень covered paths сгруппирован в таблице «Границы покрытия» source page. На уровне функций независимо просмотрены Python metadata/lifecycle/hooks/HookResult, версии аккаунтных API, очереди и UI thread, requests/media/settings, Xposed/reflection/class proxy, intents/file handlers, Android dialogs/bulletins, Elyx archive/metadata/imports/assets/locales/settings/dependencies/build/reload/troubleshooting, DevServer, DEX build/load/install/debug workflow, generated Telegram class inventories и обе утилиты. Сигнатуры и statements в machine facts относятся к документам/коду именно этого commit; чтение справок не обозначено runtime test.

Все исходные 32 факта имеют уникальные ID/claims, существующие evidence paths и диапазоны строк в пределах файлов. Evidence URLs закреплены за commit. Статусы docs/code используются по происхождению: описанные в справке API и workflow остаются `docs`, статические наблюдения двух сохранённых скриптов — `code`.

## Исправления

1. Расширен fact `skill-foss-027`: дополнены заявленные `exteragram.jar` stubs, получение из APK через exteralib и отсутствие Gradle task/build definition в snapshot; версия toolchain остаётся документационным заявлением.
2. Добавлен `skill-foss-033` с DEX loader chain: `DexClassLoader` → загрузка Java entry class → reflection-вызов `initAndStart()`, а также ADB push, `Install from file` и in-app restart. Указано, что это схема из docs, не испытание.
3. Добавлен `skill-foss-034` о диалогах и bulletins. Source page теперь называет DialogBuilder типы, callback/UI-thread caveat и BulletinHelper группы/duration constants вместо одного только упоминания этих документов в coverage table.
4. Сохранено расхождение имени скрипта: `SKILL.md` и `debugging.md` отсылают к отсутствующему `scripts/adb_push_py.py`; pinned tree содержит `scripts/push_plugin.py`, чья Usage строка всё ещё печатает имя `adb_push_py.py`. Fact `skill-foss-029` это корректно фиксирует.
5. Уточнено, что push script закрывает сокеты после `sendall` и не получает серверные ответы. `successfully` в выводе не подтверждает принятие `write_plugin`/`reload_plugin`.

В JSON evidence paths, line ranges и SHA сверены; сейчас **34 facts, 34 уникальных ID, 34 уникальных claims**, все пути существуют и конечные строки входят в файл. Факты синхронизированы в `wiki/facts/skill-foss.json`.

## Дубликаты и различия provenance

Внутри facts-файла повторов нет. Повторяющиеся документированные знания обнаружены в уже принятых `official-sdk` и `skill-makarworld`: metadata/lifecycle, HookResult strategies, account scope, `run_on_queue`, `send_request`, Xposed hooks, class proxy, FilesController, Elyx archive/import/settings/dependencies и DevServer. Это самостоятельное подтверждение от `fossSquad/exteraSkill`, оставленное как отдельное provenance этого commit; канонические темы для последующего синтеза: `lifecycle`, `hooks`, `accounts`, `threading`, `requests`, `java_reflection`, `files`, `elyx`, `devserver`, `build` и `debug`. Пересечения с `exteragram-utils` относятся к одноимённым stubs/объявлениям и не повышают их до runtime implementation. Генератор Telegram class references частично пересекается с `official-sdk:common-telegram-classes-index`, но у skill файлы объявлены как вывод генератора DrKLO `master`; это разные provenance и разные версии. DEX build/load/how-to уникально документирован здесь среди проверенных skill/API facts; `for-vibecoders` отдельно сообщает отсутствие такой практики в просмотренных материалах.

Совместимость не сведена к одному baseline: общий Python setup/plugin example указывает SDK 1.4.4.3, multi-account API требует 1.4.5.0+, Elyx pages используют 1.4.5.3+. DEX toolchain заявлен отдельно и не подтверждён проектом этого репозитория.

## Остаточные пробелы

- В репозитории нет SDK, клиента exteraGram, DEX loader implementation, Gradle-проекта, tests или CI; поэтому API availability, signatures, build prerequisites, permissions, installation, reload и hook behavior не проверялись в установленном приложении.
- DEX `DexClassLoader` example импортирует `java.io.File`, но не использует его; `ApplicationLoader` в примере также не импортирован. Код только иллюстративен и не может считаться проверяемым standalone loader.
- Документационные reference inventories `ChatActivity`, `LaunchActivity`, `MessageObject`, `MessagesController`, `SendMessagesHelper` и `TLRPC` сгенерированы утилитой, чьи URL указывают на подвижный DrKLO/Telegram `master`; это не pinned API конкретного exteraGram build. Парсеры пропускают часть возможных declarations.
- Снимок содержит упомянутый отсутствующий push filename как ссылку в документации; причина rename/missing file неизвестна. External `extera-pysdk-builds`, exteragram-utils, ElyxBuilder, `elyx_dev_client.py` и примерные DEX repos не вложены и здесь отдельно не сверялись.
- Большие upstream inventories перечислены и описаны как generated indices; страница не извлекает каждый Telegram класс/метод в отдельный fact. Для точного Java API нужно сверять соответствующий pinned build.

Вердикт означает независимую проверку относительно полного сохранённого snapshot и названных границ документации; он не гарантирует совместимость, полноту живого SDK или успешную сборку/установку.
