# Журнал wiki

## [2026-09-27] ingest | Исходные документы

Сохранены исходный Markdown-радар и описание LLM Wiki. Выделены пары сборщик/проверяющий на gpt-6-luna; исходники рассматриваются как данные.

## [2026-09-27] ingest | Дополнительный JSON-экспорт

Сохранены 39 сообщений с дополнительным сравнением developer-инструментов и отчетом26сентября. Потерянные ссылки по-прежнему есть; APK/EAF представлены метаданными. Расширен реестр первоисточников.

## [2026-09-27] review | radar

Отдельные субагенты /root/collect_radar и /root/review_radar (`gpt-6-luna`). Состояние: accepted-with-gaps. [Источник](sources/radar.md), [проверка](reviews/radar.md).

## [2026-09-27] review | official-sdk

Отдельные субагенты /root/collect_official_sdk и /root/review_official_sdk (`gpt-6-luna`). Состояние: accepted-with-gaps. [Источник](sources/official-sdk.md), [проверка](reviews/official-sdk.md).

## [2026-09-27] review | for-vibecoders

Отдельные субагенты /root/collect_vibecoders и /root/review_vibecoders (`gpt-6-luna`). Состояние: accepted-with-gaps. [Источник](sources/for-vibecoders.md), [проверка](reviews/for-vibecoders.md).

## [2026-09-27] review | gradle-plugin

Отдельные субагенты /root/collect_gradle_plugin и /root/review_gradle_plugin (`gpt-6-luna`). Состояние: accepted-with-gaps. [Источник](sources/gradle-plugin.md), [проверка](reviews/gradle-plugin.md).

## [2026-09-27] review | extcli

Отдельные субагенты /root/collect_extcli и /root/review_extcli (`gpt-6-luna`). Состояние: accepted-with-gaps. [Источник](sources/extcli.md), [проверка](reviews/extcli.md).

## [2026-09-27] ingest | Уточнение источников пользователем

Получены точные URL NagramXTurbo, AyuSamplePlugin, PLEngine и exteragram-utils 0.1.3. Сохранены [адреса](../raw/user-supplied-urls.json); неопределенная идентичность этих источников заменена подтвержденными адресами с сохранением происхождения уточнения.

## [2026-09-27] review | altylib

Отдельные субагенты /root/collect_altylib и /root/review_altylib (`gpt-6-luna`). Состояние: accepted-with-gaps. [Источник](sources/altylib.md), [проверка](reviews/altylib.md).

## [2026-09-27] review | exteralib

Отдельные субагенты /root/collect_exteralib и /root/review_exteralib (`gpt-6-luna`). Состояние: accepted-with-gaps. [Источник](sources/exteralib.md), [проверка](reviews/exteralib.md).

## [2026-09-27] lint | Переносимость ссылок и точность формулировки

Три ссылки на рабочие JSON заменены ссылками на копии внутри wiki. На странице for-vibecoders убрана неподтвержденная привязка к Jython: примеры показывают Python с взаимодействием с Java. Контракты и исходные снимки не изменены. Промежуточно сверены 1883 контрольные суммы исходных файлов; остальные source pairs продолжают обработку.


## [2026-09-27] review | catalib

Отдельные субагенты /root/collect_catalib и /root/review_catalib (`gpt-6-luna`). Состояние: accepted-with-gaps; 34 уникальных факта. Дополнены support API, offline harness, scaffold, watch/deploy/doctor/logs; зафиксированы gaps runtime и версий. [Источник](sources/catalib.md), [проверка](reviews/catalib.md).

## [2026-09-27] review | template-n08

Отдельные субагенты /root/collect_template_n08 и /root/review_template_n08 (`gpt-6-luna`). Состояние: accepted-with-gaps; 37 уникальных фактов. Сверены bridge signatures, lifecycle, DEX build/loader и cleanup gaps. [Источник](sources/template-n08.md), [проверка](reviews/template-n08.md).

## [2026-09-27] ingest | Сводные страницы wiki

Скомпилированы девять независимо проверенных источников: 309 записей с происхождением, 290 строк вызовов/API-групп, 11 страниц сущностей и 15 канонических правил. Пары продолжают обработку; этот снимок индекса промежуточный.

## [2026-09-28] review | template-robotiaga

Отдельные субагенты /root/collect_template_robotiaga и /root/review_template_robotiaga (`gpt-6-luna`). Состояние: accepted-with-gaps; 40 фактов. README/ROADMAP расходятся насчёт JVM callback на AyuGram 12.9.0, runtime остаётся неподтверждённым; CI без host JAR подтверждает только ограниченный packaging smoke. [Источник](sources/template-robotiaga.md), [проверка](reviews/template-robotiaga.md).

## [2026-09-28] ingest | Сравнение версий и форматов

Созданы [матрица версий и форматов](compatibility.md), уточнены межисточниковые [пробелы и конфликты](gaps.md). Индекс и реестр пересобраны по десяти завершённым парам; API, сущности и канонические правила сохраняют ссылки на source facts. В текущем корпусе 349 фактов.

## [2026-09-28] review | Дополнены пользовательские ссылки и примеры

ExteraGram Utils: `/root/collect_exteragram_utils` + `/root/review_exteragram_utils`, `gpt-6-luna`, `accepted-with-gaps`, 41 факт; сверены wheel и sdist, уточнены disconnect/timeout и несовпадение CLI с документированным протоколом. [Источник](sources/exteragram-utils.md), [проверка](reviews/exteragram-utils.md).

AyuGram Desktop PLEngine: `/root/collect_ayugram_plengine` + `/root/review_ayugram_plengine`, `gpt-6-luna`, `accepted-with-gaps`, 27 фактов; исправлены выводы о HTTP fallback и JSON типах. `doDrawPopup` call-site не найден в изученной выборке; runtime не проверялся. [Источник](sources/ayugram-plengine.md), [проверка](reviews/ayugram-plengine.md).

NagramXTurbo: `/root/collect_nagramx_turbo` + `/root/review_nagramx_turbo`, `gpt-6-luna`, `accepted-with-gaps`, 31 факт; исправлены attribution/Room/build claims и отделён клиентский код от plugin API. [Источник](sources/nagramx-turbo.md), [проверка](reviews/nagramx-turbo.md).

AyuSamplePlugin: `/root/collect_ayu_sample` + `/root/review_ayusample`, `gpt-6-luna`, `accepted-with-gaps`, 22 факта; проверены 13 файлов snapshot и сохранены различия provenance от PLEngine. [Источник](sources/ayugram-sample.md), [проверка](reviews/ayugram-sample.md).

ExteraGram MCP сборщик завершил 31 факт; независимая проверка идёт. ExteraGram docs и skill-makarworld собираются отдельными агентами. После добавления четырёх проверенных источников пересобраны факты и API: 14/76 источников, 470 фактов, 429 API-строк; lint structural checks пока ждут завершения остальных пар.

## [2026-09-28] review | ExteraGram MCP и новый снимок

`/root/collect_exteragram_mcp` + `/root/review_exteragram_mcp` (`gpt-6-luna`): accepted-with-gaps, 37 уникальных фактов. Code snapshot содержит 81 регистрацию инструмента (101 объявление `it(...)`), тогда как README/docs называют 76; тесты, сборка, ADB и runtime не проверялись. [Источник](sources/exteragram-mcp.md), [проверка](reviews/exteragram-mcp.md).

