---
type: review
source_id: plugins-store-plugin-guard
title: "Plugin Guard (v1.4.5)"
reviewer: independent-verifier
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5
artifact_sha256: 3bcd97ff899f1049d664d5762f699c07c213f9ba6757da98c562f9cdc705a9ca
plugin_id: "plugin_guard"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
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
