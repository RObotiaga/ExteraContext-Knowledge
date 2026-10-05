---
type: source
source_id: plugins-store-profile-plugin
title: "Источник: Profile_Plugin — генератор карточки профиля в Pillow (Python `.plugin`, `Kangel-Plugins/Plugins-Store`)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 114f5a230b0cf82aa9986a5a89b06b2495c37240
path: "Plugins/Profile_Plugin.plugin"
artifact_sha256: c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1
plugin_id: "Profile_Plugin"
plugin_version: "1.0"
author: "@MorePlugins"
min_version: "11.9.0"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-profile-plugin.md
date: "2026-10-03"
---

# Источник: Profile_Plugin — генератор карточки профиля в Pillow (Python `.plugin`, `Kangel-Plugins/Plugins-Store`)

- Плагин: `Profile_Plugin`, версия `1.0` («Profile Generator»), `__id__ = "Profile_Plugin"` (`14`), `__name__ = "Profile Generator"` (`15`), `__author__ = "@MorePlugins"` (`17`), `__min_version__ = "11.9.0"` (`18`), `__icon__ = "NewsEmoji/0"` (`19`), `__version__ = "1.0"` (`20`)
- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Проверенный файл: `Plugins/Profile_Plugin.plugin` — один Python-файл (не `.eaf`), 26 450 байт, 617 строк (LF только, CRLF нет, BOM нет; строка 1 пустая — файл начинается с `\n`; завершающего перевода строки нет)
- SHA-256 артефакта: `c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1` (совпадает с `Plugins-Store/store.json` → `Profile_Plugin.hash` в текущем checkout и с независимой Raw-загрузкой по pinned commit)
- Локальная копия в рабочем checkout: `Plugins-Store/Plugins/Profile_Plugin.plugin`, git blob `ceaaf92a992b496ee9a332dad618afa33fd1a2d9` (`git hash-object --no-filters` совпадает); blob на проверенном commit идентичен (`git rev-parse 114f5a2…:Plugins/Profile_Plugin.plugin` == `HEAD:…` == `ceaaf92…`), файл в рабочем дереве не изменён
- Проверенный commit: `114f5a230b0cf82aa9986a5a89b06b2495c37240` («Update plugin from 10.11.2025», 10.11.2025), существует и является предком `HEAD` (`f8f35b18b6148b20027b3bdeff505d240086444a`). Сам файл плагина на этом commit не менялся с `9719d95` («Update plugin in 29.10.25»), где он и появился целиком (617 строк)
- Каталог на pinned commit: `store.txt` — для `Profile_Plugin` содержит только `url`; `store.json` с `hash`/`version` на pinned commit отсутствует. `store.json` в текущем checkout (`HEAD`) содержит `Profile_Plugin.version = "1.0"` и `hash = c97b1e50…`
- Pinned URL: https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin
- Pinned Raw (независимо скачан: HTTP 200, 26 450 байт, sha256 `c97b1e50…` и git blob `ceaaf92…` совпали с локальной копией): https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin
- Внешние зависимости обработки: `PIL` (`Image`, `ImageDraw`, `ImageFont` — `11`), `requests` (`12`), `threading` (`12`), `uuid`/`os` (`12`); UI/хост-хелперы — `BulletinHelper` (`5`), `get_send_messages_helper`, `get_messages_controller`, `send_request`, `RequestCallback`, `send_message` (`4`), `ApplicationLoader` (`6`), `TLRPC` (`7`), `File` (`8`), `Locale` (`9`), `log` (`10`)

## Проверенные утверждения

1. **Рендеринг карточки профиля в Pillow.** `create_profile_image` (`363`) задаёт геометрию (`364–370`), берёт путь шрифта `FontManager.get(self.font_index).get_path()` (`372`) и создаёт шесть начертаний через `ImageFont.truetype(font_path, 18/14/15/16/14/13)` (`374–379`); при исключении каждый из шести шрифтов заменяется на `ImageFont.load_default()` (`381–386`, седьмой вызов — в `create_premium_icon`, `538`). После расчёта высоты (`388–396`) холст создаётся как `img = Image.new('RGB', (WIDTH, height), self._hex_to_rgb(self.bg_color))` (`397`), рисование идёт через `draw = ImageDraw.Draw(img)` (`398`). Дополнительно `Image.new` используется для круглой маски и аватара (`406`, `408` — `"L"` и `"RGBA"`) и для иконки Premium (`535`), `ImageDraw.Draw` — для маски и Premium (`407`, `536`). Результат сохраняется ровно один раз: `img.save(output_path, "PNG")` (`517`), сразу после чего вызывается `self._send_profile(output_path)` (`518`). Сохранения в JPEG/WEBP и повторных `img.save` в файле нет. См. `Plugins/Profile_Plugin.plugin:363–398,372–386,517–518`.

