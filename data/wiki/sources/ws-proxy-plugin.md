---
type: code
source_id: ws-proxy-plugin
platform: Android
review_status: accepted-with-gaps
review: ../reviews/ws-proxy-plugin.md
date: 2026-09-28
---

# tg_ws_proxy.plugin: локальный SOCKS5 и WebSocket-транспорт Telegram

- Репозиторий: [ReaIRyanGosling/tg_ws_proxy.plugin](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin).
- Закреплённый SHA: `c292816de3139634e62388aa78d0abcfbcadc27c`, ветка `main`; дерево зафиксировано 2026-09-27. [Снимок дерева](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/tree/c292816de3139634e62388aa78d0abcfbcadc27c), [commit](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/commit/c292816de3139634e62388aa78d0abcfbcadc27c), [entrypoint](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin).
- Проверка происхождения: сохранённые `snapshot.json` и `tree.json` называют тот же SHA; первичная GitHub-страница файла указывает SHA в breadcrumb и 1136 строк; проверенные локальные SHA-256 совпадают с `file-manifest.json` для `README.md` (`73d0c971…b9b18f`) и `tg_ws_proxy.plugin` (`9aa7d6df…b8e2e36`). GitHub metadata snapshot называет репозиторий публичным и `fork: false`; это подтверждает первичный репозиторий в рамках сохранённых GitHub-метаданных, но не доказывает авторство заимствованных алгоритмов. Репозиторий не объявляет лицензию (`license: null`), в полном зафиксированном дереве нет LICENSE.
- Роль: самостоятельный `.plugin` с `BasePlugin`, SOCKS5 listener и ручным WebSocket-транспортом. README говорит только, что это proxy plugin для AyuGram/exteraGram и что он основан на Flowseal/tg-ws-proxy. Это практический пример вмешательства в сетевой путь Android-клиента, а не API-гайд и не доказательство совместимости клиентского API.
- Метаданные entrypoint: `__id__ = "tg_ws_proxy_plugin"`, `__name__ = "tg-ws"`, `__version__ = "1.2.0"`, `__min_version__ = "11.12.0"`.
- Все результаты ниже получены статическим чтением закреплённого текста. Плагин не загружался, сеть/Telegram не использовались, тесты, сборка и установка не выполнялись; статус `runtime-verified` отсутствует.

## Покрытие и границы

| Прочитанный путь / свидетельство | Что извлечено | Пробел |
|---|---|---|
| `raw/ws-proxy-plugin/snapshot.json`, `tree.json`, `file-manifest.json`, `repository.json` | SHA, полный состав короткого дерева (2 файла), metadata репозитория, контрольные суммы | GitHub repository metadata является сохранённым ответом API на дату snapshot, а не непрерывно обновляемым реестром |
| `raw/ws-proxy-plugin/files/README.md` | Однострочное назначение и заявление об основе Flowseal | README не описывает настройку, протокол, требования или лицензию; Flowseal-код отдельно не сравнивался |
| `raw/ws-proxy-plugin/files/tg_ws_proxy.plugin:1-1136` | Весь единственный plugin entrypoint: metadata, маршрутизация, framing, thread/loop, settings, host callbacks | Внешние реализации `BasePlugin`, `SharedConfig`, `ConnectionsManager` и host behavior не входят в это дерево |
| `raw/ws-proxy-plugin/radar-context.md`, `radar-urls.json` | Сопоставление утверждений радара и фактического URL | Радар вторичен; отдельные исторические commit URLs отсутствуют, поэтому версии алгоритма Flowseal и историю до/после SHA не сверяли |

В сохранённом source tree нет отдельных tests, build/CI, манифеста разрешений, документации API или LICENSE. Отсутствие файлов подтверждено только для этого короткого дерева, а не для всех публикаций автора. Имена Android/Telegram API ниже цитируются как call-sites плагина; их сигнатуры и совместимость с AyuGram/exteraGram этим источником не устанавливаются. Независимый запрос к GitHub API для commit `c292816de3139634e62388aa78d0abcfbcadc27c` подтвердил SHA дерева и оба blob SHA из `tree.json`; локальные Git blob SHA и SHA-256 также совпали с деревом и manifest.

## Архитектура и поведение, видимое в коде

### Вход в плагин и настройки

