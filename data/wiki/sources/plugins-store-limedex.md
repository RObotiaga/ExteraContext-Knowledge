---
type: source
source_id: plugins-store-limedex
title: limedex (v2.5.7)
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 8cb930bf899079c56b07143b1f7209f7b25197ff
path: Plugins/limedex.eaf
version: 2.5.7
plugin_id: limedex
author: "@limeplug"
min_version: 12.9.0
platform: Android
review_status: accepted
review: ../reviews/plugins-store-limedex.md
date: 2026-10-03
---

# limedex (v2.5.7)

Источник: [Plugins/limedex.eaf](https://github.com/Kangel-Plugins/Plugins-Store/blob/8cb930bf899079c56b07143b1f7209f7b25197ff/Plugins/limedex.eaf).
Репозиторий: `Kangel-Plugins/Plugins-Store`.
Закреплённый commit: `8cb930bf899079c56b07143b1f7209f7b25197ff`.

## Проверенные сведения

1. Архитектура пакета Elyx (.eaf): `refmap.yml` в корне архива маршрутизирует метаданные `limedex/meta.yml`, точку входа `limedex/src/main.py`, ресурсы `limedex/res` и локали `limedex/locales`. [Plugins/limedex.eaf:1](https://github.com/Kangel-Plugins/Plugins-Store/blob/8cb930bf899079c56b07143b1f7209f7b25197ff/Plugins/limedex.eaf).
2. Метаданные `limedex/meta.yml`: `id: limedex`, `version: 2.5.7`, `author: @limeplug`, `app_version: ">=12.9.0"`, `sdk_version: ">=1.4.5.1"`, `pythonVer: "3.11"`, `compiled: false`. [Plugins/limedex.eaf:1](https://github.com/Kangel-Plugins/Plugins-Store/blob/8cb930bf899079c56b07143b1f7209f7b25197ff/Plugins/limedex.eaf).
3. Точки входа UI: `CHAT_ACTION_MENU` (`id=limedex_open`) и `DRAWER_MENU` (`id=limedex_drawer`, `priority=80`). [Plugins/limedex.eaf:1](https://github.com/Kangel-Plugins/Plugins-Store/blob/8cb930bf899079c56b07143b1f7209f7b25197ff/Plugins/limedex.eaf).
4. Двухуровневое кэширование: `context.getCacheDir()/limedex`, JSON-файлы, `OrderedDict` для поиска, `.part` файлы с валидацией magic bytes PNG/JPEG. [Plugins/limedex.eaf:1](https://github.com/Kangel-Plugins/Plugins-Store/blob/8cb930bf899079c56b07143b1f7209f7b25197ff/Plugins/limedex.eaf).
5. Жизненный цикл: `on_plugin_load` регистрирует меню, `on_plugin_unload` закрывает `view.dismiss()` и вызывает `remove_menu_item`. [Plugins/limedex.eaf:1](https://github.com/Kangel-Plugins/Plugins-Store/blob/8cb930bf899079c56b07143b1f7209f7b25197ff/Plugins/limedex.eaf).
