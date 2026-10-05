---
type: review
source_id: plugins-store-bot-tags
title: "Bot Tags"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: efd7ae39edca5bcf33919884888a75f6ce8529b1
artifact_sha256: 4de9e922b4029540201e121e0a2e9dbdc02272b2bc1d7b37f12fa19d771977b7
plugin_id: "bot_tags"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: Bot Tags

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверка выполнена независимо по исходному файлу на коммите `efd7ae39edca5bcf33919884888a75f6ce8529b1`.

| ID | Вердикт | Проверка |
|---|---|---|
| `bot-tags-001` | Принят | Хук add_on_send_message_hook и стратегии MODIFY/CANCEL подтверждены строками 37–40. |
| `bot-tags-002` | Принят | Функция _u16len и расчет UTF-16 сдвига подтверждены строками 33–35. |
| `bot-tags-003` | Принят | Коррекция _shift_entities и усечение _clamp_entities подтверждены строками 62–85. |
| `bot-tags-004` | Принят | Обработка команд .tag/.тег и reload_settings=True подтверждены строками 48–57. |
| `bot-tags-005` | Принят | Вызов BulletinHelper.show_info через run_on_ui_thread подтвержден строками 59–60. |
