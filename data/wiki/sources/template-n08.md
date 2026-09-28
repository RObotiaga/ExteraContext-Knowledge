---
type: source
source_id: template-n08
platform: Android
review_status: accepted-with-gaps
review: ../reviews/template-n08.md
date: 2026-09-27
---

# Kotlin/DEX plugin template n08

Источник: [репозиторий](https://github.com/exteraStuff/pydex-plugin-template) на снимке `435425db4436927185534e1e06111a6a22aa1740` (ветка `master`, дата снимка 2026-09-27). Лицензия — MIT. Это шаблон для Android-плагина exteraGram/AyuGram: Python-файл остается точкой входа движка плагинов, а основная логика Kotlin собирается в DEX, сжимается и вкладывается в комментарий этого же `.py`.

## Идентичность и расхождение с радаром

Радар называет проект `n08i40k/exteragram-plugin-template`. Запрос страницы GitHub по этому старому адресу [перенаправляется на `exteraStuff/pydex-plugin-template`](https://github.com/n08i40k/exteragram-plugin-template), и canonical URL, API snapshot, SHA и просмотренное дерево указывают на один и тот же текущий репозиторий. Доказательств, что после переезда это иной плагин или отдельная копия, нет; в базе источник остается одним `template-n08`, исторический owner/name сохранен как alias.

Радар также говорит о связке с отдельным `extera-gradle-plugin`. В этом конкретном snapshot проект не применяет его: `build.gradle.kts` регистрирует собственные `ShadowJar` и `BuildDexTask`, а `BuildDexTask.kt` напрямую вызывает API R8. Поэтому описание ниже относится к реализации этого репозитория на SHA, не к внешнему Gradle-плагину.

## Покрытие

| Прочитанный материал | Что извлечено | Пропуски |
|---|---|---|
| `README.md`, `justfile`, `scripts/prepare_release.py`, `.github/workflows/release.yml` | локальный цикл, реальные recipes, упаковка, выпуск и CI; justfile отдельно получен по пути из tree | workflow не запускался |
| `exteragram-plugin-template.py` полностью | metadata, DEX decoder/loader, bridge calls, меню, lifecycle, диагностирование | API приложения проверен только по коду шаблона |
| все Kotlin-файлы `src/main/kotlin/ru/n08i40k/template/**` | публичные bridge methods, callbacks, hooks, threading, shutdown, i18n, utilities | runtime приложения и устойчивость к конкретным версиям клиента не проверялись |
| `build.gradle.kts`, `buildSrc/build.gradle.kts`, `buildSrc/src/main/kotlin/BuildDexTask.kt`, `settings.gradle.kts`, `gradle.properties`, `gradle/libs.versions.toml`, `proguard-rules.pro` | плагины, SDK/JVM, зависимости, relocation, compile classpath, R8/Dex inputs/outputs | зависимости не скачивались, сборка не выполнялась |
| `tools/embed_dex.py`, `tools/dev_watch.py`, `tools/FixTelegramJar.java` | формат упаковки, reload-процесс, compile-only host JAR preprocessing | инструменты не запускались |
| `.gitattributes`, `.gitignore`, `.python-version`, `pyproject.toml`, `uv.lock` (верхняя часть), Gradle wrapper properties, i18n resources, `LICENSE` | LFS для Telegram JAR, исключения generated outputs, версии Python/Gradle, декларация окружения, языки, лицензия | транзитивные pins `uv.lock` не инвентаризировались целиком; wrapper JAR бинарный и не анализировался |

В манифесте snapshot 47 файлов после дополнительного получения `justfile`, Gradle wrapper properties, `.gitattributes`, `.gitignore`, `.python-version` и `uv.lock` по путям из `tree.json`; сюда входит бинарный wrapper JAR. Все Kotlin/Python исходники и относящиеся к сборке текстовые конфиги просмотрены; бинарный wrapper JAR, транзитивные записи lockfile и Gradle wrapper scripts не анализировались подробно. Файлы и ссылки закреплены в [дереве snapshot](../../raw/template-n08/tree.json) и [манифесте](../../raw/template-n08/file-manifest.json).

## Модель исполнения и lifecycle

Python-класс `TemplatePlugin(BasePlugin)` исполняется штатным движком, но Kotlin-часть находится в `ru.n08i40k.template.Plugin`. Python читает встроенный DEX из комментариев между точными маркерами `# === EMDEDDED DEX BEGIN ===` и `# === EMDEDDED DEX END ===`, Base64-декодирует и потоково распаковывает XZ/LZMA. DEX загружается через `dalvik.system.InMemoryDexClassLoader(ByteBuffer.wrap(dex), ApplicationLoader.applicationContext.getClassLoader())`. Родительский classloader — classloader приложения.

Вызовы Python→JVM являются контрактом по строковому имени: `getDeclaredMethod(name, *types).invoke(None, *args)`. Указанные `types` необходимы для выбора перегрузки. Совпадающие пары на двух сторонах:

| Kotlin static entry | Bridge call | Смысл |
|---|---|---|
| `Plugin.getBuildDate(): String` | `call("getBuildDate")` | время сборки из `BuildConfig.BUILD_TIME` |
| `Plugin.inject(String, ValueCallback<String>): Unit` | `call("inject", String(version), Logger(), types=(String.getClass(), ValueCallback.getClass()))` | инициализация JVM-плагина и прокси-логгер |
| `Plugin.finalizeInject(): Unit` | `call("finalizeInject")` | установка hooks после Python UI |
| `Plugin.invokeChatContextMenuCallback(String, Long): Unit` | key и dialog id, с JVM типами `String` и `Long.TYPE` | dispatch на Kotlin callback |
| `Plugin.invokeSettingsActionCallback(String): Unit` | key и JVM `String` | dispatch действия из настроек |
| `Plugin.eject(): Unit` | `call("eject")` | неблокирующий запрос выгрузки |

Успешный порядок в `TemplatePlugin._run_plugin_load`: подготовка classloader → `inject` → регистрация Python UI → `finalizeInject`. Загрузка запускается в выделенном daemon thread; lock и флаг `_full_load_started` не дают двум параллельным загрузкам одной Python-инстанции дублировать эту последовательность. Ошибка любого этапа формирует отчет с stage/version/log, копирует его в clipboard и показывает диалог/bulletin; затем вызывается `on_plugin_eject`.

`Plugin.inject` синхронизирован. Он отказывает во второй инъекции в том же classloader, а для разных classloader-ов использует `System.getProperties()` и `HANDLE_KEY` как межзагрузчиковой rendezvous: предыдущий plugin получает `ejectPromise()`, и новый ждет его thread перед своей инициализацией. Поле `INSTANCE` и флаг `WAS_INJECTED` volatile. `finalizeInject` разрешено вызывать после Python-регистрации UI; если eject прошел раньше него, метод возвращает без ошибки.

Выгрузка Kotlin снимает все `XC_MethodHook.Unhook`, отменяет `backgroundScope`, ждет завершения его `Job`, затем уведомляет `EjectNotifier`. `Plugin.inject` заранее выставляет `WAS_INJECTED`; тот же classloader нельзя повторно использовать даже после очистки `INSTANCE`. Python unload вызывает Kotlin `eject()` без ожидания потока teardown и сразу очищает bridge reference. Отдельно найден потенциальный cleanup gap: исключение в Python load stages ведет к `on_plugin_eject()`, который только снимает меню/сбрасывает bridge и сам не вызывает Kotlin `eject()`; если JVM inject уже завершился, Kotlin `INSTANCE` может остаться. Это вывод из ветвей кода, не проверенный runtime сценарий. Listener priority сортируется по возрастанию; шаблон подписывает `RefCounter.wait()` под priority `999`, а `Logger` — под `1000`, чтобы дождаться refcount и залогировать eject последним. UI-dispatch helper-ы увеличивают refcount перед постановкой callback в main thread и уменьшают в `finally`. Для `runBlockingOnUIThread` suspend-блок исполняется через `runBlocking` на UI thread. Это реализованная стратегия source-кода, не доказательство отсутствия зависания при ошибочном caller usage.

## Точки расширения и важные вызовы

| Модуль/класс | API или call-site | Назначение и поток/жизненный цикл | Доказательство |
|---|---|---|---|
| Python `TemplatePlugin` | `on_plugin_load()` / `_run_plugin_load()` | новый daemon thread; bridge, меню и finalize последовательны | [Python template](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/exteragram-plugin-template.py#L505-L551) |
| Python `JvmPluginBridge` | `InMemoryDexClassLoader(ByteBuffer.wrap(dex), appClassLoader)` | загрузить Kotlin-классы в контексте Android app loader | [bridge](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/exteragram-plugin-template.py#L105-L145) |
| Kotlin `Plugin` companion | `inject(version, logReceiver)`; `finalizeInject()`; `eject()` | публичные JVM-static lifecycle entry points; inject/finalize blocking и synchronized, eject any-thread и возвращается сразу | [Plugin.kt](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/Plugin.kt#L67-L168) |
| Kotlin `Plugin` | `getSharedPrefs(): SharedPreferences` | приватные preferences приложения с именем plugin ID и `MODE_PRIVATE` | [Plugin.kt](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/Plugin.kt#L170-L174) |
| Kotlin `Plugin` | `coroutineScope()` / `childCoroutineScope()` | базовая IO scope с `SupervisorJob` и fatal exception handler; child добавляет child `SupervisorJob`, не теряя остальной context | [Plugin.kt](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/Plugin.kt#L176-L188) |
| Kotlin `Plugin.hookMethods` | `XposedBridge.hookMethod(Member, XC_MethodHook)`; before/after wrappers | добавляет `Unhook` в список; callback обернут в `Logger.tryOrFatal`; все снятия сгруппированы в eject | [Plugin.kt](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/Plugin.kt#L212-L269) |
| `HookBundle` / `InstallHook` | `inject(before, after)`; `(Member, (MethodHookParam) -> Unit) -> Unit` | расширяемые группы hooks получают две функции-установщика, но не управляют unhook самостоятельно | [hook API](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/hook/HookBundle.kt), [installer](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/hook/HookInstaller.kt) |
| `ExampleHookBundle` | поиск `LaunchActivity.declaredMethods` по `name == "onResume" && parameterCount == 0`, затем `after(onResume)` | демонстрация поиска reflection-ом и after hook; при отсутствии метода логирует пропуск | [example bundle](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/hook/impl/ExampleHookBundle.kt) |
| `ChatContextMenuActions` | `chatContextMenuCallbackRegistry.register(key) { ... }`; `freeze()` | Kotlin callbacks принимают `Long peerId`; ключ обязан совпасть с Python key `example`; реестр замораживается после регистрации | [actions](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/ChatContextMenuActions.kt) |
| `SettingsMenuActions` | `settingsActionCallbackRegistry.register(key) { ... }`; `freeze()` | аналогичный registry для `Runnable`-действий настроек | [settings actions](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/SettingsMenuActions.kt) |
| Python `ChatContextMenu` | `add_menu_item(MenuItemData(CHAT_ACTION_MENU,... on_click=...))`; `remove_menu_item(item_id)` | регистрирует/снимает host UI пункты; хранит ID; click извлекает диалог ID из объекта либо mapping `dialog_id`/`dialogId`/`chatActivity`/`fragment` | [Python menu](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/exteragram-plugin-template.py#L202-L296) |
| Python `SettingsActions` | `create_settings() -> [Header, Text(... on_click=...)]` | пример settings control и callback dispatch; UI остается в Python | [settings](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/exteragram-plugin-template.py#L299-L331) |
| `LockableRegistry<T>` | `register`, `freeze`, `get` | запрещает позднюю регистрацию, повторный freeze и доступ до freeze; неизвестный ключ — `IllegalArgumentException` | [registry](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/registry/LockableRegistry.kt) |
| `EjectNotifier` | `subscribe(priority, listener): () -> Unit`, `fire()` | CopyOnWriteArrayList listener-ов, сортировка priority по возрастанию, callback затем очистка; unsubscribe closure доступна | [notifier](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/event/eject/EjectNotifier.kt) |
| `RefCounter` | `inc()`, `dec()`, suspend `wait()` | атомарное число, один waiter на экземпляр; ноль завершает `CompletableDeferred`; предназначен удерживать async callbacks при eject | [counter](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/util/RefCounter.kt) |
| `runOnUIThread` / `runBlockingOnUIThread` | `AndroidUtilities.runOnUIThread { try { block() } finally { RefCounter.dec() } }` | выполняет host UI operation на main thread и учитывает незавершенный callback для выгрузки | [thread helpers](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/util/Run.kt) |
| `BulletinHelper.show` | `BulletinFactory.of(fragment).createSimpleBulletin(...)` либо emoji/drawable; `.show()` | `@AnyThread`, переключается через `runOnMainThread`; безопасно возвращается, если нет безопасного фрагмента | [bulletin helper](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/util/BulletinHelper.kt) |
| `Logger` | `info`, `fatal`, `tryOrFatal`; `ValueCallback.onReceiveValue` | форматирует сообщения с classloader-instance ID; сбой receiver запрашивает eject; fatal по умолчанию инициирует eject | [logger](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/util/Logger.kt) |
| `getField` / `Field.getAs<T>` | `getDeclaredField(name)`, `isAccessible = true`; безопасный cast | reflection helpers шаблона; `getLastFragment()` использует приватное поле `LaunchActivity.actionBarLayout` | [reflection](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/util/Reflection.kt), [fragment helper](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/util/Fragment.kt) |
| `LocaleController.resolveLanguageCode` | `Locale.getISOLanguages()` validation | выбирает базовый/короткий язык клиента, нормализует региональный тег; неизвестный код сводится к `en` | [locale extension](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/extension/LocaleController.kt) |
| `MessagePluralFormatter` | `MessageValueFormatter.typeId == "plural"`; `format(...)` | ручное plural category для русского (`one/few/many`) и default языка (`one/other`) в i18n4k; отрицательное количество берется по модулю | [formatter](https://github.com/exteraStuff/pydex-plugin-template/blob/435425db4436927185534e1e06111a6a22aa1740/src/main/kotlin/ru/n08i40k/template/i18n/MessagePluralFormatter.kt) |

## Сборка, артефакты и рецепты

1. `just init <package> <plugin-id> <name>` меняет Java/Kotlin namespace и package directory, ID/filename, display name, Gradle/ProGuard references и `pyproject.toml`; затем вызывает `uv sync`. Regex требует dotted lowercase package и ID из `[a-z0-9][a-z0-9._-]*`.
2. `just dex` проверяет Java и при необходимости запускает `just strip-telegram-jar`, затем `./gradlew buildDexDebug`. `just loc` вызывает `generateI18n4kFiles` отдельно от полной DEX сборки.
3. Variant tasks имеют имена `buildDexDebug` и `buildDexRelease`; выводы — `dist/dex/debug/classes.dex` и `dist/dex/release/classes.dex`. Дополнительный output `build/intermediates/dex-classpath/<variant>/classpath.jar` объединяет классы host/dependency classpath, чтобы убрать дубли при R8.
4. `just embed [DEX_PATH] [OUTPUT] [SOURCE]` применяет LZMA XZ с preset `9 | PRESET_EXTREME`, base64 и строки комментария шириной 120. Marker strings должны присутствовать и END должен следовать за BEGIN. README ожидает `dist/<plugin-id>.py`; embedded-комментарий не создает runtime Python string.
5. `just ci-release <version> [output]` принимает строгую версию `x.y.z`, во временной копии обновляет `__version__` и `pyproject.toml`, строит release DEX, затем встраивает его в `.plugin`-артефакт. GitHub Release workflow отдельно публикует этот `.plugin` и `classes.dex`, прикрепляет build provenance attestations, коммитит обновленные metadata в выбранную ветку и отправляет tag/release; workflow прочитан, но не запускался.
6. `just watch [--debug] [--poll seconds]` следит за Python source и debug DEX. При изменениях генерирует временную копию, отправляет ее в extera dev server через `exteragram_utils.dev_client.DeviceConnection.write_plugin`, ждет 0.3 сек и вызывает `reload_plugin`. При выходе пытается остановить debugger и отключиться.
7. `just update-apk <apk>` преобразует host APK через `dex2jar`, затем `tools/FixTelegramJar.java` восстанавливает вложенные class inheritance и исключает классы, поставляемые Gradle dependencies; recipe сохраняет полный `Telegram.jar` и stripped classpath JAR в `libs/` и коммитит полный host jar. `just strip-telegram-jar` повторно строит stripped JAR. `just gen-stubs <rt.jar> <android.jar>` запускает `java2pyi` для JDK, Android и host jars.

Gradle обрабатывает каждую Android variant: ShadowJar берет Kotlin/Java outputs и runtime jars, переносит `kotlin`, `kotlinx`, `de.comahe.i18n4k` под `ru.n08i40k.template_shaded.*`, а AndroidX тоже перемещает, кроме явно исключенных классов и `androidx.recyclerview.**`/`androidx.lifecycle.**`, объявленных `compileOnly`. `BuildDexTask` подает shaded jar в R8, boot classpath отдельно как library files, host/dependency compile classpath как classpath; debug `BUILD_TIME` фиксирован на 0, release использует epoch millis, поэтому `getBuildDate()` в debug не сообщает реальную дату сборки; выставляет `minSdk`, режим DEBUG/RELEASE и `OutputMode.DexIndexed`. При объединении classpath JAR дубликаты class entry пропускаются, оставляя первый найденный.

Текущие настройки этого snapshot: Gradle wrapper `9.1.0`, Android Gradle Plugin `9.0.1`, Shadow plugin `9.6.1`, R8 `9.4.17`, i18n4k plugin `0.11.2`, Kotlin `2.2.0`, JVM bytecode 11, Java compile target 11 с core-library desugaring, min SDK API 26 и compile SDK API 36.1. GitHub workflow использует Temurin JDK 21, Python 3.14, Android Build Tools 36.1.0 и `platforms;android-36.1`. Версии зависимостей в version catalog: Aliuhook 1.1.3; coroutines 1.10.2; i18n4k core 0.11.2; desugar_jdk_libs 2.1.5; RecyclerView 1.4.0; Lifecycle ViewModel 2.6.2; immutable collections 0.4.0. Python окружение требует Python `>=3.14` и `exteragram-utils>=0.1.3`; dev group содержит Ruff `>=0.15.4` и ty `>=0.0.15`. Kotlin stdlib, coroutines и i18n4k идут `implementation`; Telegram, Aliuhook, immutable collections, RecyclerView и Lifecycle — `compileOnly`; desugar — `coreLibraryDesugaring`.

`proguard-rules.pro` сохраняет `ru.n08i40k.template.**` полностью, запрещает обфускацию и сохраняет annotation/inner/enclosing/signature metadata. Это важно для Java reflection, Python bridge и имен класса, но правило привязано к исходному namespace: `just init` обновляет его. R8 вызывается напрямую; `-ignorewarnings` применяется к unresolved warnings Telegram JAR. Упоминание рефлексии, R8 и reload подтверждено исходниками; внешний `extera-gradle-plugin` здесь не используется.

## Практические рецепты

- **Добавить callback пункта меню:** согласовать key в `ChatContextMenu.MENU_ITEMS` Python и `ChatContextMenuButton` Kotlin; зарегистрировать обработчик в `ChatContextMenuActions.register`, freeze уже выполняется в конце метода; в Python callback передать JVM типы `String` и `Long.TYPE`.
- **Добавить настройку:** вернуть `Header`/`Text` из Python `create_settings`; привязать key к `SettingsActionButton` и `SettingsMenuActions.register`. UI и dispatch принадлежат Python/bridge, логика действия — Kotlin.
- **Добавить hook:** отдельный `HookBundle` ищет или получает `Member`, устанавливает `before`/`after` callback; зарегистрировать bundle в `Plugin.hookMethods`. Центральный список хранит `Unhook` и очищается при eject.
- **Запустить фоновые задачи:** брать `Plugin.coroutineScope()` либо `childCoroutineScope()`. Корневая scope на `Dispatchers.IO` отменяется при eject; исключение без локальной обработки приводит в `Logger.fatal`, который запрашивает eject.
- **Обновить API хоста для компиляции:** `just update-apk <APK>`; для автоматического обновления на debug/release убедиться, что stripped jar новее полного Telegram JAR и `FixTelegramJar.java`.
- **Проверить готовый файл:** по коду можно проверить присутствие маркеров, декодировать XZ/Base64 и сравнить `classes.dex`; в текущем исследовании никакие recipes, build, upload, device reload или runtime не запускались.

## Ограничения и статус доказательств

- В репозитории snapshot отсутствуют тесты и полученные результаты сборки/устройства. Данная страница имеет статус анализа кода; `runtime-verified` утверждений нет.
- Python metadata задает `__min_version__ = "12.1.1"` (legacy key), не `__app_version__`; документация README на этом SHA не уточняет фактическую совместимость API. Не выводить из этого, что Kotlin compileOnly поверхность гарантированно подходит любой версии клиента.
- Метод `Plugin.getVersion()` существует, но Python bridge на текущем снимке не вызывает его; указывать его как реально используемый pipeline вызов нельзя.
- `getSharedPrefs`, coroutine scopes, reference counter, plural formatter и reflection helpers являются кодом шаблона. Они не доказывают, что каждый из них нужен или протестирован для любого плагина.
- Не включено: полная семантика exteraGram `BasePlugin`/`MenuItemData`, host class internals и API Aliuhook; upstream, версии клиентов и совместимость по устройствам за рамками локального snapshot.
- README перечисляет команды/зависимости и является docs evidence. Сигнатуры и детали реализации выше — code evidence; только наличие кода не означает успешный build или runtime.