`Hook` — пустой подкласс `WsProxyPlugin`, переданный как `__plugin__`. При `on_plugin_load()` код стартует daemon-поток со своим asyncio loop и сервером, запускает отдельный daemon-поток обновления доменов и спустя 0,5 с включает proxy клиента. События `AppEvent.START` и `RESUME` повторно вызывают включение. При unload отключается proxy клиента, loop получает callback остановки, задачи отменяются, поток ожидается до 2 секунд. Исключения API и цикла во многих местах проглатываются.

Listener привязан к `127.0.0.1:1081`. `enable_client_proxy()` вызывает `SharedConfig.loadProxyList/addProxy/saveConfig`, меняет `SharedConfig.currentProxy`, затем вызывает `get_connections_manager().setProxySettings(...)` и уведомляет `NotificationCenter.proxySettingsChanged`. Disable сбрасывает `currentProxy`, если его address равен `127.0.0.1`, и отдельно вызывает `setProxySettings(False, ...)`. По коду это глобальная настройка host-клиента, без явного account ID. `create_settings()` объявляет один `Switch(key="auto_start", default=True)`, но чтения этого ключа нет в сохранённом исходнике: из snapshot нельзя заключить, что переключатель управляет lifecycle.

`on_plugin_load()` запускает отдельный daemon-поток обновления доменов. Его внутренний `while True` не имеет stop-события, а `on_plugin_unload()` его не останавливает; повторные загрузки могут оставить несколько таких потоков. Это видно статически и не проверялось на реальном lifecycle.

### SOCKS5 и выбор маршрута

`handle_client()` читает greeting версии 5, потребляет заявленный список методов и сразу отвечает методом no-auth (`05 00`); проверку, что клиент предлагал этот метод, код не показывает. Затем принимается только команда CONNECT; адрес назначения декодируется из IPv4, доменного имени или IPv6. Неподдержанная команда получает SOCKS reply `0x07`, неизвестный тип адреса — `0x08`. Для IP, который не попадает в заданные Telegram ranges, плагин открывает прямое TCP-соединение к запрошенным host/port и ретранслирует байты в обе стороны.

Для Telegram IP плагин подтверждает SOCKS CONNECT, читает первые 64 байта и пытается распознать MTProto obfuscated init: Java `AES/CTR/NoPadding` используется для чтения protocol tag и DC id из зашифрованного префикса. Известные адреса `_IP_TO_DC` имеют приоритет над расшифрованным DC; для таких адресов DC в obfuscated init патчится. Поддержанные теги — abridged `0xEFEFEFEF`, intermediate `0xEEEEEEEE` и padded-intermediate `0xDDDDDDDD`; признаки media-соединения берутся из знака DC в init или IP mapping. Для HTTP-методов проверка выполняется после чтения этих 64 байт и обработчик просто завершает соединение.

Классификатор Telegram принимает строку адреса через IPv4 `inet_aton` и проверяет числовые IP ranges. Если SOCKS client передаёт hostname ATYP=3, `_is_telegram_ip` вернёт `False` при разборе hostname, после чего запрос пойдёт по общей прямой TCP ветке. Это описывает именно routing по данному call-site, не runtime-эффект для конкретного host resolver.

Для определённого DC `RawWebSocket.connect(target_ip, domain)` устанавливает TLS на порт 443 к IP, отправляет вручную HTTP/1.1 Upgrade на `/apiws`, с Host, WebSocket v13, `binary`, Origin `https://web.telegram.org` и жёстко заданным Firefox/Android User-Agent. В обычном маршруте выбираются `kws{dc}.web.telegram.org` и `kws{dc}-1.web.telegram.org` (для media обратный порядок). Код принимает статус 101, а redirect ответы отмечает отдельно.

`RawWebSocket` самостоятельно кодирует и читает WebSocket frames: исходящие бинарные frames маскируются; входящие masked/unmasked payload читаются; ping вызывает pong, close подтверждается close, pong игнорируется. Handshake принимает любой HTTP-ответ со статусом 101, не проверяя `Sec-WebSocket-Accept`; проверка TLS-сертификата и hostname также отключена выше. Обработчик возвращает payload каждого frame отдельно и не собирает fragmented message/continuation frames. Потоки TCP↔WebSocket обслуживаются двумя asyncio tasks, завершаются по первой закончившейся задаче и затем закрывают обе стороны. `MsgSplitter` ведёт AES-CTR decrypt state по init, читает длины MTProto-пакетов, но возвращает исходные зашифрованные байты; splitter используется для границ отправляемых WebSocket frames, не для расшифровки payload приложения.