2. **Перехват исходящих сообщений и отмена команды `.profile`.** Хук регистрируется в `on_plugin_load` вызовом `self.add_on_send_message_hook()` (`45`) внутри `try/except` (`41–47`); сам callback — `on_send_message_hook(self, account, params) -> HookStrategy` (`86`). Не-строковый `params.message` возвращает `HookResult()` (`87–88`), затем текст сравнивается с настройкой `command = self.get_setting("command", ".profile")` (`91`) по условию точного равенства или префикса `command + " "` (`93`). Внутри — разбор `message_text.split(maxsplit=1)` (`95`), при отсутствии цели показывается `BulletinHelper.show_error("Укажите ID пользавателя")` и возвращается `HookResult(strategy=HookStrategy.CANCEL)` (`97–98`); далее собираются цвета через `validate_hex_color` (`106–116`), создаётся `ProfileManager(...)` (`118–124`) и вызывается `profile.generate_profile()` (`125`), после чего снова возвращается `HookResult(strategy=HookStrategy.CANCEL)` (`126`). Ветка `except` логирует `traceback` и тоже возвращает `CANCEL` (`127–130`), а несовпавший текст — `HookResult()` (`131`). Итого `HookStrategy.CANCEL` встречается трижды (`98`, `126`, `130`). Настройка команды объявлена декларативно в `create_settings` (`51–57`, `default=".profile"`). См. `Plugins/Profile_Plugin.plugin:41–47,86–131,51–57`.

3. **`FontManager.init()`: объявление шрифтов, фоновая загрузка и кэш в `extra_profiles/`.** `FontManager.init()` (`556`) заполняет список пятью `Font(...)` (`558–562`: Huninn — `.ttf`, Roboto/Montserrat/Ubuntu — `.woff2`, «Кастомный шрифт» с `download_uri=None`) и запускает `threading.Thread(target=FontManager._download_fonts, daemon=True).start()` (`564`). Поток (`566–570`) для каждого шрифта с `download_uri` и отсутствующим файлом вызывает `font.download()` (`569–570`), который делает `requests.get(self.download_uri, timeout=10)` (`613`) и пишет ответ в `self.get_path()` (`614–615`). `Font.get_path()` (`599–604`) формирует `<name>.ttf` (`603`) в каталоге `Filesystem.get_temp_dir()` (`157–167`), то есть `<ApplicationLoader.getFilesDirFixed()>/extra_profiles/` (`159`, `162`). Кастомный шрифт потоком не скачивается: при `index == 4` URL берётся из `FontManager.custom_font_url` и качается лениво в `FontManager.get` (`575–586`, `requests.get(url, timeout=15)` — `581`); `requests.get` в файле всего два (`581`, `613`), `import requests` — `12`. См. `Plugins/Profile_Plugin.plugin:556–570,599–617,157–167,575–586`.

4. **Отправка PNG в чат.** `_send_profile(output_path)` (`543`) получает хелпер `helper = get_send_messages_helper()` (`545`), генерирует фото `photo = helper.generatePhotoSizes(output_path, None)` (`546`) и отправляет `send_message({"peer": self.params.peer, "photo": photo, "path": output_path})` (`547`). `output_path` — файл `profile_<uuid4>.png` в `extra_profiles/`, собранный в `_create_profile` (`266–275`, путь — `270`), а вызов идёт из `create_profile_image` сразу после `img.save` (`517–518`). Ошибка логируется и показывает `LocalizationManager.get_string("photo_error")` (`548–550`). `generatePhotoSizes` и `send_message` встречаются в файле по одному разу (`546`, `547`). См. `Plugins/Profile_Plugin.plugin:543–550,266–275,517–518`.

