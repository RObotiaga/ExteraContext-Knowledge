---
type: review
source_id: opexgram-docs
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: yearningss/opexgram-docs

- **Вердикт:** `accepted-with-gaps`.
- **Scope:** только документационный репозиторий `yearningss/opexgram-docs`, ветка `main`, pinned SHA `31388f39340c210765471d235f7ab51a760177e0` (snapshot от 2026-09-27). Заявленная версия Opexgram — 12.10.1-beta6. Это отдельный источник от упомянутой в радаре сборки APK 12.10.1-beta4; данные и версии между ними не объединялись.
- **Идентичность и целостность:** `snapshot.json` указывает тот же репозиторий, SHA и `status: available`; `tree.json` содержит `truncated: false`. Все четыре файла из `file-manifest.json` (`README.md`, `docs/ai-integration.md`, `docs/badges-api.md`, `docs/settings-reference.md`) проверены по числу байт и SHA-256 — совпали. В tree есть также `.gitignore`; он не входит в manifest сохранённых текстов и не содержит относящегося к API документа. Лицензия не указана в сохранённых GitHub metadata.
- **Радар:** `radar-context.md` содержит описание APK beta4 и общие поисковые выводы, но `radar-urls.json` пуст. Сверено назначение как документационного источника; утверждения радара не приняты за свидетельство этой документации или pinned beta6.

## Независимое покрытие

Прочитаны целиком все сохранённые Markdown-файлы:

- `README.md` (155 строк): заявленные Android/Telegram версии, multidex и имена пакетов/модулей, Badges, AI, LRCLIB, UI, export и storage. Ссылка `docs/architecture.md` ведёт на файл, которого нет в полном tree.
- `docs/ai-integration.md` (68 строк): endpoints-подсказки Gemini/OpenAI, summary prompt/trigger, fact-check JSON и UI, multipart transcription, сериализация истории и Q&A prompt.
- `docs/badges-api.md` (202 строки): базовые URL/headers, snapshot и tuple schema, все семь endpoint, примеры payload/response, ETag interval, nonce/poll лимиты, bearer auth, developer key, поля профиля и badge/caption update.
- `docs/settings-reference.md` (64 строки): все 26 перечисленных ключей, типы, описания и задокументированные диапазоны/значения.

## Найденное и исправленное

- Дополнен факт `opexgram-docs-008`: теперь он фиксирует не только позиционный кортеж `badges[]`, но и top-level поля примера `/v1/badges`: `version`, `tier1_document_id`, `info_url`, `buy_url`, `prices`, `caption_max`, `badges`.
- Дополнен `opexgram-docs-012`: перечислены все поля примера `/v1/me` (`tier`, `document_id`, `changeable`, `change_available_at`, `has_caption`, `caption`) вместе с документированным поведением 401.
- Уточнён `opexgram-docs-003`: `summary` ограничен 110 символами, `sources[]` содержит URL.
- В `opexgram-docs-020` добавлен пропущенный сетевой ключ `opexgram_proxy_vpn`.
- Дополнено описание экспорта точными заявленными типами медиа (фото, видео, голосовые, анимации, стикеры), offline HTML и именем `ChatExportService`; отдельно добавлен факт `opexgram-docs-023` о заявленной базе/версии, multidex и названиях модулей, с явной пометкой о том, что исходники/плагинный SDK в snapshot отсутствуют.
- В source frontmatter поставлены `review_status: accepted-with-gaps` и ссылка на этот отчёт.

## Точность, повторы и границы

Схемы и поведение представлены как `docs`; документация описывает внешний REST-сервис и функции клиента, но это не проверенные объявления или вызовы API плагинов. Примеры endpoint/prompt/schema точно ограничены приведённым текстом. Факт о metadata пакетов не утверждает, что такие классы доступны стороннему плагину. Сигнатуры SDK, hooks, поля/ошибки вне примеров и runtime-поведение не выведены из README.

Проверены 23 уникальных ID фактов; одинаковых ID и дословно дублирующих фактов внутри этого набора нет. Ключ `opexgram_lyrics` и LRCLIB GET относятся к разным сведениям — preference и заявленному сетевому/UX сценарию. Badge endpoint и tuple/schema snapshot также оставлены отдельными фактами. Канонически для будущего синтеза: AI — topic `ai`; REST/auth/cache — `badges-api`/`network`/`accounts`/`storage`; настройки — `settings`; LRCLIB — `media`; export — `storage`.

## Остаточные gaps

- Доступны только документационные файлы: отсутствуют APK/manifest, исходники клиента, код SDK/loader плагинов, сервер Badges API, тесты и runtime capture. Поэтому claims о реальной реализации, потоках, lifecycle/account scope, разрешениях, thread safety, секретах и доступности функций для плагинов не подтверждены.
- AI integration перечисляет корневые URLs, но не задаёт точные модельные endpoints/HTTP методы и payload, аутентификацию/хранение ключей, ошибки, streaming, отмену, разрешения и privacy/data-retention. Формат `multipart/form-data` не является полной спецификацией upload.
- Badges — опубликованная в документации спецификация и примеры, не проверенный серверный контракт; нет проверки ответов сервиса, security properties nonce/token, rate limits и поведения недокументированных ошибок. `X-Opexgram-Dev-Key` нельзя считать пригодным для клиентского plugin-пакета.
- Settings reference не даёт defaults, миграций, lifecycle/scope, UI wiring или способа доступа из плагина. Подсказка о пяти DEX и сокращённых модулях не заменяет отсутствующий `docs/architecture.md` или код.
- Публичная лицензия и правовой режим интеграции/копирования не установлены. Runtime, build и tests не запускались.

**Итог:** `accepted-with-gaps`, 23 уникальных факта. Достаточно надёжно как индекс документационных контрактов и идей для дальнейшей проверки; недостаточно для утверждения, что описанные возможности существуют в сборке или доступны плагину.
