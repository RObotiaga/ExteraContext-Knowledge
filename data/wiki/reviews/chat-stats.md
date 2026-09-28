---
type: review
source_id: chat-stats
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: DedyaSergey/Chat-Stats-Plugin

- Вердикт: **accepted-with-gaps**.
- Проверенный snapshot: `DedyaSergey/Chat-Stats-Plugin`, branch `main`, SHA `d9d096cff9b15000012fd3bf79041213605981cc`, captured `2026-09-27T15:53:22Z`. Сверены `snapshot.json`, полный Git tree и manifest; tree содержит только `README.md` и `chat_stats.plugin`. SHA-256 обоих сохранённых файлов и Git blob SHA совпали с manifest/tree. Идентичность и назначение сверены с `radar-context.md`, пустым `radar-urls.json` и соответствующим участком `raw/radar.md`.
- Проверка статическая. Клиент и плагин не запускались, тесты/сборка/установка не выполнялись; ограничения запроса соблюдены.

## Независимое покрытие

Прочитаны оба файла snapshot целиком. В `chat_stats.plugin` прослежены metadata и `BasePlugin` lifecycle, `on_plugin_load()` → `add_on_send_message_hook()`, все ветки `_chat_id()`, настройки и ограничение истории, периодические подсчёты, форматирование результатов, UI dialog callbacks и send-hook callback. README проверен полностью по функциям, командам, совместимости, установке и приватности. По tree дополнительных исходников, тестов, build-файлов или license-файла нет. Небольшой источник и все его релевантные материалы охвачены; поведения host API, runtime или APK этот snapshot не раскрывает.

## Найденное и исправленное

- Подтверждены `chat_stats`, версия `1.3.3`, declared minimum `12.1.1`, hook call-site, storage key `stats`, запись `{t, c}`, лимит хвоста 5000, команды/`HookStrategy.CANCEL`, UI thread, fallback chat key `unknown` и окно дат. Конкретные method call-sites проверены по закреплённому исходнику; host-сигнатуры не выводились за пределы callback, реально объявленного плагином.
- Проверено использование `account`: аргумент присутствует в `on_send_message_hook(self, account: int, params)`, но внутри метода не читается. Chat key строится только через `_chat_id(params)`, а состояние читается/записывается по plugin setting `stats`. Вывод ограничен схемой самого плагина: области изоляции host settings этот код не устанавливает.
- Проверен общий ключ `unknown`: `_chat_id()` возвращает его после исчерпания `peer`, вложенных peer ID и трёх dialog-полей; затем ключ передаётся в `_add_message()` и используется как map key. Следовательно, все события без распознанного ID для этого settings namespace сводятся в один bucket. Это статическое следствие кода.
- Проверены period reports: `today` начинается от локальной полуночи, `week`/`month` — сравнения с `now - 7/30 days`; верхнего временного предела нет. `_make_text()` подменяет выбранный count, но `chars` и `average = chars / total` берёт по всей сохранённой (максимум 5000) истории. В source page уточнено, что период может показывать нулевой count при ненулевых all-history symbols/average.
- Проверена защита persisted state: верхний уровень settings проверяется как dict, а `messages` как list только в append-path; тип вложенного chat entry и формат записей не проверяются в `_get_counts()`. Поврежденные nested values могут дать исключение при подсчете/рендеринге; save path hook ловит и логирует исключение. Это ограничение добавлено на source page и в факт 016.
- Добавлен `chat-stats-015` о документированных шагах установки из README; до проверки этого пути на клиенте он имеет статус `docs`. В `chat-stats-014` убрано повторное упоминание лимита 5000: это поведение уже покрывает кодовый факт 005, а документация и реализация совпадают. Facts JSON содержит **16 уникальных записей с 16 уникальными ID**; повторяющихся строк claim нет.
- Пересекающиеся общие темы — регистрация send hook, callback параметры, UI-thread dispatch и plugin settings — уже имеют другие source provenance в общей базе. Для канонического синтеза использовать темы `hooks`, `threading`, `ui` и `storage`; сохранять pinned SHA именно этого плагина. Утверждение `unknown` fallback, отсутствие account в собственной ключевой схеме и ошибка смешения периодических чисел специфичны для этого источника.

## Остаточные gaps

- Источник не содержит тестов, документации host API или клиентского кода. Не подтверждены порядок вызова send hook относительно отправки, доставка/успех отправки, plugin settings scope между аккаунтами, типы и наличие полей `params`, сериализация settings и compatibility с конкретными APK.
- Не проверены установка, UI, фактическая локальность/резервное копирование данных, account isolation, поведение при malformed stored rows, DST/timezone transitions или обработка сообщений в реальном клиенте. README privacy/compatibility/installation assertions остаются `docs`; исходник без сетевых вызовов не является runtime security audit.
- В radar URL capture нет исторических commit permalinks; проверен только доступный репозиторий и зафиксированный SHA. GitHub metadata snapshot сообщает `license: null`; в полном двухфайловом tree отдельной лицензии нет.

Эти ограничения оставлены явными, поэтому вердикт — **accepted-with-gaps**; абсолютная полнота или runtime-работоспособность не заявляются.
