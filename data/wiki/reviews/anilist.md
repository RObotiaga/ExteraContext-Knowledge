---
type: source-review
source_id: anilist
reviewer: /root/review_anilist
model: gpt-6-luna
verdict: accepted-with-gaps
reviewed_at: 2026-09-28
---

# Независимая проверка Islite/AniList.co

## Область и закреплённая версия

Проверен источник `Islite/AniList.co`, commit [`69d542a692e13713a859869899679a80cb73eb55`](https://github.com/Islite/AniList.co/tree/69d542a692e13713a859869899679a80cb73eb55). Сборщик `/root/collect_anilist`, проверяющий `/root/review_anilist` — разные роли. Радары упоминают репозиторий как результат поиска и сомневаются, что он является developer-tool/BasePlugin проектом; проверенный код подтверждает более узкую формулировку: это Android plugin-интеграция AniList/Shikimori и полезный пример hook, очередей, контекста сообщений, settings и custom UI, а не SDK или инструментарий создания плагинов.

Подтверждена идентичность снимка: `snapshot.json` и `tree.json` указывают один SHA; дерево не усечено и содержит 16 entries: каталог `anilist_anime` и 15 файлов. Каждый из 15 файлов присутствует в `file-manifest.json`, локальный размер и SHA-256 совпадают, а вычисленный Git blob SHA-1 совпадает с соответствующей записью дерева. Лишних локальных файлов снимка не найдено. Обнаруженные ошибочные commit-ссылки на файлы в source page исправлены на полный pinned SHA; все file links теперь указывают на закреплённый снимок.

## Независимое покрытие

Сверены все 15 blob entries из `tree.json` и содержимое релевантных разделов; README в дереве нет. Разбор охватывает:

- `anilist_anime/main.py` — входной класс, `BasePlugin`, `on_plugin_load`, настройки, message hook, команды, ошибки и queue/UI-thread call-sites.
- `anilist_anime/api.py`, `constants.py` — AniList и Shikimori GraphQL/REST функции, query constants, заголовки, timeout, retry, разбор ответов, сезонные и жанровые поиски.
- `anilist_anime/search.py` — выбор provider, кэширование и парсинг результатов, передача account/reply/topic контекста, отправка текста/media/описания, multi-result и ongoing paths.
- `anilist_anime/mapping.py`, корневой `mapping.json` — загружаемый или inline mapping, aliases, scopes/separator config и локальная версия mapping.
- `anilist_anime/formatter.py` — titles, genres/tags/spoiler, display fields, description/cover source, template expansion.
- `anilist_anime/settings_ui.py`, `collapsible_ui.py` — configurable command aliases, provider selectors, mapping URL/JSON, collapsible settings groups, modes и callbacks.
- `anilist_anime/popup_ui.py`, `template_editor.py`, `chat_preview_ui.py` — UI entry points, result selection и local send options, token editor, preview and history behavior.
- `anilist_anime/utils.py`, `metainfo.yml`, `refmap.yml` — setting coercion, command parsing/cache cleanup, declared plugin metadata and entry point.

Проверены радарный фрагмент и идентичность из `radar-context.md`, `radar-urls.json` (пустой массив), `repository.json`, `snapshot.json`, `tree.json` и manifest. Наблюдения по большим Android UI-модулям основаны на их точках входа и относящихся к предмету обработчиках; визуальная проверка на Android и проверка host SDK отсутствуют.

## Результаты проверки и исправления

- Основные факты о метаданных, API call-sites, таймаутах, ретраях, search маршрутах, account/reply/thread-передаче и настройках совпадают с закреплённым кодом. Нет утверждений о runtime-совместимости или выполненном тесте.
- Исправлен `anilist-007`: GraphQL `errors` приводят к `tag_error`, только если ответ не содержит `data`; частичный ответ с `data` возвращается. Изначальная формулировка обобщала обработку ошибок чрезмерно.
- Сужен `anilist-003`: только ветви с обработанным непустым запросом явно возвращают `HookStrategy.CANCEL`. Для пустого tag/search query и обработанного исключения возвращается обычный `HookResult()`; семантика такого значения зависит от не включённого host SDK. Это также добавлено как отдельный gotcha (`anilist-022`).
- Нормализованы `evidence_path` у фактов, где имя модуля опускалось у дополнительных диапазонов; все 23 факта теперь имеют путь и проверяемый диапазон, ссылки ведут на pinned SHA.
- Добавлены детали, ранее недостаточно видимые в source page: `anilist-021` описывает placeholder editor, live preview, visibility toggles, ограниченную undo/redo history и сохранение; `anilist-023` — popup multi-select и параметры отправки, передаваемые callback-ам. Факт `anilist-020` ограничен наблюдаемым пользовательским выбором URL для mapping, без заявления о внешне проверенном сетевом эффекте.
- Внутри `work/anilist-facts.json` сейчас 23 уникальных ID (`anilist-001`…`anilist-023`), повторяющихся ID/дублей нет. Связанные по смыслу confirmations из других репозиториев могут храниться с отдельным provenance; canonical topic для тематического объединения — `hooks`, `threading`, `network`, `requests`, `workflow`, `storage`, `media`, `ui` и `security` согласно ID каждого факта. Это обзор интеграционного примера, не API-контракт ExteraGram.

## Остаточные пробелы

1. В полном закреплённом дереве нет README, LICENSE, тестов, CI-конфигурации или build/packaging файлов; GitHub metadata также имеет `license: null`. Инструкции автора, лицензия, воспроизводимый build/install flow и automated test status неизвестны.
2. `app_version >=12.8.1`, `sdk_version >=1.4.4.3`, версия `0.3.38` и `requirements: []` — только значения `metainfo.yml`. Код импортирует `requests`; снимок не показывает, откуда среда получает эту зависимость. Никакая целевая версия клиента не проверялась.
3. `main.py` показывает регистрацию hook на загрузке, но отдельный `on_plugin_unload` в классе не найден; удаляет ли hook host автоматически, из этих файлов установить нельзя.
4. Android UI, очереди, reply/topic delivery, отправка медиа, сетевые сервисы и popup lifecycle не запускались. Ни один факт не имеет `runtime-verified` status.
5. `api.py` комментарий объясняет браузерный User-Agent обходом Cloudflare, но эффективность/необходимость этого заголовка независимым сетевым наблюдением не подтверждена. AniList и Shikimori live schema/rate limits отдельно не сверялись.
6. При пустом mapping setting используется URL с плавающей веткой `main` внешнего mapping-репозитория; его содержимое не закреплено. Ошибка fetch/JSON молча заменяет mapping пустым словарём.

## Вердикт

**accepted-with-gaps.** Страница описывает роль проекта и подтверждённые кодом приёмы; существенные пробелы совместимости, сборки, лицензии, сети и runtime явно отмечены. Принятие не означает, что совместимость или поведение UI проверены на устройстве.
