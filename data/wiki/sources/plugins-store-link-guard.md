---
type: source
source_id: plugins-store-link-guard
title: "Источник: link_guard — проверка ссылок (Python `.plugin`, `Kangel-Plugins/Plugins-Store`)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: f553639c2305591ce215564bfc544982daa125dc
path: "Plugins/link_guard.plugin"
artifact_sha256: ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4
plugin_id: "link_guard"
plugin_version: "1.7.0"
author: "@Robobloxi"
min_version: ">=12.1.1"
app_version: ">=12.1.1"
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-link-guard.md
date: "2026-10-03"
---

# Источник: link_guard — проверка ссылок (Python `.plugin`, `Kangel-Plugins/Plugins-Store`)

- Плагин: `link_guard`, версия `1.7.0` («Link Guard»), `__id__ = "link_guard"`, автор `@Robobloxi`, `__app_version__ = ">=12.1.1"`
- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Проверенный файл: `Plugins/link_guard.plugin` — один Python-файл (не `.eaf`), 117 880 байт, 3237 строк (LF, завершается переводом строки)
- SHA-256 артефакта: `ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4` (совпадает с `Plugins-Store/store.json` → `link_guard.hash` и с Raw-загрузкой по проверенному commit)
- Локальная копия в рабочем checkout: `Plugins-Store/Plugins/link_guard.plugin`, git blob `2792ea197aa5adcf91e76deee3263616f77e21e4` (blob на проверенном commit идентичен: `git rev-parse f553639…:Plugins/link_guard.plugin` == `HEAD:Plugins/link_guard.plugin`)
- Проверенный commit: `f553639c2305591ce215564bfc544982daa125dc` («Update plugin: link_guard v1.7.0», ancestor of `HEAD`); он же указан в задании. На этом commit `store.json` содержит `version: 1.7.0` и `hash: ee1073af…`
- Pinned URL: https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin
- Pinned Raw (независимо скачан: HTTP 200, 117 880 байт, sha256 совпал с локальным файлом): https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin

## Проверенные утверждения

1. **Перехват `openUrl` и подавление исходного вызова.** `on_plugin_load` (`1719–1746`) выполняет шаг `self._step("openUrl", self._install_open_url_hook)` (`1737`). `_install_open_url_hook` (`2463–2489`) через `find_class("org.telegram.messenger.browser.Browser")` (`2473–2475`) вызывает `self.hook_all_methods(cls, "openUrl", handler)` (`2482`) и складывает результаты в `self._hooks` (`2484`). `on_open_url` (`2692–2752`) на ветке с диалогом вызывает `param.setResult(None)` (`2744`), после чего показывает диалог; повторное открытие выполняет `_reopen` из callback-ов диалога — `do_open` (`2881–2886`) и `accept` в `_confirm_trust` (`2907–2910`), а также из `_finish_expanded` (`2818`), если диалог недоступен. См. `Plugins/link_guard.plugin:1719–1746,2463–2489,2692–2752,2867–2917,3086–3118`.
2. **Защита от homograph/punycode.** Присутствуют и используются: `decode_idna` (`1084–1090`; вызовы — `1130`, `1151`, `1209`), `scripts_of` (`1093–1106`; смешение письменностей → HIGH `f_mixed`, `1246–1251`), словарь `LOOKALIKE_LETTERS` (`816–845`), `to_latin_lookalike` (`1109–1110`; свёртка в латиницу и проверка бренда, `1259–1262`) и `levenshtein` (`984–999`; проверка опечатки бренда, `1274–1278`). Показ IDNA-домена отличается от `host` → LOW `f_punycode` (`1246–1247`). См. `Plugins/link_guard.plugin:816–845,984–999,1084–1110,1245–1278`.
3. **Удаление трекеров.** `clean_url(url, aggressive=False)` (`1154–1181`) разбирает query через `urlsplit`, декодирует имя параметра (`unquote_plus`, `1166`) и отбрасывает его при `low in TRACKER_EXACT` или `low.startswith(TRACKER_PREFIXES)`, либо при `aggressive and low in TRACKER_AGGRESSIVE` (`1168–1172`). Наборы: `TRACKER_EXACT` (`540–583`), `TRACKER_PREFIXES` (`585–586`), `TRACKER_AGGRESSIVE` (`588–606`). Агрессивный режим включается настройкой `aggressive` (`_aggressive`, `1995–1996`); при отсутствии query функция возвращает URL без изменений (`1159–1160`). См. `Plugins/link_guard.plugin:540–606,1154–1181,1995–1996`.
4. **База `LGDB` и локальный whitelist.** Формат: `DB_MAGIC = b"LGDB"` (`1390`), `DB_FORMAT = 1` (`1391`), `DB_HASH_SECTIONS = ("MALW", "WHIT", "FR10", "FR30")` (`1394`); `DomainDatabase.__init__` (`1398–1431`) требует наличие `MALW` (`1415–1416`), валидирует заголовки хеш-секций (`1417–1419`) и хранит `total` из `MALW` (`1431`). `_contains` (`1457–1505`) считает усечённый SHA-256 ключ (`1464–1465`) и выполняет бинарный поиск (lower bound) по индексу (`1470–1477`) с последующим декодированием varint-блока (`1489–1504`); `WHIT` → `is_popular` (`1507–1508`), `MALW` (с обходом родительских доменов в `chain`, `1510–1524`) → `malicious_hit`, `FR10`/`FR30` → `freshness` (`1529–1534`). Отдельно от `WHIT` существует локальный пользовательский whitelist из настройки `whitelist`: чтение `_whitelist_list`/`_whitelist` (`1983–1993`), ранний выход в `analyze` (`1223–1226`), добавление/удаление и сохранение (`1961–1981`). См. `Plugins/link_guard.plugin:1390–1394,1398–1431,1457–1534,1961–1993`.
5. **Контекстное меню и выгрузка.** `MenuItemData`/`MenuItemType` импортируются с fallback (`26–33`), `HAS_MENU` (`35`); `on_plugin_load` при `HAS_MENU` вызывает `self._step("menu", self._register_menu)` (`1741–1744`). `_register_menu` (`1792–1807`) регистрирует два пункта через `self.add_menu_item(MenuItemData(menu_type=MenuItemType.MESSAGE_CONTEXT_MENU, …))` — «проверить» (`1793–1800`, `priority=5`) и «копировать без трекеров» (`1801–1807`, `priority=4`). `on_plugin_unload` (`1748–1760`) в цикле вызывает `self.unhook_method(h)` для сохранённых `self._hooks` (`1749–1754`) и `self.remove_menu_item(item)` для обоих пунктов (`1755–1760`); `_refresh_menu` (`1780–1790`) снимает и регистрирует пункты заново. См. `Plugins/link_guard.plugin:26–35,1741–1744,1748–1760,1792–1807`.

