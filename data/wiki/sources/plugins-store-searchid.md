---
type: source
source_id: plugins-store-searchid
title: SearchID.plugin
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: 997557613ba8132f8373e34a6cf8038eb9f87c12
path: Plugins/SearchID.plugin
version: 1.0.1
plugin_id: SearchID
author: "@jaxbastard"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-searchid.md
date: 2026-10-03
---

# SearchID.plugin

Исходник плагина `SearchID` из репозитория `Kangel-Plugins/Plugins-Store`, зафиксированный на commit `997557613ba8132f8373e34a6cf8038eb9f87c12`.

## Проверенные сведения

- Плагин получает методы `fillItems` через `_chaquopy_reflector.getMethods()`, выбирает первый найденный метод для установки хука и при неудаче пробует установить хуки на все методы `fillItems`. [Исходный код, строки 95–124](https://github.com/Kangel-Plugins/Plugins-Store/blob/997557613ba8132f8373e34a6cf8038eb9f87c12/Plugins/SearchID.plugin#L95-L124)
- Перед поиском плагин читает поле `query` через `get_private_field`, нормализует его и сохраняет состояние поиска. [Исходный код, строки 36–48](https://github.com/Kangel-Plugins/Plugins-Store/blob/997557613ba8132f8373e34a6cf8038eb9f87c12/Plugins/SearchID.plugin#L36-L48)
- Хук `getName()` добавляет ID плагина к имени в результате, если активный поисковый запрос содержится в ID без учёта регистра. [Исходный код, строки 55–73](https://github.com/Kangel-Plugins/Plugins-Store/blob/997557613ba8132f8373e34a6cf8038eb9f87c12/Plugins/SearchID.plugin#L55-L73)
- При обработке ошибки плагин формирует traceback и передаёт его в callback копирования, переданный в `BulletinHelper.show_with_button()`. [Исходный код, строки 19–29](https://github.com/Kangel-Plugins/Plugins-Store/blob/997557613ba8132f8373e34a6cf8038eb9f87c12/Plugins/SearchID.plugin#L19-L29)
- При выгрузке плагин пытается снять сохранённые хуки и сбрасывает внутреннее состояние. [Исходный код, строки 140–149](https://github.com/Kangel-Plugins/Plugins-Store/blob/997557613ba8132f8373e34a6cf8038eb9f87c12/Plugins/SearchID.plugin#L140-L149)
