# Независимая проверка: `av1-decoder`

- **Источник:** `stxlvn/exteragram-av1-sw-decoder`, pinned commit `6367bdcabbf2f7b4b08baa133284f4f122927947` (`main` на момент снимка 2026-09-27 15:47:45 UTC).
- **Область:** независимо прочитаны весь `README.md` (50 строк) и весь `av1_sw_decoder.plugin` (853 строки); сверены `tree.json`, `snapshot.json`, двухфайловый `file-manifest.json`, repository metadata, `radar-context.md` и пустой `radar-urls.json`. README и source целиком входят в captured files. Полное дерево содержит ещё `.gitignore` (19 байт), но его содержимое в capture не сохранено и не проверялось. Исходный код, SDK, тесты, release artifact или приложение не запускались, не собирались и не устанавливались.
- **Вердикт:** `accepted-with-gaps`.

## Независимое покрытие

README покрыт целиком: назначение и установка, режимы качества, ограничения разрешения, dav1d/HEVC переключатели, диагностика/privacy summary и перечисленные hooks. Source проверен от imports/metadata до последней строки: inventory system MediaCodec и классификация, quality filtering, Telegram/ExoPlayer/Media3 reflection hooks, error/fallback policy, trace callbacks, timer/worker lifecycle, настройки, redaction и обе сетевые отправки, ручной SDK source dump.

Текущие SHA-256 файлов побайтно совпадают с обеими записями manifest: `README.md` — `3bcd92529efd7b658ecec16781922a111ff621d1056d8b5b6f4fe4d8476d0453`; `av1_sw_decoder.plugin` — `c4498d215a140a85ff77c1ad2def6402d5da8be14e33dce22c13e6b0fdf70bf8`. SHA в manifest, snapshot, tree и pinned permalinks совпадает. Tree не truncated; в нём три blob: `.gitignore`, README и `.plugin`. GitHub repository metadata имеет `license: null`, а license file в tree нет.

Функции из радара сверены с первоисточниками: это готовый ExteraGram plugin/deep-hook пример для выбора уже зарегистрированных системных кодеков. Он не реализует AV1 decoder и не является plugin SDK. Metadata заявляет минимумы ExteraGram и SDK, но в capture нет SDK implementation и нет проверки совместимости с реальным клиентом. Все API-таблицы оставлены как call-sites самого plugin, а не спецификация SDK. README claims отделены от source facts; статическое чтение не названо runtime verification.

## Исправления и точность

- Исправлена ошибка учёта дерева: ранее source page и fact утверждали, что в полном tree только README и `.plugin`. Фактически tree включает ещё `.gitignore`; двухфайловым остаётся именно content manifest. Page и fact теперь различают полный tree и захваченные файлы.
- В frontmatter source page поставлены `accepted-with-gaps` и ссылка на этот отчёт.
- Уточнён Android 10+ claim. Это указано README и повторено текстом warning в UI, но код не имеет API 29 minimum guard и динамически сканирует codecs. Наличие AV1 на конкретном Android 10 device из исходника не выводится.
- Явно разделены заявления о производительности: README предупреждает о software decode высокого разрешения на слабом CPU; UI говорит, что dav1d обычно быстрее libgav1. В коде подтверждается только ordering по имени, benchmark и throughput data нет.
- Уточнено, что `onCodecInitialized` логирует codec без AV1 MIME-фильтра, поэтому этот callback не доказывает именно AV1 initialization. Флаг `sw_failed` сбрасывается при новом `on_plugin_load`, в том числе при reload plugin.
- Дополнены machine facts: уникальных ID **28**, повторов ID нет. Общие границы Android floor и README claim разнесены, чтобы один факт не выдавался за независимые подтверждения.

## Повторы и canonical topics

Поиск по другим source pages, API/topics/recipes и общему facts JSON не обнаружил второго источника, уже описывающего этот AV1/MediaCodec механизм; повторы fact IDs внутри `av1-decoder-facts.json` отсутствуют. Единственная смежная запись — вторичная ссылка в `wiki/sources/radar.md`, где говорится, что детали decoder/API надо подтвердить по исходнику; она не дублирует проверенные здесь контракты. Для будущего тематического синтеза подходят `media` (codec discovery/order/fallback), `portability` (client metadata и per-device availability), `hooks`/`lifecycle` (reflection/reload), `network`/`security` (диагностика и SDK dump). Общий index и другие source pages не менялись.

## Остаточные пробелы

- Содержимое `.gitignore` не захвачено; проверены только наличие и размер tree entry. Его ignore patterns и возможное влияние на release/package workflow не установлены.
- Нет ExteraGram SDK и Telegram/Media3 implementation: не подтверждены сигнатуры и внутренние поля на реальных версиях клиента; private `enableDecoderFallback` и reflective hooks могут зависеть от build.
- Не подтверждены Android 10 универсальность и наличие codec на устройстве, скорость/качество декодирования, преимущество dav1d, поведение reload/hook cleanup или результат воспроизведения.
- Release artifact, упаковка/воспроизводимость, CI, tests и build instructions в полном tree отсутствуют. Нельзя проверить README install flow.
- Network endpoint, фактическая передача/хранение данных, backend contract и содержимое ответов не проверялись. SDK dump отдельно отправляет module paths/source без обычной redaction.
- GitHub metadata не объявляет лицензию и license file в pinned tree отсутствует; лицензионные условия по этому снимку определить нельзя.

Этот вердикт означает, что сведения доступных двух source/doc файлов сверены и пригодны для статической справки; он не гарантирует поведение недоступного SDK, клиента, release package или устройства.
