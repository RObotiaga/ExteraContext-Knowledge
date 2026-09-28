---
type: source
source_id: nullgram
platform: Android
review_status: accepted-with-gaps
review: ../reviews/nullgram.md
date: 2026-09-28
---

# Nullgram: tcp2ws, конфигурация и интеграция функций в Android-клиент

- Репозиторий: [qwq233/Nullgram](https://github.com/qwq233/Nullgram)
- Закреплённый snapshot: `b3d4f45e1ebd1a15576b46f87172ce076cf390f1`, ветка `master`, снят `2026-09-27T15:57:17Z`; ссылки на исходники ниже закреплены на этом SHA.
- Лицензия репозитория по GitHub и `LICENSE`: GPL-2.0. `libs/tcp2ws/README.txt` отдельно указывает происхождение части SOCKS-кода из декомпилированного Nekogram и java-socks-proxy-server (автор bbottema, Apache-2.0). Перед повторным использованием проверьте provenance, LICENSE и NOTICE отдельных файлов.
- Роль: клиент-донор практик Android-интеграции — изолированный transport-модуль, UI/config wiring, typed preferences и provider strategy. Это Telegram-клиент, а не SDK/хост плагинов: изученные внутренние классы не объявляются публичным plugin API или подтверждёнными seams ExteraGram/AyuGram.
- Проверка: чтение закреплённых исходников и документации; приложение, сборка и тесты не запускались, runtime-поведение не подтверждено.

## Покрытие

| Прочитано в snapshot | Что извлечено | Границы и пропуски |
|---|---|---|
| `snapshot.json`, `tree.json`, `repository.json`, `radar-context.md`, `radar-urls.json`, `README.md`, `README_CN.md`, `README_JA.md`, `LICENSE` | SHA, метаданные, заявления README, лицензия и проверяемая формулировка радара | `radar-urls.json` пуст; исторических ссылок для проверки нет. README — docs, не доказательство runtime. |
| `docs/CONTRIBUTING.md`, `.github/workflows/ci.yml`, `.github/workflows/pr.yml`, `settings.gradle.kts`, `TMessagesProj/build.gradle.kts`, `libs/tcp2ws/build.gradle.kts`, `gradle/libs.versions.toml` | Правила вклада, модули/зависимость tcp2ws, статическая CI-конфигурация | CI и Gradle не запускались; оценивалась только конфигурация файлов. |
| `libs/tcp2ws/README.txt`, `LICENSE-2.0.txt`, `NOTICE.txt`, `ProxyHandler.java`, `Socks4Impl.java`, `Socks5Impl.java`, `SocksConstants.java`, `Utils.java`, `tcp2wsServer.java` | SOCKS listener, WebSocket transport, relay, протоколы и retry | Не проверялись сеть, производительность, безопасность, полнота SOCKS или корректная остановка listener. |
| `WebSocketHelper.kt`, `WsSettingsActivity.java`, `ConfigManager.kt`, `Defines.kt`, `Annotations.kt`, `libs/ksp/.../ConfigSwitch.kt`, `ConnectionsHelper.kt`, `CloudStorage.kt` | Подключение transport к настройкам клиента, config keys и генератор, per-account вызовы Telegram API | Внутренняя реализация Nullgram; callback/thread/lifecycle host app отдельно не тестировался. CloudStorage зависит от Telegram-бота. |
| `BaseTranslator.kt`, `TranslateHelper.kt`, `GoogleTranslator.kt`, `BottomBuilder.kt`, `PopupBuilder.kt`, `GeneralSettingActivity.java`, `MainSettingActivity.java` | Абстракция translation provider, HTTP client, coroutine/error path и UI wiring | Не все provider implementations и экраны перечислены; сеть и поведение UI не проверялись. |

`tree.json` не усечён (30 706 entries, включая директории и файлы). Построчное чтение всего Telegram-клиента не выполнялось; срез ограничен перечисленными feature paths. В изученных файлах нет plugin SDK: README описывает third-party Telegram app. Это характеристика выбранного материала, не доказательство отсутствия плагинных интеграций во всём репозитории.

## Технические факты

### tcp2ws и сеть

`settings.gradle.kts` включает `:libs:tcp2ws`; Android-модуль подключает его через `implementation(project(":libs:tcp2ws"))`. У библиотеки собственный `java`/`kotlin("jvm")` Gradle-модуль с `nv-websocket-client:2.14`. Это пример разрезания transport-реализации на модуль, но не plugin API.

`WebSocketHelper.getSocksPort(port)` хранит singleton состояние, выбирает заданный или временно свободный порт, настраивает `tcp2wsServer` через `setCdnDomain`, `setTls`, `setUserAgent`, `setConnHash` и вызывает `start(port)` один раз. Если явный порт не сработал, код повторяет попытку с `-1` для выбора ephemeral port; при второй ошибке возвращает `-1`. `wsReloadConfig()` обновляет поля созданного server object, но не перезапускает listener в просмотренном коде.

`tcp2wsServer.start(int)` требует CDN mapping, открывает локальный `ServerSocket`, задаёт accept timeout 200 ms и запускает отдельный listener thread; каждый принятый socket обслуживает новый `Thread(new ProxyHandler(...))`. `stop()` только выставляет `stopping = true`: listener увидит флаг после очередного timeout и закроет socket. Здесь не показаны join, закрытие активных сессий или ограничение thread pool; конкретный call-site `stop()` не найден в срезе.

`ProxyHandler` выбирает SOCKS4 или SOCKS5 по первому байту. CONNECT проходит connect → MTProto handshake processing → relay. UDP dispatch активен, но `Socks4Impl.udp()` прямо отказывает; UDP association реализован только в наследнике SOCKS5 через `DatagramSocket`. Для BIND вызов `comm.bind()` закомментирован, хотя ветка продолжает relay, поэтому работающего BIND handshake код не показывает. Адреса также ограничены: SOCKS5 command parser отклоняет ATYP `0x03` (domain name), несмотря на отдельную domain ветку в `calcInetAddress`; для ATYP `0x04` вызывается `Inet4Address.getByAddress` с 16 байтами, а исключение преобразуется в `null`. По статическому анализу это не подтверждает IPv6 поддержку. SOCKS4 разбирает только 4-byte address. Эти ограничения не позволяют заявлять полную SOCKS4/5 совместимость.

WebSocket открывается как `ws://<host>/api` или `wss://<host>/api`; добавляются listener binary messages/disconnect, extension `permessage-deflate`, protocol `binary` и заголовки `User-Agent`/`Conn-Hash`. Ошибки, сообщение которых содержит `520`, повторяются максимум 10 раз; другие ошибки прекращают цикл. Открытые сокеты переиспользуются из `inactiveWs`, закрытые удаляются и получают close. Это transport-техника Nullgram, не общий сетевой API.

Радар упоминает tcp2ws в разделе находок NiagramX. Проверенный здесь факт уже: закреплённый Nullgram содержит `libs/tcp2ws` и использует его из `WebSocketHelper`. Поскольку `radar-urls.json` пуст, этим snapshot нельзя подтвердить дату/происхождение NiagramX изменения или приоритет авторства.

### Конфигурация и provider strategy

`ConfigManager` — Kotlin singleton над `SharedPreferences("globalConfig", MODE_PRIVATE)` с typed getters/defaults и setters; записи синхронизируются на preferences, ловят/логируют исключения и используют `apply()`. Для Java вызовов применён `@JvmStatic`. Деталь поведения: `putString` при пустой строке сначала удаляет ключ, затем в том же вызове записывает пустую строку; `getStringSetOrDefault` при исключении возвращает пустой set.

`Defines` централизует keys и defaults через `BooleanConfig`, `IntConfig` и `StringConfig`. KSP processor создаёт `top.qwq2333.gen.Config` с accessors, связывающими эти объявления с `ConfigManager` и `Defines`. Аннотация `FloatConfig` объявлена в `Annotations.kt`, однако просмотренный processor не ищет её и не генерирует Float accessors. Значит, объявленная аннотация сама по себе не означает поддержки типа генератором.

`WsSettingsActivity` показывает конкретный UI паттерн: экран списка даёт выбор встроенного/custom provider, а custom host редактируется в `AlertDialog`. По подтверждению сохраняется host, переключается provider, вызывается `wsReloadConfig()` и обновляются затронутые строки через `notifyItemChanged`. Это экран Nullgram, не plugin settings API.

`BaseTranslator` задаёт прикладной provider contract через `suspend translateText(text, from, to)` и `getTargetLanguages()`, с переопределяемым language-code conversion. Защищённое поле базового класса создаёт Ktor `HttpClient(OkHttp)` с JSON content negotiation, cookies, UTF-8 и GBK response fallback; базовый класс кэширует успешные результаты в `LruCache` вместимостью 200 по паре source object/target language. Для строк source object является текстом; `translate` также принимает poll objects. `TranslateHelper` выбирает provider по enum, запускает UI orchestration на Main и переводит перевод в IO; HTTP 429 превращается в отдельную ошибку UI. Это образец strategy внутри приложения, loader/registration API отсюда не следует.

### Account и cloud requests

`ConnectionsHelper(instance)` наследует `AccountInstance(instance)`, singleton массив создаётся по `UserConfig.MAX_ACCOUNT_COUNT`. `sendRequestAndDo(req, flags, action)` отправляет `TLObject` через account-specific `connectionsManager`, ждёт callback в `withContext(Dispatchers.IO)` через `CountDownLatch.await()` и вызывает action там же. В просмотренном методе нет timeout или cancellation bridge для latch; без дополнительной защиты ожидание может зависнуть.

`CloudStorage(instance)` тоже account-scoped. Он вызывает `TL_bots.invokeWebViewCustomMethod()` с методами `getStorageValues`, `saveStorageValue`, `deleteStorageValues`, `getStorageKeys` и сериализует `KeyPair` как JSON. Lazy per-account массив ищет `gao_cai_sheng_2_bot`. Это remote схема конкретного Telegram bot, а не локальное или защищённое plugin storage; код логирует `response.data` на debug уровне, поэтому payload аналогичных пользовательских хранилищ не следует писать в лог.

### Workflow и сборка

`docs/CONTRIBUTING.md` требует задавать config keys в `Defines`, использовать `Log` вместо `FileLog`, соблюдать UTF-8/LF и не менять root `build.gradle.kts` произвольно. README требует signing key, локальные password/alias properties и Firebase `google-services.json`; это инструкции сборки клиента, не плагина. CI workflow на pinned SHA указывает JDK 17, Android NDK `28.1.13356709`, checkout submodules (кроме update `libs/rust`) и вызов `:TMessagesProj:assembleRelease`. Workflow не запускался в этой задаче.

## Таблица методов и call-site

| Модуль / метод | Вызов | Назначение и контекст | Первичный permalink |
|---|---|---|---|
| `WebSocketHelper` | `getSocksPort(port: Int): Int`; `wsReloadConfig()` | Локальный proxy port, provider/TLS/headers; singleton transport клиента | [WebSocketHelper.kt](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/helpers/WebSocketHelper.kt#L85-L135) |
| `tcp2wsServer` | `setCdnDomain`, `setTls`, `setUserAgent`, `setConnHash`, `start(int)`, `stop()` | Конфигурация transport и listener lifecycle | [configuration](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/tcp2ws/src/main/java/org/tcp2ws/tcp2wsServer.java#L27-L36), [lifecycle](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/tcp2ws/src/main/java/org/tcp2ws/tcp2wsServer.java#L126-L181) |
| `ProxyHandler` | `prepareServer()`, `processRelay()`, `relay()` | SOCKS flow и WS frame relay; worker thread на TCP клиента | [connect](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/tcp2ws/src/main/java/org/tcp2ws/ProxyHandler.java#L119-L171), [dispatch](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/tcp2ws/src/main/java/org/tcp2ws/ProxyHandler.java#L185-L218) |
| `Socks4Impl` / `Socks5Impl` | `getClientCommand()`, `connect()`, `udp()` | Command parsing, address limits, SOCKS5 UDP; source inspection notes BIND/domain/IPv6 gaps above | [SOCKS4](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/tcp2ws/src/main/java/org/tcp2ws/Socks4Impl.java#L107-L135), [SOCKS5](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/tcp2ws/src/main/java/org/tcp2ws/Socks5Impl.java#L131-L174), [address helper](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/tcp2ws/src/main/java/org/tcp2ws/Utils.java#L20-L30) |
| `WsSettingsActivity` | `onItemClick(...)` | Переключение backend/TLS, custom endpoint, targeted UI refresh | [WsSettingsActivity.java](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/activity/WsSettingsActivity.java#L69-L140) |
| `ConfigManager` | typed getters, `put*`, `deleteValue` | App preferences abstraction | [ConfigManager.kt](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/config/ConfigManager.kt#L31-L35), [methods](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/config/ConfigManager.kt#L44-L132) |
| `ConfigSwitchGenerator` | KSP `process(Resolver)` | Генерация config facade из annotated fields | [annotations](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/Annotations.kt#L22-L56), [processor](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/libs/ksp/src/main/kotlin/top/qwq2333/nullgram/ConfigSwitch.kt#L39-L177) |
| `ConnectionsHelper` | `sendRequestAndDo(req, flags, action)` | Account-bound callback bridge на IO dispatcher | [ConnectionsHelper.kt](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/helpers/ConnectionsHelper.kt#L30-L55) |
| `CloudStorage` | `get(key)`, `set(key,value)`, `delete(key)` | Per-account remote storage через Telegram bot API | [CloudStorage.kt](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/config/CloudStorage.kt#L36-L105) |
| `BaseTranslator` / `TranslateHelper` | `translateText(...)`, `translate(...)` | Provider strategy, base-class HTTP client/cache, Main/IO split | [BaseTranslator.kt](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/translate/BaseTranslator.kt#L41-L135), [TranslateHelper.kt](https://github.com/qwq233/Nullgram/blob/b3d4f45e1ebd1a15576b46f87172ce076cf390f1/TMessagesProj/src/main/java/top/qwq2333/nullgram/helpers/TranslateHelper.kt#L95-L128) |

## Практические рецепты и ограничения

1. **Изолировать сетевую функцию клиента:** вынесите protocol implementation в отдельный Gradle module, а app layer пусть владеет настройками и сроком жизни. Для transport-подобной функции задайте close/cancel и ограничение сессий: Nullgram создаёт thread на listener и каждого клиента, но `stop()` не показывает закрытия активных соединений.
2. **Провести новую опцию от ключа к UI:** определите typed key/default в одном catalog, убедитесь что KSP генерирует нужный accessor, свяжите настройку с UI и обновлением зависимого состояния. Сверьте annotations и реально обрабатываемые типы.
3. **Добавить сетевого провайдера:** реализуйте provider-specific subclass контракта `BaseTranslator`, объявите capabilities, возвращайте структурированный HTTP status/error и используйте общий coroutine/error flow. Не трактуйте внутренний контракт как регистрацию через plugin loader.
4. **Портировать account-scoped действие:** привяжите объект к account instance и проверьте lifecycle при смене аккаунта. `CountDownLatch.await()` здесь не имеет timeout в просмотренном методе и не является готовым cancellable шаблоном.

- Runtime совместимость tcp2ws с endpoints, TLS/custom host, корректное завершение listener и полнота SOCKS4/5 не проверялись. BIND явно не подключён; SOCKS4 отказывает UDP; SOCKS5 domain ATYP отвергается, а IPv6 ветка не подтверждена; безопасное освобождение socket pool при race не доказано.
- Listener создаёт `new ServerSocket(port)` без явного bind address, поэтому код не фиксирует привязку только к loopback; также WebSocketHelper выбирает свободный port, закрывая временный socket до запуска listener, что оставляет окно гонки при bind.
- Не установлена совместимость внутренних классов с конкретной версией ExteraGram/AyuGram; внешние plugin APIs не исследовались. Внутренние Telegram/Nullgram классы и generated `Config` — не публичный plugin contract.
- Радарное утверждение о первенстве/датировке tcp2ws в NiagramX не подтверждено: исторических ссылок нет. Подтверждено наличие и использование `libs/tcp2ws` в Nullgram на указанном SHA.
- Отдельный статус: пока не проверено независимым reviewer; все доказательства имеют статус code/docs/inference, не runtime-verified.
