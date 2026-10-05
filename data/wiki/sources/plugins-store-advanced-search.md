---
type: source
source_id: plugins-store-advanced-search
title: "Plugins Store: advanced_search"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 4ddb6c27adbc0714a2adc48e0417ebdffd22128f
path: "Plugins/advanced_search.plugin"
artifact_sha256: aee561b7e1a34ae719b567b9b41389f2e7141cf80ce4f81374b72901e7a9761c
plugin_id: "advanced_search"
plugin_version: "1.2"
author: "@dekma0091"
min_version: ">=12.5.1"
app_version: ">=12.5.1"
sdk_version: ">=1.4.0"
platform: Android
evidence_status: code
review_status: accepted
collector_model: "gpt-6-luna"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-advanced-search.md
date: "2026-10-03"
---

# Plugins Store: advanced_search

Источник: [Plugins/advanced_search.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/4ddb6c27adbc0714a2adc48e0417ebdffd22128f/Plugins/advanced_search.plugin).  
Репозиторий: `Kangel-Plugins/Plugins-Store`  
Зафиксированный commit: `4ddb6c27adbc0714a2adc48e0417ebdffd22128f`

## Проверенные факты

1. **Метаданные** — строки 1–5: ID `advanced_search`, версия `1.2`, автор `@dekma0091`; описание: «Продвинутый поиск по чатам, документам с различными фильтрами».
2. **Загрузка DEX** — строки 58–85: встроенная строка декодируется из Base64; выполняется попытка распаковки zlib с использованием исходных байтов при ошибке. Сначала используется `InMemoryDexClassLoader`, затем, если загрузка этим способом завершается ошибкой, — `DexClassLoader`.
3. **Класс точки входа** — строка 37: `ni.dekma.advanced_search.AdvancedSearchBridge`.
4. **Выбор языка** — строки 20–32: сначала вызывается `LocaleController.getLocaleStringIso639()`. Если это не удаётся или возвращается пустое значение, используется `Locale.getDefault().getLanguage()`.
5. **Жизненный цикл** — строки 129–138 и 144–149: `on_plugin_load` вызывает `self.bridge.load()`, а `on_plugin_unload` вызывает `self.bridge.unload()`.
