---
type: review
source_id: plugins-store-extera-clean
title: "exteraClean (extera_clean)"
reviewer: independent-verifier
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 73eaf8ef9da6505dd1a5498665017a1016595576
artifact_sha256: 1c6894abbc507e49d95c22bf02ba9f69539da7d966948f6784c0c80c8197ea15
plugin_id: "extera_clean"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: exteraClean (extera_clean)

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверка выполнена независимо по исходному коду `Plugins/extera_clean.plugin` на commit `73eaf8ef9da6505dd1a5498665017a1016595576`.

| ID | Вердикт | Проверка |
|---|---|---|
| `extera-clean-001` | Принят | Удаление диалогов через deleteDialog/TL_messages_deleteHistory подтверждено строками 1413–1482. |
| `extera-clean-002` | Принят | Регистрация DRAWER_MENU (priority 175) и отмена токенов подтверждены строками 102–113. |
| `extera-clean-003` | Принят | Фоновый поток threading.Thread(daemon=True) и проверка токенов подтверждены строками 566–603. |
| `extera-clean-004` | Принят | Пауза time.sleep(0.35) и LineProgressView.setProgress подтверждены строками 1501–1506. |
| `extera-clean-005` | Принят | Вывод BulletinHelper.show_success/error на UI-потоке подтвержден строками 1508–1526. |
