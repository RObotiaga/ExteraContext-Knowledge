---
type: code
source_id: ayugram4a
platform: Android
review_status: accepted-with-gaps
review: ../reviews/ayugram4a.md
reviewer: /root/review_ayugram4a
review_model: gpt-6-luna
accepted_facts: 41
date: 2026-09-28
---

# AyuGram4A (Android)

- Репозиторий: [BRYCE00182/AyuGram4A](https://github.com/BRYCE00182/AyuGram4A)
- Закреплённый HEAD: [`0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8`](https://github.com/BRYCE00182/AyuGram4A/tree/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8), ветка `rewrite`; GitHub API на 2026-09-28 подтвердил тот же SHA.
- Лицензия по метаданным GitHub: GPL-2.0; перед переносом кода сверяйте условия проекта и лицензии.
- `TMessagesProj` — Android application module: compile/target SDK 33, min SDK 21, Java 11. Это настройки клиентского приложения, не plugin SDK.
- Роль: производный Telegram Android-клиент, полезный как пример того, как встраивать пользовательские функции в крупный fork, хранить локальную историю и привязывать их к UI, аккаунту и сетевому lifecycle.
- Это не документация публичного API плагинов ExteraGram. Найденные Ayu-классы вызываются статически из fork-классов `org.telegram.*`; эти call-site’ы являются внутренними точками модификации клиента. Для стороннего плагина нужен отдельный контракт host SDK.
- Snapshot/tree и скачанные файлы лежат в `raw/ayugram4a/`; список файлов и SHA-256 — `raw/ayugram4a/file-manifest.json`. Файлы получены с URL, содержащими закреплённый commit SHA. В снимок вошло 71 доказательное файла без ошибок загрузки.

## Покрытие

| Прочитанные пути | Извлечено | Ограничение |
|---|---|---|
| `README.md`, `LICENSE`, `repository.json`, `snapshot.json`, `tree.json`, `radar-context.md`, `radar-urls.json` | Идентичность fork, заявленные функции, лицензия, commit и контекст радара | README — документация, не подтверждение runtime-поведения; исторических commit URL в `radar-urls.json` нет |
| Выбранный пакет `TMessagesProj/src/main/java/com/radolyn/ayugram/` целиком (52 Java-файла: config/utils, filters, forwarder, message history, Room entity/DAO/database, sync, settings UI, async waiters) | Реализации локальных предпочтений, regex-фильтров, ghost state, истории сообщений, AyuSync и их внутренние методы | Это не весь Telegram upstream и не проверка совместимости SDK |
| `ApplicationLoader.java`, `UserConfig.java`, `MessagesStorage.java`, `SendMessagesHelper.java`, `MessageObject.java`, `SharedConfig.java`, `LaunchActivity.java`, `ChatActivity.java`, `ChatMessageCell.java` | Выбранные места app init, account state, storage, пересылки, drawer, chat-list, message-history и presentation integration | Core-файлы большие; изучались выбранные Ayu call-site’ы и непосредственно связанные участки |
| `TMessagesProj/build.gradle`, root `build.gradle`, `gradle.properties`, `TMessagesProj/google-services.json`, `.github/workflows/release.yml` | Сборочная конфигурация, секрето-/сервисно-зависимые входы и CI-файл из последнего commit | Сборка и workflow не запускались |

Не загружался весь Telegram upstream и не выполнялись приложение, build или tests. В runtime приложения ничего не проверялось.

## Основные выводы

### Встраивание в клиент и граница plugin API

README описывает AyuGram4A как fork exteraGram с патчами Telegraher и перечисляет ghost mode, историю сообщений, message filters и AyuSync. Статические исходники подтверждают, что по крайней мере эти механизмы реализованы непосредственно в клиенте: например, `LaunchActivity` вызывает `AyuConfig.toggleGhostMode()`, `ChatActivity` вызывает `AyuFilter.isFiltered(...)`, `ApplicationLoader` запускает `AyuSyncController.create()`, а `MessagesStorage` вызывает `AyuMessagesController`. Это полезные архитектурные примеры интеграции в fork, но не регистрации расширений из внешнего плагина.

Есть заметное ограничение исходного набора. В секции сборки README просит реализовать `AyuMessageUtils` и `AyuHistoryHook`; в `ChatActivity` `AyuHistoryHook` также импортирован и вызывается. Поиск дерева закреплённого снимка не нашёл файлов ни с одним из этих имён (папка `proprietary` в Java package не содержит отслеживаемого файла). Поэтому README подтверждает только заявленную необходимость, а не предоставляет контракт либо реализацию этих классов. Сборка этого снимка здесь не проверялась.

### Настройки и фильтрация сообщений

`AyuConfig` статически загружает предпочтения из private `SharedPreferences` (`ayuconfig`) и бережёт однократную загрузку synchronized-блокировкой. `setGhostMode` централизованно меняет четыре сетевых поведенческих флага и сохраняет их через `apply()`. `isGhostModeActive` проверяет точную комбинацию флагов, поэтому он может возвращать `false` при частичной конфигурации, даже если некоторые ghost-настройки включены.

Regex-правила сериализуются Gson в одну JSON-строку preference `regexFilters`. `AyuFilter.rebuildCache()` компилирует шаблоны с `MULTILINE` и опциональным `CASE_INSENSITIVE`; сопоставление использует `Matcher.find()`. Кеш индексируется парой dialog ID/message ID и разделяет результат между элементами сгруппированного сообщения. `ChatActivity` решает фильтр в своём adapter path, нормализуя группу к primary message, а для скрытого элемента возвращает внутренний sentinel `-1000`. Конкретный sentinel и этот метод не следует считать переносимым API.

### Локальная история сообщений

`AyuDatabase` — Room database версии 21 с DAO для `EditedMessage` и `DeletedMessage`. `AyuData` строит её под именем `ayu-data`; текущая реализация явно включает `allowMainThreadQueries()` и `fallbackToDestructiveMigration()`. Это показывает схему реализации, одновременно предупреждая о возможной потере локальных записей при несовместимой миграции и о риске тяжёлых операций на UI thread.

DAO различает ключи пользователя, диалога, topic и сообщения. `EditedMessageDao` выдаёт полный список ревизий в хронологическом порядке, а последнюю ревизию — отдельно. `DeletedMessageDao` транзакционно восстанавливает связанный объект, выбирает диапазон по topic/message ID и поддерживает группировку media по `groupedId`. `AyuMessagesController` проверяет policy сохранения перед обработкой; для удаления также проверяет существование записи, чтобы не дублировать её.

Интеграция происходит на уровне Telegram storage: в `MessagesStorage` обнаружение редакции текста или media вызывает `onMessageEdited(...)`; путь потери media сохраняет старое сообщение через `onMessageEditedForce(...)`, если включена история. `ChatActivity` добавляет пункт меню истории и использует deleted-state policy при применении событий удаления. Это плотная fork-интеграция с локальными таблицами Telegram, а не обособленный extension seam.

### Потоки, аккаунты и сеть AyuSync

`ApplicationLoader` запускает AyuSync после базового создания аккаунтов и singleton-контроллеров. Контроллер выделяет `DispatchQueue("AyuSyncController")`; когда sync выключен, ставится empty controller и обнуляется WebSocket instance. Account mapping хранится как `userId -> accountId`, а события для неизвестных user ID отбрасываются.

WebSocket endpoint `/sync/ws/v1` и HTTP пути (`/user/v1`, `/sync/register/v1`, `/sync/force/v1`) строятся в `AyuSyncConfig`; `useSecureConnection` переключает схемы `ws/http` на `wss/https`. Handshake содержит auth token и идентификаторы приложения/устройства, соединение настраивает timeout и автоматический reconnect. Полученный JSON диспетчеризуется по `type` на `sync_force`, `sync_batch` и `sync_read`; неизвестный тип логируется и игнорируется. `sync_read` переносит `userId`, `dialogId`, `untilId`, `unread`, а принимающая сторона проверяет текущее число непрочитанных до локального изменения.

В `EasyWaiter` показан конкретный шаблон observer lifecycle: подписка/отписка account-scoped `NotificationCenter` выполняется через UI looper, а фоновой вызывающий поток синхронизируется latch. `await()` блокирует до `unsubscribe()`, не задаёт timeout и поэтому может ждать бесконечно, если ожидаемое событие не наступило; его нельзя вызывать из UI потока. В `SendMessagesHelper` некоторые Ayu forwarding ветви запускаются через `new Thread`; они возвращают `0` немедленно, а значит caller-visible return value не подтверждает завершение пересылки. Это детали реализации именно данного клиента.

### Особая пересылка сообщений

`AyuForwarder.intelligentForward(...)` разбивает выделение на последовательные обычные и Ayu-особые батчи: обычные проходят через стандартный `SendMessagesHelper` (с ожиданием результата), а записи с флагами `ayuDeleted`/`ayuNoforwards` — через локальную реконструкцию. Этот путь заранее скачивает разрешённые медиа, заново отправляет текст, документы и фото от текущего аккаунта, восстанавливает границы альбомов через `groupId`/`final` и сохраняет caption/entities. Код оставляет TODO для replies, не имеет принудительной загрузки из cache при отсутствующем файле и пропускает неподдерживаемые типы; это частный алгоритм форка, не переносимый API и не рекомендация обходить ограничения.

`AyuEasyUtils` реализует синхронные обёртки над асинхронными Telegram-событиями: подписывает waiter до запуска UI-потока отправки/загрузки, связывает ожидаемую отправку с dialog ID, а для одиночной загрузки ждёт upload completion. Это опирается на внутренние `NotificationCenter`, `FileLoader` и `SendMessagesHelper`; waiter без timeout/отмены делает такой вызов потенциально неограниченно блокирующим.

## Вызовы и точки интеграции

| Модуль/класс | Сигнатура или call-site | Назначение и lifecycle/thread/account | Доказательство |
|---|---|---|---|
| `AyuConfig` | `loadConfig()`; `setGhostMode(boolean)`; `saveDeletedMessageFor(int,long)` | Static app preferences; первая загрузка синхронизирована, policy учитывает account/dialog и настройку bot | [AyuConfig.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/AyuConfig.java#L63-L169) |
| `AyuFilter` → `ChatActivity` | `isFiltered(MessageObject, GroupedMessages)` | UI adapter path; per-dialog/message cache, group primary object; внутренний sentinel скрытия | [AyuFilter.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/AyuFilter.java#L25-L97), [ChatActivity.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java#L28971-L28986) |
| `AyuData` / `AyuDatabase` | `create()`, `getEditedMessageDao()`, `getDeletedMessageDao()` | Static Room handles; миграции destructive, main-thread queries разрешены | [AyuData.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/database/AyuData.java#L18-L53), [AyuDatabase.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/database/AyuDatabase.java#L20-L28) |
| `MessagesStorage` → `AyuMessagesController` | `onMessageEdited(...)`, `onMessageEditedForce(...)` | Storage processing path; controller фильтрует по preference и сохраняет ревизии | [MessagesStorage.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/org/telegram/messenger/MessagesStorage.java#L4261-L4267) |
| `ApplicationLoader` → `AyuSyncController` | `AyuSyncController.create()` | После основного startup; создаёт queue/controller и начинает connect либо отключает sync | [ApplicationLoader.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/org/telegram/messenger/ApplicationLoader.java#L231-L235), [AyuSyncController.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/sync/AyuSyncController.java#L32-L71) |
| `AyuSyncWebSocketClient` → `AyuSyncController` | `onTextReceived(String)` → `invokeHandler(JsonObject)` | WebSocket worker receives JSON; dispatch is account-scoped by `userId` and typed by `type` | [AyuSyncWebSocketClient.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/sync/AyuSyncWebSocketClient.java#L101-L110), [AyuSyncController.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/sync/AyuSyncController.java#L322-L352) |
| `EasyWaiter` | `subscribe()` / `unsubscribe()` / `await()` | Account NotificationCenter observer lifecycle bridged to UI looper with latch | [EasyWaiter.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/easy/EasyWaiter.java#L23-L95) |
| `AyuForwarder` → `AyuEasyUtils` | `intelligentForward(...)`; `forwardMessages(...)` | Смешанные выделения делятся на обычные форварды и Ayu-особые повторные отправки; медиа и album group обрабатываются через client internals | [AyuForwarder.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/AyuForwarder.java#L47-L180), [AyuEasyUtils.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/easy/AyuEasyUtils.java#L19-L249) |
| `LaunchActivity` | drawer item → `AyuConfig.toggleGhostMode()` | App-specific menu integration; hard-coded ID from AyuConstants | [LaunchActivity.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java#L637-L653) |
| `LaunchActivity` → `AyuCustomHandlers` | `handleAyu(BaseFragment)` / `handleXiaomi(BaseFragment)` | Custom `tg:ayu`/`tg:xiaomi` URL routing passes active fragment to an app-local handler; uses Bulletin UI and, on the MIUI branch, `ACTION_DELETE` for this package | [LaunchActivity.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java#L2663-L2672), [AyuCustomHandlers.java](https://github.com/BRYCE00182/AyuGram4A/blob/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8/TMessagesProj/src/main/java/com/radolyn/ayugram/AyuCustomHandlers.java#L19-L43) |

## Приёмы, пригодные как образцы

1. Для локальных функций храните пользовательские настройки централизованно, устанавливайте явные defaults и инвалидируйте производные кеши при смене правил.
2. Для message history отделяйте таблицы/DAO от точек обнаружения изменений; в ключ включайте account/user, dialog, topic и message, когда эти области независимы.
3. На UI path фильтруйте группу последовательно и решайте результат для primary элемента, чтобы не показывать только часть альбома.
4. В multi-account сетевой функции отделяйте серверную user identity от локального account index и отклоняйте события без разрешённого mapping.
5. Для observer-ожиданий явно описывайте thread, момент снятия observer, блокирующее поведение и timeout/cancel strategy.
6. Переносите только алгоритм/модель, если это применимо. Доступ к `MessagesStorage`, `ChatActivity`, `LaunchActivity`, `DispatchQueue` и внутренним Telegram TL API требует fork-level модификации или подтверждённой host API.

## Радар и противоречия

В радаре строка 1469 говорит, что у `BRYCE00182/AyuGram4A` были только изменения `release.yml`, без пользовательских функций. У закреплённого HEAD commit сообщение `Update release.yml`, а GitHub commit metadata показывает единственный изменённый путь `.github/workflows/release.yml`. Это подтверждает commit-level часть утверждения; радарный пересказ про все изменения за целый день шире одного commit и остаётся `secondary`. В `radar-urls.json` исторических commit URL нет. Дата commit — 2023-09-09 23:31 UTC, поэтому её нельзя без оговорки приравнять к календарному «9 сентября» в другом часовом поясе.

README рекламирует историю сообщений и перечисляет AyuHistoryHook/AyuMessageUtils как необходимые для сборки собственного fork, но snapshot не содержит их исходников. Это ограничение покрытия исходника; README-контракт не используется здесь как подтверждённая сигнатура.

## Открытые ограничения

- Нет runtime проверки, сборки или тестов; функциональная работа клиента не подтверждена этим ingest.
- Два README-упомянутых класса отсутствуют в закреплённом дереве; один вызывается из `ChatActivity`.
- Большие core-классы изучены выборочно по Ayu call-site’ам; полный upstream-поведенческий контракт и совместимость по версиям не исследовались.
- AyuSync server/API здесь изучен только со стороны Android клиента; backend-контракт отдельно не сверялся.
- Раздел `AyuGram proprietary` содержит вызовы недоступной реализации; детали его поведения остаются неизвестны.
