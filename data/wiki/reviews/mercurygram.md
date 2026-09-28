# Независимое ревью: `Mercurygram/Mercurygram`

**Вердикт:** `accepted-with-gaps`  
**Проверяющий:** `/root/review_mercurygram` · **модель:** `gpt-6-luna`  
**Закреплённый SHA:** [`1c103ff74bad9fe954d099a9fd4d0f45ba2e99c4`](https://github.com/Mercurygram/Mercurygram/tree/1c103ff74bad9fe954d099a9fd4d0f45ba2e99c4)  
**Уникальных фактов после проверки:** 37

## Объём и независимое покрытие

Сверены `wiki/sources/mercurygram.md`, исходные 35 записей `work/mercurygram-facts.json`, закреплённые `tree.json`, `file-manifest.json`, `radar-context.md` и `radar-urls.json`. Snapshot содержит 15 130 записей дерева, не усечён; manifest содержит 36 захваченных файлов и один явно недоступный файл. По снимку повторно сверены README, wire-format документация папок, CONTRIBUTING/versioning, Gradle pin, implementations и call sites для локальных папок/sync, поиска, черновиков, composer counter, pins, watchdog, Unicode fold и Tor companion AIDL. Приложение, сборка и тесты не запускались.

Проверены вызовы и evidence на закреплённом снимке для `MgFolders`/`ConnectionsManager`, `MgFolderSync`/`MessagesController`/`MessagesStorage`, `MgSearchQuery`/`MediaDataController`, `MgAccountConfig` и saveDraft call site, `MgCharCounter`/`ChatActivityEnterView`, `MgPins`, `MgPushWatchdog`/`AppStartReceiver`, `MgUnicodeFold`/`LocaleController`, `MgTorClient` и `IMgTorService.aidl`, а также README и `gradle/mg-version.gradle`. Все 37 fact IDs уникальны; claim-тексты не дублируются; ссылки и line ranges facts ведут в файлы manifest и остаются в пределах длины соответствующих файлов, а каждый URL указывает на один pinned SHA.

## Найденное и исправленное

1. У folder sync было чрезмерно общее описание LWW: более новый blob действительно заменяет синхронизируемый набор, но первый pull сохраняет pre-feature локальные Mercurygram-папки и публикует их объединение с cloud copy. Эта миграционная ветка добавлена в страницу и отдельный факт `mercurygram-035`.
2. Добавлены существенные folder-sync ограничения из комментария/реализации: порядок уже существующих папок сам по себе не синхронизируется; upload после ошибки повторяется только при следующем изменении или запуске. Они выделены в `mercurygram-036`. При cloud apply также сохраняются локальные encrypted-chat entries, которые нельзя представить wire IDs; это добавлено в страницу и `mercurygram-037`.
3. `mercurygram-014` ссылался на Javadoc с описанием даты вместо исполняемого parser/timezone code. Evidence исправлен на `MgSearchQuery.java:113-167`. В описании переноса папки дополнена упущенная миграция storage-key при смене ID; call site и storage sequence находятся в `MgFolders.java:91-120`.
4. Факт `mercurygram-035` у сборщика дублировал формулу Gradle versionCode уже учтённую в `mercurygram-033`, ошибочно относил её к workflow переводов и приписывал рецепту переводов неподтверждённый источник. Повтор устранён: `mercurygram-033` теперь ссылается на фактическое присваивание в `mg-version.gradle:79-82`, а прежний ID `035` использован для отдельного first-sync факта. Число уникальных записей выросло до 37 за счёт трёх неповторяющихся folder-sync ограничений/исключений при устранении одного дубля.
5. В тексте typed search добавлен source-test coverage с ясным указанием, что тесты не запускались. Fact не выдаёт source inspection за runtime test.

Подтверждённое отсутствие `MgCharCounterTest.kt`: путь отсутствует в полном pinned `tree.json`; manifest содержит целевой raw URL с `HTTP Error 404: Not Found`. Поэтому для character counter остаются проверенными только implementation и call site, а отдельный source test в этом snapshot отсутствует.

## Проверка дубликатов и radar

Внутри страницы и fact JSON одинаковые факты объединены либо разграничены по разным поведению и lifecycle: ordinary LWW versus first-sync migration, локальный counter versus отсутствующий test, version-code formula versus release-channel documentation. Совпадения по общим темам с другими клиентами остаются отдельными source attestations; возможные канонические темы — local folder storage/sync, typed search, privacy drafts, local pins, composer UI, push lifecycle, Unicode local search и Android companion IPC/build.

Радар ссылается на исторические feature commits для папок, sync, typed search, drafts, counter и push. Страница явно сообщает, что implementation claims сверены с этим pinned SHA, и что исторические patch commits не считаются доказательством неизменной текущей реализации.

## Остаточные gaps

- Проверен выбранный integration slice, а не весь Mercurygram или Telegram upstream. Непроверенные radar-кандидаты явно перечислены в source page: отключение proximity sensor, полное разрешение после photo crop, tracking cleanup и подтверждение `t.me`/`tg://`, Instant View, пользовательские ringtone URI, video quality variants, optimizations больших аккаунтов, default launch folder/free folder reorder и периферийные Unicode-fold consumers. Radar mentions: [`radar-context.md`](../../raw/mercurygram/radar-context.md#L166), [`radar-context.md`](../../raw/mercurygram/radar-context.md#L231), [`radar-context.md`](../../raw/mercurygram/radar-context.md#L897), [`radar-context.md`](../../raw/mercurygram/radar-context.md#L1007), [`radar-context.md`](../../raw/mercurygram/radar-context.md#L1056), [`radar-context.md`](../../raw/mercurygram/radar-context.md#L1176).
- Unicode Fold проверен на центральном `LocaleController.getTranslitString` seam; все пользовательские search call sites отдельно не прослеживались. Premium behavior folders выводится из ID классов и кода обработки server limits, но реальный backend quota не измерялся.
- Не проверялись Android runtime/Doze/OEM поведение, серверные результаты search, межустройственный sync, отображение/accessibility counter, приложение Tor companion, установка и межпроцессное подписание, Gradle/native build и CI.
- Snapshot статически показывает код и тест-исходники, но не гарантирует эксплуатационное поведение. README claims о версии каналов и сборке остаются помеченными как `docs`.

Итог `accepted-with-gaps` означает, что существенные утверждения выбранной области подкреплены кодом/документацией pinned SHA, исправлены обнаруженные ошибки и явно названы оставшиеся непроверенные участки; это не заключение об абсолютной полноте большого клиента.
