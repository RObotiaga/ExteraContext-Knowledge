---
source_id: radar-corpus
review_status: accepted-with-gaps
review: ../reviews/radar.md
review_scope: "radar.md SHA256 B7074AEA3FB2D4A20367C3DB971856E93D617936558AD852CCD6099C74A73100; export.json SHA256 F76C499B06C688924AEBF5F4390298FE0C5E4C47C406A18313D8E52260297D24; export-text.md SHA256 6DFDE68FF7AB9C8EA86528D4A8E67C36A46533292BB989BFDC170806B0848591"
source_candidate_count: 66
non_source_reference_count: 15
---

# Radar: карта утверждений и кандидатов на первоисточники

**Статус:** вторичный отчёт, собранный в разные дни; не является подтверждённой документацией ExteraGram/AyuGram и не устанавливает контракт API. Технические утверждения ниже — указатели на места, которые нужно сверять с кодом репозитория, документацией SDK соответствующей версии, APK либо воспроизводимым поведением. Таблицы в исходнике часто потеряли названия репозиториев в первой колонке; такие пробелы оставлены как потерянные данные, не заполнены догадками.

**Источники:** [`raw/radar.md`](../../raw/radar.md), 5253 строки, и [`raw/radar-export-text.md`](../../raw/radar-export-text.md), 5512 строк. Второй файл экспортирует те же ранние сообщения и добавляет диалог 26 сентября и сравнение developer tools; это один корпус, не отдельная пара источников. Диапазоны с префиксом `export:` ниже относятся ко второму файлу. Неизменённый JSON export находится в [`raw/radar-export.json`](../../raw/radar-export.json). Нормализованный реестр содержит 66 уникальных записей кандидатов с `canonical_source_id`, `relationship` и `identification_status`; отдельно перечислены 15 технических и платформенных упоминаний, которые не являются подтверждёнными самостоятельными источниками: [`radar-source-candidates.json`](../source-candidates.json).

## Тематический указатель

### Начало радара: plugin runtimes, примеры и предложения переноса (строки 1–422)

- **1–60:** SyncProfile, ViboGram и кроссплатформенная структура Python-плагина; функции NiagramX (одна галочка, кэш перевода, загрузка) и идеи ASCII art. В первых таблицах названия репозиториев в колонке «Репозиторий/Источник» пусты. Параметры SyncProfile и ViboGram — заявления отчёта.
- **62–180:** extCLI как shell/developer console, `re-extera` как Python+DEX пример, ViboGram Plugin Store и hook marker; звук Telegram iOS и архитектурные идеи. Таблица проектов в строках 76–80 с утраченной первой колонкой. Утверждения о TLRPC, установочных методах и SDK — требуют проверки против точного SDK/клиента.
- **184–237:** короткие реплики пользователя/ответы и переходы отчётов; самостоятельных устойчивых технических выводов мало.
- **238–312:** Chat-Stats-Plugin, Smooth-Scroll-Plugin и re-extera; ViboGram — история заменённого медиа, Margelet Dim/Rainbow/Size, `.ascii`, badges; советы по выносу ASCII обработки в host.
- **313–422:** AltyLib как набор библиотечных абстракций и функций клиента/переноса (массовые действия, AI-feed и др.). Состав и актуальность AltyLib в отчёте не подкреплены ссылкой; полезность библиотеки не означает пригодность как runtime-зависимости.

### Miogram, Opexgram, клиенты-доноры и инструменты сборки (строки 423–779)

- **423–549:** `mioplugin`/Miogram SDK, документация и каталог; изменения runtime в exteraless; идеи Multi-Chat, Smart AI Feed, Kanban, Floating Chat, Custom UI Studio. Репозиторий `mioplugin` не указан, а несколько ячеек таблицы проектов пусты.
- **550–595:** анализ APK Opexgram 12.10.1 beta4: AI, Quote Studio, экспорт чата, Scheduled Gifts, badges, свайпы и UI. Это пересказ анализа APK; единственная ссылка рядом ведёт к Telegram-анонсу, который подтверждает только часть перечня. APK надо считать отдельным проверяемым артефактом.
- **599–753:** extera-gradle-plugin, Kotlin/DEX template, AyuGram Desktop PLEngine, re-extera hooks/regex inspector, Miogram lyrics и online halo, NiagramX Repeat One. Таблица найденных проектов в строках 607–612 лишилась имён. Утверждения об API desktop PLEngine относятся к другой платформе, не к Android BasePlugin.
- **754–779:** запрос и ответ о каталоге KPM. Зафиксированы новый путь GitHub и зеркала Codeberg/GitVerse; это URL-происхождение, сообщённое в самом отчёте, не проверка текущей доступности.

