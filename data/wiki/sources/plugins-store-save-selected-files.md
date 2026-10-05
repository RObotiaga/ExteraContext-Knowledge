---
type: source
source_id: plugins-store-save-selected-files
title: Save Selected Files
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: fb496c21e6490656a815a513aaee0c57173e2118
path: Plugins/save_selected_files.plugin
version: 1.2.0
plugin_id: save_selected_files
author: "@akresik"
min_version: 12.9.0
platform: Android
review_status: accepted
review: ../reviews/plugins-store-save-selected-files.md
date: 2026-10-03
---

# Save Selected Files

Исходный код плагина `save_selected_files` (v1.2.0) из репозитория `Kangel-Plugins/Plugins-Store` на закреплённом коммите `fb496c21e6490656a815a513aaee0c57173e2118`.

Файл: [Plugins/save_selected_files.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/fb496c21e6490656a815a513aaee0c57173e2118/Plugins/save_selected_files.plugin).

## Проверенные сведения

1. Регистрация хуков через `hook_all_constructors` для `SharedMediaLayout` и `hook_all_methods` для `SearchViewPager.showActionMode` и `CacheControlActivity.createView`: [строки 42–52](https://github.com/Kangel-Plugins/Plugins-Store/blob/fb496c21e6490656a815a513aaee0c57173e2118/Plugins/save_selected_files.plugin#L42-L52).
2. Внедрение кнопки действия `ActionBarMenuItem` с темой и иконкой `R_tg.drawable.msg_download` и тегом `save_selected_files_button`: [строки 168–187](https://github.com/Kangel-Plugins/Plugins-Store/blob/fb496c21e6490656a815a513aaee0c57173e2118/Plugins/save_selected_files.plugin#L168-L187).
3. Сохранение файлов через `MediaStore.Downloads.EXTERNAL_CONTENT_URI`, `ContentValues` и `Files.copy`, с докачкой через `FileLoader.loadFile()`: [строки 263–317](https://github.com/Kangel-Plugins/Plugins-Store/blob/fb496c21e6490656a815a513aaee0c57173e2118/Plugins/save_selected_files.plugin#L263-L317).
4. Закрытие `actionMode` на UI-потоке и делегирование пакетного сохранения в фоновую очередь через `run_on_queue`: [строки 200–217](https://github.com/Kangel-Plugins/Plugins-Store/blob/fb496c21e6490656a815a513aaee0c57173e2118/Plugins/save_selected_files.plugin#L200-L217).
5. Изоляция ошибок в `AfterHook` с перехватом `Exception` и логированием traceback: [строки 31–40](https://github.com/Kangel-Plugins/Plugins-Store/blob/fb496c21e6490656a815a513aaee0c57173e2118/Plugins/save_selected_files.plugin#L31-L40).
