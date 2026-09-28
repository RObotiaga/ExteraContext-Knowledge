# Независимая проверка: `nagramx-turbo`

- **Источник:** [`temporaryna/NagramXTurbo`](https://github.com/temporaryna/NagramXTurbo), Android fork Nagram X.
- **Проверенный SHA:** `267a33ead32b6f003b6aa8f913e7727e9992a7f2`, snapshot branch `dev`, сохранён 2026-09-27. `tree.json` не помечен truncated и содержит 21 821 path entry (20 970 blobs); repository API metadata и radar context сверены отдельно.
- **Охват:** прочитаны README, CHANGELOG, LICENSE, корневой и app-module Gradle build files, конфигурация Turbo UI, forwarding, Ayu deleted-message storage/media, updater/network, font и bookmark helpers и выбранные интеграционные call-sites. SHA-256 локально совпал со всеми 52 файлами, которые удалось сохранить из raw snapshot. Код, Gradle, тесты, APK и приложение не запускались и не собирались.
- **Вердикт:** `accepted-with-gaps`.
- **Итог:** 31 уникальный fact ID; в source page обновлены границы, build/storage details, review status и ссылка на этот отчёт.

## Независимое покрытие

Основа роли и version boundary перепроверены по `README.md`, `CHANGELOG.md`, `LICENSE`, `repository.json`, `snapshot.json`, `tree.json`, `radar-context.md` и `radar-urls.json`. Документационные statements отделены от кодовых; README не использовался как доказательство runtime-поведения.

Статически прочитаны Gradle-настройки `build.gradle` и `TMessagesProj/build.gradle`, а также `BuildVars.java`, `NekoSettingsActivity.java`, `TurboSettingsActivity.java`, `NaConfig.kt`, `NekoConfig.java` и конфигурационные cells. Проверялись `TURBO_BASE`, фактические SDK/NDK и Java/Kotlin targets, обязательные Telegram credentials, default values и видимость строк настроек.

Forwarding-покрытие: `ShareAlert.java`, `ForwardTextEdit.java`, `ProtectedForward.java`. Deleted-message и локальная история: `AyuSavePreferences.java`, `AyuMessagesController.java`, `AyuMessageUtils.java`, `AyuDatabase.java`, `DeletedMessageDao.java`, `DeletedMessage.java`, `AyuMessageBase.java`, `AyuViewDeleted.java`, `AyuQueues.java`; отдельно подтверждены user/dialog/topic/reply/group lookup shapes и поля Room entity.

Network/update-покрытие: `BaseRemoteHelper.java`, `UpdateHelper.java`, `ApkDownloader.java`. Media/audio: выбранные ветви `MediaController.java`, `SecretMediaViewer.java`, `AudioEnhance.kt`; UI context также сверялся по `ChatActivityEnterView.java`, `ChatActivity.java`, `DialogsActivity.java`, `PhotoViewer.java`, `MusicPlayerService.java`, `SettingsActivity.java`, `AppIconsSelectorCell.java`, `NekoAboutActivity.java`, `LaunchActivity.java` и связанным adapter/cell files. Font/bookmark-покрытие: `FontPickerActivity.java`, реальный `TypefaceHelper.java`, `BookmarkManagerActivity.java`, `BookmarksActivity.java`, `BookmarksHelper.kt`.

Raw manifest содержит три неуспешных первоначальных запроса по путям, отсутствующим в pinned tree: `TypefaceHelper.kt` вместо `TypefaceHelper.java`, `BookmarksHelper.kt` под `java` вместо `kotlin`, и `AppIconsSelectorCell.java` под `tw...settings` вместо `org/telegram/ui/Cells`. Идентификация сверена с `tree.json`; правильные файлы сохранены и прочитаны. Эти записи не считаются недоступностью реальных файлов проекта.

## Исправления сборщика

- Разведены документационная классификация Android-клиента и ограниченный inference об отсутствии ExteraGram/KPM contract в выбранных путях. В fact `nagramx-turbo-001` убрано неподтверждённое слияние «клиент / не plugin», а `nagramx-turbo-026` явно ограничен просмотренным срезом.
- `nagramx-turbo-006` уточнён: build property/environment/local.properties передаёт boolean в `BuildConfig`; просмотренный код доказывает скрытие forwarding/deleted/edit-history settings rows в base, но не исключение всех соответствующих реализаций из APK.
- Исправлена ошибка о том, что индексы якобы объявлены в DAO. `DeletedMessage` задаёт Room `@Index`, а `DeletedMessageDao` задаёт запросы; сохранено отдельно, что `userId` не равен локальному account-slot ID. Запросы вынесены в отдельный fact.
- У `nagramx-turbo-007` доказательство defaults перенесено на конфигурационные объявления в `NaConfig.kt`. У `nagramx-turbo-024` исправлена ссылка с CHANGELOG строки 14 на перечень Turbo settings в строке 19. У `nagramx-turbo-025` claim ограничен сведениями README строки 7, без неподкреплённого там ABI списка.
- `nagramx-turbo-018` уточняет, что `BaseRemoteHelper.load()` не принимает account ID, а controllers берутся из `UserConfig.selectedAccount`.
- `nagramx-turbo-020` уточнён до проверки начальной URL-строки, временного файла и переименования по окончании чтения. В source page отдельно указано, что redirect, фактическая проверка длины/hash и подписи в этом срезе не верифицировались; прежняя формулировка могла звучать как подтверждение полного защищённого origin/integrity.
- Добавлены pinned build constraints и credential guard: текущий snapshot прекращает Gradle configuration без собственного `TELEGRAM_APP_ID`/`TELEGRAM_APP_HASH` или при публичном API ID `6`. README setup остаётся docs, а проверка сборкой не заявляется.
- Покрытие дополнено `BookmarksHelper`: owner key/fallback, миграция прежних account-slot keys, нормализация ID и предел 30 закладок на dialog.

## Повторы и канонические темы

JSON содержит 31 уникальный ID; идентичные claims внутри фактов не оставлены. Параллельные записи о DAO queries и entity indexes имеют разные доказательства и остаются раздельными. `nagramx-turbo-001` и `nagramx-turbo-026` также различаются: первый фиксирует назначение проекта по README, второй — ограниченный negative-search inference.

В уже принятых фактах похожие темы — `official-sdk:settings-storage`, `official-sdk:ui-thread`, `official-sdk:account-client`, `official-sdk:notification-account`, `extcli:extcli-013`, а также storage/settings/threading recipes AltyLib — относятся к plugin APIs или другой реализации. Они не подтверждают внутренние Android contracts NagramXTurbo и не были склеены. Canonical topics для будущего synthesis: `build`, `storage`, `accounts`, `threading`, `network`, `media`, `ui`, `portability`, `distribution`. В source page повторения между обзорной таблицей, подробными facts и call-site таблицей — навигационные, а не дополнительные уникальные факты.

## Остаточные пробелы

- Snapshot — выборка 52 сохранённых файлов из полного дерева. Большая часть upstream Telegram, dependency и ресурсов не читалась построчно; граница соответствует перечисленным в source page собственным feature areas и интеграционным call-sites.
- `radar-urls.json` пуст, а дерево не содержит Git commit history. `pushed_at` из repository metadata от 2026-09-22 не позволяет установить, были ли после 26 августа собственные Turbo changes или только upstream sync/build/docs; radar assertion остаётся непроверенным.
- README/CHANGELOG перечисляют множество UI-функций share sheet, media viewer, icons, font import и base build. Код просмотрен по выбранным call-sites, но не трассировались все действия, обработка ошибок, UI states, font import/permissions, APK install/update/signing и runtime redirect behavior.
- Room migrations, удаление/очистка всей истории, полный lifecycle Ayu media/reactions/edits/last-seen и полная account isolation не проверялись. В частности, точная account scoping локальной БД требует дальнейшей проверки call-sites и схемы.
- Совместимость внутренних классов с PySDK/ExteraGram неизвестна; публичный plugin API в этом срезе не обнаружен, но отсутствие подобного кода во всём репозитории не утверждается.
- Источники и разрешения Android SDK/NDK, API credentials, сборка, install flow, networking, подпись артефактов и runtime behavior не проверялись запуском. Утверждения source inspection имеют статус `code`/`docs`/`inference`, не `runtime-verified`.

Снимок принят как полезное, привязанное к SHA статическое описание собственной архитектуры и интеграционных точек Nagram X Turbo. Открытые gaps перечислены; абсолютная полнота по непрочитанному upstream-коду не заявляется.
