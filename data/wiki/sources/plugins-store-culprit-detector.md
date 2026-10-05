---
type: source
source_id: plugins-store-culprit-detector
title: "Источник: Culprit Detector (culprit_detector) — пассивный детектор виновников падений и утечек"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: c38b0cdc42f868dd89ae96747e4bb4ebf2a30646
path: "Plugins/culprit_detector.plugin"
artifact_sha256: da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0
plugin_id: "culprit_detector"
plugin_version: "1.7.0"
author: "@chestertech & @useful_plugins"
min_version: "12.6.4"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-culprit-detector.md
date: "2026-10-03"
---

# Источник: Culprit Detector (culprit_detector) — пассивный детектор виновников падений и утечек

- Плагин: `culprit_detector`, версия `1.7.0` («Culprit Detector», `__id__ = "culprit_detector"` — строка 33, `__version__ = "1.7.0"` — строка 35)
- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Проверенный файл: `Plugins/culprit_detector.plugin` — один Python-файл (не `.eaf`), 1 293 614 байт, 25 120 строк, UTF-8 без BOM
- SHA-256 артефакта: `da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0` (совпадает с `Plugins-Store/store.json` → `culprit_detector.hash`, с локальной копией в checkout и с независимо скачанным Raw-файлом по pinned commit: HTTP 200, 1 293 614 байт)
- Локальная копия в рабочем checkout: `Plugins-Store/Plugins/culprit_detector.plugin` — содержимое побайтово совпадает с blob на pinned commit и с `HEAD` (сравнение после нормализации переводов строк расхождений не дало; `git diff c38b0cdc… HEAD -- Plugins/culprit_detector.plugin` пуст, последний commit, менявший файл, — сам `c38b0cdc…`)
- Проверенный commit: `c38b0cdc42f868dd89ae96747e4bb4ebf2a30646` («Update plugin: culprit_detector v1.7.0»), существует в клоне, является предком `HEAD` (`f8f35b18b6148b20027b3bdeff505d240086444a`); `store.json` даёт `version: 1.7.0`, `status: utilities`, `min_version: 12.6.4`
- Pinned URL: https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin
- Pinned Raw (независимо скачан: HTTP 200, 1 293 614 байт, sha256 совпал с локальным файлом и `store.json`): https://raw.githubusercontent.com/Kangel-Plugins/Plugins-Store/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin
- Встроенный нативный артефакт: блоб `_SO_ARM64` (строка 349 — 2 663, base64 из 222 112 символов) распаковывается `zlib.decompress(base64.b64decode(...))` в 400 648 байт; независимая распаковка даёт ELF64, little-endian, `e_machine = 0xB7` (AArch64/arm64), `e_type = 3` (DYN), sha256 `559b74082818c2f3bc97a4d5701b15a2ac67700804d68f487aafea732703550e`; в бинаре присутствуют символы `cd_abi_version`, `cd_start`, `cd_stop`, `cd_oom_start`, `cd_smaps_groups`, `cd_dmabuf_fd_scan`, `cd_gref_start`, `cd_gref_live`, `cd_thread_sig_unblock`

## Проверенные утверждения

1. **Собственные JSON-вердикты вместо prefs движка (пассивный режим).** Каталог плагина задаётся `_DIR_CANDIDATES` (`263–267`: `/storage/emulated/0/Download/CulpritDetector`), путь строится `_data_path(name)` (`280–286`); вердикты — это отдельные JSON-файлы в этом каталоге: `crash_verdict.json` (`287`), `leak_verdict.json` (`3199`), `globalref_verdict.json` (`18806`), `native_crash_verdict.json` (`2673`) и др. Запись идёт через атомарный помощник `_atomic_json_write` (`7332`) → `_atomic_json_write_impl` (`6278`, `json.dumps` — `6292`) с native-путём `cd_verdict_write` и fallback'ами; конкретно вердикт падения пишется в `_write_crash_verdict` (`8050` → `8081`), вердикт утечек — `_b27_write_leak` (`3419` → `3454`). Prefs движка не пишутся: движковый sentinel `plugin_crash_sentinel` только проверяется на существование (`23499` — `File(_fdir, "plugin_crash_sentinel")`, `23500` — `_sf.exists()`, `23503` — «не трогаем»), а в `_coexist_selfcheck` явно зафиксирован «режим ПАССИВНЫЙ: prefs движка не пишем (plugin_enabled_/crash_detected/crash_plugin_id)» (`23506`). См. `Plugins/culprit_detector.plugin:263-287,3199,23499-23506`.

