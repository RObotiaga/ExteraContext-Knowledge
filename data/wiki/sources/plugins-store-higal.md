---
type: source
source_id: plugins-store-higal
title: "Hide Gallery (higal)"
source_type: plugin
source: "Plugins-Store"
repository: "https://github.com/Kangel-Plugins/Plugins-Store"
commit: "e5b2b5d4f20e4b10ec449c25da3806bbcebbf418"
version: "1.0"
plugin_id: "higal"
name: "Hide Gallery"
author: "@ka1Plugins"
min_version: "12.5.1"
platform: Android
review_status: accepted
review: ../reviews/plugins-store-higal.md
date: 2026-10-03
---

# Hide Gallery (higal)

Источник фактов — `Plugins/higal.plugin` в репозитории Plugins-Store на коммите `e5b2b5d4f20e4b10ec449c25da3806bbcebbf418`. Метаданные в файле указывают ID `higal`, название `Hide Gallery`, версию `1.0`, автора `@ka1Plugins` и минимальную версию приложения `12.5.1` ([строки 36–42](https://github.com/Kangel-Plugins/Plugins-Store/blob/e5b2b5d4f20e4b10ec449c25da3806bbcebbf418/Plugins/higal.plugin#L36-L42)).

## Подтверждённые факты

- **higal-001 — размытие и fallback.** Плагин пытается создать `RenderEffect` при `Build.VERSION.SDK_INT >= 31`. Если эффект не создан или недоступен, `_visual` использует `ColorMatrixColorFilter`; матрица задаёт масштаб каналов RGB `0.15`, alpha — `1.0` ([строки 103–140](https://github.com/Kangel-Plugins/Plugins-Store/blob/e5b2b5d4f20e4b10ec449c25da3806bbcebbf418/Plugins/higal.plugin#L103-L140)).
- **higal-002 — хуки ячеек и layout.** Для `PhotoAttachPhotoCell` плагин перебирает объявленные методы и устанавливает хуки на `setHasSpoiler`, `setPhotoEntry` и `setChecked`. Для `ChatAttachAlertPhotoLayout` он устанавливает хук на `onInit` и пытается установить хук на `onHidden` ([строки 224–251](https://github.com/Kangel-Plugins/Plugins-Store/blob/e5b2b5d4f20e4b10ec449c25da3806bbcebbf418/Plugins/higal.plugin#L224-L251)).
- **higal-003 — обработка кликов по сетке.** Плагин создаёт `dynamic_proxy` для `RecyclerListView.OnItemClickListenerExtended` и передаёт его в `setOnItemClickListener`. При клике по ячейке `PhotoAttachPhotoCell` он добавляет `imageId` записи в `revealed` и снимает визуальный эффект ([строки 261–300](https://github.com/Kangel-Plugins/Plugins-Store/blob/e5b2b5d4f20e4b10ec449c25da3806bbcebbf418/Plugins/higal.plugin#L261-L300)).
- **higal-004 — очистка при выгрузке.** `on_plugin_unload` выключает плагин, пытается снять `RenderEffect` и `ColorFilter` с дочерних ячеек `PhotoAttachPhotoCell` текущей сетки и сбрасывает сохранённые данные и ссылки ([строки 77–102](https://github.com/Kangel-Plugins/Plugins-Store/blob/e5b2b5d4f20e4b10ec449c25da3806bbcebbf418/Plugins/higal.plugin#L77-L102)).
- **higal-005 — сброс после закрытия PhotoViewer.** На `PhotoViewer.closePhoto` устанавливается `before`-хук. Если плагин активен, хук планирует `_reset` через `run_on_ui_thread` с задержкой 350 мс ([строки 219–222](https://github.com/Kangel-Plugins/Plugins-Store/blob/e5b2b5d4f20e4b10ec449c25da3806bbcebbf418/Plugins/higal.plugin#L219-L222)).