Обновлена матрица границ Desktop/mobile и страница конфликтов; пересобраны индекс, API, topics, сущности и правила. Промежуточно независимо проверено 15/76 источников: 507 фактов и 464 строки API; оставшиеся пары продолжают работу.

## [2026-09-28] review | makarworld/exteragram-plugin-skill

`/root/review_skill_makarworld`: accepted-with-gaps, 39 уникальных facts. Получены два недостающих корневых файла snapshot (`.gitattributes`, `.gitignore`), сверены хэши 24/24 blobs. Исправлена чрезмерно узкая формулировка Elyx refmap, добавлены dev/debugger, DevServer, pre-installed libraries, Java callback proxies и repo release details. Runtime/build/SDK implementation не проверялись. [Источник](sources/skill-makarworld.md), [проверка](reviews/skill-makarworld.md).

## [2026-09-28] review | ExteraGram docs и skill-makarworld

`/root/collect_exteragram_docs` + `/root/review_exteragram_docs` (`gpt-6-luna`): accepted-with-gaps, 27 уникальных фактов. Проверены все 9 docs pages и 56 ссылок/якорей; уточнено, что примеры используют `on_load`, а расхождение со stub `on_plugin_load` версионное. [Источник](sources/exteragram-docs.md), [проверка](reviews/exteragram-docs.md).

`/root/collect_skill_makarworld` + `/root/review_skill_makarworld` (`gpt-6-luna`): accepted-with-gaps, 39 уникальных фактов после независимых дополнений. Проверены все 24 файла snapshot, 15 reference и 4 examples; команды skill не запускались. [Источник](sources/skill-makarworld.md), [проверка](reviews/skill-makarworld.md).

Промежуточная пересборка: 17/76 принятых пар, 573 факта, 524 API-строки. Skill-foss и skill-faust собираются отдельными агентами.

## [2026-09-28] review | exteraSkill

`/root/collect_skill_foss` + `/root/review_skill_foss` (`gpt-6-luna`): accepted-with-gaps, 34 уникальных факта. Проверены все 48 файлов snapshot и manifest; документирован DEX/ADB workflow, а `scripts/adb_push_py.py` подтверждён как отсутствующий alias старого имени (`scripts/push_plugin.py`). [Источник](sources/skill-foss.md), [проверка](reviews/skill-foss.md).

Пересобрана база: 18/76 источников, 607 фактов и 556 API-строк. Проверки skill-faust, mioplugin и сбор zwylib продолжаются.

## [2026-09-28] review | README-only skill-faust

`/root/collect_skill_faust` + `/root/review_skill_faust` (`gpt-6-luna`): accepted-with-gaps, 35 фактов. Independent review подтвердил полный pinned tree из одного README и 404 для отсутствующих заявленных docs/support paths; README противоречит сам себе по `.plugin`, base64 и ADB. [Источник](sources/skill-faust.md), [проверка](reviews/skill-faust.md).

Промежуточный ingest: 19/76 независимых пар, 642 факта, 586 API-строк. Mioplugin проходит review; собираются zwylib и re-extera.

## [2026-09-28] review | mioplugin

`/root/collect_mioplugin` + `/root/review_mioplugin` (`gpt-6-luna`): accepted-with-gaps, 36 уникальных фактов. Проверены README/manifests и 11 Python examples, Rust/WASM SDK; отмечены различия каталога, Python схем, GPL-3.0/MIT, отсутствие host/runtime и неполные бинарные файлы. [Источник](sources/mioplugin.md), [проверка](reviews/mioplugin.md).

После сборки: 20/76 завершённых источников, 678 фактов, 621 API-строка; zwylib и два re-extera fork сейчас собираются.

## [2026-09-28] review | zwylib-docs

`/root/collect_zwylib` + `/root/review_zwylib` (`gpt-6-luna`): accepted-with-gaps, 63 уникальных факта по 13 MDX API pages. Добавлены 12 пропусков, исправлены локальные доказательства; implementation/runtime, version, UI threading и account ownership в документационном snapshot не подтверждаются. [Источник](sources/zwylib.md), [проверка](reviews/zwylib.md).

Индекс обновлён: 21/76 принятых пар, 741 факт, 683 API-строки. Re-extera forks проходят независимую проверку; tg-streaks собирается.

## [2026-09-28] review | fossSquad/re-extera

`/root/collect_re_extera` + `/root/review_re_extera` (`gpt-6-luna`): accepted-with-gaps, 43 факта после удаления дублирующего SettingsRegistry claim и исправлений сигнатуры/provenance. Все 120 полученных файлов совпали с manifest; runtime и host JAR не проверялись. [Источник](sources/re-extera.md), [проверка](reviews/re-extera.md).

Сводный индекс отражает 22 принятых источника, 784 факта, 726 API-строк. SHAJON fork пока на review; tg-streaks и ElyxBuilder shareui собираются.

## [2026-09-28] review | SHAJON-404/re-extera fork

`/root/collect_re_extera_shajon` + `/root/review_re_extera_shajon` (`gpt-6-luna`): accepted-with-gaps, 29 фактов. Reviewer пересчитал полные pinned trees: 117 общих путей, 60 изменённых, 57 только SHAJON, 13 только fossSquad; цифры частичных manifests отличаются. Зафиксированы отсутствие host JAR/runtime и неполный просмотр hook/UI implementations. [Источник](sources/re-extera-shajon.md), [проверка](reviews/re-extera-shajon.md).

После добавления fork: 23/76 принятых источника, 813 фактов, 752 API-строки. Tg-streaks и два ElyxBuilder форка в сборе.

## [2026-09-28] review | tg-streaks

`/root/collect_tg_streaks` + `/root/review_tg_streaks` (`gpt-6-luna`): accepted-with-gaps, 27 уникальных фактов по SHA `e9fa83619480964ccd3b8565af8c1301318ac7ad`. Версия радара 2.20.0 расходится со snapshot 2.20.1; runtime, artifact identity и миграция реальных баз не проверялись. [Источник](sources/tg-streaks.md), [проверка](reviews/tg-streaks.md).

Индекс: 24/76 проверенных пар, 840 фактов, 778 API-строк. Shareui проходит review, Kangel и CEPS собираются.

## [2026-09-28] review | ElyxBuilder shareui и Kangel

ShareUI `e45963fe787938ebc9a8abb3a3794b232fb72e97` и Kangel `b6db59093324dc5148f811c9058a6c1414fbb849` прошли независимую проверку отдельными парами `gpt-6-luna`. В facts: 28 и 30 уникальных записей соответственно, оба accepted-with-gaps. Зафиксированы отсутствие client loader/interpreter, разные obfuscation/refmap details и отсутствие runtime/build verification. [ShareUI](sources/elyxbuilder-shareui.md) · [review](reviews/elyxbuilder-shareui.md); [Kangel](sources/elyxbuilder-kangel.md) · [review](reviews/elyxbuilder-kangel.md).

Пересборка: 26/76 источников, 900 фактов, 833 API-строки. CEPS и iOS bubble-outline собираются.

## [2026-09-28] correction | ElyxBuilder shareui review count

