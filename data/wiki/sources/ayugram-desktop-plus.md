---
type: source
source_id: ayugram-desktop-plus
platform: Desktop
review_status: accepted-with-gaps
review: ../reviews/ayugram-desktop-plus.md
reviewer: /root/review_ayugram_desktop_plus
model: gpt-6-luna
date: 2026-09-28
---

# AyuGram Desktop Plus: нативные паттерны форка Telegram Desktop

Источник: [Kindness-Kismet/AyuGramDesktop-Plus](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus) на SHA `b59475e090b64fd5c8bc4124535c515050b70ef0`; ветка `main`, snapshot за 2026-09-27. Лицензия объявлена как GPL-3.0-or-later; сохранён корневой LICENSE. Уникальный collector: `/root/collect_ayugram_desktop_plus` (`gpt-6-luna`). Независимая проверка ожидается.

## Роль и границы

Это **нативный Desktop-форк** Telegram Desktop на C++20/Qt для Windows, Linux и macOS. Полезен как пример изменения самого клиента: жизненный цикл feature, CMake, реактивные настройки, Qt network, UI/data threading, обработка `HistoryItem` и локальная debug-поверхность. Он не предоставляет ExteraGram Android plugin API, Android hook API или совместимый формат .plugin/DEX. Код `Telegram/SourceFiles/ayu/` компилируется в приложение как source; слово `features` не означает runtime plugin loader.

README перечисляет возможности настройки UI, авто-пробелы CJK/Latin, фильтры, переводчик и emoji packs. Это обзор документации, не подтверждение работы конкретной сборки. В коде различайте собственные Ayu классы, Qt API и HTTP API внешних сервисов: например, Google Translate — внешний provider, а `QNetworkAccessManager` — транспорт Qt. Debug TCP service является developer tool процесса, а не plugin IPC. Подтверждений runtime в этой работе нет.

## Версия и получение

- Репозиторий: `https://github.com/Kindness-Kismet/AyuGramDesktop-Plus`
- SHA: `b59475e090b64fd5c8bc4124535c515050b70ef0` (закреплённый снимок `main`; дерево не truncated).
- Снимок: [`snapshot.json`](../../raw/ayugram-desktop-plus/snapshot.json), [`tree.json`](../../raw/ayugram-desktop-plus/tree.json), файлы и SHA-256: [`file-manifest.json`](../../raw/ayugram-desktop-plus/file-manifest.json).
- Manifest содержит **63 выбранных файла**, а полный `tree.json` — 7 355 blob-объектов; snapshot доступен и не truncated. В выборке есть README/LICENSE, AGENTS, app-debug guides/CLI, CMake/build-файлы и выбранные ayu settings/lifecycle/features/UI/debug/data исходники. Это целевой срез, а не полный обход Telegram Desktop. Исторических URL в `radar-urls.json` нет (`[]`).
- Источник радара: [`radar-context.md`](../../raw/ayugram-desktop-plus/radar-context.md), выдержка из `raw/radar.md` с указанием, что найденный результат относится к Desktop fork, а не Android plugin source.

## Покрытие

| Прочитанные файлы | Извлечено | Пропуски |
|---|---|---|
| `README.md`, `AGENTS.md`, `Telegram/build/version`, `Telegram/CMakeLists.txt`, `scripts/build.py`, `scripts/build_support/cmake_patch.py` | Позиционирование, лицензия, структура `ayu/`, CMake source registration, правила rpl/threading и описанный build/debug workflow | Сборка и версии окружения не проверялись запуском |
| `ayu_infra.{h,cpp}`, `ayu_settings.{h,cpp}`, `ayu_state.{h,cpp}`, `ayu_worker.{h,cpp}`, `utils/telegram_helpers.h`, `data/ayu_database.{h,cpp}` | Инициализация, JSON/reactive settings, account/session lifecycle, SQLite schema/migrations | Не все call-sites upstream и не весь Telegram core |
| `features/auto_space/*`, `features/filters/{filters_controller,filters_cache_controller,filters_utils}.*`, `features/translator/{ayu_translate_provider.*, implementations/base.*, implementations/google.*}` | TextWithEntities трансформация, внутреннее HistoryItem filtering/cache, async translation и внешний network provider | Не прослежены все call-sites сообщений в upstream |
| `features/emoji_packs/{emoji_packs,emoji_font}.*` | Скачивание, SHA-256 verification, общий size limit на этапе импорта, staging/activation | Preset manifest size не сверяется с числом скачанных байт; UI picker и platform font backend изучены частично |
| `ui/message_history/{history_inner.cpp,history_item.cpp}`, `ui/context_menu/context_menu.*` | Примеры внутренних точек изменения истории/меню | Не являются общими hook-контрактами |
| `debug/debug_server.*`, `debug/debug_commands.*`, `debug/commands/*`, `.claude/skills/app-debug/{SKILL.md,guides/*,scripts/cli.py}` | Debug-only localhost протокол и локальные инструменты наблюдения | CLI/debug server не запускались |
| `radar-context.md`, `radar-urls.json` | Контекст упоминания и отсутствие заданных historical URL | Утверждения радара — только secondary |

