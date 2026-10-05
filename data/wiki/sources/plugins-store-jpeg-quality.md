---
type: source
source_id: plugins-store-jpeg-quality
title: JPEG Quality Slider
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 25d32cf2b5a19280df07e2689ef2fce4d1db2656
path: Plugins/jpeg_quality.plugin
version: 2.1
plugin_id: jpeg_quality
author: "@dekma0091"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-jpeg-quality.md
date: 2026-10-03
---

# Источник: jpeg_quality.plugin

- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Зафиксированный commit: `25d32cf2b5a19280df07e2689ef2fce4d1db2656`
- Исходный файл: [Plugins/jpeg_quality.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf2b5a19280df07e2689ef2fce4d1db2656/Plugins/jpeg_quality.plugin)
- Версия плагина: `2.1`

## Подтверждённые факты

1. Base64-данные декодируются; затем предпринимается распаковка `zlib.decompress`. Ошибка распаковки игнорируется. [Строки 35–40](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf2b5a19280df07e2689ef2fce4d1db2656/Plugins/jpeg_quality.plugin#L35-L40).
2. DEX загружается через `InMemoryDexClassLoader`; в нём загружается класс `dev.extera.jpegquality.JpegQualityBridge`. [Строки 41–45](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf2b5a19280df07e2689ef2fce4d1db2656/Plugins/jpeg_quality.plugin#L41-L45).
3. `NativeBridge._invoke_static` использует `getDeclaredMethods()`, проверяет имя и число параметров, вызывает `setAccessible(True)` и затем статический метод. [Строки 66–78](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf2b5a19280df07e2689ef2fce4d1db2656/Plugins/jpeg_quality.plugin#L66-L78).
4. При сбое `attach()` вызывается `detach()`. Если откат успешен, сбрасывается `is_active`, после чего повторно выбрасывается исходная ошибка; `RuntimeError` формируется только при ошибке отката. [Строки 46–58](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf2b5a19280df07e2689ef2fce4d1db2656/Plugins/jpeg_quality.plugin#L46-L58).
5. `JpegQualityPlugin` связывает `bridge.start()` с `on_plugin_load()` и `bridge.stop()` с `on_plugin_unload()`. [Строки 81–99](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf2b5a19280df07e2689ef2fce4d1db2656/Plugins/jpeg_quality.plugin#L81-L99).
