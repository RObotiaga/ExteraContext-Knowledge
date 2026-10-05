---
type: review
source_id: plugins-store-advanced-search
title: "Plugins Store: advanced_search"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 4ddb6c27adbc0714a2adc48e0417ebdffd22128f
artifact_sha256: aee561b7e1a34ae719b567b9b41389f2e7141cf80ce4f81374b72901e7a9761c
plugin_id: "advanced_search"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: Plugins Store `advanced_search`

Проверен источник `Plugins/advanced_search.plugin` в commit `4ddb6c27adbc0714a2adc48e0417ebdffd22128f`.

Сборщик предоставил 5 фактов. Принято 5 фактов.

Все пять утверждений подтверждены соответствующими строками файла. Уточнение к факту о загрузке DEX: распаковка zlib — попытка; при исключении используются исходные декодированные байты. Загрузка через `DexClassLoader` предусмотрена как резервный путь при ошибке ветки с `InMemoryDexClassLoader`.

| ID | Вердикт | Проверка |
|---|---|---|
| `advanced-search-001` | Принят | Метаданные подтверждены строками 1–5. |
| `advanced-search-002` | Принят | Загрузка DEX с fallback на DexClassLoader подтверждена строками 58–85. |
| `advanced-search-003` | Принят | Имя класса ENTRY_CLASS подтверждено строкой 37. |
| `advanced-search-004` | Принят | Логика выбора языка подтверждена строками 20–32. |
| `advanced-search-005` | Принят | Вызовы load/unload в жизненном цикле подтверждены строками 129–149. |
