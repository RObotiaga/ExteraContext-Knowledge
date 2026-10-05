---
type: review
source_id: plugins-store-search-plus
title: "Search+ (search_plus)"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: ad51ff05579edd2b5af08c4294aa455fb81a24da
artifact_sha256: 16aea984e3e00d4582e7047f9d34f15f0258372cedc88a85b3f3395067fb5462
plugin_id: "search_plus"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью Search+ (search_plus)

Сборщик предоставил 5 фактов. Принято 5 фактов.

Все пять утверждений сверены с исходным кодом `Plugins/search_plus.plugin`.

| Факт | Решение | Результат проверки |
|---|---|---|
| `search-plus-001` | Одобрить | Подтверждено: задержка вычисляется как 10000 - uptime_ms при uptime_ms < 10000; при ошибке применяется fallback 120000. Строки 1706–1723. |
| `search-plus-002` | Одобрить | Подтверждено: метод хранит слабые ссылки и на parent, и на view; перед добавлением очищает записи с уже недоступным view. Строки 1747–1752. |
| `search-plus-003` | Одобрить | Подтверждено: очистка выполняется через _native_run_on_ui_thread; восстановление focus listener и снятие watcher происходят, если сохранённые объекты доступны. Строки 1761–1805. |
| `search-plus-004` | Одобрить | Подтверждено: хук устанавливается на подходящие перегрузки ConnectionsManager.sendRequest, выбранные по параметрам TLObject и RequestDelegate. Строки 2110–2133. |
| `search-plus-005` | Одобрить | Подтверждено: сбрасываются флаги, хранилище и токены; plugin_instance обнуляется только при совпадении с выгружаемым экземпляром. Строки 1808–1830. |

Проверены метаданные `version: 2.6`, `author: @SearchPlusss` и `min_version: 12.5.1` в `Plugins-Store/store.json`. Ссылки на код привязаны к указанному commit и содержат точные диапазоны строк.
