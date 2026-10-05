---
type: source
source_id: plugins-store-plugin-guard
title: "Plugin Guard (v1.4.5)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5
path: "Plugins/plugin_guard.plugin"
artifact_sha256: 3bcd97ff899f1049d664d5762f699c07c213f9ba6757da98c562f9cdc705a9ca
plugin_id: "plugin_guard"
plugin_version: "1.4.5"
author: "@dekma0091 && @DefinitelyNotDekma"
min_version: "12.5.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-plugin-guard.md
date: "2026-10-03"
---

# Plugin Guard (v1.4.5)

Исходный код плагина: [Plugins/plugin_guard.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin).

## Проверенные сведения

1. Предустановочная проверка `_perform_file_scan` по базе сигнатур и AST-сканирование `scan_plugin_code`: [строки 4643–4704](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L4643-L4704).
2. Хукирование конструкторов `InstallPluginBottomSheet` и внедрение кнопки «Проверка PluginGuard»: [строки 7091–7102](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L7091-L7102).
3. Анализ AST через `CombinedASTVisitor` и изолированный интерпретатор `ASTEval`: [строки 3937–3963](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L3937-L3963).
4. Автоблокировка кнопки установки при `score < 40` или `CRITICAL` (пропуск для elyx/.eaf): [строки 4758–4777](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L4758-L4777).
5. Декларативные настройки в `create_settings` и снятие хуков в `on_plugin_unload`: [строки 875–917](https://github.com/Kangel-Plugins/Plugins-Store/blob/6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5/Plugins/plugin_guard.plugin#L875-L917).
