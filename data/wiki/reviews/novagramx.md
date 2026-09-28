# Независимое ревью: `ferelking242/novagramx`

**Вердикт:** `accepted-with-gaps`  
**Проверяющий:** `/root/review_novagramx` · **модель:** `gpt-6-luna`  
**Закреплённый SHA:** [`5fc9938a74d2a27a639b6b2a837606886f4b4c13`](https://github.com/ferelking242/novagramx/tree/5fc9938a74d2a27a639b6b2a837606886f4b4c13)  
**Уникальных фактов после проверки:** 29

## Объём и независимое покрытие

Независимо сверены `wiki/sources/novagramx.md`, 27 исходных записей `work/novagramx-facts.json`, `raw/novagramx/tree.json`, `file-manifest.json`, `snapshot.json`, `repository.json`, `radar-context.md` и `radar-urls.json`. Snapshot дерева полный (`tree_truncated: false`, 34 014 записей); manifest содержит 42 захваченных файла, а для двух запрошенных путей старого package location прямо записан HTTP 404. Source-specific radar context и URL list пусты. В сохранённом общем radar export NovagramX отнесён к reference implementation для regex firewall, локального last-seen и privacy hooks; это вторичный context, не доказательство кода и не plugin API.

Перечитаны README и относящиеся к назначенному срезу реализации: `AyuFilter.java`, `NaConfig.kt`, regex editor/settings/lists/popups, `ChatActivity.java`, `ProfileActivity.java`, `MessagesController.java`, `LastSeenHelper.java`, Room entity/DAO/database/migration, `AyuQueues.java`, `GhostModeActivity.java`, `PasscodeHelper.java`, `AyuGhostUtils.java`, `AyuGhostPreferences.java`, `AyuState.java`, `ConnectionsManager.java`, `staging.yml` и `canary.yml`. Для десятков тысяч upstream/Telegram-файлов полного чтения не заявляется; прочитаны точки, относящиеся к radar slice и plugin-integration seams. Дерево/manifest проверялись как инвентарь, не как утверждение, что весь код доступен локально. Никакие приложение, сборка, runtime или тесты не запускались.

## Найденное и исправленное

1. Добавлены два пропущенных машинных факта (ID `novagramx-028` и `novagramx-029`) о центральном сетевом seam Ghost Mode: `ConnectionsManager.sendRequestInternal` вызывает interceptor перед TL serialization, блокирует либо сохраняет/заменяет completion callback; для read-after-send используется storage queue и краткое разрешение в `AyuState`. Это полезнее для integration analysis, чем сводить описание к UI-переключателям.
2. Зафиксировано конкретное условие offline-after-send: `handleOfflineAfterSend` проверяет `ghostModeTypingExclusion` и пропускает обёртку callback при включённом typing exclusion. Это наблюдаемое поведение; источник не объясняет его замысел, поэтому страница не называет его подтверждённым багом.
3. Уточнён импорт regex: edit UI сообщает ошибку синтаксиса, но import path сливает входящие `FilterModel` и сохраняет список; runtime `buildPattern()` в случае ошибки ставит `pattern = null` и пишет в `FileLog`. `novagramx-027` дополнен прямым evidence на importer, поэтому его предупреждение о внешних/импортированных правилах не осталось выводом только из UI и компилятора.
4. Исправлен `novagramx-020`: отрицательный поиск ограничен `UserCell` и `ProfileActivity`, это не недоступность источника. Статус сменён с `unavailable` на `inference`, в claim/path явно отражена ограниченность проверенных UI-файлов.
5. Уточнена qualified-сигнатура regex `GroupedMessages` как `MessageObject.GroupedMessages`; добавлены `AyuGhostUtils`, `AyuState` и `ConnectionsManager` в coverage/API inventory. Страница помечает README-утверждения о LLM, voice transcription, UnifiedPush, локальной anti-revoke/edit history и иконках как непроверенные реализации вне назначенного radar-среза.

## Claims, signatures и provenance

Все fact IDs уникальны (`novagramx-001`…`029`), claim-тексты не повторяются дословно. У всех машинных фактов один и тот же version SHA, доказательство ведёт на файл конкретного snapshot; проверены также основные классы/сигнатуры и номера строк в захваченных файлах. README-функции сохранены как документационные заявления, workflow — как статическая конфигурация, а выводы по отсутствующим call sites и предполагаемому смыслу поведения помечены `inference`. Ни один source inspection не назван runtime-проверкой.

Внутри источника сгруппированы, но не смешаны: regex decisions/config/edit/import/cache; отдельные peer blocklists; last-seen persistence versus data collection; Ghost UI locks versus network interception; read-after-send versus offline-after-send. Общие темы с NagramX/Nekogram/AyuGram должны позднее объединяться с несколькими provenance; форки нельзя сводить к единому контракту. Историю upstream diff/происхождения реализации не проверяли, потому что исторические commit URLs для этого источника в radar metadata отсутствуют.

## Остаточные gaps

- Подтверждён только срез radar: regex firewall, локальный last-seen, Ghost Mode/network hooks. README-only темы LLM, голосовая транскрипция, UnifiedPush, message deletion/edit history и Solar Icons не исследовались в реализации; соответствующих файлов нет среди 42 захваченных manifest entries. Это не утверждение об отсутствии их в полном репозитории.
- Не установлено, где `LastSeenHelper.getFormattedLastSeenOrDefault` подключён к реальному экрану: просмотрены только helper и два указанных UI-файла, без полного поиска по незахваченному коду.
- Не проверены runtime semantics regex/requests, UI, passcode flow end-to-end, Android multi-account/Doze behavior, сборка/CI и совместимость ExteraGram plugin hooks. `ConnectionsManager`/Java call sites остаются внутренними seams, не документированным API плагина.
- Не проверены upstream diff и исторические feature commits; source-specific radar context/URLs пусты. Снимок доказывает только состояние указанного SHA.

Итог `accepted-with-gaps` означает, что существенные claims назначенного среза согласованы с pinned source и исправлены обнаруженные ошибки/пропуски. Это не гарантия полноты всего клиента или корректности runtime-поведения.
