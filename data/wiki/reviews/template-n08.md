---
type: review
source_id: template-n08
review_status: accepted-with-gaps
date: 2026-09-27
---

# Независимая проверка: exteraStuff/pydex-plugin-template

- Вердикт: **accepted-with-gaps**.
- Проверенный снимок: `exteraStuff/pydex-plugin-template`, SHA `435425db4436927185534e1e06111a6a22aa1740`, alias исходного запроса `n08i40k/exteragram-plugin-template`. Загружено 47 файлов по `file-manifest.json`; полный tree содержит 74 записи с директориями. Исследование кода не запускало plugin, Gradle/just/uv recipes, workflow, тесты, установку или устройство; выводы являются статическим просмотром исходников, не runtime evidence.
- Назначение и границы radaра сверены по `raw/template-n08/radar-context.md` и `radar-urls.json`: Python/BasePlugin точка входа с Kotlin/DEX backend; интерес для DEX toolchain; упоминание внешнего `extera-gradle-plugin`. README, `build.gradle.kts` и `BuildDexTask.kt` показывают собственные `ShadowJar` и `BuildDexTask`, прямой вызов R8; claims о применении внешнего Gradle plugin к этому SHA не подтверждаются.

## Независимое покрытие

По `tree.json` и `file-manifest.json` перечитаны целевые текстовые файлы: `README.md`, `justfile`, `exteragram-plugin-template.py`, `build.gradle.kts`, `buildSrc/build.gradle.kts`, `buildSrc/src/main/kotlin/BuildDexTask.kt`, `gradle.properties`, `gradle/libs.versions.toml`, `gradle/wrapper/gradle-wrapper.properties`, `proguard-rules.pro`, `settings.gradle.kts`, `scripts/prepare_release.py`, `tools/embed_dex.py`, `tools/dev_watch.py`, `tools/FixTelegramJar.java`, `.gitattributes`, `.gitignore`, `.python-version`, `pyproject.toml`, `uv.lock` (для lockfile проверены верхние metadata/declarations, не весь транзитивный inventory), `.github/workflows/release.yml`, `LICENSE`, обе i18n properties и все Kotlin-файлы `src/main/kotlin/ru/n08i40k/template/**` (Plugin, action handlers/constants, registries, hooks, eject notifier, locale/i18n, Throwable и UI/thread/reflection/logger utilities). `gradlew`, `gradlew.bat` просмотрены поверхностно; `gradle-wrapper.jar` не анализировался как бинарный файл.

Охват соответствует небольшому шаблону: Python→JVM reflection bridge signatures/types, декодирование/загрузка embedded DEX и parent classloader, параллельность load/eject и меж-classloader rendezvous, реестры callback, hooks и централизованный unhook, scope/refcount/UI thread, menu/settings integration, storage/account limitation, R8 inputs/modes/output, classpath merge/first duplicate wins, shading exclusions, keep rules, host jar preprocessing, just tasks, dev watcher, release metadata/workflow, toolchain pins и диагностика. Публичные bridge-вызовы сопоставлены между Python и Kotlin: `getBuildDate()`, `inject(String, ValueCallback)`, `finalizeInject()`, `invokeChatContextMenuCallback(String, long)`, `invokeSettingsActionCallback(String)`, `eject()`; Python передает `String`/`ValueCallback` class tokens и primitive `Long.TYPE` в соответствии с Kotlin декларациями.

## Исправления и уточнения

- Добавлены 5 новых уникальных фактов: одноразовый inject на classloader; потенциальный cleanup gap, когда Python load failure обнуляет bridge, не вызывая Kotlin eject; асинхронность `on_plugin_unload`/`Plugin.eject`; debug `BUILD_TIME=0`; и side effects ручного Release workflow (push metadata commit, tag и release).
- В существующем факте о toolchain добавлена конкретная версия Gradle wrapper `9.1.0`. Таблица покрытия исправлена: первоначальный набор raw не содержал justfile и ряда релевантных текстовых конфигов; они отдельно получены по путям из tree с сохранением SHA манифеста. README claim об LFS Telegram JAR теперь подтвержден `.gitattributes` (`libs/Telegram.jar`); wrapper properties проверены, wrapper JAR нет.
- Сверены R8 program/classpath/library inputs, режимы debug/release, `-ignorewarnings` для unresolved warnings и `DexIndexed`; Gradle классы AndroidX из `compileOnly` исключены из relocation вместе с указанными отдельными классами. Фактическая debug дата сборки не содержится в `getBuildDate()`.
- Review выявил lifecycle риск из веток исключений Python: `_run_plugin_load` делегирует Python `on_plugin_eject`, который не вызывает JVM `eject`. Это зафиксировано как inference и требует runtime проверки до вывода о проявлении; страница не говорит, что такой сценарий воспроизводился.

## Дубликаты и остаточные пробелы

В facts JSON после правок **37 уникальных фактов с 37 уникальными ID**; внутристраничных дублей нет. Поиск по source/topic pages нашел тематическое пересечение с отдельным форком [RObotiaga/exteragram-plugin-template](../sources/template-robotiaga.md), а также со сторонним Gradle plugin. Это независимые репозитории/версии с собственными контрактами, поэтому не объединять их факты в этой source page; для будущего синтеза использовать канонические темы `build`, `lifecycle`, `hooks`, `threading` и отдельно сохранять provenance/SHA каждого источника.

Остались runtime gaps по фактической загрузке в exteraGram/AyuGram, достижимости ветки cleanup failure, reflection behavior на конкретных APK, UI и hook совместимости, работе host `compileOnly` классов, результате R8 и device watcher. Не проверялись полная транзитивная детализация `uv.lock`, бинарный Gradle wrapper JAR, GitHub Actions execution и внешний `extera-gradle-plugin`; эти границы не позволяют считать проверку runtime или гарантировать совместимость с текущими клиентами.