5. **Негативное свидетельство: `on_plugin_unload` и очистка в файле отсутствуют.** Полнотекстовый поиск по pinned файлу: `on_plugin_unload` — 0 совпадений; `remove_on_send_message_hook`/`remove_hook` — 0; `os.remove`/`unlink`/`shutil`/`rmtree`/`cleanup` — 0. Единственная работа с потоком — `threading.Thread(..., daemon=True).start()` (`564`): ссылка на поток не сохраняется, `join`/остановки нет. Хук, зарегистрированный в `on_plugin_load` (`45`), кодом плагина не снимается. Временные файлы создаются и не удаляются: `avatar_<uuid4>.jpg` (`252–255`), `profile_<uuid4>.png` (`268–270`, сохраняется в `517`, отправляется в `547`), `custom_font.ttf` (`578`) и `<Font>_*.ttf` (`603–604`); `Filesystem.write_file` (`173–179`) только создаёт файлы. См. `Plugins/Profile_Plugin.plugin:1–617,41–47,156–179,252–255,266–275,517,543–570,599–617`.

## Границы проверки

Утверждения подтверждены статическим чтением pinned артефакта: построчное чтение исходника, полнотекстовый поиск по ключевым символам, сверка git blob (`HEAD` == pinned commit == локальный файл), sha256 (локальный файл == `store.json` в `HEAD` == независимая Raw-загрузка по commit) и HTTP-проверка pinned Raw. Плагин не устанавливался и не запускался в клиенте, поэтому это не подтверждает ни загрузку плагина, ни runtime-совместимость с ExteraGram `>=11.9.0`, ни фактическую отрисовку/отправку изображения. Все `evidence_status` — `code`, ни один факт не является `runtime-verified`.

Границы по фактам: (001) `ImageFont.truetype` для трёх из четырёх объявленных URL получает файл с расширением `.ttf`, хотя источник — `.woff2` (`559–561` против `603`), поэтому на устройстве реально может срабатывать именно fallback `load_default()`; поведение зависит от сборки Pillow и не проверялось. (002) вызов `self.add_on_send_message_hook()` находится внутри `try/except` (`46–47`), то есть ошибка `FontManager.init()`/`LocalizationManager.init()` (`43–44`) предотвращает регистрацию хука; при этом факт фиксирует контракт кода (`on_send_message_hook` + `CANCEL`), а не срабатывание на конкретной сборке. Сам API `add_on_send_message_hook(priority=0)` подтверждён официальной документацией SDK в базе знаний (`official-sdk:hook-registration`), но приоритет в этом плагине не задаётся (дефолт). (003) формулировка «`init()` скачивает» неточна: сетевые вызовы выполняет `Font.download` (`613`) из daemon-потока (`566–570`), а кастомный URL — лениво в `FontManager.get` (`581`); сам `FontManager.init()` объявляет список и стартует поток. (004) `get_send_messages_helper` и `generatePhotoSizes` в базе знаний ExteraContext как отдельные символы не подтверждены (`find_api` — пусто), `check_compatibility` по `generatePhotoSizes` для ExteraGram/Android/Python вернул `unknown`, поэтому подтверждён только вызов, а не успешная отправка фото на целевой версии. (005) отсутствие `on_plugin_unload` в файле не доказывает утечку хуков: хост может сбрасывать инстанс плагина и его регистрации при выгрузке, а `daemon=True` (`564`) не блокирует завершение JVM; доказано лишь отсутствие собственного кода очистки. Отдельно: на pinned commit каталог — `store.txt` без `hash`/`version`, `store.json` появился позже, поэтому hash-сверка сделана по локальному `store.json` (`HEAD`) и по Raw-загрузке, а не по каталогу на pinned commit.

## Проверенные факты (JSON)

