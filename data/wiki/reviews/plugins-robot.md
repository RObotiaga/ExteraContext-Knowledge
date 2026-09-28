---
type: review
source_id: plugins-robot
review_status: accepted-with-gaps
reviewed_sha: 79021a05ecb77c8d7fca875298ffbac5970331aa
date: 2026-09-28
---

# Независимая проверка itsv1eds/exteraPluginsRobot

## Объём

Проверен pinned snapshot `itsv1eds/exteraPluginsRobot` на SHA [`79021a05ecb77c8d7fca875298ffbac5970331aa`](https://github.com/itsv1eds/exteraPluginsRobot/tree/79021a05ecb77c8d7fca875298ffbac5970331aa), а также первичный радар-контекст и подготовленная source page. Дерево не обрезано. Независимо повторно рассчитаны SHA-256 всех 60 сохранённых файлов из manifest: совпали 60 из 60. Сверены назначения и основные утверждения по README, `plugin_parser.py`, `plugin_formats.py`, `elyx_parser.py`, `bot/services/{submission,plugin_files,validation,versioning,moderation,moderation_stats,publish,poster,backup,audit}.py`, `request_store.py`, `storage.py`, `catalog.py`, `channel_parser.py`, `subscription_store.py`, `userbot/client.py`, а также релевантным call sites в `bot/routers/{user_flow,admin_flow,catalog_flow,moderation_flow,poster_flow}.py` и `main.py`. Это проверка feature-relevant кода, не построчный аудит всех изображений и локализованных сообщений.

Идентифицирован исторический [commit `31ecf63280d4ca6ef3b450eabb7b729187056937`](https://github.com/itsv1eds/exteraPluginsRobot/commit/31ecf63280d4ca6ef3b450eabb7b729187056937): GitHub API возвращает дату 2026-09-10, сообщение `[fix] buttons, submissions and poster` и 17 изменённых файлов. Он не использован как доказательство API pinned snapshot. Второй radar-текст сообщает о крупном commit 14 сентября, но не содержит SHA или permalink, поэтому тот исторический эпизод отдельно проверить невозможно.

## Проблемы и исправления

- Добавлено покрытие quiz gate перед подачей обычного plugin: три вопроса за прогон, неверный ответ запускает quiz заново. Это submit workflow, а не валидатор формата.
- Уточнена роль iconpacks: README на проверяемом SHA говорит, что iconpacks доступны в каталоге; allowlist `plugin_formats.py` принимает `.plugin` и Elyx, но не `.icons`. Код содержит отдельную внутреннюю функцию `publish_icon` через userbot. Radar-фразу о публичном приёме `.icons` нельзя подтвердить этим снимком, поэтому она не перенесена как факт.
- Добавлено покрытие подписок на конкретный plugin и общего ключа `all`, а также best-effort DM fan-out при обновлении. Ошибки Telegram отправки подавляются, так что статический код не доказывает доставку.
- Добавлена отсутствовавшая недельная статистика модерации: уникальные проверенные plugin requests, yes/no, решения, навигация по неделям и подробности модератора; отчёт исключает icon submissions, а экран доступен super-admin.
- Отделён общий poster scheduler (время, повтор, автоудаление и публикация сейчас) от публикации/планирования plugin-заявок.
- В `plugins-robot-facts.json` факт `plugins-robot-034` повторял ограничение audit history, уже записанное в `plugins-robot-022`; удалён повтор. Добавлены факты `037`–`042`; README claim об iconpacks (`040`, статус `docs`) отделён от внутренней кодовой публикации (`042`, статус `code`). Остальные ID уникальны.
- Сигнатуры и внутренние bot-контракты не выданы за API ExteraGram/Android SDK. README-тезисы помечены `docs`; статическое чтение не объявлено runtime-проверкой. Указанный commit сентября подтверждён только как историческая метаинформация, а текущие утверждения закреплены за pinned SHA.

Покрытие радара и снимка соответствует инфраструктурной границе этого источника: intake и metadata parsing, форматные ограничения, duplicate/blocklist/version policy, draft/request lifecycle, moderation/votes/appeals, publication/update, catalog/search/channel-history, subscription notification, SQLite/cache/backup/audit, poster и запуск фоновых workers. Отдельные огромные локализованные ветки Joinly, broadcast и полный UX аудита не пересказывались как Android developer API.

## Дубликаты и происхождение

В исходном наборе было 36 записей с уникальными ID; семантический повтор `022`/`034` устранён, затем добавлены пять фактов. Итог: **41 факт, 41 уникальный ID**. Повторяемые знания с другими источниками остаются отдельными подтверждениями; кандидаты на позднюю канонизацию: `plugin metadata intake/format validation`, `submission and moderation lifecycle`, `catalog publication/subscriptions`, `Telegram channel publishing`, `SQLite persistence/audit`.

## Остаточные пробелы

- Бот, парсеры, Telegram Bot API, Telethon, планировщики, восстановление backup и миграция не запускались. Нет runtime-подтверждения фактической доставки, forum permissions, поведения при rate limit или доступности аккаунтов.
- Злонамеренные Elyx архивы, граничные parser cases и восстановление после аварии не испытывались. Кодовые ограничения нельзя считать security certification или sandbox.
- Commit от 14 сентября не идентифицируется по первичному SHA/permalink в сохранённом radar context.
- Рецензия охватывает релевантные workflow и интеграционные точки. Полный анализ Joinly, broadcast и всех локализованных UI-состояний выходит за границу source page; покрытие не претендует на исчерпывающий аудит всего Telegram-бота.
- README содержит заявления о live bot, установке и Python 3.12; они остаются documentation claims. Наличие или точность автоматических тестов не проверялись запуском; в pinned tree отдельной test suite и CI workflow не найдено.

## Вердикт

**accepted-with-gaps** — независимая сверка поддерживает описанные versioned инфраструктурные факты и их API relevance; выявленные пропуски добавлены, повтор удалён, provenance проверен. Материал не подтверждает runtime поведение бота, клиентскую совместимость plugin или полноту за пределами указанного scope.
