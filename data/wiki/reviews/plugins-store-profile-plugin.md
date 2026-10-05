---
type: review
source_id: plugins-store-profile-plugin
title: "Источник: Profile_Plugin — генератор карточки профиля в Pillow (Python `.plugin`, `Kangel-Plugins/Plugins-Store`)"
reviewer: independent-verifier
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 114f5a230b0cf82aa9986a5a89b06b2495c37240
artifact_sha256: c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1
plugin_id: "Profile_Plugin"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: plugins-store-profile-plugin

- Плагин: `Profile_Plugin` (Profile Generator), версия `1.0`, Python `.plugin`, `__min_version__ = "11.9.0"`
- Commit (как в задании): `114f5a230b0cf82aa9986a5a89b06b2495c37240` — существует, «Update plugin from 10.11.2025», ancestor of `HEAD`; файл плагина на нём идентичен локальной копии (blob `ceaaf92a992b496ee9a332dad618afa33fd1a2d9`), расхождения нет
- Проверенный файл: `Plugins/Profile_Plugin.plugin`, 26 450 байт, 617 строк (LF, CRLF нет, BOM нет; строка 1 пустая, завершающего перевода строки нет)
- SHA-256 артефакта: `c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1` (совпадает с `Plugins-Store/store.json` в текущем checkout и с независимой Raw-загрузкой по pinned commit: HTTP 200, 26 450 байт, git blob `ceaaf92…`)
- Источник: [plugins-store-profile-plugin.md](../sources/plugins-store-profile-plugin.md)
- Проверка: независимое сопоставление 5 кандидатов с содержимым pinned файла (построчное чтение, полнотекстовый поиск, сверка git blob/sha256, независимая Raw-загрузка по commit); статус доказательности — `code` (статический анализ, не runtime-проверка)

## Вердикт

Сборщик предоставил 5 фактов. Принято 5 фактов.

| ID | Вердикт | Основание |
|---|---|---|
| `plugins-store-profile-plugin:profile-plugin-001` | Принято | `create_profile_image` (`363`) создаёт холст `img = Image.new('RGB', (WIDTH, height), ...)` (`397`), рисует через `draw = ImageDraw.Draw(img)` (`398`), создаёт шесть начертаний `ImageFont.truetype(font_path, 18/14/15/16/14/13)` (`374–379`) с fallback на `ImageFont.load_default()` (`381–386`) и сохраняет единожды `img.save(output_path, "PNG")` (`517`) с последующей отправкой (`518`). |
| `plugins-store-profile-plugin:profile-plugin-002` | Принято | Хук регистрируется в `on_plugin_load` вызовом `self.add_on_send_message_hook()` (`45`); callback `on_send_message_hook(self, account, params)` (`86`) сравнивает текст с `command = self.get_setting("command", ".profile")` (`91`, `93`) и возвращает `HookResult(strategy=HookStrategy.CANCEL)` (`98`, `126`, `130`), а на не-строковый `params.message` и несовпавший текст — `HookResult()` (`88`, `131`). |
| `plugins-store-profile-plugin:profile-plugin-003` | Принято | `FontManager.init()` (`556`) объявляет пять `Font(...)` (`558–562`) и запускает `threading.Thread(target=FontManager._download_fonts, daemon=True).start()` (`564`); поток вызывает `font.download()` (`569–570`), где `requests.get(self.download_uri, timeout=10)` (`613`) пишет файл в `<ApplicationLoader.getFilesDirFixed()>/extra_profiles/<name>.ttf` (`159`, `162`, `599–604`); кастомный URL качается лениво в `FontManager.get` (`581`). |
| `plugins-store-profile-plugin:profile-plugin-004` | Принято | `_send_profile` (`543`) получает `helper = get_send_messages_helper()` (`545`), вызывает `photo = helper.generatePhotoSizes(output_path, None)` (`546`) и `send_message({"peer": self.params.peer, "photo": photo, "path": output_path})` (`547`); `output_path` — `profile_<uuid4>.png` в `extra_profiles/` (`268–270`), отправка идёт сразу после `img.save` (`517–518`). |
| `plugins-store-profile-plugin:profile-plugin-005` | Принято | Полнотекстовый поиск по pinned файлу: `on_plugin_unload` — 0, `remove_on_send_message_hook`/`remove_hook` — 0, `os.remove`/`unlink`/`shutil`/`rmtree`/`cleanup` — 0; хук зарегистрирован (`45`) и не снимается; `threading.Thread(..., daemon=True)` (`564`) не сохраняется и не join-ится; временные файлы `avatar_<uuid4>.jpg` (`252–255`), `profile_<uuid4>.png` (`268–270`, `517`, `547`), `custom_font.ttf` (`578`) и `<Font>_*.ttf` (`603–604`) не удаляются. |

## Замечания о точности

