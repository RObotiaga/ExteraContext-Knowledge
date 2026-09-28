---
type: code
source_id: ayugram-desktop
platform: Desktop
review_status: accepted-with-gaps
review: ../reviews/ayugram-desktop.md
date: 2026-09-28
---

# AyuGram Desktop: ограниченные seams для plugin UI

- Репозиторий: [AyuGram/AyuGramDesktop](https://github.com/AyuGram/AyuGramDesktop)
- Закреплённая версия: ветка `dev`, commit [`db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a`](https://github.com/AyuGram/AyuGramDesktop/tree/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a), снимок от 2026-09-27.
- Лицензия: GitHub API возвращает `NOASSERTION`/`Other`; корневой `LICENSE` сохранён, но его условия отдельно не классифицировались. Проверяйте сам файл и upstream перед переносом кода.
- Роль: крупный C++/Qt fork Telegram Desktop. В этой записи исследованы только Ayu-specific metadata/info UI, settings builder и context-menu точки, связанные с упоминанием AyuGram Desktop PLEngine в радаре.
- Это не руководство по PLEngine и не подтверждение публичного plugin SDK. Найденные ниже объявления — часть самого клиента; они не доказывают, что внешний плагин может их вызывать.
- Snapshot, полный tree, входные README, выбранные исходники и SHA-256-манифест сохранены в `raw/ayugram-desktop/`.

## Покрытие

| Прочитанные пути | Что подтверждено | Пропуски |
|---|---|---|
| `snapshot.json`, `tree.json`, `repository.json`, `file-manifest.json`, `radar-context.md`, `radar-urls.json`, `files/README.md`, `files/README-RU.md`, `files/LICENSE` | Идентичность снимка, дерево, GitHub license metadata, README claims и конкретное утверждение радара от 6 сентября | `radar-urls.json` пуст; README описывает продукт, но не раскрывает plugin API; LICENSE сохранён, но не анализировался построчно |
| `Telegram/SourceFiles/ayu/ui/boxes/plugin_info_box.h`, `plugin_info_box.cpp` | C++-структура метаданных, ограниченный парсер, проверки ID/name, UI показа описания/иконки | Не прослеживались все caller’ы и весь plugin loading/runtime; эта пара файлов подтверждает UI/metadata seam, а не исполнение плагина |
| `Telegram/SourceFiles/ayu/ui/settings/ayu_builder.h`, `ayu_builder.cpp`, `settings_ayu.h`, `settings_ayu.cpp`; `Telegram/SourceFiles/ayu/ayu_settings.h/.cpp`, `ayu_state.h/.cpp`, `ayu_infra.h/.cpp` | Внутренний builder компонентов настроек, его использование, хранилище настроек и startup helpers Ayu | Не является host API внешних расширений; прочитаны выбранные Ayu файлы, не весь Settings framework |
| `Telegram/SourceFiles/ayu/ui/context_menu/context_menu.h`, `context_menu.cpp`, `ayu_settings.h`, `ayu_settings.cpp` | Внутренние действия peer/message menus и настройка видимости через modifier | Это статические call-sites клиента; полный upstream menu framework и integration callers вне охвата |

Файлы получены по URL с commit SHA из snapshot. Дерево содержит 6 673 entries; из 17 выбранных файлов были сохранены README/LICENSE и указанные C++-файлы. В приложении, сборке и tests ничего не запускалось. Runtime проверки не было.

## Что подтверждает исходный код

### Метаданные плагина и их граница

`Ui::PluginMetadata` содержит `id`, `name`, `description`, `author`, `version`, `icon`, `minVersion` и `requirements` (`plugin_info_box.h:19-28`). Публично объявлены `ParsePluginMetadata(const QByteArray&)` и `ShowPluginInfoBox(SessionController*, pluginPath, metadata)` (`plugin_info_box.h:30-35`). Имена полей сами по себе не задают ABI, способ загрузки, зависимости или поддерживаемую версию PLEngine.

Реализация `ParsePluginMetadata` читает `__id__`, `__name__`, `__description__`, `__author__`, `__version__`, `__icon__`, `__min_version__` и `__requirements__` из текста; `ExtractField` использует регулярные выражения для заключённых в кавычки значений, включая многострочные формы, а не запускает Python (`plugin_info_box.cpp:45-78,438-457`). Парсер ограничивает длину некоторых display fields, подставляет version `1.0`, требует ID по regex `^[a-zA-Z][a-zA-Z0-9_-]{1,31}$` и непустое имя; иначе возвращает пустую структуру (`plugin_info_box.cpp:441-474`). Это подтверждённая логика чтения метаданных, но отсутствие в этой функции dependency/version enforcement не доказывает, что таких проверок нет в других не изученных call-sites.

`requirements` из этой metadata-проекции лишь разделяются по запятым, обрезаются и сохраняются в QStringList; из этого кода нельзя выводить установку или разрешение зависимостей (`plugin_info_box.cpp:449-457`). `ShowPluginInfoBox` показывает box для `SessionController`, пути и metadata; при указанной иконке ожидается форма `shortName/index`, затем запрашивается sticker set. Это UI-обработка иконки и сведений, не контракт API плагина (`plugin_info_box.cpp:477-523`).

Описание обрабатывает `**bold**` и Markdown-подобные `[label](url)` ссылки. URL проходят `Ui::InputField::IsValidMarkdownLink`; обычный текст дополнительно парсится на ссылки и упоминания (`plugin_info_box.cpp:83-131`). Для автора описания это означает, что текущий UI содержит узкую совместимость с такой разметкой; не следует считать её полной реализацией Markdown.

### Внутренний builder настроек

`Settings::AyuBuilder::AyuSectionBuilder` принимает `Builder::SectionBuilder&` и предоставляет `base()`, `addSettingToggle`, `addToggle`, `addCollapsibleToggle`, `addChooseButton`, `addSlider`, badge/divider helpers (`ayu_builder.h:14-90`). Это удобно как локальный C++-образец построения Ayu settings screen. `settings_ayu.cpp` создаёт его рядом с базовым builder и вызывает `addSettingToggle` из функций построения разделов (`settings_ayu.cpp:638-687`); код относится к внутренней странице настроек клиента.

У `addToggle` начальное значение берётся через getter и передаётся builder’у как `rpl::single(initialValue)`; поток изменения фильтруется сравнением с getter и вызывает setter только при различии, а подписка привязана к `button->lifetime()` (`ayu_builder.cpp:66-93`). `addSettingToggle` адаптирует typed getter/setter на singleton `AyuSettings` к общему toggle builder (`ayu_builder.cpp:46-64`). Это паттерн для UI клиента с lifecycle-owned subscription, не доступный автоматически стороннему `.plugin`.

### Внутренние точки добавления context menu

В `context_menu.h` экспортированы C++ helpers для peer- и message-menu действий, например `AddAyuGramActions(PeerData*, Data::Thread*, SessionController*, PeerMenuCallback)` и `AddCreateFilterAction(PopupMenu*, SessionController*, HistoryItem*, selectedText)` (`context_menu.h:22-54`). Реализация `AddAyuGramActions` проверяет `peerData`, наличие включённых filters/сохранения удалённых сообщений, вычисляет forum topic/root ID и передаёт callback submenu в `PeerMenuCallback`; пункты выполняют конкретные client settings/navigation действия (`context_menu.cpp:250-324`). Это практический seam только для модификации/сборки клиента. Он не подтверждает runtime registration API для сторонних плагинов.

`needToShowItem(ContextMenuVisibility)` показывает item всегда для `Visible`, а для `VisibleWithModifier` — только при зажатом `base::IsExtendedContextMenuModifierPressed()` (`context_menu.cpp:245-248`). Call-sites проверяют это перед созданием действий (`context_menu.cpp:518-575,786-803,983-1000`); это пример условного раскрытия UI, а не plugin hook.

## API и call-sites из исследованных файлов

| Модуль/класс | Сигнатура или call-site | Назначение и границы lifecycle | Доказательство |
|---|---|---|---|
| `Ui::PluginMetadata` | поля `id/name/description/author/version/icon/minVersion/requirements` | Модель отображаемых plugin metadata; структура сама по себе не задаёт сериализационный ABI | [plugin_info_box.h](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/boxes/plugin_info_box.h#L19-L28) |
| `Ui` | `ParsePluginMetadata(const QByteArray&) -> PluginMetadata` | Синхронное извлечение метаданных из bytes; не выполняет код плагина | [plugin_info_box.cpp](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/boxes/plugin_info_box.cpp#L438-L474) |
| `Ui` | `ShowPluginInfoBox(not_null<SessionController*>, const QString &pluginPath, PluginMetadata)` | Создаёт info UI на уровне окна/session controller; optional icon ведёт к sticker-set request через session API | [plugin_info_box.cpp](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/boxes/plugin_info_box.cpp#L477-L523) |
| `Settings::AyuBuilder::AyuSectionBuilder` | `addToggle(ToggleArgs&&) -> Ui::SettingsButton*` | Создаёт toggle в текущем Ayu settings section; getter/setter и подписка связаны с кнопкой/lifetime | [ayu_builder.h](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/settings/ayu_builder.h#L34-L44), [реализация](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/settings/ayu_builder.cpp#L66-L93) |
| `AyuUi` | `AddAyuGramActions(PeerData*, Data::Thread*, SessionController*, const PeerMenuCallback&)` | Внутреннее добавление Ayu submenu для конкретного peer/topic, с фильтрами/историей | [context_menu.h](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/context_menu/context_menu.h#L24-L27), [call-site](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/context_menu/context_menu.cpp#L250-L324) |

Методы C++ из этой таблицы нельзя выдавать за API ExteraGram Android, AyuGram Desktop PLEngine или общий протокол плагинов.

## Техники для разработчика

1. Для совместимости metadata сначала сверяйте точные ключи и ограничения с парсером выбранного клиентского SHA. Здесь минимально проверяются ID и имя; `min_version` и `requirements` только извлекаются в `PluginMetadata` в охваченной реализации.
2. Для описания используйте только подтверждённые этим рендерером конструкции: ограниченный `**bold**` и валидируемые markdown-ссылки. Проверка runtime-рендеринга отсутствует.
3. Если вы модифицируете сам AyuGram Desktop, изучайте `AyuSectionBuilder`/`AyuUi::AddAyuGramActions` как внутренние точки UI интеграции; сторонний plugin должен обращаться к документированным extension interfaces своего PLEngine.
4. Не переносите `SessionController*`, `PeerData*`, `Data::Thread*`, Qt/RPL callbacks и singleton `AyuSettings` в Android BasePlugin код: их типы и lifecycle принадлежат C++/Qt desktop-клиенту.

## Утверждения радара и пробелы

Радар утверждает, что обновлённый AyuGram Desktop sample использует пункты контекстного меню, `SectionBuilder/AyuSectionBuilder` и изменённый preprocess-message контракт `char*` → `std::string*` (`raw/ayugram-desktop/radar-context.md:33`, исходная строка 634). Это частично подкреплено отдельными сохранёнными репозиториями PLEngine и AyuSamplePlugin: в sample есть пример `doPreProcessMessageStd(std::string*, std::string*)`, а снимок PLEngine содержит Std и legacy `char*` callbacks. Эти снимки не подтверждают точный исторический переход, удаление legacy API или версию PLEngine, соответствующую sample. В закреплённом AyuGramDesktop SHA нет PLEngine headers/implementation или preprocess-message API: полный tree содержит 6 673 записи, а среди путей с `plugin`, `plengine` и `preprocessmessage` найдены только UI metadata box и ресурсы его иконки. `radar-urls.json` для этого источника пуст, поэтому конкретная ссылка радара на sample не установлена. Совпадение названия `AyuSectionBuilder` в клиенте и движке не доказывает наличие стабильного внешнего SDK/API.

README рекламирует пользовательские возможности и связывает на сайт документации, но эти заявления не использовались как доказательства plugin API. Snapshot tree не показывает отдельный PLEngine или preprocess hook в этом SHA; внешние контракты описаны в самостоятельных PLEngine/sample источниках. Не исследованы весь клиент и все upstream settings/menu framework, историческая связь sample с точным engine commit и runtime. Совместимость плагинов на указанном SHA не установлена; приложение, сборка и tests не запускались.
