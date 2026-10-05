---
type: source
source_id: plugins-store-customitemmenu
title: "Источник: Кастомные пункты меню (customitemmenu)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: f8f35b18b6148b20027b3bdeff505d240086444a
path: "Plugins/CustomItеmMеnu.plugin"
artifact_sha256: 5cc1ac05bf214d6431b910a44f9dbafd4896a96f78249670ca1548113b7c7a71
plugin_id: "customitemmenu"
plugin_version: "1.5"
author: "@n1ksly, @podyshka1"
min_version: "12.2.3"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-customitemmenu.md
date: "2026-10-03"
---

# Источник: Кастомные пункты меню (customitemmenu)

- Плагин: `customitemmenu`, версия `1.5`
- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Проверенный файл: `Plugins/CustomItеmMеnu.plugin` (в имени файла — кириллические «е» U+0435 в «Itе» и «Mеnu»; тот же символ использован в URL в percent-encoding `%D0%B5`)
- Проверенный commit: `f8f35b18b6148b20027b3bdeff505d240086444a`
- Pinned URL: https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/CustomIt%D0%B5mM%D0%B5nu.plugin
- Локальная копия: `Plugins-Store/Plugins/CustomItеmMеnu.plugin`, 433 строки, git blob `a2fa1df159d5c40f63397837c8216a0ea3117377` (совпадает с `git ls-tree` для commit), SHA-256 `5cc1ac05bf214d6431b910a44f9dbafd4896a96f78249670ca1548113b7c7a71` (совпадает с `hash` в `store.json`). `git diff HEAD` по файлу пуст, содержимое по pinned raw-URL совпадает с локальной копией.
- Метаданные в файле: `__id__ = "customitemmenu"` (строка 25), `__version__ = "1.5"` (26), `__min_version__ = "12.2.3"` (28), `__icon__ = "DMJDuckX2/49"` (24).

## Проверенные утверждения

1. `on_plugin_load` (строка 47) вызывает `self._add_drawer_links()` (строка 85). `_add_drawer_links()` (249) сначала перебирает `self._custom_menu_items` и вызывает `self.remove_menu_item(menu_id)` для каждого ранее зарегистрированного id в `try/except` (250–254), затем очищает список (255). Далее для каждого элемента настройки с непустыми `title` и `url` создаётся `MenuItemData` с `menu_type` из списка четырёх типов — `DRAWER_MENU`, `MESSAGE_CONTEXT_MENU`, `CHAT_ACTION_MENU`, `PROFILE_ACTION_MENU` — по индексу `menu_type` (288–292), `priority=5 + i` (296), и регистрируется через `self.add_menu_item(menu_item)` (299); возвращённый `menu_id` сохраняется в `self._custom_menu_items` (300).
2. `IconsAlert` (355) строится на `BottomSheet.Builder(self.activity)` (396) с отключёнными top/bottom padding (397–398): кастомный `FrameLayout` (400) с фоном `Theme.key_windowBackgroundGray` (402), в который добавлен `UniversalRecyclerView(get_last_fragment(), Callback2(self.fillItems), Callback5(self.onClick), None)` (405) через `LayoutHelper.createFrame(-1, 700)` (406); строки иконок создаются `UItem.asButton(0, icon_res_id, icon)` (376), показ — `builder.show()` + `setCanDismissWithSwipe(False)` (408–409). Java-интерфейсы обёрнуты через `dynamic_proxy`: `class Callback2(dynamic_proxy(Utilities.Callback2))` (335–342) и `class Callback5(dynamic_proxy(Utilities.Callback5))` (344–351); импорт `dynamic_proxy` — строка 9.
3. Инвентарь иконок строится в `on_plugin_load` словарным включением (79–83): для каждого имени `i` из `dir(R.drawable)` берётся `getattr(R.drawable, i)` (80) при условии, что все символы `i` входят в `X = 'abcdefghijklmnopqrstuvwxyz' + '0123456789' + '_'` (31), имя не начинается с `_` (`not i.startswith('_')`) и `i` отсутствует в локальном `blacklist` (49–77). **Исправление к кандидату:** исключаются имена, начинающиеся с подчёркивания, а не символ `_` внутри имени (например, `ic_ab_new`, `sms_bubble` проходят символьный фильтр); `blacklist` содержит **143** уникальные строки (49–77), а не 129 — число 129 из файла не воспроизводится.
4. Негативное свидетельство: `parse_markdown` импортирован из `markdown_utils` (строка 10) и больше в файле не встречается — единственное вхождение токена `parse_markdown` это строка импорта. Тексты диалогов передаются как строки: `_show_version_dialog`/`_show_help_dialog` (321–328) → `self._show_info(...)` (330–331) → `AlertManager.show_info_alert(...)` (416–428), где `message` уходит в `builder.set_message(message)` (424) без какого-либо вызова парсера markdown. Это свидетельство уровня файла: сам плагин не применяет markdown-парсер; поведение `AlertDialogBuilder.set_message` на целевом клиенте по этому файлу не проверяется.
5. В файле (433 строки) нет `on_plugin_unload` — ни определения, ни упоминания; жизненный цикл ограничен `on_plugin_load` (47). Состояние хранится в настройке `custom_items` как JSON: `self.get_setting("custom_items", "[]")` (196) и `json.dumps` в `set_setting` (215, 220). `set_items()` (218) вызывает `self.set_setting("custom_items", json.dumps(items), reload_settings=True)` (220), затем `self._add_drawer_links()` (223) и `get_last_fragment()` (224) с вызовом `fragment.rebuildAllItems()` (226) — под проверками `if fragment and hasattr(fragment, "rebuildAllItems")` (225).

