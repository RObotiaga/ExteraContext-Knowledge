# Независимая проверка: SyncProfile-Selfhosted

- Вердикт: **accepted-with-gaps**.
- Область: `Kukuryzen666/SyncProfile-Selfhosted`, ветка `main`, SHA `2ae2d881405b2b903368f10caf3a5315c8f1ab02`, captured `2026-09-27T15:49:33.573768Z`. SHA снимка и дерева совпадают; pinned GitHub recursive tree независимо вернул 12 записей без truncation. SHA-256 и размер каждого из 7 полученных файлов совпали с `file-manifest.json`; `.gitignore` есть в полном дереве, но не был получен, так как не влияет на рассматриваемый API/lifecycle contract.
- Итоговый набор: **31 уникальный факт**, ID `syncprofile-server-001`…`syncprofile-server-031`. JSON прочитан независимо, число фактов, непрерывность и уникальность ID проверены; точных повторов claim нет.
- Это независимая статическая проверка pinned snapshot. Код не запускался; сборка, тесты, установка и HTTP-вызовы не выполнялись.

## Независимое покрытие

Сверены `snapshot.json`, полный `tree.json`, `file-manifest.json`, `repository.json`, `radar-context.md`, `radar-urls.json`, source page и `work/syncprofile-server-facts.json`. Радар связывает этот репозиторий с self-hosted сервером, ExteraGram Plugin SDK/ZwyLib, AyuGram/ExteraGram и delta sync. `radar-urls.json` пуст, поэтому прямой URL-путь радара не подтверждён; snapshot и GitHub API tree подтверждают идентичность репозитория и pinned SHA.

Изучены целиком README, thread-safety rule и оба workflow. По `sync.plugin` сопоставлены metadata; slot settings/profile payload; локальный Premium import; полный и delta HTTP пути; single/multi-account публикация; cache load/save/snapshot; user/chat/full TL patch paths; MessagesController и MessageObject hook registration; profile/message menu handlers; Settings callbacks и clear-cache flow. Для `CHANGELOG.md` сверены записи v10.2.34 и связанные с кэшированием разделы, но не весь исторический файл. `zwylib.plugin` не проходился построчно: проверены только imports/call-sites, нужные SyncProfile (`JsonCacheFile` и `async_manager`). Кодовые paths, не просмотренные построчно, не представлены как полная оценка каждой обработки Telegram-объекта.

Repo metadata и README описывают серверную часть и поддержку двух клиентов, но pinned tree содержит только `sync.plugin`, `zwylib.plugin`, README, changelog, agent rule и два workflow плюс `.gitignore`. В нём нет backend, API/schema specification, deployment files или tests. Поэтому endpoints ниже — контрактные ожидания клиентского кода, а не доказательство server behavior. README claims о реальном времени и двух платформах сохраняют статус `docs`.

## Найденное и исправленное

- Выявлен дефект delta snapshot: `_update_snapshot_partial()` вызывает `self._patch_cache.pop(...)`, однако поле не создаётся нигде в `sync.plugin`; changelog v10.2.34 сообщает об удалении patch cache. При непустом ответе worker уже меняет `_profiles_cache`, затем падает до публикации snapshot, записи timestamp и локального сохранения. Это статическое следствие control flow; runtime-эффект не проверялся. Исправлены facts `syncprofile-server-014` и source page.
- Исправлено обобщение о thread handling. Startup sync и delta worker вызываются из фонового/executor пути, но Settings callback полного скачивания напрямую вызывает `_sync_database()`, где синхронно выполняется `urlopen(timeout=8)`. Прямой blocking call подтверждается source code; что callback фактически исполняется на UI thread, без клиентского runtime оставлено как непроверенное следствие обычной модели UI callback.
- Уточнён clear-cache flow: action удаляет `profiles`, оставляя `chats` и `_last_sync_timestamp`, а затем асинхронно повторно помещает локальные аккаунты в память. При старте пустой профильный cache выбирает полный запрос с `force_clean=False`; ненулевой timestamp включает `If-Modified-Since`, и условный `304` может оставить остальные записи не загруженными. Явная кнопка полного скачивания использует `force_clean=True`.
- Добавлено отсутствие `auth_key` field в Settings UI: payload читает `get_setting("auth_key", "")`, но `create_settings()` не объявляет control для этого значения. Указано только, что штатный UI-ввод не найден; возможную внешнюю настройку хостом код не исключает.
- Уточнена граница chat данных: локальные `chats` сохраняются/загружаются и могут применяться к TL chat objects, но сетевые handlers этого bundle их не заполняют. Cache structure не используется как доказательство chat HTTP schema.
- Добавлена локальная presentation интеграция reply colors через `MessageObject.getReplyColorId()` / `getReplyColor()`. Она остаётся отдельной от HTTP contract.

## Дубликаты и канонизация

Повторных claims внутри 31 source facts нет. Пересечения с `syncprofile` ожидаемы, поскольку это разные репозитории и ревизии: profile field names, default cookie/config guard, self-hosted reference, cache concepts и multi-account usage сохраняют отдельный provenance. В частности, этот SHA — один AyuGram-labelled `sync_profile` plugin v10.2.34 с mapping-style delta handling и дефектным partial update; соседний `SyncProfile` SHA — две редакции v10.3.27 с иным helper, retry/cache lifecycle и account behavior. Их нельзя сливать как один контракт. Позднее тематическое объединение допустимо для тем HTTP sync, account slots, storage и hooks при явном сохранении версии и разницы wire shapes.

## Остаточные gaps

- Серверные маршруты, схема и валидация профиля, auth/cookie правила и ротация, timestamp units/ordering, deletion semantics, конфликт записей, ограничения запросов, deployment и безопасность self-hosted инсталляции не устанавливаются этим snapshot.
- Ни live endpoint, ни один клиент runtime/device сценарий не проверен; README/changelog self-reports не подтверждают работу HTTP API, TL flags, hooks или video-avatar/custom-emoji rendering.
- `zwylib.plugin` проверен лишь на границе использования этим плагином; его полный API/совместимость не оценивались. Полный исторический changelog и все ветви Telegram object processing также не проходились строка за строкой.
- Полное дерево содержит `.gitignore`, который acquisition не сохранил. Для выводов об API и backend это несущественно; источник не содержит LICENSE.

Эти пробелы ограничивают вывод клиентской реализацией pinned SHA; полнота или корректность отсутствующего сервера не заявляется.