Финальный `review_elyxbuilder_shareui` добавил два факта о `watch`/`pyzipper` и расхождениях CLI/docs; итоговый набор — 30 фактов (не первоначальные 28 сборщика). Последняя сборка уже включает исправленное число.

## [2026-09-28] review | CEPS

`/root/collect_ceps` + `/root/review_ceps` (`gpt-6-luna`): accepted-with-gaps, 26 уникальных фактов. Все 55 файлов SHA-сверены; исправлены guard seal conditions и installer отказ для `.ceps` без shares. Runtime, Android и CI не проверялись. [Источник](sources/ceps.md), [проверка](reviews/ceps.md).

На момент этой записи: 27/76 принятых пар, 926 фактов, 858 API-строк. Bubble-outline reviewer затем создал полный report и принял источник с оговорками; AV1 decoder проходит review, Link Guard и SyncProfile собираются.

## [2026-09-28] review | xwwvv/ios-bubble-outline

`/root/collect_bubble_outline` + `/root/review_bubble_outline` (`gpt-6-luna`): accepted-with-gaps, 29 уникальных фактов. Reviewer сверил pinned DEX `drawOutline` descriptor (`float/int/boolean`) с тем, что доступно в snapshot; reflection/runtime bridge и устройство не проверялись. Название репозитория не означает iOS implementation: в снимке только Android ExteraGram plugin и Kotlin DEX. [Источник](sources/bubble-outline.md), [проверка](reviews/bubble-outline.md).

Индекс пересобран: 28/76 принятых источников, 955 фактов и 885 API-строк. AV1 decoder проходит review; Link Guard и SyncProfile в работе.

## [2026-09-28] review | stxlvn/exteragram-av1-sw-decoder

`/root/collect_av1_decoder` + `/root/review_av1_decoder` (`gpt-6-luna`): accepted-with-gaps, 28 уникальных fact ID. Проверены pinned SHA, оба manifest blobs, README и plugin source. Reviewer уточнил platform/version и callback claims; SDK/client internals, build, release, tests и runtime недоступны или не проверялись. [Источник](sources/av1-decoder.md), [проверка](reviews/av1-decoder.md).

Индекс пересобран: 29/76 принятых источников, 983 факта и 910 API-строк.

## [2026-09-28] review | L0lopop/Link-Guard

`/root/collect_link_guard` + `/root/review_link_guard` (`gpt-6-luna`): accepted-with-gaps, 32 уникальных факта по pinned SHA `b9cd180c83b47a724970e026f64ec8039cc0f650`. Независимая проверка сверила source/docs/tests/workflows, уточнила whitelist priority, неразобранную `tg://` схему, выбор аккаунта и reduced mode; build, тесты и runtime не запускались. [Источник](sources/link-guard.md), [проверка](reviews/link-guard.md).

Индекс пересобран: 30/76 принятых источников, 1 015 фактов и 941 API-строка. SyncProfile передан отдельному reviewer; self-hosted server и Plugins Robot собираются.

## [2026-09-28] review | Kukuryzen666/SyncProfile

`/root/collect_syncprofile` + `/root/review_syncprofile` (`gpt-6-luna`): accepted-with-gaps, 42 уникальные записи по pinned SHA `addbd38ff37965be31d2e9e2845793539bfd60ce`. Review исправил claims о backoff/fallback и приписанном радару polling interval, дополнил callbacks и поведение `START`/`RESUME`. Тесты и runtime не запускались; совместимость с серверами/клиентами не установлена. [Источник](sources/syncprofile.md), [проверка](reviews/syncprofile.md).

Индекс пересобран: 31/76 принятый источник, 1 057 фактов и 981 API-строка.

## [2026-09-28] review | Kukuryzen666/SyncProfile-Selfhosted

`/root/collect_syncprofile_server` + `/root/review_syncprofile_server` (`gpt-6-luna`): accepted-with-gaps, 31 уникальный факт. Pinned tree не содержит серверного приложения, поэтому факты описывают клиентский контракт; review выявил обращение к отсутствующему `_patch_cache`, неполный clear-cache flow и синхронный full-fetch из Settings. SHA подтверждён, hashes семи файлов совпали. [Источник](sources/syncprofile-server.md), [проверка](reviews/syncprofile-server.md).

Индекс пересобран: 32/76 принятых источника, 1 088 фактов и 1 006 API-строк.

## [2026-09-28] review | itsv1eds/exteraPluginsRobot

`/root/collect_plugins_robot` + `/root/review_plugins_robot` (`gpt-6-luna`): accepted-with-gaps, 41 уникальный факт. Хэши 60 файлов совпали; reviewer удалил повтор и дополнил quiz, subscriptions, moderation statistics, iconpacks и poster. Commit `31ecf63` подтверждён API GitHub, более поздняя радарная дата остаётся без pinned URL. Это Telegram-каталог, не Android SDK; бот не запускался. [Источник](sources/plugins-robot.md), [проверка](reviews/plugins-robot.md).

Индекс пересобран: 33/76 принятых источника, 1 129 фактов и 1 043 API-строки.

## [2026-09-28] review | shareui/packit-source

`/root/collect_packit` + `/root/review_packit` (`gpt-6-luna`): accepted-with-gaps, 36 уникальных фактов. Hashes всех 276 полученных файлов совпали; reviewer исправил число файлов в tree, добавил экспортные заголовки и вложенную лицензию. Статически отмечены потеря `repoId` в deeplink и nonce fallback с fixed seed при ошибке `/dev/urandom`; условия на устройстве не проверялись. [Источник](sources/packit.md), [проверка](reviews/packit.md).

Индекс пересобран: 34/76 принятых источника, 1 165 фактов и 1 079 API-строк.

## [2026-09-28] review | Kangel-Plugins/Plugins-Store

`/root/collect_plugins_store` + `/root/review_plugins_store` (`gpt-6-luna`): accepted-with-gaps, 21 уникальный факт. SHA всех 15 manifest-файлов совпали. Статический review уточнил RSA signature check и зеркала; в KPM 1.5.4 update path не показывает вызов integrity check, применяемый обычной установкой. [Источник](sources/plugins-store.md), [проверка](reviews/plugins-store.md).

Индекс пересобран: 35/76 принятых источников, 1 186 фактов и 1 099 API-строк.

## [2026-09-28] review | mr-Vestr/plugins

`/root/collect_vestr_plugins` + `/root/review_vestr_plugins` (`gpt-6-luna`): accepted-with-gaps, 28 уникальных фактов. Проверены SHA всех 15 файлов манифеста и три руководства; reviewer уточнил пропущенную англоязычную документацию и расхождения описаний. Double start updater зафиксирован как статическое наблюдение; build, тесты, host client и runtime отсутствуют/не запускались. [Источник](sources/vestr-plugins.md), [проверка](reviews/vestr-plugins.md).

Индекс пересобран: 36/76 принятых источников, 1 214 фактов и 1 126 API-строк.

## [2026-09-28] review | ReaIRyanGosling/tg_ws_proxy.plugin

`/root/collect_ws_proxy_plugin` + `/root/review_ws_proxy_plugin` (`gpt-6-luna`): accepted-with-gaps, 36 уникальных фактов по pinned commit. Независимый review сопоставил GitHub tree/blob hashes, объединил повтор и уточнил worker pool, unload, handshake, fragmentation и DC fallback. Runtime и client compatibility не проверялись. [Источник](sources/ws-proxy-plugin.md), [проверка](reviews/ws-proxy-plugin.md).

