---
type: source
source_id: plugins-store-save-emoji
title: Save Emoji
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 97c33f6b986cf1aa44dd2b5f543dc6cb3a70baeb
path: Plugins/save_emoji.plugin
version: 1.1.0
plugin_id: save_emoji
author: "@uipurple"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-save-emoji.md
date: 2026-10-03
---

# Save Emoji

Исходный код плагина `save_emoji` из репозитория `Kangel-Plugins/Plugins-Store`, зафиксированный на commit `97c33f6b986cf1aa44dd2b5f543dc6cb3a70baeb`.

Файл: [Plugins/save_emoji.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/97c33f6b986cf1aa44dd2b5f543dc6cb3a70baeb/Plugins/save_emoji.plugin)

Плагин объявляет ID `save_emoji`, имя `Save Emoji`, версию `1.1.0`, автора `@uipurple` и ограничения версий приложения и SDK (`>=12.5.1` и `>=1.4.3.3`). В описании сказано, что он добавляет кнопку сохранения эмодзи и стикеров в папку «Загрузки» (строки 9–16).

При загрузке плагина вызывается `_load_dex()`, при выгрузке — `_unload_dex()` (строки 28–32). `_load_dex()` сначала вызывает `_unload_dex()`, декодирует встроенные Base64-данные, создаёт `InMemoryDexClassLoader`, загружает класс `saveemoji.SaveEmoji` и вызывает его метод `start` (строки 18, 34–42). `_unload_dex()` пытается вызвать метод `stop`, если класс загружен; исключения при этом подавляются, после чего ссылки на класс и загрузчик сбрасываются (строки 44–51).

Источник подтверждает заявленные метаданные и действия, непосредственно видимые в коде. Встроенный DEX здесь не декодировался и не анализировался, поэтому внутреннее поведение класса `saveemoji.SaveEmoji` этим описанием не устанавливается.