```json
[
  {
    "id": "plugins-store-profile-plugin:profile-plugin-001",
    "claim": "Карточка профиля рендерится в Pillow: create_profile_image создаёт холст Image.new('RGB', ...), рисует через ImageDraw.Draw, создаёт шесть начертаний ImageFont.truetype с fallback на ImageFont.load_default() и сохраняет результат один раз через img.save(output_path, \"PNG\").",
    "evidence_status": "code",
    "evidence": "Plugins/Profile_Plugin.plugin:363-398,372-386,517-518",
    "internal_evidence": "create_profile_image:363 (константы WIDTH/AVATAR_SIZE/AVATAR_LEFT/AVATAR_TOP/NAME_LEFT/PADDING/HEADER_HEIGHT:364-370); font_path = FontManager.get(self.font_index).get_path():372; ImageFont.truetype(font_path, 18/14/15/16/14/13):374-379; fallback ImageFont.load_default() для каждого из шести шрифтов:381-386; расчёт высоты с учётом about и reg_date:388-396; img = Image.new('RGB', (WIDTH, height), self._hex_to_rgb(self.bg_color)):397; draw = ImageDraw.Draw(img):398; прямоугольник шапки:399; круглая маска Image.new('L'):406 + ImageDraw.Draw(mask):407, аватар Image.new('RGBA'):408, img.paste:415; эллипс-заглушка с инициалами:417-431; иконка Premium: Image.new('RGBA'):535, ImageDraw.Draw(img):536, draw.text с ImageFont.load_default():538; img.save(output_path, \"PNG\"):517 (единственный img.save в файле); self._send_profile(output_path):518; ImageFont.truetype — 6 совпадений (374-379), ImageFont.load_default — 7 (381-386,538), Image.new — 4 (397,406,408,535), ImageDraw.Draw — 3 (398,407,536)",
    "artifact_sha256": "c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L363-L398",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L363-L398",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L372-L386",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L517-L518"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin"
  },
  {
    "id": "plugins-store-profile-plugin:profile-plugin-002",
    "claim": "Исходящие сообщения перехватываются через self.add_on_send_message_hook() в on_plugin_load; команда .profile (по умолчанию) обрабатывается и отменяется HookResult(strategy=HookStrategy.CANCEL).",
    "evidence_status": "code",
    "evidence": "Plugins/Profile_Plugin.plugin:41-47,86-131,51-57",
    "internal_evidence": "on_plugin_load:41 (try:42; FontManager.init():43; LocalizationManager.init():44; self.add_on_send_message_hook():45; except:46; plog:47); on_send_message_hook(self, account, params) -> HookStrategy:86; не-строковый params.message → HookResult():87-88; command = self.get_setting(\"command\", \".profile\"):91; условие message_text == command or message_text.startswith(command + \" \"):93; split(maxsplit=1):95; нет цели → BulletinHelper.show_error(\"Укажите ID пользавателя\"):97; HookResult(strategy=HookStrategy.CANCEL):98; validate_hex_color по 12 цветам:106-116; ProfileManager(...):118-124; profile.generate_profile():125; HookResult(strategy=HookStrategy.CANCEL):126; except → plog + BulletinHelper.show_error(get_string(\"error\")):127-129; HookResult(strategy=HookStrategy.CANCEL):130; финальный HookResult():131; add_on_send_message_hook — 1 совпадение (45), HookStrategy.CANCEL — 3 (98,126,130); настройка command объявлена в create_settings:51-57 (Input key=\"command\", default=\".profile\")",
    "artifact_sha256": "c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L86-L131",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L41-L47",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L86-L131",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L51-L57"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin"
  },
  {
    "id": "plugins-store-profile-plugin:profile-plugin-003",
    "claim": "FontManager.init() объявляет пять шрифтов и запускает загрузку в отдельном daemon-потоке; файлы скачиваются через requests и кэшируются в <ApplicationLoader.getFilesDirFixed()>/extra_profiles/.",
    "evidence_status": "code",
    "evidence": "Plugins/Profile_Plugin.plugin:556-570,599-617,157-167",
    "internal_evidence": "FontManager.init():556; список Font(...):558-562 (Huninn .ttf:558; Roboto .woff2:559; Montserrat .woff2:560; Ubuntu .woff2:561; «Кастомный шрифт» download_uri=None:562); threading.Thread(target=FontManager._download_fonts, daemon=True).start():564; _download_fonts:566-570 (if font.download_uri and not font.exists(): font.download():569-570); Font.download:609-617 (requests.get(self.download_uri, timeout=10):613; open(self.get_path(),'wb') + write(resp.content):614-615); Font.get_path:599-604 (fn = self.name.replace(\" \", \"_\") + \".ttf\":603); Filesystem.get_temp_dir:157-167 (ApplicationLoader.getFilesDirFixed():159; File(fixed_dir, \"extra_profiles\").getAbsolutePath():162; os.makedirs:163-164); FontManager.get(index==4):573-586 (custom_font_url:575; requests.get(url, timeout=15):581; fallback FontManager.fonts[0]:585); import requests:12; requests.get — 2 совпадения (581,613); threading.Thread — 1 (564); extra_profiles — 1 (162)",
    "artifact_sha256": "c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L556-L570",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L556-L570",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L599-L617",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L157-L167",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L573-L586"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin"
  },
  {
    "id": "plugins-store-profile-plugin:profile-plugin-004",
    "claim": "Сгенерированный PNG отправляется в чат через get_send_messages_helper().generatePhotoSizes(output_path, None) и send_message({\"peer\": ..., \"photo\": photo, \"path\": output_path}).",
    "evidence_status": "code",
    "evidence": "Plugins/Profile_Plugin.plugin:543-550,266-275,517-518",
    "internal_evidence": "_send_profile(output_path):543; helper = get_send_messages_helper():545; photo = helper.generatePhotoSizes(output_path, None):546; send_message({\"peer\": self.params.peer, \"photo\": photo, \"path\": output_path}):547; except → plog(\"send_profile error\") + BulletinHelper.show_error(get_string(\"photo_error\")):548-550; путь файла формируется в _create_profile:266-275 (tmp_file = f\"profile_{uuid.uuid4()}.png\":268; temp_dir = Filesystem.get_temp_dir():269; file_path = Filesystem.get_absolute_path(temp_dir, tmp_file):270; create_profile_image(file_path, profile_data, avatar_path):272); вызов после сохранения: img.save(output_path, \"PNG\"):517 → self._send_profile(output_path):518; generatePhotoSizes — 1 совпадение (546), send_message — 1 (547); import get_send_messages_helper/send_message:4",
    "artifact_sha256": "c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L543-L550",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L543-L550",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L266-L275",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L517-L518"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin"
  },
  {
    "id": "plugins-store-profile-plugin:profile-plugin-005",
    "claim": "Негативное свидетельство: в pinned файле нет on_plugin_unload; зарегистрированный send-message-хук кодом плагина не снимается, daemon-поток загрузки шрифтов не останавливается и не join-ится, созданные временные файлы (аватар, профиль, шрифты) не удаляются.",
    "evidence_status": "code",
    "evidence": "Plugins/Profile_Plugin.plugin:1-617,41-47,156-179,252-255,266-275,517,543-570,599-617",
    "internal_evidence": "полнотекстовый поиск по pinned файлу: on_plugin_unload — 0 совпадений; remove_on_send_message_hook/remove_hook — 0; os.remove/unlink/shutil/rmtree/cleanup — 0; регистрация хука self.add_on_send_message_hook():45, парного снятия нет; threading.Thread(..., daemon=True).start():564 — ссылка на поток не сохраняется, join/остановки нет; Filesystem.get_temp_dir создаёт каталог:163-164; avatar_<uuid4>.jpg:252-255; profile_<uuid4>.png:268-270 + img.save:517 + send_message:547; custom_font.ttf:578; <Font>_*.ttf:603-604; Filesystem.write_file только пишет файл:173-179; on_plugin_load:41-47 — единственный lifecycle-метод плагина (есть только on_plugin_load и create_settings)",
    "artifact_sha256": "c97b1e50a2eec17e8c26d6d334edac380c0de9eaaaac6f2089170545ceded7f1",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L41-L47",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L41-L47",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L156-L179",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L252-L275",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin#L1-L617"
    ],
    "url_verified": "https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/114f5a230b0cf82aa9986a5a89b06b2495c37240/Plugins/Profile_Plugin.plugin"
  }
]
```

## Результат ревью

Сборщик предоставил 5 фактов. Принято 5 фактов. Все пять подтверждены содержимым pinned артефакта (`Plugins/Profile_Plugin.plugin` @ `114f5a230b0cf82aa9986a5a89b06b2495c37240`, sha256 `c97b1e50…`, blob `ceaaf92…`, HTTP 200 по pinned Raw, 26 450 байт). Уточнены границы: (001) литерал в коде — `img.save(output_path, "PNG")` с двойными кавычками, `truetype` вызывается для шести размеров, fallback — шесть отдельных `load_default()`; (002) регистрация хука находится в `try/except` (`46–47`), `CANCEL` возвращается тремя путями (`98`, `126`, `130`), приоритет не задаётся; (003) сетевые вызовы делает `Font.download` (`613`) из daemon-потока (`564`, `566–570`), кастомный URL — лениво в `FontManager.get` (`581`), кэш — `<getFilesDirFixed()>/extra_profiles/` (`159`, `162`), три из четырёх URL — `.woff2` при сохранении как `.ttf` (`603`); (004) словарь `send_message` также использует двойные кавычки, `peer` берётся из `self.params.peer`, а `get_send_messages_helper`/`generatePhotoSizes` базой знаний не подтверждены (`check_compatibility` → `unknown`); (005) отсутствие `on_plugin_unload` подтверждено поиском (0 совпадений), но это не доказывает утечку — host может сбрасывать инстанс и его регистрации, а `daemon=True` не блокирует JVM. Расхождения по pinned commit нет: commit существует, является предком `HEAD`, blob файла на нём совпадает с локальной копией; каталог на pinned commit — `store.txt` (только `url`), `store.json` с `hash c97b1e50…` есть лишь в текущем checkout.