Индекс пересобран: 37/76 принятых источников, 1 250 фактов и 1 155 API-строк.

## [2026-09-28] review | Flowseal/tg-ws-proxy

`/root/collect_ws_proxy` + `/root/review_ws_proxy` (`gpt-6-luna`): accepted-with-gaps, 35 уникальных фактов. Reviewer перепроверил 75 файлов по SHA-256 и Git blob SHA; уточнил проверку `Sec-WebSocket-Accept`, TLS context при заданном SNI и отсутствие allowlist в Worker example. Read-only review кода/тестов; build/runtime не выполнялись, security review и сравнение lineage с upstream не делались. [Источник](sources/ws-proxy.md), [проверка](reviews/ws-proxy.md).

Индекс пересобран: 38/76 принятых источников, 1 285 фактов и 1 188 API-строк. Незавершённые reviews `tayugram-mcp` и `chat-stats` возвращены в очередь после лимита GPT-6 Luna.

## [2026-09-28] review | DedyaSergey/Chat-Stats-Plugin

`/root/collect_chat_stats` + `/root/review_chat_stats_retry` (`gpt-6-luna`): accepted-with-gaps, 16 уникальных фактов; SHA и два file/blob hashes совпали. Reviewer независимо проверил account-argument, общий ключ `unknown` и расчёт периодных отчётов. Host API contract, настройка по аккаунтам, client compatibility и runtime остались непроверенными. [Источник](sources/chat-stats.md), [проверка](reviews/chat-stats.md).

## [2026-09-28] review | DedyaSergey/Smooth-Scroll-Plugin

`/root/collect_smooth_scroll` + `/root/review_smooth_scroll` (`gpt-6-luna`): accepted-with-gaps, 25 фактов. Добавлен пропущенный `.gitignore`; hashes всех 11 файлов совпали. Review уточнил busy loop при FPS-gate отказе, незавершённый animation step и gesture task без отмены при unload; touch listener, scroll-offset mutation и GPU/FPS telemetry в snapshot не подтверждены. [Источник](sources/smooth-scroll.md), [проверка](reviews/smooth-scroll.md).

Индекс пересобран: 40/76 принятых источников, 1 326 фактов и 1 227 API-строк.

## [2026-09-28] review | MRsuperkosmos/tayugram-mcp

`/root/collect_tayugram_mcp` + `/root/review_tayugram_mcp_retry` (`gpt-6-luna`): accepted-with-gaps, 34 уникальных факта. Проверены 49 blobs; 200 имён в TOOLS совпадают с 200 регистрациями. Review нашёл расхождения docs/tests/source в `FLOOD_WAIT`, delete safety, `tg_logout`, lockfile и detached sleep cleanup. Не запускались тесты, MCP/Telegram, CI, сборка и установка. [Источник](sources/tayugram-mcp.md), [проверка](reviews/tayugram-mcp.md).

Индекс пересобран: 41/76 принятый источник, 1 360 фактов и 1 261 API-строка.

## [2026-09-28] review queue paused by GPT-6 Luna usage limit

Отдельные reviewers для `tayugram-mcp` и `chat-stats` завершились сообщением о лимите модели до 06:09. Оба источника возвращены в `collected`, не включаются в проверенные факты; их независимый review остаётся в очереди. Имена не проверявших агентов очищены из текущего reviewer assignment; сбор продолжен по другим доступным источникам без смены модели.

## [2026-09-28] review | MRsuperkosmos/tayugram-mcp

`/root/collect_tayugram_mcp` + `/root/review_tayugram_mcp_retry` (`gpt-6-luna`): accepted-with-gaps, 34 уникальных факта. Проверены все 49 tree blobs на SHA-256 manifest и Git blob SHA; tool names из TOOLS.md статически совпали с 200 уникальными core/domain registrations. Исправлены описание JSON schemas, разделение MCP SDK/протокола/GramJS, документы о FLOOD_WAIT и delete safety, неполный/несогласованный lockfile, тестовые side effects, несуществующий tg_logout и lifecycle detached sleep helper. Runtime, live Telegram, tests, install/build не запускались. [Источник](sources/tayugram-mcp.md), [проверка](reviews/tayugram-mcp.md).


## [2026-09-28] review | Islite/AniList.co

`/root/collect_anilist` + `/root/review_anilist` (`gpt-6-luna`): accepted-with-gaps, 23 уникальных факта. Все 15 tree blobs совпали по Git SHA-1, SHA-256 и размеру; ссылки и evidence ranges закреплены за commit. Уточнены частичные GraphQL errors и default HookResult ветви, добавлены editor/multi-select детали. README/build/tests/license, host SDK lifecycle/compatibility и Android runtime остаются gaps. [Источник](sources/anilist.md), [проверка](reviews/anilist.md).

## [2026-09-28] collection | vibeDN/ViboGram

`/root/collect_vibogram` (`gpt-6-luna`): collected, 28 уникальных фактов на commit `5f51b6befb2ce9370ea9acf40759d71053db2776`. Snapshot SHA совпал с tree SHA; SHA-256 всех 17 приобретённых файлов совпали с manifest, permalinks закреплены за commit. Зафиксированы противоречия документации и реализации hooks, а также непроверенная iOS-сборка/runtime. Независимый review ожидается; Xcode/Bazel, установка и runtime не запускались. [Источник](sources/vibogram.md), [факты](../work/vibogram-facts.json).


## [2026-09-28] review | Kisyndra1337/CustomNFT-Exteragram-Plugin

`/root/collect_custom_nft_retry` + `/root/review_custom_nft` (`gpt-6-luna`): accepted-with-gaps, 28 уникальных фактов. Review подтвердил provenance 11 файлов и уточнил reflection-поиск коллекций, live-кэш без дедупликации и fallback counts при сборке подарка. Полный SDK/runtime и UI не проверялись; tests, сборка и установка не выполнялись. [Источник](sources/custom-nft.md), [проверка](reviews/custom-nft.md).

Пересобрана wiki: 44/76 проверенных источников, 1 429 фактов и 1 326 API-строк; выполнена проверка 2 108 сохранённых файлов по manifest. Linter сообщает только о 32 источниках, которые ещё не прошли независимое review; структурных ошибок и битых внутренних ссылок нет.


## [2026-09-28] review | vibeDN/ViboGram

`/root/collect_vibogram` + `/root/review_vibogram` (`gpt-6-luna`): accepted-with-gaps, 31 уникальный факт. Независимо проверены 23 файла pinned commit; шесть сборочных/debug-файлов досняты с того же SHA. Уточнены повторный запуск CPython, error boundaries, whitespace в marker и resource wiring; smoke test после перемещения ресурсов не подтверждён. iOS build/runtime, sandbox и threading не проверялись. [Источник](sources/vibogram.md), [проверка](reviews/vibogram.md).

Пересобрана wiki: 45/76 проверенных источников, 1 460 фактов и 1 352 API-строки; manifest сверил 2 179 сохранённых файлов. Linter оставил 31 ошибку для строк без завершённого review и 31 предупреждение о неоднозначных evidence locators.


## [2026-09-28] review | voterol/ReqGram

