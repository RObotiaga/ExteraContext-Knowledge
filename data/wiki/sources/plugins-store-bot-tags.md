---
type: source
source_id: plugins-store-bot-tags
title: "Bot Tags"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: efd7ae39edca5bcf33919884888a75f6ce8529b1
path: "Plugins/bot_tags.plugin"
artifact_sha256: 4de9e922b4029540201e121e0a2e9dbdc02272b2bc1d7b37f12fa19d771977b7
plugin_id: "bot_tags"
plugin_version: "1.0.0"
author: "@cobra_S0FT | @excess_plugins"
min_version: "12.5.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-bot-tags.md
date: "2026-10-03"
---

# Bot Tags

Исходный код плагина: [Plugins/bot_tags.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae39edca5bcf33919884888a75f6ce8529b1/Plugins/bot_tags.plugin).

## Проверенные сведения

1. Регистрация хука отправки сообщений `add_on_send_message_hook` и использование `HookStrategy.MODIFY` / `CANCEL`: [строки 37–40](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae39edca5bcf33919884888a75f6ce8529b1/Plugins/bot_tags.plugin#L37-L40).
2. Вычисление длины в UTF-16 code units через `_u16len` (`utf-16-le` с `surrogatepass`) и расчет сдвига: [строки 33–35](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae39edca5bcf33919884888a75f6ce8529b1/Plugins/bot_tags.plugin#L33-L35).
3. Коррекция смещения и ограничение длины entities через `_shift_entities` и `_clamp_entities`: [строки 62–85](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae39edca5bcf33919884888a75f6ce8529b1/Plugins/bot_tags.plugin#L62-L85).
4. Внутричатовая конфигурация через команды `.tag` и `.тег` с `reload_settings=True` в `set_setting`: [строки 48–57](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae39edca5bcf33919884888a75f6ce8529b1/Plugins/bot_tags.plugin#L48-L57).
5. Отображение уведомлений `BulletinHelper.show_info` через `run_on_ui_thread`: [строки 59–60](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae39edca5bcf33919884888a75f6ce8529b1/Plugins/bot_tags.plugin#L59-L60).
