---
type: source-review
source_id: ayugram4a
reviewer: /root/review_ayugram4a
model: gpt-6-luna
verdict: accepted-with-gaps
reviewed_at: 2026-09-28
accepted_facts: 41
---

# Независимая проверка BRYCE00182/AyuGram4A

## Версия и граница проверки

Проверен `BRYCE00182/AyuGram4A`, ветка `rewrite`, pinned SHA [`0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8`](https://github.com/BRYCE00182/AyuGram4A/tree/0c3d253f39f23d7c6da6f53ac21b4d56fa3a48e8). `snapshot.json`, `tree.json` и commit evidence содержат тот же SHA; дерево имеет `truncated: false`. Манифест содержит 71 файл; независимо перепроверены существование и SHA-256 каждого локального файла — расхождений нет. В Ayu-пакете насчитывается 52 Java-файла. Источник рассматривается как Android-клиент-донор, а не SDK плагинов. Проверка не запускала приложение, сборку, тесты или workflow.

Радарный контекст из `raw/ayugram4a/radar-context.md:1469` и URL-реестр были сопоставлены со страницей источника. Утверждение радара о событии 9 сентября шире доступного commit: pinned commit сообщает `Update release.yml` и затрагивает только `.github/workflows/release.yml`; это подтверждает commit-level наблюдение, но само по себе не доказывает весь дневной диапазон. Статус `secondary` для формулировки радара сохранён.

Независимо проверены manifest, README, метаданные и полный inventory Ayu-пакета; ключевые implementation seams сверены по `AyuConfig`, `AyuFilter`, Room entities/DAO, `AyuMessagesController`, `AyuGhostUtils`, `AyuState`, `AyuSyncConfig`, `AyuSyncController`, `AyuSyncWebSocketClient`, `AyuInterceptor`, `EasyWaiter` и специализированным waiters, `AyuEasyUtils`, `AyuForwarder`, `AyuCustomHandlers`, preference screens, а также по указанным точкам входа в `ApplicationLoader`, `MessagesStorage`, `SendMessagesHelper`, `UserConfig`, `ChatActivity` и `LaunchActivity`. Это не построчная проверка всего Telegram upstream: core-классы велики, проверялись связанные с Ayu области и их непосредственные вызовы.

## Результат проверки и исправления

- Проверены 39 исходных уникальных facts; их ID, pinned SHA и evidence metadata заполнены. Исправлены три сокращённых evidence path до полных путей в снимке (`ChatActivity`, `AyuSyncController`, `AyuForwarder`). README claims оставлены `docs`, вывод о границе стороннего API — `inference`, радар — `secondary`; статическое чтение не названо runtime-проверкой. API и call-sites ведут на pinned permalink.
- До проверки не было описано содержимое `AyuForwarder` как существенная техника integration: смешанные выделения сегментируются на обычные форварды и особый путь реконструкции Ayu-сообщений, который повторно отправляет текст/документы/фото, учитывает альбомы и зависит от синхронных внутренних helpers. Добавлен факт `ayugram4a-040` и отдельный раздел; явно перечислены TODO replies, отсутствие cache fallback и пропуск неподдерживаемых типов. Это fork-specific реализация, не публичный API и не рекомендация обхода ограничений.
- Добавлен факт `ayugram4a-041` о `tg:ayu`/`tg:xiaomi` обработчиках, которым `LaunchActivity` передаёт активный `BaseFragment`. Отмечено, что они используют внутренний `BulletinFactory`, а MIUI-ветка `handleXiaomi` запускает `ACTION_DELETE` для текущего package; это локальная маршрутизация приложения, не внешний handler contract.
- Уточнён факт `ayugram4a-030`: `EasyWaiter` ждёт без timeout как основное событие, так и UI-переходы subscribe/unsubscribe. Ожидание может навсегда блокировать фонового caller при потерянном событии или остановленном UI dispatch; страница теперь прямо предупреждает об этом. Никакой runtime-частоты такого отказа не утверждается.
- Проверка повторов: внутри страницы/JSON факты 006 и 037 сохраняются раздельно только потому, что 006 фиксирует метаданные pinned commit, а 037 хранит более широкий вторичный тезис радара и ограничивает его доказательную силу. Остальные тематические группы описывают разные механизмы; новых дублирующих facts не добавлено. Сходные методы синхронизации, истории или UI у других клиентов должны сохранять отдельный source provenance. Канонические темы для последующего синтеза: клиентские integration seams, локальная история/DAO, синхронное ожидание событий и message forwarding.

После дополнений — **41 уникальный факт**. Факты о методах Ayu принадлежат встроенному fork-коду (`code`); README и metadata claims не трактуются как plugin API. Внешний ExteraGram SDK здесь не сопоставлялся, поэтому рекомендация об отдельной адаптации для стороннего плагина остаётся выводом по отсутствию обнаруженного registration contract в изученном дереве.

## Остаточные пробелы

- README требует `AyuMessageUtils` и `AyuHistoryHook` для сборки форка; файлы отсутствуют в pinned tree, хотя `ChatActivity` импортирует/вызывает `AyuHistoryHook`. Реализации и совместимый build результата нет.
- Core-файлы Telegram просмотрены выборочно вокруг Ayu call-sites. Поведение upstream за пределами этих участков, полная совместимость версий и все downstream effects не покрыты.
- AyuSync описан со стороны клиента; server/backend schema и live account/network lifecycle отдельно не проверялись.
- `EasyWaiter`/`AyuEasyUtils` остаются без timeout/cancel/error completion в рассмотренных ожиданиях. Это видимое статическое ограничение, но последствия на устройстве не проверены.
- Не выполнялись build, tests, приложение или device runtime. Собираемость и фактическое поведение по исходникам не подтверждены.

Вердикт: **accepted-with-gaps**. Источник и 41 факт пригодны как pinned статическая справка при сохранении границы между внутренними точками модификации клиента и публичным API сторонних плагинов, а также при явном учёте отсутствующих proprietary-классов, backend-контракта и непроверенного runtime.