2. **Вшитый arm64 ELF `libculprit.so` и загрузка через `ctypes.CDLL` (ожидаемая ABI 15).** Блоб `_SO_ARM64` (`349`) распаковывается `_b3_extract_so` (`4148–4153`) и материализуется как файл `libculprit.so` (`_SO_NAME` — `2667`); независимая распаковка подтверждает ELF64 AArch64 (см. метаданные выше). Загрузка: сначала пробуется `jclass("java.lang.System").load(path)` (`4929`), затем библиотека открывается `lib = ctypes.CDLL(path)` (`4937`); версия ABI читается `lib.cd_abi_version()` (`4940`) и сверяется с константой `_SO_ABI_EXPECT = 15` (`2668`): при несовпадении выставляется `_ABI_FAIL`, натив отключается, и плагин остаётся inert (`4943–4947`); при совпадении пишется лог «native .so ABI=%d OK (expected %d)» (`4949`). Далее идёт `cd_init`/`cd_start` (`4954–4965`). См. `Plugins/culprit_detector.plugin:349,2667-2668,4148-4153,4929,4937-4949`.

3. **Подмена `Thread$UncaughtExceptionHandler` через `dynamic_proxy` с цепочкой на предыдущий хэндлер и атрибуцией по стектрейсу.** Интерфейс берётся как `jclass("java.lang.Thread$UncaughtExceptionHandler")` (`12378`); класс `_CrashHandler(dynamic_proxy(_UEH_IFACE))` (`12384–12385`) в `__init__(prev)` сохраняет предыдущий хэндлер (`12386–12387`), а в `uncaughtException(thread, ex)` вызывает `self._prev.uncaughtException(thread, ex)` (`12393–12396`); `_capture_crash` в единственной точке выхода возвращает `False` (`12374`), то есть `swallow` не подавляет цепочку. Установка: `prev = _JThread.getDefaultUncaughtExceptionHandler()`, `_PREV_UEH = prev`, `_JThread.setDefaultUncaughtExceptionHandler(_OUR_UEH)` (`23519–23521`). Атрибуция виновника — по стектрейсу: кадры собираются из `ex.getStackTrace()` (`12107–12115`), укладываются в `stack_top` (`12202`), а `_pm_scan_stack` (`12421–12434`) сопоставляет кадры с известными id плагинов (использование — `12734–12735`, `src = "self-kill/jstack"`). См. `Plugins/culprit_detector.plugin:12107-12115,12374,12376-12397,12421-12434,12734-12735,23519-23521`.

4. **Мониторинг памяти и телеметрия через нативную библиотеку.** Pre-OOM watchdog запускается `_NLIB.cd_oom_start(sentinel, pct*1000, rate, poll_ms, topn, cooldown_ms)` (`22965–22967`) с последующим потоком-потребителем `culprit-oom-fmt` на eventfd (`22971–22973`) и остановкой `cd_oom_stop` (`23072`). Снимки памяти: `cd_smaps_groups` / `cd_smaps_rollup` (объявления — `4643–4646`; вызовы — `10523–10529`, `10555–10560`) и текстовый `/proc/self/smaps_rollup` (`10592–10594`); dma-buf — `cd_dmabuf_fd_scan` (объявление — `4647–4648`; вызов — `10501–10510`). Счётчики JNI global-ref: `cd_gref_start/stop/running/total/untagged/tags/snapshot/top1/live/overflow` объявляются через `ctypes` (`4507–4525`) и читаются в `_gref_*` (`8932–8986`), включая live/overflow (`19585–19600`). См. `Plugins/culprit_detector.plugin:4507-4525,4643-4648,8932-8986,10501-10510,10523-10529,22965-22973,23072`.

5. **Симметричный жизненный цикл.** `on_plugin_load` (`22812`) вызывает `_reg_snapshot_restore()` — восстановление tid→plugin реестра после reload (`22833–22838`, лог «tid->plugin реестр восстановлен после reload») — и ставит UEH: `self._install_crash_handler()` (`22857`), плюс повторно в цепочке install-ов (`22863`). `on_plugin_unload` (`22999`) сначала сохраняет реестр `_reg_snapshot_dump()` (`23002–23007`), затем снимает натив: `_NLIB.cd_stop()` (`23100–23104`), после чего возвращает предыдущий хэндлер `_JThread.setDefaultUncaughtExceptionHandler(_PREV_UEH)` и обнуляет `_OUR_UEH` (`23105–23108`). См. `Plugins/culprit_detector.plugin:22812,22833-22838,22857,22863,22999-23007,23100-23108`.