## Границы проверки

Утверждения подтверждены статическим чтением указанной версии исходника (AST-разбор + сверка с pinned commit); это не подтверждает исполнение на клиенте/устройстве. Отсутствие `on_plugin_unload` установлено для этого файла; поведение базового класса `BasePlugin` за пределами файла не проверялось. `parse_markdown` из `markdown_utils` объявлен, но в snapshot `exteragram-utils 0.1.3` его тело — `...` (нереализованный парсер), поэтому отказ от вызова не меняет наблюдаемое поведение, но оставляет мёртвый импорт. Негативные утверждения (отсутствие вызова, отсутствие unload) ограничены данным файлом и данной ревизией.

## Проверенные факты (JSON)

```json
[
  {
    "id": "plugins-store-customitemmenu:customitemmenu-001",
    "claim": "on_plugin_load (строка 47) вызывает self._add_drawer_links() (строка 85); _add_drawer_links() сначала удаляет ранее зарегистрированные пункты через self.remove_menu_item(menu_id) для каждого id из self._custom_menu_items и очищает список (250-255), затем для каждого элемента настройки с непустыми title и url создаёт MenuItemData с menu_type из четырёх типов MenuItemType — DRAWER_MENU, MESSAGE_CONTEXT_MENU, CHAT_ACTION_MENU, PROFILE_ACTION_MENU по индексу menu_type (288-292), priority=5 + i (296) — и регистрирует его через self.add_menu_item(menu_item) (299), сохраняя возвращённый menu_id в self._custom_menu_items (300).",
    "evidence_status": "code",
    "evidence": "Plugins/CustomItеmMеnu.plugin:47,85,249-255,288-300",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/CustomIt%D0%B5mM%D0%B5nu.plugin#L249-L300"
  },
  {
    "id": "plugins-store-customitemmenu:customitemmenu-002",
    "claim": "IconsAlert (355) построен на BottomSheet.Builder(self.activity) (396) с кастомным FrameLayout (400) и UniversalRecyclerView(get_last_fragment(), Callback2(self.fillItems), Callback5(self.onClick), None) (405), добавленным через LayoutHelper.createFrame(-1, 700) (406); строки создаются UItem.asButton(0, icon_res_id, icon) (376), а интерфейсы обёрнуты через dynamic_proxy(Utilities.Callback2) (335) и dynamic_proxy(Utilities.Callback5) (344).",
    "evidence_status": "code",
    "evidence": "Plugins/CustomItеmMеnu.plugin:9,335-351,355,363-377,395-409",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/CustomIt%D0%B5mM%D0%B5nu.plugin#L335-L406"
  },
  {
    "id": "plugins-store-customitemmenu:customitemmenu-003",
    "claim": "Инвентарь иконок — словарное включение в on_plugin_load (79-83): для каждого имени i из dir(R.drawable) берётся getattr(R.drawable, i) (80) при условии, что все символы i входят в X = 'abcdefghijklmnopqrstuvwxyz' + '0123456789' + '_' (31), имя не начинается с '_' (not i.startswith('_')) и i отсутствует в blacklist (49-77); blacklist содержит 143 уникальные строки (не 129), а фильтр исключает только ведущее подчёркивание, а не символ '_' внутри имени.",
    "evidence_status": "code",
    "evidence": "Plugins/CustomItеmMеnu.plugin:31,49-77,79-83",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/CustomIt%D0%B5mM%D0%B5nu.plugin#L49-L83"
  },
  {
    "id": "plugins-store-customitemmenu:customitemmenu-004",
    "claim": "Негативное свидетельство: parse_markdown импортирован из markdown_utils (строка 10) и нигде в файле не вызывается — это единственное вхождение токена; тексты диалогов передаются строками через _show_version_dialog/_show_help_dialog (321-328) → _show_info (330-331) → AlertManager.show_info_alert (416-428), где message уходит в builder.set_message(message) (424) без вызова markdown-парсера.",
    "evidence_status": "code",
    "evidence": "Plugins/CustomItеmMеnu.plugin:10,321-331,416-428",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/CustomIt%D0%B5mM%D0%B5nu.plugin#L10-L10"
  },
  {
    "id": "plugins-store-customitemmenu:customitemmenu-005",
    "claim": "on_plugin_unload в файле отсутствует (ни определения, ни упоминания; единственная точка входа жизненного цикла — on_plugin_load, строка 47); состояние хранится в настройке custom_items как JSON через get_setting(196) и json.dumps/set_setting (215, 220); set_items() (218) вызывает set_setting(..., reload_settings=True) (220), затем self._add_drawer_links() (223) и get_last_fragment() (224) с fragment.rebuildAllItems() (226) под проверками if fragment and hasattr(fragment, \"rebuildAllItems\") (225).",
    "evidence_status": "code",
    "evidence": "Plugins/CustomItеmMеnu.plugin:47,85,195-226",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/CustomIt%D0%B5mM%D0%B5nu.plugin#L195-L226"
  }
]
```

## Результат ревью

Сборщик предоставил 5 фактов. Принято 5 фактов. Все пять подтверждены указанным исходником; в факте 003 исправлено число элементов `blacklist` (143 вместо 129) и уточнена семантика фильтра (`startswith('_')`), в факте 005 уточнено, что вызов `rebuildAllItems()` защищён проверкой `hasattr`.