1. **Факт 001 (литералы и число вызовов).** В кандидате сохранение приведено как `img.save(output_path, 'PNG')`, в коде — `img.save(output_path, "PNG")` (`517`) с двойными кавычками; семантика та же (`str`), но цитата не буквальная. `ImageFont.truetype` вызывается шесть раз (`374–379`), fallback — шесть отдельных `ImageFont.load_default()` (`381–386`), а не общий shim; седьмой `load_default` — в `create_premium_icon` (`538`). `Image.new` встречается 4 раза (`397`, `406`, `408`, `535`), `ImageDraw.Draw` — 3 (`398`, `407`, `536`).
2. **Факт 002 (условия и стратегии).** `self.add_on_send_message_hook()` (`45`) стоит внутри `try/except` (`46–47`): исключение в `FontManager.init()` или `LocalizationManager.init()` (`43–44`) предотвращает регистрацию хука. `CANCEL` возвращается тремя путями (`98` — нет цели, `126` — успешная обработка, `130` — исключение), а на несовпавший текст и не-строковый `params.message` возвращается `HookResult()` (`131`, `88`) — стратегия по умолчанию. Приоритет хука не задаётся (дефолт `priority=0`); сам API `add_on_send_message_hook(priority=0)` подтверждён официальной документацией SDK в базе знаний (`official-sdk:hook-registration`).
3. **Факт 003 (кто именно скачивает).** Формулировка «`init()` скачивает» неточна: `FontManager.init()` только объявляет список (`558–562`) и стартует daemon-поток (`564`), сетевой вызов делает `Font.download` (`613`) из `_download_fonts` (`566–570`). Кастомный шрифт (индекс 4) потоком не скачивается: у него `download_uri=None` (`562`), а URL из настройки качается лениво в `FontManager.get` (`581`, `timeout=15`). Кэш-каталог — `<getFilesDirFixed()>/extra_profiles/` (`159`, `162`). Три из четырёх объявленных URL — `.woff2` (`559–561`), но сохраняются под именем `<name>.ttf` (`603`) и передаются в `ImageFont.truetype` (`374`): при несовместимой сборке Pillow это приведёт к fallback `load_default()` — на устройстве не проверялось.
4. **Факт 004 (цитата и подтверждённость API).** В словаре кода также двойные кавычки (`547`), ключи `peer`/`photo`/`path`; `peer` берётся из `self.params.peer` события хука. `get_send_messages_helper` и `generatePhotoSizes` в базе знаний ExteraContext как отдельные символы не подтверждены (`find_api` — пусто), `check_compatibility` по `generatePhotoSizes` для ExteraGram/Android/Python вернул `unknown`. Факт фиксирует вызов в исходнике, а не фактическую отправку фото на целевой сборке.
5. **Факт 005 (негативное свидетельство).** Отсутствие `on_plugin_unload` подтверждено поиском (0 совпадений), но само по себе не доказывает утечку хуков: хост может сбрасывать инстанс плагина и его регистрации при выгрузке, а `daemon=True` (`564`) не блокирует завершение JVM. Доказано ровно то, что собственного кода очистки в файле нет. Символ `remove_on_send_message_hook` в базе знаний также не подтверждён (`find_api` — пусто), поэтому возможность явного снятия send-хука версионно не установлена; рецепт `recipes/managed-hooks.md` прямо указывает, что пустой список cleanup не подтверждает снятие перехвата.
6. **Расхождение по каталогу.** На pinned commit `114f5a2…` каталог — `store.txt`, где у `Profile_Plugin` есть только `url` (без `hash`/`version`); `store.json` на этом commit отсутствует. Поэтому hash-сверка выполнена с локальным `store.json` в `HEAD` (`version = "1.0"`, `hash = c97b1e50…`) и с независимой Raw-загрузкой по pinned commit, а не с каталогом на pinned commit.

## Границы проверки

Плагин не устанавливался и не запускался в клиенте: это статическая проверка одного pinned файла, а не runtime-совместимость. Все пять фактов имеют `evidence_status: code`. Поведение host-API (`get_send_messages_helper`, `generatePhotoSizes`, `send_message`, `ApplicationLoader.getFilesDirFixed`, `BulletinHelper`, `TLRPC.TL_upload_getFile`, `TL_inputPeerPhotoFileLocation`) зависит от версии APK и в этом источнике не проверялось; `check_compatibility` по `generatePhotoSizes` вернул `unknown`. Отсутствие runtime-проверки означает, что не подтверждены ни фактическая отрисовка карточки, ни загрузка аватара через `send_request`/`RequestCallback` (`233–242`), ни отправка фото. Строка 1 файла пустая (файл начинается с `\n`), поэтому якоря `#L…` соответствуют содержимому 1:1.

## Pinned источник

Проверенный (pinned commit существует, предок `HEAD`, blob `ceaaf92…` совпадает с локальной копией, Raw HTTP 200, 26 450 байт, sha256 `c97b1e50…`):
https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin

Raw-подтверждение:
https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin
