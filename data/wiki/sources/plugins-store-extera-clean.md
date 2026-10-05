---
type: source
source_id: plugins-store-extera-clean
title: "exteraClean (extera_clean)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 73eaf8ef9da6505dd1a5498665017a1016595576
path: "Plugins/extera_clean.plugin"
artifact_sha256: 1c6894abbc507e49d95c22bf02ba9f69539da7d966948f6784c0c80c8197ea15
plugin_id: "extera_clean"
plugin_version: "1.0.2"
author: "@plugin_ai"
min_version: "12.1.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-extera-clean.md
date: "2026-10-03"
---

# exteraClean (extera_clean)

Исходный код плагина: [Plugins/extera_clean.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/73eaf8ef9da6505dd1a5498665017a1016595576/Plugins/extera_clean.plugin).

## Проверенные сведения

1. Массовая очистка неактивных диалогов на уровне сущностей Telegram: `MessagesController.deleteDialog`, `TL_messages_deleteHistory`, `TL_channels_leaveChannel`, `TL_messages_deleteChatUser`: [строки 1413–1482](https://github.com/Kangel-Plugins/Plugins-Store/blob/73eaf8ef9da6505dd1a5498665017a1016595576/Plugins/extera_clean.plugin#L1413-L1482).
2. Жизненный цикл: добавление пункта в боковое меню `DRAWER_MENU` с `priority=175` и очистка в `on_plugin_unload` с инкрементом токенов отмены: [строки 102–113](https://github.com/Kangel-Plugins/Plugins-Store/blob/73eaf8ef9da6505dd1a5498665017a1016595576/Plugins/extera_clean.plugin#L102-L113).
3. Фоновые потоки `threading.Thread(target=..., daemon=True)` с токенами отмены `_load_token` и `_batch_token`: [строки 566–603](https://github.com/Kangel-Plugins/Plugins-Store/blob/73eaf8ef9da6505dd1a5498665017a1016595576/Plugins/extera_clean.plugin#L566-L603).
4. Задержка `time.sleep(0.35)` между запросами для защиты от FloodWait и обновление `LineProgressView.setProgress`: [строки 1501–1506](https://github.com/Kangel-Plugins/Plugins-Store/blob/73eaf8ef9da6505dd1a5498665017a1016595576/Plugins/extera_clean.plugin#L1501-L1506).
5. Итоговые уведомления через `BulletinHelper.show_success` и `show_error` на UI-потоке: [строки 1508–1526](https://github.com/Kangel-Plugins/Plugins-Store/blob/73eaf8ef9da6505dd1a5498665017a1016595576/Plugins/extera_clean.plugin#L1508-L1526).