## Границы проверки

Утверждения подтверждены статическим чтением pinned артефакта (построчное чтение исходника, сверка blob-хеша и sha256, независимая Raw-загрузка по commit). Плагин не устанавливался и не запускался в клиенте, поэтому это не подтверждает ни загрузку плагина, ни runtime-совместимость с ExteraGram `>=12.1.1`. Все `evidence_status` — `code`, ни один факт не является `runtime-verified`.

`org.telegram.messenger.browser.Browser`, `android.net.Uri`, `android.content.Intent`, `ApplicationLoader`, `TL_update*` — внутренние классы клиента, а не документированный plugin API; поведение на другой версии APK не проверялось. `param.setResult(None)` (Xposed-стиль) означает подавление исходного вызова, а не «успешное открытие»: `_reopen` вызывается только из callback-ов диалога (`2886`, `2910`) либо из `_finish_expanded` (`2818`) при недоступном UI. Подписки `add_hook` на `TL_update*` (`2497–2502`) в `on_plugin_unload` явно не снимаются — снятие в этом файле относится к method-hook-ам из `hook_all_methods` и к пунктам меню; автоматическую очистку хостом этот исходник не доказывает. Проверка Левенштейна работает после предфильтров (разница длин ≤ 2 и popcount XOR letter-mask ≤ 1–2), то есть это эвристика, а не полный поиск по всем брендам. Бинарный поиск относится к секциям `MALW`/`WHIT`/`FR10`/`FR30`; прочие секции `LGDB` (`PLAT`, `BRND`, `SUFX`, `TLDR`) в `DB_HASH_SECTIONS` не входят.

## Проверенные факты (JSON)

