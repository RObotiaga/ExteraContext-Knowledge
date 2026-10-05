---
type: source
source_id: plugins-store-advanced-search
title: Advanced Search
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 4ddb6c2f0fcf6d623a35f299f24ba8fbe640e70b
path: Plugins/advanced_search.plugin
version: 1.2
plugin_id: advanced_search
author: "@dekma0091"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-advanced-search.md
date: 2026-10-03
---

# Plugins Store: advanced_search

Источник: [Plugins/advanced_search.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/4ddb6c2f0fcf6d623a35f299f24ba8fbe640e70b/Plugins/advanced_search.plugin).  
Репозиторий: `Kangel-Plugins/Plugins-Store`  
Зафиксированный commit: `4ddb6c2f0fcf6d623a35f299f24ba8fbe640e70b`

## Проверенные факты

1. **Метаданные** — строки 1–5: ID `advanced_search`, версия `1.2`, автор `@dekma0091`; описание: «Продвинутый поиск по чатам, документам с различными фильтрами».
2. **Загрузка DEX** — строки 58–85: встроенная строка декодируется из Base64; выполняется попытка распаковки zlib с использованием исходных байтов при ошибке. Сначала используется `InMemoryDexClassLoader`, затем, если загрузка этим способом завершается ошибкой, — `DexClassLoader`.
3. **Класс точки входа** — строка 37: `ni.dekma.advanced_search.AdvancedSearchBridge`.
4. **Выбор языка** — строки 20–32: сначала вызывается `LocaleController.getLocaleStringIso639()`. Если это не удаётся или возвращается пустое значение, используется `Locale.getDefault().getLanguage()`.
5. **Жизненный цикл** — строки 129–138 и 144–149: `on_plugin_load` вызывает `self.bridge.load()`, а `on_plugin_unload` вызывает `self.bridge.unload()`.
