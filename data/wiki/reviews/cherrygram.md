---
type: source-review
source_id: cherrygram
reviewer: /root/review_cherrygram
model: gpt-6-luna
verdict: accepted-with-gaps
reviewed_at: 2026-09-28
accepted_facts: 14
---

# Независимая проверка arsLan4k1390/Cherrygram

## Область и закреплённая версия

Проверен `arsLan4k1390/Cherrygram`, ветка `main`, commit [`cec3075847d933e13014954ed8b776b767760ce8`](https://github.com/arsLan4k1390/Cherrygram/commit/cec3075847d933e13014954ed8b776b767760ce8). `repository.json`, `snapshot.json`, `tree.json` и manifest указывают на этот же репозиторий и SHA; дерево полное, 30 032 entries. В `radar-urls.json` пустой список. Использованные выдержки из предоставленного радара находятся в [`raw/radar.md`](../../raw/radar.md#L162); в `raw/cherrygram/radar-context.md` сохранены их номера исходных строк.

Это большой Android Telegram fork, а не plugin SDK. Rадар не выделяет отдельную свежую Cherrygram-функцию для переноса: он описывает крупную синхронизацию с upstream до Telegram 12.10.1. Поэтому проверены именно границы, полезные для plugin-разработки: прямые compile-time call-sites, собственные menu/preferences helpers, один сетевой пример, сведения README о сборке и Gradle-модульная граница. Это не полный feature review всего клиента.

## Независимое покрытие

Сверены документы и первичные файлы из снимка:

- `README.md`, `LICENSE` — формулировка о third-party/unofficial Android fork, GPL v2-or-later, README build-инструкция и оговорка, что она уводит на ветку `main_Reproducible_Builds` и требует submodules/локальных signing/Firebase/Extra.kt данных.
- `settings.gradle`, корневой `build.gradle`, `gradle.properties`, `TMessagesProj/build.gradle`, `TMessagesProj_App/build.gradle`, `TMessagesProj_AppHuawei/build.gradle`, `TMessagesProj_AppStandalone/build.gradle` — modules, SDK/NDK/JVM versions и выбранные зависимости на этом SHA.
- `TMessagesProj/src/main/java/uz/unnarsx/cherrygram/core/CGFeatureHooks.kt`, `.../chats/CGChatMenuInjector.kt`, `.../chats/CGMessageMenuInjector.kt`, `.../preferences/CherrygramPreferencesNavigator.kt` — internal helpers и их compile-time природа.
- `TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java` вместе с `.../Components/ChatActivityEnterView.java`, `.../Cells/ChatMessageCell.java`, `.../messenger/SendMessagesHelper.java`, `.../messenger/MessageObject.java` — выбранные host call-site для меню и message behavior; полный upstream diff не анализировался.
- `.../chats/gemini/network/ApiClient.java`, `ApiCallback.java` и добавленный в manifest `.../preferences/GeminiPreferencesEntry.java` — network worker, callback delivery/error path и реальный caller.

`file-manifest.json` содержит 22 записи: SHA-256 сверены для всех 21 сохранённых файлов; единственная acquisition-error запись — первоначальный неверный `ApiClient.kt` путь с 404, после чего корректные `ApiClient.java` и `ApiCallback.java` получены. Во время review дополнительно захвачен `GeminiPreferencesEntry.java` тем же pinned SHA, чтобы подтвердить caller. Ни source code, ни приложение, ни build/test команды не запускались.

## Найденные проблемы и исправления

- `cherrygram-013` ссылался на незакреплённый URL корня GitHub и выдавал номера исходных строк радара за строки `radar-context.md`. В выдержке line numbers исходника — текстовые префиксы: реальные локальные строки excerpt 10, 35, 60 соответствуют исходным `raw/radar.md` 162, 256, 405. Исправлены `evidence_url`/`evidence_path`, и source page теперь даёт локальные ссылки на обе выдержки.
- Описание tree scan смешивало пути с `plugin` и собственный hook helper. В полном tree нашлось 11 путей с подстрокой `plugin`: 9 vendored protobuf compiler paths и два Gradle build plugins. `CGFeatureHooks.kt` отдельно имеет `hook` в имени, но это helper в исходнике, а не plugin runtime. Source page теперь описывает именно ограниченный path scan и не заявляет текстовый аудит всего кода.
- Сетевой summary расширен по фактическому caller. `fetchModels` передаёт `onResult` в worker thread и в случае не-200/исключения вызывает callback с пустым списком без error-typed результата; `GeminiPreferencesEntry` отдельно переключает обработчик на UI и игнорирует пустой список. Это code inspection, не runtime подтверждение.
- Добавлен отдельный `cherrygram-014` из README: сборка направлена на `main_Reproducible_Builds` и требует submodules и локальных signing/Firebase/Extra.kt данных. Утверждение имеет статус `docs`, а не build verification. Удалено повторное изложение worker-callback gotcha из списка практических выводов; machine JSON содержит 14 уникальных ID без дублирования. `outputs/plugin-wiki/work/cherrygram-facts.json` и canonical `work/cherrygram-facts.json` синхронизированы; `work/build_wiki.py` читает первый существующий путь и ставит `outputs/plugin-wiki/work` первым, поэтому сборщик использует проверенный идентичный JSON.

## Точность API и граница plugin runtime

Проверены line-level вызовы и сигнатуры: `CGFeatureHooks.switchNoAuthor/switchNoCaptions`, `CGChatMenuInjector.injectCherrygramShortcuts`, `CGMessageMenuInjector.showGeminiItems` и helper calls для parallel lists, `CherrygramPreferencesNavigator.createGemini`, `ApiClient.fetchModels` и его caller. Build claims сверены с конкретными файлами/строками pinned SHA; README утверждения остаются `docs`, вывод о наличии/отсутствии SDK — ограниченный `inference`, radar — `secondary`, статически прочитанные вызовы — `code`. Никакое source inspection не помечено `runtime-verified`.

**`CGFeatureHooks`, menu injectors, preferences navigator и Gemini helpers — compile-time integration самого Cherrygram.** Они вызываются прямым кодом из Telegram классов и опираются на внутренние `ChatActivity`, `MessageObject`, TLRPC и UI-типы. Это не runtime hook framework и не публичный API ExteraGram/AyuGram plugin. На эту сторону нельзя переносить сигнатуры как plugin контракт.

## Повторы и canonical topics

В JSON 13 различных ID; одинаковых claims и повторных ID внутри списка нет. API table и поясняющая проза повторяют одни доказательства намеренно в разных формах, но машинный слой содержит каждый факт один раз. Внешние похожие идеи (menu injection, settings routing, async network) следует синтезировать позднее под canonical topics `hooks`, `ui`, `preferences`, `network`, `build` и `portability`, сохраняя версионное provenance Cherrygram отдельно. Даже когда другие Telegram forks имеют схожие helpers, их внутренние типы и call-site не следует объединять в единый plugin API.

## Остаточные gaps и вердикт

Остальные 166 tree paths в `uz/unnarsx/cherrygram` не исследованы систематически; это включает camera, privacy, helpers, preferences, update/analytics и другие client features. Рассмотрены лишь отобранные integration points и упомянутые в радаре изменения. Не проверены полный upstream diff, текущая совместимость этих внутренних сигнатур, разрешение зависимостей, воспроизводимая сборка, работа приложения и runtime behavior. README ссылается на отдельную build-ветку; её содержимое не подменялось данным commit. `radar-urls.json` пуст, поэтому происхождение выдержек ограничено предоставленным локальным радаром.

**Вердикт: `accepted-with-gaps`, 14 уникальных фактов.** Источник пригоден как пример исходной интеграции Telegram fork и ограниченного build контекста; он не документирует runtime plugin API и не даёт основания для выводов о runtime-поведении.
