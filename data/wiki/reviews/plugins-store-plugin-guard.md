---
type: review
source_id: plugins-store-plugin-guard
reviewer: verifier
repository: Kangel-Plugins/Plugins-Store
commit: 6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5
plugin_id: plugin_guard
review_status: accepted
date: 2026-10-03
---

# Ревью: Plugin Guard (v1.4.5)

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверка выполнена независимо по исходному коду `Plugins/plugin_guard.plugin` на commit `6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5`.

| ID | Вердикт | Проверка |
|---|---|---|
| `plugin-guard-001` | Принят | Предустановочное сканирование и сопоставление сигнатур подтверждены строками 4643–4704. |
| `plugin-guard-002` | Принят | Хук на конструкторы InstallPluginBottomSheet подтвержден строками 7091–7102. |
| `plugin-guard-003` | Принят | Анализ AST через CombinedASTVisitor и интерпретатор ASTEval подтвержден строками 3937–3963. |
| `plugin-guard-004` | Принят | Автоблокировка кнопки установки при score < 40 и пропуск elyx подтверждены строками 4758–4777. |
| `plugin-guard-005` | Принят | create_settings и очистка в on_plugin_unload подтверждены строками 875–917. |
