---
type: source
source_id: plugins-store-network-async
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-network-async.md
date: 2026-10-01
---

# Kangel-Plugins/Plugins-Store — Сеть, асинхронность, потоки, WebSocket и прокси (Раздел plugins-store-network-async)

Источник: [репозиторий Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store), снимок commit `00de67026419f9dbe3a2787bb1236e8aaead8f76` (`main`). Раздел `plugins-store-network-async` охватывает 138 плагинов каталога, реализующих механизмы параллелизма через `threading.Thread`, `asyncio`, `concurrent.futures.ThreadPoolExecutor`, сокетные коммуникации (`socket`), протоколы прикладного уровня (`requests`, `urllib`), WebSocket-клиенты, локальные веб-серверы (`http.server`), туннелирование/прокси (VLESS Reality/gRPC/WS, Sing-box, SOCKS5, MTProto), обход сетевых блокировок, rate limiting и мостирование нативных MTProto RPC-вызовов клиента ExteraGram.

## Роль и границы источника

Этот источник представляет собой массив реальных практических реализаций (call-sites) сетевого и асинхронного взаимодействия внутри сред Chaquopy/Android в форках Telegram (exteraGram, AyuGram). Он наглядно демонстрирует:
1. Архитектурные паттерны изоляции фоновых циклов событий (`asyncio`) от UI-потока Android и главного потока Python.
2. Ограничения среды выполнения Chaquopy на Android (недоступность C-бинарных расширений, таких как нативный `aiohttp`, и необходимость использования чистых Python-пакетов вроде `websocket-client` совместно с сертификатами `certifi`).
3. Механизмы интеграции внешних протоколов прокси (VLESS, VMess, Trojan, SOCKS5, WebProxy) с нативным контроллером прокси клиента (`com.exteragram.messenger.proxy.ProxyController`).
4. Паттерны неблокирующего перехвата исходящих сообщений в хуках (`HookStrategy.CANCEL` + `run_on_queue` + `run_on_ui_thread`).
5. Защиту от сетевых блокировок и FloodWait со стороны Telegram API (скользящее окно, экспоненциальный backoff).

Код плагинов исследован статически; плагины не запускались на реальных физических устройствах в рамках текущего сбора. Статус всех извлечённых фактов нормализован как `code`.

## Покрытие