### Пулы, домены и fallback

`_WsPool` хранит до четырёх idle соединений на пару (DC, media), удаляет закрытые/старше 120 секунд и греет пулы при старте asyncio loop для DC 1–5. Попытка пула сначала задаёт SNI `sprinthost.ru`, после исключения пробует обычный `server_hostname=domain`. `report_success()` пустой. В памяти также есть cooldown для DC (60 секунд), IP (3600 секунд) и WebSocket timeout (обычно 5 секунд, 2 секунды при недавнем отказе).

Для неизвестной маршрутизации или отказа основного WebSocket `_do_fallback()` последовательно содержит: (1) попытку `_CfWorkerPool.get()`; (2) попытку `/apiws?dst=<DC-IP>&dc=<dc>` по `_worker_domains`; (3) `kws{dc}.<domain>` через `_balancer`; (4) обычный TCP напрямую на сохранённый DC IP и 443. В этом pinned файле метод `_CfWorkerPool.set_domains()` объявлен, но вызовов его нет: `_worker_domains` создаётся пустым, а обновление endpoint-ов вызывает только `_balancer.update_domains_list()`. Поэтому две первые ветви имеют пустой список доменов в показанном исходнике; configured domain-backed fallback — ветвь `kws{dc}.<domain>`. `_dd()` преобразует список закодированных доменов и suffix; query с случайными 7 буквами добавляется к URL. Стартовое значение — встроенный список; сетевые исключения молча пропускаются, а новый список принимается только при наличии хотя бы трёх записей.

Есть ещё ограничение вне известного списка DC: `_dc_from_init()` допускает значения до 1000, но `dc_opt`/`DC_DEFAULT_IPS` содержит только DC 1–5. Для такого распознанного DC вызывается `_do_fallback()`, который сразу возвращает `False`, если для DC нет `DC_DEFAULT_IPS` адреса; после уже отправленного SOCKS success handler закрывает клиента. Это не универсальный fallback для всех DC.

В коде `_ssl_ctx` создаётся через `ssl.create_default_context()`, затем hostname checking выключается и `verify_mode` задаётся в `ssl.CERT_NONE`; это прямой факт реализации и не является оценкой безопасности или подтверждением доверенного peer. Для прямых не-Telegram TCP-соединений отдельный TLS слой плагин не добавляет.

## Точки вызова

