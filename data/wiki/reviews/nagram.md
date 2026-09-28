# Независимая проверка: `nagram`

- **Источник:** [NextAlone/Nagram](https://github.com/NextAlone/Nagram), Android-клиент Telegram.
- **Pinned snapshot:** `b8db62a65e1e4dee34d92bff412548ef628ddb06`, `main`, захвачен 2026-09-27.
- **Вердикт:** `accepted-with-gaps`.
- **Принято:** 34 уникальных fact ID в `work/nagram-facts.json`.
- **Объём:** полный рекурсивный tree содержит 24 638 entries и не помечен truncated. После получения ещё нужных документов проверены хэши и Git blob IDs всех 65 файлов `raw/nagram/files`; пропусков или несовпадений нет. Сборка, tests и приложение не запускались.

## Независимое покрытие

Сверены snapshot/repository metadata, raw tree, file manifest, radar context/URLs, README и его целевые блоки о feature list/build/debug, `README.NekoX.md` в пределах его происхождения, `LICENSE`, `BRANDING.md`, корневые Gradle settings и `TMessagesProj/build.gradle`. По коду проверены все 24 исходные записи и добавленные подтверждённые patterns: menu/config migration; Java/Kotlin `ItemOptions`; account-scoped `NotificationCenter` и lifecycle/thread ограничения; `ChatActivity` menu/double-tap/forwarding call sites; Markdown spans; Ktor logging, ObjectBox retention и detail/search UI; lyrics; audio recorder effects; motion-photo dispatch/error path; SAF sticker cache/account observers; OEM AI dispatch; local profile overrides; message-to-clipboard URI.

Line evidence сверена с файлами commit. В `evidence.json` 44 evidence row; все line ranges укладываются в сохранённые файлы. Для каждого из 34 facts есть хотя бы одна evidence row. Локальные SHA-256, byte counts и Git blob SHA-1 всех 65 manifest files совпадают с pinned snapshot/tree.

## Найденные проблемы и исправления

- Русскоязычные поля всех 24 исходных записей в `work/nagram-facts.json` были повреждены преобразованием кодировки. Текст обратимо восстановлен, JSON записан в UTF-8.
- `nagram-001` сужен до утверждения, действительно подтверждённого `README.md:1-3`. Документированные функции теперь отдельно помечены `docs`; буквальный заголовок README `Additional feature over Nagram` не интерпретируется как доказательство происхождения функции.
- Дублирующий `nagram-007` объединён с `nagram-003`: тот же `MessageMenuCompact` и те же методы, с уточнением `@JvmStatic` interop. `nagram-014` оставлен отдельно как доказательство вызова helper из host menu.
- Уточнено, что `NaConfig.addConfig` и `checkMigrate` — private helpers, а `MessageMenuCompact.parseCsv` — private; это внутренние детали клиента, не public SDK. В списке меню названы реальные blacklist option groups.
- Добавлены факты о разнице README toolchain (`android-33`/build-tools `33.0.0`) и Gradle (`compileSdkVersion 36`/build-tools `36.0.0`), отдельной branding policy, voice effects lifecycle, external sticker cache/account observers, OEM AI, локальных self-profile overrides, FileProvider/clipboard path и diagnostic log UI.
- Зафиксирован статически видимый failure path: если `embedMotionPhotoMetadata` возвращает `false`, `MotionPhotoHelper.createMotionPhoto` проходит мимо вложенной проверки output и далее возвращает `Success`. Это анализ control flow; фактическое поведение на устройстве не проверялось.
- Сетевой журнал хранит запросы/ответы без видимой очистки секретов; сохранённые headers/body затем показывает detail screen. Это риск содержимого приложения, установленный чтением кода, не проверка privacy поведения на устройстве.

## Повторы и provenance

Внутренний повтор `nagram-003`/`nagram-007` устранён. `nagram-017` описывает HTTP wrapper и `finally`, `-018` — собранное содержимое/redaction, `-019` — ObjectBox/retention, `-034` — detail view, `-035` — list/search/clear: это разные стадии diagnostic pipeline, поэтому они оставлены раздельными. Menu helper (`-003`) и его host wiring (`-014`) также не дублируют друг друга.

Nagram рассматривается только как `NextAlone/Nagram`. README благодарит Nullgram, но это acknowledgement не доказывает происхождение конкретной реализации. `NagramX` (`risin42/NagramX`), `NagramXTurbo` (`temporaryna/NagramXTurbo`) и `Nullgram` (`qwq233/Nullgram`) — отдельные source identities; их контракты и факты не перенесены. Radar сообщает вторично о переносе Live Photo между родственными клиентами, но это утверждение не используется как code evidence для Nagram.

## Остаточные gaps

- Просмотрено 65 выбранных файлов из 24 638 tree entries; полный diff относительно Telegram/NekoX upstream и все крупные host classes не анализировались. Граница по upstream-коду ограничена конкретными plugin-development-полезными patterns и их call sites.
- Не прослежены все callers `LocalPeerColorHelper`, `StickerSetHelper` и GIF export branch `MessageHelper`; некоторые дополнительные функции и UI call sites могут быть вне сохранённой выборки. Из набора Prism syntax-highlighting файлов не строилась отдельная end-to-end цепочка.
- `README.NekoX.md` не используется как контракт Nagram; исторические унаследованные заявления полностью не сверялись с кодом этого commit.
- Наличие plugin SDK/lifecycle/manifest в публичном snapshot не обнаружено. Вывод ограничен полным деревом и не исключает внешних unpublished инструментов. Ни один внутренний класс не подтверждён как совместимый API для ExteraGram/AyuGram plugins.
- Runtime, build и tests не проверялись; все `code` выводы — статическое чтение данного SHA, а не подтверждение поведения установленного приложения.
