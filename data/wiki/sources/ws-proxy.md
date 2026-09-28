---
type: source
source_id: ws-proxy
platform: tool
review_status: accepted-with-gaps
review: ../reviews/ws-proxy.md
date: 2026-09-28
---

# Flowseal/tg-ws-proxy — локальный MTProto-to-WebSocket bridge

Источник: [Flowseal/tg-ws-proxy](https://github.com/Flowseal/tg-ws-proxy), ветка `main`, снимок зафиксирован на commit [`caa949bee0873d2b95dfb4fbeb1b7868b0ee3843`](https://github.com/Flowseal/tg-ws-proxy/commit/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843), полученный 2026-09-27. Метаданные репозитория и файл `LICENSE` называют лицензию MIT. Snapshot/tree/file manifest сохранены в [raw/ws-proxy](../../raw/ws-proxy/); SHA-256 каждого приобретённого файла записан в `file-manifest.json`. Пиннутый GitHub-файл с лицензией подтверждает commit и текст MIT; закреплённый файл реализации доступен по [proxy/tg_ws_proxy.py](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/tg_ws_proxy.py).

## Роль источника и границы

Это самостоятельная Python-программа, принимающая локальные MTProto-соединения Telegram Desktop и направляющая их через Telegram WebSocket endpoint, Cloudflare proxy/Worker или TCP fallback. Это не ExteraGram/AyuGram-плагин, SDK или API клиента. Упомянутый радаром большой `.plugin` — отдельный репозиторий/источник `ws-proxy-plugin`; его реализация сюда не переносится и здесь не подтверждается. Поэтому сведения ниже полезны для сопоставления транспортной идеи и формата протокола, но не дают основания считать Python API доступным внутри `BasePlugin`.

Изучен именно сохранённый commit, а не актуальная ветка `main`. Код и tests только читались: прокси не запускался, CI и тесты не выполнялись, сетевые конечные точки не проверялись, работа в Telegram Desktop или на устройстве не подтверждена. Документационные инструкции по развёртыванию — утверждения авторов источника, не результаты этой работы.

## Покрытие снимка

| Прочитанный путь в снимке | Извлечено | Границы и пробелы |
|---|---|---|
| `snapshot.json`, `repository.json`, `tree.json`, `file-manifest.json`, `radar-context.md`, `radar-urls.json` | Идентичность репозитория, точный SHA, набор полученных файлов, роль источника в радаре | Radar использован только для идентификации и постановки границ; его архитектурные утверждения отдельно не считаются фактом об этом проекте |
| `docs/EN/README.md:36-142`, `docs/EN/BuildFromSource.md:1-78` | Назначение, схемы маршрута и конфигурации, CLI/точки входа, поддерживаемые упаковочные сценарии | Не собирал бинарные файлы; заявленная поддержка ОС не проверялась |
| `docs/EN/CfProxy.md:1-32`, `docs/EN/CfWorker.md:1-129`, `docs/EN/TestDc.md:1-23`, `docs/EN/TrayConfig.md:1-32` | Авторские инструкции для пользовательского домена/Worker, тестовых DC и сохранения настроек | Развёртывание Cloudflare, DNS, DPI и Telegram-клиента не выполнялось; ограничения зависят от внешних сервисов и могут изменяться |
| `proxy/tg_ws_proxy.py:1-767` | Разбор obfuscated init, DC/media/protocol, связка crypto-контекста, асинхронная обработка клиента, соединение/fallback, listener lifecycle, CLI | Статический анализ одного файла и вызовов его подсистем; криптографическая корректность и совместимость не тестировались |
| `proxy/bridge.py:1-431`, `proxy/raw_websocket.py:1-292` | Разбиение MTProto-пакетов на WebSocket frames, пересылка/перешифрование, реализация WebSocket handshake/framing/control и предел размера | Это реализация прокси, не официальный протокол или API плагинов |
| `proxy/fake_tls.py:1-256`, `proxy/_aes.py:1-132` | Проверка и обёртка Fake TLS, совместимый AES-CTR слой | Не выполнялась security review; внешний вид TLS не доказывает незаметность или криптографическую безопасность |
| `proxy/config.py:1-220`, `proxy/utils.py:1-152`, `proxy/balancer.py:1-43`, `proxy/pool.py:1-355`, `proxy/stats.py:1-43` | Defaults, нормализация и получение доменов, DC maps, TLS helper, выбор домена, preconnect pools, counters | Не проверялись внешние URL/домены в эксплуатации. В `pool.py` есть явные TODO, отмеченные ниже |
| `tests/test_bridge.py:1-116`, `tests/test_config.py:1-87`, `tests/test_fake_tls.py:1-133`, `tests/test_pool.py:1-53`, `tests/test_raw_websocket.py:1-130`, `tests/test_update_check.py:1-70` | Прочитаны сценарии и ожидаемые локальные контракты для splitter, парсинга, Fake TLS, pool refill, framing и разбора update metadata | Тесты не запускались; тестовые ожидания не являются runtime-доказательством |
| `pyproject.toml:1-82`, `windows.py`, `macos.py`, `linux.py`, `utils/default_config.py`, `utils/diagnostics.py`, `utils/logging_setup.py`, `utils/tray_common.py`, `utils/update_check.py`, `ui/ctk_tray_ui.py`, `ui/i18n/*`, packaging и GitHub Actions | Packaging entry points/dependencies проверены; tray/default-config/update/logging/diagnostics/локализация и workflow просмотрены на уровне путей и основных связей | UI-поведение, все release matrix детали, platform-specific ветки и каждый helper не описаны построчно; CI не запускался |

## Архитектура и транспортные факты

### Начало соединения и декодирование MTProto

- CLI по умолчанию слушает `127.0.0.1:1443`; секрет создаётся как 16 случайных байт в hex или проверяется как ровно 32 hex-символа. Для Telegram Desktop README указывает локальный MTProto proxy с тем же портом; настройки `ProxyConfig` включают таблицу DC→IP, размеры socket buffer и pool, CF/Worker fallbacks, Fake TLS, PROXY protocol и force-test-DC.
- `asyncio.start_server` создаёт задачу `_handle_client` для каждого нового подключения. При завершении listener watchdog замечает закрытые sockets и пытается поднять listener снова; при переданном `stop_event` сервер отменяет клиентские tasks, закрывает listener и очищает задачи статистики.
- Входной handshake — 64 байта obfuscated2. Код получает pre-key и IV из байтов после 8-байтового skip, получает AES key как `SHA256(prekey + secret)`, расшифровывает и проверяет transport tag; отрицательный signed DC index трактуется как media, а абсолютное значение — DC ID. Поддерживаются abridged, intermediate и padded-intermediate tags.
- Relay-init генерируется заново как 64 случайных байта с отбрасыванием зарезервированных сигнатур. Тег протокола и signed DC index шифруются в соответствующую область начального пакета. Затем `_build_crypto_ctx` создаёт отдельные AES-CTR encrypt/decrypt contexts для клиента и Telegram, чтобы bridge переводил шифрование между двумя сторонами.
- Test DC автоматически распознаются при DC ID `>=10000`; offset 10000 снимается для выбора маршрута, а `--force-test-dc` принудительно переводит номера 1–3 в test endpoints. Документация отдельно ограничивает test mode прямыми DC→IP и Worker путями.

### WebSocket и пересылка

- Прямые домены строятся из `kws{dc}.web.telegram.org` и `kws{dc}-1.web.telegram.org`; для DC 203 используется DC 2. В media-режиме порядок этих двух доменов меняется. Production path — `/apiws`, test path — `/apiws_test`.
- `RawWebSocket.connect(host, domain, timeout=10, path='/apiws', *, sni=None, secure=True)` открывает TCP/TLS к целевому IP, задаёт SNI и HTTP `Host` доменом, отправляет Upgrade с `Sec-WebSocket-Protocol: binary` и принимает любой ответ HTTP 101 без проверки `Sec-WebSocket-Accept`. Иной ответ выдаётся как `WsHandshakeError` с status/location; 3xx распознаются отдельно для переключения доменов.
- Исходящие binary frames маскируются, длина кадра кодируется стандартными short/16-bit/64-bit полями. Приём обслуживает fragmentation и ping/pong/close, ограничивает отдельный frame и собранное сообщение 16 MiB; серверные немаскированные данные принимаются.
- `MsgSplitter` расшифровывает копию потока для чтения transport-length, но сохраняет исходные ciphertext bytes для отправки: это позволяет один MTProto packet переслать отдельным WebSocket frame. Неполный packet остаётся буферизованным; abridged и intermediate framing разбираются разными ветками, padded-intermediate использует intermediate framing. Если framing не распознан/длина некорректна, splitting отключается или хвост отдаётся целиком.
- Два асинхронных направления bridge пересылают TCP↔WebSocket и преобразуют ciphertext через контексты клиента/Telegram. Читатель client→WS может сгруппировать пакеты в `send_batch`; накопленный splitter-хвост отправляется при EOF. TCP fallback использует отдельную пару потоков и те же crypto contexts.

### Выбор маршрута и восстановление

- При отсутствии заданного DC redirect, blacklisted DC/media либо проблемном таймауте доступности начинается fallback. Порядок в `do_fallback`: Worker (если задан и есть адрес назначения), обычный CF proxy (если разрешён и это не test DC), затем прямой TCP к DC:443, если известен IP.
- WebSocket redirect всех доменов для одного DC/media добавляет маршрут в runtime blacklist; некоторые ошибки/redirect включают cooldown для DC/media, timeout к target IP — отдельный IP cooldown. Успешный WS убирает cooldown этого IP и обновляет pool statistics.
- CF proxy-список встроен в обфусцированном виде. При отсутствии пользовательских доменов код загружает список с `raw.githubusercontent.com/.../main/.github/cfproxy-domains.txt`, декодирует и валидирует элементы, удаляет дубли и принимает обновление лишь при наличии как минимум трёх валидных доменов; до этого остаётся текущий/default pool. Обновление выполняется daemon thread сразу и далее каждый час.
- Документированный Worker отвечает только на WebSocket Upgrade по `/apiws`; его пример берёт `dst` из query, открывает raw TCP `dst:443` через `cloudflare:sockets` и двунаправленно связывает сокет с WebSocket. Код Python формирует для него `/apiws?dst=<DC IP>&dc=<id>`. Описание Worker — схема из документации, не доказательство успешного развёртывания.
- В коде примера Worker `dst` прямо берётся из query и передаётся в `connect({ hostname: dst, port: 443 })`; пример не показывает проверку/allowlist назначения. Это ограничение опубликованного примера, поэтому перед публичным развёртыванием его следует дополнить ограничением допустимых host.
- WS pool разделён по `(dc, is_media)`, выдаёт только живые соединения не старше 120 секунд и планирует пополнение после hit/miss. Пополнение использует экспоненциальную задержку до часа; warmup проходит по настроенным DC и обоим media flags. CF Worker pool имеет срок 100 секунд и предел одного idle соединения на DC.
- Важное ограничение из самого `pool.py`: автор оставил TODO, что неверный `is_media` при доменной обработке может дать TCP reset после handshake. В Worker pool обработчик `report_failure` сейчас сразу возвращает, а код ниже должен был выключать Worker domain при HTTP 429; автоматическое отключение по daily-limit фактически не выполняется в этом снимке.

### Fake TLS, настройки и поставка

- При `--fake-tls-domain` вход TLS ClientHello проверяется HMAC-SHA256, привязанным к proxy secret, и timestamp с допуском 120 секунд. При успешной проверке прокси отправляет синтетический ServerHello и затем читает obfuscated2 handshake из TLS-shaped stream; неверный ClientHello перенаправляется к masking domain, а не-TLS первый байт получает HTTP 301. Проверки являются описанием кода; они не доказывают сокрытие трафика от DPI.
- CLI включает `--dc-ip DC:IP` (можно повторять), `--cfproxy-domain`, `--cfproxy-worker-domain`, `--no-cfproxy`, `--no-secure`, `--fake-tls-domain`, `--force-test-dc`, `--proxy-protocol`, `--buf-kb`, `--pool-size`, `--log-file`, `--log-max-mb`, `--log-backups`, `-v`. Валидатор `--dc-ip` требует числовой DC и полный IPv4 address; повторный DC перезаписывается последним значением.
- Документация tray хранит JSON конфигурацию в `%APPDATA%/TgWsProxy`, `~/Library/Application Support/TgWsProxy`, `~/.config/TgWsProxy` либо `$XDG_CONFIG_HOME/TgWsProxy`, включая secret, DC IPs, buffers, pool size, CF toggles, update checks и UI appearance. Это desktop-приложение, не Android plugin storage.
- `pyproject.toml` объявляет Python `>=3.8`, MIT, Hatchling, зависимые Python пакеты и отдельные entry points `tg-ws-proxy`, `tg-ws-proxy-tray-win`, `tg-ws-proxy-tray-macos`, `tg-ws-proxy-tray-linux`. README заявляет binary targets Windows, macOS и Linux; наличие этих объявлений не означает, что артефакты построены или проверены здесь.
- Локальные tests описывают ожидаемые граничные случаи: произвольная chunking для splitter, отложенная обработка неполного packet, malformed/duplicate domain parsing, wrong secret/stale timestamp/tampered Fake TLS body, fragmented/oversized WebSocket message, pool refill и version parsing. Их существование не равносильно успешному прохождению.

## Вызовы, важные для сопоставления с плагином

Это интерфейсы Python транспорта из pinned source, не API ExteraGram/AyuGram.

| Модуль / объект | Сигнатура или используемый вызов | Назначение и lifecycle | Доказательство |
|---|---|---|---|
| `proxy.tg_ws_proxy` | `async def _run(stop_event: Optional[asyncio.Event] = None)`; `def run_proxy(stop_event=None)`; `main()` | Поднимает async TCP listener, ведёт client tasks, остановку и watchdog; `main` разбирает CLI и вызывает `asyncio.run` | [tg_ws_proxy.py:L473-L497](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/tg_ws_proxy.py#L473-L497), [L638-L767](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/tg_ws_proxy.py#L638-L767) |
| `proxy.tg_ws_proxy` | `async def _handle_client(reader, writer, secret: bytes)` | Один task на TCP client; handshake → DC/протокол → WS/fallback → bridge, потом закрытие клиента | [tg_ws_proxy.py:L250-L275](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/tg_ws_proxy.py#L250-L275), [L277-L442](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/tg_ws_proxy.py#L277-L442) |
| `proxy.raw_websocket.RawWebSocket` | `connect(host, domain, timeout=10.0, path='/apiws', *, sni=None, secure=True)` | TCP/TLS dial, HTTP Upgrade и доменная fronting-параметризация; отдельный WebSocket helper | [raw_websocket.py:L67-L160](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/raw_websocket.py#L67-L160) |
| `RawWebSocket` | `send(data)`, `send_batch(parts)`, `recv()`, `close()` | Binary frame I/O, control frames и сборка фрагментов; async connection lifecycle | [raw_websocket.py:L162-L221](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/raw_websocket.py#L162-L221) |
| `proxy.bridge.MsgSplitter` | `MsgSplitter(relay_init, proto_int)`, `split(chunk)`, `flush()` | Парсит длину MTProto transport packets на потоке для WS framing, не меняя передаваемые ciphertext bytes | [bridge.py:L33-L129](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/bridge.py#L33-L129) |
| `proxy.bridge` | `do_fallback(reader, writer, relay_init, label, dc, is_test_dc, is_media, media_tag, ctx, splitter=None)` | Упорядоченный выбор Worker/CF/TCP fallback, затем переиспользуемый bridge | [bridge.py:L131-L172](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/bridge.py#L131-L172) |
| `proxy.config` | `ProxyConfig`; `coerce_domain_list(value)`; `parse_dc_ip_list(dc_ip_list)` | Runtime defaults; нормализация входа доменов; проверка CLI списка DC | [config.py:L62-L79](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/config.py#L62-L79), [L82-L103](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fb1b7868b0ee3843/proxy/config.py#L82-L103), [L201-L220](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fb1b7868b0ee3843/proxy/config.py#L201-L220) |
| `proxy.config` | `start_cfproxy_domain_refresh()`; `refresh_cfproxy_domains()` | Инициализирует fallback domain pool и daemon refresh loop раз в час | [config.py:L158-L198](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/config.py#L158-L198) |
| `proxy.pool._WsPool` | `async get(dc, is_media, target_ip, domains)`; `warmup()`; `reset()` | Предварительно открытые прямые WS connections, отдельно по DC/media; пул привязан к event loop | [pool.py:L19-L110](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/pool.py#L19-L110), [L199-L219](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/pool.py#L199-L219) |
| `proxy.fake_tls` | `verify_client_hello(data, secret)`; `build_server_hello(secret, client_random, session_id)`; `FakeTlsStream` | Статический Fake TLS handshake validation/response и record-like stream abstraction | [fake_tls.py:L57-L110](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/fake_tls.py#L57-L110), [L126-L208](https://github.com/Flowseal/tg-ws-proxy/blob/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843/proxy/fake_tls.py#L126-L208) |

## Практические приёмы, переносимые только как идеи

- Разделяйте выбор маршрута и transport bridge: здесь `do_fallback` принимает состояние DC/media и вызывает несколько независимо реализованных транспортов. Для плагина эту схему можно рассматривать только как архитектурную идею; сетевые ограничения и API Android-клиента нужно исследовать отдельно.
- Если разбиваете зашифрованный поток по длинам протокола, используйте копию с отдельным decryptor только для чтения framing, сохраняя оригинальные ciphertext-срезы. Входящие chunks произвольны, поэтому храните неполный хвост между вызовами и сбрасывайте его при закрытии.
- При клиентском WebSocket отправлении маскируйте frames и корректно обслуживайте control frames, fragmentation и пределы размера; тесты в проекте фиксируют полезные крайние случаи для локального протокола.
- Для динамических endpoints нормализуйте, валидируйте и дедуплицируйте конфигурацию до смены активного пула; проект сохраняет ранее известный набор при пустом или низкокачественном ответе. Удалённый список доменов и IP в коде динамичны/операционно чувствительны и не должны копироваться в plugin как постоянная гарантия.
- Разделяйте тексты docs, поведение code, ожидаемые тестовые contracts и факты, проверенные на клиенте. Для этого источника runtime-проверок нет.

## Пробелы и оговорки радара

- Радар описывает `.plugin` с локальным SOCKS5 на порту `1081`, получение DC и TCP fallback. Это относится к отдельной реализации `ws-proxy-plugin`, не к `Flowseal/tg-ws-proxy`: README текущего источника и его CLI задают standalone MTProto proxy на `127.0.0.1:1443` по умолчанию. Не переносите порт, BasePlugin, hook или lifecycle из одного источника в другой.
- GitHub pinned raw source, commit page и LICENSE доступны; GitHub HTML tree URL вернул ограниченный fetch. Сверка выполнена по сохранённым `snapshot.json`, `tree.json`, `file-manifest.json` и открывшимся commit-pinned GitHub LICENSE/source URLs. Snapshot hash и manifest позволяют повторить выбор версии.
- Не изучались внешняя реализация Telegram DC и WebSocket endpoint, исходный upstream `Nekogram/WSProxy`, Cloudflare runtime quotas/current dashboard, сетевые ответы живых серверов и актуальные клиентские правила. Совместимость WebSocket endpoint и доступность доменов изменчивы.
- Не оценивалась безопасность прокси, сохранность секрета, модели угроз, эффективность DPI маскирования, корректность собственного криптографического слоя или последствия публичного bind. Не считать наличие `DomainCensorFilter`, TLS context или Fake TLS проверкой безопасности.
- При передаче явного `sni` WebSocket-контекст создаётся с отключённой проверкой имени сертификата (`check_hostname=False`); цепочка сертификата продолжает проверяться базовым SSL context. Режим обычного domain SNI использует контекст с hostname checking. Это описание конфигурации TLS, не оценка общего уровня безопасности.
- В примере Cloudflare Worker query-параметр `dst` не проверяется по allowlist перед TCP `connect`; пример сам по себе не ограничивает назначения. Это статическое чтение docs-кода, не проверка действующего Worker или Cloudflare сетевых ограничений.
- Статический набор tests прочитан, но не исполнен. Страница не утверждает, что тесты проходят или что описанный маршрут работает в Telegram Desktop.