## Границы проверки

Утверждения подтверждены статическим чтением pinned артефакта (построчное чтение, сверка git blob, sha256, независимая Raw-загрузка по commit, сверка с `store.json`) и независимой распаковкой вшитого блоба. Плагин не устанавливался и не запускался в клиенте, arm64-библиотека не исполнялась, поэтому все `evidence_status` — `code`; ни один факт не является `runtime-verified`.

Границы по фактам:

1. «Пассивность» здесь означает отсутствие записи crash-состояния движка (`plugin_enabled_`/`crash_detected`/`crash_plugin_id`) и чтение (не изменение) движкового sentinel `plugin_crash_sentinel` (`23499–23503`). Это не означает отсутствия побочных эффектов вообще: плагин ставит хуки и нативные обработчики сигналов, а в ветке opt-in `_AUTO_DISABLE` (по умолчанию `False` — `343`) может выключить приписанного виновника через `PluginsController` (`23526–23538`, `23481–23482`); отдельная ветка само-восстановления `_b31_enable_pref()` вызывает `PC.setPluginEnabled(self, True)` для самого плагина (`18094–18099`). `set_setting("safe_mode", False)` (`22816`) относится к собственным настройкам плагина, а не к prefs движка.
2. Значение, возвращаемое `cd_abi_version()`, статически не проверяемо (arm64-код не исполнялся на устройстве); подтверждены факт вшивания arm64 ELF, путь `ctypes.CDLL`, константа ожидания `15` и логика отключения при несовпадении. Порядок «сначала `System.load`, затем `CDLL`» означает, что `CDLL` — рабочий путь загрузки и/или fallback при ошибке `System.load`.
3. Цепочка на предыдущий хэндлер реализована и фактически всегда исполняется, так как `_capture_crash` заканчивается `return False` (`12374`); ветка `if not swallow` оставлена как защитная. Установка UEH идемпотентна (`_OUR_UEH is not None` → ранний выход, `23516–23517`). Атрибуция по стектрейсу — эвристическая (сопоставление подстрок id плагинов с кадрами), а не доказательство причины падения.
4. Наличие и объявление всех перечисленных `cd_*` символов через `ctypes` подтверждено; значения, которые вернёт нативная библиотека на конкретном устройстве (порог, PSS smaps, число dma-buf/global-ref), в этом источнике не измерялись. Для `cd_oom_start` в исходнике указаны параметры порога/скорости/периода (`_OOM_PCT`, `_OOM_RATE_MBPS`, `_OOM_POLL_S`, `_OOM_TOPN`, `_OOM_COOLDOWN_S`), но не проверялось их фактическое влияние на runtime.
5. «Симметричность» подтверждена в объёме пары «tid-реестр + UEH»: реестр сохраняется при выгрузке (`23002–23007`) и восстанавливается при загрузке (`22833–22838`), UEH ставится (`22857`) и возвращается (`23105–23108`). Прочие ветки cleanup (множество `*_unhooks`, `_b*_stop`) в этот факт не включены.

## Проверенные факты (JSON)