| Компонент | Вызов / сигнатура | Назначение и lifecycle | Evidence |
|---|---|---|---|
| Entrypoint | `__plugin__ = Hook`; `class Hook(WsProxyPlugin)` | Host загружает подкласс `BasePlugin`; в файле только Android embedded Python контекст | [metadata и Hook](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L14-L30), [entrypoint](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L1133-L1136) |
| Plugin lifecycle | `on_plugin_load()`, `on_app_event(event_type)`, `on_plugin_unload()` | Запуск сетевого listener/domain updater, включение proxy на START/RESUME, отключение и остановка loop; вызывается host | [lifecycle](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L890-L929) |
| Settings | `create_settings() -> list` | Единственный UI control — switch `auto_start`, default `True`; код не читает сохранённое значение | [settings](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L930-L935) |
| Host proxy state | `SharedConfig.addProxy/ currentProxy/ saveConfig`; `ConnectionsManager.setProxySettings(...)`; `NotificationCenter.proxySettingsChanged` | Изменение глобальной proxy-конфигурации host-клиента при plugin lifecycle; отдельная account-параметризация отсутствует в call-site | [host calls](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L857-L888) |
| Local SOCKS server | `asyncio.start_server(self.handle_client, '127.0.0.1', 1081)` | Listener принимает loopback TCP-клиентов в plugin-owned event loop/thread | [server](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L916-L929) |
| SOCKS routing | `handle_client(local_reader, local_writer)` | SOCKS5 CONNECT parse; прямой TCP relay либо Telegram DC/WebSocket branch | [request dispatch](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L936-L1019) |
| MTProto init | `_dc_from_init(data)`, `_patch_init_dc(data, dc)`, `MsgSplitter(init_data, proto_int)` | Расшифровка obfuscated init metadata, коррекция DC поля для mapped IP, packet-boundary splitting | [init and splitter](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L211-L360) |
| WebSocket transport | `RawWebSocket.connect(ip, domain, path='/apiws', timeout=20.0, sni=None)`; `send/recv/close` | TLS + ручной HTTP upgrade, WebSocket binary/control frames; все операции asyncio | [connect and frames](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L385-L532) |
| Pool / fallback | `_WsPool.get(...)`, `_CfWorkerPool.get(...)`, `_do_fallback(...)` | Warm idle transports, переключение между endpoint-ами и прямым TCP | [pools](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L536-L692), [fallback](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/blob/c292816de3139634e62388aa78d0abcfbcadc27c/tg_ws_proxy.plugin#L785-L844) |

## Практические приёмы, переносимые как идеи

- Для сетевого plugin-прототипа можно выделить host integration (proxy settings), локальный transport endpoint, protocol classifier, основной transport и fallback в отдельные методы. Здесь это разделение видно по `WsProxyPlugin`, `handle_client`, `RawWebSocket`, pools и `_do_fallback`; совместимость такой архитектуры с иным клиентом нужно подтвердить отдельно.
- Долгую работу можно держать в отдельном daemon thread с отдельным asyncio loop, передавая stop callback через `loop.call_soon_threadsafe`; исходник не показывает runtime-проверку гонок, остановки каждого потока или повторной загрузки.
- При потоковом forwarding packet framing должен учитывать чтение произвольных TCP chunks: `MsgSplitter` накапливает ciphertext и вычисляет границы по расшифрованной длине, после чего сохраняет исходные encrypted bytes. Это техника именно этого MTProto-пути, не общий decoder.
- Пулы ограничивают простой и возраст, а endpoint fail cooldown отделён от pool warmup. Для сходной реализации нужно также проверить cancellation, исчерпание очереди и судьбу фоновых задач; в этой версии `report_success()` пустой и систематические тесты отсутствуют.
- В качестве источника endpoint-списка есть встроенный seed плюс периодическое обновление и минимальный порог количества значений. Код не закрепляет внешний branch URL на commit, поэтому содержимое после fetch изменяемо относительно source SHA.

## Что говорит и чего не доказывает радар

Радар называет файл «полноценным WebSocket-транспортом», сообщает о рабочем примере, основанном на Flowseal, и рекомендует отдельный code/security review до установки. Код подтверждает наличие SOCKS5 listener, MTProto DC classifier и WebSocket implementation, но для обозначенного в коде `/apiws?dst=...` worker route домены не назначаются пулу в этом файле. Рабочее соединение, производительность, версия клиента, заявленное покрытие всего Telegram трафика и совместимость с конкретными сборками остаются утверждениями радара/README, не подтверждёнными запуском в этом сборе. Наличие вызовов `SharedConfig` и `ConnectionsManager` показывает точки интеграции в коде, но не публичный или стабильный API. Radar URL не содержит исторических commit-ссылок; отдельное сравнение с Flowseal upstream не выполнялось.

## Незаполненные пробелы

- Статический snapshot не устанавливает успешность SOCKS negotiation, TLS/WebSocket handshake, MTProto DC decoding, fallback и host proxy переключений на живом клиенте; runtime-проверок и тестов не было.
- Протокольное поведение WebSocket fragmentation и проверка handshake response не покрыты тестами; исходник не собирает continuation frames и не проверяет `Sec-WebSocket-Accept`.
- Background domain updater не имеет видимого stop path при unload; частота/число оставшихся потоков после циклов load/unload не измерялись.
- Нет source-tree evidence об Android permissions, потоковых гарантиях host API, UI потоке, поведении разных аккаунтов, поддержке заданного `__min_version__` или ограничениях Python runtime клиента.
- Источник заявляет основу Flowseal, а динамический список доменов загружается из `main`; upstream-версия и отдельные исторические ревизии не зафиксированы. Поэтому точное происхождение каждой реализации и постоянство удалённых worker endpoints не определены.
- `license` в captured repository metadata равен `null`; явного LICENSE в зафиксированных двух файлах нет. Право повторного использования/распространения по этому snapshot не устанавливается.
- Внешнее изменение кода отсутствует: страница — описание источника, а не code/security review и не руководство к установке.
