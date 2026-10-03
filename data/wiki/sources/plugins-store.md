---
type: source
source_id: plugins-store
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store.md
date: 2026-09-28
---

# Kangel-Plugins/Plugins-Store — каталог KPM и примеры Python-плагинов

Источник: [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store), ветка `main`, снимок дерева и репозитория `513e29a07858e5dec3a8dcdc6a860fe4296f1d43`, полученный 2026-09-27. [Пиннутый commit](https://github.com/Kangel-Plugins/Plugins-Store/commit/513e29a07858e5dec3a8dcdc6a860fe4296f1d43). По метаданным репозитория лицензия — GPL-3.0. Локальные provenance-файлы: [snapshot](../../raw/plugins-store/snapshot.json), [tree](../../raw/plugins-store/tree.json), [manifest полученных файлов](../../raw/plugins-store/file-manifest.json), [контекст радара](../../raw/plugins-store/radar-context.md) и [URL радара](../../raw/plugins-store/radar-urls.json).

## Роль и границы источника

Это каталог файлов для Kangel Plugins Manager, названного в README менеджером плагинов. Репозиторий хранит текущие `.plugin` и `.eaf`, каталог `store.json` и версии в `legacy_versions/`. В каталоге есть и собственный пакет `Plugins/kangel_plugins_manager.eaf`: в снимке он содержит исходный код менеджера версии 1.5.4, включая получение каталога, проверку доверия и путь установки. Это срез реализации менеджера внутри распространяемого плагина, а не исходники штатного загрузчика/движка ExteraGram и не SDK. Документация `AGENTS.md` остаётся описанием формата со стороны автора репозитория; примеры плагинов показывают call-site `BasePlugin`/`hook_method`, но не гарантируют совместимость произвольной версии клиента.

Снимок содержит 1 583 записи дерева, включая 688 текущих `.plugin` и 12 `.eaf` под `Plugins/`, а также 616 файлов `.plugin`/`.eaf`/`.elyx` под `legacy_versions/`. `store.json` содержит 698 записей плагинов. Эти количества описывают снимок, а не актуальный счётчик магазина; соответствие каждой записи манифеста одному файлу в этой работе не проверялось. В корне README состоит из краткого описания каталога и не содержит руководства разработчика.

## Покрытие

| Прочитанный путь в снимке | Что извлечено | Границы / пропуски |
|---|---|---|
| `README.md:1-7` | Назначение репозитория как каталога плагинов KPM; README не описывает SDK | Не трактовал эмоциональную просьбу в README как техническое требование к исследованию |
| `AGENTS.md:1-73` | Структура каталога, перечисленные поля метаданных, хеширование, сохранение старых версий и описание Elyx | Это документация автора; пункты про подпись и поведение загрузки сверены отдельно только с заархивированным KPM 1.5.4, не со всеми версиями |
| `store.json:1-12201` (весь JSON) | Структурно прочитан каталог из 698 записей; отмечены поля и реальные записи `proxy_sub`, `ReadAllButton`, `NoColorButton` | Не проверялись все файлы/хеши/подписи и не анализировались все плагины каталога |
| `.github/workflows/mirror.yml:1-95` | Триггеры, переписывание raw-ссылок и отправка трёх зеркал | Workflow прочитан как текст; CI не запускался и push не выполнялся |
| `Plugins/ArticleViewerFix.plugin:1-30` | Конкретный hook `ArticleViewer$WindowView.handleTouchEvent(MotionEvent)` и callback до метода | Один маленький пример, без проверки на устройстве |
| `Plugins/NoMoreBlur.plugin:1-41` | Поиск классов, просмотр объявленных методов, условная установка hook и пустой `on_plugin_unload` | Версионная устойчивость целевых имён не проверялась |
| `Plugins/ReadAllButton.plugin:1-55` | Файл прочитан полностью: metadata, выбор языка, регистрация пункта drawer menu и callback чтения всех диалогов | Call-site статически изучен; поведение SDK/клиента не тестировалось |
| `Plugins/NoColorButton.plugin:1-19` | Файл прочитан полностью: metadata и before-hook `ButtonBot.getColor` с фильтром по `this.button.style != null` | Короткий образец; существование метода/фильтра и эффект на целевом клиенте не тестировались |
| `Plugins/kangel_plugins_manager.eaf` — архив целиком; внутренние `kpmplugin/metainfo.json`, `refmap.json` | Проверены ZIP-структура, ID/версия/минимум приложения и переход к исходному `main.py`; в `kpmplugin/src/` прочитаны `store.py`, `security/verify.py`, `elyx_parser.py`, `mixins/store_ops.py`, `mixins/installer.py` и вызов обновления в `views/plugin_list.py` | Это статический просмотр одного заархивированного снимка KPM 1.5.4; не запускался. Не покрыты остальные UI/hooks и штатный движок клиента |

Приобретены по SHA без исполнения также `Plugins/AdBlock.plugin`, `Plugins/AIAssistant.plugin`, `Plugins/FastZovMail.plugin`, `Plugins/QuickSettings.plugin` и `Plugins/Vless.plugin`; их код не включён в содержательное покрытие этой страницы. Помимо KPM-пакета прочитаны только три небольших примера (`ArticleViewerFix`, `NoMoreBlur`, `ReadAllButton`) и заголовок `NoColorButton`; 688 текущих `.plugin`, остальные 11 `.eaf` и 616 архивных артефактов индивидуально не анализировались. Исторические GitHub commit URLs из радара не использовались как отдельные источники реализации.

## Технические факты

### Каталог и распространение

- В `store.json` верхний уровень — объект, ключи которого являются ID плагинов. Документация перечисляет URL файла, имя, версию, автора, описание, хеш, иконку, минимальную версию клиента, статус-категорию, требования/зависимости, локализованные описания и `legacy_version`. В реально полученной записи `proxy_sub` также присутствует `signature`, хотя она не перечислена в схеме `AGENTS.md`; алгоритм проверки приведён ниже по исходнику заархивированного KPM 1.5.4.
- Документация называет `Plugins/<файл>` местом текущей версии и `legacy_versions/<id>/` местом предыдущих выпусков. Название исторического файла включает версию. При коллизии имени существующий файл не перезаписывается: добавляется числовой суффикс (`_1` и далее). Это правило хранения предотвращает замену уже существующего архивного файла, но не описывает пользовательский механизм отката в KPM.
- Обычный `.plugin` описан как один Python-файл; Elyx `.eaf`/`.elyx` в документации описан как ZIP-архив с `refmap` и связанными `metainfo`, `main`, `strings`, `assets`. Для метаданных Elyx указаны имена `metainfo.json`/`.yml` и запасной поиск по архиву. Это зафиксированное описание формата репозитория, а не независимая спецификация официального SDK.
- Корневой `store.json` содержит URL скачивания файлов по изменяемому адресу ветки `main`; конкретную запись следует связывать с версией/хешем из каталога и pinned commit, а не считать URL `main` неизменяемой ссылкой на артефакт.
- В `mirror.yml` запуск настроен на push в `main` или ручной dispatch. Шаги восстанавливают исходный `store.json`, переписывают Forgejo raw-ссылки на адрес соответствующей площадки и делают force-push в GitHub, Codeberg и GitVerse. Наличие workflow доказывает описанную автоматизацию, но не успешность её выполнения в этом снимке.

### Встроенный KPM: кодовое поведение по снимку

Архив `Plugins/kangel_plugins_manager.eaf` — ZIP; проверка структуры архива чтением списка записей не исполняла его код. Его `refmap.json` направляет к `kpmplugin/src/main.py`, а `metainfo.json` называет пакет `kangel_plugins_manager`, версию `1.5.4`, `app_version >=12.9.0` и `sdk_version >=1.4.5.3`. Поэтому следующие сведения — статическая проверка именно этого пакета/снимка, не контракт SDK и не тест в приложении.

- `kpmplugin/src/store.py` задаёт четыре источника каталога в порядке auto-перебора: Forgejo (`kangel`), GitHub, Codeberg, GitVerse. При auto-режиме загрузчик пробует URL каталога каждого зеркала; GitHub имеет два варианта URL. После загрузки он нормализует данные и запрашивает SHA коммита у того же зеркала для кэша. Если API с SHA недоступно, `is_cache_valid()` считает существующий кэш пригодным fallback-режимом; тогда обычное обновление может завершиться на кэше без перебора URL каталога. Форсированное обновление проходит по URL.
- `security/verify.py` загружает `public_key.pem` из Elyx assets и проверяет `SHA256withRSA` над UTF-8-строкой `plugin_id:version:file_hash`. Исключения и отсутствующий ключ/подпись дают `False`. `StoreOpsMixin._check_plugin_data` сопоставляет байтовый SHA-256 с хешем текущей записи; если подпись есть — требует успешной проверки, а если подписи нет — совпавшего хеша достаточно. Опция `block_untrusted_plugins` используется с default `True` перед сохранением плагина в `install_plugin_by_id`; отключение настройки пропускает этот gate. Файловая safety-проверка также знает legacy-хеши/подписи.
- Для URL с суффиксом `.eaf` `InstallerMixin` удаляет имеющийся целевой каталог Elyx, распаковывает архив в `ElyxPlugins/<id>` (либо найденный fallback-каталог), читает метаданные с учётом refmap и устанавливает присутствующие `dex/`, `wheels/`, `native/`. Для обычного плагина скачанные байты записываются как `<id>.py`. Это описывает call-site данного KPM, не все разновидности Elyx.
- В `update_selected_plugins` сравниваются локальная и удалённая версии; при различии метод напрямую записывает `.plugin` или вызывает распаковку `.eaf`. В самом этом пути нет вызова `_check_plugin_data`, хотя прямой install его делает. UI вызывает `update_selected_plugins` непосредственно. Это видимый по коду разрыв проверок; без runtime-анализа нельзя заключать, что никакой иной клиентский слой не участвует.

Доказательства для встроенного пакета приведены как `Plugins/kangel_plugins_manager.eaf!<внутренний путь>:<строки>`: исходный текст хранится внутри бинарного архивного blob по [пиннутой ссылке на пакет](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/kangel_plugins_manager.eaf). Это не отдельные GitHub-файлы и просмотр исходников не означает запуска.

### Образцы клиентского кода

- `ReadAllButton` объявляет метаданные `__id__`, `__name__`, `__description__`, `__author__`, `__min_version__`, `__icon__`, `__version__` и наследуется от `BasePlugin`. В `on_plugin_load()` он передаёт `MenuItemData` в `add_menu_item`, указывая `MenuItemType.DRAWER_MENU`, текст, callback и icon key. Callback вызывает `get_messages_storage().readAllDialogs(-1)` и показывает результат через `BulletinHelper`. Это полезный образец связи пункта меню с логикой, но точный контракт следует сверять с SDK нужной версии.
- `ArticleViewerFix` передаёт в `hook_method` reflection-метод `org.telegram.ui.ArticleViewer$WindowView.handleTouchEvent(MotionEvent)` и callback-объект, который в `before_hooked_method` задаёт `param.setResult(False)`. Сам плагин оборачивает инициализацию в `try/except` с `log`. Это пример точечного hook; сигнатура зависит от клиентской версии.
- `NoMoreBlur` в `on_plugin_load()` ищет классы через `find_class`, перебирает `getDeclaredMethods()` и выбирает методы по имени (`deviceBlurEnabled`, `chatBlurEnabled`, `isBlurEnabled`, затем `draw`), после чего вызывает `self.hook_method`. Ошибки ловятся на уровне всего процесса установки. Файл оставляет `on_plugin_unload()` пустым, поэтому он не подтверждает, что такой приём обеспечивает корректную очистку ресурсов.
- `NoColorButton` передаёт reflection-метод `BotInlineKeyboard.ButtonBot.getColor` в `hook_method` как `before` callback `fn`; в фильтре указан `this.button.style != null`, а callback задаёт `BotInlineKeyboard.BackgroundColor.NONE`. Это ещё один конкретный call-site, не подтверждение доступности класса/метода и синтаксической или runtime-работоспособности на других версиях.
- Каталог содержит и очень короткие Python-плагины, и крупные скрипты, однако размер/наличие `.plugin` само по себе ничего не говорит о безопасном поведении при установке или исполнении.

## Вызовы и наблюдаемые контракты

Все сигнатуры ниже — фактические call-site выбранных `.plugin` файлов в указанном commit, не нормативный API всего SDK.

| Модуль / объект | Сигнатура или call-site | Назначение и контекст | Доказательство |
|---|---|---|---|
| `ReadAllButton` | `on_plugin_load()` → `self.add_menu_item(MenuItemData(menu_type=MenuItemType.DRAWER_MENU, text=..., on_click=..., icon=...))` | Регистрация пункта бокового меню при загрузке плагина; далее callback выполняет работу и показывает bulletin | [ReadAllButton.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ReadAllButton.plugin#L16-L55) |
| `ReadAllButton` | `get_messages_storage().readAllDialogs(-1)` | Наблюдаемый вызов хранилища сообщений при пользовательском клике | [ReadAllButton.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ReadAllButton.plugin#L49-L55) |
| `ArticleViewerFix` | `self.hook_method(clazz.getClass().getDeclaredMethod("handleTouchEvent", MotionEvent), ArticleViewerFix())` | Установка hook на Java reflection method во время `on_plugin_load`; callback выполняется до оригинального метода | [ArticleViewerFix.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ArticleViewerFix.plugin#L16-L30) |
| `ArticleViewerFix` | `before_hooked_method(self, param)` → `param.setResult(False)` | Возвращает заданный результат на перехваченном вызове; конкретное значение/эффект относятся к этому примеру | [ArticleViewerFix.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ArticleViewerFix.plugin#L16-L19) |
| `NoMoreBlur` | `find_class("...").getClass().getDeclaredMethods()`; `self.hook_method(m, hook)` | Reflection-поиск методов с фильтрацией по именам при `on_plugin_load` | [NoMoreBlur.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/NoMoreBlur.plugin#L13-L41) |
| `NoColorButton` | `self.hook_method(BotInlineKeyboard.ButtonBot.getClass().getDeclaredMethod("getColor"), before=fn, before_filters=[base_plugin.HookFilter.Condition("this.button.style != null")])`; `fn` задаёт `BotInlineKeyboard.BackgroundColor.NONE` | Before-hook для метода без явных параметров в reflection-вызове; контракт метода и filter DSL проверяйте на целевой SDK | [NoColorButton.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/NoColorButton.plugin#L1-L19) |

## Практические приёмы и рецепты

1. **В каталоге — манифест, в исходном скрипте — исполняемые метаданные.** Для своей каталогизации храните устойчивый plugin ID и отдельно отображаемые `name`/`version`; пример `ReadAllButton` показывает набор Python-полей, а `store.json` содержит запись, адрес артефакта и ограничения каталога. Не объявляйте одноимённые поля одинаковым контрактом до сверки с загрузчиком.
2. **Архивируйте старые байты до публикации новой версии.** Следуйте задокументированному шаблону `legacy_versions/<id>/<base>_v<version>.<ext>` и при совпавшем имени сравнивайте хеши, выбирая новый суффикс вместо перезаписи. Это правило относится к истории файлов каталога.
3. **Если добавляете пункт меню, держите wiring отдельно от обработчика.** Образец `ReadAllButton` формирует локализованный текст, регистрирует `MenuItemData` в `on_plugin_load()` и передаёт bound method callback. Проверьте на нужной версии SDK правильность enum, аргументов и поведения callback.
4. **Reflection-hook снабжайте проверками отсутствия цели и обработкой ошибки.** В `NoMoreBlur` классы/методы находятся динамически и установка может завершиться ошибкой при изменении клиента. Этот пример обрабатывает исключение, но выбирает цели только по имени метода; сверяйте полную сигнатуру на нужной версии клиента.

## Ограничения и противоречия

- Статус: исходные объявления и код для ограниченного набора плагинов — `code`; схема `AGENTS.md` — `docs`; упоминания радара — только вторичный контекст. Никаких запусков, установок, сборок или проверок на Android-устройстве не было, поэтому результат не `runtime-verified`.
- README и внутренний `AGENTS.md` расходятся по глубине: README только говорит, что здесь лежат плагины для KPM, а `AGENTS.md` описывает структуру, схему, Elyx и автоматизацию. Полной отдельной спецификации протокола магазина в репозитории нет; часть контрактов можно восстановить по вложенному исходнику KPM 1.5.4, но это не определяет поведение всех версий клиента.
- В документационной схеме `AGENTS.md` не упомянуто поле `signature`, хотя оно есть в опубликованных записях `store.json`. В заархивированном исходнике KPM проверка реализована: `security/verify.py` проверяет RSA-подпись `SHA256withRSA` над UTF-8-строкой `plugin_id:version:file_hash`, используя встроенный `kpmplugin/res/public_key.pem`. `StoreOpsMixin._check_plugin_data` сначала сопоставляет SHA-256 загруженных байтов с хешем текущей записи и проверяет подпись, если она задана; при совпавшем хеше и пустой подписи код принимает артефакт. Путь установки `install_plugin_by_id` вызывает эту проверку, если настройка `block_untrusted_plugins` включена (значение по умолчанию в этом call-site — `True`). Это вывод из кода именно KPM 1.5.4, не runtime-проверка и не гарантия проверки всеми версиями клиента.
- В `update_selected_plugins` обнаружен отдельный предел проверки: прямой путь обновления загружает версию и записывает `.plugin`/распаковывает `.eaf` при изменении номера, но сам не вызывает `_check_plugin_data`; UI вызывает этот метод напрямую. Поэтому путь установки нового плагина и путь обновления в этом снимке не имеют одинаково видимого integrity gate. Мы не проверяли runtime-перехваты/другие окружения, поэтому фиксируем наблюдение как ограничение статического анализа, а не доказанный эксплойт.
- В радаре встречается устаревшее имя организации `KangelPlugins` без дефиса и старые сообщения о 404; идентичность этого источника подтверждена фактически доступным репозиторием `Kangel-Plugins/Plugins-Store` и pinned SHA. Radar указывает Codeberg и GitVerse как зеркала; workflow снимка задаёт именно push туда и на GitHub. Отдельные зеркала и их состояние в этой задаче не проверялись.
- `min_version`, перечисленный статус категории, зависимости и сигнатуры относятся к конкретному каталогу/записи. Они не задают текущий минимум всех клиентов ExteraGram/AyuGram и не подтверждают поддержку каждого API.
- Не изучены все поля всех 698 записей и соответствие каждой записи конкретному файлу/подписи; не проверялись состояние зеркал в сети, остальные плагины магазина, исторические версии и поведение на устройстве. Код менеджера покрыт только в перечисленных модулях одного `.eaf`; штатный движок плагинов клиента и его фактическая интеграция не изучены. Для практической разработки сопоставляйте call-site из примеров и требования KPM с [официальной документацией SDK](official-sdk.md) и целевой версией клиента.
