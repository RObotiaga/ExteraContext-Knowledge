---
type: review
source_id: plugins-store-advanced-search
reviewer: verifier
repository: Kangel-Plugins/Plugins-Store
commit: 4ddb6c2f0fcf6d623a35f299f24ba8fbe640e70b
plugin_id: advanced_search
review_status: accepted
date: 2026-10-03
---

# Ревью: Plugins Store `advanced_search`

Проверен источник `Plugins/advanced_search.plugin` в commit `4ddb6c2f0fcf6d623a35f299f24ba8fbe640e70b`.

Сборщик предоставил 5 фактов. Принято 5 фактов.

Все пять утверждений подтверждены соответствующими строками файла. Уточнение к факту о загрузке DEX: распаковка zlib — попытка; при исключении используются исходные декодированные байты. Загрузка через `DexClassLoader` предусмотрена как резервный путь при ошибке ветки с `InMemoryDexClassLoader`.

| ID | Вердикт | Проверка |
|---|---|---|
| `advanced-search-001` | Принят | Метаданные подтверждены строками 1–5. |
| `advanced-search-002` | Принят | Загрузка DEX с fallback на DexClassLoader подтверждена строками 58–85. |
| `advanced-search-003` | Принят | Имя класса ENTRY_CLASS подтверждено строкой 37. |
| `advanced-search-004` | Принят | Логика выбора языка подтверждена строками 20–32. |
| `advanced-search-005` | Принят | Вызовы load/unload в жизненном цикле подтверждены строками 129–149. |
