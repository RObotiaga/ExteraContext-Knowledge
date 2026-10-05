---
type: review
source_id: plugins-store-sorter-plus
title: "Plugins Store: sorter_plus (Sorter+ 1.4.3)"
reviewer: independent-verifier
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 39d0a8797ddca6fd23159567311e7a0e03c342b6
artifact_sha256: c99e7327a4def4d894689fc8c1b743c10762db5f40766e53c2d7f511993bd904
plugin_id: "sorter_plus"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-05"
---

# Ревью: Plugins Store `sorter_plus` (Sorter+ 1.4.3)

Сборщик предоставил 5 фактов. Принято 5 фактов.

## Проверка происхождения

- Закреплённый commit `39d0a8797ddca6fd23159567311e7a0e03c342b6` существует в локальном клоне (`git cat-file -t` → `commit`), сообщение `Update plugin: sorter_plus v1.4.3`, дата 2026-10-01T23:40:49+03:00.
- GitHub API для `Plugins/sorter_plus.plugin?ref=39d0a87…` возвращает HTTP 200, `sha = e1544cdbeedc2b8ce297fbe6c116b3887366f8b6`, `size = 250319`. Эти же значения дают локальные `git hash-object Plugins/sorter_plus.plugin` и `git cat-file -s 39d0a87…:Plugins/sorter_plus.plugin` — файл закреплённой ревизии и независимо полученный артефакт совпадают.
- `git diff 39d0a879… HEAD -- Plugins/sorter_plus.plugin` пуст, blob закреплённой ревизии равен blob рабочей копии (`e1544cdb…`), поэтому номера строк локального файла совпадают с номерами в pinned URL.
- SHA-256 файла `c99e7327a4def4d894689fc8c1b743c10762db5f40766e53c2d7f511993bd904` совпадает с `hash` записи `sorter_plus` в `store.json` (`version: 1.4.3`, `min_version: 12.1.1`, `author: "@plugin_ai"`, `status: customization`).

## Верификация фактов

| ID | Вердикт | Проверка и уточнения |
|---|---|---|
| `sorter-plus-001` | Принят | `_install_hooks` подтверждён строками 404–430: `PluginsActivity` резолвится через `find_class` (406), `createView(Context)` — 418–419 и 425, `fillItems(ArrayList, UniversalAdapter)` — 420–423 и 426. Хук `PluginCell.set` подтверждён 432–451 (перебор `getDeclaredMethods`, выбор первого метода `set` с двумя параметрами). Отрицательная часть подтверждена: `UniversalAdapter` встречается только в строках 413, 414 и 421 и используется лишь как класс типа параметра, ни один `hook_method` на него не указывает; `EXTRA_PLUGIN_VIEW_CLASSES = []` (130), поэтому `_install_extra_plugin_view_hooks` (455+) не выполняет тело цикла. Уточнение: помимо этих трёх точек файл ставит и другие хуки (install surface 514, open-for-view 539, engine path 562, success bulletin 595, activity result 2984) — они вне пяти фактов. |
| `sorter-plus-002` | Принят | Разделение на before/plugin/after подтверждено строками 775–792 (`seen_plugin_item` и три списка), вызовы `_filter_plugin_items`/`_sort_plugin_items` — 794–795, `items.clear()` — 801, вставка `UItem.asFullyCustom(self._pills_container)` — 805–811. Уточнения: пилюли добавляются только при `self._pills_container is not None`; пустое состояние папки вставляется тем же `UItem.asFullyCustom(empty_view)` (813–819) и является альтернативой списку плагинов, а не дополнением; before/after-элементы предварительно обрезаются helpers `_trim_trailing_spaces`/`_trim_leading_spaces` (798–799). |
| `sorter-plus-003` | Принят | Фильтрация подтверждена строками 1101–1143: `all` (1102–1103), `AUTO_NEW_FOLDER_ID` и автопапка `new` (1104–1105, 1113–1114), `enabled`/`disabled` (1115–1118), `author` (1119–1131), ручная папка по `folder["plugins"]` (1134–1143), причём пустой список включённых даёт пустой результат (1135–1136). Сортировка подтверждена 1145–1171 и совпадает с ключами `SORT_MODES` (45–51): `default`, `name_asc`, `name_desc` (reverse=True), `enabled_first` (кортеж «включённость, имя»), `recent` (mtime, reverse=True). Уточнение: `_sort_plugin_items` сравнивает строковые литералы, а не элементы `SORT_MODES` напрямую; неизвестный режим возвращает исходный порядок. |
| `sorter-plus-004` | Принят | `get_setting` подтверждён строками 5899–5913, `set_setting` — 5968 и 5971–5977, вызов `_write_state_backup()` — 5978. Имя бэкапа формируется из `__id__` в `_state_backup_path` (5763–5779): основной путь `<filesDir>/sorter_plus_state.json` (5768), fallback `~/.sorter_plus_state.json` (5776) и относительный `sorter_plus_state.json` (5779). Состав JSON подтверждён 5808–5821; восстановление из бэкапа при пустом `folders_json` — 5914–5930. Уточнение: в fallback-ветке имя файла начинается с точки — это `~/.sorter_plus_state.json`, а не `sorter_plus_state.json` в домашнем каталоге. |
| `sorter-plus-005` | Принят | `on_plugin_load` подтверждён строками 353–356 (`_load_state`, `_load_visual_prefs`, `_install_hooks`), `on_plugin_unload` — 358–391, цикл снятия хуков `for hook in list(self._hooks): self.unhook_method(hook)` — 370–375, очистка `self._hooks = []` и обнуление ссылок — 375–391, `_unhook_activity_result` — 364 и 390 (реализация 3005–3010). Уточнение: `_unhook_activity_result` вызывается дважды (364 и 390) — дублирование идемпотентно, исключения `unhook_method` подавляются; сами хуки регистрируются не в `on_plugin_load` напрямую, а внутри `_install_hooks`, который он вызывает. |

