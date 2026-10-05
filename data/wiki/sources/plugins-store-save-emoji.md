---
type: source
source_id: plugins-store-save-emoji
title: "Save Emoji"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 97c33f63831619c95748edf7a52ec91b88da3151
path: "Plugins/save_emoji.plugin"
artifact_sha256: 9bbff8af727d3cf8d760fc46fb8e0eb2ecf52243c45c20a9130ba253df6252c6
plugin_id: "save_emoji"
plugin_version: "1.1.0"
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
review: ../reviews/plugins-store-save-emoji.md
date: "2026-10-03"
---

# Save Emoji

Исходный код плагина `save_emoji` из репозитория `Kangel-Plugins/Plugins-Store`, зафиксированный на commit `97c33f63831619c95748edf7a52ec91b88da3151`.

Файл: [Plugins/save_emoji.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/97c33f63831619c95748edf7a52ec91b88da3151/Plugins/save_emoji.plugin)

Плагин объявляет ID `save_emoji`, имя `Save Emoji`, версию `1.1.0`, автора `@uipurple` и ограничения версий приложения и SDK (`>=12.5.1` и `>=1.4.3.3`). В описании сказано, что он добавляет кнопку сохранения эмодзи и стикеров в папку «Загрузки» (строки 9–16).

При загрузке плагина вызывается `_load_dex()`, при выгрузке — `_unload_dex()` (строки 28–32). `_load_dex()` сначала вызывает `_unload_dex()`, декодирует встроенные Base64-данные, создаёт `InMemoryDexClassLoader`, загружает класс `saveemoji.SaveEmoji` и вызывает его метод `start` (строки 18, 34–42). `_unload_dex()` пытается вызвать метод `stop`, если класс загружен; исключения при этом подавляются, после чего ссылки на класс и загрузчик сбрасываются (строки 44–51).

Источник подтверждает заявленные метаданные и действия, непосредственно видимые в коде. Встроенный DEX здесь не декодировался и не анализировался, поэтому внутреннее поведение класса `saveemoji.SaveEmoji` этим описанием не устанавливается.
