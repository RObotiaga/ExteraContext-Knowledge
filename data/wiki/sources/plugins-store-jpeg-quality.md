---
type: source
source_id: plugins-store-jpeg-quality
title: "Источник: jpeg_quality.plugin"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 25d32cf5ddc45d905120f9a83116667d1ac03f46
path: "Plugins/jpeg_quality.plugin"
artifact_sha256: b34d7ca3114625957e6d569bc003d912d93237966818a5b59ea3419a166ae0b7
plugin_id: "jpeg_quality"
plugin_version: "2.1"
author: "@dekma0091"
min_version: "12.5.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-jpeg-quality.md
date: "2026-10-03"
---

# Источник: jpeg_quality.plugin

- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Зафиксированный commit: `25d32cf5ddc45d905120f9a83116667d1ac03f46`
- Исходный файл: [Plugins/jpeg_quality.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf5ddc45d905120f9a83116667d1ac03f46/Plugins/jpeg_quality.plugin)
- Версия плагина: `2.1`

## Подтверждённые факты

1. Base64-данные декодируются; затем предпринимается распаковка `zlib.decompress`. Ошибка распаковки игнорируется. [Строки 35–40](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf5ddc45d905120f9a83116667d1ac03f46/Plugins/jpeg_quality.plugin#L35-L40).
2. DEX загружается через `InMemoryDexClassLoader`; в нём загружается класс `dev.extera.jpegquality.JpegQualityBridge`. [Строки 41–45](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf5ddc45d905120f9a83116667d1ac03f46/Plugins/jpeg_quality.plugin#L41-L45).
3. `NativeBridge._invoke_static` использует `getDeclaredMethods()`, проверяет имя и число параметров, вызывает `setAccessible(True)` и затем статический метод. [Строки 66–78](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf5ddc45d905120f9a83116667d1ac03f46/Plugins/jpeg_quality.plugin#L66-L78).
4. При сбое `attach()` вызывается `detach()`. Если откат успешен, сбрасывается `is_active`, после чего повторно выбрасывается исходная ошибка; `RuntimeError` формируется только при ошибке отката. [Строки 46–58](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf5ddc45d905120f9a83116667d1ac03f46/Plugins/jpeg_quality.plugin#L46-L58).
5. `JpegQualityPlugin` связывает `bridge.start()` с `on_plugin_load()` и `bridge.stop()` с `on_plugin_unload()`. [Строки 81–99](https://github.com/Kangel-Plugins/Plugins-Store/blob/25d32cf5ddc45d905120f9a83116667d1ac03f46/Plugins/jpeg_quality.plugin#L81-L99).
