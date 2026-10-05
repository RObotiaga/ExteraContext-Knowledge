# Ревью: plugins-store-link-guard

- Плагин: `link_guard` (Link Guard), версия `1.7.0`, Python `.plugin`
- Commit (как в задании): `f553639c2305591ce215564bfc544982daa125dc` — существует, «Update plugin: link_guard v1.7.0», ancestor of `HEAD` (расхождения нет)
- Проверенный файл: `Plugins/link_guard.plugin`, 117 880 байт, 3237 строк; локальный blob `2792ea197aa5adcf91e76deee3263616f77e21e4` совпадает с blob на pinned commit
- SHA-256 артефакта: `ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4` (совпадает с `Plugins-Store/store.json`, в том числе на pinned commit; и с Raw-загрузкой по pinned commit: HTTP 200, 117 880 байт)
- Источник: [plugins-store-link-guard.md](../sources/plugins-store-link-guard.md)
- Проверка: независимое сопоставление 5 кандидатов с содержимым pinned файла (построчное чтение + сверка blob/sha256 + Raw-загрузка по commit); статус доказательности — `code` (статический анализ, не runtime-проверка).

## Вердикт

Сборщик предоставил 5 фактов. Принято 5 фактов.

| ID | Вердикт | Основание |
|---|---|---|
| `plugins-store-link-guard:link-guard-001` | Принято | `on_plugin_load:1737` вызывает `_install_open_url_hook` (`2463–2489`), который находит `org.telegram.messenger.browser.Browser` (`2473–2475`) и вызывает `hook_all_methods(cls, "openUrl", handler)` (`2482`), сохраняя хуки в `self._hooks` (`2484`). На ветке с диалогом `on_open_url` вызывает `param.setResult(None)` (`2744`); `_reopen` (`3086–3118`) вызывается из `do_open` (`2886`), `accept` (`2910`) и `_finish_expanded` (`2818`). |
| `plugins-store-link-guard:link-guard-002` | Принято | `decode_idna` (`1084–1090`), `scripts_of` (`1093–1106`), `LOOKALIKE_LETTERS` (`816–845`), `to_latin_lookalike` (`1109–1110`) и `levenshtein` (`984–999`) присутствуют; используются в `analyze` на `1130,1151,1209,1246–1251,1259–1262,1274–1278`. |
| `plugins-store-link-guard:link-guard-003` | Принято | `clean_url` (`1154–1181`) отбрасывает параметр при `low in TRACKER_EXACT` или `low.startswith(TRACKER_PREFIXES)`, либо при `aggressive and low in TRACKER_AGGRESSIVE` (`1168–1172`); наборы — `540–583`, `585–586`, `588–606`; агрессивный режим — настройка `aggressive` (`1995–1996`). |
| `plugins-store-link-guard:link-guard-004` | Принято | `DB_MAGIC = b"LGDB"` (`1390`), `DB_HASH_SECTIONS = ("MALW","WHIT","FR10","FR30")` (`1394`); `_contains` (`1457–1505`) делает бинарный поиск по индексу (`1470–1477`); `WHIT`→`is_popular` (`1507–1508`), `MALW`→`malicious_hit` (`1520–1524`), `FR10/FR30`→`freshness` (`1529–1534`); локальный whitelist из настройки `whitelist` (`1223–1226`, `1961–1993`). |
| `plugins-store-link-guard:link-guard-005` | Принято | `_register_menu` (`1792–1807`) добавляет два пункта `MenuItemType.MESSAGE_CONTEXT_MENU` через `add_menu_item` (`1794`, `1802`), регистрация идёт из `on_plugin_load` (`1741–1744`); `on_plugin_unload` (`1748–1760`) снимает `self._hooks` через `unhook_method` (`1751`) и пункты меню через `remove_menu_item` (`1758`). |

## Замечания о точности

1. **Факт 001 (последовательность).** `param.setResult(None)` (`2744`) выполняется на ветке с диалогом до его показа и подавляет исходный вызов; `_reopen` вызывается не сразу за ним, а из callback-ов диалога (`do_open` `2886`, `accept` `2910`) либо из `_finish_expanded` (`2818`), когда UI недоступен. Само открытие делает `_reopen` через `Browser.openUrl` (`3096–3098`), reflection `method.invoke` (`3100–3114`) или `Intent` (`3116`). Рекурсию hook-а гасит bypass-окно `APPROVAL_WINDOW = 10.0` (`1717`, `2682–2690`, установка в `3086–3092`). `hook_all_methods` применяется к внутреннему классу клиента, а не к plugin API.
2. **Факт 002 (эвристика, не полный перебор).** Проверка `levenshtein` (`1274`) достигается только после предфильтров: разница длин ≤ 2 (`1267`) и popcount XOR letter-mask ≤ 1–2 (`1269–1273`), и результат принимается при `1 <= dist <= limit` (`1275`). `LOOKALIKE_LETTERS` (`816–845`) покрывает кириллические/греческие/латинско-подобные символы, но не все IDN-гомоглифы; `scripts_of` различает только LATIN/CYRILLIC/GREEK/ARMENIAN/HEBREW (`1102`). Декодирование — через `ascii`+`idna`-кодек (`1088`), без нормализации Unicode.
3. **Факт 003 (только query).** `clean_url` не трогает path/fragment и возвращает URL без изменений, если query пуст (`1159–1160`); сравнение имён параметров идёт по декодированному (`unquote_plus`) значению в нижнем регистре (`1166–1167`), а `TRACKER_PREFIXES` проверяются через `startswith`. Список `TRACKER_AGGRESSIVE` применяется только при включённой настройке `aggressive`.
4. **Факт 004 (`WHIT` ≠ локальный whitelist).** Секции `MALW/WHIT/FR10/FR30` — это `DB_HASH_SECTIONS` с проверкой заголовков (`1394`, `1417–1419`); `WHIT` — раздел популярных доменов в бинарной базе. Пользовательский whitelist — отдельная настройка `whitelist` (`1983–1993`) с ранним выходом из `analyze` (`1223–1226`). «Бинарный поиск» относится к индексу секции (lower bound по 64-битному усечению SHA-256, `1470–1477`) с последующим varint-декодированием блока (`1489–1504`); прочие секции (`PLAT`, `BRND`, `SUFX`, `TLDR`) в `DB_HASH_SECTIONS` не входят.
5. **Факт 005 (объём unload).** `on_plugin_unload` снимает только method-hook-и, возвращённые `hook_all_methods` (список `self._hooks`), и два пункта меню. Подписки `add_hook` на шесть имён `TL_update*` (`2491–2502`) в этом файле не имеют парного `remove_hook`; автоматическая очистка хостом при unload этим исходником не подтверждается и здесь не утверждается.

## Границы проверки

Плагин не устанавливался и не запускался в клиенте: это статическая проверка одного pinned файла, а не runtime-совместимость. Все пять фактов имеют `evidence_status: code`. Поведение host-классов (`org.telegram.messenger.browser.Browser`, `android.net.Uri`, `android.content.Intent`, `ApplicationLoader`, `TL_update*`) и точные сигнатуры перегрузок зависят от версии APK и в этом источнике не проверялись; `MenuItemData`/`MenuItemType` импортируются с fallback (`26–35`).

## Pinned источник

Проверенный (pinned commit существует, Raw HTTP 200, 117 880 байт, sha256 `ee1073af…` совпадает с локальным файлом и `store.json`):
https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin

Raw-подтверждение:
https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin
