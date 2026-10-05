---
type: source
source_id: plugins-store-custom-chats-title
title: "Custom Header (custom_chats_title)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 86560477e15a3668ceb1ba456af87772cff171a4
path: "Plugins/custom_chats_title.plugin"
artifact_sha256: 07e2b1aa9be3128975121be4f369c09acf2e21e0766126a4ee338e43da30d8c0
plugin_id: "custom_chats_title"
plugin_version: "3.1.1"
author: "@l_limon_l"
min_version: ">=12.5.1"
app_version: ">=12.5.1"
sdk_version: ">=1.4.4.3"
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-custom-chats-title.md
date: "2026-10-03"
---

# Custom Header (custom_chats_title)

Исходный код плагина: [Plugins/custom_chats_title.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/86560477e15a3668ceb1ba456af87772cff171a4/Plugins/custom_chats_title.plugin).

## Проверенные сведения

1. Перехват заголовков через `ActionBar.setTitle` и проверку `DialogsActivity`, а также поддержка `DialogStoriesCell` (`AnimatedTextView.setText`): [строки 233–255](https://github.com/Kangel-Plugins/Plugins-Store/blob/86560477e15a3668ceb1ba456af87772cff171a4/Plugins/custom_chats_title.plugin#L233-L255).
2. Мультиаккаунтная привязка настроек через `setting_key(account)` и определение аккаунта через `currentAccount` / `UserConfig.selectedAccount`: [строки 260–271](https://github.com/Kangel-Plugins/Plugins-Store/blob/86560477e15a3668ceb1ba456af87772cff171a4/Plugins/custom_chats_title.plugin#L260-L271).
3. Векторный логотип `telegram_logo_2` в `SpannableString` с односимвольным плейсхолдером: [строки 317–345](https://github.com/Kangel-Plugins/Plugins-Store/blob/86560477e15a3668ceb1ba456af87772cff171a4/Plugins/custom_chats_title.plugin#L317-L345).
4. Обучение стандартным заголовкам через `LocaleUtils.getActionBarTitle()`: [строки 222–232](https://github.com/Kangel-Plugins/Plugins-Store/blob/86560477e15a3668ceb1ba456af87772cff171a4/Plugins/custom_chats_title.plugin#L222-L232).
5. Снятие хуков и восстановление исходного заголовка через `self.refresh()` в UI-потоке при выгрузке: [строки 184–193](https://github.com/Kangel-Plugins/Plugins-Store/blob/86560477e15a3668ceb1ba456af87772cff171a4/Plugins/custom_chats_title.plugin#L184-L193).
