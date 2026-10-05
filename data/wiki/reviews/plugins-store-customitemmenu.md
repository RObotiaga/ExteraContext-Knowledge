---
type: review
source_id: plugins-store-customitemmenu
title: "Источник: Кастомные пункты меню (customitemmenu)"
reviewer: independent-verifier
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: f8f35b18b6148b20027b3bdeff505d240086444a
artifact_sha256: 5cc1ac05bf214d6431b910a44f9dbafd4896a96f78249670ca1548113b7c7a71
plugin_id: "customitemmenu"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: plugins-store-customitemmenu

- Плагин: `CustomItеmMеnu.plugin`, версия 1.5 (id `customitemmenu`)
- Commit: `f8f35b18b6148b20027b3bdeff505d240086444a`
- Источник: [plugins-store-customitemmenu.md](../sources/plugins-store-customitemmenu.md)
- Проверка: независимое сопоставление кандидатов с исходным кодом; статус доказательности — `code` (статический анализ AST + сверка blob/pinned raw-URL, не runtime-проверка).

## Вердикт

Сборщик предоставил 5 фактов. Принято 5 фактов.

| ID | Вердикт | Основание |
|---|---|---|
| `plugins-store-customitemmenu:customitemmenu-001` | Принято | Подтверждены вызов `_add_drawer_links()` из `on_plugin_load`, предварительное снятие старых id через `remove_menu_item` с очисткой списка и повторная регистрация `MenuItemData`/`add_menu_item` для четырёх `MenuItemType` с сохранением возвращённого `menu_id`. Строки 47, 85, 249–255, 288–300. |
| `plugins-store-customitemmenu:customitemmenu-002` | Принято | Подтверждены `BottomSheet.Builder`, `FrameLayout`, `UniversalRecyclerView` с `Callback2`/`Callback5`, `UItem.asButton` и `LayoutHelper.createFrame(-1, 700)`; обёртки `dynamic_proxy(Utilities.Callback2/Callback5)` подтверждены. Строки 9, 335–351, 355, 376, 396, 405–406. |
| `plugins-store-customitemmenu:customitemmenu-003` | Принято (с исправлением) | Формула `getattr(R.drawable, i)` и фильтр по `X` подтверждены, но заявленных 129 служебных ресурсов в файле нет: `blacklist` (49–77) содержит 143 уникальные строки. Также фильтр — `not i.startswith('_')`, то есть отсекается ведущее подчёркивание, а не символ `_` внутри имени. В факт внесена исправленная формулировка. |
| `plugins-store-customitemmenu:customitemmenu-004` | Принято | `parse_markdown` встречается в файле ровно один раз — в строке импорта 10; тексты диалогов идут строками до `builder.set_message` (424) без парсера. Строки 10, 321–331, 416–428. |
| `plugins-store-customitemmenu:customitemmenu-005` | Принято | `on_plugin_unload` в файле отсутствует (проверены все 433 строки: упоминаний нет), состояние — JSON в `custom_items`, `set_items()` использует `reload_settings=True` и вызывает `rebuildAllItems()`. Строки 47, 195–226. |

## Замечания о точности

1. **Факт 003 — число в чёрном списке.** AST-подсчёт литерала `blacklist` (49–77) даёт 143 уникальных строки без дублей; значение 129 из кандидата не воспроизводится статически. Если 129 было получено фильтрацией по фактическому `dir(R.drawable)` на конкретной сборке, это runtime-величина и в файле не подтверждается. Дополнительно: кандидат говорит об «исключении `_`», тогда как код исключает только имена с ведущим подчёркиванием — имена вида `ic_ab_new` и `sms_bubble` проходят символьный фильтр (последнее дополнительно отсекается `blacklist`).
2. **Факт 005 — защищённый вызов.** В коде нет прямого `get_last_fragment().rebuildAllItems()`: сначала `fragment = get_last_fragment()` (224), затем `if fragment and hasattr(fragment, "rebuildAllItems"): fragment.rebuildAllItems()` (225–226). Формулировка уточнена, смысл кандидата сохранён.
3. **Факт 004 — граница негативного свидетельства.** Утверждение «тексты выводятся как plain text» верно только на уровне файла: плагин не применяет `parse_markdown`, а передаёт строки в `AlertDialogBuilder.set_message`. Рендеринг внутри самого `AlertDialogBuilder` по этому файлу не проверяется; отдельно в базе знаний `parse_markdown` в snapshot `exteragram-utils 0.1.3` объявлен с телом `...` (нереализованный парсер), поэтому мёртвый импорт не меняет наблюдаемое поведение.
4. **Факт 005 — lifecycle-риск без runtime-вывода.** Отсутствие `on_plugin_unload` означает, что зарегистрированные пункты меню не снимаются при выгрузке плагина (в отличие от паттернов `remove_menu_item` в unload у других плагинов store). Это следует из кода, но последствия для конкретной сборки клиента не тестировались.

## Pinned источник

https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/CustomIt%D0%B5mM%D0%B5nu.plugin
