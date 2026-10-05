---
type: source
source_id: plugins-store-search-plus
title: "Search+ (search_plus)"
source_type: "code"
repository: "Kangel-Plugins/Plugins-Store"
commit: "ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a"
path: "Plugins/search_plus.plugin"
plugin_id: "search_plus"
plugin_version: "2.6"
author: "@SearchPlusss"
min_version: "12.5.1"
platform: Android
review_status: accepted
review: ../reviews/plugins-store-search-plus.md
date: 2026-10-03
---

# Search+ (search_plus)

Исходный код плагина: [Plugins/search_plus.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a/Plugins/search_plus.plugin).

Метаданные версии, автора и минимальной версии приложения сверены с `Plugins-Store/store.json`.

## Проверенные сведения

- Загрузка и отложенная установка хуков при холодном запуске: [Plugins/search_plus.plugin:1706-1723](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a/Plugins/search_plus.plugin#L1706-L1723).
- Отслеживание внедрённых view через слабые ссылки WeakReference: [Plugins/search_plus.plugin:1747-1752](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a/Plugins/search_plus.plugin#L1747-L1752).
- Очистка view, тегов и состояния восстановления фокуса на UI-потоке: [Plugins/search_plus.plugin:1761-1805](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a/Plugins/search_plus.plugin#L1761-L1805).
- Поиск и установка хука `sendRequest`: [Plugins/search_plus.plugin:2110-2133](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a/Plugins/search_plus.plugin#L2110-L2133).
- Выгрузка плагина и снятие хуков: [Plugins/search_plus.plugin:1808-1830](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a/Plugins/search_plus.plugin#L1808-L1830).

Все ссылки на исходный код в этой записи закреплены за commit `ad51ff088f1dcbe1a7b0fc5678887bfe7dfa4e0a`.
