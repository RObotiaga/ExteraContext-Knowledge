---
type: review
source_id: exteralib
review_status: accepted-with-gaps
reviewed_sha: 75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a
date: 2026-09-27
---

# Независимая проверка fossSquad/exteralib

## Объём

Проверен снимок `fossSquad/exteralib` на SHA [`75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a`](https://github.com/fossSquad/exteralib/tree/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a). `snapshot.json` указывает `tree_truncated: false`; весь tree содержит 23 пути. `radar-context.md` и `radar-urls.json` проверены: для этого slug радарных упоминаний нет.

Самостоятельно прочитаны README, вся единственная реализация `src/main/java/com/exteralib/Main.java`, `build.gradle`, `settings.gradle`, `gradle/wrapper/gradle-wrapper.properties`, `.github/workflows/build.yml`, обе issue templates и `LICENSE`. Сверены `tree.json`, `file-manifest.json`, `repository.json`, `snapshot.json`, `radar-context.md` и `radar-urls.json`. Wrapper JAR/скрипты и прочие служебные файлы дерева не анализировались как не относящиеся к пользовательскому контракту; в дереве нет иных Java/Kotlin исходников, тестов, SDK или плагинных модулей.

## Независимое покрытие и исправления

- Подтверждён фактический объём проекта: одноразовый Java CLI вызывает `Dex2jarCmd` через reflection, затем переписывает ZIP/JAR записи и байт версии у валидных `.class`; кода сборки `.dex` плагина, hooks SDK, entry point, loader или lifecycle API в полном дереве нет. GitHub description и README рассматриваются как заявления проекта, а не как доказательство такого API.
- Перепроверены аргументы CLI и разрешение имени результата, reflective invocation и dependency version, игнорирование результата вызова dex2jar, поведение временного файла при ошибках, обработка ZIP-записей и classfile header, память для отдельного класса, Java/Shadow-конфигурация, wrapper, workflow и release trigger.
- Добавлено в source page и facts JSON: `Files.newOutputStream` без опций усекает существующий output-файл; родительский каталог не создается. Также отражено, что выходные `ZipEntry` строятся только из имени: дополнительные ZIP-атрибуты явно не копируются.
- Проверена сверка README с кодом: «core classes», «любой APK» и «Java-17 compatible» не подтверждены как гарантии реализации. Код не содержит выбора core-пакетов; он передает APK dex2jar и пропускает полученные `.class` через изменение заголовка. Документационное обещание single executable JAR сопоставлено с Shadow/CI конфигурацией, но собранный бинарник не исследовался.
- Исправлены frontmatter источника: статус `accepted-with-gaps` и ссылка на этот отчет. Итоговый JSON записан в `C:\Users\sofar\Documents\Codex\2026-09-27\g\work\exteralib-facts.json` и содержит **19 уникальных фактов** с уникальными ID.

## Дубликаты и канонические темы

Внутри страницы повторов, требующих удаления, не найдено. JSON IDs уникальны; близкие факты описывают разные контракты (позиционные аргументы, reflection-вызов, classfile rewrite, выходной путь, ZIP-метаданные, сборка и CI) и сохранены раздельно. При будущей тематической сводке объединять по темам CLI/output handling, DEX-to-JAR conversion, classfile compatibility, build/distribution и отсутствие plugin lifecycle API; один вывод о границах проекта не дублировать в каждом разделе.

## Остаточные пробелы

- Не запускались проект, Gradle, сторонние программы или загруженный код; APK не конвертировался, output JAR не инспектировался и не проверялся в компиляторе или клиенте.
- Не проверялись успешный GitHub Actions run на этом SHA и совместимость конкретного результата с версией ExteraGram/AyuGram. В снимке нет SDK/patcher, которым такую совместимость можно было бы подтвердить.
- `dex-tools` изучен по dependency declaration и используемому reflection-контракту, но его исходники и фактический fat JAR не анализировались. Поэтому успешность reflective invocation и полнота dependency packaging остаются не runtime-проверенными.
- Документационные обещания и наличие GPL-3.0 license-файла сами по себе не устанавливают совместимость либо права на распространение стороннего APK и его декомпилированных классов.

## Вердикт

**accepted-with-gaps** — статическое описание исходника и конфигурации подтверждено, а пропущенные операционные детали добавлены. Остаточные ограничения касаются отсутствующей runtime-проверки и неизвестной совместимости выходного JAR с конкретным клиентом; отчет не утверждает, что инструмент запускался или прошел тест.
