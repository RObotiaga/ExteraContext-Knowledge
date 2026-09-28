# Независимая проверка: official-sdk

- Вердикт: **accepted-with-gaps**.
- Объём: официальный раздел документации <https://plugins.exteragram.app/docs>, все 33 HTML snapshots из `raw/official-sdk/manifest.json`, source page и JSON facts. Снимки получены 2026-09-27T15:48:33Z.
- SDK docs не дают commit SHA. SHA-256 manifest: `ABC56C5291E3077279FF3F0129433BB657EEC5D3DE0B3DF1E38CF21A23A20FE5`. Каждый HTML-файл присутствует и совпадает с размером в manifest; индивидуальные SHA-256 сняты во время проверки, исходные файлы не изменялись.
- В базе нет `raw/official-sdk/tree.json`, `radar-context.md` или `radar-urls.json`. Полнота навигации сверена по manifest и всем HTML. Версия PySDK 1.4.5.5 для сравнения сверена по экспортированному радару `raw/radar-export-text.md`; это вторичное свидетельство.
- Итог: source page лежит в [`../sources/official-sdk.md`](../sources/official-sdk.md). В `work/official-sdk-facts.json` 54 факта: уникальные ID, `claim` и `recipe` по-русски, названия API сохранены точно, labels статусов нормализованы к `docs` и `inference`.

## Покрытие первичных страниц

Все 33 страницы из manifest проверены по сохранённым ответам. Ниже приведён полный inventory с назначенной manifest областью и первичным URL.

| Snapshot | Область в manifest | URL первоисточника |
|---|---|---|
| `alert-dialog-builder` | dialog API | <https://plugins.exteragram.app/docs/alert-dialog-builder> |
| `android-utils` | UI thread, listeners, log helpers | <https://plugins.exteragram.app/docs/android-utils> |
| `available-libraries` | preinstalled packages | <https://plugins.exteragram.app/docs/available-libraries> |
| `bulletin-helper` | bulletin API | <https://plugins.exteragram.app/docs/bulletin-helper> |
| `class-proxy` | Java subclass/proxy DSL | <https://plugins.exteragram.app/docs/class-proxy> |
| `client-utils` | queues, requests, send/edit, controllers | <https://plugins.exteragram.app/docs/client-utils> |
| `common-telegram-classes` | source class index | <https://plugins.exteragram.app/docs/common-source-classes> |
| `dev-server` | TCP commands/debug | <https://plugins.exteragram.app/docs/dev-server> |
| `elyx-assets` | assets API | <https://plugins.exteragram.app/docs/elyx/assets> |
| `elyx-dependencies` | PIP/wheels/plugin dependencies | <https://plugins.exteragram.app/docs/elyx/dependencies> |
| `elyx-development-and-build` | ADB sync/build/reload | <https://plugins.exteragram.app/docs/elyx/development> |
| `elyx-elyxbuilder` | CLI/build/watch | <https://plugins.exteragram.app/docs/elyx/elyxbuilder> |
| `elyx-localization` | translation API | <https://plugins.exteragram.app/docs/elyx/localization> |
| `elyx-metadata` | identity/version/requirements | <https://plugins.exteragram.app/docs/elyx/metadata> |
| `elyx-modules-and-imports` | namespace/import rules | <https://plugins.exteragram.app/docs/elyx/modules-and-imports> |
| `elyx-project-structure` | archive/refmap | <https://plugins.exteragram.app/docs/elyx/project-structure> |
| `elyx-public-api` | stable Elyx exports | <https://plugins.exteragram.app/docs/elyx/public-api> |
| `elyx-quick-start` | structured plugin recipe | <https://plugins.exteragram.app/docs/elyx/quick-start> |
| `elyx-settings-storage` | persistent Elyx settings | <https://plugins.exteragram.app/docs/elyx/settings> |
| `elyx-troubleshooting` | failure diagnostics | <https://plugins.exteragram.app/docs/elyx/troubleshooting> |
| `elyx` | format overview | <https://plugins.exteragram.app/docs/elyx> |
| `file-utils` | directories, I/O, file handlers | <https://plugins.exteragram.app/docs/file-utils> |
| `first-plugin` | minimal plugin, send hook, settings | <https://plugins.exteragram.app/docs/first-plugin> |
| `hook-utils` | Java reflection | <https://plugins.exteragram.app/docs/hook-utils> |
| `intents` | global intent handlers | <https://plugins.exteragram.app/docs/intents> |
| `introduction` | SDK baseline and capabilities | <https://plugins.exteragram.app/docs> |
| `multi-account` | multi-account callbacks/helpers | <https://plugins.exteragram.app/docs/multi-account> |
| `pip-dependencies` | Python package manager | <https://plugins.exteragram.app/docs/pip> |
| `plugin-class` | metadata/lifecycle/hooks/storage | <https://plugins.exteragram.app/docs/plugin-class> |
| `plugin-settings` | settings row types | <https://plugins.exteragram.app/docs/plugin-settings> |
| `setup` | installation/setup | <https://plugins.exteragram.app/docs/setup> |
| `text-formatting` | HTML/Markdown/entity conversion | <https://plugins.exteragram.app/docs/text-formatting> |
| `xposed-hooking` | Xposed-compatible hooks | <https://plugins.exteragram.app/docs/xposed-hooking> |