### Клиенты, плагины, каталоги и SDK (строки 780–1863)

- **780–1037 (7 сентября):** `tg-streaks`, минимальный `iptag-plugin-Exteragramm-`, обновления re-extera; Mercurygram folders, search operators, локальные drafts, символы, NiagramX proxy и Miogram music search. Раздел содержит заметное повторение оценок/статусов клиентов.
- **1038–1239 (8 сентября):** KPM и Link Guard, transfer `exteraStuff/gradle-plugin`, Miogram Cloud Vault, декоративные Unicode-названия, proximity sensor, crop/edit photo, email auth code; ряд описаний о KPM ограничен доступным тогда индексом.
- **1240–1482 (9 сентября):** `gradle-plugin` manifest icon, `tcp2ws` из Nullgram, NullcoreGram media confirmation/video gestures/DoH, AyugramX local folders/presets; часть заголовков и таблиц не даёт URL первоисточника.
- **1483–1578:** пользовательское решение о developer skills и список репозиториев `exteraSkill`, `exteragram-plugin-skill`, `exteragram-plugins-skill`, `exteragram-plugin-template`, re-extera, exteraless, n08i40k template и exteraStuff toolchain. В этом месте даны имена, но не URL.
- **1579–1863 (10 сентября):** `re-extera` regex/filter work; Miogram Plugin Forge, Go/WASM, AI Sheet, Cloud Vault; NullcoreGram DoH; KPM-проверки и список сравнительных клиентов. Это сочетает наблюдения за кодом с рекомендациями по новым плагинам.

### Срезы 11–16 сентября (строки 1864–3862)

- **1864–2182 (11 сентября):** `for-vibecoders`, `exteraPluginsRobot`, ReqGram, Miogram AI Companion/Vault, NiagramX text animation/forward count, Mercurygram push watchdog. Ссылки на перечисленные проекты частично сохранены; таблицы функций описывают переносимость, а не подтверждённый API контракт.
- **2183–2397 (12 сентября):** `tg_ws_proxy.plugin` и upstream `Flowseal/tg-ws-proxy`, CEPS, Link Guard, exteraStuff/gradle-plugin; затем Miogram YouTube Music и AI-transcription/Chaquopy, Telegram-iOS layout. Security/build claims требуют проверки самого pipeline и threat model.
- **2398–2602:** музыкальный поиск, транскрибация, Chaquopy `.py` runtime, UI layout; отдельные «что проверено» статусы, в том числе KPM. Повторные рекомендации сводить в один тематический плагин.
- **2603–3011 (13 сентября):** Link Guard 1.5.0; Miogram Anti-TSPU/Fake-TLS, Presence, multi-step AI agent, GitHub plugin catalog; NiagramX unread priority и blocked-user avatar. Много архитектурных рекомендаций выходит за Python BasePlugin и требует DEX/native/backend.
- **3012–3408 (14 сентября):** tayugram-mcp, exteraPluginsRobot moderation stats, Gradle publish task; Miogram Push Doctor, NiagramX join date, exteraless hidden accounts, Roblox presence. Часть новых repo строк дана без прямых ссылок.
- **3409–3628 (15 сентября):** NiagramX per-chat password/biometric и navigation bar; Miogram image-aware AI и Lua plugin manager; остальные client changes. Отчёт сам оговаривает, что compatibility/plugin implementation не подтверждена.
- **3629–3862 (16 сентября):** air-raid-alert plugin, DEX Gradle pipeline, exteraless DEX compatibility; NiagramX Live Photo, Mercurygram local pinning, exteraless HDR/video decoder. Не смешивать клиентские функции и зрелость соответствующего плагина.

### Срезы 17–22 сентября (строки 3863–5010)

- **3863–4098 (17 сентября):** `xwwvv/ios-bubble-outline` как Kotlin/DEX пример; NiagramX emoji packs; Mercurygram local drafts, link tracking cleanup и подтверждения ссылок. Повтор локальных черновиков со строками 923 и 3972 — одна тема, отдельные даты.
- **4099–4228 (18 сентября):** NiagramX map provider/OSMDroid, Mercurygram custom notification sounds, Miogram Android 16 DEX-core signal; раздел исключений и проверки.
- **4229–4558 (19 сентября):** `yearningss/exteraGram-docs` и перечисленные страницы архитектуры/hooks/SDK/backend/settings/UI/AI; затем функции других клиентов: Instant View, стартовая папка, folder reorder и Premium promo UI. Указанные docs — вторичная документация, сверять каждый API-символ с кодом и JAR.
- **4559–4748 (20 сентября):** Miogram/Amegram dynamic hotpatch и anti-censorship, NiagramX proxy recovery, Amegram local AI; отдельно отмечены риски старых моделей и ограниченная переносимость.
- **4749–4950 (21 сентября):** exteraless Vosk transcription, launcher shortcuts Ghost/Safe Mode, скрытие Gift-кнопки; затем общие client checks.
- **4951–5010 (22 сентября):** NiagramX resources optimization и выводы для Kotlin/DEX packaging. Наблюдение об оптимизации в отчёте нельзя принимать за универсальную проблему сборки.

