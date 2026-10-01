---
type: source
source_id: plugins-store-dex-native
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-dex-native.md
date: 2026-10-01
---

# KPM Plugins-Store: Динамическая загрузка DEX, нативные вызовы ctypes и Elyx-модули (.eaf)

Источник: раздел партиции `plugins-store-dex-native` официального каталога [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store), включающий 111 плагинов и модулей. В выборку вошли плагины, использующие динамическую загрузку байткода Dalvik/ART (`DexClassLoader`, `InMemoryDexClassLoader`), упаковку байткода (Base64, сжатие `zlib`, хвостовые комментарии скрипта), прямое взаимодействие с нативным кодом через `ctypes` (`android_dlopen_ext`, вызовы C/Go/Rust разделяемых библиотек `.so`, низкоуровневые структуры `libc`), многофайловые пакеты Elyx (`.eaf`) с картами переопределения путей (`refmap`), а также встроенные средства аудита и защиты от намеренных сбоев среды.

## Роль и границы источника

Партиция `plugins-store-dex-native` демонстрирует наиболее технически глубокие способы расширения возможностей Android-клиентов ExteraGram и AyuGram поверх базовой песочницы Chaquopy Python:

1. **Расширение возможностей виртуальной машины ART**: плагины не ограничиваются готовыми Java-классами клиента Telegram, а динамически компилируют и догружают собственные Java/Kotlin компоненты (например, кастомные контейнеры UI, хуки Xposed/Pine, контроллеры тем, парсеры медиапотоков).
2. **Преодоление ограничений платформы Android**:
   - Обход запрета на выполнение модифицируемого байткода на Android 14+ (`SecurityException: Writable dex file is not allowed`) через явное управление POSIX-атрибутами доступа (`os.chmod(path, 0o444)`).
   - Преодоление изоляции пространств имён динамического компоновщика Android Linker Namespace (Android 7.0+) при загрузке библиотек `.so` через прямой вызов системной функции `android_dlopen_ext` из `libdl.so`.
   - Обход ограничений Hidden API на рефлексию системных классов через запуск доверенного байткода `ni.shikatu.hiddenapi.HiddenApiWrapper`.
3. **Высокопроизводительные нативные вычисления**: интеграция C, C++, Go и Rust библиотек для задач, непосильных интерпретатору Python (прокси-движки Sing-box/WireGuard, эмуляторы Libretro/QuickNES, движок DOOM, real-time цифровая обработка звука DSP, транскодирование Ogg Opus).
4. **Многофайловая дистрибуция Elyx (`.eaf`)**: переход от монолитных однофайловых `.plugin` к структурированным ZIP-контейнерам с виртуальным маппингом файлов через `refmap.yml`/`refmap.json`, изоляцией ресурсов и распространением бинарных APK-компаньонов.
5. **Защита процесса и анализ угроз**: выявление скрытых бинарных нагрузок (Base64-сигнатуры DEX `ZGV4` и ELF `f0VMRg`) и блокировка попыток плагинов совершить принудительное завершение клиента (`Process.killProcess`, вызовы `kill`/`exit` в `libc.so`).

**Границы источника**:
- Все примеры извлечены непосредственно из рабочего каталога плагинов магазина KPM (`Plugins-Store/Plugins/`).
- Статус большинства доказательств классифицирован как `code`: код проверен статическим анализом и синтаксическим сопоставлением, но запуск всех бинарных `.so` модулей на реальном оборудовании не производился.
- Зависимость от архитектуры процессора: нативные библиотеки `.so` требуют сборки под соответствующий ABI (в подавляющем большинстве случаев `arm64-v8a`, реже `armeabi-v7a`), плагины без мультиархитектурных бинарников не запустятся на x86_64 эмуляторах.

---

## Покрытие

