# Независимая проверка: `template-robotiaga`

- **Источник:** `RObotiaga/exteragram-plugin-template`
- **Commit:** `bbf44de36e16c360a3f5afcbc99bc331ac52ebb9`
- **Область:** сохранённый raw snapshot, source page и 40 подготовленных facts; review выполнен по сохранённым данным как данным, без запуска исходника, сборки, тестов и установки.
- **Вердикт:** `accepted-with-gaps`

## Покрытие

Сверены snapshot tree/manifest и контекст радара; прочитаны Python bridge, все **21 Kotlin `.kt` файла** из raw snapshot, Gradle/D8/R8 и host-JAR glue, EAF packer и DEX validators, legacy embed/watch scripts, CI/release workflows, metadata, `justfile`, README/ROADMAP и 15 файлов skill/reference docs. Бинарные host JAR не исследовались как код.

Source page покрывает архитектуру EAF, межслойные reflection signatures и lifecycle, hooks/registries, упаковку, shading/relocation, host JAR подготовку, debug/release gates и документированные ограничения. Исправлена ошибка в ссылке на радар: она теперь ведёт к сохранённому вторичному контексту, а не к несвязанному диапазону README. В coverage исправлено количество Kotlin исходников с 20 на 21.

## Исправления и точности evidence

1. README runtime claim уточнён как **документационное заявление**. ROADMAP для AyuGram 12.9.0 конкретно подтверждает установку EAF/Python UI, но оставляет JVM callback pending с `JVM plugin is not loaded`. Код подтверждает реализацию bridge и failure path, но не успешное исполнение на устройстве. Артефакт, версия сборки и runtime-логи, поддерживающие широкое утверждение README, в snapshot не приведены. Источник и fact `template-robotiaga-035` теперь отделяют `docs`, `code` и фактический статус, не представляя runtime как проверенный.
2. CI synthetic payload с `dex\n035` классифицирован как packaging/layout smoke. Gradle release DEX и статическая runtime-surface проверка запускаются лишь при наличии обоих host JAR; их отсутствие означает skip, а не доказательство полного build. Ни один запуск CI данного SHA независимо не инспектировался.
3. Исправлена ссылка на контекст радара. Сохранил различие между радарной оценкой внешнего `extera-gradle-plugin` и собственным Gradle/D8 pipeline репозитория.
4. В machine facts повторов не обнаружено: **40 записей, 40 уникальных ID и 40 уникальных claims**. Близкие записи описывают разные контрактные поверхности (например, class loading, поиск DEX, порядок init и замену classloader поколения); их объединение потеряло бы отдельные доказательства. Повтор тех же знаний на source page оставлен в контексте разделов, не создаёт дополнительных machine facts.

## Остаточные пробелы

- Runtime bridge на AyuGram 12.9.0 остаётся неподтверждённым по ROADMAP; broad README claim не имеет привязанных к сборке логов/artifact в доступном snapshot.
- Проверка не доказывает, что host JAR соответствуют конкретному APK: бинарные архивы не разбирались и их provenance не установлен.
- Фактические CI/release runs этого SHA не проверялись; описание workflow относится к кодовой конфигурации, а не факту выполнения.
- Часть skill-документации пересказывает внешний SDK/практику и обозначена как docs. Её текущая применимость требует сверки с официальными docs и точным host APK; она не подтверждена одной лишь реализацией шаблона.

Страница и facts приняты с этими ограничениями; review не утверждает runtime readiness или абсолютную полноту неполученных бинарных/upstream материалов.
