---
type: source
source_id: plugins-store-gifts-studio
title: "Gifts Studio — исходный код"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 00c5dd3d81ee66ec92ccd735bdbc0541387837a6
path: "Plugins/gifts_studio.plugin"
artifact_sha256: 7bd8890afca1208291db9110abd2aa7ef89df10c1022e5e7b251ec70f7991ea5
plugin_id: "gifts_studio"
plugin_version: "2.4.1"
author: "Daxo-Developer & @Daxo_OS"
min_version: "12.5.1"
app_version: ">=12.5.1"
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-gifts-studio.md
date: "2026-10-03"
---

# Gifts Studio — исходный код

Проверенный файл: [Plugins/gifts_studio.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/00c5dd3d81ee66ec92ccd735bdbc0541387837a6/Plugins/gifts_studio.plugin).

Все ссылки ниже закреплены за commit `00c5dd3d81ee66ec92ccd735bdbc0541387837a6`. Указанные факты основаны на статическом чтении кода, а не на runtime-тестировании.

## Проверенные сведения

- Метаданные плагина и tuple `CONTAINER_CLASSES`: [строки 25–41](https://github.com/Kangel-Plugins/Plugins-Store/blob/00c5dd3d81ee66ec92ccd735bdbc0541387837a6/Plugins/gifts_studio.plugin#L25-L41).
- Перебор классов контейнера и установка хука на `fillItems`: [строки 336–347](https://github.com/Kangel-Plugins/Plugins-Store/blob/00c5dd3d81ee66ec92ccd735bdbc0541387837a6/Plugins/gifts_studio.plugin#L336-L347).
- Регистрация пунктов меню: [строки 348–361](https://github.com/Kangel-Plugins/Plugins-Store/blob/00c5dd3d81ee66ec92ccd735bdbc0541387837a6/Plugins/gifts_studio.plugin#L348-L361).
- Lifecycle, создание интерполятора и планирование начальных циклов: [строки 265–314](https://github.com/Kangel-Plugins/Plugins-Store/blob/00c5dd3d81ee66ec92ccd735bdbc0541387837a6/Plugins/gifts_studio.plugin#L265-L314).
- Определение русской локали и fallback: [строки 301–324](https://github.com/Kangel-Plugins/Plugins-Store/blob/00c5dd3d81ee66ec92ccd735bdbc0541387837a6/Plugins/gifts_studio.plugin#L301-L324).