```json
[
  {
    "id": "plugins-store-culprit-detector:culprit-detector-001",
    "claim": "Вердикты падений и утечек сохраняются в собственные JSON-файлы плагина в его каталоге CulpritDetector (crash_verdict.json, leak_verdict.json, globalref_verdict.json и др.) через атомарную запись _atomic_json_write; prefs движка не модифицируются — движковый sentinel plugin_crash_sentinel только проверяется, а запись plugin_enabled_/crash_detected/crash_plugin_id явно исключена в режиме «ПАССИВНЫЙ».",
    "evidence_status": "code",
    "evidence": "Plugins/culprit_detector.plugin:263-287,3199,8081,23499-23506",
    "internal_evidence": "_DIR_CANDIDATES:263-267; _resolve_dir:268-278; _data_path:280-286; _CRASH_FILE_NAME=crash_verdict.json:287; _LEAK_FILE_NAME=leak_verdict.json:3199; _GLOBALREF_FILE_NAME=globalref_verdict.json:18806; _write_crash_verdict:8050 -> _atomic_json_write:8081; _b27_write_leak:3419 -> _atomic_json_write:3454; _atomic_json_write:7332 -> _atomic_json_write_impl:6278 (json.dumps:6292, cd_verdict_write:6313-6325); sentinel plugin_crash_sentinel «не трогаем»:23499-23503; «режим ПАССИВНЫЙ: prefs движка не пишем (plugin_enabled_/crash_detected/crash_plugin_id)»:23506; _AUTO_DISABLE=False:343",
    "artifact_sha256": "da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L23499-L23506",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L23499-L23506",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L263-L287",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L8050-L8086"
    ]
  },
  {
    "id": "plugins-store-culprit-detector:culprit-detector-002",
    "claim": "В плагин вшит arm64 ELF libculprit.so: base64-блоб _SO_ARM64 распаковывается через zlib и записывается как libculprit.so; библиотека загружается через ctypes.CDLL, а ожидаемая ABI равна 15 (_SO_ABI_EXPECT) — при несовпадении lib.cd_abi_version() с 15 натив отключается и плагин остаётся inert.",
    "evidence_status": "code",
    "evidence": "Plugins/culprit_detector.plugin:349,2667-2668,4148-4153,4929,4937-4949",
    "internal_evidence": "_SO_ARM64 = ( ... base64 ... ):349-2663; распаковка zlib.decompress(base64.b64decode(...)):4153; выделенный путь libculprit.so:4154; _SO_NAME:2667; _SO_ABI_EXPECT=15:2668; System.load(path):4929; lib = ctypes.CDLL(path):4937; _abi = int(lib.cd_abi_version()):4940; проверка _abi != _SO_ABI_EXPECT -> _ABI_FAIL + inert:4943-4947; лог ABI OK:4949; cd_init/cd_start:4954-4965; независимая распаковка блоба: ELF64 LE AArch64 (e_machine=0xB7), 400648 байт, sha256 559b74082818c2f3bc97a4d5701b15a2ac67700804d68f487aafea732703550e, символ cd_abi_version присутствует",
    "artifact_sha256": "da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L4937-L4949",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L4937-L4949",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L2667-L2668",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L4148-L4153"
    ]
  },
  {
    "id": "plugins-store-culprit-detector:culprit-detector-003",
    "claim": "Плагин подменяет java.lang.Thread$UncaughtExceptionHandler: класс _CrashHandler строится через dynamic_proxy(_UEH_IFACE), сохраняет предыдущий хэндлер и вызывает его в uncaughtException; виновник атрибутируется по стектрейсу исключения — кадры берутся из ex.getStackTrace(), а _pm_scan_stack сопоставляет их с известными id плагинов.",
    "evidence_status": "code",
    "evidence": "Plugins/culprit_detector.plugin:12107-12115,12374,12376-12397,12421-12434,12734-12735,23519-23521",
    "internal_evidence": "jclass(\"java.lang.Thread$UncaughtExceptionHandler\"):12378; from java import dynamic_proxy:12384; class _CrashHandler(dynamic_proxy(_UEH_IFACE)):12385; __init__(self, prev) + self._prev = prev:12386-12387; self._prev.uncaughtException(thread, ex):12394-12395; единственный выход _capture_crash — return False:12374; _PREV_UEH/_OUR_UEH:12401-12402; кадры из ex.getStackTrace():12107-12115; stack_top:12202; _pm_scan_stack:12421-12434; использование для атрибуции (src=self-kill/jstack):12734-12735; установка prev=getDefaultUncaughtExceptionHandler + setDefaultUncaughtExceptionHandler(_OUR_UEH):23519-23521",
    "artifact_sha256": "da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L12384-L12396",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L12384-L12396",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L12376-L12397",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L23519-L23521"
    ]
  },
  {
    "id": "plugins-store-culprit-detector:culprit-detector-004",
    "claim": "Мониторинг памяти и телеметрия идут через нативную библиотеку по ctypes: pre-OOM watchdog запускается cd_oom_start с порогами (процент/скорость/период/топ/cooldown), снимки smaps снимаются cd_smaps_groups и cd_smaps_rollup, dma-buf — cd_dmabuf_fd_scan, счётчики JNI global-ref — семейством cd_gref_* (total/untagged/tags/snapshot/live/overflow).",
    "evidence_status": "code",
    "evidence": "Plugins/culprit_detector.plugin:4418-4420,4507-4525,4643-4648,8932-8986,10501-10510,10523-10529,22965-22973",
    "internal_evidence": "cd_oom_start argtypes:4419-4420; вызов cd_oom_start(sentinel, pct*1000, rate, poll_ms, topn, cooldown_ms):22965-22967; rc<0 -> detection disabled:22968-22969; поток culprit-oom-fmt на cd_b6_eventfd:22971-22973; cd_oom_stop при выгрузке:23072; cd_smaps_groups/cd_smaps_rollup argtypes:4644-4645; cd_dmabuf_fd_scan argtypes:4647-4648; _dmabuf_fd_scan -> cd_dmabuf_fd_scan:10501-10510; _smaps_scan_native -> cd_smaps_groups:10523-10529; _smaps_rollup_native -> cd_smaps_rollup:10555-10560; /proc/self/smaps_rollup текст:10592-10594; cd_gref_* argtypes/restype:4507-4525; чтение счётчиков:8932-8986; live/overflow счётчики:19585-19600",
    "artifact_sha256": "da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L22965-L22973",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L22965-L22973",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L4507-L4525",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L10501-L10529"
    ]
  },
  {
    "id": "plugins-store-culprit-detector:culprit-detector-005",
    "claim": "Жизненный цикл симметричен: on_plugin_load восстанавливает tid→plugin реестр через _reg_snapshot_restore и ставит UEH через _install_crash_handler, а on_plugin_unload сохраняет реестр _reg_snapshot_dump, вызывает нативный cd_stop() и возвращает предыдущий хэндлер через _JThread.setDefaultUncaughtExceptionHandler(_PREV_UEH).",
    "evidence_status": "code",
    "evidence": "Plugins/culprit_detector.plugin:22812,22833-22838,22857,22863,22999-23007,23100-23108",
    "internal_evidence": "on_plugin_load:22812; _reg_snapshot_restore() + лог «tid->plugin реестр восстановлен после reload»:22833-22838; self._install_crash_handler():22857; повторно в цепочке install-ов:22863; on_plugin_unload:22999; _reg_snapshot_dump() + лог «реестр сохранён для reload»:23002-23007; _NLIB.cd_stop() + лог «натив: хуки сняты»:23100-23104; _JThread.setDefaultUncaughtExceptionHandler(_PREV_UEH):23105-23108; _reg_snapshot_dump:4020; _reg_snapshot_restore:4053",
    "artifact_sha256": "da78c1b975ccfec856498abb8e977bfcc9d54023e54c3e84765570321c721fe0",
    "url": "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L23100-L23108",
    "pinned_urls": [
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L23100-L23108",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L22833-L22838",
      "https://github.com/Kangel-Plugins/Plugins-Store/blob/c38b0cdc42f868dd89ae96747e4bb4ebf2a30646/Plugins/culprit_detector.plugin#L22999-L23007"
    ]
  }
]
```