```json
[
  {
    "id": "plugins-store-link-guard:link-guard-001",
    "claim": "on_plugin_load устанавливает перехват openUrl через hook_all_methods для Browser.openUrl, а при показе диалога вызывает param.setResult(None) с последующим _reopen.",
    "evidence_status": "code",
    "evidence": "Plugins/link_guard.plugin:1719-1746,2463-2489,2692-2752,2867-2917,3086-3118",
    "internal_evidence": "on_plugin_load:1737 (self._step('openUrl', self._install_open_url_hook)); _install_open_url_hook:2463-2489 (find_class('org.telegram.messenger.browser.Browser'):2473-2475, hook_all_methods:2482, self._hooks:2484); on_open_url:2692 (param.setResult(None):2744); _show_verdict.do_open -> _reopen:2881-2886; _confirm_trust.accept -> _reopen:2907-2910; _finish_expanded -> _reopen:2818; _reopen:3086-3118 (Browser.openUrl:3096-3098, method.invoke:3100-3114, Intent:3116)",
    "artifact_sha256": "ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L2463-L2489",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1719-L1746",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L2463-L2489",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L2692-L2752",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L2867-L2917",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L3086-L3118"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin"
  },
  {
    "id": "plugins-store-link-guard:link-guard-002",
    "claim": "Защита от homograph/punycode подмены: decode_idna, scripts_of, LOOKALIKE_LETTERS, to_latin_lookalike и проверка Левенштейна (levenshtein).",
    "evidence_status": "code",
    "evidence": "Plugins/link_guard.plugin:816-845,984-999,1084-1110,1245-1278",
    "internal_evidence": "LOOKALIKE_LETTERS:816-845; levenshtein:984-999; decode_idna:1084-1090 (вызовы:1130,1151,1209); scripts_of:1093-1106; to_latin_lookalike:1109-1110; f_punycode:1246-1247; f_mixed:1248-1251; f_lookalike:1259-1262; f_typo(levenshtein):1274-1278",
    "artifact_sha256": "ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1084-L1110",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L816-L845",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L984-L999",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1084-L1110",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1245-L1278"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin"
  },
  {
    "id": "plugins-store-link-guard:link-guard-003",
    "claim": "Удаление трекеров через clean_url с фильтрацией по TRACKER_EXACT, TRACKER_PREFIXES, TRACKER_AGGRESSIVE.",
    "evidence_status": "code",
    "evidence": "Plugins/link_guard.plugin:540-606,1154-1181,1995-1996",
    "internal_evidence": "TRACKER_EXACT:540-583; TRACKER_PREFIXES:585-586; TRACKER_AGGRESSIVE:588-606; clean_url:1154-1181 (unquote_plus:1166; условие drop:1168-1172; no-query return:1159-1160; urlunsplit:1181); _aggressive:1995-1996; вызовы clean_url:1217,1225,1353",
    "artifact_sha256": "ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1154-L1181",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L540-L606",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1154-L1181",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1995-L1996"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin"
  },
  {
    "id": "plugins-store-link-guard:link-guard-004",
    "claim": "База доменов LGDB (бинарный поиск, секции MALW, WHIT, FR10, FR30) и локальный белый список whitelist.",
    "evidence_status": "code",
    "evidence": "Plugins/link_guard.plugin:1390-1394,1398-1431,1457-1534,1961-1993",
    "internal_evidence": "DB_MAGIC:1390; DB_FORMAT:1391; DB_HASH_SECTIONS='MALW,WHIT,FR10,FR30':1394; DomainDatabase.__init__:1398-1431 (MALW обязателен:1415-1416, _check_hashes:1417-1419, total:1431); _contains:1457-1505 (sha256-ключ:1464-1465, бинарный поиск lower bound:1470-1477, varint-блок:1489-1504); WHIT/is_popular:1507-1508; chain+malicious_hit(MALW):1510-1524; freshness(FR10/FR30):1529-1534; локальный whitelist: analyze:1223-1226, _remove_domain:1961-1964, _on_add_domain:1966-1976, _save_whitelist:1978-1981, _whitelist_list:1983-1990, _whitelist:1992-1993",
    "artifact_sha256": "ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1398-L1534",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1390-L1394",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1398-L1431",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1457-L1534",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1961-L1993"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin"
  },
  {
    "id": "plugins-store-link-guard:link-guard-005",
    "claim": "Регистрация пунктов контекстного меню сообщения MenuItemType.MESSAGE_CONTEXT_MENU и снятие хуков/пунктов меню в on_plugin_unload.",
    "evidence_status": "code",
    "evidence": "Plugins/link_guard.plugin:26-35,1741-1744,1748-1760,1792-1807",
    "internal_evidence": "импорты MenuItemData/MenuItemType:26-33; HAS_MENU:35; on_plugin_load -> _step('menu', _register_menu):1741-1744; on_plugin_unload:1748-1760 (unhook_method(h) для self._hooks:1749-1754; remove_menu_item для _menu_check/_menu_copy:1755-1760); _register_menu:1792-1807 (MenuItemType.MESSAGE_CONTEXT_MENU:1794 и 1802; priority 5/4); _refresh_menu (снятие и повторная регистрация):1780-1790",
    "artifact_sha256": "ee1073af64f891d42c05758e0321e1f17cd373c311eb54024a1903e13e330fb4",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1792-L1807",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L26-L35",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1741-L1744",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1748-L1760",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin#L1792-L1807"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/f553639c2305591ce215564bfc544982daa125dc/Plugins/link_guard.plugin"
  }
]
```

## Результат ревью

Сборщик предоставил 5 фактов. Принято 5 фактов. Все пять подтверждены содержимым pinned артефакта (`Plugins/link_guard.plugin` @ `f553639c2305591ce215564bfc544982daa125dc`, sha256 `ee1073af…`, HTTP 200 по pinned Raw); формулировки оставлены в границах того, что непосредственно следует из кода. Уточнены границы: (001) `param.setResult(None)` выполняется на ветке с диалогом до его показа, а `_reopen` вызывается из callback-ов диалога или из `_finish_expanded`; (002) проверка Левенштейна идёт после предфильтров по длине и letter-mask; (004) `MALW/WHIT/FR10/FR30` — это `DB_HASH_SECTIONS`, а `WHIT` (популярные домены) не совпадает с пользовательским whitelist из настройки `whitelist`; (005) `on_plugin_unload` снимает method-hook-и из `self._hooks` и оба пункта меню, но подписки `add_hook` на `TL_update*` явно не снимает. Расхождения pinned commit нет: указанный в задании commit существует, является предком `HEAD`, и blob файла на нём совпадает с локальной копией.
