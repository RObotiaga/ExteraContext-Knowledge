---
type: source
source_id: plugins-store-plugstonav
title: "Plugins Tab (plugstonav)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 5a4efa002a7a85a232063849dc11f4c6ce7a730f
path: "Plugins/plugstonav.plugin"
artifact_sha256: 700fdf19b33142da8e3787917595ff818bcbddd1a4703a73e96957e86f00f355
plugin_id: "plugstonav"
plugin_version: "1.3.1"
author: "@limeplug"
min_version: ">=12.5.1"
app_version: ">=12.5.1"
sdk_version: ">=1.4.4.3"
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-plugstonav.md
date: "2026-10-03"
---

# Plugins Tab (plugstonav)

Исходный код плагина `plugstonav` версии 1.3.1 из репозитория `Kangel-Plugins/Plugins-Store` на закреплённом коммите `5a4efa002a7a85a232063849dc11f4c6ce7a730f`.

Файл: [Plugins/plugstonav.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/5a4efa002a7a85a232063849dc11f4c6ce7a730f/Plugins/plugstonav.plugin).

## Проверенные сведения

1. Защита SDK guard `BuildVersion.SDK_INT >= 26` перед использованием `InMemoryDexClassLoader`: [строки 35–39](https://github.com/Kangel-Plugins/Plugins-Store/blob/5a4efa002a7a85a232063849dc11f4c6ce7a730f/Plugins/plugstonav.plugin#L35-L39).
2. `_read_payload()` собирает содержимое между DEX-маркерами, декодирует Base64 и декомпрессирует через zlib; `load()` передаёт ByteBuffer в `InMemoryDexClassLoader`: [строки 37–43, 84–101](https://github.com/Kangel-Plugins/Plugins-Store/blob/5a4efa002a7a85a232063849dc11f4c6ce7a730f/Plugins/plugstonav.plugin#L37-L43).
3. `_invoke()` использует `getDeclaredMethods()` с фильтрацией по имени и числу параметров и проверкой однозначности: [строки 67–82](https://github.com/Kangel-Plugins/Plugins-Store/blob/5a4efa002a7a85a232063849dc11f4c6ce7a730f/Plugins/plugstonav.plugin#L67-L82).
4. Входной класс — `com.extera.plugins.plugstonav.PluginsNavBridge`; `on_plugin_load()` вызывает `self.dex.load()`: [строки 16, 104–115](https://github.com/Kangel-Plugins/Plugins-Store/blob/5a4efa002a7a85a232063849dc11f4c6ce7a730f/Plugins/plugstonav.plugin#L16-L16).
5. `Dex.unload()` сбрасывает `loaded` в `finally`; `on_plugin_unload()` перехватывает исключение и пишет его в лог: [строки 59–65, 116–121](https://github.com/Kangel-Plugins/Plugins-Store/blob/5a4efa002a7a85a232063849dc11f4c6ce7a730f/Plugins/plugstonav.plugin#L59-L65).