| Путь или артефакт | Извлечённые механизмы и данные | Границы и специфические условия |
|---|---|---|
| `Plugins-Store/Plugins/MandreTweaks.plugin` | Файловый `DexClassLoader`, схема скачивания DEX, замена `.tmp`, `os.chmod(0o444)`, двусторонний `TweaksRunnableBridge`, рефлексивный вызов `unload()`. | Требует доступный HTTP-источник или локальный кэш `dex_modules`. |
| `Plugins-Store/Plugins/SwagLogs.plugin` | Очистка кэша DEX, смена прав доступа перед `os.remove` (`0o666`), инстанцирование Kotlin-раннера. | Зависит от сигнатуры файла в локальных настройках плагина. |
| `Plugins-Store/Plugins/custom_profile.plugin` | Встраивание сжатого `_DEX_B64` в тело плагина, распаковка `zlib.decompress()`, права `0o400`, каталог `cpb_native`. | Тяжелый скрипт (>1.6 МБ) из-за встроенного бинарного блоба. |
| `Plugins-Store/Plugins/etg_max.plugin` | Контроль целостности скачиваемого DEX через SHA-256, метод `_make_read_only()`, системный fallback ClassLoader. | При несовпадении хеша загрузка прерывается. |
| `Plugins-Store/Plugins/account_hider.plugin` | Чистая загрузка из памяти через `InMemoryDexClassLoader` и `ByteBuffer.wrap()`, вызов `start()` / `stop()`. | Доступно только на Android 8.0+ (API 26+). |
| `Plugins-Store/Plugins/AtmosFX.plugin` | Считывание собственного байткода из комментариев скрипта (`# DEX_BEGIN`), распаковка без засорения AST Python. | Требует права на чтение собственного файла плагина (`open(__file__)`). |
| `Plugins-Store/Plugins/material_settings_list.plugin` | Проверка `Build.VERSION.SDK_INT >= 26`, zlib-распаковка Base64, логирование и информирование пользователя. | При API < 26 плагин корректно сообщает о несовместимости. |
| `Plugins-Store/Plugins/DynamicDexLoader.plugin` | Универсальный хост динамической загрузки DEX по URL из сети, ведение реестра `dynamic_dex_loader.json`. | Отсутствует проверка сигнатур сторонних скачиваемых DEX. |
| `Plugins-Store/Plugins/GreenPass.plugin` | `android_dlopen_ext` из `libdl.so`, структура `android_dlextinfo`, управление памятью C-строк через `libc.free`, Singbox/Go ядро. | Сложная многопоточная инициализация Go runtime внутри одного процесса. |
| `Plugins-Store/Plugins/ReMandre.plugin` | Загрузка C-extensions Python (`_cffi_backend.so`) через `ctypes.PyDLL` с функцией `PyInit_*`, пакетный менеджер нативных модулей. | Требует совместимости версий CPython и ABI. |
| `Plugins-Store/Plugins/extera_doom_native.plugin` | Клонирование `.so` с меткой времени (`libexdoom_session_%d.so`) для изоляции статического C-состояния, рендеринг пикселей в `ctypes.c_uint32*N`. | Память под каждую новую сессию выделяется заново. |
| `Plugins-Store/Plugins/nes_emulator.plugin` | Полная реализация Libretro C-ABI через `ctypes.CFUNCTYPE`, прямой zero-copy маппинг адреса памяти в Java `ByteBuffer` (`from_address`, `memmove`). | Критично удерживать ссылки на Python-колбэки от сборщика мусора. |
| `Plugins-Store/Plugins/culprit_detector.plugin` | Межпоточный кольцевой буфер `_Slot` в памяти Python, нативный Kill-Guard (перехват вызовов `kill`/`exit` в libc), слежение за JNI global refs (`cd_gref_snapshot`). | Требует пересобранную библиотеку `libculprit.so` с совпадающим ABI. |
| `Plugins-Store/Plugins/mandre_lib.plugin` | Системные вызовы `libc.malloc`/`free`, привязка к ядрам CPU `sched_setaffinity`, снятие Hidden API ограничений через DEX. | Низкоуровневые вызовы могут зависеть от версии ядра Linux. |
| `Plugins-Store/Plugins/voice_changer_rt.plugin` | Сложные C-структуры `VcParams` (13 полей DSP параметров), обработка 16-битных PCM буферов. | Чувствителен к задержкам на аудио-потоке. |
| `Plugins-Store/Plugins/voice_changer_rust.plugin` | Интеграция Rust `cdylib` для кодирования/декодирования аудио Opus и расчёта контрольных сумм Ogg CRC. | Требует скомпилированные бинарники `libvoice_dsp_arm64.so`. |
| `Plugins-Store/Plugins/air_raid_alert.eaf` | Пакет Elyx: спецификация `refmap.yml`, `metainfo.yml`, внешние зависимости `requirements: requests>=2.31`. | Необходим установленный рантайм Elyx / KPM. |
| `Plugins-Store/Plugins/nowfylite.eaf` | Встраивание Android APK-компаньона (`nowfylite/app/NowfyBridge.apk`) и установка через `PackageInstaller` сессию. | Запрашивает системное разрешение на установку неизвестных приложений. |
| `Plugins-Store/Plugins/plugin_guard.plugin` | Сканирование плагинов на сигнатуры DEX (`ZGV4`) и ELF (`f0VMRg`), аудит системных символов (`/system/bin/sh`, `ptrace`, `execve`). | Статический эвристический анализ, возможны false positives. |

---

## Технические факты и архитектурные решения

### 1. Файловая динамическая загрузка DEX (`DexClassLoader`) и ограничения Android 14+

Файловая загрузка скомпилированного байткода DEX применяется в плагинах со сложной логикой (например, модульные надстройки интерфейса, темы и логгеры):
- `MandreTweaks.plugin` ([строки 293–305](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L293-L305)):
  ```python
  cl = DexClassLoader(
      self.dex_path,
      self.ctx.getDir("dex_opt", 0).getAbsolutePath(),
      None,
      self.ctx.getClassLoader()
  )
  self.dex_main_class = cl.loadClass("com.swagaplugins.plugin.modulartweaks.MandreTweaks")
  ```
