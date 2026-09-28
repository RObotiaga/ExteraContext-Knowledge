---
type: review
source_id: ws-proxy-plugin
reviewer: /root/review_ws_proxy_plugin
model: gpt-6-luna
verdict: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: `tg_ws_proxy.plugin`

**Вердикт: `accepted-with-gaps`.** Сверен pinned snapshot `ReaIRyanGosling/tg_ws_proxy.plugin` на commit [`c292816de3139634e62388aa78d0abcfbcadc27c`](https://github.com/ReaIRyanGosling/tg_ws_proxy.plugin/commit/c292816de3139634e62388aa78d0abcfbcadc27c). Проверка была отдельной от сбора и ограничена статическим чтением; плагин не запускался, не собирался и не устанавливался.

## Provenance и охват

Независимый GitHub API запрос вернул этот же commit SHA, tree SHA `8b6138da600efd80c7620ea6efd27bb5d4b90c97`, полный tree из двух файлов и те же blob SHA: README `8f5ac1e2b71a1186c5d43829271df71a440c60ea`, entrypoint `220dea62597464fbc9d55d659efe2fa8a98b3c26`. Пересчитанные SHA-256 обоих локальных файлов совпали с `file-manifest.json`; также независимо рассчитанные Git blob SHA совпали с tree. Репозиторий/ветка/commit соответствуют радару. Сохранены и проверены оба первичных файла: `README.md` и весь `tg_ws_proxy.plugin` (строки 1–1136). `radar-context.md` рассмотрен как вторичный источник, а `radar-urls.json` подтверждает URL репозитория. README сообщает о назначении для AyuGram/exteraGram и основе Flowseal; сам upstream Flowseal не сравнивался, поэтому lineage реализации не подтверждён.

Охват кода включает metadata и entrypoint, hooks и settings, host proxy calls, SOCKS5 parsing/routing, MTProto init decode/patch, packet splitter, TLS/HTTP upgrade, WebSocket frames, TCP/WS bridges, оба пула, fallback, cooldown и remote domain refresh. Для worker pool отдельно прослежены setter и все call sites. В дереве нет дополнительных API docs, tests, build/CI, permissions manifest или LICENSE. Сигнатуры `BasePlugin`, `SharedConfig`, `ConnectionsManager` и callbacks описывают call-sites этого файла, а не нормативную документацию клиента.

## Найденные проблемы и исправления

- Подтверждено существенное состояние worker pool: `_CfWorkerPool._worker_domains` создаётся пустым; `set_domains()` не вызывается ни в одном месте pinned файла. Refresh обновляет `_balancer`, но не worker pool. Поэтому pool-backed worker и прямой `/apiws?dst=...` путь не имеют доменов и пропускаются; после них остаётся domain-backed `kws{dc}.<domain>` ветвь. Страница и fact уточняют, что речь о статическом кодовом пути, а не проверенном серверном результате.
- Добавлен lifecycle gap: refresh daemon thread заходит в `while True`, не принимает stop-сигнал, а unload его не останавливает. После повторных load возможны дополнительные потоки. Это статический вывод; число потоков в runtime не измерялось.
- Добавлен протокольный gap: handshake принимает статус 101 без проверки `Sec-WebSocket-Accept`; frame reader не собирает continuation frames в сообщение. Транспорт не проходил interoperability tests.
- Уточнён отказ для DC: init decoder допускает DC до 1000, таблица fallback endpoint-ов содержит только DC 1–5. Для распознанного значения вне таблицы `_do_fallback()` возвращает `False`; SOCKS CONNECT уже был подтверждён, затем handler закрывает соединение.
- Подтверждены и сохранены остальные важные ограничения: TLS certificate/hostname verification отключены; `auto_start` switch не читается; no-auth ответ отправляется без видимой проверки предложенного метода; hostname SOCKS target не попадает в Telegram IPv4 classifier и направляется напрямую; HTTP transport отбрасывается после чтения 64 байт; `report_success()` пустой. Описания не называют их runtime findings.
- Сведения о Flowseal и «рабочем» транспорте оставлены как README/radar claims с соответствующим evidence status. Сам снимок не доказывает совместимость с актуальными версиями клиента или работоспособность сети.

## Факты и повторы

В `work/ws-proxy-plugin-facts.json` теперь **36 фактов с 36 уникальными ID**. Внутри набора точных дублирующих claims нет: hostname ATYP=3 был объединён с более общим claim о прямой TCP ветке и особенностях её классификатора. По точным claim и тематическому поиску в имеющемся глобальном facts-каталоге точных повторов из других источников не найдено; общие темы proxy transport у других источников оставляются с отдельным provenance. Каноническая тема для последующего сведения: `network-proxies`; дополнительные темы — `lifecycle`, `threading`, `security`, `accounts`, `testing`.

## Остаточные пробелы

- Не установлены runtime-результаты SOCKS negotiation, handshake, Telegram DC decode, pool reuse, fallback, worker endpoints, thread cleanup или proxy switching на AyuGram/exteraGram.
- Не проверены host API declarations/гарантии, account semantics, Android runtime/Python compatibility и минимальная версия клиента.
- Не выполнено сравнение с Flowseal на pinned upstream commit; remote domain list адресует изменяемую ветку `main`.
- `license: null` в repository metadata и отсутствие LICENSE в полном зафиксированном tree означают, что право повторного использования/распространения этим snapshot не установлено.
- Отсутствие тестов/build/CI подтверждено только для этого двухфайлового pinned tree. Вывод не гарантирует абсолютную полноту за пределами изученного snapshot.

Source page обновлена и связана с этим review. Pipeline verdict: `accepted-with-gaps`.
