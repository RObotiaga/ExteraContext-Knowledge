---
type: source
source_id: exteralib
platform: tool (Java CLI; produces JVM class JARs)
review_status: accepted-with-gaps
review: ../reviews/exteralib.md
date: 2026-09-27
---

# fossSquad/exteralib — извлечение APK и конвертация DEX в JAR

**Источник:** [fossSquad/exteralib](https://github.com/fossSquad/exteralib), снимок `75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a` (`main`, дата захвата 2026-09-27). Код: [Main.java](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java). Лицензия — GNU GPL v3 (`LICENSE`); это не библиотека SDK плагинов, а самостоятельная Java CLI-утилита для подготовки JAR из APK. GitHub description называет репозиторий «exteraGram patcher for building .dex plugins», но в зафиксированном дереве нет сборки плагинов/DEX, patcher-интеграции или SDK-кода: фактически это утилита преобразования.

## Зачем это может понадобиться автору плагина

README обещает извлечь «core classes» ExteraGram, превратить DEX в JAR и изменить версию class-файлов для Java 17. Практическая роль источника ограничена получением потенциального compile-time материала из APK. В снимке нет API для плагинных hooks, entry point, регистрации/выгрузки, загрузчика, доступа к аккаунтам или Telegram UI; нет образца плагина, шаблонов Gradle для потребителя либо определения интерфейса совместимости. Поэтому наличие этого репозитория само по себе не подтверждает, что полученный JAR можно безопасно добавить как `compileOnly` dependency или что он содержит конкретный hook API.

Особенно важно различать заявленное извлечение core-классов и реализацию: `main` передает весь APK аргументом в dex2jar, а затем обрабатывает все записи `.class` во временном JAR. В коде нет фильтрации пакетов, выбора «core» модулей, очистки, исключения Android-классов или специального выбора `classes*.dex`. Результат нельзя считать проверенным минимальным SDK-пакетом.

## Покрытие снимка

| Путь | Что изучено | Ограничение |
|---|---|---|
| `README.md` | Возможности, сборка, CLI usage, credits | Заявления сверены с реализацией ниже; README не доказывает работу на реальном APK |
| `src/main/java/com/exteralib/Main.java` | Вся единственная Java-реализация: аргументы, reflection, zip-конвертация, изменение class header, ошибки | Код не запускался; нет исходника dex2jar в этом репозитории |
| `build.gradle`, `settings.gradle` | Java/application/Shadow plugins, версия, зависимости, main class | Не запускался Gradle и не скачивались зависимости |
| `gradle/wrapper/gradle-wrapper.properties` | Версия Gradle wrapper: 8.14 bin | Wrapper JAR и скрипты перечислены в дереве, но их содержимое не анализировалось: для контрактов библиотеки несущественно |
| `.github/workflows/build.yml` | CI-сборка и публикация артефакта на тегах | Workflow исследован статически; успешный CI на этом SHA не проверялся |
| `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml` | Поля issue-форм | Не описывают технический API |
| `LICENSE` | Полный файл GPL v3 | Вывод только о заявленной лицензии репозитория, не о лицензиях целевого APK или результата конверсии |
| `tree.json`, `snapshot.json`, `radar-context.md`, `radar-urls.json`, `file-manifest.json` | Граница снимка, пути и контрольные суммы, упоминания радара | В контексте радара упоминаний нет; тестовых файлов/папок в дереве нет |

Дерево снимка содержит 23 записи и одну production-реализацию `src/main/java/com/exteralib/Main.java`. Нет `src/test`, Kotlin, Android/Gradle plugin-модуля, DEX-patcher hooks, loader, compiled Telegram classes или инструкций по потреблению результата. `gradle/wrapper/gradle-wrapper.properties` дополнительно получен тем же SHA после первичного снимка; SHA репозитория не менялся. README и repository description являются рекламными метаданными; конкретную поддержку patcher-а нужно искать в другом источнике.

## Реальный CLI и ход обработки

Точка входа — `com.exteralib.Main.main(String[] args)` ([строки 16–55](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java#L16-L55)). Принимается позиционная форма:

```text
java -jar exteralib.jar <input.apk> -o <output.jar-or-directory>
```

Проверяется только `args.length >= 3` и строгое равенство `args[1]` строке `-o`; остальные аргументы игнорируются. Ошибка формата печатает usage и завершает процесс с кодом 1. Нет отдельной валидации расширения APK, существования входа, доступности выходного пути или формата архива до начала обработки.

Если третий аргумент уже является существующим каталогом, к нему добавляется имя входного файла с заменой конечного `.apk` на `.jar`; суффикс проверяется с учетом регистра. Для входа `client.APK` автоматическое имя будет `client.APK.jar`. Для несуществующего пути каталогом его код не считает. Каталог назначения не создается автоматически.

Выход открывается через `Files.newOutputStream` с параметрами Java по умолчанию: существующий файл назначения усекается. При пересоздании архива каждая запись строится только из имени (`new ZipEntry(entry.getName())`), поэтому времена, комментарии и прочие ZIP-атрибуты исходных записей явно не переносятся; содержимое обычных записей копируется, а сжатие создается заново.

Внутри создается временный `.jar`, затем класс dex2jar загружается по имени `com.googlecode.dex2jar.tools.Dex2jarCmd` через reflection: вызываются публичный конструктор без аргументов и `doMain(String[])` с `{"-f", inputApk, "-o", tempJar}`. Это не reflection к API ExteraGram и не обход patcher-а; это способ найти CLI dex2jar во включенной зависимости во время выполнения. При отсутствии класса/конструктора/метода, проблеме конвертации или записи ошибка попадает в общий `catch`, печатается stack trace, процесс завершается с кодом 1. Результат `doMain` не проверяется, как и наличие/валидность промежуточного JAR перед патчингом.

`patchJar(File inputJar, File outputJar)` ([строки 57–90](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java#L57-L90)) читает временный архив через `ZipInputStream`, создает выходной через `ZipOutputStream`, сохраняет имена записей. Для каждой записи с именем, оканчивающимся `.class`, весь байтовый массив читается в память. Если массив не короче 8 байт и первые четыре байта равны `CAFEBABE`, изменяется только байт `classData[7]` на десятичное 61 — младший байт major version; старший байт `classData[6]` и minor version `[4..5]` остаются прежними. Остальные записи копируются буфером 8192 байта. Метаданные записей не переносятся явно: выходные `ZipEntry` создаются только с тем же именем. Это правка заголовка файла класса, а не перекомпиляция и не трансляция байткода на Java 17.

Временный архив удаляется только после успешного `patchJar`; при исключении до этой точки явного cleanup нет. Сообщение `Dex2jar finished` печатается сразу после reflection-вызова, оно не является доказательством успешного преобразования. Сообщение `Success!` появляется после копирования и удаления временного архива.

## Контракты вызовов и lifecycle

| Модуль / класс | Сигнатура или фактический вызов | Назначение | Lifecycle / поток / аккаунт | Доказательство |
|---|---|---|---|---|
| CLI / `com.exteralib.Main` | `public static void main(String[] args)` | Проверить минимум аргументов и `-o`, разрешить имя выходного файла, оркестрировать одноразовую конвертацию | Отдельный JVM process; синхронно на main thread; понятия Telegram account нет | [Main.java:16–55](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java#L16-L55) |
| Dex2jar runtime bridge | `Class.forName("com.googlecode.dex2jar.tools.Dex2jarCmd")`; `getDeclaredConstructor().newInstance()`; `getMethod("doMain", String[].class)`; `invoke(..., (Object) new String[]{"-f", inputApk, "-o", tempJar})` | Вызвать встроенный dex2jar CLI рефлексивно и получить промежуточный JAR | Внутри CLI-процесса, синхронный вызов; API dex2jar 2.4.28 по dependency declaration | [Main.java:33–53](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java#L33-L53), [build.gradle:20–25](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/build.gradle#L20-L25) |
| ZIP-конвертация / `Main.patchJar` | `private static void patchJar(File inputJar, File outputJar) throws Exception` | Копировать записи dex2jar JAR и менять младший байт major версии валидных `.class` на 61 | Однократная синхронная работа; класс целиком буферизуется в heap; аккаунт/клиентный lifecycle отсутствуют | [Main.java:57–90](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java#L57-L90) |
| ZIP-чтение / `Main.readAllBytes` | `private static byte[] readAllBytes(InputStream is) throws Exception` | Читать текущую запись ZIP блоками по 8192 байта в `ByteArrayOutputStream` | Синхронно, без предела размера отдельного класса | [Main.java:92–100](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java#L92-L100) |

Это CLI, а не DEX-patcher API. В исходнике отсутствуют hook annotations/classes, patcher interface, регистрация callback-ов, plugin metadata/entry point, load/unload/enable lifecycle, методы Telegram UI или reflection-доступ к классам Telegram. Нельзя заимствовать из этой страницы сигнатуру hook-а: ее здесь нет.

## Сборка и dependency isolation

`build.gradle` применяет Gradle `java`, `application` и Shadow plugin `8.1.1`; group `com.fossSquad`, version `1.0-SNAPSHOT`, source/target compatibility Java 17, main class `com.exteralib.Main`. Репозитории — Maven Central и Google. Единственная явно объявленная application dependency — `de.femtopedia.dex2jar:dex-tools:2.4.28` в `implementation`. Wrapper настроен на Gradle `8.14-bin`.

README и CI собирают `shadowJar`, ожидаемый путь — `build/libs/exteralib-1.0-SNAPSHOT-all.jar`. Это объясняет, как CLI получает dex2jar в fat JAR, но в `build.gradle` нет правил Shadow relocation (`relocate`), исключений, minimization или classpath-разделения. Поэтому README-формулировка «embeds dex2jar» подтверждается dependency + Shadow-сборкой как намерение, но фактический собранный архив не исследован. Reflection используется для runtime-поиска dex2jar CLI, однако не делает dependency optional: без класса выполнение падает.

Сборка предназначена для Java-инструмента на JVM. В снимке нет Android Gradle Plugin, Kotlin plugin/compiler, SDK/target SDK, Java source set для плагина, D8/R8 шагов или сборки `.eaf`. Упоминание Java 17 относится к classfile major 61 в выходном JAR и к сборке самой утилиты, а не к гарантированной совместимости любого плагина с Java 17/Android runtime.

CI запускается на Ubuntu, устанавливает Temurin JDK 17, вызывает `./gradlew shadowJar`, копирует fat JAR в `exteralib.jar`, загружает artifact; на push тегов `v*` дополнительно публикует GitHub Release через `softprops/action-gh-release@v2`. Файл фиксирует лишь workflow; факт успешного исполнения CI на SHA `75edeba…` здесь не проверялся.

## Сверка README: заявления против кода

| Заявление README | Что подтверждает реализация | Практическое уточнение |
|---|---|---|
| «Автоматически извлекает core classes» из любого APK | Код передает `inputApk` в dex2jar, затем пишет записи полученного JAR | В коде нет выборки core-пакетов, очистки или списка поддерживаемых APK. Слово «любой» тестами не подтверждено. |
| DEX → JAR через dex2jar | Зависимость `dex-tools:2.4.28` объявлена и CLI вызывается reflection | Реальная конвертация конкретного APK не запускалась; code path опирается на конкретные class/method имена dex2jar. |
| «Java-17 compatible» / меняет major version | Для записи `.class` с magic `CAFEBABE` байт 7 становится `61` | Не проверяется валидность после изменения; не меняется API/байткод/зависимости/Android framework; это не гарантия компилируемости или запуска. |
| Один исполняемый JAR | Gradle Shadow plugin и CI ожидают `*-all.jar` и копируют его | Репозиторий не содержит собранный бинарник в изученном дереве; сборка не выполнялась. |

## Приемы применения и осторожности

Если использовать инструмент для подготовки compile reference, сначала соберите его согласно README на JDK 17 и обработайте APK нужной версии клиента, сохраняя связь JAR с точной версией/сборкой APK. Затем независимо проверьте содержимое архива: какие пакеты/классы реально попали, не нужны ли Android/Telegram зависимости отдельно, компилируется ли минимальный тестовый плагин против нужных символов и соответствует ли тип/сигнатура актуальному patcher SDK. Эти проверки в репозитории не автоматизированы и здесь не выполнялись.

Не используйте версию classfile 61 как доказательство, что dex2jar output «стал Java 17». Изменение заголовка не добавляет методы Java 17 API и не исправляет ссылки на классы Android. Для конкретной сборки необходимо проверять исходную и целевую среду, classpath и поведение patcher/loader. Также отдельно учитывайте GPL v3 проекта; исходник не определяет правовой режим перераспространения APK или его декомпилированных классов.

## Лицензия, тесты и уверенность

README указывает GNU GPL v3 и корневой `LICENSE` содержит текст GNU General Public License version 3. В дереве отсутствуют автоматические тесты. Никакой чужой код не запускался, Gradle не запускался, APK не конвертировался, скомпилированный JAR не проверялся, установка плагина и работа hooks не проверялись. Все описания исполнения выше — анализ исходного кода (`code`) либо пересказ документации (`docs`), не `runtime-verified`.

Уверенность высокая для поведения, непосредственно видимого в единственном `Main.java` и Gradle/CI-файлах; низкая/отсутствует для практической совместимости выходного JAR с конкретным ExteraGram/AyuGram patcher: в снимке нет SDK и нет результатов запусков. В переданном радарном контексте для `exteralib` упоминаний нет, поэтому противоречия радару не выявлены.