Синтез покрывает API single-file плагина, hooks/lifecycle, UI, threads/queues, account scope, settings, reflection, Xposed, Class Proxy, отправку/форматирование текста, file handlers, Intents, Elyx structure/imports/assets/localization/settings/dependencies, ElyxBuilder, troubleshooting и DevServer. Common Telegram Classes описан как навигационный указатель к upstream-классам, не как доказательство API Python wrapper.

## Найденное и исправленное

- Страница лежала в `outputs/plugin-wiki/sources/`, хотя заданная структура требует `outputs/plugin-wiki/wiki/sources/`. Перенос выполнен после проверки абсолютных путей внутри базы. Относительные ссылки на raw изменены на `../../raw/official-sdk`; ссылка на facts также поправлена. Все локальные ссылки проверены.
- Все 50 исходных facts были на английском и использовали labels статусов вне схемы. Переведены `claim` и `recipe`; statuses приведены к `docs`/`inference`. Статусы `code` не назначались: исходный код SDK не был предоставлен.
- Явно сохранён version skew: Introduction сообщает SDK **1.4.4.3**; Multi-account требует SDK **>=1.4.5.0**; Elyx Metadata/Quick Start примерами используют SDK **>=1.4.5.3**. PySDK **1.4.5.5** упоминается радаром для конкретных проектов и не доказывает поддержку каждой сигнатуры docs этой версией. Intents отдельно указывает app version code `66999` / `12.6.4`, Class Proxy — `>=66690`; эти app gates не представлены как SDK версии.
- Уточнено различие ID: single-file допускает дефис, Elyx validator его отвергает. Исправлено описание правил Elyx ID и добавлен факт по troubleshooting.
- Добавлены отсутствовавшие сведения о необязательности ElyxBuilder и Python requirements, различии `--ast`/`--compile`, том, что watch не устанавливает архив на устройство, ключевых Elyx troubleshooting сценариях, `log`/`copy_to_clipboard`, Common Telegram Classes и пределах этих ссылок.
- Проверка повторов по нормализованным `topic + claim` не выявила дубликатов. Все 54 ID уникальны, evidence paths ведут к существующим raw snapshots/manifest. Повторяющиеся темы разрешено объединять при последующем тематическом синтезе с отдельным provenance.

## Остаточные пробелы и границы

- Нет `tree.json` или отдельных radar-context/URL captures именно для official-sdk; navigation coverage подтверждён manifest. PySDK 1.4.5.5 приведён в secondary radar export.
- Не предоставлены SDK source repository/commit и конкретная установленная сборка клиента. Сигнатуры, требования и feature gates подтверждены опубликованными страницами, но не кодом клиента.
- SDK/plugin runtime, hooks, accounts, threading, DevServer и ElyxBuilder не запускались. Поведение установленной версии, обработка исключений, concurrency и совместимость конкретного приложения остаются непроверенными.
- В просмотренных 33 страницах не найден permission declaration/grant API. Это наблюдение только по этим docs, не доказательство отсутствия API в коде клиента или других источниках.
- Upstream Telegram targets из Common Telegram Classes не загружались в рамках этого review. Документация сама предупреждает, что список TL schema может быть неактуальным.

В пределах snapshots не осталось противоречий, которые мешали бы источнику быть принятым с этими границами. Вердикт относится к документации; он не обещает абсолютной полноты по недоступному runtime или исходному коду.
