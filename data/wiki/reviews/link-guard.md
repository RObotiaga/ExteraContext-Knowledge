---
type: review
source_id: link-guard
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: L0lopop/Link-Guard

- Вердикт: **accepted-with-gaps**.
- Проверен snapshot `b9cd180c83b47a724970e026f64ec8039cc0f650` (`main`, сохранён 2026-09-27). SHA совпадает в `snapshot.json`, `tree.json`, source page и pinned GitHub permalinks. Дерево полное (`truncated=false`): 17 tracked blobs; все 11 сохранённых текстовых source blobs соответствуют `file-manifest.json` по SHA-256 и размеру. В снимке также есть `.gitignore` и пять графических assets, которые не добавляют сведений о plugin API/поведении.
- Радарный контекст и `radar-urls.json` сверены отдельно: последний содержит только URL репозитория, historical commit URL нет. Primary evidence — pinned source/docs/tests, а радар использован только для старой версии `1.4.1` и исторической оценки базы. Исходник, тесты и workflows не запускались; никаких build/install/runtime результатов этой проверкой не заявляется.

## Покрытие и проверка claims

Независимо сверены все релевантные сохранённые blobs: `README.md`, `README.ru.md`, `LICENSE`, `update.json`, `src/link_guard.plugin`, `scripts/build_db.py`, оба workflow (`feeds.yml`, `keepalive.yml`), оба тестовых файла (`test_link_guard.py`, `test_db_format.py`) и `state/manifest.json`; также проверены `snapshot.json`, `tree.json`, `file-manifest.json`, `repository.json`, `radar-context.md` и `radar-urls.json`. В коде сверены metadata и import fallbacks, settings/defaults, полный набор функций плагина, URL parser/heuristics/cleaner, DB parser и refresh, network helpers, updater, hook installation/callbacks, source/anchor caches, open/reopen/dialog flows, outgoing hook, message menus и unload path. Для сборщика базы сверены feed definitions, gates, popular-domain/service/platform filters, output sections и workflow publication; документационные обещания отделены от code evidence.

Радар говорит о версии `1.4.1` и примерно `2,84 млн` записей. Закреплённые entrypoint и `update.json` указывают `1.7.0`, а `state/manifest.json` фиксирует срез `2026-09-12` с 2 984 804 адресами и семью успешными feeds. README описывает более 3 млн записей и одиннадцать публичных списков; source script на этом SHA содержит девять feed-ов без ключа и до трёх keyed feed-ов. Это несовпадающие временные/режимные заявления, не одна подтверждённая текущая цифра.

Сверены названные API и диапазоны строк в source table и JSON facts. `BasePlugin`, hooks, settings controls и helpers показаны только как используемые call-sites; `Browser.openUrl`, `TL_update*` и Telegram/Android classes помечены как client internals. В facts нет утверждений `runtime-verified`, итоговая схема статусов допустима, а локальные permalinks закреплены на snapshot SHA. Исправлена одна ошибочная граница evidence: manifest заканчивается строкой 54, не 55.

Проверка выявила и добавила существенные детали: whitelist завершает анализ до MALW lookup и эвристик; `URL_RE` принимает `tg://`, но analyzer возвращает пустой verdict для схемы `tg`; `account` из update callbacks не передаётся в определение источника, а contact lookup использует `get_messages_controller()` без явного аккаунта; README описывает reduced mode старого клиента и ограничение удаления whitelist через long-press, но metadata указывает `>=12.1.1`; база исключает top 50 000 популярных имён и использует top 200 000 для подавления части эвристик, при этом найденный MALW имеет приоритет. Детали отражены в source page и фактах с соответствующим статусом evidence.

В facts был повтор: `link-guard-029` повторял ограничение outgoing entities из `link-guard-013` и menu coverage из `link-guard-014`. Он объединён в `link-guard-013`. Для `link-guard-023` недопустимая тема `permissions` заменена на `security`. Внутренние факты имеют уникальные ID; после исправлений — **32 уникальных факта**. Повторение этих знаний в других source records допустимо как отдельная provenance. При тематическом сведении исходящие entities относятся к канонической теме hooks; whitelist и схемы URL — security; источники сообщений и multi-account caveat — accounts; очистка URL — network.

## Остаточные пробелы

1. Нет определений host Plugin API/helpers в этом репозитории и нет конкретного host APK; поэтому точные overload contracts, lifecycle/thread semantics и runtime account selection не подтверждены.
2. Поддержка схемы `tg` анализатором отсутствует в pinned code; как клиент фактически открывает такой URI и какие другие `Browser.openUrl` пути обходят hook, не проверялось.
3. README описывает reduced mode старых клиентов, но metadata задаёт minimum app version `>=12.1.1`; доступность старых версий и long-press settings на конкретных сборках не установлена.
4. Нет runtime/device-проверки hook, UI, permissions, сетевого поведения, shortener/RDAP ответов, атомарной установки обновлённой базы или plugin update/install flow. Проверка загруженного plugin файла по ID/version в первых 4096 байтах не является подписью.
5. Живые threat feeds и release artifact не входят в pinned source tree; manifest исторический. Фактическая будущая база, её содержание, feed доступность и текущий release размер неизвестны.
6. README sample commands и CI не исполнялись. Статическое чтение тестов показывает намерения и проверки в stubs/fixture data, но не подтверждает, что тесты проходят на этом окружении или что клиент работает.
7. Проверка статическая и относится к одному SHA; она не даёт гарантии для другого commit, SDK или версии клиента.

Source page получила `review_status: accepted-with-gaps` и ссылку на этот отчёт. Эта оценка принимает покрытие источника для справочной базы при явно сохранённых границах, но не означает runtime acceptance или гарантию абсолютной полноты для внешнего host API.
