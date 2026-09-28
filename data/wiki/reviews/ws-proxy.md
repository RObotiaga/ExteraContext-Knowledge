---
type: review
source_id: ws-proxy
reviewer: /root/review_ws_proxy
model: gpt-6-luna
verdict: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: `Flowseal/tg-ws-proxy`

**Вердикт: `accepted-with-gaps`.** Независимо сверена standalone-программа `Flowseal/tg-ws-proxy` на commit [`caa949bee0873d2b95dfb4fbeb1b7868b0ee3843`](https://github.com/Flowseal/tg-ws-proxy/commit/caa949bee0873d2b95dfb4fbeb1b7868b0ee3843). Сборщик — `/root/collect_ws_proxy`; эту проверку провёл отдельный reviewer `/root/review_ws_proxy`. Исходник не запускался, тесты не выполнялись, проект не собирался и не устанавливался.

## Provenance и границы источника

`repository.json`, `snapshot.json`, `tree.json`, `file-manifest.json`, `radar-context.md` и `radar-urls.json` сверены друг с другом: репозиторий — `Flowseal/tg-ws-proxy`, ветка `main`, snapshot указывает SHA `caa949bee0873d2b95dfb4fbeb1b7868b0ee3843`, полученный 2026-09-27; сохранённый полный tree не помечен truncated. В metadata лицензия обозначена как MIT; захваченный `LICENSE` содержит текст MIT с copyright Flowseal 2026. Для всех 75 сохранённых файлов независимо пересчитаны SHA-256, длина и Git blob SHA: они совпали с `file-manifest.json` и соответствующими blob IDs в pinned `tree.json`. Таким образом подтверждены выбор commit, целостность локального набора и license evidence. Это не устанавливает происхождение каждой строки кода от упомянутого upstream `Nekogram/WSProxy`.

Самостоятельно прочитаны связанные снимки: `docs/EN/README.md`, `BuildFromSource.md`, `CfProxy.md`, `CfWorker.md`, `TestDc.md`, `TrayConfig.md`; core `proxy/tg_ws_proxy.py`, `bridge.py`, `raw_websocket.py`, `pool.py`, `config.py`, `utils.py`, `fake_tls.py`, `_aes.py`, `balancer.py`; все шесть сохранённых `tests/test_*.py`; а также `pyproject.toml`, `utils/default_config.py`, `utils/diagnostics.py`, `utils/logging_setup.py`, `utils/tray_common.py`, `utils/update_check.py`, tray entry points/UI и локали. Радар использован как контекст, а не как доказательство реализации.

Tree содержит 90 файлов, из них приобретено 75. Не получены Dockerfile, три packaging spec, скрипт сборки DMG, изображения/иконки и несколько служебных dotfiles/assets. Это не закрывает детали binary packaging и release matrix; таблица покрытия source page ограничивает соответствующие выводы просмотренными docs, `pyproject.toml`, workflow и entry points. Все requested areas — handshake, routing/fallback, WebSocket frames, pools/configuration — представлены в сохранённых исходниках.

## Проверка покрытия и исправления

Независимо прослежен путь от obfuscated2 handshake до классификации DC/media/protocol, генерации relay init и crypto contexts; обычный и test DC routing; direct WS и редиректы/cooldowns; Worker/CF/TCP fallback; splitter и обе стороны bridge; direct/Worker pool, refresh и конфигурационные defaults/CLI. Прочитаны framing/control logic, pool failure/refill logic и вызовы их основных consumers. Конфигурационные инструкции сверены с соответствующими README страницами. Набор локальных тестов проверен только чтением и не служит результатом их прохождения.

Найдены и исправлены следующие места:

- Fact `ws-proxy-004` теперь различает отсутствующий secret (генерируется) и неверный переданный secret (CLI завершает работу с ошибкой), вместо возможного прочтения «иначе сгенерировать».
- В `ws-proxy-008` transport tag назван `padded-intermediate`; `PROTO_TAG_SECURE` — имя константы в этом исходнике.
- В `ws-proxy-013` и source page добавлено, что ответ 101 принимается без сверки `Sec-WebSocket-Accept`.
- Добавлена документированная граница Worker example: query `dst` напрямую подаётся в `connect` и пример не показывает валидацию/allowlist назначения. Это предупреждение о snippet, не утверждение о проверенном или развёрнутом Worker.
- Добавлено точное TLS caveat: при явном `sni` выбирается SSL context с `check_hostname=False`; стандартная проверка цепочки сертификатов остаётся включена.
- Формулировки `ws-proxy-001` и `ws-proxy-032` сужены, чтобы разделить идентичность standalone-инструмента и его README route/defaults.

## Факты и разделение источников

В `outputs/plugin-wiki/work/ws-proxy-facts.json` **35 фактов с 35 уникальными ID**. В наборе не осталось точных повторов; overlap вокруг standalone identity/default port устранён уточнением claims. Пересечения с `ws-proxy-plugin` относятся к похожей транспортной схеме, но это отдельный репозиторий с другой реализацией, портом, runtime и host integration. Источник Flowseal не доказывает вызовы `BasePlugin`, Android lifecycle или plugin API, а детали большого `.plugin` не переносятся на Python proxy. Оба источника должны сохранить отдельные provenance; сводить общие правила позже в канонической теме `network-proxies`.

## Остаточные пробелы

- Не установлены runtime-работа TLS/WebSocket handshake, MTProto relay, redirect routing, fallback, pool reuse, Cloudflare Worker или Telegram Desktop.
- Тесты не запускались; ни одно code-reading наблюдение не имеет статуса `runtime-verified`.
- Не изучены не приобретённые Docker/package files и подробности сборки binaries; также не проверялись изменяемый remote domain list, текущие внешние endpoint-ы, Cloudflare ограничения или Telegram-side поведение.
- Не выполнена security review реализации/системы. Обнаруженные framing/TLS/Worker caveats описаны как свойства кода/docs и не доказывают эксплуатационную уязвимость либо конкретный сетевой результат.
- Не сделано отдельное построчное сравнение с `Nekogram/WSProxy`; lineage остаётся заявлением upstream автора.

Source page получила `review_status: accepted-with-gaps` и ссылку на этот отчёт. Pipeline verdict: `accepted-with-gaps`.
