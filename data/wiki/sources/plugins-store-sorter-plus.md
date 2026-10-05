---
type: source
source_id: plugins-store-sorter-plus
title: "Plugins Store: sorter_plus (Sorter+ 1.4.3)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 39d0a8797ddca6fd23159567311e7a0e03c342b6
path: "Plugins/sorter_plus.plugin"
artifact_sha256: c99e7327a4def4d894689fc8c1b743c10762db5f40766e53c2d7f511993bd904
plugin_id: "sorter_plus"
plugin_version: "1.4.3"
author: "@plugin_ai"
min_version: "12.1.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-sorter-plus.md
date: "2026-10-05"
---

# Plugins Store: sorter_plus (Sorter+ 1.4.3)

Источник: [Plugins/sorter_plus.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin).  
Репозиторий: `Kangel-Plugins/Plugins-Store`.  
Зафиксированный commit: `39d0a8797ddca6fd23159567311e7a0e03c342b6` (`Update plugin: sorter_plus v1.4.3`, 2026-10-01T23:40:49+03:00).  
Артефакт: 250319 байт, git blob `e1544cdbeedc2b8ce297fbe6c116b3887366f8b6`, SHA-256 `c99e7327a4def4d894689fc8c1b743c10762db5f40766e53c2d7f511993bd904` (совпадает с `hash` записи `sorter_plus` в `store.json`).

Одностраничный Python-плагин `Sorter+` (`__id__ = "sorter_plus"`, `__version__ = "1.4.3"`, `__author__ = "@plugin_ai"`, `__min_version__ = "12.1.1"`, строки 1–7) добавляет над списком плагинов ряд пилюль-папок, фильтрует и сортирует `UItem`-элементы списка, а состояние хранит в настройках плагина и JSON-бэкапе. В `store.json` запись `sorter_plus` имеет `name: Sorter+`, `version: 1.4.3`, `min_version: 12.1.1`, `status: customization` и SHA-256, совпадающий с файлом.

## Проверенные сведения

1. **Хуки списка плагинов** — [строки 404–453](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L404-L453): `_install_hooks` резолвит `PluginsActivity`, `android.content.Context`, `java.util.ArrayList` и `org.telegram.ui.Components.UniversalAdapter`, затем объявляет `PluginsActivity.createView(Context)` (418–425) и `PluginsActivity.fillItems(ArrayList, UniversalAdapter)` (420–426) и регистрирует их через `hook_method`. Отдельного хука на `UniversalAdapter` нет: класс встречается в файле только в строках 413, 414 и 421 как тип параметра, а `EXTRA_PLUGIN_VIEW_CLASSES = []` ([строка 130](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L130)) делает `_install_extra_plugin_view_hooks` no-op. Дополнительно `_install_plugin_cell_hook` (432–451) ищет среди объявленных методов `PluginCell` первый `set` с двумя параметрами и хукает его.
2. **Переупорядочивание списка** — [строки 773–834](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L773-L834): `_process_fill_items` пропускает собственные элементы (`_is_our_custom_item`, 782–783) и делит остальные на `before_plugin_items` / `plugin_items` / `after_plugin_items` по признаку `seen_plugin_item` (778–792), после чего вызывает `items.clear()` и заново собирает список: before-часть, контейнер пилюль как `UItem.asFullyCustom(self._pills_container)` ([строка 807](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L807)), отфильтрованные и отсортированные плагины (821–832) и after-часть (833–834). Пустое состояние папки вставляется тем же способом — `UItem.asFullyCustom(empty_view)` (813–819).
3. **Фильтрация и сортировка** — [строки 1101–1171](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L1101-L1171): `_filter_plugin_items` возвращает список без изменений для `all`, фильтрует по свежести mtime для `AUTO_NEW_FOLDER_ID` и автопапки `new`, по `_plugin_enabled` для `enabled`/`disabled`, по `_plugin_author` для автопапки `author` и по списку id `folder["plugins"]` для ручной папки. `_sort_plugin_items` (1145–1171) реализует режимы `SORT_MODES` ([строки 45–51](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L45-L51)): `default`, `name_asc`, `name_desc`, `enabled_first` (по имени внутри групп) и `recent` (по mtime).
4. **Сохранение порядка и настроек** — [строки 5897–5978](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L5897-L5978): `_load_state` читает `selected_folder_id`, `sort_mode`, `folder_counter`, `all_pill_index`, `add_pill_index`, `add_pill_migrated` и `folders_json` через `get_setting`; `_save_state` записывает те же ключи через `set_setting` и вызывает `_write_state_backup`. Имя бэкапа формируется в `_state_backup_path` ([5763–5779](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L5763-L5779)) из `__id__` — `sorter_plus_state.json` в каталоге `filesDir` (fallback `~/.sorter_plus_state.json`). `_write_state_backup` ([5798–5823](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L5798-L5823)) пишет JSON с ключами `folders`, `selected_folder_id`, `sort_mode`, `folder_counter`, `all_pill_index`, `add_pill_index`; `_read_state_backup` (5781–5796) используется как fallback, если `folders_json` пуст.
5. **Жизненный цикл** — [строки 353–391](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L353-L391): `on_plugin_load` вызывает `_load_state`, `_load_visual_prefs` и `_install_hooks`; `on_plugin_unload` снимает накопленные хуки циклом `for hook in list(self._hooks): self.unhook_method(hook)` (370–375) с подавлением исключений, дополнительно вызывает `_unhook_activity_result` ([3005–3010](https://github.com/Kangel-Plugins/Plugins-Store/blob/39d0a8797ddca6fd23159567311e7a0e03c342b6/Plugins/sorter_plus.plugin#L3005-L3010)), очищает `self._hooks` и обнуляет ссылки на `View` и состояние.

## Границы и наблюдаемые особенности

- Проверка статическая: установка, включение/выключение и работа на конкретной сборке ExteraGram/AyuGram не выполнялись. Совместимость с клиентом `>= 12.1.1` заявлена метаданными и не подтверждена runtime.
- Существование внутренних классов Telegram (`PluginsActivity`, `PluginCell`, `UniversalAdapter`, `UItem.asFullyCustom`) привязано к конкретной сборке клиента и закреплённым SHA плагина не гарантируется.
- `on_plugin_unload` вызывает `_unhook_activity_result` дважды (строки 364 и 390) — это идемпотентное дублирование; `unhook_method` вызывается с подавлением исключений, поэтому повторное снятие не влияет на результат.
- Помимо трёх ключевых точек плагин устанавливает и другие хуки (`_install_surface_hooks`, `_open_for_view_hook`, `_engine_path_hook`, `_success_bulletin_hook`, activity-result), которые в пять проверенных фактов не входят.
