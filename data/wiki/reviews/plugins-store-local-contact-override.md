---
type: review
source_id: plugins-store-local-contact-override
title: "Local Contact Override"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 11222d1c197556c267062bb64d879313a78effce
artifact_sha256: 5cd8fb147d01ec10e570191b3610fd74ed7557629fd3811993a5306d72fa62bc
plugin_id: "local_contact_override"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Review: Local Contact Override

Сборщик предоставил 5 фактов. Принято 5 фактов.

Independent static-source review of plugin v7.0.0 at commit `11222d1c197556c267062bb64d879313a78effce`. All five claims were directly supported by the cited implementation lines.

| ID | Вердикт | Проверка |
|---|---|---|
| `local-contact-override-001` | Принят | Локальное переопределение без сетевых вызовов подтверждено строками 28–29, 128–143. |
| `local-contact-override-002` | Принят | Хуки на MessagesController подтверждены строками 105–127. |
| `local-contact-override-003` | Принят | Формула _dialog_to_chat_id с CHANNEL_OFFSET подтверждена строками 32–40. |
| `local-contact-override-004` | Принят | Пункты меню профиля и чата подтверждены строками 263–284. |
| `local-contact-override-005` | Принят | Экспорт и импорт через CLIPBOARD_SERVICE подтверждены строками 524–573. |
