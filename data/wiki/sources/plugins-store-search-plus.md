---
type: source
source_id: plugins-store-search-plus
title: "Search+ (search_plus)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: ad51ff05579edd2b5af08c4294aa455fb81a24da
path: "Plugins/search_plus.plugin"
artifact_sha256: 16aea984e3e00d4582e7047f9d34f15f0258372cedc88a85b3f3395067fb5462
plugin_id: "search_plus"
plugin_version: "2.6"
author: "@SearchPlusss"
min_version: "12.5.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-search-plus.md
date: "2026-10-03"
---

# Search+ (search_plus)

Исходный код плагина: [Plugins/search_plus.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff05579edd2b5af08c4294aa455fb81a24da/Plugins/search_plus.plugin).

Метаданные версии, автора и минимальной версии приложения сверены с `Plugins-Store/store.json`.

## Проверенные сведения

- Загрузка и отложенная установка хуков при холодном запуске: [Plugins/search_plus.plugin:1706-1723](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff05579edd2b5af08c4294aa455fb81a24da/Plugins/search_plus.plugin#L1706-L1723).
- Отслеживание внедрённых view через слабые ссылки WeakReference: [Plugins/search_plus.plugin:1747-1752](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff05579edd2b5af08c4294aa455fb81a24da/Plugins/search_plus.plugin#L1747-L1752).
- Очистка view, тегов и состояния восстановления фокуса на UI-потоке: [Plugins/search_plus.plugin:1761-1805](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff05579edd2b5af08c4294aa455fb81a24da/Plugins/search_plus.plugin#L1761-L1805).
- Поиск и установка хука `sendRequest`: [Plugins/search_plus.plugin:2110-2133](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff05579edd2b5af08c4294aa455fb81a24da/Plugins/search_plus.plugin#L2110-L2133).
- Выгрузка плагина и снятие хуков: [Plugins/search_plus.plugin:1808-1830](https://github.com/Kangel-Plugins/Plugins-Store/blob/ad51ff05579edd2b5af08c4294aa455fb81a24da/Plugins/search_plus.plugin#L1808-L1830).

Все ссылки на исходный код в этой записи закреплены за commit `ad51ff05579edd2b5af08c4294aa455fb81a24da`.
