---
type: review
source_id: plugins-store-limedex
reviewer: verifier
repository: Kangel-Plugins/Plugins-Store
commit: 8cb930bf899079c56b07143b1f7209f7b25197ff
plugin_id: limedex
review_status: accepted
date: 2026-10-03
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
