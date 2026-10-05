---
type: review
source_id: plugins-store-limedex
title: "limedex (v2.5.7)"
reviewer: independent-verifier
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 8cb930bf899079c56b07143b1f7209f7b25197ff
artifact_sha256: 24982dc3d0a956fad15408c330243ff209884d55bb3c4edc40c9dd7fb89032f9
plugin_id: "limedex"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: limedex (v2.5.7)

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверка выполнена независимо по коду архива `Plugins/limedex.eaf` на commit `8cb930bf899079c56b07143b1f7209f7b25197ff`.

| ID | Вердикт | Проверка |
|---|---|---|
| `limedex-001` | Принят | `refmap.yml:1–4` в корне архива маршрутизирует все заявленные компоненты пакета Elyx. |
| `limedex-002` | Принят | `limedex/meta.yml` полностью совпадает по всем полям метаданных. |
| `limedex-003` | Принят | `limedex_open` (`CHAT_ACTION_MENU`) и `limedex_drawer` (`DRAWER_MENU`, 80) подтверждены `main.py`. |
| `limedex-004` | Принят | Кэширование в `getCacheDir()/limedex`, `OrderedDict` и `.part` файлы подтверждены кодом `api.py`. |
| `limedex-005` | Принят | Закрытие `view.dismiss()` и удаление `remove_menu_item` в `on_plugin_unload` подтверждены `main.py`. |
