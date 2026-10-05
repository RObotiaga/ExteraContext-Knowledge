# Ревью: plugins-store-culprit-detector

- Плагин: `culprit_detector` (Culprit Detector), версия `1.7.0`, Python `.plugin`, `__min_version__ = "12.6.4"`
- Commit (как в задании): `c38b0cdc42f868dd89ae96747e4bb4ebf2a30646` — существует, «Update plugin: culprit_detector v1.7.0», является предком `HEAD` (`a39cec371261c22355ce106b1a0ca559d8340f16`)
- Проверенный файл: `Plugins/culprit_detector.plugin`, 1 293 614 байт, 25 120 строк, UTF-8 без BOM; локальная копия побайтово совпадает с blob на pinned commit и с `HEAD`, `git diff c38b0cdc… HEAD -- Plugins/culprit_detector.plugin` пуст
- SHA-256 артефакта: `da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0` (совпадает с `Plugins-Store/store.json` → `culprit_detector.hash` и с Raw-загрузкой по pinned commit: HTTP 200, 1 293 614 байт)
- Вшитый нативный артефакт: независимая распаковка `_SO_ARM64` (`349` — `2663`) дала ELF64 little-endian AArch64 (`e_machine = 0xB7`), 400 648 байт, sha256 `559b7408…`; в бинаре присутствуют `cd_abi_version`, `cd_start`, `cd_stop`, `cd_oom_start`, `cd_smaps_groups`, `cd_dmabuf_fd_scan`, `cd_gref_start`, `cd_gref_live`
- Источник: [plugins-store-culprit-detector.md](../sources/plugins-store-culprit-detector.md)
- Проверка: независимое сопоставление 5 кандидатов с содержимым pinned файла (построчное чтение, сверка git blob и sha256, Raw-загрузка по commit, независимая распаковка вшитого блоба); статус доказательности — `code` (статический анализ, не runtime-проверка)

## Вердикт

Сборщик предоставил 5 фактов. Принято 5 фактов.

| ID | Вердикт | Основание |
|---|---|---|
| `plugins-store-culprit-detector:culprit-detector-001` | Принято | Каталог вердиктов — `/storage/emulated/0/Download/CulpritDetector` (`263–267`, `280–286`); вердикты — собственные JSON (`crash_verdict.json` — `287`, `leak_verdict.json` — `3199`, `globalref_verdict.json` — `18806`), запись через `_atomic_json_write` (`7332` → `6278`, `json.dumps` — `6292`; `_write_crash_verdict` — `8050` → `8081`). Движковый sentinel `plugin_crash_sentinel` только проверяется («не трогаем» — `23499–23503`), и в `_coexist_selfcheck` прямо зафиксирован «режим ПАССИВНЫЙ: prefs движка не пишем (plugin_enabled_/crash_detected/crash_plugin_id)» (`23506`). |
| `plugins-store-culprit-detector:culprit-detector-002` | Принято | Блоб `_SO_ARM64` (`349`) распаковывается `zlib.decompress(base64.b64decode(...))` (`4153`) в `libculprit.so` (`_SO_NAME` — `2667`); независимая распаковка подтверждает ELF64 AArch64. Загрузка: `System.load(path)` (`4929`), затем `ctypes.CDLL(path)` (`4937`); `lib.cd_abi_version()` (`4940`) сверяется с `_SO_ABI_EXPECT = 15` (`2668`), при несовпадении — `_ABI_FAIL` и inert (`4943–4947`). |
| `plugins-store-culprit-detector:culprit-detector-003` | Принято | `jclass("java.lang.Thread$UncaughtExceptionHandler")` (`12378`), `_CrashHandler(dynamic_proxy(_UEH_IFACE))` (`12385`) сохраняет `prev` (`12386–12387`) и вызывает `self._prev.uncaughtException(thread, ex)` (`12393–12396`); `_capture_crash` возвращает `False` (`12374`), поэтому цепочка не подавляется. Установка — `23519–23521`; атрибуция по стектрейсу — `ex.getStackTrace()` (`12107–12115`), `stack_top` (`12202`), `_pm_scan_stack` (`12421–12434`, применение — `12734–12735`). |
| `plugins-store-culprit-detector:culprit-detector-004` | Принято | `cd_oom_start` объявлен и вызывается с порогами (`4419–4420`, `22965–22967`) с потоком-потребителем на eventfd (`22971–22973`); smaps — `cd_smaps_groups`/`cd_smaps_rollup` (`4643–4646`, вызовы `10523–10529`, `10555–10560`); dma-buf — `cd_dmabuf_fd_scan` (`4647–4648`, `10501–10510`); JNI global-ref — `cd_gref_*` (`4507–4525`, чтение `8932–8986`, live/overflow `19585–19600`). Все объявления идут через `ctypes`. |
| `plugins-store-culprit-detector:culprit-detector-005` | Принято | `on_plugin_load` (`22812`) вызывает `_reg_snapshot_restore()` (`22833–22838`, `4053`) и `self._install_crash_handler()` (`22857`, повторно `22863`); `on_plugin_unload` (`22999`) сохраняет реестр `_reg_snapshot_dump()` (`23002–23007`, `4020`), вызывает `_NLIB.cd_stop()` (`23100–23104`) и возвращает `_JThread.setDefaultUncaughtExceptionHandler(_PREV_UEH)` (`23105–23108`). |

## Замечания о точности

1. **Факт 001 («пассивность»).** Подтверждённое содержание — отказ от записи crash-состояния движка при чтении (не изменении) sentinel `plugin_crash_sentinel` (`23499–23503`) и сохранение вердиктов в собственные JSON. Формулировка не должна читаться как «плагин ничего не меняет»: он ставит хуки, нативные обработчики сигналов и UEH; в opt-in ветке `_AUTO_DISABLE` (по умолчанию `False` — `343`) может выключить приписанного виновника через `PluginsController` (`23481–23482`, `23526–23538`), а `_b31_enable_pref()` включает сам плагин через `PC.setPluginEnabled(self, True)` (`18094–18099`). `set_setting("safe_mode", False)` (`22816`) — собственная настройка плагина, а не prefs движка. Также в исходнике нет обращений к `SharedPreferences`/main-settings движка.
2. **Факт 002 (ABI 15).** Статически подтверждены вшивание arm64 ELF, путь `ctypes.CDLL` и константа ожидания `15`; значение, которое вернёт `cd_abi_version()` на конкретной сборке `.so`, не исполнялось (arm64-бинарь на Android-хосте не запускался). Порядок «сначала `System.load`, при ошибке — `CDLL`» в исходнике залогирован как штатный (`4931–4934`), поэтому `CDLL` — рабочий путь загрузки, а не только fallback.
3. **Факт 003 (цепочка и атрибуция).** `_capture_crash` имеет единственную точку выхода `return False` (`12374`), значит ветка `if not swallow` практически всегда приводит к вызову предыдущего хэндлера; переменная `swallow` оставлена как защитная. Установка идемпотентна (`_OUR_UEH is not None` → ранний выход, `23516–23517`). Атрибуция виновника — эвристика по подстрокам id плагинов в кадрах стека (`_pm_scan_stack`, `12421–12434`), а не доказательство причины падения.
4. **Факт 004 (телеметрия).** Подтверждены наличие символов, объявления `argtypes`/`restype` через `ctypes` и вызовы. Измеренные значения (проценты smaps, число dma-buf, счётчики global-ref, фактический порог OOM) в этом источнике не проверялись: для этого нужен запуск на устройстве. Часть телеметрии дублируется чтением `/proc/self/smaps_rollup` (`10592–10594`).
5. **Факт 005 (объём симметрии).** Симметрия подтверждена для пары «tid→plugin реестр + UEH». Остальные ветки очистки при выгрузке (множество списков `*_unhooks`, `_b*_stop`, `cd_gref_stop`, `cd_oom_stop`) в факт не включены, хотя в исходнике присутствуют (`23008–23123`).

## Границы проверки

Плагин не устанавливался и не запускался в клиенте: это статическая проверка одного pinned файла плюс независимая распаковка вшитого `.so`, а не runtime-совместимость. Все пять фактов имеют `evidence_status: code`. Вшитый бинарь — ELF64 AArch64 (`e_machine = 0xB7`), поэтому его нельзя исполнить в окружении проверки; корректность возвращаемых им значений (`cd_abi_version()`, PSS smaps, dma-buf, global-ref) не подтверждена. Внутренние классы клиента (`com.exteragram.messenger.plugins.PluginsController`, `java.lang.Thread$UncaughtExceptionHandler`, `org.telegram.messenger.ApplicationLoader`, `org.telegram.messenger.LocaleController`) — не документированный plugin API; факты описывают только поведение исходника, а не успешность работы на конкретной сборке. Расхождения pinned commit нет.

## Pinned источник

Проверенный (commit существует, предок `HEAD`, Raw HTTP 200, 1 293 614 байт, sha256 `da78c1b9…` совпадает с локальным файлом и `store.json`):

https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin

Raw-подтверждение:

https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin
