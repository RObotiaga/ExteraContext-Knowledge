---
type: comparison
date: 2026-09-28
---

# Версии, форматы плагина и границы совместимости

Эта страница сводит совместимые только в пределах собственного источника сведения о версиях, загрузчиках и артефактах. Одинаковое имя API или метаданных само по себе не устанавливает совместимость между клиентами.

## Версии SDK и клиентов

| Источник | Что заявлено или наблюдается | Как применять |
|---|---|---|
| [Официальная документация SDK](sources/official-sdk.md) | Вводная страница указывает SDK 1.4.4.3, Python 3.11 и exteraGram 12.5.1+. Multi-account требует SDK 1.4.5.0+, Elyx-примеры — 1.4.5.3+. Intents требуют app 12.6.4+. | Проверяйте нижнюю версию каждой используемой возможности, а не полагайтесь только на introductory baseline. Для установленного клиента нужна отдельная runtime-проверка. Доказательства: [baseline](facts.json), [расхождение версий](facts.json). |
| [Официальные Android PySDK builds](sources/official-sdk-builds.md) | Captured release stream содержит 14 snapshots; sdk_version 1.4.3.9, 1.4.4.1 и 1.4.5.0 встречаются в нескольких builds с разными commit/stubs digests. | Используйте version + channel + build + tag + commit. Digest/size подтверждают artifact identity, но не symbol-level API diff. |
| [Публичные docs ExteraGram](sources/exteragram-docs.md) | Snapshot `main` показывает lifecycle examples с `on_load`; отдельно полученный `exteragram-utils` 0.1.3 stub объявляет `on_plugin_load`/`on_plugin_unload`. | Сохраняйте эти версии раздельно: пример документации не подтверждает контракт другого package/stub, и ни один callback не проверялся в runtime. [Сравнение](gaps.md). |
| [for-vibecoders](sources/for-vibecoders.md) | README позиционирует примеры для ExteraGram 12.5.1+ и AyuGram на его основе, но это не тестовая матрица. | Сначала сверяйте фактические сигнатуры и состояние hook cleanup с кодом проекта; пример не доказывает работу на каждом APK. Доказательства: [страница источника](sources/for-vibecoders.md), [обзор проверки](reviews/for-vibecoders.md). |
| [AltyLib](sources/altylib.md) | Однофайловый плагин объявляет минимальную версию клиента 11.9.1. | Это metadata конкретного плагина, не версия Python SDK и не гарантия совместимости других клиентов. Валидатор библиотеки проверяет текстовое наличие нескольких ключей, а не весь manifest. Доказательства: [факты AltyLib](facts/altylib.json). |
| [Kotlin/DEX template n08](sources/template-n08.md) | Python entry объявляет `__min_version__ = 12.1.1`; bridge и host APIs привязаны к snapshot, но независимой матрицы клиентских сборок нет. | Различайте version gate плагина и реально доступные Java-классы целевого APK. Доказательства: [метаданные шаблона](facts/template-n08.json), [проверка](reviews/template-n08.md). |

## Форматы и загрузчики

| Формат | Наблюдаемая модель | Основной риск при переносе |
|---|---|---|
| Single-file Python | SDK разбирает metadata как литералы верхнего уровня и загружает Python-файл; релиз можно доставлять напрямую или через dev server. | Сигнатуры Python callbacks и доступность runtime imports определяются версией клиента. |
| Elyx archive | ZIP с refmap и выбранным entry module; импортёр изолирует локальные модули для плагина и документирует собственный API. | Elyx metadata, валидатор ID, assets, localization и Python loader имеют свои правила; не считать пакет обычным ZIP с тем же single-file контрактом. |
| Kotlin/DEX + Python | В [n08](sources/template-n08.md) Python извлекает встроенный DEX и загружает его через `InMemoryDexClassLoader`; release workflow публикует Python plugin и `classes.dex`. | Reflection использует строковые имена и точные JVM-типы; порядок inject/finalize/eject и cleanup нужно сохранять. |
| Kotlin/DEX + EAF | [RObotiaga template](sources/template-robotiaga.md) описывает EAF package, отдельный bridge и собственный build pipeline. | Независимая проверка подтвердила конфликт README и ROADMAP по callback на AyuGram 12.9.0. Без артефакта и runtime-лога успешное выполнение остаётся неподтверждённым. |
| Native Desktop plugin | Изучены [PLEngine](https://github.com/MrCheatEugene/AyuGramDesktop-PLEngine) (27 проверенных фактов) и [пример](https://github.com/MrCheatEugene/AyuSamplePlugin) (22); оба среза приняты с gaps. | Desktop ABI, native callbacks и потоки не являются Android `BasePlugin` API. Точная версия engine для sample неизвестна; ни один источник не проверялся в runtime. |

## Сходные инструменты решают разные задачи

- [Gradle plugin](sources/gradle-plugin.md) генерирует plugin JAR и DEX и принимает настройки manifest/services. Он не реализует само пользовательское dev server или reload lifecycle. Смотри [границы инструмента](facts/gradle-plugin.json).
- [n08 template](sources/template-n08.md) содержит собственные ShadowJar/BuildDexTask и Python-to-JVM bridge. В данном SHA он не применяет отдельный `extera-gradle-plugin`.
- [exteralib](sources/exteralib.md) — Java CLI для преобразования APK в JAR и изменения версии заголовка class-файлов; его название/описание не означает SDK hooks или сборщик plugin DEX.
- [catalib](sources/catalib.md) включает Python bundler, SDK facade и developer workflow, но README говорит об остановке поддержки и repository metadata указывает archived. Авторы заявляют паритет API; конкретные версии официального SDK отдельно не сравнивались.
- [exteragram-utils 0.1.3](sources/exteragram-utils.md) — отдельный Python package, указанный пользователем как developer utilities. Проверка пакета выделяет Python SDK stubs отдельно от реализованного development CLI; независимый review принят с gaps.
- [ExteraGram MCP](sources/exteragram-mcp.md) — MCP/dev-server tooling для команд и ADB; 81 зарегистрированный инструмент в коде расходится с 76 в README. Это вспомогательный инструмент, не SDK/runtime API плагина.
- [zwylib-docs](sources/zwylib.md) — API reference repository; он описывает вызовы, но не содержит SDK implementation. Не использовать страницу документации как доказательство текущей бинарной или runtime-совместимости.
- [ElyxBuilder](sources/elyxbuilder-shareui.md) и [Kangel fork](sources/elyxbuilder-kangel.md) — tooling для сборки Elyx archives; их builder API и варианты config различаются. Ни один репозиторий не содержит конечный client loader/DSL interpreter, так что собранный archive не подтверждает загрузку клиентом.

## Порядок проверки совместимости

1. Запишите client, platform, SDK version, source SHA и формат entry package.
2. Выпишите именно используемые hooks/callbacks/imports и минимальные версии из источника этих объявлений.
3. Проверьте конечный package: entry, metadata, relocated dependencies, DEX/JAR contents и resources.
4. Отдельно проверьте загрузку, события, аккаунт и выгрузку в целевой сборке. Успешная сборка или чтение исходников не подтверждают runtime.
5. При разногласии README, roadmap и реализации укажите каждое утверждение с источником и оставьте результат неразрешённым, пока нет воспроизводимой проверки.

[Сущности и платформы](entities/index.md) · [Справочник API](apis/index.md) · [Правила разработки](rules.md) · [Пробелы](gaps.md) · [Индекс](index.md)
