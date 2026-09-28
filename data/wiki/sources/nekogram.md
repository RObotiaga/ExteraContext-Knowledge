---
type: source
source_id: nekogram
platform: Android
review_status: accepted-with-gaps
review: ../reviews/nekogram.md
date: 2026-09-28
---

# Nekogram

Источник: [Nekogram/Nekogram](https://github.com/Nekogram/Nekogram), основной репозиторий клиента Nekogram. Snapshot закреплён на `e924154e8d3b99a645b0521013ff9b501b28e8ce` (`main`, получен 2026-09-27). Ссылки ниже ведут на этот commit. Исходники и README прочитаны как данные; сборка и приложение не запускались.

## Роль и границы

Nekogram — Android-клиент Telegram, а не plugin SDK. В snapshot присутствуют клиентские внутренние классы с настройками, несколькими аккаунтами, remote helper и media streaming; это примеры реализации внутри форка. Нельзя считать их публичными либо совместимыми API ExteraGram/AyuGram. Radar характеризует последние изменения Nekogram преимущественно как UI/build fixes, но это только контекст радара, а не доказательство по выбранному commit.

## Покрытие

| Материал | Извлечено | Пропуски |
|---|---|---|
| `README.md`, `LICENSE`, `.gitmodules` | описание, заявленные upstream API manuals, сборка, лицензия, native/submodule границы | LICENSE загружена, но отдельный лицензионный анализ не делался; submodule исходники не входят в обзор |
| `NekoConfig.java`, `Extra.java`, `PasscodeHelper.java`, `AccountsHelper.java` | конфигурационный lifecycle, экспорт/импорт и auto-sync trigger, per-account локальная конфигурация, account selector и panic/passcode примеры | весь UI настроек и все feature call-sites не просмотрены |
| `CloudSettingsHelper.java`, `CloudStorageHelper.java`, `BaseRemoteHelper.java`, `ConfigHelper.java`, `UpdateHelper.java` | bot custom-method storage, inline-bot remote fetch/cache, account selection и callbacks | backend/bot implementation и сетевое поведение не проверялись |
| `MediaStreamingProvider.java`, `MediaStreamingServer.java` | read-only URI streaming, Android O+ proxy FD и loopback fallback/range requests | Android manifest/URI grants и runtime media players не проверялись |
| `Translator.java`, `TextWithEntitiesTranslator.java`, `DeepLOAuth.java`, `DeepLOAuthWebviewActivity.java`, `CronetHelper.java` | локальный async/cache API, entity-aware translation, OAuth/Cronet utility surface | внешний provider SDK и полные call-sites перевода не анализировались |
| `README.md`, `build.gradle`, `TMessagesProj/build.gradle`, `gradle.properties`, `settings.gradle`, `.github/workflows/build.yml`, `release.yml` | локальные credentials/config inputs, Android/native build, CI dependencies/secrets/artifacts/release | сборка не запускалась; достоверность и доступность секретов не проверялись |

Tree snapshot содержит 21 220 путей; выбранные файлы сверены через сохранённый tree/manifest. Обзор ограничен feature package и build entrypoints, не является построчным аудитом Telegram upstream.

## Технические наблюдения

### Конфигурация, аккаунты и локальная безопасность

`NekoConfig` — статический фасад над `SharedPreferences("nekoconfig")`. Инициализация вызывает `loadConfig(false)`, а загрузка синхронизируется и пропускается повторно после `configLoaded`, если не передан `force=true`. Методы `toggle*`/`set*` изменяют поле и сохраняют значение по ключу. После чтения конфигурации listener отслеживает дальнейшие изменения, отправляет analytics event и запускает cloud auto-sync debounce. Это полезный образец для простого локального settings store; для плагина нужен собственный namespaced storage и явный lifecycle, а не зависимость от внутреннего класса Nekogram.

`exportConfigs()` сериализует только разрешённый набор известных ключей, присутствующих в prefs; `importConfigs()` сначала очищает prefs и восстанавливает поддержанные типизированные поля. Среди экспортируемых строк есть `cfAccountID`/`cfApiToken` и translation-provider значения. Облачная синхронизация передаёт этот JSON в Telegram bot custom method под ключом `neko_settings`. Следствие для собственных плагинов: экспортировать чувствительные токены вместе с обычными настройками и автоматически синхронизировать их следует только при осознанном выборе пользователя; не предполагать, что экспорт конфигурации не содержит секретов.

`CloudSettingsHelper.doAutoSync()` отменяет ранее запланированный UI runnable и планирует запись через 1200 мс. Sync берёт `UserConfig.selectedAccount`; `CloudStorageHelper` создаётся отдельно на каждый индекс аккаунта и наследуется от `AccountInstance`. Запросы идут через `TL_bots.invokeWebViewCustomMethod`, получают bot/user через resolver при первом обращении и возвращают callback на UI thread. Это конкретный клиентский образец debounced async operation с account scope, но backend-хранилище, доступность bot API и конфиденциальность данных зависят от внешней стороны.

Конфигурационный import проверяет, что JSON — объект, затем очищает весь prefs namespace перед чтением известных полей. Неизвестные поля теряются; импорт должен трактоваться как замена поддерживаемой конфигурации, а не merge. Изменения собираются в одном editor и применяются после чтения известных полей. Для переносимого формата всё равно полезно проверять типы и версию payload до очистки/записи.

`PasscodeHelper` хранит хеш и соль в обычном private SharedPreferences. Он формирует `SHA-256(salt16 || UTF8(passcode) || salt16)`, использует 16 случайных байт соли, а контроль скрытия аккаунта — отдельные prefs-флаги. Это пример account-specific gating/panic flow, не образец современного password KDF/keystore: source не показывает аппаратно защищённый секрет или key stretching. Специальный panic-код при совпадении отключает разрешённые аккаунты через `performLogout(1)`.

`AccountsHelper.fillAccountSelectorMenu(...)` строит список только из активированных и не скрытых аккаунтов; он сортируется по `loginTime`. Выбор подменяет аккаунт через `LaunchActivity.switchToAccount(account, true)`, а long-press используется для drag reorder при текущем аккаунте/планшете. Для plugin call sites нельзя кэшировать `UserConfig.selectedAccount` надолго: идентификатор текущего аккаунта может смениться после действия UI.

### Внешние вызовы, сеть и медиа

`BaseRemoteHelper` запрашивает данные у helper inline bot только если настроен bot и выбранный аккаунт активен. Запрос составляется из метода, параметров и `VERSION_CODE`, build type, системного языка, MCC и `pushString`; полученные тексты кешируются в shared preferences на сутки. Для собственного remote API полезны TTL cache и single-flight `loading` guard, а состав `getRequestExtra()` — пример данных, которые могут покинуть устройство; не копировать поля автоматически.

`MediaStreamingProvider.openFile(uri, mode)` допускает только `"r"` и на Android O+ открывает `ProxyFileDescriptor` read-only. URI преобразуется из `tg` в `content` с authority `<applicationId>.streaming`, а Intent получает `FLAG_GRANT_READ_URI_PERMISSION`. Ниже Android O или при `NekoConfig.forceHttpStreaming` используется singleton NanoHTTPD на `127.0.0.1:61579`; сервер хранит не более шести путей в LRU map и поддерживает byte-range ответы. Это pattern передачи media через OS/player интерфейс, не готовая plugin API. Любой свой локальный streaming server нужно удерживать на loopback, ограничивать lifetime/keys и соблюдать URI permission.

`Translator` использует общий cached thread pool и LRU translation cache ёмкостью 200 ключей. Ключ учитывает текст, hash entities, целевой язык, provider и keepFormatting. Публичный `translate(...)` возвращает асинхронный callback, а входная модель сохраняет Telegram `MessageEntity`; при переводе текст с форматированием надо обрабатывать entity offsets вместе с текстом, а не переводить только строку. Конкретный интерфейс `ITranslator` package-private и не является SDK.

### Build и release

README требует рекурсивный shallow clone, заполнение `local.properties` release keystore, две Firebase Android-конфигурации и `google-services.json`, открытие проекта в Android Studio (не импорт), и значения `Extra.java`. Build workflow использует JDK 21, Android SDK/build-tools 37, NDK 27.3 и CMake 3.22.1, рекурсивные submodules, signing/API/helper-bot/Sentry/maps/Firebase secrets и сборки `assembleRelease`, `bundlePlay`, Sentry source upload. Release workflow запускается по тегам `v*` или вручную и передаёт артефакты в GitHub Release и Telegram uploader. Это требования сборки клиента, не среда/контракт плагина.

## Вызовы и внутренние точки

| Класс/метод | Контракт/назначение | Lifecycle / thread / account | Evidence |
|---|---|---|---|
| `NekoConfig.loadConfig(boolean)` | грузит поля из `nekoconfig` | static init; synchronized; глобальная конфигурация клиента | [NekoConfig.java#L154-L185](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/NekoConfig.java#L154-L185) |
| `NekoConfig.exportConfigs()` / `importConfigs(String)` | сериализация allowlist и восстановление; import очищает namespace | синхронный JSON/prefs | [NekoConfig.java#L265-L320](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/NekoConfig.java#L265-L320), [#L518-L570](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/NekoConfig.java#L518-L570) |
| `CloudSettingsHelper.doAutoSync()` | отменяет и откладывает sync на 1.2 с | UI runnable; selected account в момент sync | [CloudSettingsHelper.java#L158-L180](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/CloudSettingsHelper.java#L158-L180) |
| `CloudSettingsHelper.syncToCloud()` / `restoreFromCloud()` | сохраняет/восстанавливает export JSON, timestamps | `CloudStorageHelper(selectedAccount)`; callbacks | [CloudSettingsHelper.java#L166-L211](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/CloudSettingsHelper.java#L166-L211) |
| `CloudSettingsHelper.encodeConfig/decodeConfig` | gzip + Base64 без padding/wrap с version prefix `0`; принимает также raw JSON | статические утилиты | [CloudSettingsHelper.java#L220-L252](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/CloudSettingsHelper.java#L220-L252) |
| `CloudStorageHelper.getInstance(int)` | lazy singleton на каждый индекс аккаунта | account-scoped `AccountInstance` | [CloudStorageHelper.java#L21-L44](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/CloudStorageHelper.java#L21-L44) |
| `CloudStorageHelper.setItem/getItem/getItems/remove*` | key/value CRUD через bot custom method | RPC callback переводится на UI thread | [CloudStorageHelper.java#L46-L128](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/CloudStorageHelper.java#L46-L128) |
| `BaseRemoteHelper.load(Delegate)` | inline bot query, TTL prefs cache и одновременный запрос guard | выбранный активный аккаунт; callback из `InlineBotHelper` | [BaseRemoteHelper.java#L75-L143](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/remote/BaseRemoteHelper.java#L75-L143) |
| `PasscodeHelper.setPasscodeForAccount/checkPasscode` | salt+SHA-256, проверка account code и panic logout | индексированный аккаунт; LaunchActivity для переключения | [PasscodeHelper.java#L21-L68](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/PasscodeHelper.java#L21-L68), [#L98-L118](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/PasscodeHelper.java#L98-L118) |
| `AccountsHelper.fillAccountSelectorMenu(...)` | меню активных видимых аккаунтов и switch/drag | FragmentPreviewWindow; selected account | [AccountsHelper.java#L41-L64](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/AccountsHelper.java#L41-L64), [#L120-L154](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/AccountsHelper.java#L120-L154) |
| `MediaStreamingProvider.openForStreaming(...)` | Android O+ content URI proxy; fallback HTTP mode | Activity result, read grant; supplied account id | [MediaStreamingProvider.java#L141-L184](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/streaming/MediaStreamingProvider.java#L141-L184) |
| `MediaStreamingServer.addFile/serve(...)` | loopback stream, LRU route, byte range | singleton local server, port 61579 | [MediaStreamingServer.java#L24-L68](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/streaming/MediaStreamingServer.java#L24-L68), [#L90-L119](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/streaming/MediaStreamingServer.java#L90-L119) |
| `Translator.translate(...)` | entity-aware async translation | cached thread pool; callback; no account id in API | [Translator.java#L61-L80](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/translator/Translator.java#L61-L80), [#L313-L335](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/translator/Translator.java#L313-L335) |
| `TelegramTranslator.translate(...)` | Telegram RPC-backed provider via internal translator interface | selected account; async RPC/future | [TelegramTranslator.java#L15-L55](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/translator/TelegramTranslator.java#L15-L55) |
| `InlineBotHelper.query(...)` | per-account inline query, cached result path and network fallback | account-scoped BaseController; result callback on UI thread | [InlineBotHelper.java#L39-L86](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/InlineBotHelper.java#L39-L86) |
| `WebAppHelper.processBotEvents(...)` | JSON get_config/set_config bridge for one trust flag | BotWebViewContainer delegate callback; SharedPreferences | [WebAppHelper.java#L27-L52](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/WebAppHelper.java#L27-L52) |
| `MessageFilterHelper.shouldBlockMessage/checkBlockedEntities(...)` | account-scoped blocked sender/forwarder check; spoiler and collapsed quote entities | current account from MessageObject | [MessageFilterHelper.java#L13-L55](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/MessageFilterHelper.java#L13-L55) |
| `CronetHelper.init/createEngine(...)` | async provider install, then HTTP engine setup | readiness via `isAvailable()`; failure logged | [CronetHelper.java#L16-L51](https://github.com/Nekogram/Nekogram/blob/e924154e8d3b99a645b0521013ff9b501b28e8ce/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/CronetHelper.java#L16-L51) |

## Практические рецепты и ограничения

* Настройки: хранить параметры плагина под своим namespace; задавать типизированные defaults; держать import allowlist; валидировать полный payload до очистки/записи; отделять секреты от обычного export/sync.
* Account-aware действия: принимать account id из текущего callback/UI контекста или перепроверять `selectedAccount` непосредственно перед обращением к `MessagesController`/`ConnectionsManager`; не захватывать его в долгоживущем singleton.
* Сетевые операции: повторить полезную структуру remote helper — TTL cache, один in-flight запрос, callback/error на главный поток; передавать на сервер только нужный контекст и документировать поля.
* Медиа: если нужна передача player через content URI, выдавать read grant и поддерживать API fallback; не расширять сетевой listener за loopback без аутентификации и контроля доступа.
* Build/release: клиентская сборка требует private per-maintainer keys/configuration и recursive native submodules; не использовать release workflow как рецепт сборки стороннего plugin.

Кроме общих settings/account примеров, отобраны полезные integration points: inline bot network/cache, ограниченный Web App config bridge, Cronet readiness и privacy-aware message entity filtering. В source tree не найдено отдельной plugin engine или публичного plugin lifecycle/API surface — это ограниченный вывод по tree и README (`inference`), не утверждение о совместимости всех Nekogram distributions. Отсутствуют runtime/device verification, анализ всех feature UI и полного caller graph. README ссылается на официальные Telegram API/MTProto manuals, но они не входят в этот snapshot и здесь не пересказывались.
