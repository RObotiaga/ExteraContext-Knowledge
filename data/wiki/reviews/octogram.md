# Независимое ревью OctoGram

## Объём и идентификация

- Источник: [`OctoGramApp/OctoGram`](https://github.com/OctoGramApp/OctoGram), закреплённый commit `895d766d7277dbf23638be4844295ea0fe56558e` (`main`, snapshot от 2026-09-27).
- Проверены `raw/octogram/tree.json`, `snapshot.json`, `repository.json`, `radar-context.md`, `radar-urls.json`, `file-manifest.json`, source page и все 15 записей `work/octogram-facts.json`.
- В tree snapshot 33 287 записей (31 827 blob), без усечения; в собственном `it.octogram` namespace — 232 Java/Kotlin-файла. Radar содержит только вторичные наблюдения об отсутствии заметных новых функций/коммитов; `radar-urls.json` пуст.
- Манифест файлов содержит 27 путей: 26 файлов доступны в начальном наборе, а `TMessagesProj/src/main/java/org/telegram/messenger/ConnectionsManager.java` отсутствует после 404. Манифестируемый набор содержит 12 файлов собственного namespace, 12 core/build файлов и 2 документа. Текущий raw-каталог также содержит более широкую выборку; она не проходила полный построчный аудит в этом ревью.

Подробно сверены объявления и фактические вызовы в `ConfigProperty.kt`, `OctoConfig.java`, `OctoPreferences.java`, `PreferencesFragment.java`, `DeepLinkManager.java`, `StandardHTTPRequest.java`, `OctoLogging.java`; связанные core call-sites в `DrawerLayoutAdapter.java`, `ChatActivity.java`, `ChatActivityEnterView.java`; а также build metadata, `settings.gradle`, README и LICENSE. Проверка не является сборкой, запуском клиента или runtime-тестом.

## Результат по фактам

Все 15 ID уникальны и приняты после уточнений. Сигнатуры, вызываемые методы, SHA, evidence paths и line ranges сверены с сохранённым исходником и совпадают с указанным commit. Статусы доказательств применены правильно: 13 фактов `code`, один `docs` (README-инструкции) и один ограниченный `inference` о типе проекта/отсутствии подтверждённого plugin API. Статуса `runtime-verified` нет.

Исправлено в source page и fact JSON:

- `octogram-002`: неподдержанный тип вызывает `IllegalArgumentException` лишь когда ключ непустой и выполняется проверка типа для записи. При null-ключе значение остаётся в памяти, а проверка типа не запускается; поле обновляется до возможного исключения.
- `octogram-003`: `OctoConfig.loadConfig()` восстанавливает Boolean/String/Integer/Long под блокировкой, но не имеет ветви Float. `ConfigProperty` умеет записывать Float; при этом в просмотренных объявлениях `OctoConfig` Float-property не найден.
- `octogram-009`: добавлена точная ссылка на профильный callback в `DeepLinkManager`, который передаёт навигацию в `AndroidUtilities.runOnUIThread`.
- `octogram-010`: уточнен evidence path для builder defaults и `build()`; установлено, что при заданном теле синхронный I/O начинается уже в `build()`, поэтому на рабочую очередь нужно переносить весь путь создания и выполнения запроса.
- Уточнён подсчёт coverage: tree содержит 232, а не 233 файла собственного namespace. Разделены curated manifest и более широкое содержимое raw-каталога.

Остальные факты проверены без изменения семантики: версии snapshot (`001`), настройки (005), lifecycle и обновление списка (006–007), account/call-site threading (008–009), синхронный HTTP helper (010), debug logging (011), места врезки client UI (012), Gradle-конфигурация (013), README-инструкции (014) и ограниченное архитектурное заключение (015). Конкретные builder/load/request/call-site сигнатуры соответствуют приведённым anchors. В README-утверждениях сохранен статус документации; вывод об отсутствии публичного SDK остаётся inference по просмотренной выборке, а не доказательством по всему дереву.

## Coverage и остаточные gaps

Исходная страница подходит как ограниченная карта внутренних точек интеграции: она охватывает типизированное хранение и миграцию настроек, preference UI и fragment lifecycle, account-aware deep link, синхронный network helper, private-build logging, несколько OctoGram call-sites, build metadata и README build/distribution guidance. Переносимость этих классов в ExteraGram нигде не утверждается.

Остаточные ограничения:

- Детально не исследованы остальные 220 Java/Kotlin-файлов namespace; из них 214 физически присутствуют в текущем raw-каталоге, а 18 отсутствуют там. В частности, выборка не разбирает целиком custom AI/translation, account/fingerprint/locked-chat, updater, camera, experiments и другие UI/component subsystems. Эти темы требуют отдельного целевого прохода, если они станут предметом запроса.
- `.github/workflows`, ресурсы и JNI не проверялись целиком; CI, сборка, тесты и поведение APK не запускались. Сравнение с upstream и commit history не выполнялось.
- Недоступный файл `ConnectionsManager.java` независимо не проверен. Использование `ConnectionsManager.getInstance(currentAccount).sendRequest(...)` подтверждается call-site в `DeepLinkManager.java`, но детали реализации network manager не покрыты.
- Общих одинаковых утверждений среди этих 15 фактов не найдено. Факты о current account, UI dispatcher и HTTP worker thread используют сходную практическую рекомендацию, но относятся к разным вызовам и контрактам. Возможное объединение повторяющихся общих рецептов между разными источниками следует делать на canonical topic-страницах; source-local provenance сохраняется.

## Вердикт

**`accepted-with-gaps` — принято 15 уникальных фактов из 15.** Страница пригодна как evidence-backed выборка для изученных API и integration points. Она не является полной документацией клиента или ExteraGram plugin API и не подтверждает runtime/build-поведение. По непроверенным подсистемам полнота не заявляется.
