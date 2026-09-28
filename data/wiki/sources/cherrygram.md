---
type: code
source_id: cherrygram
platform: Android
review_status: accepted-with-gaps
review: ../reviews/cherrygram.md
reviewer: /root/review_cherrygram
review_model: gpt-6-luna
accepted_facts: 14
date: 2026-09-28
---

# Cherrygram (Android Telegram client fork)

Источник: [arsLan4k1390/Cherrygram](https://github.com/arsLan4k1390/Cherrygram), снимок `main` на commit [`cec3075847d933e13014954ed8b776b767760ce8`](https://github.com/arsLan4k1390/Cherrygram/commit/cec3075847d933e13014954ed8b776b767760ce8). Захват репозитория зафиксирован 2026-09-27; анализ выполнен 2026-09-28. README называет проект неофициальным форком Telegram for Android; в LICENSE указана GNU GPL версии 2 или новее.

## Роль и границы

Это исходный код целого Android-клиента, а не документация SDK плагинов. Изученные `CGFeatureHooks`, `CGChatMenuInjector` и `CGMessageMenuInjector` — внутренние compile-time точки интеграции Cherrygram с Telegram UI. Их сигнатуры полезны как примеры организации функций в форке, но не являются API ExteraGram/AyuGram и не обещают бинарную совместимость с плагинами. Полный upstream-код Telegram и vendored JNI зависимости построчно не анализировались; выборка сосредоточена на собственном пакете Cherrygram, его call-site в `ChatActivity`, сетевом примере Gemini и Gradle-модулях.

| Прочитанный файл | Что подтверждает | Границы |
|---|---|---|
| `README.md`, `LICENSE` | Идентичность Android-клиента; требования/инструкция сборки из README; GPL-2.0-or-later | Инструкция README не означает, что сборка проверена |
| `CGFeatureHooks.kt`, `ChatActivity.java` | Небольшой Kotlin-фасад функций и его прямое использование в UI-классе Telegram | Не runtime hook framework; call-site требуют редактирования кода клиента |
| `CGChatMenuInjector.kt`, `CGMessageMenuInjector.kt`, `ChatActivity.java` | Передача в helpers моделей Telegram, объектов UI и списков элементов меню | Рассмотрены показательные helper-методы и интеграционные вызовы, не все методы этих крупных файлов |
| `CherrygramPreferencesNavigator.kt` | Навигация к собственной настройке через `BaseFragment.presentFragment` | Внутренний навигатор Cherrygram |
| `ApiClient.java`, `ApiCallback.java`, `GeminiPreferencesEntry.java` | Пример сетевого вызова, worker callback и его реального UI-маршалинга в настройке | Только получение списка моделей Gemini; не общий networking API |
| `settings.gradle`, корневой `build.gradle`, `gradle.properties`, `TMessagesProj/build.gradle`, три `TMessagesProj_App*/build.gradle` | Gradle-модульная граница, версии SDK/NDK и часть зависимостей | Gradle не запускался; фактическая разрешимость зависимостей не проверена |
| `tree.json`, `snapshot.json`, `file-manifest.json`, `radar-context.md`, `radar-urls.json` | Закрепление версии, проверка дерева, SHA256 захваченных файлов и контекст радара | В `radar-urls.json` нет отдельных исторических ссылок |

## Подтверждённые точки интеграции

`CGFeatureHooks` — Kotlin `object` с двумя короткими методами, переключающими поля конфигурации Cherrygram. В `ChatActivity` эти методы вызываются рядом с действием пересылки, а также в других внутренних ветках. Пример показывает удобный способ вынести конкретное поведение из upstream-класса в компактный фасад, но фактический hook здесь — заранее добавленный прямой вызов при компиляции приложения.

Для меню чата `CGChatMenuInjector` принимает Telegram UI-контролы (`ActionBarMenuItem`), контекст текущего чата (`ChatActivity`, `TLRPC.Chat`, `TLRPC.User`) и состояние secret chat. Вызовы стоят непосредственно в коде построения верхнего меню `ChatActivity`. Для меню сообщения `CGMessageMenuInjector` принимает `ChatActivity`, `MessageObject` и мутируемые списки текста, option ID и иконок; его методы вызываются из сборщика меню сообщений. Это тесно связанная с конкретной версией Telegram интеграция: изменение структур меню и внутренних типов требует переноса call-site и повторной адаптации.

Настройки Cherrygram маршрутизируются через `CherrygramPreferencesNavigator`: методы получают `BaseFragment` и открывают конкретный экран через `presentFragment`. Для плагина этот пример полезен как локальный способ связать действие UI со страницей настроек, если среда предоставляет сопоставимый публичный маршрут; сами Cherrygram-классы не следует считать доступными снаружи.

Сетевой пример Gemini использует один статический `ExecutorService` с одним потоком для `fetchModels(...)`, задаёт connect/read timeout 5 секунд и выполняет показ/скрытие диалога через `AndroidUtilities.runOnUIThread`. Сам `callback.onResult(modelList)` вызывается worker-потоком после работы запроса и получает пустой список как при не-200 ответе, так и при исключении; у интерфейса нет отдельного канала результата ошибки. Реальный `GeminiPreferencesEntry` явно переводит callback на UI-поток и прекращает обработку пустого списка, а HTTP/сетевую ошибку `ApiClient` показывает отдельным диалогом. Поэтому, повторяя API-паттерн, нужно самому маршалить UI-обновления и не трактовать пустой список как успешный каталог моделей. Это статическое чтение кода, не проверка runtime-поведения.

## Сигнатуры и вызовы

| Модуль/класс | Сигнатура / call-site | Назначение и контекст | Источник |
|---|---|---|---|
| `core.CGFeatureHooks` | `switchNoAuthor(b: Boolean)`, `switchNoCaptions(b: Boolean)` | Kotlin singleton меняет `CherrygramChatsConfig`; внутреннее состояние клиента, не межплагинный контракт | [CGFeatureHooks.kt:16-24](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/uz/unnarsx/cherrygram/core/CGFeatureHooks.kt#L16-L24) |
| `ui.ChatActivity` | `CGChatMenuInjector.INSTANCE.injectCherrygramShortcuts(ChatActivity.this, headerItem, currentChat, currentUser, currentEncryptedChat != null)` | Синхронное добавление пунктов при построении меню заголовка чата | [ChatActivity.java:4742](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java#L4742) |
| `chats.CGChatMenuInjector` | `injectCherrygramShortcuts(chatActivity: ChatActivity, headerItem: ActionBarMenuItem, currentChat: TLRPC.Chat?, currentUser: TLRPC.User?, secretChat: Boolean)` | Компонует shortcuts по конфигурации и аккаунтно-чатовому контексту; вызывается UI-потоком из ChatActivity | [CGChatMenuInjector.kt:105-110](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/uz/unnarsx/cherrygram/chats/CGChatMenuInjector.kt#L105-L110) |
| `chats.CGMessageMenuInjector` | `showGeminiItems(chatActivity: ChatActivity, popupLayout: ActionBarPopupWindowLayout, selectedObject: MessageObject)` | Добавляет вложенное подменю для Gemini к выбранному сообщению; использует тип сообщения и состояние чата | [CGMessageMenuInjector.kt:42-46](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/uz/unnarsx/cherrygram/chats/CGMessageMenuInjector.kt#L42-L46) |
| `ui.ChatActivity` | `CGMessageMenuInjector.INSTANCE.injectForwardWoAuthorship(...items, options, icons)` и соседние `injectViewHistory` / `injectSaveMessage` | Helper добавляет/фильтрует пункты в согласованные списки текста, option IDs и drawable IDs | [ChatActivity.java:47148-47151](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java#L47148-L47151) |
| `preferences.CherrygramPreferencesNavigator` | `createGemini(fragment: BaseFragment) = fragment.presentFragment(GeminiPreferencesEntry())` | Маршрутизация внутреннего экрана настроек | [CherrygramPreferencesNavigator.kt:17-30](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/uz/unnarsx/cherrygram/preferences/CherrygramPreferencesNavigator.kt#L17-L30) |
| `chats.gemini.network.ApiClient` и потребитель `GeminiPreferencesEntry` | `fetchModels(Context, Theme.ResourcesProvider, String apiKey, ApiCallback)`; `onResult` идёт на worker, UI потребитель оборачивает его в `runOnUIThread` | При не-200 ответе/исключении передаётся пустой список без типизированной ошибки; потребитель его игнорирует | [ApiClient.java:42-90](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/uz/unnarsx/cherrygram/chats/gemini/network/ApiClient.java#L42-L90), [GeminiPreferencesEntry.java:152-174](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/TMessagesProj/src/main/java/uz/unnarsx/cherrygram/preferences/GeminiPreferencesEntry.java#L152-L174) |

## Build/dependency seam

`settings.gradle` включает `TMessagesProj` как основной Android library и три app-модуля (`TMessagesProj_App`, Huawei и Standalone); каждый app зависит от `project(':TMessagesProj')`. Поэтому изменения клиентского UI, модели и функции компилируются в общем модуле, а упаковка/сервисные зависимости приложения остаются на стороне соответствующего app-модуля. Это структура исходного fork, а не Gradle plugin contract для стороннего DEX.

README относит build steps к ветке `main_Reproducible_Builds` и указывает clone с submodules, Android Studio/SDK/NDK prerequisites, signing values для app modules, Firebase `google-services.json` и значения `Extra.kt` ([README.md:33-50](https://github.com/arsLan4k1390/Cherrygram/blob/cec3075847d933e13014954ed8b776b767760ce8/README.md#L33-L50)). Это инструкция проекта, не подтверждение успешной сборки данного снимка. В закреплённом снимке `gradle.properties` задаёт `APP_VERSION_NAME=12.10.1`, `APP_VERSION_NAME_CHERRY=11.2.0`, `APP_PACKAGE=uz.unnarsx.cherrygram`, `APP_VERSION_CODE=7039`. Основной модуль использует compile SDK/build tools 36, NDK `27.2.12479018`, Java/Kotlin JVM target 17; README отдельно описывает Android Studio 2025.1.4 и SDK 36. В `TMessagesProj/build.gradle` явно помечены как Cherrygram-зависимости OkHttp 5.4.0, coroutines 1.11.0 и Google Generative AI SDK 0.9.0. Это значения на данном SHA, не гарантия для более поздних сборок.

## Практические выводы для плагин-разработчика

- Используйте fork как каталог примеров клиентских UI-интеграций: найдите построение нужного меню, затем проследите данные и lifecycle через call-site и helper. Применяйте такой подход только при работе с совместимым исходным fork или поддерживаемым API клиента.
- Не трактуйте `CGFeatureHooks`, `CGChatMenuInjector`, `CGMessageMenuInjector` или `CherrygramPreferencesNavigator` как доступный SDK. Они принадлежат package `uz.unnarsx.cherrygram`, но принимают/меняют внутренние структуры Telegram и встраиваются компилятором.
- Для внешнего plugin runtime отдельно проверяйте его документированный API, разрешения, classloader и версию клиента. Cherrygram не подтверждает, что его паттерны можно повторить в DEX без исходников.
- Пример `ApiClient.fetchModels` передаёт ключ в query-параметре `key`; если повторять этот конкретный вызов, учитывайте, что URL могут попасть в журналы и диагностику.

## Радар и незакрытые пробелы

Radar-context сообщает, что проверенные изменения Cherrygram в основном синхронизировали Telegram до 12.10.1 и не дали отдельной свежей функции, прошедшей фильтр новых plugin-кандидатов. Это вторичный контекст радара, а не свойство, выведенное из всего журнала Git. В данном полном снимке по именам/пути не обнаружен публичный plugin SDK или каталог плагинов; совпадения `plugin` относятся к vendored protobuf/build tooling, кроме одного `CGFeatureHooks.kt`. Полный `tree.json` даёт только пути: в нём 11 путей с подстрокой `plugin` (9 в vendored protobuf и 2 Gradle build plugins); `CGFeatureHooks.kt` отдельно является единственным Cherrygram-owned именем с `hook`, но не содержит plugin runtime. `README.md` также не документирует публичный plugin SDK. Поэтому отсутствие публичного SDK — ограниченный вывод по path scan и выбранному README, а не доказательство отсутствия всех возможных механизмов в невключённых submodules или иных ветках.

Не проверялись: сборка, приложение и runtime-поведение; совместимость внутренних сигнатур между версиями; полный diff с Telegram upstream; историческая ветка `main_Reproducible_Builds`, упомянутая в README. Дерево содержит 166 путей в собственном `uz/unnarsx/cherrygram` namespace, тогда как manifest покрывает только выбранные helper/UI/build-файлы; остальные подсистемы клиента (в частности camera, настройки, helpers, analytics/update и privacy) не исследованы систематически. Радар не даёт отдельных URL для этих утверждений: `radar-urls.json` пуст. Для radar slice использованы [исходные строки 162, 256 и 405 в захваченном radar](../../raw/radar.md#L162) и соответствующие выдержки [локального context](../../raw/cherrygram/radar-context.md#L10).

Машинные факты: [`../../work/cherrygram-facts.json`](../../work/cherrygram-facts.json). Снимок и хеши: [`../../raw/cherrygram/snapshot.json`](../../raw/cherrygram/snapshot.json), [`../../raw/cherrygram/file-manifest.json`](../../raw/cherrygram/file-manifest.json), [`../../raw/cherrygram/evidence.md`](../../raw/cherrygram/evidence.md).