`/root/collect_reqgram` + `/root/review_reqgram` (`gpt-6-luna`): accepted-with-gaps, 34 уникальных факта. Сверены выбранные AyuGram/ReqGram Swift, TelegramCore/UI integrations, storage/hooks, badge/gift flows, Bazel/build/version/workflow paths. Добавлены README/build требования и gaps, исправлено badge specification evidence. Это iOS client/module, не Android plugin contract; исходная реализация App Group, полная трассировка Ghost Mode/plugins, device/build и server behavior не подтверждены. [Источник](sources/reqgram.md), [проверка](reviews/reqgram.md).

## [2026-09-28] review | exteraless/exteraless

`/root/collect_exteraless` + `/root/review_exteraless` (`gpt-6-luna`): accepted-with-gaps, 32 уникальных факта. По pinned SHA независимо сверены SDK/runtime, permissions, hooks, client/account helpers, Elyx/EAF lifecycle, installer и build; manifest hashes совпали для 67 файлов. Добавлены dev-server loopback/token и pure-Python wheel/dependency cleanup; historical radar fixes без commit ссылок остались gap. UI/media breadth, CI/build и runtime не проверялись. [Источник](sources/exteraless.md), [проверка](reviews/exteraless.md).

Пересобрана wiki: 47/76 проверенных источников, 1 526 фактов и 1 416 API-строк; manifest сверил 2 200 файлов. Linter оставил 29 ошибок для незавершённых review и 32 warning по evidence locators.


## [2026-09-28] review | fuckramochka/miogram

`/root/collect_miogram` + `/root/review_miogram` (`gpt-6-luna`): accepted-with-gaps, 38 уникальных фактов по commit `8ce2a35`. Проверены 78 выбранных файлов: plugin manager/hooks, Forge, Rust/WASM и Kotlin/WAMR core, hotpatch, LRC/player/online halo, Smart Feed, Kanban и multi-chat. Исправлена неверная трактовка отсутствующего core; найден отдельный core engine, но проверенный Forge path идёт в Python manager; `MIOG`/`HYPR`/FlatBuffers и trust/loading paths не сведены. Runtime/build/CI не запускались. [Источник](sources/miogram.md), [проверка](reviews/miogram.md).

## [2026-09-28] review | HSSkyBoy/NiagramX

`/root/collect_niagramx` + `/root/review_niagramx` (`gpt-6-luna`): accepted-with-gaps, 27 фактов на SHA `f97133c`. Проверено 51 сохранённый файл и paths/строки фактов; уточнены default/placement VPN setting и `checkVpnState()` call site, устранён повтор о plugin API. Исторические URL радара относятся к отдельным revisions; plugin host, build/runtime не проверялись. [Источник](sources/niagramx.md), [проверка](reviews/niagramx.md).

Пересобрана wiki: 49/76 независимо проверенных источников, 1 591 факт и 1 475 API-строк; manifest сверил 2 366 файлов. Linter оставил 27 ошибок для незавершённых источников и 32 evidence-locator warning.


## [2026-09-28] review | fuckramochka/amegram

`/root/collect_amegram` + `/root/review_amegram` (`gpt-6-luna`): accepted-with-gaps, 42 факта по SHA `8a5819b`. Независимо сверены 324 выбранных primary files: Python/Chaquopy/Xposed, custom MioHook/WASM/FlatBuffers, Forge, AI/STT, hotpatch и связанные call-sites. Исправлено смешение legacy plugin catalog с guest execution; добавлены gaps по wire/trust path, LiteRT/STT, MioHook production bindings и DEX patch. Runtime/build/device не запускались. [Источник](sources/amegram.md), [проверка](reviews/amegram.md).

Пересобрана wiki: 50/76 проверенных источников, 1 633 факта и 1 513 API-строк; manifest сверил 2 657 файлов. Linter оставил 26 ошибок для незавершённой очереди и 32 warnings по evidence locators.


## [2026-09-28] review | Mercurygram/Mercurygram

`/root/collect_mercurygram` + `/root/review_mercurygram` (`gpt-6-luna`): accepted-with-gaps, 37 фактов по SHA `1c103ff`. Проверены selected folder/sync, typed search, drafts, counter, watchdog, local pins, Unicode fold, Tor AIDL и build files. Добавлены first-sync migration, порядок папок, повтор upload и secret-chat storage; исправлен поиск/date evidence и устранён дубль versionCode. `MgCharCounterTest.kt` отсутствует в полном pinned tree (404). Runtime/build/device/CI и server behavior не запускались. [Источник](sources/mercurygram.md), [проверка](reviews/mercurygram.md).

Пересобрана wiki: 51/76 проверенных источников, 1 670 фактов и 1 550 API-строк; manifest сверил 2 690 файлов. Linter оставил 25 ошибок для источников в очереди и 32 evidence-locator warnings.


## [2026-09-28] review | ferelking242/novagramx

`/root/collect_novagramx` + `/root/review_novagramx` (`gpt-6-luna`): accepted-with-gaps, 29 фактов на pinned SHA `5fc9938`. Reviewer независимо проверил regex-фильтры, last-seen и Ghost Mode, добавил факты о `ConnectionsManager.sendRequestInternal` и read/offline-after-send, уточнил importer для некорректных regex и исправил ограниченный вывод о last-seen. README-only функции, plugin-host compatibility, runtime/build/device не проверялись. [Источник](sources/novagramx.md), [проверка](reviews/novagramx.md).

Пересобрана wiki: 52/76 проверенных источников, 1 699 фактов и 1 578 API-строк; manifest сверил 2 722 файла. Linter оставил 24 ошибки для источников в очереди и 32 evidence-locator warnings.


## [2026-09-28] review | NullCoreDeveloper/NullcoreGram

`/root/collect_nullcoregram` + `/root/review_nullcoregram` (`gpt-6-luna`): accepted-with-gaps, 33 факта по SHA `926c62a`. Review независимо сверил evidence и строки, уточнил account binding TXT-запроса и добавил ограниченные inference о cache TTL/инвалидации и возможной гонке. Источники `NetworkRequestBuilder`/`NetworkResponse` отсутствуют в полном tree, поэтому транспорт DoH неизвестен; runtime/build/tests не запускались. [Источник](sources/nullcoregram.md), [проверка](reviews/nullcoregram.md).

Пересобрана wiki: 53/76 проверенных источников, 1 732 факта и 1 609 API-строк; manifest сверил 2 759 файлов. Linter оставил 23 ошибки для источников в очереди и 32 evidence-locator warnings.


## [2026-09-28] review | yearningss/opexgram-docs

`/root/collect_opexgram_docs` + `/root/review_opexgram_docs` (`gpt-6-luna`): accepted-with-gaps, 23 факта на SHA `31388f3`. Независимо сверены все четыре документа и их SHA-256; уточнены поля badge-схем, AI fact-check и settings. Snapshot содержит документацию beta6, отдельно от APK beta4; implementation, SDK, server, auth и runtime не проверены. [Источник](sources/opexgram-docs.md), [проверка](reviews/opexgram-docs.md).

Пересобрана wiki: 54/76 проверенных источников, 1 755 фактов и 1 632 API-строки; manifest сверил 2 761 файл. Linter оставил 22 ошибки для источников в очереди и 32 evidence-locator warnings.


## [2026-09-28] review | qwq233/Nullgram

