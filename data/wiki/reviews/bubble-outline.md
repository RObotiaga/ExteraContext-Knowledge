---
type: review
source_id: bubble-outline
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: xwwvv/ios-bubble-outline

- Вердикт: **accepted-with-gaps**.
- Snapshot: `15355c3affe1b41fd9551014c50ed893d3fd4f4c` (`main`), сохранён 2026-09-27; pinned SHA совпадает в `snapshot.json`, `tree.json` и ссылках source page.
- Радарный контекст и пустой `radar-urls.json` сверены отдельно. Радар описывает проект как DEX/ExteraGram пример и визуальную стилизацию пузырей «в сторону iOS»; это не свидетельство native iOS реализации.
- Прочитаны весь Python entrypoint `BubbleOutline.plugin`, Kotlin `Main.kt`, Gradle module/root/settings/properties/wrapper configuration, checked-in `gradlew` и `gradlew.bat`, manifest, workflow, версии, сохранённый artifact manifest и полное дерево. Все 14 исходно сохранённых текстовых файлов совпали с их SHA-256 и размерами в manifest. В snapshot tree 29 записей, `truncated=false`; blob DEX получен отдельным запросом к закреплённому SHA, его размер, manifest SHA-256 и Git blob SHA проверены. `gradle-wrapper.jar` и `telegram-stubs.jar` в дереве отсутствуют.
- DEX не загружался в Android, не исполнялся и не собирался. Только статически разобран его method proto: единственный `Main.drawOutline` имеет descriptor `(...;Ljava/lang/String;FIZ)V`, то есть последние параметры — primitive `float`, `int`, `boolean`. Полный bytecode и соответствие всей Kotlin реализации бинарному артефакту не проверялись.

## Покрытие и сверка

Проверены все относящиеся к реализации и интеграции части небольшого репозитория: metadata и SDK/app gates; plugin load, cache/network, class loading, hook, retry и callback; settings и reflection bridge; Kotlin geometry, color/alpha/width/radius, mutable `Paint`/`RectF`, exception handling; Gradle toolchain и D8 task; stubs; wrapper bootstrap; CI trigger, build, artifact generation/push; версия и опубликованный DEX; отсутствие docs/tests/license и iOS-native файлов. В source page отражено, что `force_everywhere` передаётся, но не используется, и что у класса плагина нет собственного unload callback. Внешние base-plugin/hook helpers и host API в snapshot отсутствуют, поэтому их контракты не приписаны проекту.

Имя `ios-bubble-outline`, `__name__ = "iOS Bubble Outline"` и описание радаром iOS-стилизации не меняют платформу реализации: entrypoint использует ExteraGram Python APIs и Android Telegram classes, Kotlin рисует через Android `Canvas`, сборка создаёт DEX. В закреплённом tree нет Swift/Objective-C/Xcode/iOS packaging. Следовательно, статус source — Android; выводов о native iOS API здесь нет.

Точная reflection signature разобрана по обеим сторонам. Python передаёт `Class` для `java.lang.Float`, `java.lang.Integer`, `java.lang.Boolean`; Kotlin source объявляет non-null `Float`, `Int`, `Boolean`; pinned DEX подтверждает primitive descriptor `FIZ`. `getDeclaredMethod` требует точные типы, поэтому если `find_class` возвращает обычные классы с указанными boxed именами, поиск метода не совпадёт. Код `find_class` и Java bridge host SDK отсутствуют, поэтому этот последний шаг остаётся `inference`, а не доказанным runtime результатом. Проверка версии artifact также ограничена: plugin metadata/log — `1.0.3`, `version.txt`/`actual.json` — `1.0.0`, Kotlin `Main.version()` возвращает `1`; бинарный DEX нельзя считать соответствующим текущему source только по соседству в tree.

## Исправления и facts

Переданная версия содержала 26 facts. После проверки JSON содержит **29 фактов с 29 уникальными ID**. Добавлены три недостающие developer-facing детали: отсутствие unload/cancel path в классе и предел retry; подавление renderer exceptions и однократная диагностика Python bridge; отсутствие wrapper JAR и собственный download fallback Gradle 8.10.2 без видимой checksum-проверки. Fact о версии дополнен Kotlin `Main.version()`; build toolchain дополнен Gradle Wrapper version. Reflection fact оставлен `inference`, но обновлён по фактическому pinned DEX proto с чёткой границей неизвестного helper/runtime.

Пограничные claims о mutable DEX URL, выборе непустого cache и проверке целостности payload оставлены раздельными: это разные решения (идентичность upstream источника, поведение cache и integrity перед class loading), а не дубли факта. Внутри JSON повторяющихся ID нет. Пересекающиеся темы UI/platform/version в source page сопровождают разбор конкретных call sites и итоговые gaps; отдельные факты не смешивают iOS inference с Android code.

Исправлены в `wiki/sources/bubble-outline.md` и `work/bubble-outline-facts.json`: уточнено, что конкретно подтверждает/не подтверждает DEX; добавлен проверенный primitive method proto; зафиксированы `Main.version()`, wrapper fallback, отсутствие unload cleanup и error visibility; смягчено утверждение о reflection failure с учётом отсутствующего определения `find_class`; разделены network, cache и integrity claims. Frontmatter source теперь содержит `review_status: accepted-with-gaps` и ссылку на этот review.

## Остаточные gaps

1. Не исследованы реализации `BasePlugin`, `MethodHook`, `find_class` и host Java/Python bridge; поэтому unload semantics, hook priority/thread, runtime class-token mapping и lifecycle framework behavior неизвестны.
2. Reflection conclusion не проверялся вызовом на устройстве. Статический DEX descriptor точен для pinned artifact, но результат именно `find_class(...)` в ExteraGram может установить только чтение соответствующего host helper или runtime-проверка.
3. Не анализировался полный DEX bytecode и его соответствие всему `Main.kt`; наличие blob или `actual.json` не доказывает успешную публикацию/сборку CI.
4. Не проверялись Telegram/ExteraGram versions, `ChatMessageCell` symbols, поток hook, UI settings, storage policy, cache/network behavior и визуальный результат.
5. Нет документации, тестов, test fixtures, license file или license metadata в pinned tree/repository snapshot; права использования по этому источнику не установлены.
6. Источник не содержит native iOS implementation, поэтому iOS lifecycle, UI, hook, packaging и переносимость остаются за границей доступных доказательств.

Это статическая проверка конкретного pinned snapshot, не runtime acceptance и не гарантия поведения внешнего host SDK или иных версий репозитория.