- **Защита от Writable DEX на Android 14+ (API 34+)**:
  Начиная с Android 14, компонент ART выбрасывает критическое исключение `SecurityException: Writable dex file is not allowed`, если файл DEX доступен для записи процессу.
  В `MandreTweaks.plugin` ([строки 158–167, 279–286](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L158-L167)) и `SwagLogs.plugin` ([строки 140–152](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SwagLogs.plugin#L140-L152)) выработан доказанный паттерн:
  1. Данные пишутся во временный файл `dex_path + ".tmp"`.
  2. Если целевой файл уже существовал, его права предварительно расширяются до `0o666`, чтобы позволить удаление или замену.
  3. Выполняется атомарная замена через `os.replace(tmp_path, self.plugin.dex_path)`.
  4. Непосредственно перед вызовом `DexClassLoader` файлу присваиваются права только для чтения: `os.chmod(self.plugin.dex_path, 0o444)` (или `0o400` в `custom_profile.plugin`).
- **Контракт выгрузки и деинициализации**:
  В `on_plugin_unload()` плагин обязан вызвать метод деинициализации в скомпилированном классе:
  `self.dex_main_class.getDeclaredMethod("unload").invoke(None)` ([MandreTweaks.plugin:214-222](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L214-L222)). Это позволяет Java-коду снять хуки Xposed/Pine и освободить ресурсы. Ссылка `self.dex_main_class` зануляется для предотвращения утечки `ClassLoader`.
- **Двусторонний мост Java-Python через dynamic_proxy**:
  Для получения обратных вызовов из Java в Python плагин создаёт класс-мост, реализующий интерфейс `java.lang.Runnable`:
  ```python
  class TweaksRunnableBridge(dynamic_proxy(Runnable)):
      def __init__(self, plugin, dex_cls):
          super().__init__()
          self.plugin = plugin
          self.cls = dex_cls
      def run(self):
          # Обработка событий из DEX
          ...
  ```
  Экземпляр моста передаётся в метод инициализации Java-модуля: `init_method.invoke(None, TweaksRunnableBridge(self, self.dex_main_class), self.ctx)` ([MandreTweaks.plugin:26-35, 301-304](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L26-L35)).

---

### 2. Загрузка DEX в оперативной памяти (`InMemoryDexClassLoader`)

Загрузка байткода непосредственно из памяти процесса без сохранения на диск является самым распространённым паттерном (76 плагинов в выборке):
- **Сигнатура конструктора**: `InMemoryDexClassLoader(ByteBuffer dex_buffer, ClassLoader parent)`.
- **Способы хранения байткода**:
  1. *Встроенная Base64-строка*: `base64.b64decode(DEX_B64)` используется в плагинах от `@RnPlugins` (`account_hider.plugin`, `Material_Containers.plugin`, `ReactionsBelow.plugin`, `chip_folders.plugin`, `quiet_reactions.plugin`).
     ```python
     dex_bytes = base64.b64decode(DEX_B64)
     buffer = ByteBuffer.wrap(dex_bytes)
     parent_cl = ApplicationLoader.applicationContext.getClassLoader()
     self.dex_loader = InMemoryDexClassLoader(buffer, parent_cl)
     self.dex_class = self.dex_loader.loadClass("dev.rooni.accounthider.AccountHider")
     self.dex_instance = self.dex_class.newInstance()
     self.dex_class.getMethod("start").invoke(self.dex_instance)
     ```
  2. *Сжатие zlib поверх Base64*: `zlib.decompress(base64.b64decode(DEX_BASE64))` в `material_settings_list.plugin` ([строки 140–152](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/material_settings_list.plugin#L140-L152)) и `zwyNoForwardLimit.plugin` ([строки 300–315](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/zwyNoForwardLimit.plugin#L300-L315)), что сокращает размер плагина на 40–60%.
  3. *Хвостовой блок комментариев скрипта*: в `AtmosFX.plugin` ([строки 111–120](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/AtmosFX.plugin#L111-L120)), `ayu_rofls.plugin`, `wide_messages.plugin` и `wp.plugin` бинарные данные размещаются в конце `.plugin` файла в строках комментария между маркерами `# DEX_BEGIN` и `# DEX_END`. Метод `_read_payload()` открывает собственный файл через `open(__file__, "r", encoding="utf-8")`, вырезает комментарии, декодирует Base64 и распаковывает zlib. Это исключает тяжелые строковые константы из AST Python при компиляции скрипта.
  4. *Сетевая загрузка в память*: `DynamicDexLoader.plugin` ([строки 105–135](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/DynamicDexLoader.plugin#L105-L135)) загружает байты через `requests.get(url).content` и сразу оборачивает их в `ByteBuffer.wrap()`, монтируя модули на лету без касания диска.
- **Ограничение по версии Android**:
  `InMemoryDexClassLoader` доступен только на Android 8.0+ (API 26+). В `material_settings_list.plugin` ([строка 134](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/material_settings_list.plugin#L134)) и `AtmosFX.plugin` ([строка 66](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/AtmosFX.plugin#L66)) присутствует явный guard:
  `if Build.VERSION.SDK_INT < 26: raise RuntimeError("InMemoryDexClassLoader requires Android 8.0+")`.
- **Гибридный фолбэк (In-Memory → File-based)**:
  В `expressive_tab.plugin` ([строки 205–225](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/expressive_tab.plugin#L205-L225)) и `global_font_picker.plugin` ([строки 805–820](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/global_font_picker.plugin#L805-L820)) реализована отказоустойчивая схема: плагин сначала пытается загрузить байткод через `InMemoryDexClassLoader`. При возникновении любой ошибки байты записываются в файл в папке `context.getCodeCacheDir()`, файл помечается `os.chmod(dex_file, 0o444)` и загружается через стандартный `DexClassLoader`.

---

### 3. Преодоление изоляции Linker Namespace в Android через `android_dlopen_ext`

Начиная с Android 7.0 (Nougat) и вплоть до Android 14+, системный компоновщик Bionic изолирует пространства имён библиотек (`android_namespace_t`). Прямой вызов `ctypes.CDLL(path)` для пользовательской `.so` библиотеки из папки плагина часто завершается ошибкой `dlopen failed: library "..." not found`.

Плагины `GreenPass.plugin` ([строки 5935–5975](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/GreenPass.plugin#L5935-L5975)), `ReMandre.plugin` ([строки 254–280](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ReMandre.plugin#L254-L280)), `Vless.plugin` ([строки 174–205](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Vless.plugin#L174-L205)), `exitfy.plugin` ([строки 2329–2365](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/exitfy.plugin#L2329-L2365)), `extera_doom_native.plugin` ([строки 44855–44895](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/extera_doom_native.plugin#L44855-L44895)) и `nes_emulator.plugin` ([строки 365–420](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nes_emulator.plugin#L365-L420)) используют системный вызов `android_dlopen_ext` из `libdl.so`:

```python
class android_dlextinfo(ctypes.Structure):
    _fields_ = [
        ("flags", ctypes.c_uint64),
        ("reserved_addr", ctypes.c_void_p),
        ("reserved_size", ctypes.c_size_t),
        ("relro_fd", ctypes.c_int),
        ("library_fd", ctypes.c_int),
        ("library_fd_offset", ctypes.c_uint64),
        ("library_namespace", ctypes.c_void_p),
    ]

libdl = ctypes.CDLL("libdl.so")
open_ext = libdl.android_dlopen_ext
open_ext.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(android_dlextinfo)]
open_ext.restype = ctypes.c_void_p

info = android_dlextinfo()
# Флаги 2 | 0x100 соответствуют RTLD_NOW | RTLD_GLOBAL
handle = open_ext(path.encode("utf-8"), 2 | 0x100, ctypes.byref(info))
if handle:
    lib = ctypes.CDLL(path, handle=handle)
else:
    lib = ctypes.CDLL(path, mode=2 | 0x100)
```
Полученный нативный дескриптор `handle` передаётся напрямую в конструктор `ctypes.CDLL(path, handle=handle)`, что полностью обходит проверки компоновщика на расположение библиотеки.

---

### 4. Управление памятью C/Go и освобождение указателей через `libc.so`

При вызове функций C или Go runtime, возвращающих динамически выделенные строки (например, JSON-статус или логи), прямой возврат `ctypes.c_char_p` приводит к автоматическому копированию строки в Python-объект, но C-буфер остаётся неосвобождённым в нативной куче (memory leak).

В `GreenPass.plugin` ([строки 6004–6065](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/GreenPass.plugin#L6004-L6065)) и `Vless.plugin` ([строки 257–305](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Vless.plugin#L257-L305)) реализован безопасный паттерн управления памятью:
```python
# Настройка сигнатуры
self.lib.StartCore.argtypes = [ctypes.c_char_p]
self.lib.StartCore.restype = ctypes.c_void_p  # Важно: возврат как указатель, а не c_char_p

self.libc = ctypes.CDLL("libc.so")
self.libc.free.argtypes = [ctypes.c_void_p]

# Вызов и безопасное чтение
result_ptr = self.lib.StartCore(config_bytes)
if result_ptr:
    try:
        raw_str = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode("utf-8", errors="ignore")
    finally:
        self.libc.free(result_ptr)  # Обязательное освобождение буфера в libc
```

---

### 5. Изоляция статического состояния C через сессионное клонирование `.so`

В нативных движках (DOOM, QuickNES Libretro) состояние звуковых буферов, эмулятора и глобальных переменных компилируется как статические переменные C (`static`). В Android вызов `dlclose` не гарантирует фактическую выгрузку библиотеки из адресного пространства процесса (библиотека может удерживаться ссылками других подсистем или внутренним счетчиком компоновщика).

В `extera_doom_native.plugin` ([строки 45690–45698](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/extera_doom_native.plugin#L45690-L45698)) и `nes_emulator.plugin` ([строки 480–485](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nes_emulator.plugin#L480-L485)) применён приём сессионного клонирования:
```python
# Создание уникальной копии бинарника для текущей сессии
load_path = os.path.join(session_dir, f"libexdoom_session_{int(time.time() * 1000)}.so")
shutil.copyfile(orig_so_path, load_path)
self.lib = ctypes.CDLL(load_path)
```
Каждая новая сессия запускает движок с абсолютно чистого листа в изолированном пространстве символов, исключая влияние предыдущей игры на новую.

---

### 6. Zero-Copy обмен памятью и видеокадрами (`from_address`, `memmove`)

Для рендеринга видеокадров и воспроизведения звука в реальном времени преобразование через промежуточные списки Python недопустимо из-за падения FPS:
- В `extera_doom_native.plugin` ([строки 45715–45720, 45980–45995](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/extera_doom_native.plugin#L45715-L45720)):
  ```python
  PixelArray = ctypes.c_uint32 * self.total_pixels
  self.c_pixels = PixelArray()
  # Нативный тикер рендерит кадр напрямую в c_pixels
  self.lib.exdoom_tick(self.c_pixels, self.total_pixels)
  # Быстрое получение байтов фрейма
  self._frame_bytes = ctypes.string_at(ctypes.addressof(self.c_pixels), self.total_pixels * 4)
  ```
- В `nes_emulator.plugin` ([строки 1205–1215, 1360–1370](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nes_emulator.plugin#L1205-L1215)): отображение прямого Java-буфера `ByteBuffer` на массив ctypes по физическому адресу без промежуточного копирования:
  ```python
  # addr — нативный адрес Java direct ByteBuffer
  self._bb_mem = (ctypes.c_char * self._bb_cap).from_address(addr)
  # Быстрое копирование PCM-звука или пикселей напрямую в память Java
  ctypes.memmove(self._bb_mem, (ctypes.c_char * byte_count).from_buffer(pcm), byte_count)
  ```

---

### 7. Привязка Libretro C-ABI через `ctypes.CFUNCTYPE`

Плагины эмуляторов (`nes_emulator.plugin`, `emulate_core.eaf`) реализуют стандартный ABI ретро-эмуляторов Libretro на чистом Python:
- Регистрация C-колбэков ([nes_emulator.plugin:660–670](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nes_emulator.plugin#L660-L670)):
  ```python
  EnvironmentCallback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_uint, ctypes.c_void_p)
  VideoRefreshCallback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_size_t)
  AudioSampleCallback = ctypes.CFUNCTYPE(None, ctypes.c_int16, ctypes.c_int16)
  AudioSampleBatchCallback = ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.POINTER(ctypes.c_int16), ctypes.c_ulong)
  InputPollCallback = ctypes.CFUNCTYPE(None)
  InputStateCallback = ctypes.CFUNCTYPE(ctypes.c_int16, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint)
  ```
- Удержание ссылок: созданные экземпляры трамплинов CFUNCTYPE сохраняются в постоянных полях объекта плагина (`self._c_callbacks = [...]`), иначе сборщик мусора Python удалит нативный адрес колбэка, что приведёт к немедленному `SIGSEGV` при вызове из C.

---

### 8. Низкоуровневая телеметрия, межпоточные кольцевые буферы и Kill-Guard

Плагин `culprit_detector.plugin` (более 23 тыс. строк кода) реализует комплексную систему глубокой диагностики нативного и управляемого рантайма:
- **Разделяемый межпоточный буфер `_Slot`** ([строки 2085–2100, 3350–3370](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/culprit_detector.plugin#L2085-L2100)):
  ```python
  class _Slot(ctypes.Structure):
      _fields_ = [
          ("tid", ctypes.c_int64),
          ("pid_idx", ctypes.c_int32),
          ("seq", ctypes.c_int32)
      ]
  _REG_BUF = ctypes.create_string_buffer(_SLOT_SIZE * _SLOT_COUNT)
  _REG_ADDR = ctypes.addressof(_REG_BUF)
  _NLIB.cd_init(ctypes.c_uint64(_REG_ADDR), _SLOT_COUNT, _SLOT_SIZE)
  ```
- **Нативный Kill-Guard (перехват самоубийств процесса)** ([строки 16760–16815](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/culprit_detector.plugin#L16760-L16815)):
  Некоторые плагины при ошибках или перезагрузке принудительно убивают процесс через `Process.killProcess(Process.myPid())` или системные функции `kill`, `tgkill`, `exit`, `_exit`, `_Exit`. Kill-Guard в `libculprit.so` перехватывает эти функции на уровне `libc.so`, блокирует вызов, формирует вердикт `selfkill_blocked` и позволяет клиенту продолжить работу.
- **Трекинг JNI Global References** ([строки 3705–3710, 17595–17605](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/culprit_detector.plugin#L3705-L3710)):
  Вызов нативной функции `cd_gref_snapshot` опрашивает внутренние таблицы виртуальной машины ART для подсчёта неосвобождённых ссылок JNI по каждому активному плагину.
- **Управление CPU Affinity** ([mandre_lib.plugin:5950–5985](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mandre_lib.plugin#L5950-L5985)):
  Прямой вызов системной функции `sched_setaffinity(pid, mask_size, mask_ptr)` из `libc.so` для распределения тяжелых фоновых потоков по высокопроизводительным ядрам процессора.

---

### 9. Архитектура многофайловых пакетов Elyx (`.eaf`) и распространение APK

Пакеты с расширением `.eaf` представляют собой ZIP-архивы со специализированной модульной структурой:
- **Карта переопределения путей `refmap.yml` / `refmap.json`**:
  Располагается в корне архива и определяет сопоставление виртуальных подсистем с реальными файлами:
  ```yaml
  metainfo: ios_input_panel/meta.yml
  main: ios_input_panel/src/main.pyc
  assets: ios_input_panel/res
  locales: ios_input_panel/locales
  elyxbuilder: ios_input_panel/.elyxbuilder
  ```
- **Манифест `metainfo.yml`**:
  Содержит уникальный `id`, отображаемое `name`, версию `version`, автора `author`, ограничения клиента `app_version: '>=12.9.0'`, SDK `sdk_version: '>=1.4.5.0'`, рантайма Elyx `elyx_version`, и список зависимостей pip `requirements: requests>=2.31`.
- **Встроенные APK-сервисы (`nowfylite.eaf`)**:
  В `nowfylite.eaf` внутри архива содержится полноценное Android-приложение `nowfylite/app/NowfyBridge.apk`. Плагин при загрузке проверяет установку пакета через `PackageManager.getPackageInfo()`. Если мост отсутствует, плагин запускает программную установку через системный `PackageInstaller` ([nowfylite/src/main.py:1200–1260](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nowfylite.eaf)):
  ```python
  installer = context.getPackageManager().getPackageInstaller()
  params = SessionParams(SessionParams.MODE_FULL_INSTALL)
  session_id = installer.createSession(params)
  session = installer.openSession(session_id)
  stream = session.openWrite("NowfyBridge.apk", 0, int(apk_size))
  # Запись байтов и коммит сессии через PendingIntent
  session.commit(pending.getIntentSender())
  ```
  При отказе PackageInstaller плагин выполняет фолбэк на Intent с `ACTION_VIEW` и MIME-типом `application/vnd.android.package-archive`.

---

### 10. Статический анализ безопасности и бинарные эвристики

Плагины `plugin_guard.plugin` и `plugin_verifier.plugin` содержат встроенные сканеры исходного кода плагинов перед их установкой:
- **Детектирование бинарных сигнатур**:
  Поиск Base64-префиксов скомпилированного байткода DEX (`ZGV4`, соответствующий ASCII `dex\n035` или `dex\n038`) и разделяемых библиотек ELF (`f0VMRg`, соответствующий `\x7fELF`) ([plugin_guard.plugin:174–178, 2374–2385](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/plugin_guard.plugin#L174-L178)).
- **Поиск опасных системных символов в `.so`**:
  Сканирование сырых байтов разделяемых библиотек на эксплойт-маркеры: `/system/bin/sh`, `libsu.so`, `ptrace`, `execve`, `mprotect`, `kill`, `fork` ([plugin_guard.plugin:3264–3285](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/plugin_guard.plugin#L3264-L3285)).
- **Категоризация рисков**:
  Плагины, использующие модуль `ctypes` или библиотеки `.so`, автоматически получают статус риска «Нативный код (.so)», так как машинный код принципиально закрыт от статического анализа в песочнице Python ([plugin_guard.plugin:5104–5120, 6007–6015](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/plugin_guard.plugin#L5104-L5120)).

---

## Вызовы и наблюдаемые контракты

| Интерфейс / Метод | Контекст вызова | Назначение и параметры | Ссылка на код |
|---|---|---|---|
| `DexClassLoader(dex_path, opt_dir, lib_path, parent)` | Файловая загрузка DEX | Загрузка внешнего байткода из дискового файла в изолированный ClassLoader. | [`MandreTweaks.plugin:299`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L299) |
| `os.chmod(path, 0o444)` | Подготовка DEX | Установка атрибута read-only для предотвращения SecurityException на Android 14+. | [`MandreTweaks.plugin:164`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L164) |
| `unload().invoke(None)` | Выгрузка плагина | Рефлексивный вызов статического метода выгрузки Java-модуля и снятие хуков. | [`MandreTweaks.plugin:218`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L218) |
| `dynamic_proxy(Runnable)` | Инициализация моста | Реализация интерфейса Runnable на Python для колбэков жизненного цикла из DEX. | [`MandreTweaks.plugin:26`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/MandreTweaks.plugin#L26) |
| `InMemoryDexClassLoader(ByteBuffer.wrap(bytes), parent)` | In-Memory загрузка | Загрузка байткода DEX прямо из оперативной памяти без записи на диск (Android 8.0+). | [`account_hider.plugin:25`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/account_hider.plugin#L25) |
| `_read_payload()` | Извлечение блоба | Чтение собственного Python-скрипта и извлечение zlib-Base64 данных из комментариев. | [`AtmosFX.plugin:111`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/AtmosFX.plugin#L111) |
| `android_dlopen_ext(path, flags, byref(info))` | Загрузка `.so` | Обход изоляции Linker Namespace в Android через функцию libdl со структурой dlextinfo. | [`GreenPass.plugin:5969`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/GreenPass.plugin#L5969) |
| `ctypes.CDLL(path, handle=handle)` | Создание CDLL | Инстанцирование CDLL-обёртки с предварительно разрешённым системным дескриптором handle. | [`GreenPass.plugin:5971`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/GreenPass.plugin#L5971) |
| `libc.free(ptr)` | Очистка C-памяти | Освобождение динамически выделенной памяти C/Go строк во избежание нативных утечек. | [`GreenPass.plugin:6060`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/GreenPass.plugin#L6060) |
| `ctypes.PyDLL(path)` | Python C-Extension | Загрузка скомпилированных C-расширений Python (`_cffi_backend.so`) с удержанием GIL. | [`ReMandre.plugin:271`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ReMandre.plugin#L271) |
| `shutil.copyfile(orig, session_path)` | Сессионная изоляция | Клонирование `.so` с уникальным timestamp для полного сброса static C переменных. | [`extera_doom_native.plugin:45690`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/extera_doom_native.plugin#L45690) |
| `(c_char * cap).from_address(addr)` | Zero-Copy маппинг | Прямое связывание массива ctypes с адресом Java direct ByteBuffer. | [`nes_emulator.plugin:1209`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nes_emulator.plugin#L1209) |
| `ctypes.memmove(dst, src, count)` | Быстрое копирование | Низкоуровневая передача сырых PCM и видео-буферов между C и Java. | [`nes_emulator.plugin:1323`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nes_emulator.plugin#L1323) |
| `ctypes.CFUNCTYPE(...)` | Libretro трамплин | Создание Си-совместимого указателя на функцию обратного вызова из Python. | [`nes_emulator.plugin:661`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nes_emulator.plugin#L661) |
| `cd_kg_start(pw)` | Native Kill-Guard | Перехват libc-функций kill/tgkill/exit для блокировки намеренных аварий процесса. | [`culprit_detector.plugin:16802`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/culprit_detector.plugin#L16802) |
| `cd_gref_snapshot(arr, n)` | Диагностика JNI | Снятие снимка активных JNI global references для поиска утечек памяти в ART. | [`culprit_detector.plugin:17598`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/culprit_detector.plugin#L17598) |
| `sched_setaffinity(pid, size, mask)` | Управление CPU | Привязка ресурсоемких потоков к высокопроизводительным ядрам процессора. | [`mandre_lib.plugin:5980`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mandre_lib.plugin#L5980) |
| `PackageInstaller.createSession(params)` | Установка APK | Системный запуск инсталляции APK-компаньона, запакованного в пакет `.eaf`. | [`nowfylite.eaf:main.py:1225`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nowfylite.eaf) |
| `elyx.assets.read(name)` | Ресурсы Elyx | Абстрагированное чтение бинарных ассетов из распакованного каталога пакета `.eaf`. | [`google_photo_picker.eaf:main.py:3`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/google_photo_picker.eaf) |

---

## Практические приёмы и рецепты

### Рецепт 1: Безопасная загрузка DEX из памяти процесса (InMemoryDexClassLoader)
```python
import base64
import zlib
from dalvik.system import InMemoryDexClassLoader
from java.nio import ByteBuffer
from org.telegram.messenger import ApplicationLoader

class DexMemoryLoader:
    def __init__(self, compressed_b64: str, target_class: str):
        self.raw_data = compressed_b64
        self.target_class_name = target_class
        self.loader = None
        self.instance = None

    def load(self):
        dex_bytes = zlib.decompress(base64.b64decode(self.raw_data))
        buffer = ByteBuffer.wrap(dex_bytes)
        parent_cl = ApplicationLoader.applicationContext.getClassLoader()
        self.loader = InMemoryDexClassLoader(buffer, parent_cl)
        clazz = self.loader.loadClass(self.target_class_name)
        self.instance = clazz.newInstance()
        clazz.getMethod("start").invoke(self.instance)
        return self.instance

    def unload(self):
        if self.instance and hasattr(self.instance, "stop"):
            self.instance.getClass().getMethod("stop").invoke(self.instance)
        self.instance = None
        self.loader = None
```

### Рецепт 2: Файловая загрузка DEX с поддержкой ограничений Android 14+
```python
import os
from dalvik.system import DexClassLoader

def install_and_load_dex(context, dex_bytes: bytes, module_name: str, main_class: str):
    data_dir = context.getDir("dex_modules", 0).getAbsolutePath()
    opt_dir = context.getDir("dex_opt", 0).getAbsolutePath()
    dex_path = os.path.join(data_dir, f"{module_name}.dex")
    tmp_path = dex_path + ".tmp"

    with open(tmp_path, "wb") as f:
        f.write(dex_bytes)

    # Перед перезаписью на Android 14+ необходимо вернуть права на запись, если файл существовал
    if os.path.exists(dex_path):
        try: os.chmod(dex_path, 0o666)
        except Exception: pass
        try: os.remove(dex_path)
        except Exception: pass

    os.replace(tmp_path, dex_path)
    # КРИТИЧНО: ART требует 0o444 (read-only) для предотвращения SecurityException
    os.chmod(dex_path, 0o444)

    loader = DexClassLoader(dex_path, opt_dir, None, context.getClassLoader())
    return loader.loadClass(main_class)
```

### Рецепт 3: Загрузка нативной библиотеки .so в обход Android Linker Namespace
```python
import ctypes

class AndroidDlExtInfo(ctypes.Structure):
    _fields_ = [
        ("flags", ctypes.c_uint64),
        ("reserved_addr", ctypes.c_void_p),
        ("reserved_size", ctypes.c_size_t),
        ("relro_fd", ctypes.c_int),
        ("library_fd", ctypes.c_int),
        ("library_fd_offset", ctypes.c_uint64),
        ("library_namespace", ctypes.c_void_p),
    ]

def load_native_library(so_path: str):
    libdl = ctypes.CDLL("libdl.so")
    open_ext = libdl.android_dlopen_ext
    open_ext.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(AndroidDlExtInfo)]
    open_ext.restype = ctypes.c_void_p

    info = AndroidDlExtInfo()
    # RTLD_NOW (2) | RTLD_GLOBAL (0x100)
    handle = open_ext(so_path.encode("utf-8"), 2 | 0x100, ctypes.byref(info))
    if handle:
        return ctypes.CDLL(so_path, handle=handle)
    return ctypes.CDLL(so_path, mode=2 | 0x100)
```

### Рецепт 4: Изоляция статического C-состояния (сессионное клонирование)
```python
import os, time, shutil, ctypes

def create_isolated_session_library(base_so_path: str, cache_dir: str):
    session_id = int(time.time() * 1000)
    session_so = os.path.join(cache_dir, f"native_session_{session_id}.so")
    shutil.copyfile(base_so_path, session_so)
    # Загружаем свежую копию
    lib = ctypes.CDLL(session_so)
    return lib, session_so
```

### Рецепт 5: Упаковка многофайлового плагина Elyx (.eaf)
Для создания пакета `.eaf`:
1. Создать структуру каталогов:
   - `refmap.yml` — карта путей в корне.
   - `metainfo.yml` — манифест параметров.
   - `src/main.py` — точка входа.
   - `res/` — ассеты и иконки.
   - `locales/` — локализации строк.
2. Содержимое `refmap.yml`:
   ```yaml
   metainfo: metainfo.yml
   main: src/main.py
   assets: res
   strings: locales
   ```
3. Запаковать каталог в ZIP-архив и изменить расширение на `.eaf`.

---

## Ограничения и противоречия

1. **Несовместимость `InMemoryDexClassLoader` на старых версиях Android**:
   Вызов `InMemoryDexClassLoader` гарантированно приводит к аварии на Android 7.1 и ниже (API < 26). Плагины обязаны проверять `Build.VERSION.SDK_INT` и предусматривать фолбэк на дисковый `DexClassLoader`.
2. **Архитектурная привязка `.so` библиотек**:
   Подавляющее большинство плагинов с нативным кодом содержат бинарники исключительно под `arm64-v8a` (64-битные ARM устройства). При запуске на 32-битных ARM (`armeabi-v7a`) или эмуляторах x86/x86_64 загрузка завершается `OSError: dlopen failed`. Разработчикам необходимо либо поставлять fat-архивы со всеми ABI, либо детектировать `Build.SUPPORTED_ABIS` перед вызовом загрузчика.
3. **Утечки памяти при отсутствии явного `libc.free`**:
   Возврат строк из Go или C runtime через тип `ctypes.c_char_p` приводит к автоматическому копированию строки в память Python, но память в нативной куче остаётся неочищенной. Всегда используйте возврат через `ctypes.c_void_p` и ручной вызов `free()`.
4. **Ненадёжность выгрузки нативных библиотек через `dlclose`**:
   В Android Bionic функция `dlclose()` часто не выгружает разделяемую библиотеку физически из памяти, сохраняя значения статических переменных. Если плагин зависит от чистого начального состояния C-переменных, обязательно используйте сессионное клонирование файла `.so`.
5. **Предупреждения систем защиты и антивирусов**:
   Использование `ctypes`, динамической загрузки DEX или упаковки бинарников в Base64 автоматически переводит плагин в группу повышенного риска в сканерах каталогов KPM (`plugin_guard.plugin`), так как машинный код закрыт для статического анализа.