`/root/collect_nullgram` + `/root/review_nullgram` (`gpt-6-luna`): accepted-with-gaps, 24 факта на SHA `b3d4f45`. Все 43 сохранённых файла совпали с manifest по SHA-256; исправлены ветки SOCKS4 UDP/BIND, ограничения SOCKS5 для домена/IPv6 и описание translator cache/client. Runtime и сетевую совместимость не запускали; внутренние classes не подтверждают публичный plugin contract. [Источник](sources/nullgram.md), [проверка](reviews/nullgram.md).

Пересобрана wiki: 55/76 проверенных источников, 1 779 фактов и 1 655 API-строк; manifest сверил 2 761 файл. Linter оставил 21 ошибку для источников в очереди и 32 evidence-locator warnings.


## [2026-09-28] review | BRYCE00182/AyuGram4A

`/root/collect_ayugram4a` + `/root/review_ayugram4a` (`gpt-6-luna`): accepted-with-gaps, 41 факт на SHA `0c3d253`. Все 71 файл manifest совпали по SHA-256. Review уточнил границы radar commit, AyuSync, proprietary `AyuMessageUtils`/`AyuHistoryHook` и `EasyWaiter` без timeout/cancel/error completion; отсутствие implementation/build и client/plugin compatibility осталось явным gap. [Источник](sources/ayugram4a.md), [проверка](reviews/ayugram4a.md).

Пересобрана wiki: 56/76 проверенных источников, 1 820 фактов и 1 687 API-строк; manifest сверил 2 830 файлов. Linter оставил 20 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | AyuGram/AyuGramDesktop

`/root/collect_ayugram_desktop` + `/root/review_ayugram_desktop` (`gpt-6-luna`): accepted-with-gaps, 12 фактов на SHA `db3b989`. Все 17 файлов manifest совпали по SHA-256. Review уточнил preprocess ABI: README рекомендует `std::string*`, но engine поддерживает и этот callback, и legacy `char*`; историческую связь sample с engine нельзя установить. Ограниченный Desktop UI snapshot, runtime/build/tests не проверялись. [Источник](sources/ayugram-desktop.md), [проверка](reviews/ayugram-desktop.md).

Пересобрана wiki: 57/76 проверенных источников, 1 832 факта и 1 697 API-строк; manifest сверил 2 851 файл. Linter оставил 19 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | Kratapand26/AyugramX

`/root/collect_ayugramx` + `/root/review_ayugramx` (`gpt-6-luna`): accepted-with-gaps, 18 фактов на SHA `e61bc31`. Reviewer подтвердил 18 уникальных facts и SHA-256 всех 21 доступного файла; уточнил local/cloud filter storage и синхронизацию порядка. README недоступен (404), radar URLs пусты, regex subsystem вне среза; runtime/build/tests не запускались. [Источник](sources/ayugramx.md), [проверка](reviews/ayugramx.md).

Пересобрана wiki: 58/76 проверенных источников, 1 850 фактов и 1 714 API-строк; manifest сверил 2 864 файла. Linter оставил 18 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | Kindness-Kismet/AyuGramDesktop-Plus

`/root/collect_ayugram_desktop_plus` + `/root/review_ayugram_desktop_plus` (`gpt-6-luna`): accepted-with-gaps, 25 фактов на SHA `b59475e`. Хэши 63 файлов совпали; reviewer исправил false claim про размер emoji preset и locator README, добавил SQLite storage и уточнил частичный охват UI picker/font backend. Проверено 63 из 7 355 blobs; runtime/build не запускались. [Источник](sources/ayugram-desktop-plus.md), [проверка](reviews/ayugram-desktop-plus.md).

Пересобрана wiki: 59/76 проверенных источников, 1 875 фактов и 1 735 API-строк; manifest сверил 2 925 файлов. Linter оставил 17 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | Ahefh/ayugram-ios-tweak

`/root/collect_ayugram_ios_tweak` + `/root/review_ayugram_ios_tweak` (`gpt-6-luna`): accepted-with-gaps, 15 фактов на SHA `79de9c9`. Reviewer перепроверил README и `Tweak.m`, уточнил, что стартовый log не доказывает установку hook и ненайденный `Method` молча пропускается; поправил runner claim. Hook injection/signing/IPA/install/runtime не проверялись; Android API нет. [Источник](sources/ayugram-ios-tweak.md), [проверка](reviews/ayugram-ios-tweak.md).

Пересобрана wiki: 60/76 проверенных источников, 1 890 фактов и 1 750 API-строк; manifest сверил 2 926 файлов. Linter оставил 16 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | arsLan4k1390/Cherrygram

`/root/collect_cherrygram` + `/root/review_cherrygram` (`gpt-6-luna`): accepted-with-gaps, 14 фактов на SHA `cec3075`. Reviewer исправил evidence radar-факта, уточнил Gemini callback и добавил README build requirement; 21 сохранённый файл совпал по SHA-256, а одна неверная попытка получить `ApiClient.kt` устранена через реальный `.java` файл. Из 166 путей собственного namespace исследован выбранный срез; полный client/build/runtime не проверяли. [Источник](sources/cherrygram.md), [проверка](reviews/cherrygram.md).

Пересобрана wiki: 61/76 проверенных источников, 1 904 факта и 1 760 API-строк; manifest сверил 2 945 файлов. Linter оставил 15 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | NextAlone/Nagram

`/root/collect_nagram` + `/root/review_nagram` (`gpt-6-luna`): accepted-with-gaps, 34 факта на SHA `b8db62a65e1e4dee34d92bff412548ef628ddb06`. Независимая проверка сверила 65 сохранённых файлов с manifest/tree и проверила 44 evidence rows; reviewer исправил повреждённую кодировку, объединил повтор и добавил пропущенные client patterns. Публичный plugin SDK в полном snapshot не обнаружен; runtime/build/tests не запускались, часть upstream/UI call-sites осталась за границей чтения. [Источник](sources/nagram.md), [проверка](reviews/nagram.md).

Пересобрана wiki: 62/76 проверенных источника, 1 938 фактов и 1 791 API-строка; manifest сверил 3 007 файлов. Linter оставил 14 ошибок только для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | risin42/NagramX

`/root/collect_nagramx` + `/root/review_nagramx` (`gpt-6-luna`): accepted-with-gaps, 26 фактов на SHA `2db685af00a4352c877ecf96474cbf0494284715`. Независимый reviewer уточнил credential fallback, вывод о plugin engine и privacy condition, добавил fragment cleanup и forwarding menu; ID уникальны. Радарный форк с engine не установлен, большая часть upstream/submodules не изучалась, сборка и runtime не запускались. [Источник](sources/nagramx.md), [проверка](reviews/nagramx.md).

Пересобрана wiki: 63/76 проверенных источников, 1 964 факта и 1 814 API-строк; manifest сверил 3 028 файлов. Linter оставил 13 ошибок только для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | Nekogram/Nekogram

`/root/collect_nekogram` + `/root/review_nekogram` (`gpt-6-luna`): accepted-with-gaps, 36 уникальных фактов на SHA `e924154e8d3b99a645b0521013ff9b501b28e8ce`. Reviewer проверил исходные 31 fact и расширил coverage ещё на пять integration points: Inline Bot, Web App bridge, Cronet, message filter и TelegramTranslator; устранил повтор в import narrative и обозначил границы. Submodules/full caller graph, build, runtime и device не проверялись. [Источник](sources/nekogram.md), [проверка](reviews/nekogram.md).

