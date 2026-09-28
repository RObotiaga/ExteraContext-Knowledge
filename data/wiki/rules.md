# Канонические правила разработки

Это синтез по исследованным источникам. Повторные подтверждения одного правила собраны под одним идентификатором; исходные наблюдения остаются в facts для происхождения. Рекомендации не означают проведенного испытания в клиенте.

## У регистрации должен быть владелец и путь снятия

Канонический ID: `resource-owner`.

Сохраняйте handles сразу после регистрации. При выгрузке снимайте hooks, observers и menu callbacks; освобождение только через atexit не заменяет plugin unload. Частичную ошибку загрузки обрабатывайте тем же механизмом очистки.

Подтверждения и ограничения: [official-sdk:lifecycle](sources/official-sdk.md); [for-vibecoders:fvb-003](sources/for-vibecoders.md); [for-vibecoders:fvb-028](sources/for-vibecoders.md); [altylib:altylib-025](sources/altylib.md); [altylib:altylib-041](sources/altylib.md). [Тема](topics/lifecycle.md), [рецепты](recipes/index.md).

## Переопределение callback и подписка — два действия

Канонический ID: `hook-subscription`.

В SDK наличие callback метода не регистрирует перехват. Укажите имена событий через add_hook и отдельную подписку outgoing-send; для Java hook проверьте точный Member и сохраняемый Unhook.

Подтверждения и ограничения: [official-sdk:hook-registration](sources/official-sdk.md); [official-sdk:xposed-hooks](sources/official-sdk.md); [for-vibecoders:fvb-003](sources/for-vibecoders.md). [Тема](topics/hooks.md), [рецепты](recipes/index.md).

## Сохраняйте аккаунт события до конца операции

Канонический ID: `event-account`.

Учитывайте account callback даже при другом выбранном аккаунте UI. Захватите его до постановки работы в очередь и используйте в запросе и ключе кеша. Helper без account может обращаться к выбранному сейчас аккаунту.

Подтверждения и ограничения: [official-sdk:account-scope](sources/official-sdk.md); [official-sdk:account-client](sources/official-sdk.md); [official-sdk:notification-account](sources/official-sdk.md); [extcli:extcli-013](sources/extcli.md). [Тема](topics/accounts.md), [рецепты](recipes/index.md).

## Передавайте изменения интерфейса в UI thread

Канонический ID: `ui-boundary`.

Сеть, разбор и файловый ввод-вывод выполняйте в фоновой очереди; результат применяйте через UI dispatcher. Timer debounce/throttle сам по себе не дает UI context. При возврате результата сверяйте актуальность lifecycle и account.

Подтверждения и ограничения: [official-sdk:queue-api](sources/official-sdk.md); [official-sdk:ui-thread](sources/official-sdk.md); [altylib:altylib-035](sources/altylib.md). [Тема](topics/threading.md), [рецепты](recipes/index.md).

## Метаданные должны соответствовать статическому парсеру

Канонический ID: `literal-metadata`.

Держите необходимые metadata литералами верхнего уровня. Загрузчик и validator выбранного формата определяют правила ID: ограничения single-file и Elyx могут расходиться, даже если оба создают BasePlugin.

Подтверждения и ограничения: [official-sdk:metadata-ast](sources/official-sdk.md); [official-sdk:plugin-id-single](sources/official-sdk.md); [official-sdk:elyx-troubleshooting](sources/official-sdk.md). [Тема](topics/build.md), [рецепты](recipes/index.md).

## Сверяйте импорты с упаковщиком и загрузчиком

Канонический ID: `import-contract`.

Entry, относительные imports, динамические имена, assets и зависимые wheels проверяйте в конечном формате. Не переносите правила Elyx module isolation на bundler в один Python-файл без изучения его bootstrap.

Подтверждения и ограничения: [official-sdk:elyx-entry](sources/official-sdk.md); [official-sdk:elyx-imports](sources/official-sdk.md); [official-sdk:elyx-public-api](sources/official-sdk.md); [official-sdk:elyx-archive](sources/official-sdk.md). [Тема](topics/build.md), [рецепты](recipes/index.md).

## Объявленная зависимость еще не означает возможность установки

Канонический ID: `wheel-platform`.

Документированный package manager поддерживает pure-Python universal wheels. Native extensions и desktop-specific wheels требуют другого пути, даже если import имя известно. Предустановленная библиотека и __requirements__ — разные источники доступности.

Подтверждения и ограничения: [official-sdk:elyx-requirements](sources/official-sdk.md); [official-sdk:preinstalled-libs](sources/official-sdk.md); [for-vibecoders:fvb-029](sources/for-vibecoders.md). [Тема](topics/build.md), [рецепты](recipes/index.md).

