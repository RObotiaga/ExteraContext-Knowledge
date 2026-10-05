---
type: review
source_id: plugins-store-local-contact-override
reviewer: verifier
repository: Kangel-Plugins/Plugins-Store
commit: 11222d1645e546123e4ea97a315e21975e5361fe
plugin_id: local_contact_override
review_status: accepted
date: 2026-10-03
---

# Review: Local Contact Override

Сборщик предоставил 5 фактов. Принято 5 фактов.

Independent static-source review of plugin v7.0.0 at commit `11222d1645e546123e4ea97a315e21975e5361fe`. All five claims were directly supported by the cited implementation lines.

| ID | Вердикт | Проверка |
|---|---|---|
| `local-contact-override-001` | Принят | Локальное переопределение без сетевых вызовов подтверждено строками 28–29, 128–143. |
| `local-contact-override-002` | Принят | Хуки на MessagesController подтверждены строками 105–127. |
| `local-contact-override-003` | Принят | Формула _dialog_to_chat_id с CHANNEL_OFFSET подтверждена строками 32–40. |
| `local-contact-override-004` | Принят | Пункты меню профиля и чата подтверждены строками 263–284. |
| `local-contact-override-005` | Принят | Экспорт и импорт через CLIPBOARD_SERVICE подтверждены строками 524–573. |
