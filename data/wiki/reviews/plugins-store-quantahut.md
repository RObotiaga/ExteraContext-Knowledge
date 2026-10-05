---
type: review
source_id: plugins-store-quantahut
reviewer: verifier
repository: Kangel-Plugins/Plugins-Store
commit: d0efb7b72bcac954d97af04670d6492900ade596
plugin_id: quantahut
review_status: accepted
date: 2026-10-05
---

# Ревью: Plugins Store `quantahut` (QuantaHut 1.5.4)

Сборщик предоставил 5 фактов. Принято 5 фактов.

## Проверка происхождения

- Закреплённый commit `d0efb7b72bcac954d97af04670d6492900ade596` существует: GitHub API возвращает HTTP 200, сообщение `Update plugin: quantahut v1.5.4`, дата 2026-10-02T17:02:16Z. Файл на этом SHA доступен по raw-URL.
- Независимо скачанный `https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/d0efb7b72bcac954d97af04670d6492900ade596/Plugins/quantahut.plugin` побайтово совпадает с файлом в локальном клоне: 214541 байт, SHA-256 `6d77ec8e97925d069c7561e1bb5828e69fed115e565dd93fbb6ad9ea65f1a307`.
- Git-идентификаторы совпадают: `git rev-parse d0efb7b...:Plugins/quantahut.plugin` = `git rev-parse HEAD:Plugins/quantahut.plugin` = `f1ecf88928b7198bdfe74cbadf7ac1b8c86e1ebd`; `git diff` закреплённой ревизии против рабочей копии по этому файлу пуст.
- SHA-256 и версия совпадают с записью `quantahut` в `store.json` (`version: 1.5.4`, `min_version: 12.9.0`, `status: library`, `hash: 6d77ec8e...`). Метаданные в файле: строки 40–50 (`__version__ = "1.5.4"`, `__min_version__ = "12.9.0"`, `__requirements__ = "cachetools"`, `__id__ = "quantahut"`).

## Верификация фактов

| ID | Вердикт | Проверка и уточнения |
|---|---|---|
| `quantahut-001` | Принят | Хук конструктора `ChatActivityEnterView` подтверждён строками 4242–4250, привязка `TextWatcher` к `messageEditText` — 4262–4295, условие `text.startswith("!")` — 4285–4287. Перехват `PluginCell.set` подтверждён строками 701 и 782–836, литерал `BETA` — строка 752. Уточнение: «ряд пилюль» не является частью `PluginCell` — панель `pills_container` вставляется отдельным `UItem.asFullyCustom` в список плагинов (503–511, 1387–1421), а бейдж `BETA` встраивается внутрь ячейки. Отрицательная часть подтверждается отсутствием в файле символов `DialogsActivity`, `dialogsAdapter`, `unreadCount`, `getUnreadCount`; это статическое наблюдение, а не runtime-гарантия. |
| `quantahut-002` | Принят | `SendMessagesHelper.SendMessageParams.of(...)` (14 позиционных аргументов) — 4784–4799, `get_send_messages_helper()` — 4801, `sendMessage(params)` под `run_on_ui_thread` — 4803. Хуки `fillMessageMenu(MessageObject, ArrayList, ArrayList, ArrayList)` и `processSelectedOption(int)` подтверждены строками 3704–3720. Уточнение: вызовы выполняются асинхронно на UI-потоке, а не синхронно в момент формирования пункта меню. |
| `quantahut-003` | Принят | Селектор `pill_shape_style` (`Pill`/`Chips`, `default=0`) — строка 140; радиусы `dp(16)`/`dp(8)` — 1441–1443 и 1686–1687. `Theme.getColor(...)` подтверждён в строках 316, 325, 756, 1691–1703 (всего в файле десятки обращений). |
| `quantahut-004` | Принят | `LRUCache`/`weakref` как атрибуты экземпляра — 82–100 и объекты-хуки (704, 2290, 4194). `JsonCacheFile` — 2321–2357, `LocalizationDatabase` (SQLite, `quantahut_localization.db`) — 2372–2380; `UserConfig.selectedAccount` → `AccountInstance.getInstance` — 4773–4777, `fragment.getCurrentAccount()` — 3121, `get_account_instance()` — 1052. Уточнения: `JsonCacheFile` экспортируется через `__all__` (3106), но внутри файла не инстанцируется — фактическое постоянное хранилище это SQLite через `github_localization` (2732); изоляция частичная, так как `_message_menu_registry` (3878) и `github_localization` — модульные синглтоны. `UserConfig.selectedAccount` — глобальный выбор интерфейса, а не аккаунт события (каноническое правило `event-account`). |
| `quantahut-005` | Принят | `on_plugin_load()` (180–208) → `setup_hooks()` (641–647) → `_ensure_message_menu_hooks(self)` (643) → `_message_menu_registry.ensure_hooks(plugin)` (3881–3882), handles сохраняются в `_unhook_fill`/`_unhook_process` (3711, 3720). `on_plugin_unload()` (976–1015) снимает `self.hook_refs`, `settings_search_*`, бейдж и link-alias конструктор. Уточнение подтверждено: `cleanup_quantahut_hooks()` определён (3884–3885), но не вызывается ни в этом файле, ни в `on_plugin_unload`, поэтому модульные хуки `fillMessageMenu`/`processSelectedOption` явно не снимаются. Согласно официальному SDK, `hook_method` требует ручного сохранения и снятия выданных handles, так что при повторном включении плагина возможна повторная регистрация. |

## Проверка повторов

- ID уникальны: `plugins-store-quantahut:quantahut-001..005`; в `facts.json` префикса `plugins-store-quantahut` до этой записи не было.
- Упоминания `quantahut` в существующей базе относятся только к импорту библиотеки сторонним плагином `memory_monitor.plugin` (факт `plugins-store-automation-tools:fact-023` про `restart_app`), а не к устройству самого QuantaHut; дословных повторов пять новых фактов не создают.
- Факты разнесены по каноническим темам `ui`, `requests`, `storage`, `lifecycle` и описывают разные механизмы: интерфейс, отправку, хранение, жизненный цикл.

## Остаточные пробелы и вердикт

Проверка статическая: сборка, установка, включение/выключение и повторная загрузка на устройстве с клиентом `>= 12.9.0` и `cachetools` не выполнялись, runtime-подтверждений нет. Не разбирались не входящие в пять утверждений участки: импорт/экспорт бэкапов и плагинов (`.backup`, `.plugins`), сетевые запросы локализации, диалоги импорта и экспорта настроек. Доступность внутренних классов Telegram (`PluginCell`, `ChatActivityEnterView`, `ChatActivity.fillMessageMenu`, `SendMessagesHelper.SendMessageParams`) привязана к конкретной сборке клиента и не гарантируется закреплённым SHA плагина.

**Вердикт: `accepted`.** Все пять фактов подтверждены исходником на закреплённом commit; уточнения касаются структуры UI (пилюли и бейдж — разные элементы), фактического постоянного хранилища (SQLite, а не `JsonCacheFile`) и явного пробела очистки модульных хуков меню сообщений.