## Разделяйте классы хоста и packaged program input

Канонический ID: `dex-classpath`.

Для JVM-плагина compile classpath может включать извлеченный JAR хоста, но это не означает включение всех его классов в DEX. Проверяйте фильтрацию, relocation и R8 keep rules по фактическому конвейеру.

Подтверждения и ограничения: [gradle-plugin:gradle-plugin-008](sources/gradle-plugin.md); [gradle-plugin:gradle-plugin-009](sources/gradle-plugin.md); [gradle-plugin:gradle-plugin-011](sources/gradle-plugin.md); [gradle-plugin:gradle-plugin-012](sources/gradle-plugin.md); [extcli:extcli-025](sources/extcli.md). [Тема](topics/build.md), [рецепты](recipes/index.md).

## Reload обязан учитывать состояние старой загрузки

Канонический ID: `reload-state`.

Снятие hooks и остановка фоновых задач должны предшествовать новой регистрации. Сам вызов unload/load не доказывает, что старые Java listeners, threads или глобальные registry очищены.

Подтверждения и ограничения: [extcli:extcli-009](sources/extcli.md); [for-vibecoders:fvb-028](sources/for-vibecoders.md); [altylib:altylib-025](sources/altylib.md); [official-sdk:elyx-troubleshooting](sources/official-sdk.md). [Тема](topics/lifecycle.md), [рецепты](recipes/index.md).

## Называйте точную политику кеша

Канонический ID: `ttl-contract`.

У AltyLib TTL фиксирован после записи и не продлевается чтением; expiry/FIFO eviction не является LRU. TTL=0 в этом снимке превращается в бессрочную запись. Эти свойства нельзя заменять обещанием generic TTL cache.

Подтверждения и ограничения: [altylib:altylib-004](sources/altylib.md); [altylib:altylib-005](sources/altylib.md); [altylib:altylib-006](sources/altylib.md); [altylib:altylib-060](sources/altylib.md). [Тема](topics/storage.md), [рецепты](recipes/index.md).

## Потоковый вывод требует политики обрезки и редактирования

Канонический ID: `stream-tail`.

У extCLI relay хранит хвост текста до4096символов и редактирует сообщение по интервалу. Это конкретная политика реализации; она не дает общего гарантированного лимита UTF-16 для любого Telegram send/edit API.

Подтверждения и ограничения: [extcli:extcli-021](sources/extcli.md); [official-sdk:send-request](sources/official-sdk.md). [Тема](topics/requests.md), [рецепты](recipes/index.md).

## Разделяйте сборку, передачу и установку

Канонический ID: `watch-install`.

Watch может только пересобирать архив. Планируйте отдельную стадию доставки, установку/reload и чтение результата загрузчика, иначе успех файловой сборки не доказывает обновление плагина на устройстве.

Подтверждения и ограничения: [official-sdk:elyxbuilder-cli](sources/official-sdk.md); [extcli:extcli-009](sources/extcli.md). [Тема](topics/debug.md), [рецепты](recipes/index.md).

## При конфликте документации и кода сохраняйте обе версии

Канонический ID: `docs-source-drift`.

Для поведения конкретного снимка указывайте найденную реализацию и SHA. Заявление README оставляйте docs с пояснением расхождения. Например @CacheableTask и рассказ про одни up-to-date checks требуют отдельного consumer build, если нужна гарантия фактического кеширования.

Подтверждения и ограничения: [gradle-plugin:gradle-plugin-039](sources/gradle-plugin.md); [altylib:altylib-060](sources/altylib.md). [Тема](topics/testing.md), [рецепты](recipes/index.md).

## Проверяйте происхождение и экспорт помощника

Канонический ID: `api-export`.

Импортированная функция не становится собственным API библиотеки. Отмечайте исходный модуль, public exports и re-export behavior; send_request в AltyLib приходит из client_utils и не перечислен в __all__.

Подтверждения и ограничения: [altylib:altylib-031](sources/altylib.md); [official-sdk:send-request](sources/official-sdk.md). [Тема](topics/requests.md), [рецепты](recipes/index.md).

## Замена Java-метода должна вернуть совместимый тип

Канонический ID: `replacement-type`.

Сверяйте return type выбранной Java сигнатуры. Для изменений thisObject/args/result и короткоживущего replacement сохраняйте handle и снимайте его в finally даже при ошибке основной операции.

Подтверждения и ограничения: [official-sdk:xposed-param](sources/official-sdk.md); [for-vibecoders:fvb-019](sources/for-vibecoders.md). [Тема](topics/hooks.md), [рецепты](recipes/index.md).

[Индекс](index.md) · [Сущности](entities/index.md) · [Противоречия и пробелы](gaps.md)