Пересобрана wiki: 64/76 проверенных источников, 2 000 фактов и 1 847 API-строк; manifest сверил 3 062 файла. Linter оставил 12 ошибок только для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | Ettacent/NimarkoGram

`/root/collect_nimarkogram` + `/root/review_nimarkogram`: accepted-with-gaps, 36 фактов на SHA `881d0ea1ce5f6a3a234f46d0e928bb0d95305f6b`. Reviewer не нашёл повторов; проверил все evidence paths, сверил ссылки с SHA и добавил API menu/file hooks. README заявляет DEX loading, но runtime путь для чужих DEX/JAR/APK в просмотренных файлах не подтверждён. Не проверялись весь utility/UI surface, PipController, security, build и runtime. Параметр spawn был `gpt-6-luna`, однако reviewer сообщил, что фактически его instance был GPT-6; effective model identity требует отдельного подтверждения. [Источник](sources/nimarkogram.md), [проверка](reviews/nimarkogram.md).

Пересобрана wiki: 65/76 проверенных источников, 2 036 фактов и 1 876 API-строк; manifest сверил 3 140 файлов. Linter оставил 11 ошибок только для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | OctoGramApp/OctoGram

`/root/collect_octogram` + `/root/review_octogram` (`gpt-6-luna`): accepted-with-gaps, 15 уникальных фактов на SHA `895d766d7277dbf23638be4844295ea0fe56558e`. Reviewer сверил все 15 evidence ranges, уточнил `ConfigProperty`/`OctoConfig` error paths, deep-link call-site и sync I/O в `build()` при HTTP body. Просмотрена выборка; 220 файлов собственного namespace подробно не изучены, `ConnectionsManager.java` недоступен, build/runtime не запускались. [Источник](sources/octogram.md), [проверка](reviews/octogram.md).

Пересобрана wiki: 66/76 проверенных источников, 2 051 факт и 1 891 API-строка; manifest сверил 3 164 файла. Linter оставил 10 ошибок только для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] unavailable-verified | Nekogram/NekoX

`/root/collect_nekox` + `/root/review_nekox` (`gpt-6-luna`): `unavailable-verified`, 8 facts; исторический SHA не установлен. Reviewer независимо проверил HTTP 404 и уточнил, что архивный Nagram README связывает исторический URL с `NekoX-Dev/NekoX`, но современный snapshot официального Telegram Android не подтверждён как код оригинального NekoX. Вторичный README сохранён с provenance `secondary`, без claims о реализации. [Источник](sources/nekox.md), [проверка](reviews/nekox.md).

Пересобрана wiki: 67/76 завершённых проверок, 2 059 фактов и 1 892 API-строки; manifest сверил 3 166 файлов. Linter оставил 9 ошибок только для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] unavailable-verified | phxc/telegraher

`/root/collect_telegraher` + `/root/review_telegraher`: `unavailable-verified`, 3 факта; pinned source SHA отсутствует. Reviewer подтвердил пустой публичный repository ID `552598807`: commits/refs HTTP 409, branches/tags пусты, contents HTTP 404. Forks `nikitasius/Telegraher` и `pegioner/Telegraher` имеют отдельную цепочку от DrKLO/Telegram и исключены. Сохранены 2 `unavailable` и 1 `secondary`; лицензия/build/API/runtime неизвестны. Reviewer self-report указал GPT-6, хотя spawn request был `gpt-6-luna`; effective model identity не подтверждена. [Источник](sources/telegraher.md), [проверка](reviews/telegraher.md).

Пересобрана wiki: 68/76 завершённых проверок, 2 062 факта и 1 894 API-строки; manifest сверил 3 166 файлов. Linter оставил 8 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] unavailable-verified | Xposed-Modules-Repo/com.my.televip

`/root/collect_televip` + `/root/review_televip` (`gpt-6-luna`): `unavailable-verified`, 9 facts на snapshot SHA `ebb10ec44719a516177f525e70ab19d686e3d288`. Review добрал пропущенный `SUMMARY`, подтвердил, что tree содержит только README/SUMMARY, release 3.6.2 публикует `TeleVip.apk`, а тег `315-3.5` указывает на пустое Git tree. APK не скачан, содержимое и source correspondence не проверены; внешний upstream не выдан за target. License file/build/tests/runtime отсутствуют. [Источник](sources/televip.md), [проверка](reviews/televip.md).

Пересобрана wiki: 69/76 завершённых проверок, 2 071 факт и 1 894 API-строки; manifest сверил 3 167 файлов. Linter оставил 7 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | Karpathy LLM Wiki pattern

`/root/collect_llm_wiki_pattern` + `/root/review_llm_wiki_pattern` (`gpt-6-luna`): accepted-with-gaps, 32 unique facts (29 docs, 3 inference) на gist commit `ac46de1ad27f92b28ac95459c782c07f6b8c964a`. Приложение пользователя побайтно совпало с локальной копией; все 75 строк совпали с gist после нормализации окончания строк. Facts перенесены в canonical root `work/`, pipeline восстановлен с сохранением 76 rows. Gaps: метод не определяет plugin API, fixed schema, entity dedup, write permissions/conflict protocol или reasoning traces. [Источник](sources/llm-wiki-pattern.md), [проверка](reviews/llm-wiki-pattern.md).

Пересобрана wiki: 70/76 проверенных источников, 2 103 факта и 1 894 API-строки; manifest сверил 3 167 файлов. Linter оставил 6 ошибок для источников в очереди и 36 evidence-locator warnings.


## [2026-09-28] review | Kangel/Plugins-Store (Codeberg)

`/root/collect_plugins_store_codeberg` + `/root/review_plugins_store_codeberg` (`gpt-6-luna`): accepted-with-gaps, 21 фактов на SHA `3a9417b85597127d843b0411792721f111297a0a`. Reviewer сверил все 18 исходных facts, добавил три подтверждённых AGENTS facts и проверил 17 manifest SHA-256. Каталог: 700 против 698 GitHub; 255/257 legacy_version deltas объясняются URL rewrite, содержательные plugin_guard/camera_enhancer; выбранный `.eaf` совпадает байтово. Tree truncated на 1 000, остальные плагины не проверены. 11 manifest-selected файлов `.eaf` извлечены и SHA-256 сверены, lint теперь разрешает raw-path errors. [Источник](sources/plugins-store-codeberg.md), [review](reviews/plugins-store-codeberg.md).

Пересобрана wiki: 71/76 проверенных источников, 2 124 факта и 1 909 API-строк; manifest сверил 3 184 файла. Linter оставил 5 ошибок только для источников в очереди и 37 evidence-locator warnings.


## [2026-09-28] review | Kangel/Plugins-Store (GitVerse)

`/root/collect_plugins_store_gitverse` + `/root/review_plugins_store_gitverse`: accepted-with-gaps, 7 уникальных фактов на SHA `08ddcb84661a148b66d691f4f06fd6779e67b793`. Reviewer проверил все 1 321 blob paths, пять ключевых файлов плюс LICENSE, их SHA-256, 698 catalog IDs и различия с GitHub/Codeberg. Принято 7 facts; осталось 1 315 файлов и прочие artifacts, runtime/CI не запускались. Spawn был задан `gpt-6-luna`, но reviewer self-reported фактический GPT-6; телеметрии модели нет, поэтому этот источник помечен как проверенный по содержанию, но фактическое соблюдение Luna не подтверждено. [Источник](sources/plugins-store-gitverse.md), [review](reviews/plugins-store-gitverse.md).

