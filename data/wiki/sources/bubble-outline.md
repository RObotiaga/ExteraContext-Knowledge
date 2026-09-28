---
type: source
source_id: bubble-outline
platform: Android
review_status: accepted-with-gaps
review: ../reviews/bubble-outline.md
date: 2026-09-28
---

# xwwvv/ios-bubble-outline — Android ExteraGram-плагин с Kotlin DEX

Источник: [xwwvv/ios-bubble-outline](https://github.com/xwwvv/ios-bubble-outline), ветка `main`, закреплённый snapshot `15355c3affe1b41fd9551014c50ed893d3fd4f4c` (сохранён 2026-09-27). GitHub metadata в этом snapshot не указывает лицензию. Имя `ios-bubble-outline` и UI-описание «в стиле iOS» не означают iOS-реализацию: единственный прикладной код — ExteraGram Python plugin и Android/Kotlin DEX для `Canvas`; Swift/UIKit/Objective-C кода в снимке нет.

Ничего не запускалось, не собиралось и не устанавливалось. Runtime-поведение, совместимость с конкретным APK и корректность опубликованного DEX не проверялись. Утверждения о реализации ниже имеют статус `code`; замечания о отсутствующих файлах основаны на полном неповреждённом дереве snapshot.

## Идентификация и расхождение радара

Радар назвал проект «новым DEX-плагином» и описал его как визуальную модификацию пузырей сообщений. В коде это подтверждается как назначение Android ExteraGram-плагина: Python entrypoint объявляет API-совместимость ExteraGram, скачивает DEX и hook-ит `ChatMessageCell.onDraw(Canvas)`, а Kotlin рисует закруглённый stroke поверх фона. Радарная пометка `iOS` относится к стилизации интерфейса, а не к платформе плагина. Других исторических commit URL в `radar-urls.json` нет.

## Покрытие и границы

| Область | Прочитанное и результат | Пропуск |
|---|---|---|
| Snapshot и README/docs | Полное дерево `tree.json` (29 записей, `truncated=false`), `snapshot.json`, `repository.json`, radar context и radar URLs. В pinned tree нет README, каталога docs или LICENSE; metadata GitHub возвращает `license: null`. | У проекта нет README/docs и заявленной лицензии в этом snapshot; выводы о назначении сверены с кодом и вторичным радаром. |
| Entry point, hooks и lifecycle | `BubbleOutline.plugin` целиком: metadata, DEX fetch/cache/loading, reflection bridge, registration, retry, settings и callback. | Нет исходников базового `BasePlugin`, `MethodHook`, `find_class` или host-клиента в этом репозитории; точная семантика SDK и hook-priority здесь не определена. |
| DEX code и rendering | `app/src/main/java/com/myplugin/outline/Main.kt` целиком: static bridge, чтение геометрии cell, цвет/alpha/ширина/radius и рисование. Отдельно получен и статически разобран method proto сохранённого `outputs/bubble-outline.dex`; его blob SHA совпал с pinned tree. | Не проверено на устройстве; отсутствуют тесты/тестовые фикстуры и версия host Telegram, на которой symbols существуют. |
| UI/settings | `create_settings()` и `draw_outline()` в plugin entrypoint. | Нет валидации реальным settings UI; `forceEverywhere` передаётся в Kotlin, но в Kotlin-реализации не используется. |
| Сеть и storage | `requests.get`, локальный DEX cache через `ApplicationLoader.applicationContext.getDir`, диагностический файл в `Android/media/<package>`. | Нет сетевого trace и проверки Android storage policy на конкретной версии OS. Нет checksum/signature/version validation перед загрузкой DEX. |
| Сборка и CI | Все текстовые build/config файлы snapshot: `app/build.gradle`, `build.gradle`, `gradle.properties`, `settings.gradle`, `gradle/wrapper/gradle-wrapper.properties`, `gradlew`, `gradlew.bat`, `.gitignore`, manifest, workflow, `version.txt`, `outputs/actual.json`. | CI/build не запускались. Нет test task/test source в дереве. `.plugin` ссылается на DEX по mutable `main`, а не на SHA. |
| Артефакты | В дереве присутствует `outputs/bubble-outline.dex` (5 244 байта) и `outputs/actual.json`. Последний указывает `1.0.0`, тогда как plugin metadata — `1.0.3`; `version.txt` также `1.0.0`. Для DEX проверены pinned Git blob и method proto `drawOutline`. | Полный байткод и соответствие остальному исходному Kotlin не анализировались. |
| iOS-specific | Проверено всё дерево: Swift, Objective-C, Xcode project, UIKit или iOS packaging отсутствуют. | Нельзя вывести iOS lifecycle, hook mechanism, rendering API, permissions, build constraints или переносимость по Android-коду. Для iOS нужен отдельный первичный источник/API и отдельная проверка. |

Все исходные permalink ниже привязаны к SHA `15355c3affe1b41fd9551014c50ed893d3fd4f4c`. API Android и ExteraGram здесь нельзя считать iOS API или автоматически переносить в iOS plugin ecosystem.

## Архитектура, hook и lifecycle

`BubbleOutline.plugin` — Python entrypoint на базе `BasePlugin`. Он задаёт `__id__ = ios_bubble_outline`, `__version__ = 1.0.3`, минимальную версию приложения `>=12.9.0` и SDK `>=1.4.4.3`. В `on_plugin_load()` plugin сначала читает/скачивает DEX, загружает класс `com.myplugin.outline.Main`, вызывает static `start()`, затем пробует hook; если hook не установлен, запускает daemon thread с 30 попытками через секунду.

Hook устанавливается на declared method `org.telegram.ui.Cells.ChatMessageCell.onDraw(android.graphics.Canvas)` через `find_class`, `setAccessible(true)` и `self.hook_method(..., 2147483647)`. `OutlineHook.after_hooked_method` передаёт `param.thisObject` и первый аргумент Canvas в plugin renderer. Это пример внутреннего Android Telegram hook point на конкретном snapshot; стабильность symbol/method signature между host releases не доказана. Код не задаёт отдельную account scope.

`Main` — Kotlin `object`, экспортирующий через `@JvmStatic` `start()`, `version()` и `drawOutline(...)`. `start()` пустой; `version()` возвращает целое `1`. Python вызывает `drawOutline` через Java reflection с точными parameter classes. Kotlin берёт bounds у cell через reflective getters `getBackgroundDrawableLeft/Top/Right/Bottom`; при неположительной ширине/высоте возвращается. Затем вычисляет цвет, alpha и dp width, считывает общий `SharedConfig.bubbleRadius` (fallback 18; clamp 0..60), переиспользует `Paint`/`RectF` и рисует `Canvas.drawRoundRect`. Внутри renderer широкий `catch(Throwable)` молча подавляет исключения; Python регистрирует только первую ошибку вызова reflection.

В классе плагина не объявлен собственный unload callback: видимый retry thread daemon и заканчивает цикл после успешного hook либо исчерпания 30 повторов, но код не отменяет его при выгрузке плагина. Это только наблюдение по этому классу, а не вывод о поведении базового `BasePlugin`.

## UI, storage, network и доверие к артефакту

Settings описаны декларативными `Header`, `Input` и `Switch`: цвет `#RRGGBB`, ширина в dp, opacity 0–100 и `force_everywhere`. Entry point читает значения на каждом draw и передаёт reflection bridge. Kotlin clamp-ит opacity к 0–100, alpha переводит в диапазон 0–255, width ограничивает минимумом 0.5 dp. Парсер цвета принимает 6 hex цифр (добавляет непрозрачный alpha) или 8 hex цифр; невалидное значение превращается в чёрный. Параметр `forceEverywhere` присутствует в API, но тело Kotlin-функции его не читает; текущее поведение не подтверждает обещание «форсировать везде».

Есть вероятное несовпадение Python reflection signature и Kotlin declaration: entrypoint передаёт в `getDeclaredMethod` классы `java.lang.Float`, `java.lang.Integer`, `java.lang.Boolean`, а Kotlin объявляет non-null `Float`, `Int`, `Boolean`. Статический разбор DEX подтвердил descriptor `drawOutline(Ljava/lang/Object;Landroid/graphics/Canvas;Ljava/lang/String;FIZ)V`, где последние типы — примитивные `float`, `int`, `boolean`; Java reflection требует точного совпадения параметров. Если `find_class` возвращает обычные boxed `Class` для написанных имён, lookup не найдёт метод. Descriptor теперь проверен по pinned binary, но фактический результат `find_class` и runtime-вызов без host SDK/устройства не проверялись, поэтому итог о сбое вызова остаётся inference. Возможные исправления — передать primitive class tokens либо объявить boxed Kotlin-параметры.

`_fetch_dex()` предпочитает любой непустой локальный cache файл `bubble-outline-v2.dex`; иначе делает `requests.get(DEX_URL, timeout=30)`, вызывает `raise_for_status()`, пишет байты на диск и возвращает их. URL фиксирует `outputs/bubble-outline.dex` на GitHub `main`. Код не проверяет hash, подпись, размер, версию или происхождение; cached DEX не инвалидируется по версии/etag. Это наблюдение о реализации и поверхности supply-chain risk, не runtime-эксплуатация.

Загрузка сначала пробует `InMemoryDexClassLoader(ByteBuffer.wrap(data), appClassLoader)`, при исключении — `DexClassLoader(cachePath, app.getDir(DEX_OPT_DIR, 0), null, appClassLoader)`. Для cache/optimized dirs применяются app context `getDir`. Диагностика пытается записывать append-only лог в `/storage/emulated/0/Android/media/<package>/ios_bubble_outline_debug.log`; ошибки этой записи подавляются. Плагин также пишет Android `Log.d("tmessages", ...)` и вызывает `self.log()` с защитой от исключений.

## Build, CI и версия

Gradle Wrapper properties задают Gradle `8.10.2`; root pins Android Gradle Plugin `8.4.2` и Kotlin Android plugin `1.9.24`. `app` использует Android library plugin, namespace `com.myplugin.outline`, `compileSdk 34`, `minSdk 21`, Java source/target 11 и Kotlin JVM target 11. `telegram-stubs.jar` подключается `compileOnly` только если файл существует; в snapshot `app/libs` содержит лишь `.gitkeep`, поэтому Telegram stubs в checkout отсутствуют. `gradle-wrapper.jar` также отсутствует; сохранённые `gradlew` и `gradlew.bat` содержат собственный fallback, который скачивает Gradle distribution 8.10.2 через curl/wget либо PowerShell `Invoke-WebRequest` без видимой проверки checksum.

Custom task `:app:packageDex` зависит от `runD8`: после сборки classes JAR вызывает найденный Android build-tools D8 с `--min-api 21` и android boot classpath, затем переименовывает `classes.dex` в `outputs/bubble-outline.dex`. GitHub Actions запускается на push в `main` или вручную, ставит Temurin JDK 17, вызывает Gradle task, записывает build log при ошибке и генерирует `outputs/actual.json` из `version.txt`. `Commit artifacts` задан с `if: always()`, коммитит `outputs` и пробует push, игнорируя ошибку push (`|| true`). Наличие этой конфигурации не является доказательством, что конкретная сборка workflow прошла.

Есть явное расхождение версий в текстовых исходниках snapshot: plugin declares `1.0.3`, `version.txt` и сохранённый `outputs/actual.json` равны `1.0.0`, а `Main.version()` возвращает целое `1`; import log string и lifecycle log содержат `v1.0.3`. Workflow записывает `actual.json` из `version.txt`, но это не доказывает версию или соответствие исходнику лежащего рядом DEX: binary отсутствует в локальном raw snapshot и не анализировался. Версионный контракт между wrapper, Kotlin source и manifest поэтому не унифицирован.

## Таблица вызовов и точек вмешательства

| Модуль/класс | Сигнатура или call-site | Назначение и lifecycle | Доказательство |
|---|---|---|---|
| `IosBubbleOutlinePlugin` | `on_plugin_load()` | Инициализирует поля, загружает DEX, вызывает `start()`, hook-ит метод; запускается на загрузке plugin. | [entrypoint](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/BubbleOutline.plugin#L60-L80) |
| `IosBubbleOutlinePlugin` | `_fetch_dex()`; `requests.get(DEX_URL, timeout=30)` | Cache-first загрузка DEX; network call без hash/signature check. | [fetch/cache](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/BubbleOutline.plugin#L82-L113) |
| `IosBubbleOutlinePlugin` | `_load_dex(data)` | In-memory classloader, fallback на `DexClassLoader` и optimized app dir. | [DEX loading](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/BubbleOutline.plugin#L115-L137) |
| `IosBubbleOutlinePlugin` | `_try_hook()`; `find_class(...ChatMessageCell).getDeclaredMethod("onDraw", Canvas)` | Инъекция post-draw callback с максимальным числом priority `2147483647`. | [hook registration](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/BubbleOutline.plugin#L147-L168) |
| `OutlineHook` | `after_hooked_method(param)` | После оригинального draw передаёт cell и Canvas renderer-у. | [hook callback](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/BubbleOutline.plugin#L224-L230) |
| `IosBubbleOutlinePlugin` | `create_settings()` | Возвращает Header, три Input и Switch с config defaults. | [settings UI](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/BubbleOutline.plugin#L170-L198) |
| `IosBubbleOutlinePlugin` | `draw_outline(cell, canvas)` → reflected `drawOutline(Object, Canvas, String, Float, Integer, Boolean)` | Читает settings на draw path и мостит Python значения в DEX. | [Python bridge](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/BubbleOutline.plugin#L200-L221) |
| Kotlin `Main` | `@JvmStatic fun drawOutline(cell: Any, canvas: Canvas, colorHex: String, widthDp: Float, opacityPct: Int, forceEverywhere: Boolean)` | Рисует stroke по bounds cell; `forceEverywhere` не используется в теле. | [renderer](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/app/src/main/java/com/myplugin/outline/Main.kt#L23-L53) |
| Kotlin `Main` | `bubbleRadius()` | Reflectively читает `SharedConfig.bubbleRadius`; fallback 18. | [radius lookup](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/app/src/main/java/com/myplugin/outline/Main.kt#L59-L66) |
| Gradle `runD8` | `:app:packageDex` → D8 `--min-api 21` | Формирует standalone `.dex` в `outputs/`. | [DEX task](https://github.com/xwwvv/ios-bubble-outline/blob/15355c3affe1b41fd9551014c50ed893d3fd4f4c/app/build.gradle#L64-L113) |

В workflow шаг генерации `actual.json` использует обычное условие GitHub Actions `success()`, поэтому при ошибке `Build DEX` он будет пропущен; шаг `Commit artifacts` помечен `if: always()` и всё равно запустится. Это описывает YAML snapshot, а не результат конкретного workflow run.

## Практические техники и ограничения

- Для Android ExteraGram DEX-оболочки пример показывает разделение Python UI/hook lifecycle и Kotlin drawing implementation с reflection bridge. Это схема конкретного проекта, а не рекомендация переносить Android API в iOS.
- Условный retry полезен, когда Telegram class ещё не доступен при plugin-load: здесь ограничение — максимум 30 секунд, daemon thread и отсутствие отдельного cancel/unload path в видимом коде.
- Горячий draw path повторно использует `Paint`/`RectF` и меняет Paint-параметры только при изменении color/alpha/width/radius; но код не содержит явной синхронизации. Вызов из hook/thread и безопасность общего mutable renderer state не проверялись.
- Versioned cache name сам по себе не является cache validation: источник читает любой непустой DEX и скачивает исполняемый артефакт с изменяемой ветки `main` без integrity check.
- Для iOS реализации нужны iOS-specific первичные API и hooks/render lifecycle; этот source не даёт их и не является подтверждением native iOS bubble customization.

## Открытые пробелы

1. Нет README, пользовательской документации, тестов и license-файла в закреплённом tree; GitHub API указывает отсутствие license metadata.
2. Неизвестно, проверялся ли DEX на живом ExteraGram, с какими версиями Telegram internal methods работает hook и на каком потоке вызывается draw callback.
3. Не подтверждены соответствие DEX исходному `Main.kt`, успешность текущего CI и реальное поведение cache/network/storage на Android.
4. DEX получен через pinned SHA и его Git blob hash совпал с `tree.json`; статически проверен только `drawOutline` descriptor. Полное соответствие binary исходному `Main.kt`, runtime-вызов и поведение на host не устанавливались.
5. Нет Swift/Objective-C/Xcode/iOS lifecycle, UI, hook, network/storage или distribution implementation; вопросы iOS неразрешимы этим источником.
6. `force_everywhere` UI setting передаётся в Kotlin, но не влияет на текущий renderer; поведение, подразумеваемое названием настройки, не реализовано в видимом коде.
7. Gradle wrapper JAR отсутствует, а fallback scripts скачивают distribution без видимой проверки checksum; фактический supply-chain/build outcome не проверялся.
