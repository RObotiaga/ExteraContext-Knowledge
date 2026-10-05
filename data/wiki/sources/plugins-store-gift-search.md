---
type: source
source_id: plugins-store-gift-search
title: "Источник: Gift Search"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 948a85533a5d5aa85453cf412204b11265471350
path: "Plugins/gift_search.plugin"
artifact_sha256: 3ed5e78fa51fa4e56af3a71599986d0978a8c6f0918256ffce5b9d68340f436e
plugin_id: "gift_search"
plugin_version: "1.0.1r"
author: "@uipurple"
min_version: ">=12.5.1"
app_version: ">=12.5.1"
sdk_version: ">=1.4.3.3"
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-gift-search.md
date: "2026-10-03"
---

# Источник: Gift Search

- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Файл: `Plugins/gift_search.plugin`
- Версия плагина: `1.0.1r`
- Проверенный commit: `948a85533a5d5aa85453cf412204b11265471350`
- Pinned URL: [Plugins/gift_search.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/948a85533a5d5aa85453cf412204b11265471350/Plugins/gift_search.plugin)

## Проверенные наблюдения

1. Встроенный DEX декодируется из base64, передаётся в `InMemoryDexClassLoader` через `ByteBuffer`, после чего загружается `giftsearch.HooksInjection`. Вызов `start()` выполняется после загрузки класса. [Строки 235–243](https://github.com/Kangel-Plugins/Plugins-Store/blob/948a85533a5d5aa85453cf412204b11265471350/Plugins/gift_search.plugin#L235-L243).
2. Выгрузка вызывает DEX-метод `stop()`, затем сбрасывает `dex_class` и `dex_loader` в `None`. Перед повторной загрузкой вызывается та же очистка. [Строки 235–249](https://github.com/Kangel-Plugins/Plugins-Store/blob/948a85533a5d5aa85453cf412204b11265471350/Plugins/gift_search.plugin#L235-L249).
3. Экран настроек включает условный `Custom(view=preview)` и пункты-подэкраны с `create_sub_fragment`; фабрики подэкранов возвращают `Custom(view=v)`, если view существует. [Строки 55–83, 105–111](https://github.com/Kangel-Plugins/Plugins-Store/blob/948a85533a5d5aa85453cf412204b11265471350/Plugins/gift_search.plugin#L55-L83).
4. `_make_view()` перебирает методы DEX-класса, выбирает метод по имени и вызывает его через `invoke(None, ctx)`. Контекст берётся из `get_last_fragment().getParentActivity()` с fallback на `ApplicationLoader.applicationContext`. [Строки 85–100](https://github.com/Kangel-Plugins/Plugins-Store/blob/948a85533a5d5aa85453cf412204b11265471350/Plugins/gift_search.plugin#L85-L100).
5. `ButtonTouchListener` — dynamic proxy для `View.OnTouchListener`; он передаёт события callback-функции. Обработчик кнопки выполняет анимацию масштаба 0.965 на нажатии и возвращает масштаб к 1.0 при отпускании или отмене; обработчик возвращает `False`. [Строки 32–39, 224–233](https://github.com/Kangel-Plugins/Plugins-Store/blob/948a85533a5d5aa85453cf412204b11265471350/Plugins/gift_search.plugin#L32-L39).