### Поздние находки и ExteraGram MCP (строки 5011–5253)

- **5011–5195:** `stxlvn/exteragram-av1-sw-decoder`, exteraless runtime compatibility; Cloud Sync settings, scheduled send under Ghost Mode и Story warning. Decoder/API, поддерживаемые кодеки и ограничения надо подтвердить в исходнике/сборке.
- **5196–5253:** пользователь уточняет, какой проект называли «exteragram mcp»; ответ идентифицирует `cataIystdev/exteragram-mcp`, утверждает 76 инструментов/18 групп и npm `@catalystdev/exteragram-mcp` 1.0.0, затем перечисляет соседние проекты. Проверить совпадение написания owner (`cataIystdev` vs `catalystdev`), GitHub package и список tools.

### Добавления из экспорта диалога (export: 5176–5512)

- **export: 5176–5235:** пользователь вспоминает ExteraGram MCP. Перечислены его функции, ADB workflow и соседние `n08i40k/exteragram-plugin-template`, `catalib`, `exteragram-utils`, `SHAJON-404/re-extera`; возраст документации MCP отмечен как возможный риск. Точные API/числа tools — утверждения отчёта.
- **export: 5237–5316:** сравнение аналогов MCP: `makarworld/exteragram-plugin-skill`, ещё один agent skill с потерянным именем, `exteralib`, `catalib`, `mr-Vestr/plugins` и официальный сайт [ExteraGram Plugins Docs](https://plugins.exteragram.app/docs). Перечисленные здесь библиотеки и инструменты добавлены как кандидаты только если названы как самостоятельный developer source; общие платформенные зависимости вынесены в отдельную группу JSON.
- **export: 5318–5512 (26 сентября):** `ferelking242/novagramx` как клиент-донор с Regex Message Firewall, локальным last-seen tracker и password-protected privacy switches; `exteraless` как открытая реализация plugin runtime/permissions. Также проверены NiagramX, Mercurygram, Cherrygram, Nekogram/NekoX, TeleVip и старые Nagram-форки. Имена проектов в начале нескольких предложений потеряны, но URL к конкретным репозиториям сохранились.

## Результат сверки полноты и идентичности реестра

Реестр нормализован по уникальным идентичностям источников, а не по числу названий в сообщениях. Он содержит **66 source candidates** и **15 non-source references**. Первый список объединяет повторы и связывает зеркала/переименования; второй сохраняет API, платформы, зависимости и технологии как контекст, не заявляя, что их отдельную официальную документацию изучали. Состав всех записей, aliases и статусы дан в JSON-реестре.

Исправлены следующие ошибки идентичности и полноты:

- Официальные ExteraGram Plugin Docs и упоминания SDK/PySDK сведены в одну документальную идентичность. Номера версий и разные даты сохранены как отдельные утверждения радара, а не как доказательство единой runtime-версии.
- Основной KPM-репозиторий имеет одну запись; Codeberg и GitVerse отражены как сообщённые зеркала с непроверенной синхронностью. Старое написание `KangelPlugins/Plugins-Store` хранится как legacy-ссылка, но не автоматически отождествляется с текущим репозиторием.
- Неименованный skill из экспорта объединён с `fossSquad/exteraSkill`: совпадают дословное описание GitHub, темы `exteragram`/`ayugram`/`xposed` и дата обновления 31 июля 2026.
- Старый `n08i40k/exteragram-plugin-template` связан с указанным в инвентаре адресом `exteraStuff/pydex-plugin-template`; прошлый адрес сохранён как redirect alias, а история redirect помечена как не проверенная содержимым этого корпуса.
- `cataIystdev/exteragram-mcp` и npm-пакет `@catalystdev/exteragram-mcp` представлены отдельно: это разные опубликованные артефакты. Пакет явно связан с репозиторием, но совпадение tarball с исходным кодом не проверено.
- Анализ APK Opexgram 12.10.1 beta4 отделён от документации `yearningss/opexgram-docs` beta6. APK недоступен; beta6 docs не используются как замена и не подтверждают функции beta4. Telegram-анонс подтверждает только часть пересказа.
- В список добавлены/уточнены адреса `DedyaSergey/Chat-Stats-Plugin`, `DedyaSergey/Smooth-Scroll-Plugin`, `cataIystdev/catalib`, `fossSquad/exteralib`, `Islite/AniList.co` и `qwq233/Nullgram`. Для последнего связь с конкретным упоминанием `tcp2ws` остаётся вероятной, но не установлена без проверки пути и commit.
- `GitHub REST/Contents API`, Telegram API/TLRPC, Gradle/Kotlin/R8, ExteraGram/AyuGram как платформы и остальные зависимости перенесены в `non_source_references`. Их упоминание в сообщениях не означает, что отдельные API-документы или документация технологий были просмотрены.

Остались нерешёнными идентичности `exteragram-utils`, air-raid-alert plugin и `NagramXTurbo`; `AyuGram Desktop PLEngine / plugin sample` не имеет точного репозитория или URL. Они оставлены явно unresolved. Подробный перечень и основания находятся в [отчёте проверки](../reviews/radar.md).

## Противоречия, повторы и пределы источника

- **KPM path/status меняется во времени:** старое имя `KangelPlugins/Plugins-Store` объявляется недоступным, новый `Kangel-Plugins/Plugins-Store` — рабочим; в ранних частях каталогу приписывается 404/неполнота индекса, а позже говорится о фактическом чтении каталога (строки 72, 766–776, 782–788, 1034–1043, 1577, 1868, 2187, 3016, 3413, 3633, 3869, 4955). Это временные снимки, а не обязательно логическое противоречие.
- **Пустые ячейки таблиц:** названия проектов/источников отсутствуют в таблицах 9–13, 37–42, 76–80, 137–142, 240–244, 258–263, 354–358, 431–435, 607–612, 1046–1049, 1248–1253, 2611–2615, 3020–3024 и 3637–3641. В некоторых случаях текст соседних абзацев позволяет предположить имя; остальные нельзя восстановить только по этой странице.
- **Функции повторяются:** ViboGram ASCII art (41, 55–58 и 301–309), ViboGram text effects (261–263, 303–309), Mercurygram drafts (850, 923–944, 3925), Miogram Vault/AI/Presence и NiagramX media/proxy/UI идеи повторяются в ежедневных срезах. Повтор не является независимым подтверждением.
- **Устаревание и область платформы:** SDK версии 1.4.5.x, ExteraGram 12.10.1 и AyuGram Desktop PLEngine смешаны с датированными наблюдениями (92–103, 614–634, 1495–1562). При проверке фиксировать точный commit, сборку и Android/Desktop/iOS платформу.
- **Разные снимки документации/runtime:** экспорт сравнивает официальные docs SDK 1.4.4.3 и Python 3.11/Chaquopy 16 с утверждениями о exteraless Python 3.12; ранний радар описывает extCLI как совместимый с SDK 1.4.5.5 (export: 5190–5235, 5249–5314, 5463–5494). Это могут быть разные даты/клиенты, поэтому версии не сводить в одну текущую спецификацию.
- **Неизвестные имена в экспорте:** несколько репозиториев и skill в export: 5249–5281 и 5320–5328 имеют пустое отображаемое имя, хотя URL или описание сохранились. Кандидатный JSON помечает неустановленные owner/repo как отсутствующий URL/identity; не приписывать имя по предположению.
- **Вторичный характер утверждений:** исходник — ежедневные ChatGPT-ответы, а не первичные README/commits/docs. Оценки сложности, «стоит переносить», «не найден в KPM», перечисление поддерживаемых функций, поведение методов и API signatures не подтверждаются данным документом.
- **Потерянные URL:** отдельный JSON перечисляет `missing_url: true` там, где источник назван, но прямой адрес в radar не сохранился; `owner_repo` заполняется только когда явный формат owner/repo найден в самом файле. Имя, похожее на библиотеку или концепцию, не превращалось в предполагаемый адрес.
- **Технические пары не репозитории:** выражения `Python/BasePlugin`, `Java/Xposed`, `Kotlin/DEX`, `OpenAI/Gemini`, `LRCLib/ID3` и сходные конструкции — названия технологий/слоёв, не адреса GitHub. Для зависимостей и сервисов без точной идентичности URL оставлен пустым.

## Как использовать карту

Сначала откройте конкретный первоисточник из списка кандидатов, затем подтвердите заявленную функцию в коде/документации и запишите проверенную версию. Значения в `technical_claims_to_verify` — направления аудита, не готовые факты об API.
