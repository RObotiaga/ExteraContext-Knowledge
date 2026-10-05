---
type: source
source_id: plugins-store-quantahut
title: QuantaHut
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: d0efb7b72bcac954d97af04670d6492900ade596
path: Plugins/quantahut.plugin
version: 1.5.4
plugin_id: quantahut
author: "@luvztroy"
min_version: 12.9.0
platform: Android
review_status: accepted
review: ../reviews/plugins-store-quantahut.md
date: 2026-10-05
---

# Plugins Store: quantahut (QuantaHut)

Источник: [Plugins/quantahut.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin).  
Репозиторий: `Kangel-Plugins/Plugins-Store`.  
Зафиксированный commit: `d0efb7b72bcac954d97af04670d6492900ade596` (`Update plugin: quantahut v1.5.4`, 2026-10-02T17:02:16Z).  
Артефакт: 214541 байт, git blob `f1ecf88928b7198bdfe74cbadf7ac1b8c86e1ebd`, SHA-256 `6d77ec8e97925d069c7561e1bb5828e69fed115e565dd93fbb6ad9ea65f1a307`.

Одностраничный Python-плагин `QuantaHut` (`__id__ = "quantahut"`, `__version__ = "1.5.4"`, `__author__ = "@luvztroy"`, `__min_version__ = "12.9.0"`, `__requirements__ = "cachetools"`, `__type__ = "plugin"`, `__beta__ = "False"`, `__priority__ = 1`) позиционируется как библиотека для Quanta-плагинов и экспортирует через `__all__` утилиты (`get_localized_string`, `JsonCacheFile`, `utilities`/`hut`, `BottomSheet`, `export_plugin_settings`, `perform_haptic` и др.). В `store.json` запись `quantahut` имеет `status: library`, `version: 1.5.4`, `min_version: 12.9.0` и SHA-256, совпадающий с файлом.

## Проверенные факты

1. **Кастомизация интерфейса** — строки 4231–4294: `_link_alias_hook_enter_view_constructor` получает конструктор `ChatActivityEnterView(Activity, SizeNotifierFrameLayout, ChatActivity, Boolean.TYPE, Theme$ResourcesProvider)` и передаёт его в `self.hook_method(constructor, _LinkAliasEnterViewConstructorHook(self))`; после создания view на UI-потоке с задержкой 500 мс навешивается `CustomTextWatcher` на приватное поле `messageEditText`. При вводе строки, начинающейся с `!`, вызывается `_link_alias_show_matching_settings(search_key)`. Дополнительно метод `PluginCell.set(Plugin, PluginCellDelegate)` перехватывается для вставки бейджа `BETA` рядом с `pluginNameView` (строки 701 и 752, класс `_PluginCellSetHook` — 782–836), а ряд пилюль-фильтров строится в `_add_filter_pills` (1387–1421) и вставляется в список плагинов как `UItem.asFullyCustom(pills_container)` (503–511).
2. **Отправка сообщений и меню сообщений** — строки 4784–4803: сообщение собирается через `SendMessagesHelper.SendMessageParams.of(...)` и отправляется `get_send_messages_helper().sendMessage(params)` внутри `run_on_ui_thread`. Перехват меню сообщений выполняют `ChatActivity.fillMessageMenu(MessageObject, ArrayList, ArrayList, ArrayList)` (3704–3711) и `ChatActivity.processSelectedOption(int)` (3716–3720).
3. **Тема и форма пилюль** — строки 1441–1443 и 1686–1687: форма зависит от настройки-селектора `pill_shape_style` (варианты `Pill`/`Chips`, `default=0`, строка 140): радиус `AndroidUtilities.dp(16)` при значении 0 и `dp(8)` при 1. Цвета берутся из текущей темы через `Theme.getColor(...)` — `key_actionBarTabActiveText`, `key_actionBarTabUnactiveText`, `key_actionBarTabLine`, `key_windowBackgroundWhite`, `key_divider` (1691–1703), а также `key_windowBackgroundWhiteBlackText`/`GrayText` (316, 325) и `key_featuredStickers_addButton` для бейджа (756).
4. **Изоляция состояния и аккаунты** — строки 82–100: `LRUCache` и ссылки `weakref.ref(...)` создаются в `QuantaHut.__init__` как атрибуты экземпляра. Постоянные кэши — `JsonCacheFile` (файл в каталоге `./cache`, 2321–2357) и SQLite-класс `LocalizationDatabase` (`quantahut_localization.db`, таблицы `localization`, `emoji_cache`, `user_cache`, `text_template_cache`, 2372–2380); фактически используемое хранилище — `LocalizationDatabase` внутри модульного `github_localization`. Маршрутизация аккаунта: `get_account_instance()` (1052), `fragment.getCurrentAccount()` (3121), `UserConfig.selectedAccount` → `AccountInstance.getInstance(account)` → `getTopicsController().findTopic(...)` (4773–4777).
5. **Жизненный цикл** — строки 976–1015: `on_plugin_load()` (180–208) вызывает `setup_hooks()`, который через `_ensure_message_menu_hooks(self)` (643) регистрирует хуки меню в модульном `_message_menu_registry` (3695–3722, 3881–3882). `on_plugin_unload()` снимает все `self.hook_refs`, хуки поиска настроек, бейдж `BETA` и конструктор enter-view, но `cleanup_quantahut_hooks()` (3884–3885) не вызывается.

