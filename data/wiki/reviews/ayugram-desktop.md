---
type: review
source_id: ayugram-desktop
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: AyuGram/AyuGramDesktop

- **Вердикт: accepted-with-gaps.** Двенадцать фактов относятся к локальным UI/settings/menu точкам AyuGram Desktop и не называют их публичным plugin SDK. Подтверждения проверены на закреплённом SHA `db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a`; ни приложение, ни сборка, ни тесты не запускались.
- **Идентичность и manifest:** snapshot сообщает репозиторий `AyuGram/AyuGramDesktop`, ветку `dev`, полный commit SHA и дату 2026-09-27. `tree.json` содержит 6 673 записи без усечения. В `file-manifest.json` 17 файлов; SHA-256 каждого локального файла в `raw/ayugram-desktop/files/` совпал с manifest.
- **Независимо проверенное покрытие:** `plugin_info_box.h/.cpp` (metadata, quoted-value parsing, ограничения, description, info box); `ayu_builder.h/.cpp` и `settings_ayu.h/.cpp` (API builder и его использование); `context_menu.h/.cpp`, `ayu_settings.h/.cpp` (видимость и Ayu actions); `ayu_state.h/.cpp`, `ayu_infra.h/.cpp` (выбранные state/startup helpers); README, LICENSE и snapshot metadata. Проверены точные строки всех 12 фактов, их pinned-SHA evidence и статусы `code`, `secondary`, `inference`.

## Исправления и оценка утверждений радара

- На странице обновлены frontmatter review status/link и покрытие: перечислены также сохранённые Ayu settings/state/infra файлы. Уточнено, что эти выбранные материалы показывают реализацию самого клиента.
- Радарный контекст есть в `raw/ayugram-desktop/radar-context.md:33` (исходная строка 634), однако `radar-urls.json` пуст и не закрепляет конкретный sample URL. Предыдущее утверждение страницы, что preprocess API не подтверждён соседними источниками, было слишком сильным. Сохранённый sample snapshot содержит `doPreProcessMessageStd(std::string*, std::string*)`; PLEngine README называет `char*` hook legacy/replaced, но его snapshot всё ещё загружает и вызывает оба callback (`AyuPlugin.h:51-52`, `PLEMains.cpp:236-270`, `apiwrap.cpp:4660-4691`). Поэтому наличие нового контракта подтверждено, а буквальная замена/удаление legacy и исторический diff не подтверждены. Это уточнение добавлено в факт 011 с уникальными cross-source доказательствами.
- В полном tree этого Desktop SHA по именам `plugin`, `plengine`, `preprocessmessage` найдены только `plugin_info_box.{h,cpp}` и иконки `history_file_plugin`; PLEngine headers/implementation и preprocess hook отсутствуют. Изученный `PluginMetadata`, парсер и `ShowPluginInfoBox` доказывают только отображение metadata, а не plugin loading, ABI, выполнение или регистрацию внешних plugins. Публичная сигнатура внутренних C++ helpers не делает их доступным SDK.
- Факт 012 классифицирует вывод о клиентских seams как `inference`; ни один из других code facts не заявляет runtime-проверку. Лимиты parser, список metadata keys, settings builder/lifetime и peer-menu call-sites совпадают с локальными строками снимка.

## Дубликаты

В `work/ayugram-desktop-facts.json` **12 записей и 12 уникальных ID**; внутри набора нет повторных ID или дублирующихся claims. Темы metadata/`AyuSectionBuilder`/preprocess пересекаются с отдельными PLEngine и AyuSamplePlugin sources. Это допустимое совпадение между разными репозиториями и commit SHA: Desktop source описывает внутренние UI точки, PLEngine — callback ABI/загрузчик/call-sites, sample — примеры и их несоответствия. Provenance не сливался. Для последующего синтеза подходит канонический Desktop PLEngine topic.

## Остаточные пробелы

- Не прочитан весь 6 673-записный Telegram Desktop fork и весь общий Settings/menu framework; покрытие ограничено выбранными Ayu-specific точками и файлами manifest.
- Не прослежены все callers `ShowPluginInfoBox`, места поиска/загрузки `.plugin`, runtime и совместимость с PLEngine. В этом pinned tree отдельные PLEngine/preprocess paths не обнаружены.
- Не установлена связь конкретного radar sample URL, даты/исторического commit изменения и AyuSamplePlugin SHA с конкретной версией PLEngine; снимок движка сохраняет оба preprocess callback, хотя README описывает Std как замену legacy.
- Условия корневого LICENSE не классифицированы отдельно. Runtime, сборка и тестирование не проводились.

Вердикт относится к ограниченной задаче об Ayu-specific UI seams и непубличности их внешнего контракта; он не удостоверяет полноту клиентского fork или ABI-совместимость plugins.
