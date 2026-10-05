---
type: source
source_id: plugins-store-bot-tags
title: Bot Tags
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: efd7ae3b6a22f3020aa0f55cf64d36eb10f60c4a
path: Plugins/bot_tags.plugin
version: 1.0.0
plugin_id: bot_tags
author: "@cobra_S0FT | @excess_plugins"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-bot-tags.md
date: 2026-10-03
---

# Bot Tags

Исходный код плагина: [Plugins/bot_tags.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae3b6a22f3020aa0f55cf64d36eb10f60c4a/Plugins/bot_tags.plugin).

## Проверенные сведения

1. Регистрация хука отправки сообщений `add_on_send_message_hook` и использование `HookStrategy.MODIFY` / `CANCEL`: [строки 37–40](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae3b6a22f3020aa0f55cf64d36eb10f60c4a/Plugins/bot_tags.plugin#L37-L40).
2. Вычисление длины в UTF-16 code units через `_u16len` (`utf-16-le` с `surrogatepass`) и расчет сдвига: [строки 33–35](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae3b6a22f3020aa0f55cf64d36eb10f60c4a/Plugins/bot_tags.plugin#L33-L35).
3. Коррекция смещения и ограничение длины entities через `_shift_entities` и `_clamp_entities`: [строки 62–85](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae3b6a22f3020aa0f55cf64d36eb10f60c4a/Plugins/bot_tags.plugin#L62-L85).
4. Внутричатовая конфигурация через команды `.tag` и `.тег` с `reload_settings=True` в `set_setting`: [строки 48–57](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae3b6a22f3020aa0f55cf64d36eb10f60c4a/Plugins/bot_tags.plugin#L48-L57).
5. Отображение уведомлений `BulletinHelper.show_info` через `run_on_ui_thread`: [строки 59–60](https://github.com/Kangel-Plugins/Plugins-Store/blob/efd7ae3b6a22f3020aa0f55cf64d36eb10f60c4a/Plugins/bot_tags.plugin#L59-L60).