Пересобрана wiki: 72/76 проверенных источников, 2 131 факт и 1 911 API-строк; manifest сверил 3 190 файлов. Linter оставил 4 ошибки только для источников в очереди и 37 evidence-locator warnings.


## [2026-09-28] unavailable-verified | Opexgram 12.10.1 beta4 APK

`/root/collect_opexgram_apk` + `/root/review_opexgram_apk` (spawn requested `gpt-6-luna`): verdict `unavailable-verified`, 17 unique facts. Reviewer merged one duplicate about PNG/Quote Studio, verified the Telegram post `TechCsl/6548`, and confirmed that no APK binary is available from the post preview or local workspace. The 78 MB post attachment and separate 73.15 MB beta4 search record cannot be identified as the same file; the radar SHA-256, `com.opexgram.*`, and code claims remain unverified. Facts are in canonical `work/` and packaged `wiki/facts/`; the reviewer could not independently confirm effective model telemetry. [Источник](sources/opexgram-apk.md), [review](reviews/opexgram-apk.md).

Пересобрана wiki: 73/76 проверенных источников, 2 148 фактов и 1 912 API-строк; manifest сверил 3 190 файлов. Linter оставил 3 ошибки только для источников в очереди и 37 evidence-locator warnings.


## [2026-09-28] review | Opexgram Telegram announcement

`/root/collect_opexgram_announcement` + `/root/review_opexgram_announcement` (spawn requested `gpt-6-luna`): `accepted-with-gaps`, 5 unique facts. Reviewer independently checked `TechCsl/6548` and the channel listing; confirmed 2026-08-24 15:31:57 UTC, filename `OpexGram @TechCsl.apk`, displayed size 78 MB, and attribution of the visible caption. Four statuses were corrected from `secondary` to `docs`. No duplicate exists within these five facts. The post does not verify APK bytes/features; no raw snapshot was saved. Reviewer context self-identified as GPT-6; effective Luna deployment cannot be confirmed from available telemetry. [Источник](sources/opexgram-announcement.md), [review](reviews/opexgram-announcement.md).

Пересобрана wiki: 74/76 проверенных источников, 2 153 факта и 1 912 API-строк; manifest сверил 3 190 файлов. Linter оставил 2 ошибки только для источников в очереди и 42 evidence-locator warnings.


## [2026-09-28] unavailable-verified | exteraGram-air-raid-alert

`/root/collect_air_raid_alert` + `/root/review_air_raid_alert` (spawn requested `gpt-6-luna`): `unavailable-verified`, 4 facts. Exact GitHub repo/name and `.elyx` searches yielded no result; GitHub Code Search returned 401, GitLab/Codeberg exact searches were empty, and Wayback CDX timed out/503. Reviewer independently verified the nearest KPM entry is a distinct `.eaf` artifact and its SHA matches the saved manifest, but no evidence links it to the `.elyx` mentioned in the radar. No implementation claims were made; a never-existed claim is not supported. [Источник](sources/air-raid-alert.md), [review](reviews/air-raid-alert.md).

Пересобрана wiki: 75/76 проверенных источников, 2 157 фактов и 1 915 API-строк; manifest сверил 3 190 файлов. Linter оставил 1 ошибку только для ожидающего ревью источника и 42 evidence-locator warnings.


## [2026-09-28] review | npm ExteraGram MCP 1.0.0

`/root/collect_exteragram_mcp_npm` + `/root/review_exteragram_mcp_npm` (requested `gpt-6-luna`): `accepted-with-gaps`, 10 unique facts. Independent review confirmed npm SRI SHA-512, SHA-1, and archive SHA-256; all 99 tar paths/sizes and 434341 unpacked bytes; pinned GitHub README/package.json byte matches; and the static discrepancy of 81 JS registrations versus README's 76. It corrected the owner claim (`catalystdev` uses Latin `l`, GitHub `cataIystdev` uses capital `I`) and clarified that `prepublishOnly` does not demonstrate a successful release build/tests. Build provenance for `dist/`, cryptographic signature validation, install/runtime MCP listing, tests, and device behavior remain unverified. Reviewer self-reported GPT-6; exact runtime model telemetry is unavailable. [Source](sources/exteragram-mcp-npm.md), [review](reviews/exteragram-mcp-npm.md).

Final rebuild: 76/76 sources reviewed, 2,167 facts, 1,925 API rows, 3,190 source-file hashes checked. Lint: 0 errors, 50 evidence-locator warnings.

## [2026-10-01] ingest | Kangel-Plugins/Plugins-Store (Full 705 Plugins Manifest & 704 Corpus Inspection)

Проинспектирован весь корпус репозитория https://github.com/Kangel-Plugins/Plugins-Store (705 файлов в git tree: 690 .plugin, 2 .Plugin, 13 .eaf, суммарно свыше 876 000 строк кода; учтена коллизия имен Unlimited_Pins.plugin на NTFS). Сформирован полный машинный манифест data/plugins-manifest.json с SHA-256, размерами, строками и категориями каждого файла. Для каждого раздела проведена парная обработка: сборщик (Collector, google-antigravity/gemini-3.8-flash) и независимый проверяющий (Verifier, gpt-6-luna). Доказательства привязаны к неизменяемому коммиту 00de67026419f9dbe3a2787bb1236e8aaead8f76.

Выделено 8 тематических источников-переборок:
1. `plugins-store-ui-customization`: 83 плагина, 35 фактов. UI, кастомизация, темы, блюр, ActionBar, Bulletin, диалоги.
2. `plugins-store-messages-chat`: 150 плагинов, 30 фактов. Перехват сообщений через on_send_message, форматирование, SendMessagesHelper, ChatActivity.
3. `plugins-store-hooks-reflection`: 40 плагинов, 40 фактов. Глубокий хукинг (hook_method, hook_all_methods), HookFilter (Condition, ArgumentNotNull), setAccessible.
4. `plugins-store-media-files`: 31 плагин, 35 фактов. FileLoader, DownloadController, MediaController, генерация голосовых и видеосообщений.
5. `plugins-store-network-async`: 138 плагинов, 35 фактов. Потоки threading.Thread, asyncio, WebSockets, сетевые мосты и прокси.
6. `plugins-store-dex-native`: 111 плагинов, 35 фактов. DexClassLoader, InMemoryDexClassLoader, пакеты Elyx (.eaf), ctypes memory patching.
7. `plugins-store-accounts-storage`: 127 плагинов, 24 факта. Мультиаккаунтность (UserConfig, AccountInstance), JSON/SQLite кэширование, настройки.
8. `plugins-store-automation-tools`: 25 плагинов, 30 фактов. Автоматизация, поиск диалогов, пакетные утилиты, администрирование.

Собрано 264 новых структурированных факта (code и inference четко разграничены). Итоговый реестр facts.json расширен с 2 189 до 2 453 фактов при строго 0 дубликатах. База данных SQLite пересобрана и верифицирована (190 runs, 84 sources).
