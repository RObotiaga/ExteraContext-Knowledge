---
type: review
source_id: plugins-store-custom-chats-title
title: "Custom Header (custom_chats_title)"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 86560477e15a3668ceb1ba456af87772cff171a4
artifact_sha256: 07e2b1aa9be3128975121be4f369c09acf2e21e0766126a4ee338e43da30d8c0
plugin_id: "custom_chats_title"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: Custom Header (custom_chats_title)

Сборщик предоставил 5 фактов. Принято 5 фактов.

Все пять фактов подтверждены исходным кодом плагина на закреплённом commit `86560477e15a3668ceb1ba456af87772cff171a4`.

| ID | Вердикт | Проверка |
|---|---|---|
| `custom-chats-title-001` | Принят | Хуки на setTitle DialogsActivity и DialogStoriesCell подтверждены строками 233–255. |
| `custom-chats-title-002` | Принят | Мультиаккаунтные ключи и считывание currentAccount подтверждены строками 260–271. |
| `custom-chats-title-003` | Принят | Использование telegram_logo_2 и ImageSpan с LOGO_PLACEHOLDER подтверждено строками 317–345. |
| `custom-chats-title-004` | Принят | Обучение через LocaleUtils.getActionBarTitle() подтверждено строками 222–232. |
| `custom-chats-title-005` | Принят | unhook_method в блоке try/except и вызов refresh() подтверждены строками 184–193. |
