---
type: source
source_id: niagramx
platform: Android
review_status: accepted-with-gaps
review: ../reviews/niagramx.md
date: 2026-09-28
---

# NiagramX (HSSkyBoy/NiagramX)

[Репозиторий](https://github.com/HSSkyBoy/NiagramX), pinned snapshot: ветка dev, SHA f97133c55ff6594564b82fc6d2dffa74a960e639 (2026-09-27). Build config задаёт версию 12.10.3 ([gradle.properties:14–15](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/gradle.properties#L14-L15)); лицензия GPL v3 ([LICENSE:1–2](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/LICENSE#L1-L2)). Все основные ссылки ниже закреплены за этим SHA.

## Роль источника и границы

NiagramX — Android-клиент Telegram на базе Nagram/Nekogram/NagramX, не самостоятельный plugin SDK или проект ExteraGram-плагинов. Проверенные функции напрямую встроены в исходники клиента через NyaConfig, Kotlin/Java helpers и изменения классов Telegram. В просмотренных docs/build нет публичного контракта загрузчика внешних плагинов, manifest плагина или hook API. MediaController, ChatMessageCell, NotificationsController и ProxyRotationController здесь являются внутренними call-site; их нельзя считать API хоста ExteraGram без отдельной проверки.

Покрыты собственные подсистемы и конкретные точки из radar-context: предзагрузка аудио, локальная отрисовка галочки, chat sounds, LLM-перевод, proxy/VPN/WebSocket, build/CI. Стандартные классы Telegram не разбирались целиком; не исследованы все UI, JNI/WebRTC и сторонние зависимости. Код не запускался, runtime и сборка не проверялись.

## Сверка утверждений радара

- Repeat One preload подтверждён в pinned code. Приватный MediaController.checkIsNextMusicFileDownloaded(int currentAccount) проверяет разрешение DownloadController и размер списка, затем при NoPreloadTrackIfRepeatOne=true и repeatMode==2 завершает работу до определения следующего файла и вызова FileLoader. Настройка по умолчанию false и показана отдельным checkbox в секции AutoDownload. Python/Java hook в радаре — идея портирования, а не способ реализации внутри NiagramX. Метод private; доступность раннего hook зависит от конкретного host/DEX API.
- Локальная одна галочка подтверждается кодом: NyaConfig хранит HideReadReceiptsLocally, а ChatMessageCell.createStatusDrawableParams() меняет локальный drawable bitmask. Сам метод формирует параметры отрисовки; серверный receipt здесь не меняется.
- Контекстный LLM cache подтверждён. TranslationCache — LruCache на 256 записей; ключ зависит от модели, языка, хэша текста и хэша непустого контекста. LLMTranslator проверяет его до запроса и пишет очищенный результат после успеха.
- iOS sounds подтверждены в NotificationsController: настройка выбирает входящий/исходящий ресурс в существующих playInChatSound()/playOutChatSound(); при переключении сбрасываются кэшированные ID/loaded-флаги SoundPool.
- TCP-over-WebSocket из Nullgram подтверждается кодом: tcp2ws включён Gradle subproject, WebSocketHelper конфигурирует локальный SOCKS server, SharedConfig добавляет специальный proxy entry.
- Три historical URL не являются доказательствами этих функций: b8c3db1 добавляет настройку счётчика пересылок, ee415d4 — анимации ввода, fa093d9 — выбор быстрого proxy/speed acceleration. Исторические ссылки сверены; Repeat One и другие перечисленные функции подтверждаются текущим pinned snapshot.

## Покрытие снимка

| Прочитанные пути | Извлечено | Пропуски |
|---|---|---|
| README.md, LICENSE, .gitmodules | Назначение, требования README, лицензия, submodules | Не проверены все vendored источники и их лицензии |
| gradle.properties, build.gradle, settings.gradle, TMessagesProj/build.gradle, PR/staging/release workflows | Версия, Android/JVM build settings, tcp2ws module, CI-рецепт | CI локально не запускался |
| MediaController.java, NyaConfig.kt, NekoGeneralSettingsActivity.java | Repeat One guard, настройка и UI | Не прослежены все гонки плеера/download pipeline |
| ChatMessageCell.java, NekoChatSettingsActivity.java | Условие локальной отрисовки статуса | Не проверялись остальные UI/accessibility пути |
| NotificationsController.java, iOS sound resources | SoundPool, queue, выбор ресурсов и reset ID | Звук на устройстве не проверен |
| Translator.kt, LLMTranslator.kt, TranslationCache.kt, LlmTransport.kt, GeminiNativeClient.kt, OpenAICompatClient.kt, UrlNormalizer.kt, LlmConfig.kt, HttpClient.kt, settings/call-sites | Context/cache/provider transport/credential/error flow | Нет runtime сетевого теста; не проверены все providers |
| ProxyUtil.kt, WebSocketHelper.kt, ProxyRotationController.java, SharedConfig.java, ApplicationLoader.java, libs/tcp2ws/* | VPN callbacks, proxy restore/selection, tcp2ws integration | Живой VPN/proxy и полная сетевая цепочка не проверены |
| radar-context.md, radar-urls.json | Вторичные claims сопоставлены со снимком и historical commits | Radar остаётся вторичным источником |

Tree полный: tree_truncated=false, 29 814 записей. Анализ кода целевой, не построчный. gradle/libs.versions.toml запрошен, но отсутствует в snapshot (HTTP 404); зависимости заданы Groovy build files. Submodule contents не вошли в snapshot. README говорит об API 36/Build Tools 36.0.0+, но pinned Gradle и PR workflow задают SDK 37/Build Tools 37.0.0 — для данной версии конфигурацию следует брать из build/CI, README устарел.

## Реализация и полезные детали

### Repeat One и настройки

NyaConfig — глобальная конфигурация: getPreferences() использует SharedPreferences nkmrcfg; init() защищает загрузку volatile-флагом и synchronized-блоком. Встроенная настройка обычно соединяет ключ/default, ConfigCell в экране и guard у узкого call-site; это лишь паттерн кода клиента, не plugin settings SDK.

NoPreloadTrackIfRepeatOne — boolean по умолчанию false, checkbox добавлен в NekoGeneralSettingsActivity/AutoDownload. MediaController.checkIsNextMusicFileDownloaded(int currentAccount) сначала требует canDownloadNextTrack() и playlist не короче двух элементов. При включённом флаге и repeatMode==2 возвращается до выбора следующего индекса/пути. Иначе учитываются shuffledPlaylist и playOrderReversed, проверяются attachPath и FileLoader path, а отсутствующий music file грузится с низким приоритетом. Метод вызывается из checkIsNextMediaFileDownloaded() и из ветки обработки music message.

Для портирования проверьте host version и hookability: метод private, instance method с account id. Ниаграмный код не создаёт hook handles или plugin cleanup lifecycle. Обновление, меняющее метод/путь вызова, требует перепроверки. Нельзя утверждать, что KPM позволяет именно такой ранний выход, пока это не подтверждено в его API.

HideReadReceiptsLocally — false по умолчанию, checkbox в NekoChatSettingsActivity. createStatusDrawableParams() для исходящего отправленного сообщения формирует drawable bits с учётом scheduled, isUnread() и флага; это UI-состояние, не запись в TLRPC/MessageObject и не сетевое изменение receipt. Plugin hook должен проверять соответствующий seam в версии хоста.

### Sounds и LLM

useIosSounds — false по умолчанию. playInChatSound()/playOutChatSound() проверяют chat-sound, silent mode и запись аудио, затем используют notificationsQueue и SoundPool. Если настройка изменилась, обнуляются sound IDs и loaded-флаги, после чего выбирается ios_sound_in/out либо штатный ресурс. Видимый код не показывает явный unload старого sample при переключениях; runtime ресурсное поведение неизвестно.

LLMTranslator передаёт контекст через coroutine ThreadContextElement и ThreadLocal; withTranslationContext(context, block) оборачивает suspend-block и восстанавливает прежний thread state. doLLMTranslate использует контекст только при llmUseContext и добавляет его отдельным user message перед prompt. TranslationCache хранит до 256 process-local значений; ключ: model, язык, MD5 текста, MD5 контекста (или пустой). TTL/persistence в модуле не видны; ключ не включает provider/base URL, поэтому одинаковые остальные компоненты могут переиспользовать запись между provider. Это вывод из ключа, не runtime-confirmed collision.

Транспорт разделён: GeminiNativeClient формирует generateContent с x-goog-api-key; OpenAICompatClient — /chat/completions с Bearer token; оба используют LlmTransport/HttpClient. prepareCredentials чистит ввод, требует URL/key и отклоняет CR/LF в key. execute() использует блокирующий OkHttp execute(), возвращая статус и длительность, поэтому вызывающий код должен проверить dispatcher перед UI use. При HTTP 400 с optional params transport делает retry без них и запоминает отключение по base URL + model в памяти. LLMTranslator разбирает 429/4xx/network failure и в некоторых случаях переходит на GoogleAppTranslator. Он также логирует последние два знака API key и массив messages/prompts; при портировании важно не копировать этот диагностический риск для пользовательского контекста.

### Proxy, VPN, TCP2WS

WebSocketHelper.getSocksPort() использует 6356; overload с -1 выбирает свободный ephemeral port. При запуске tcp2ws передаются proxy domain, TLS toggle, системный HTTP User-Agent плюс идентификатор Nullgram и connHash; stopServer() останавливает server и сбрасывает state. Start/stop синхронизированы. SharedConfig добавляет entry для специального адреса, не сериализует его как обычный пользовательский proxy и запрещает обычное удаление. libs/tcp2ws README описывает часть материалов как decompiled из Nekogram/NekoInverter и называет java-socks-proxy-server первоначальным upstream: provenance отличается по компонентам.

`DisableProxyWhenVpnEnabled` по умолчанию выключен ([NyaConfig.kt#L302](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/config/NyaConfig.kt#L302)); checkbox находится в экспериментальных настройках → Connections ([NekoExperimentalSettingsActivity.java#L98](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/settings/NekoExperimentalSettingsActivity.java#L98)), а при его переключении вызывается `checkVpnState()` для немедленной сверки текущего состояния ([NekoExperimentalSettingsActivity.java#L207](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/settings/NekoExperimentalSettingsActivity.java#L207)). ProxyUtil проверяет активную сеть и остальные Android networks на TRANSPORT_VPN. При включённом флаге сохраняет ProxyDisabledByVpn, останавливает tcp2ws и отключает proxy; при уходе VPN восстанавливает его только если отключение сделал этот механизм и currentProxy сохранился. ApplicationLoader регистрирует callbacks на старте; ProxyUtil слушает default и VPN network, повторно проверяя часть событий на UI thread через 400 ms. Volatile marker отличает собственное proxy изменение от ручного.

ProxyRotationController.init() добавляет NotificationCenter observers для всех аккаунтов и глобальных proxy событий. ConnectionsManager.checkProxy() проверяет proxy выбранного аккаунта; callback меняет ping/availability на UI thread и публикует proxyCheckDone. Auto speed acceleration выбирает доступный proxy с минимальным положительным ping и меняет текущий только если улучшение не меньше 80 ms. applyProxy сохраняет настройки, публикует события и вызывает ConnectionsManager.setProxySettings. Это internal client API, не обещанная plugin surface.

### Build, debug, delivery

README: Android API 24 minimum, target API 37, JDK 21, NDK 27.2.12479018, CMake 3.31+, recursive shallow submodules, TELEGRAM_APP_ID/TELEGRAM_APP_HASH в local.properties. gradle.properties задаёт 12.10.3; build.gradle может добавить короткий COMMIT_ID к versionName. В TMessagesProj build.gradle versionCode=1273, official APP_VERSION_CODE=7089; не путайте конкретный variant code и официальный код. Root build задаёт compile/target SDK 37, Build Tools 37.0.0, JVM target 21.

PR workflow для не-md/xml изменений выполняет TMessagesProj:assembleDebug на arm64-v8a и загружает artifact. Staging workflow собирает arm64-v8a и x86_64, JDK 21/SDK 37/NDK 27.2; подпись читает CI secrets и workflow может отправить artifact в Telegram. Это заявленная CI конфигурация, не подтверждение успешной сборки данного SHA. Release workflow и supply-chain полностью не разбирались.

## Таблица call-sites

| Модуль и вызов | Назначение / lifecycle | Потоки и аккаунты | Первоисточник |
|---|---|---|---|
| NyaConfig.getPreferences(), init(), addConfig(...) | Глобальные user settings, init из ApplicationLoader | SharedPreferences приложения | [NyaConfig.kt#L24](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/config/NyaConfig.kt#L24) |
| MediaController private checkIsNextMusicFileDownloaded(int currentAccount) | Prefetch следующего трека; guard Repeat One до FileLoader | Account-scoped DownloadController/FileLoader | [MediaController.java#L3125](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/org/telegram/messenger/MediaController.java#L3125) |
| ChatMessageCell.createStatusDrawableParams() | Вычисляет локальный bitmask исходящего статуса | UI only, без отдельного сетевого запроса | [ChatMessageCell.java#L29517](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatMessageCell.java#L29517) |
| NotificationsController.playInChatSound()/playOutChatSound() | Выбор SoundPool sample открытого чата | notificationsQueue, controller аккаунта | [NotificationsController.java#L3342](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/org/telegram/messenger/NotificationsController.java#L3342) |
| LLMTranslator.withTranslationContext()/doLLMTranslate() | Context propagation, cache lookup, network provider | Coroutine/thread-local; account scope не виден | [LLMTranslator.kt#L62](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/translate/source/LLMTranslator.kt#L62) |
| TranslationCache.get()/put()/clear() | Process-local кэш на 256 значений | Не account-scoped | [TranslationCache.kt#L6](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/llm/net/TranslationCache.kt#L6) |
| LlmTransport.prepareCredentials()/execute() | Общий HTTP и обработка ошибок | Блокирующий OkHttp execute | [LlmTransport.kt#L63](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/llm/net/LlmTransport.kt#L63) |
| WebSocketHelper.getSocksPort()/stopServer()/wsReloadConfig() | Start/stop/config встроенного tcp2ws server | Синхронизированные entry points | [WebSocketHelper.kt#L41](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/helpers/WebSocketHelper.kt#L41) |
| ProxyUtil.registerNetworkCallback()/checkVpnState() | VPN/default network events, отключение и возврат proxy | App lifecycle, callbacks/UI-thread recheck | [ProxyUtil.kt#L61](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/top/nkbe/niagram/utils/ProxyUtil.kt#L61) |
| ProxyRotationController.checkAndAccelerate()/switchToFastestProxy() | Ping и применение лучшего proxy | ConnectionsManager выбранного account; UI callback; observers всех accounts | [ProxyRotationController.java#L59](https://github.com/HSSkyBoy/NiagramX/blob/f97133c55ff6594564b82fc6d2dffa74a960e639/TMessagesProj/src/main/java/org/telegram/messenger/ProxyRotationController.java#L59) |

## Рецепты и ограничения

1. Для простого поведения используйте схему «ключ/default → checkbox → guard у узкого call-site». Repeat One блокирует побочный preload до выбора следующего файла и сохраняет основной алгоритм плеера. Сначала подтвердите private method hook в target host.
2. Разделяйте серверное состояние и UI: drawable hook меняет отображение, но сам по себе не отменяет receipt на сервере.
3. Контекст coroutine передавайте coroutine context-ом, а не общим mutable singleton; cache key должен включать параметры, которые меняют ответ.
4. Разделяйте provider-specific формат и общий transport/error/cache. Не переносите блокирующий OkHttp в UI callback и не копируйте логирование пользовательских prompts/key fragments.
5. При замене sound resource используйте существующую очередь/плеер, инвалидируйте cached ID и проверьте освобождение старого sample на устройстве.
6. Для VPN/proxy observer различайте внутреннее изменение и действие пользователя; network callbacks могут повторяться.
7. Привязывайте внутренние методы к версии: NiagramX 12.10.3 не гарантирует совпадение с будущим Telegram или ExteraGram/AyuGram.

## Historical URLs и gaps

В radar-urls.json перечислены [b8c3db1](https://github.com/HSSkyBoy/NiagramX/commit/b8c3db1547f0fdf3deea4f7eceac3554320574e8), [ee415d4](https://github.com/HSSkyBoy/NiagramX/commit/ee415d4d2594927e5c3fbea12c883b0d261f200d) и [fa093d9](https://github.com/HSSkyBoy/NiagramX/commit/fa093d98e8deb64c158aeef80b1ac87e96ee28e5). Их темы — счётчик пересылок, input animation и fastest proxy. Они не являются commit history для Repeat One guard. Функции Repeat One, галочка, translation cache и iOS sounds подтверждены по текущему pinned source.

Не проверены: поддержка early return из private MediaController в конкретной версии KPM/DEX runtime; live VPN/proxy, включая ручное переключение; tcp2ws под нагрузкой; SoundPool cleanup при повторном toggle; межпровайдерные cache collisions в runtime; полный тестовый/CI результат и release signing details. NiagramX иллюстрирует клиентские реализации, но не подтверждает поведение внутри plugin host.