| Путь плагина / файла | Анализируемые компоненты и технологии | Границы и специфические условия |
|---|---|---|
| [`Plugins/zwylib.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/zwylib.plugin) | Класс `_AsyncManager`, поток `ZwyAsyncThread`, `wrap_java_call`, `Requests.async_send`, автообновление через `_AutoUpdater._loop` | Требует загрузки ZwyLib в качестве общей библиотеки; отслеживание задач по плагинам через инспекцию стека |
| [`Plugins/vlesstools.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/vlesstools.plugin) | Парсер VLESS Reality/gRPC/WS, генерация Sing-box/Clash конфигураций, `ThreadPoolExecutor(max_workers=10)`, сокетный TCP-пинг с TTL кешем, `_delete_file_delayed` | Зависит от `requests`, `yaml`, `EXTERNAL_NETWORK_QUEUE`; отправка через `SendMessagesHelper` |
| [`Plugins/proxy_sub.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/proxy_sub.plugin) | Отказоустойчивая загрузка подписок (GitVerse / GitHub), регистрация через `ProxyController.addProxy`, `ProxySettings.fromUri` | Зависит от закрытых классов `com.exteragram.messenger.proxy.ProxyController` и `SharedConfig` |
| [`Plugins/edge_tts_voiceover.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/edge_tts_voiceover.plugin) | Клиент WebSocket поверх `websocket-client`, генерация DRM-токена `Sec-MS-GEC`, распаковка бинарных ABNF-фреймов, плеер `android.media.MediaPlayer` | Обоснованный отказ от библиотеки `edge-tts` из-за несовместимости бинарного `aiohttp` с Chaquopy |
| [`Plugins/web_file_manager.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/web_file_manager.plugin) | Встроенный HTTP веб-сервер на `http.server.HTTPServer`, проверка занятости порта через `socket.connect_ex`, корректный shutdown/join | Сервер доступен локально; управление жизненным циклом потока сервера при выгрузке плагина |
| [`Plugins/downloader.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/downloader.plugin) | Ручной SOCKS5-хэндшейк через сокеты, патчинг фабрики `urllib3.util.connection.create_connection` через контекстный менеджер | Низкоуровневая подмена сокетов библиотеки requests для туннелирования трафика через Telegram-прокси |
| [`Plugins/server_status.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/server_status.plugin) | Определение типа прокси (`SharedConfig.currentProxy`), туннелирование сокетов через SOCKS5, токен поколения `_monitor_gen` для прерывания цикла | Проверка невозможности туннелирования произвольного TCP через MTProto-прокси (`secret` присутствует) |
| [`Plugins/speedtest.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/speedtest.plugin) | Измерение скорости отдачи и скачивания через эндпоинты Cloudflare Speed Test, замер пинга и получение метаданных сети через `ipinfo.io` | Передача 10 МБ буфера через `requests.post` с фиксированным таймаутом |
| [`Plugins/networktools.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/networktools.plugin) | Набор из 30+ сетевых утилит: DNS-over-HTTPS (Google/Cloudflare DoH), парсинг сертификатов TLS через `ssl`, сканирование портов через `connect_ex`, WHOIS/IP API | Использование агрессивных таймаутов на сокетах; изоляция запросов в очереди `EXTERNAL_NETWORK_QUEUE` |
| [`Plugins/discord_rpc.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/discord_rpc.plugin) | Скользящее окно rate limiting (`MAX_UPDATES_PER_HOUR = 10`), адаптивный backoff, периодический опрос через `run_on_queue`, обновление био через MTProto | Защита от Telegram FloodWait при частых сетевых мутациях профиля пользователя |
| [`Plugins/AIAssistant.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/AIAssistant.plugin) | Пул постоянных соединений `requests.Session()`, отправка мультимодальных запросов к Google Gemini, таймаут 120 секунд, дифференцированная обработка ошибок | Обработка сетевых ошибок API (HTTPError vs RequestException) и парсинг деталей JSON-ответа |
| [`Plugins/TranslaticaPro.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/TranslaticaPro.plugin) | Мостирование нативного перевода `TL_messages_translateText` через `threading.Event`, маскирование ссылок перед переводом через Google Translate | Синхронизация асинхронного нативного Telegram RPC с рабочим фоновым потоком |
| [`Plugins/privacy_firewall.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/privacy_firewall.plugin) | Неблокирующая инспекция исходящих сообщений и файлов через отмену хука (`HookStrategy.CANCEL`), фоновый анализ в `run_on_queue` и возврат в UI | Паттерн безопасной задержки отправки с подтверждением пользователя в случае сетевых находок |

## Технические факты

### 1. Архитектура асинхронности и интеграция Event Loop

Плагины в среде ExteraGram выполняются внутри процесса Android-приложения под управлением рантайма Chaquopy. В таких условиях вызов `asyncio.run()` или запуск цикла событий в главном потоке блокирует обработку UI и событий Android.

Библиотека `zwylib.plugin` реализует эталонный синглтон-менеджер `_AsyncManager` ([код, строки 2068–2135](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/zwylib.plugin#L2068-L2135)):
- **Изолированный демон-поток:** При старте менеджер создаёт `self.loop = asyncio.new_event_loop()` и запускает его в выделенном потоке `threading.Thread(target=self._run_event_loop, daemon=True, name="ZwyAsyncThread")`. Поток выполняет `self.loop.run_forever()`.
- **Маршрутизация задач и отслеживание владельца:** Метод `run_task(coro)` инспектирует стек вызовов (`_get_plugin_id_from_stack`), связывая создаваемую корутину с конкретным плагином. Корутина регистрируется в коллекции `self.tasks[plugin_id]` и запускается в цикле событий с помощью `asyncio.run_coroutine_threadsafe(task_wrapper(), self.loop)`.
- **Грациозная очистка:** При выгрузке плагина метод `cancel_all_for(plugin_id)` обходит все задачи данного плагина и потокобезопасно вызывает отмену: `self.loop.call_soon_threadsafe(task.cancel)`.
- **Связка с Java Callbacks:** Метод `wrap_java_call(java_method, *args, **kwargs)` ([строки 2138–2165](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/zwylib.plugin#L2138-L2165)) создаёт `future = loop.create_future()`, перехватывает переданный колбэк-маркер `_AsyncMarker` и перенаправляет результаты выполнения нативного Java-кода в Python `Future` через `loop.call_soon_threadsafe`.

### 2. Мостирование MTProto RPC в async/await

Взаимодействие с серверами Telegram в плагинах осуществляется через системные методы `send_request` или `ConnectionsManager`. В коде зафиксированы два взаимодополняющих подхода к мостированию этих вызовов:

1. **Асинхронный адаптер `Requests.async_send` (`zwylib.plugin`, строки 1366–1395):**
   `Requests.async_send(req, delay, **kwargs)` создаёт `asyncio.Future`. При получении ответа от `send_request` проверяется наличие `TLRPC.TL_error`. Если ошибка присутствует, фьючерс завершается исключением `Exception(f"Error {error.code}: {error.text}")`, иначе в него передаётся десериализованный `TLObject`. Доставка результата в цикл событий производится через `loop.call_soon_threadsafe`.
2. **Синхронный блокирующий мост через `threading.Event` (`TranslaticaPro.plugin`, строки 15249–15320):**
   При выполнении нативного перевода текста сообщений (`TLRPC.TL_messages_translateText`) на фоновом рабочем потоке плагин создаёт прокси-делегат `RequestDelegate`, запускает запрос через `ConnectionsManager.getInstance(account).sendRequest` и блокирует текущий поток через `done.wait(timeout_sec)`. При получении ответа или таймаута поток разблокируется, позволяя встроить вызов в линейный синхронный код пайплайна обработки текста.

### 3. Туннелирование, сетевые прокси и протокол VLESS

Плагины демонстрируют развитую инфраструктуру поддержки прокси-соединений:
- **Парсинг и нормализация VLESS Reality/gRPC/WS (`vlesstools.plugin`, строки 368–395):** Плагин парсит URL схемы `vless://`, корректно извлекая параметры безопасности Reality (`pbk` — публичный ключ, `sid` — short ID с валидацией чётности hex-строки), тип маскировки SNI, фингерпринт браузера (`fp=chrome`) и транспорты WebSocket (`ws_path`, `ws_host`) и gRPC (`grpc_service`).
- **Трансляция конфигураций в Sing-box и Clash (`vlesstools.plugin`, строки 658–715):** Разобранные структуры преобразуются в исходящие профили (outbounds) Sing-box JSON и Clash YAML с распределением по селекторам `PROXY` и правилам маршрутизации.
- **Низкоуровневый SOCKS5-клиент на сокетах (`downloader.plugin`, строки 381–420):** Метод `_socks_create_connection` реализует RFC 1928 на чистом Python:
  1. Отправка байтов `\x05\x01\x00` (или `\x05\x01\x02` при наличии логина/пароля).
  2. Проверка ответа сервера и передача субсогласования аутентификации (`\x01 + len(user) + user + len(pwd) + pwd`).
  3. Отправка команды CONNECT (`\x05\x01\x00`) с определением типа целевого адреса: IPv4 (`\x01` + `inet_aton`) или доменное имя (`\x03` + `len(host)` + `host`) и 16-битный порт в сетевом порядке байт (`big-endian`).
- **Динамический monkey-patching библиотеки urllib3 (`downloader.plugin`, строки 206–225):** Контекстный менеджер `_proxy_connection_patch` временно подменяет функцию `urllib3.util.connection.create_connection` на кастомную сокетную фабрику, что позволяет заставить стандартный `requests.get/post` ходить через прокси без изменения настроек окружения.
- **Интеграция с нативным `ProxyController` ExteraGram (`proxy_sub.plugin`, строки 164–185):** Загруженные из внешних подписок прокси добавляются непосредственно в настройки приложения через вызовы `com.exteragram.messenger.proxy.ProxyController.getInstance().addProxy(ProxyInfo(ps))` и `ProxySettings.fromUri(Uri.parse(...))`.

### 4. WebSocket и DRM в окружении Chaquopy

В плагине `edge_tts_voiceover.plugin` ([строки 1–25, 89–105, 173–245](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/edge_tts_voiceover.plugin)) зафиксирован важный технический прецедент:
- **Отказ от нативных C-расширений:** Официальная библиотека `edge-tts` не может быть собрана в Chaquopy из-за жесткой зависимости от `aiohttp`, требующего компилируемые бинарные wheels.
- **Чистая Python-реализация поверх `websocket-client`:** Протокол взаимодействия с речевыми сервисами Microsoft реализован на базе pure-python библиотеки `websocket-client`. Для корректной валидации TLS-сертификатов на различных версиях Android используется bundle из пакета `certifi` (`sslopt={"ca_certs": certifi.where()}`).
- **Генерация DRM-токена Sec-MS-GEC:** Метод `_generate_sec_ms_gec` рассчитывает заголовок, переводя текущее время Unix в тики Windows (разница эпох 11644473600 секунд), округляет до 5-минутного окна квантования (`ticks -= ticks % 300`), переводит в 100-наносекундные интервалы и формирует SHA-256 хеш со статическим токеном доверенного клиента `6A5AA1D4EAFF4E9FB37E23D68491D6F4`.
- **Мультиплексирование бинарных аудиофреймов:** В цикле приёма сообщений парсятся текстовые пакеты метаданных (`OPCODE_TEXT`) до маркера завершения синтеза `Path:turn.end`, а бинарные пакеты (`OPCODE_BINARY`) распаковываются с помощью `struct.unpack(">H", data[:2])`, отсекая 16-битный заголовок для извлечения MP3-потока.

### 5. Встроенные сокетные серверы и локальные сетевые службы

Плагины `web_file_manager.plugin` и `adb_lite.plugin` встраивают полноценные фоновые серверы для локального взаимодействия:
- **HTTP Веб-сервер в Android-процессе (`web_file_manager.plugin`, строки 40–55, 1230–1255):** Сервер поднимается на базе `http.server.HTTPServer` и слушает порт `127.0.0.1:8090` в отдельном фоновом потоке, обслуживая веб-интерфейс управления файлами приложения.
- **Проверка занятости портов перед биндингом (`web_file_manager.plugin`, строки 1264–1275):** Функция `_check_port_available` выполняет неблокирующий опрос `socket.connect_ex((host, port)) != 0` с таймаутом 1 секунда, исключая падение процесса при конфликте портов.
- **Безопасная остановка сокетных серверов:** Выгрузка сервера производится строго в порядке: `server.shutdown()` -> `server.server_close()` -> `thread.join(timeout=1)`.

### 6. Защита от FloodWait, rate limiting и адаптивные очереди

Частые мутации данных через сетевые вызовы в Telegram могут приводить к ошибкам `FLOOD_WAIT_X`.
В `discord_rpc.plugin` ([строки 200–255](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/discord_rpc.plugin#L200-L255)) реализован комплексный механизм защиты:
- **Скользящее часовое окно (Sliding Window):** Хранится история меток времени обновлений в файле `discord_rpc_history.json`. Все события старше 3600 секунд (`HOURLY_WINDOW`) фильтруются.
- **Лимит операций:** Установлен лимит `MAX_UPDATES_PER_HOUR = 10` и минимальный интервал между запросами `MIN_INTERVAL_BETWEEN_UPDATES = 10` секунд.
- **Адаптивный backoff:** При увеличении частоты обновлений свыше 3 раз в час задержка следующего цикла динамически увеличивается: `multiplier = 1 + (count - 3)`, масштабируя интервал проверки `MIN_LOOP_DELAY * multiplier`.
- **Использование `run_on_queue`:** Планирование следующего шага цикла осуществляется через неблокирующую очередь клиента `run_on_queue(self._process_cycle, GLOBAL_QUEUE, delay)`.

## Вызовы и наблюдаемые контракты

Ниже приведена сводная таблица ключевых методов, call-sites и контрактов сетевых плагинов:

| Модуль / Класс | Точная сигнатура / Call-site | Назначение и поведение | Ссылка на доказательство |
|---|---|---|---|
| `_AsyncManager` | `run_task(self, coro: Coroutine) -> concurrent.futures.Future` | Выполняет корутину в потокобезопасном цикле `ZwyAsyncThread` с привязкой к ID плагина | [`zwylib.plugin:2098-2135`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/zwylib.plugin#L2098-L2135) |
| `_AsyncManager` | `wrap_java_call(self, java_method, *args, **kwargs) -> Future` | Мостирует асинхронный Java/Android callback в Python `asyncio.Future` | [`zwylib.plugin:2138-2165`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/zwylib.plugin#L2138-L2165) |
| `Requests` | `async_send(cls, req: TLObject, delay: Optional[int] = None, **kwargs) -> TLObject` | Выполняет MTProto RPC-запрос асинхронно, преобразуя `TL_error` в Python `Exception` | [`zwylib.plugin:1366-1395`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/zwylib.plugin#L1366-L1395) |
| `VlessToolsPlugin` | `_check_server_availability(self, host: str, port: int) -> bool` | Проверяет доступность TCP-сокета с 300-секундным кешированием статуса в памяти | [`vlesstools.plugin:475-492`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/vlesstools.plugin#L475-L492) |
| `VlessToolsPlugin` | `_delete_file_delayed(self, path: str)` | Удаляет временный файл через 60 секунд в фоновом daemon-потоке после отправки | [`vlesstools.plugin:496-505`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/vlesstools.plugin#L496-L505) |
| `ProxyManagerPlugin` | `_do_fetch(self)` | Отказоустойчиво загружает конфигурации прокси, перебирая зеркала GitVerse/GitHub | [`proxy_sub.plugin:106-130`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/proxy_sub.plugin#L106-L130) |
| `ProxyController` | `PC.addProxy(ProxyInfo(ps))` | Добавляет прокси в нативную базу ExteraGram через Java-обёртку | [`proxy_sub.plugin:164-185`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/proxy_sub.plugin#L164-L185) |
| `EdgeTTSVoiceover` | `_synthesize_chunk(text, voice_id, rate, pitch) -> bytes` | Синхронно устанавливает WSS-сессию с Edge TTS, передаёт SSML и возвращает MP3 | [`edge_tts_voiceover.plugin:173-195`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/edge_tts_voiceover.plugin#L173-L195) |
| `WebFileManager` | `_stop_web_server(self)` | Грациозно останавливает `HTTPServer` через `shutdown()`, `server_close()` и `join(1)` | [`web_file_manager.plugin:1230-1255`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/web_file_manager.plugin#L1230-L1255) |
| `DownloaderPlugin` | `_proxy_connection_patch(self, patch_type)` | Контекстный менеджер, подменяющий `urllib3.util.connection.create_connection` | [`downloader.plugin:206-225`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/downloader.plugin#L206-L225) |
| `DownloaderPlugin` | `_socks_create_connection(self, dest_host, dest_port) -> socket.socket` | Выполняет RFC 1928 SOCKS5 handshake (No Auth / User-Password) через сырой сокет | [`downloader.plugin:381-420`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/downloader.plugin#L381-L420) |
| `ServerStatusPlugin` | `get_proxied_socket(self, target, port, timeout=4.0)` | Извлекает прокси Telegram и создаёт туннелированный SOCKS5 сокет с замером времени | [`server_status.plugin:229-265`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/server_status.plugin#L229-L265) |
| `SpeedTestPlugin` | `_upload_test(self) -> float` | Замеряет скорость отдачи через POST-запрос 10 МБ буфера на Cloudflare Speed Test | [`speedtest.plugin:76-105`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/speedtest.plugin#L76-L105) |
| `NetworkToolsPlugin` | `h_dig(self, args)` | Выполняет DoH (DNS-over-HTTPS) запросы к Google/Cloudflare в формате JSON | [`networktools.plugin:593-630`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/networktools.plugin#L593-L630) |
| `NetworkToolsPlugin` | `h_cert(self, args)` | Извлекает метаданные SSL-сертификата хоста через `ssl.create_default_context().wrap_socket` | [`networktools.plugin:559-580`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/networktools.plugin#L559-L580) |
| `DiscordRpcPlugin` | `_check_safety_and_cleanup_history(self) -> bool` | Проверяет соблюдение лимитов скользящего окна (`MAX_UPDATES_PER_HOUR = 10`) | [`discord_rpc.plugin:215-235`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/discord_rpc.plugin#L215-L235) |
| `GeminiAPIHandler` | `send_request(..., timeout=120) -> Dict[str, Any]` | Отправляет мультимодальный JSON-запрос к Gemini API через повторно используемую сессию | [`AIAssistant.plugin:426-485`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/AIAssistant.plugin#L426-L485) |
| `TranslaticaPro` | `_translate_text_native(self, text, dst, wait_sec=None)` | Вызывает нативный перевод Telegram MTProto и синхронизируется через `threading.Event` | [`TranslaticaPro.plugin:15249-15320`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/TranslaticaPro.plugin#L15249-L15320) |
| `PrivacyFirewall` | `on_send_message_hook(self, account, params) -> HookResult` | Отменяет хук (`CANCEL`) для глубокой проверки в очереди `run_on_queue` и алерта в UI | [`privacy_firewall.plugin:1153-1185`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/privacy_firewall.plugin#L1153-L1185) |

## Практические приёмы и рецепты

1. **Изоляция asyncio Event Loop в выделенном потоке:**
   Никогда не блокируйте UI-поток запуском циклов событий. Создайте `loop = asyncio.new_event_loop()`, запустите `threading.Thread(target=lambda: (asyncio.set_event_loop(loop), loop.run_forever()), daemon=True).start()`. Задачи отправляйте через `asyncio.run_coroutine_threadsafe(coro, loop)`.
2. **Безопасная очистка корутин при выгрузке плагина:**
   Сохраняйте запущенные фьючерсы в реестре `tasks[plugin_id]`. В хуке `on_plugin_unload` выполняйте отмену через `loop.call_soon_threadsafe(task.cancel)` во избежание утечек фоновых соединений и памяти.
3. **Чистый Python WebSocket поверх websocket-client:**
   При необходимости работы с WebSockets на Android избегайте зависимостей, требующих C-расширения (`aiohttp`). Используйте `websocket-client` и явно передавайте доверенные корневые сертификаты через `certifi`:
   ```python
   import websocket, certifi
   ws = websocket.create_connection(url, timeout=15, sslopt={"ca_certs": certifi.where()})
   ```
4. **Контекстное туннелирование urllib3 через SOCKS5:**
   Для перенаправления трафика библиотеки `requests` через кастомный прокси временно подменяйте фабрику `create_connection`:
   ```python
   @contextmanager
   def proxy_patch(sock_factory):
       import requests.packages.urllib3.util.connection as uc
       orig = uc.create_connection
       try:
           uc.create_connection = lambda addr, timeout=None, **kw: sock_factory(addr[0], addr[1])
           yield
       finally:
           uc.create_connection = orig
   ```
5. **Предотвращение зависания сокетных серверов при выгрузке:**
   При использовании встроенного `HTTPServer` реализуйте трёхэтапную остановку в `on_plugin_unload`:
   ```python
   self.server.shutdown()
   self.server.server_close()
   if self.server_thread and self.server_thread.is_alive():
       self.server_thread.join(timeout=1.0)
   ```
6. **Защита от FloodWait методом скользящего окна:**
   Для сетевых действий, изменяющих профиль пользователя Telegram (био, имя, аватар), сохраняйте временные метки успешных вызовов в локальный JSON. Проверяйте, что за последний час совершено не более 10 вызовов, а пауза между вызовами составляет не менее 10 секунд.
7. **Асинхронный перехват в хуках без блокировки UI:**
   Если хук отправки сообщения (`on_send_message_hook`) требует сетевого запроса или парсинга большого файла, немедленно возвращайте `HookResult(strategy=HookStrategy.CANCEL)`, переносите работу в `run_on_queue`, а по завершении проверки повторно вызывайте отправку либо показывайте диалог через `run_on_ui_thread`.

## Ограничения и противоречия

- **Статус верификации:** Все рассмотренные интерфейсы извлечены из исходного кода плагинов каталога (`code`). Запуск на реальных Android-устройствах, замеры задержек и нагрузочные тесты не проводились.
- **Ограничения окружения Chaquopy:** Попытка импортировать библиотеки с компилируемыми C/C++ расширениями (`aiohttp`, `uvloop`, `pycurl`) приводит к ошибке `ModuleNotFoundError` или падению загрузчика плагинов. Сетевой код должен быть реализован исключительно на стандартной библиотеке Python либо pure-python модулях.
- **Разделение типов прокси Telegram:** Прокси типа MTProto не поддерживают произвольное TCP-туннелирование. Плагины, проверяющие сетевые сокеты или сторонние веб-сервисы, обязаны фильтровать прокси со значением `secret` во избежание сбоев соединений.
- **UI Thread Safety:** Любые операции с графическим интерфейсом Telegram (показ диалогов `AlertDialogBuilder`, уведомлений `BulletinHelper`, обновление адаптеров списков) должны диспетчеризоваться строго через `run_on_ui_thread`. Вызов UI-методов из фоновых сокетных или asyncio потоков приводит к краху приложения с `CalledFromWrongThreadException`.
