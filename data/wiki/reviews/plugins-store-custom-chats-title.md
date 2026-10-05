---
type: review
source_id: plugins-store-custom-chats-title
reviewer: verifier
repository: Kangel-Plugins/Plugins-Store
commit: 8656047cf3398f6ddff97561be6b5a37171d93a5
plugin_id: custom_chats_title
review_status: accepted
date: 2026-10-03
---

# Ревью: Custom Header (custom_chats_title)

Сборщик предоставил 5 фактов. Принято 5 фактов.

Все пять фактов подтверждены исходным кодом плагина на закреплённом commit `8656047cf3398f6ddff97561be6b5a37171d93a5`.

| ID | Вердикт | Проверка |
|---|---|---|
| `custom-chats-title-001` | Принят | Хуки на setTitle DialogsActivity и DialogStoriesCell подтверждены строками 233–255. |
| `custom-chats-title-002` | Принят | Мультиаккаунтные ключи и считывание currentAccount подтверждены строками 260–271. |
| `custom-chats-title-003` | Принят | Использование telegram_logo_2 и ImageSpan с LOGO_PLACEHOLDER подтверждено строками 317–345. |
| `custom-chats-title-004` | Принят | Обучение через LocaleUtils.getActionBarTitle() подтверждено строками 222–232. |
| `custom-chats-title-005` | Принят | unhook_method в блоке try/except и вызов refresh() подтверждены строками 184–193. |