## Результат ревью

Сборщик предоставил 5 фактов. Принято 5 фактов. Все пять подтверждены содержимым pinned артефакта (`Plugins/culprit_detector.plugin` @ `c38b0cdc42f868dd89ae96747e4bb4ebf2a30646`, sha256 `da78c1b9…`, HTTP 200 по pinned Raw, локальный файл побайтово совпадает с blob на commit и с `HEAD`). Уточнены границы: (001) «пассивность» = отсутствие записи crash-prefs движка при чтении sentinel, а не отсутствие хуков и побочных эффектов; (002) подтверждён вшитый ELF64 AArch64 и загрузка через `ctypes.CDLL` с ожидаемой ABI 15, но не runtime-возврат `cd_abi_version()`; (003) цепочка на предыдущий UEH фактически всегда исполняется, поскольку `_capture_crash` возвращает `False`, а атрибуция по стектрейсу эвристическая; (004) подтверждены объявления/вызовы `cd_oom_start`, `cd_smaps_*`, `cd_dmabuf_fd_scan`, `cd_gref_*` через ctypes, без измерения результатов на устройстве; (005) симметрия подтверждена для пары «tid-реестр + UEH». Расхождения pinned commit нет: commit существует, является предком `HEAD`, файл на нём идентичен локальной копии, `store.json` содержит `version 1.7.0` и `hash da78c1b9…`.
