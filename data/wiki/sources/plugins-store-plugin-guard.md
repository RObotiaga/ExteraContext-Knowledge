---
type: source
source_id: plugins-store-plugin-guard
title: Plugin Guard (v1.4.5)
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5
path: Plugins/plugin_guard.plugin
version: 1.4.5
plugin_id: plugin_guard
author: "@chestertech & @useful_plugins"
min_version: 12.6.4
platform: Android
review_status: accepted
review: ../reviews/plugins-store-plugin-guard.md
date: 2026-10-03
---

# Plugin Guard (v1.4.5)

Исходный код плагина: [Plugins/plugin_guard.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin).

## Проверенные сведения

1. Предустановочная проверка `_perform_file_scan` по базе сигнатур и AST-сканирование `scan_plugin_code`: [строки 4643–4704](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L4643-L4704).
2. Хукирование конструкторов `InstallPluginBottomSheet` и внедрение кнопки «Проверка PluginGuard»: [строки 7091–7102](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L7091-L7102).
3. Анализ AST через `CombinedASTVisitor` и изолированный интерпретатор `ASTEval`: [строки 3937–3963](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L3937-L3963).
4. Автоблокировка кнопки установки при `score < 40` или `CRITICAL` (пропуск для elyx/.eaf): [строки 4758–4777](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L4758-L4777).
5. Декларативные настройки в `create_settings` и снятие хуков в `on_plugin_unload`: [строки 875–917](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L875-L917).
