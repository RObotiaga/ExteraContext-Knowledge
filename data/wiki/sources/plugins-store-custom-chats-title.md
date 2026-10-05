---
type: source
source_id: plugins-store-custom-chats-title
title: Custom Header
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 8656047cf3398f6ddff97561be6b5a37171d93a5
path: Plugins/custom_chats_title.plugin
version: 3.1.1
plugin_id: custom_chats_title
author: "@l_limon_l"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-custom-chats-title.md
date: 2026-10-03
---

# Custom Header (custom_chats_title)

Исходный код плагина: [Plugins/custom_chats_title.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/8656047cf3398f6ddff97561be6b5a37171d93a5/Plugins/custom_chats_title.plugin).

## Проверенные сведения

1. Перехват заголовков через `ActionBar.setTitle` и проверку `DialogsActivity`, а также поддержка `DialogStoriesCell` (`AnimatedTextView.setText`): [строки 233–255](https://github.com/Kangel-Plugins/Plugins-Store/blob/8656047cf3398f6ddff97561be6b5a37171d93a5/Plugins/custom_chats_title.plugin#L233-L255).
2. Мультиаккаунтная привязка настроек через `setting_key(account)` и определение аккаунта через `currentAccount` / `UserConfig.selectedAccount`: [строки 260–271](https://github.com/Kangel-Plugins/Plugins-Store/blob/8656047cf3398f6ddff97561be6b5a37171d93a5/Plugins/custom_chats_title.plugin#L260-L271).
3. Векторный логотип `telegram_logo_2` в `SpannableString` с односимвольным плейсхолдером: [строки 317–345](https://github.com/Kangel-Plugins/Plugins-Store/blob/8656047cf3398f6ddff97561be6b5a37171d93a5/Plugins/custom_chats_title.plugin#L317-L345).
4. Обучение стандартным заголовкам через `LocaleUtils.getActionBarTitle()`: [строки 222–232](https://github.com/Kangel-Plugins/Plugins-Store/blob/8656047cf3398f6ddff97561be6b5a37171d93a5/Plugins/custom_chats_title.plugin#L222-L232).
5. Снятие хуков и восстановление исходного заголовка через `self.refresh()` в UI-потоке при выгрузке: [строки 184–193](https://github.com/Kangel-Plugins/Plugins-Store/blob/8656047cf3398f6ddff97561be6b5a37171d93a5/Plugins/custom_chats_title.plugin#L184-L193).