## Проверка повторов и расхождений

- ID `plugins-store-sorter-plus:sorter-plus-001..005` в `facts.json` (2568 записей) отсутствуют — коллизий нет; отдельного файла фактов `plugins-store-sorter-plus.json` до этой проверки не было.
- Единственное прежнее упоминание `sorter_plus` в базе — `plugins-store-ui-customization:fact-026` (commit `00de67026419f9dbe3a2787bb1236e8aaead8f76`, `review_status: accepted-with-gaps`), где утверждается: «…выполняется хуком PluginsActivity.createView и UniversalAdapter.fillItems», а рецепт советует «Перехватывайте fillItems у UniversalAdapter». Проверка исходника на этом же старом commit (строки 335–345: `PluginsActivity.getClass().getDeclaredMethod("fillItems", ArrayListClass, UniversalAdapterClass)` → `hook_method(fill_items, …)`) показывает, что хук стоит на `PluginsActivity.fillItems`, а `UniversalAdapter` — лишь класс второго параметра. То есть `fact-026` содержит неточность в `api`/`recipe`, а новые факты `sorter-plus-001`/`sorter-plus-002` описывают тот же механизм корректно. Требуется отдельное решение по `fact-026` (исправление или supersede) — в рамках этой проверки он не изменялся.
- Пять новых фактов описывают разные механизмы (хуки, перестройка списка, фильтрация/сортировка, хранение, жизненный цикл) и не дублируют формулировки друг друга.

## Остаточные пробелы и вердикт

Проверка статическая: сборка, установка, включение/выключение и повторная загрузка на клиенте `>= 12.1.1` не выполнялись, runtime-подтверждений нет. Доступность внутренних символов Telegram (`PluginsActivity`, `PluginCell`, `UniversalAdapter`, `UItem.asFullyCustom`) привязана к конкретной сборке клиента и закреплённым SHA плагина не гарантируется. Вне пяти проверенных утверждений остались: ряд визуальных настроек пилюль и цветовые оверрайды (`pill_height`, `pill_outline`, `pill_blur`, `color_overrides`), режим перемещения папок, загрузка кастомных иконок (`sorter_plus_icons`), интеграция с `BulletinFactory`/`BulletinHelper` и прямые обращения к аккаунтам.

**Вердикт: `accepted`.** Все пять фактов подтверждены исходником на закреплённом commit; уточнения касаются состава бэкапа (имя `sorter_plus_state.json` в `filesDir` против `~/.sorter_plus_state.json` в fallback), альтернативности пустого состояния и списка плагинов, а также двойного вызова `_unhook_activity_result`. Обнаружено расхождение с ранее принятым `fact-026` по цели хука `fillItems`.
