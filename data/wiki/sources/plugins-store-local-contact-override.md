---
type: source
source_id: plugins-store-local-contact-override
title: Local Contact Override
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 11222d1645e546123e4ea97a315e21975e5361fe
path: Plugins/local_contact_override.plugin
version: 7.0.0
plugin_id: local_contact_override
author: "@daxo_os"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-local-contact-override.md
date: 2026-10-03
---

# Local Contact Override

Исходный код плагина: [Plugins/local_contact_override.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/11222d1645e546123e4ea97a315e21975e5361fe/Plugins/local_contact_override.plugin).

## Проверенные сведения

1. Локальная мутация полей пользователя (`first_name`, `last_name`, `username`) и чата (`title`, `username`) в памяти без сетевых запросов: [строки 28–29, 128–143](https://github.com/Kangel-Plugins/Plugins-Store/blob/11222d1645e546123e4ea97a315e21975e5361fe/Plugins/local_contact_override.plugin#L128-L143).
2. Хукирование `MessagesController` (`putUser`, `putUsers`, `putChat`, `putChats`): [строки 105–127](https://github.com/Kangel-Plugins/Plugins-Store/blob/11222d1645e546123e4ea97a315e21975e5361fe/Plugins/local_contact_override.plugin#L105-L127).
3. Преобразование ID диалогов с константой `CHANNEL_OFFSET = 1000000000000`: [строки 32–40](https://github.com/Kangel-Plugins/Plugins-Store/blob/11222d1645e546123e4ea97a315e21975e5361fe/Plugins/local_contact_override.plugin#L32-L40).
4. Регистрация пункта «Локальное имя» в `PROFILE_ACTION_MENU` и `CHAT_ACTION_MENU`: [строки 263–284](https://github.com/Kangel-Plugins/Plugins-Store/blob/11222d1645e546123e4ea97a315e21975e5361fe/Plugins/local_contact_override.plugin#L263-L284).
5. Экспорт и импорт JSON через `Context.CLIPBOARD_SERVICE`: [строки 524–573](https://github.com/Kangel-Plugins/Plugins-Store/blob/11222d1645e546123e4ea97a315e21975e5361fe/Plugins/local_contact_override.plugin#L524-L573).
