---
type: source
source_id: opexgram-docs
platform: Android (документация форка Telegram)
review_status: accepted-with-gaps
review: ../reviews/opexgram-docs.md
date: 2026-09-28
---

# yearningss/opexgram-docs — документация Opexgram для Android

Снимок ветки main на commit [31388f39340c210765471d235f7ab51a760177e0](https://github.com/yearningss/opexgram-docs/tree/31388f39340c210765471d235f7ab51a760177e0), полученный 2026-09-27T15:49:36Z. Репозиторий называет описываемую версию Opexgram 12.10.1-beta6; лицензия в GitHub metadata не указана. Сохранённые оригиналы и SHA-256 перечислены в raw/opexgram-docs/file-manifest.json.

Это документация, а не исходный код клиента или SDK плагинов. Ни одна описанная функция, схема API, ключ SharedPreferences или вызов не подтверждены реализацией либо запуском. Их можно использовать как требования и идеи для интеграции, но нельзя считать доступным API ExteraGram/AyuGram. Исходники и программы не запускались.

## Покрытие снимка

| Прочитанные пути | Извлечено | Пробелы |
|---|---|---|
| README.md (155 строк) | Заявленная база Android/версия, multidex и названия модулей, AI/LRCLIB, экспорт, UI, хранение и сводка Badges API | Это обзор и неподтверждённые описания; README называет одновременно Telegram for Android v12.x/v10.x (build 7), а заявленный docs/architecture.md отсутствует в сохранённом дереве. |
| docs/ai-integration.md (68 строк) | Заявленные Gemini/OpenAI endpoint, триггеры summary/fact-check/transcription/Q&A, форматы промптов и выборки истории | Нет кода клиента, точных HTTP-запросов к моделям, разрешений/жизненного цикла, обработки ошибок, streaming, хранения ключей и тестов. |
| docs/badges-api.md (202 строки) | Документированный REST-контракт, ETag-кеш, привязка через bot nonce, bearer token, операции профиля badge | Нет сервера или клиентской реализации; схемы и примеры — спецификация документации. Не исследовалась безопасность реального сервиса. |
| docs/settings-reference.md (64 строки) | Имена и предполагаемые типы ряда UI, privacy, swipe, haptics и lyrics настроек | Справочник не раскрывает читателей/писателей, defaults, миграцию, scope аккаунта, UI wiring или доступность ключей плагинам. |
| tree.json, snapshot.json, file-manifest.json, radar-context.md, radar-urls.json | Полнота снимка (дерево не усечено), идентичность версии, покрытие и контекст обнаружения | В tree 6 записей, из них 5 файлов и каталог docs (включая .gitignore); radar-urls.json пуст. Исторические ссылки на исходники Opexgram в радаре не представлены. |

## Технические факты и вызовы, описанные документацией

### AI и работа с историей

| Контекст / вызов в документации | Заявленное назначение и применение | Поток / аккаунт / ограничение | Evidence |
|---|---|---|---|
| Пакет LF4; Gemini https://generativelanguage.googleapis.com/v1beta, OpenAI https://api.openai.com/v1 | Встроенные backend'ы прямого обращения к LLM без Telegram-бота | Документация не даёт реальных сигнатур, версий моделей, auth/config API или подтверждения запросов | [AI integration](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/ai-integration.md#L7-L13) |
| Триггер summary: кнопка над списком непрочитанных | Сжать длинную историю в краткий абзац; приведён system prompt, требующий только summary | Не описаны объём/пагинация истории, dispatch в фоне, отмена, аккаунт и privacy/redaction | [AI integration](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/ai-integration.md#L19-L26) |
| ai_fact_check в контекстном меню сообщения | Попросить модель вернуть JSON с summary и массивом URL-источников; результат описан как плавающий бейдж под сообщением | Не определены валидатор JSON, доверие/проверка URL, ошибка и точка внедрения меню в доступный plugin API | [AI integration](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/ai-integration.md#L30-L43) |
| Whisper/Gemini transcription; multipart/form-data, boundary OpexgramAiBoundary7f3d, prompt Transcribe this recording. | Транскрибация аудио голосовых и видеосообщений | Заявление о работе без Telegram Premium; не указаны endpoints Gemini для аудио, ограничения файла, временные файлы и согласие пользователя | [AI integration](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/ai-integration.md#L47-L54) |
| Исторический контекст [id] date author: text; Q&A prompt ограничивает ответ только историей и существующими ID | Представлять вопрос модели вместе с сообщениями; IDS: - для отсутствия совпадения | Способ разбора ответа и переход от ID к сообщению не описаны; сигнатуры API нет | [AI integration](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/ai-integration.md#L58-L68) |

### Badges REST-интеграция

Документированный базовый URL — https://badges.mk69.dev; примеры используют User-Agent Opexgram/12.10.1-beta6, JSON и bearer token. Это контракт внешнего сервиса в документации, не API Android-плагина.

| HTTP-вызов / схема | Документированное применение | Важные детали | Evidence |
|---|---|---|---|
| GET /v1/badges | Загрузить общий snapshot бейджей и настроек | If-None-Match, gzip, локальный badges.json; при 304 следующая проверка через 1 800 000 мс. Запись badges[]: peer_id, tier, document_id, flags, optional caption | [Badges API](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L24-L64) |
| POST /v1/link/start с {}; ответ {nonce, deeplink} | Начать связывание Telegram-аккаунта с badge service, затем открыть deep link бота | Bot @opexgrambadgesbot; одноразовый nonce описан примером, не приведены криптографические свойства/срок годности | [Badges API](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L68-L87) |
| GET /v1/link/poll?nonce={nonce} | Проверять завершение привязки и получить {token,user_id} | Интервал 2 секунды, максимум 60 попыток / 120 секунд. Отмена/повтор после таймаута не описаны | [Badges API](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L91-L109) |
| POST /v1/link/dev, X-Opexgram-Dev-Key | Документированный альтернативный вход разработчика с user_id в JSON | Секретный ключ передаётся заголовком; документация не говорит, как он provisioned/protected. Не переносить ключ в клиентский плагин | [Badges API](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L113-L132) |
| GET /v1/me с Authorization: Bearer <token> | Прочитать tier, document ID, право/время смены, caption | Документация утверждает: ответ 401 сбрасывает сохранённый токен; файл хранения в README — opexgram_badges.xml | [Badges API](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L136-L159), [README](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/README.md#L150-L155) |
| PUT /v1/me/badge с {document_id} | Выбрать Telegram Custom Emoji для бейджа пользователя | Документированы ответы 200/204; проверка валидности document ID не описана | [Badges API](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L163-L178) |
| PUT /v1/me/caption с {caption} | Изменить текст всплывающей подписи бейджа | Длина ограничена динамическим caption_max из snapshot /v1/badges | [Badges API](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L182-L202) |

Поля примера глобального snapshot: `version`, `tier1_document_id`, `info_url`, `buy_url`, `prices[]`, `caption_max`, `badges[]`. Запись `badges[]` позиционная: `peer_id`, `tier`, `document_id`, `flags`, необязательный `caption`; документация трактует положительный `peer_id` как пользователя, отрицательный — как супергруппу/канал, а `document_id = 0` как стандартный эмодзи уровня ([Badges API lines 41–64](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L41-L64)). Пример `GET /v1/me` содержит `tier`, `document_id`, `changeable`, `change_available_at`, `has_caption`, `caption` ([Badges API lines 148–159](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L148-L159)).

В AI fact-check документированный объект ответа имеет `summary` до 110 символов и `sources[]` с URL; другие поля, схема ошибки, проверка источников и способ вызова модели не описаны ([AI integration lines 30–43](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/ai-integration.md#L30-L43)).

### Практические идеи и границы переноса

- Для интеграции, зависящей от изменяемого каталога, документация показывает схему ETag + локальный snapshot + ограниченный интервал обновления. Её можно взять как проектный образец; для реального плагина нужно отдельно выбрать разрешённое хранилище и сетевые API целевого SDK.
- Для привязки к внешнему сервису описан nonce/deep-link/polling workflow с ограниченным timeout. Перенос требует безопасного хранения токена, UI отмены и серверной проверки; ничего из этого не следует считать уже предоставленным Opexgram API.
- Для AI-операций источник даёт точки входа и формат контекста, достаточные для постановки требований к прототипу, но не показывает loader/hooks SDK для добавления меню, кнопку или доступ к истории в плагине.
- README заявляет LRCLIB `GET /api/get`, разбор исполнителя/названия/альбома/тайминга и показ `syncedLyrics` с автоскроллом и подсветкой. Экспорт назван Foreground Service `com.opexgram.core.ChatExportService`, создающим автономный HTML без сети и включающим фото, видео, голосовые заметки, анимации и стикеры; ни реализаций, ни точных сигнатур этих компонентов в снимке нет ([README lines 114–140](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/README.md#L114-L140)).
- README называет Android-приложение Opexgram, основу Telegram for Android v12.x/v10.x (build 7, App ID 10437595), multidex из пяти DEX, пакеты `org.telegram.*`/`com.opexgram.*` и сокращённые модули `LJ4`, `LF4`, `LM4`, `Lb6`; это недоказанные документационные утверждения, а не доступные классы или SDK плагина ([README lines 21–49](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/README.md#L21-L49)). README также называет `OpexgramSecrets` фасадом/средством целостности, но его интерфейс и реализация не приложены ([README lines 39–47, 150–155](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/README.md#L39-L47)).
- Справочник перечисляет 26 ключей SharedPreferences: графика/интерфейс, чаты/приватность, свайпы/вибрация, lyrics/стикеры/иконки и сеть (`opexgram_proxy_vpn`, `opexgram_updates`). Таблица не указывает defaults, миграцию, scope аккаунта, места чтения/записи или API для плагинов; наличие имени не доказывает работающий UI или доступность ключа из плагина ([settings reference](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/settings-reference.md#L7-L64)).

## Противоречия и незакрытые пробелы

- README указывает Opexgram 12.10.1-beta6, а контекст радара касается отдельного APK beta4 и его наблюдений. Эта страница не подтверждает APK-анализ и не смешивает версии или функции между источниками.
- README ссылается на docs/architecture.md, но файла нет в полном tree снимка. Указанные в README сокращённые пакеты LJ4, LF4, LM4, Lb6 и архитектурные названия — только заявления документации.
- Не сохранены исходники приложения, Android manifest, SDK/loader для .plugin, сервер Badges API, тесты и runtime-логи. Поэтому неизвестны реальные сигнатуры, thread/account lifecycle, разрешения, сетевой стек, поведение ошибок и доступность описанных возможностей сторонним плагинам.
- В метаданных GitHub лицензия отсутствует. Для копирования кода (которого здесь фактически нет) и интеграционного использования следует отдельно выяснять правовой статус.
- radar-urls.json пуст; документированных исторических commit-ссылок для сравнения версий нет.

## Источники снимка

- [README.md](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/README.md)
- [docs/ai-integration.md](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/ai-integration.md)
- [docs/badges-api.md](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md)
- [docs/settings-reference.md](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/settings-reference.md)
