---
type: source-review
source_id: vibogram
reviewer: /root/review_vibogram
model: gpt-6-luna
verdict: accepted-with-gaps
reviewed_at: 2026-09-28
accepted_facts: 31
---

# Независимая проверка vibeDN/ViboGram

## Область и закреплённая версия

Проверен `vibeDN/ViboGram`, ветка `main`, commit [`5f51b6befb2ce9370ea9acf40759d71053db2776`](https://github.com/vibeDN/ViboGram/tree/5f51b6befb2ce9370ea9acf40759d71053db2776), зафиксированный 2026-09-27. `repository.json`, `snapshot.json`, `tree.json` и назначение в radar-context соответствуют одному репозиторию/SHA. `radar-urls.json` — пустой массив. Радар описывал узкий Python→JSON-контракт и host-assisted ASCII-art, но его утверждение от 1 сентября об отсутствии hooks уже устарело для этого commit.

Дерево содержит 36 750 entries и не усечено. Для целевого plugin subsystem сборщик сохранил 17 файлов; для этого review на том же SHA добавлены шесть отсутствующих сборочных файлов: `third-party/python/BUILD`, `submodules/TelegramUI/BUILD`, `Telegram/BUILD`, `Swiftgram/SGDebugUI/Sources/SGDebugUI.swift`, `Swiftgram/SGPluginsUI/BUILD`, `Swiftgram/SGDebugUI/BUILD`. Локально сверены SHA-256 и размеры всех 23 записей manifest; все pinned permalinks ссылаются на тот же SHA. Код и документы читались только как данные, команды приложения и чужие исходники не запускались.

## Независимое покрытие

- `README.md`, `docs/plugin-authoring.md`, `docs/plugin-system-tier4.md` — назначение и статус проекта, формат файла, host API, ограничения переносимости, hooks, UI widgets, actions и documented gaps. Проверены README/plugin contract, а не общая roadmap Telegram-клиента.
- `Swiftgram/SGPython/Sources/SGPythonRuntime.swift`, `Swiftgram/SGPython/Sources/SGAsciiArtBridge.swift`, `Swiftgram/SGPython/BUILD` — CPython init/config, error handling, простой и rich call, event/state serialization, file store, dispatchers, image conversion и target declaration.
- `Swiftgram/SGPluginsUI/Sources/SGPluginsController.swift`, `SGPluginSettingsController.swift`, `SGPluginStoreController.swift` и `SGPluginsUI/BUILD` — import/delete/run/store/settings UI, их фильтры и вызовы runtime.
- `Swiftgram/SGDebugUI/Sources/SGDebugUI.swift`, `SGDebugUI/BUILD`, `submodules/TelegramUI/BUILD`, `Telegram/BUILD`, `third-party/python/BUILD` — debug smoke-test entry point, dependency graph и resource wiring.
- `submodules/TelegramUI/Sources/ChatControllerNode.swift`, `ApplicationContext.swift` — generic on-send dispatch, Anime-ify и `.ascii` paths, incoming-message filters и локальное удаление.
- `plugins/ascii_art.vibo`, `blackjack.vibo`, `calc.vibo`, `card_pull.vibo`, `translit_fix.vibo`, `.gitmodules` — статически проверены для сопоставления marker, entry points, settings/state и примеров composition/host-assisted input.

Полный Telegram-iOS upstream, bundled CPython payload, все плагины и backend/card-game файлы не изучались; граница — code/docs и call-sites собственного plugin subsystem плюс выбранные примеры.

## Найденные проблемы и исправления

- Уточнён `vibogram-008`: `didStart` делает повторный `start()` no-op только после успешной инициализации. При ошибке флаг остаётся false; снимок не подтверждает, что повторная CPython pre-initialization безопасна. Добавлена проверка `python.bundle` и `lastError`.
- Уточнён `vibogram-010` и текст source page: wrapper ловит исключения из вызванной функции, но syntax error или исключение top-level кода плагина возникает вне wrapper `try/except`. В таком случае rich API может вернуть `nil`, а UI показывает общий сбой/совет посмотреть device console, не переданный traceback.
- Уточнён `vibogram-012`: guide требует буквальную первую строку marker, но runtime сравнивает её после `trimmingCharacters(in: .whitespaces)`. Пробелы в начале/конце строки фактически допускаются.
- Добавлены `vibogram-029` и `vibogram-030` о двух отдельных host entry points: `.ascii` запускается при ответе на изображение, асинхронно получает media grid, вызывает Python напрямую и меняет composer для проверки; Anime-ify запускается собственным feature toggle с options и пропускает mixed-format text. Они не равны generic marker loop.
- Добавлен `vibogram-031`: текущий build graph действительно подключает UI/runtime и app resources; одновременно `SGPython/BUILD`, `TelegramUI/BUILD` и UI comments содержат устаревшие утверждения, что hooks/call-sites ещё нет. Обновлён `vibogram-024`, чтобы он различал нынешнюю wiring и отсутствие доказательства её успешной проверки.
- `vibogram-002` и source page обновлены с 17 до 23 manifest-файлов после захвата шести BUILD/debug файлов. В work JSON — 31 уникальный ID, внутренних повторов claims не обнаружено.

### Build/runtime status

`TelegramUI/BUILD` включает `SGPluginsUI` и `SGPython`; targets UI и debug menu зависят от `SGPython`; `Telegram/BUILD` app target включает `PythonStdlib` и device/simulator-specific dynload resource. Но комментарий в `Telegram/BUILD` описывает предшествующий smoke-test результат `resource bundle not found (isBundled=false)` для прежнего library `data` wiring и последующий перенос ресурсов непосредственно на app target. В snapshot нет успешного результата smoke test после этого изменения. README говорит о работающей системе, тогда как датированный 2026-08-26 `plugin-system-tier4.md` и несколько BUILD комментариев отстают от текущей интеграции. Поэтому наличие кода и wiring подтверждено, а сборка/работа текущей схемы остаются `unverified`.

## API, точность и повторы

Факты о JSON contract, temporary-file transport, settings/state, event queue, on-send fail-open behavior, incoming filter, `.forLocalPeer`, image luminance grid, store URL и iOS import limitations сверены с конкретными строками pinned SHA. Утверждения README помечены как заявления проекта. Источниковый анализ не назван runtime-тестом; ничего не помечено `runtime-verified`.

Одинаковые общие приёмы из других источников — узкий JSON host contract, marker hooks, хранение settings и подготовка медиа на стороне host — оставлены с provenance ViboGram. Для будущего тематического синтеза подходят `requests`, `hooks`, `media`, `ui`, `storage` и `portability`; версионные контракты iOS ViboGram не следует сливать с ExteraGram, AyuGram или Margelet. Другие source pages, index, topics и APIs этим review не изменялись.

## Остаточные gaps

1. Bazel/Xcode build и smoke test **после** явного app-resource wiring не выполнялись; на симуляторе и устройстве plugin runtime не запускался.
2. Не исследовались файлы vendored CPython/framework/stdlib/lib-dynload и прочая Telegram-iOS/submodule реализация. Проектные комментарии о прошлых отдельных Linux/Swift проверках не подтверждают этот app build.
3. Реальная iOS process sandbox/entitlements и наличие plugin-per-file security boundary не проверялись. `vibo.data_dir()` — путь к данным плагина, а не доказательство изоляции его Python-кода.
4. Поток и call-sites показывают синхронные вызовы, но нет runtime-замера задержки, thread-safety или проверки конкурентного исполнения. Медленный/зависший hook и сетевое поведение Plugin Store не тестировались.
5. Пять выбранных `.vibo` примеров просмотрены статически; их игра, сетевые сценарии и user-facing UI не исполнялись.

## Вердикт

**accepted-with-gaps.** Источник полезен как версионный пример iOS Python plugin host и страница после уточнений точно разделяет API, интеграцию, устаревшие заявления и незакрытую runtime-проверку. Вердикт не подтверждает успешную сборку или работу плагинов на устройстве.
