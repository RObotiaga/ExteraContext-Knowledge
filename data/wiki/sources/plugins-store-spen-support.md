---
type: source
source_id: plugins-store-spen-support
title: Samsung S-Pen Support
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 69d079633e72ecab76f8373a6a9be777f98fbdf3
path: Plugins/spen_support.plugin
version: 1.6.0
plugin_id: spen_support
author: "@huecoder"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-spen-support.md
date: 2026-10-03
---

# Источник: Samsung S-Pen Support

- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Файл: `Plugins/spen_support.plugin`
- Проверяемая версия: `1.6.0`
- Проверяемый commit: `69d079633e72ecab76f8373a6a9be777f98fbdf3`
- Pinned source: [Plugins/spen_support.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/69d079633e72ecab76f8373a6a9be777f98fbdf3/Plugins/spen_support.plugin)

## Проверенные факты

1. Стилус распознаётся по `TOOL_TYPE_STYLUS = 2`. Маска кнопки — `BUTTON_SECONDARY | BUTTON_STYLUS_PRIMARY` (2 | 32). Действия Samsung Pen 211–214 преобразуются в `ACTION_DOWN`, `ACTION_UP`, `ACTION_MOVE`, `ACTION_CANCEL` соответственно. [Строки 30–50, 70–75, 126–128](https://github.com/Kangel-Plugins/Plugins-Store/blob/69d079633e72ecab76f8373a6a9be777f98fbdf3/Plugins/spen_support.plugin#L30-L50).
2. Плагин устанавливает хуки на `Activity.dispatchTouchEvent` и `Activity.dispatchGenericMotionEvent`. Метод `ChatMessageCell.checkTextSelection` ищется рефлексией, делается доступным и вызывается через `invoke` с `MotionEvent`. [Строки 201–206, 215–225, 397–413](https://github.com/Kangel-Plugins/Plugins-Store/blob/69d079633e72ecab76f8373a6a9be777f98fbdf3/Plugins/spen_support.plugin#L201-L206).
3. Для двойного касания с кнопкой пера используется интервал менее 400 мс и порог расстояния менее 100 px по каждой координате; при совпадении плагин пытается выделить весь текст. Выбор сообщений начинается при касании с кнопкой пера и продолжается обработкой drag-событий до `ACTION_UP` или `ACTION_CANCEL`. [Строки 58–59, 131–151, 323–338, 374–395](https://github.com/Kangel-Plugins/Plugins-Store/blob/69d079633e72ecab76f8373a6a9be777f98fbdf3/Plugins/spen_support.plugin#L323-L338).
4. В метаданных заданы `__permissions__ = ["hooks"]`, `__app_version__ = ">=12.5.1"` и `__sdk_version__ = ">=1.4.4.3"`. [Строки 18–22](https://github.com/Kangel-Plugins/Plugins-Store/blob/69d079633e72ecab76f8373a6a9be777f98fbdf3/Plugins/spen_support.plugin#L18-L22).
5. Синтетические и копированные `MotionEvent` освобождаются вызовом `recycle()` в `finally`. В `select_text_at` событие также освобождается в `finally`; там же `drawSelectionBackground` возвращается в `false`, если плагин временно включил это поле. `movingHandle` и `isOneTouch` изменяются вне `finally`. [Строки 312–321, 379–395, 407–415, 434–436](https://github.com/Kangel-Plugins/Plugins-Store/blob/69d079633e72ecab76f8373a6a9be777f98fbdf3/Plugins/spen_support.plugin#L312-L321).
