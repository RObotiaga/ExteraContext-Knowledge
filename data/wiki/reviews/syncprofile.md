# Независимая проверка: SyncProfile

- Вердикт: **accepted-with-gaps**.
- Область: `Kukuryzen666/SyncProfile`, snapshot `addbd38ff37965be31d2e9e2845793539bfd60ce`, captured `2026-09-27T15:49:19Z`; pinned identity сверена по `snapshot.json` и `tree.json` (дерево не усечено). Контрольные суммы всех 12 полученных релевантных файлов совпали с `file-manifest.json`.
- Итоговый machine layer: **42 уникальных факта**, ID `syncprofile-001`…`syncprofile-042`; количество, непрерывность ID и отсутствие повторяющихся строк `claim` проверены в `work/syncprofile-facts.json`.
- Это независимая статическая проверка исходного snapshot. Код не исполнялся; сборка, тесты и установка не выполнялись.

## Независимое покрытие

По `tree.json` сверены назначение из `raw/syncprofile/radar-context.md`, пустой `radar-urls.json`, source page, facts JSON и состав snapshot. Полученные файлы: `README.md`, два `.agents/rules`, два GitHub workflow, `BUGS_AND_ARCHITECTURE_GUIDELINES.md`, `CHANGELOG.md`, `build_plugins.py`, обе версии `.plugin`, `tests/test_sync_profile.py`, `zwylib.plugin`. В дереве также есть `.gitignore`; он отсутствует в manifest локального файла, но не задаёт API, lifecycle или интеграционное поведение.

Независимо сопоставлены основные относящиеся к разработке поверхности обеих больших реализаций: metadata и slot schema; local Premium/import; active-account discovery; полная/delta синхронизация, публикация и HTTP retry; cache/snapshots/persistence; outbound/inbound custom-emoji преобразования; SDK request/update hooks; reflection hooks для `MessagesController`, profile lifecycle и message cells; UI menu/settings; build/release workflow и mock-test границы. Релевантные детали сверены непосредственно в сохранённых методах и вызовах. Архитектурные документы и thread-safety/TL правила рассматриваются как авторские `docs`, а не независимая гарантия клиента. Для changelog отдельно просмотрены текущая версия и headings истории, не весь исторический текст. Тесты не перечитывались полностью и не запускались.

Идентичность плагинов `sync_profile_exteragram` и `sync_profile_ayugram`, версия `10.3.27` и заявленные минимумы `>=12.5.1`/`>=1.4.3.3` совпадают с pinned files. Метаданные являются заявлением конкретного snapshot и не подтверждают совместимость с более поздними SDK или релизами клиента.

## Найденное и исправленное

- `syncprofile-023` преувеличивал фактический эффект keep-alive backoff. Loop вычисляет `min(base_interval * 2**_consecutive_errors, 900)`, но sync вариант обнуляет счётчик сразу после запуска отдельного thread. Async-вариант ожидает `_sync_delta_worker`, который ловит исключения внутри и возвращает; HTTP/status failures также не пробрасываются в loop. Исправлены факт и source page: код вычисляет backoff, но сетевые ошибки обычно не накапливаются для его применения. HTTP retry внутри `_api_request` остаётся отдельным механизмом.
- `syncprofile-026` описывал несуществующий безусловный fallback из `JsonCacheFile` в disk/setting. Writer при наличии cachefile пишет и возвращается; исключение уходит во внешний обработчик, не включая следующий backend. Текст facts и страницы теперь различает ветку cachefile и fallback при disk write failure; loader отдельно пробует следующие источники при пустом/ошибочном результате.
- `syncprofile-027` утверждал, что сброс сохраняет локальные профили активных аккаунтов. По фактическому порядку вызовов force-save пустых maps происходит до seed локальных профилей. Seed остаётся в памяти до результата повторной полной загрузки и явно не сохраняется в этой ветке. Исправлены claim, recipe и описание ограничения.
- `syncprofile-034` и source page приписывали радару период «каждые 30 секунд», которого я не нашёл в полном сохранённом `radar-context.md`; там указана delta sync без числа. Исправлен claim на отсутствие точного периода в captured radar и статус на `inference`; конкретные интервалы остаются подтверждёнными кодом.
- Добавлены `syncprofile-039`…`syncprofile-042`: выставление photo `has_video`/flag для user/chat TL objects (не доказательство playback); применение локальных настроек и условный delta-sync на `START`/`RESUME`; зарегистрированное действие копирования Emoji ID с несколькими источниками извлечения; различие между определёнными и реально подключёнными menu callbacks.
- В source page добавлена оговорка, что обработчики refresh одного профиля и показа деталей определены, но текущий `_register_menu_items()` не регистрирует их. Активное действие — копирование Emoji Document ID. Это предотвращает трактовку неиспользуемых методов как доступного UI.

## Дубликаты и канонизация

Повторяющихся точных claims внутри итоговых 42 записей нет; ID уникальны. Общая запись о расхождении редакций и отдельная запись о конкретном AyuGram outbound hook — разные уровни детализации. Fact про интервал и отдельная запись, сравнивающая его с радаром, также сохраняют разные provenance. Пересекающиеся знания про `async_manager` и `JsonCacheFile` уместно объединять позже по темам `async`/`storage`, сохраняя SyncProfile как отдельный кодовый provenance; совместимость его встроенного/поставляемого `zwylib.plugin` с документацией ZwyLib этим не доказывается.

## Остаточные gaps

- Контракт сервера `sync.efn.mom`, смысл timestamp и `If-Modified-Since`, schema/auth/rate limits и фактические ответы API остаются неустановленными. Серверный код находится вне этого snapshot; страница правильно трактует endpoint calls как код клиента.
- Не исследованы runtime/устройство, реальная совместимость Java overloads и TL flags с конкретными сборками AyuGram/exteraGram, доступность video media и custom-emoji отображение. Заявления README и changelog о playback, 120 FPS и «live sync» остаются docs/self-report.
- Встроенный `zwylib.plugin` поставлен в snapshot, но проверены только связанные точки использования, а не все его 149 KB API. Не выполнялся полный аудит поведения библиотеки.
- Прочитана структура тестов и выбранные релевантные области, но весь большой test file не проходился строка за строкой; результаты CI этого SHA не проверялись.
- Исторический changelog просмотрен по текущим release notes и перечню разделов, не полностью. Он не считается самостоятельной спецификацией актуального API.
- Исторический радар содержит ссылки без заполненных repo URL, а `radar-urls.json` пуст. Сам repo и SHA подтверждены снимком GitHub tree/snapshot, поэтому это не мешает идентификации источника, но provenance радарной находки неполон.
- В `tree.json` нет `LICENSE`; это не устанавливает лицензию или разрешённость повторного использования кода.

Эти ограничения оставлены явными; абсолютная полнота по runtime, backend и всему встроенному ZwyLib не заявляется.
