# Независимая проверка: `vestr-plugins`

- **Источник:** `mr-Vestr/plugins`, pinned commit [`c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c`](https://github.com/mr-Vestr/plugins/tree/c56e9d7119a1cdb46134acc8b5c4f1b8c9359c4c), снимок от 2026-09-27 15:53 UTC.
- **Проверка идентичности:** GitHub Commit API независимо вернул тот же SHA, сообщение `Update ADB Lite link to English documentation`, дату `2026-08-31T16:18:35Z`, tree SHA `c1f4671ffdbb19d7c392355cae7a16193c684cec` и verified signature. Полное дерево не truncated. SHA-256 каждого из 15 файлов `file-manifest.json` побайтно совпадает с локальным capture; missing files и checksum mismatches нет. Отдельного LICENSE в pinned tree нет, GitHub repository metadata даёт `license: null`.
- **Область чтения:** прочитаны оба README, четыре config JSON и RU/EN руководства Templates, Plugin creator и ADB Lite целиком. В коде проверены metadata и центральные implementation paths: plugin load/unload и hooks, template persistence/send/topic/import/config/update, file creation/send/save/install, ADB HTTP parser/routes/pairing/install/NSD/storage/lifecycle/update. Три реализации имеют 7 798, 5 517 и 4 451 строку соответственно; они не проверялись построчно, весь UI и все error paths не инвентаризованы.
- **Вердикт:** `accepted-with-gaps`.

## Независимое покрытие

Pinned tree содержит Templates, Plugin creator и ADB Lite: их исходники, metadata/config, двуязычные manuals, два README и screenshots. Изученные плагины — интеграционные примеры ExteraGram/AyuGram Python host, а не Plugin SDK или спецификация host API. Их сигнатуры и вызовы в справке привязаны к commit permalink и остаются call-sites конкретного снимка. Ни установка, ни запуск плагинов/host клиента, Desktop companion, ни протокол не проверялись.

`radar-context.md` указывает другие проекты; прямого назначения или описания `mr-Vestr/plugins` в локальном контексте нет. `radar-urls.json` пуст. Поэтому роль источника сопоставлена по source page и первичным README/руководствам, а не подтверждена ссылкой радара. Это не мешает проверке первоисточника, но исходное radar provenance для выбора именно этого репозитория отсутствует.

Снимок кода содержит базовые возможности, отражённые на source page: ограничения и настройки Templates, send hook и entities, topic reply call-site, `.templates` import hook, Plugin creator command/send-button/file paths, ADB Lite manual TCP server, token pairing, mDNS, preferences и install branching. Manuals добавляют documented UI workflows и настройки редактора; эти claims размечены `docs`, отдельно от статического кода. Call-sites внутренних Java методов не названы стабильными SDK контрактами. `runtime-verified` facts не добавлялись.

## Найденные проблемы и исправления

- Снимок уже содержал `TEMPLATES_EN.md`, `PLUGIN_CREATOR_EN.md` и `ADB_LITE_EN.md`; первоначальная coverage table ошибочно называла их отсутствующими. Прочитаны все три файла, coverage и расхождения с кодом обновлены. Также исправлены размеры реализаций: 7 798 / 5 517 / 4 451 строка; прежние 7 477 / 5 261 / 4 202 не совпадали с локальными файлами.
- Языковое противоречие стало точнее: обе Templates manuals говорят о двух языках, README говорят о 16, а code содержит 16 locale codes плюс `system`. Fact и source page исправлены. Реальная полнота translation strings и наличие опций в runtime не установлены.
- Добавлен пропущенный document-backed набор Plugin creator editor actions и toolbar/info settings; он явно отмечен как README/manual claim, без обещания runtime подтверждения.
- Добавлены parser framing details ADB Lite: предел чтения pre-header, `Content-Length`, socket timeouts; отсутствие видимой `Transfer-Encoding` обработки оставлено ограниченным выводом по просмотренному коду, а не доказательством сетевого поведения.
- Зафиксированы update flows всех трёх плагинов, которые используют mutable `refs/heads/main` configuration и URL загружаемого artifact. Эти remote responses/artifacts не являются частью pinned capture.
- Найдено два соседних `threading.Thread(target=download_thread, daemon=True).start()` в Templates updater, при одном запуске в сравниваемых Plugin creator и ADB Lite paths. Это отмечено как source-level possible shared-temp-path race (`inference`), не как воспроизведённый runtime bug.
- Лицензионное утверждение оставлено как вывод из metadata/tree: разрешение на повторное использование этим снимком не установлено.

Machine facts содержат **28 уникальных фактов**, повторяющихся ID нет. Добавлены IDs `vestr-plugins-025`–`028`; факт о языках уточнён. Внутри source page устранено повторение языкового disclaimer. Другие source pages, общий index и topic/API/recipe синтез не менялись.

## Дубликаты и канонизация

Поиск по source pages, topics, APIs, recipes и общему facts JSON не нашёл уже описанных Vestr-specific механизмов или второго ADB Lite источника. Известные пересечения с общей SDK документацией относятся к независимым подтверждениям host hooks; конкретные `MessageSendPreview`, `prepareSendingDocumentInternal`, `AndroidUtilities.openForView` и Telegram internal call-sites следует держать как source-specific examples, пока host version не совпадает и не подтверждён отдельный SDK контракт.

Для будущего synthesis: общие plugin lifecycle и hook composition → `lifecycle`/`hooks`; ADB Lite TCP, request framing, CORS, token, update endpoints → `network`/`security`/`distribution`; device/template persistence → `storage`; reflection-based client calls → `apis` только с точной платформой/версией и оговоркой private host internals. Не объединять это с iOS ViboGram Python contract или другими несовместимыми plugin loaders только из-за общего `.plugin` расширения.

## Остаточные пробелы

- Реализации крупные и проверены выборочно, не построчно; не установлена полнота каждого settings branch, UI path, migration/error case, language string и hook cleanup.
- В pinned tree нет build files, CI workflow или test suite; build/test результат отсутствует. Код, plugin packaging/install, thread race, updater downloads, ADB Desktop integration, network interoperability/security и поведение на ExteraGram/AyuGram не запускались и не проверялись. Необходимые host SDK/client internals для подтверждения private Java signatures не входят в источник.
- `mr-Vestr/adb-lite-desktop` — отдельный репозиторий, только linked/documented здесь; его код и matching protocol contract не изучены. Текущие ответы `refs/heads/main` и download URLs намеренно не fetched; они могут отличаться от pinned commit.
- Совместимость обоих клиентских форков и работа метаданных `__min_version__` не подтверждены на конкретных версиях. Полнота лицензии/права на использование из `license: null` и отсутствующего LICENSE файла не установлена.

Этот вердикт принимает статические сведения о доступных файлах снимка с названными ограничениями; он не даёт гарантии полноты по неразобранным веткам, внешнему Desktop companion, host SDK/client или runtime.