Исходники читались как данные. Ни чужой код, ни сборка, ни тесты не запускались; пакеты не устанавливались.

## Технические факты

### Внутренний API Desktop-форка

- **Добавление feature:** `AGENTS.md` направляет код в `ayu/features/<name>/` и требует перечислить каждый файл в `ayugram_files` в `Telegram/CMakeLists.txt`. Это compile-time включение кода в форк, без динамического loader.
- **Порядок инициализации:** `AyuInfra::init()` последовательно запускает language, database, UI settings, icon, worker, remote config manager, translator, Debug server ([код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_infra.cpp#L71-L80)). Новая подсистема должна стартовать после зависимостей и иметь подходящий shutdown lifecycle.
- **Настройки:** `AyuSettings` использует `rpl::variable<T>`; `current()` возвращает текущую величину, `value()` выдаёт producer изменений ([header](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_settings.h#L90-L156)). AGENTS требует синхронно поддерживать член, `to_json`, `from_json`, default и UI registration. Подписки UI должны привязываться к `lifetime()`.
- **Потоки и аккаунты:** UI, `Data::Session`, `History` и `PeerData` принадлежат главному потоку (AGENTS). Worker обходит `Core::App().domain().accounts()`, проверяет `maybeSession()` и ставит таймер 3000 мс, прекращая работу при shutdown ([код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_worker.cpp#L33-L80)). Это демонстрирует account/session ownership внутри Desktop.
- **Текст и история:** `AutoSpace::processText(TextWithEntities&)` обрабатывает участки текста с entities, поэтому трансформация должна сохранять диапазоны форматирования. `FiltersController` принимает решение для `HistoryItem` с учётом peer/settings; связанный результат кэшируется и инвалидируется на изменении item ([фильтр](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/features/filters/filters_controller.cpp#L98-L218)). Оба случая требуют доступа к внутренней модели клиента и не превращаются в Android plugin hooks.
- **Сетевой feature:** `MultiThreadTranslator::startTranslation()` ограничивает параллельную работу частями текста; `GoogleTranslator::startSingleTranslation()` использует Qt Network, timeout, проверку ошибки и JSON parse. HTTP provider находится вне клиента, Qt — отдельная библиотека, а классы Ayu — внутренний код, не extension API.
- **Безопасная загрузка ресурса:** Emoji preset downloader пишет чанки через `QSaveFile`, проверяет сетевой статус и SHA-256, затем передаёт файл в импорт. `preset.size` задаёт fallback total для progress, но фактический размер ответа с ним не сравнивается; импорт задаёт общий верхний предел размера файла, не сравнивая его с manifest size. Преобразование собирает pack во временном каталоге и публикует его переименованием. Это полезные общие идеи для больших ресурсов; конкретные пути и форматы принадлежат Desktop-клиенту.

### Внутренняя персистентность

`AyuDatabase` использует SQLite ORM и относительный путь `./tdata/ayudata.db`; при старте схема синхронизируется до и после версии миграций. При ошибке migration/init исходные `.db`, `-shm` и `-wal` файлы переименовываются с timestamp, затем создаётся/проверяется база заново. Это важный integration seam для форка: собственные данные живут в клиентском профиле и lifecycle старта, а не в отдельно загружаемом plugin storage API.

### Developer/debug API

`AyuDebug::StartServer()` находится под `#ifdef _DEBUG`, слушает loopback `127.0.0.1:20100` и принимает одну newline-команду на соединение. Ответ — `OK`/`ERR`; quoted args обрабатываются как JSON strings; TCP bytes копятся до целой UTF-8 строки. `Execute()` агрегирует handler maps по областям и превращает `std::exception` в `Result::Err`. Server освобождается при `aboutToQuit` ([server](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/debug/debug_server.cpp#L119-L145), [dispatch](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/debug/debug_commands.cpp#L19-L60)). В выбранном коде нет аутентификации команд; loopback ограничивает интерфейс, но не проверяет клиента. Не выставляйте такую поверхность наружу.

AGENTS описывает команды settings read/write, screenshot, control tree/click, fake session/message. `settings.set` переиспользует JSON decoder и `validate()`. Это debug-only средства процесса, синхронно действующие на UI; fake state не подтверждает поведение Telegram backend. Ни одна команда в рамках сбора не выполнялась.

## Вызовы и назначение

| Модуль/класс | Сигнатура или call-site | Роль и lifecycle | Evidence |
|---|---|---|---|
| `AyuInfra` | `init()` | Startup sequence приложения | [код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_infra.cpp#L71-L80) |
| `AyuSettings` | `current()`, `...Value()`, `to_json/from_json` | Конфигурация и реактивные изменения клиента | [header](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_settings.h#L90-L156), [serialization](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_settings.cpp#L1180-L1402) |
| `AyuWorker` | `initialize()`, `runOnce()` | Периодическая работа с несколькими `Main::Session` | [код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_worker.cpp#L33-L80) |
| `AutoSpace` | `processText(TextWithEntities&)` | Трансформация текста с форматированием | [код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/features/auto_space/auto_space.cpp#L108-L150) |
| `FiltersController` | `filter(HistoryItem*)`, `invalidate(HistoryItem*)` | Внутренний message pipeline и кеш | [код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/features/filters/filters_controller.cpp#L98-L218) |
| `MultiThreadTranslator` | `startTranslation(StartTranslationArgs)` | Очередь async частей с ограниченной конкуренцией | [код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/features/translator/implementations/base.cpp#L140-L170) |
| `GoogleTranslator` | `startSingleTranslation(...)` | Внутренний Qt network client стороннего сервиса | [код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/features/translator/implementations/google.cpp#L68-L139) |
| `EmojiPacks` | `download(...)` / install | Потоковая сеть, digest и staging | [код](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/features/emoji_packs/emoji_packs.cpp#L275-L343) |
| `AyuDebug` | `StartServer()`, `Execute(command,args)` | Localhost command bridge только Debug | [server](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/debug/debug_server.cpp#L119-L145) |

Таблица содержит native Desktop calls, Qt library calls и отдельный внешний service. Ни один не заявляется как API Android host.

## Рецепты и переносимость

1. Для **форка Desktop** размещайте feature под `ayu/features`, регистрируйте файлы в CMake и подключайте startup после необходимых зависимостей.
2. Для **реактивной настройки** реализуйте `rpl::variable`, чтение/producer, JSON сериализацию с default, validation и UI registration.
3. Для **обработки сообщений** сохраняйте entities, учитывайте peer/account и синхронизируйте cache invalidation с edit/delete.
4. Для **скачивания крупных ресурсов** пишите потоком в staging, ограничивайте/проверяйте размер, сверяйте digest и активируйте только после успешной проверки.
5. Для **Android plugin разработки** найдите API и hook contract Android host отдельно. Здесь переносимы идеи жизненного цикла/обработки данных, но не конкретные классы Ayu Desktop.

## Радар, ограничения и факты

Радар упоминает проект как Desktop форк и указывает, что такие результаты обычно не относятся к Android plugin development ([контекст радара](../../raw/ayugram-desktop-plus/radar-context.md)). Это вторичный вывод, согласующийся с README и деревом исходников. README описывает возможности и цикл AI-assisted build/debug, однако в этой работе ни сборка, ни runtime не проверялись. Исторических ссылок для сравнения с предками нет; весь upstream Telegram Desktop и все feature call-sites не покрыты. Проверок приложения на устройствах и `runtime-verified` фактов нет.

Машинный слой содержит **25 уникальных фактов**: [`ayugram-desktop-plus-facts.json`](../facts/ayugram-desktop-plus.json). `code`, `docs`, `secondary` и `inference` отделены по доказательствам.