## Вызовы и наблюдаемые контракты

| Точка вызова | Сигнатура или call-site | Назначение | Доказательство |
|---|---|---|---|
| Конструктор enter view | `ChatActivityEnterView.getDeclaredConstructor(Activity, SizeNotifierFrameLayout, ChatActivity, Boolean.TYPE, ResourcesProvider)` → `hook_method(constructor, _LinkAliasEnterViewConstructorHook(self))` | Поиск настроек по `!`-префиксу в поле ввода | [quantahut.plugin:4242-4250](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L4242-L4250) |
| Триггер `!` | `if text.startswith("!") and len(text) > 1:` → `_link_alias_show_matching_settings(search_key)` | Разбор строки ввода и показ совпавших настроек | [quantahut.plugin:4285-4294](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L4285-L4294) |
| Подмена ячейки | `PluginCell.getDeclaredMethod("set", Plugin, PluginCellDelegate)`; `badge.setText("BETA")` | Бейдж `BETA` для плагинов с `__beta__ = "True"` | [quantahut.plugin:701](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L701-L701), [752](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L752-L752), [782-836](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L782-L836) |
| Ряд пилюль | `UItem.asFullyCustom(quantahut.pills_container)`; `items.add(insert_position, pills_item)` | Панель фильтров над списком плагинов | [quantahut.plugin:503-511](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L503-L511), [1387-1421](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L1387-L1421) |
| Счётчики пилюль | `pill.setText(f"{base_text} - {count}")` | Число плагинов в фильтре (не непрочитанные сообщения) | [quantahut.plugin:1673-1678](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L1673-L1678) |
| Прямая отправка | `SendMessagesHelper.SendMessageParams.of(...)`; `get_send_messages_helper().sendMessage(params)` | Отправка deep-link в текущий чат | [quantahut.plugin:4784-4803](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L4784-L4803) |
| Меню сообщений | `ChatActivity.getDeclaredMethod("fillMessageMenu", ...)`; `ChatActivity.getDeclaredMethod("processSelectedOption", Integer.TYPE)` | Регистрация пользовательских пунктов меню | [quantahut.plugin:3704-3720](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L3704-L3720) |
| Форма пилюль | `AndroidUtilities.dp(16) if pill_shape == 0 else AndroidUtilities.dp(8)` | Радиус `Pill` (0) против `Chips` (1) | [quantahut.plugin:1441-1443](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L1441-L1443) |
| Состояние экземпляра | `LRUCache(maxsize=128)`; `weakref.ref(self)` | Кеши и слабые ссылки без общего глобального состояния | [quantahut.plugin:82-100](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L82-L100) |
| Постоянные кэши | `JsonCacheFile`; `sqlite3.connect(.../quantahut_localization.db)` | JSON-файл в `./cache` и SQLite-локализация | [quantahut.plugin:2321-2357](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L2321-L2357), [2372-2380](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L2372-L2380) |
| Аккаунт | `UserConfig.selectedAccount`; `AccountInstance.getInstance(account)` | Определение аккаунта для `findTopic` при отправке | [quantahut.plugin:4773-4777](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L4773-L4777) |
| Загрузка | `on_plugin_load()` → `setup_hooks()` → `_ensure_message_menu_hooks(self)` | Регистрация хуков при включении | [quantahut.plugin:180-208](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L180-L208) |
| Выгрузка | `on_plugin_unload()`; `self.unhook_method(ref)` для `hook_refs` | Точечное снятие зарегистрированных хуков | [quantahut.plugin:976-1015](https://github.com/Kangel-Plugins/Plugins-Store/blob/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin#L976-L1015) |

## Границы и наблюдаемые особенности

- Перехват `fillMessageMenu`/`processSelectedOption` размещён в модульном `_message_menu_registry`, а handles лежат в его полях `_unhook_fill`/`_unhook_process`, вне `self.hook_refs`; `cleanup_quantahut_hooks()` определён, но в файле не вызывается — при выгрузке модульные хуки меню сообщений явно не снимаются.
- Ряд пилюль и бейдж `BETA` — разные элементы: бейдж встраивается внутрь `PluginCell`, панель пилюль — отдельный `UItem` над списком плагинов; `_update_pill_counts` считает плагины по фильтрам, а не непрочитанные сообщения.
- В файле нет обращений к символам `DialogsActivity`, `dialogsAdapter`, `unreadCount`, `getUnreadCount`: список чатов и счётчики непрочитанных не модифицируются. Хуки установлены на `PluginSettingsActivity`, `LaunchActivity`, `PluginsActivity`, `PluginCell`, `InstallPluginBottomSheet`, `ChatActivityEnterView`, `AndroidUtilities.openForView` и `ChatActivity`.
- `UserConfig.selectedAccount` (4773) — глобальный выбранный аккаунт, а не аккаунт входящего события; `get_account_instance()` и `fragment.getCurrentAccount()` применяются в отдельных местах.
- Состояние изолировано не полностью: помимо атрибутов экземпляра есть модульные синглтоны `github_localization` (2732) и `_message_menu_registry` (3878), а также глобальный `available_languages`.
- Проверка статическая: установка, запуск и проверка Hook API на конкретной сборке ExteraGram/AyuGram не выполнялись; совместимость с клиентом `>= 12.9.0` заявлена метаданными, но не подтверждена runtime.
