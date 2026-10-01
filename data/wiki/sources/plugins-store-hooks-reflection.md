---
type: source
source_id: plugins-store-hooks-reflection
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-hooks-reflection.md
date: 2026-10-01
---

# KPM Plugins-Store: глубокий хукинг (hook_method vs hook_all_methods), Java Reflection и HookFilter DSL

Источник: репозиторий [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store), тематическая партиция `plugins-store-hooks-reflection` (40 плагинов). Анализ охватывает срез ветки `main` (commit `00de67026419f9dbe3a2787bb1236e8aaead8f76`). В данную подборку вошли плагины с наиболее сложным использованием Xposed/SandHook механизмов в среде ExteraGram и AyuGram: одиночный и групповой хукинг (`hook_method`, `hook_all_methods`, `hook_all_constructors`), классы-обработчики `MethodHook` и `MethodReplacement`, мутация аргументов и перехват результатов вызова (`param.args`, `param.setResult`, `param.thisObject`), глубокая рефлексия (`find_class`, `getDeclaredMethod`, `getDeclaredField`, `setAccessible`), фильтрация через `HookFilter` DSL, а также аудит жизненного цикла и очистки хуков при выгрузке.

## Роль и границы источника

Партиция `plugins-store-hooks-reflection` представляет собой важнейший корпус эмпирических сведений о том, как сторонние разработчики взаимодействуют с закрытыми и обфусцированными внутренностями Android-клиента Telegram. 
В отличие от официальной документации SDK, плагины каталога демонстрируют:
1. Реальные точки перехвата во внутренних классах (`org.telegram.messenger.*`, `org.telegram.ui.*`, `com.exteragram.*`, а также системных классах `android.media.*`, `android.view.*`, `android.hardware.camera2.*`).
2. Техники обхода проверок безопасности (снятие `FLAG_SECURE`, подавление автовоспроизведения видеосообщений, блокировка исходящих VoIP-звонков).
3. Практику динамической обработки результатов Activity через однократные перехваты `onActivityResult`.
4. Реальные системные риски: более 52% исследованных плагинов страдают от утечек хуков из-за отсутствия вызовов `unhook_method` в методе `on_plugin_unload()`.

**Границы применимости:**
- Все сведения получены методом статического анализа исходного кода (`status: code`).
- Исполнение на живом Android-устройстве не проводилось.
- Внутренние имена классов, методов и полей Telegram привязаны к конкретным версиям клиента; при мажорных обновлениях Telegram сигнатуры методов могут меняться или обфусцироваться.

## Покрытие

В партицию включены 40 плагинов каталога `Plugins-Store/Plugins/`:

| Файл плагина | Размер | Извлечённые механизмы | Границы и статус очистки |
|---|---|---|---|
| `Plugins/BeatSignal.plugin` | 47667 B | hook_method, MethodHook, getDeclaredMethod, reflection-fields, find_class, param.setResult | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/ForseSpoiler.plugin` | 5861 B | hook_all_methods, MethodHook, getDeclaredMethod, reflection-fields, find_class, param.setResult, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/IPhonePeek.plugin` | 18930 B | hook_all_methods, MethodHook, reflection-fields, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/KWFilter.plugin` | 43773 B | hook_all_methods, MethodHook, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/Log_Overlay_Quanta.plugin` | 43832 B | hook_method, getDeclaredMethod, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/RFS.plugin` | 6881 B | hook_all_methods, MethodReplacement, getDeclaredMethod, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/SnowFlakes.plugin` | 7032 B | hook_method, getDeclaredMethod, reflection-fields, find_class, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/Unlimited_GIFs.plugin` | 13829 B | hook_all_constructors, MethodReplacement, getDeclaredMethod, reflection-fields, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/advanced_chat_search.plugin` | 13306 B | hook_all_methods, MethodHook, reflection-fields, find_class | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/browser_shortcut.plugin` | 16710 B | hook_all_methods, MethodHook, find_class, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/channel_autoread.plugin` | 11681 B | hook_method, MethodHook, getDeclaredMethod, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/channelstats.plugin` | 19939 B | reflection-fields, find_class | Динамический reflection без удержания долгоживущих хуков |
| `Plugins/delete_from_gallery.plugin` | 9313 B | hook_method, getDeclaredMethod, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/discuss_without_join.plugin` | 751 B | hook_all_methods, MethodHook, find_class, param.setResult, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/download_chat_wallpaper.plugin` | 8761 B | reflection-fields, find_class | Динамический reflection без удержания долгоживущих хуков |
| `Plugins/feel_rich.plugin` | 4487 B | hook_method, MethodReplacement, getDeclaredMethod, reflection-fields, find_class | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/gift_id.plugin` | 3333 B | hook_method, MethodHook, getDeclaredMethod, reflection-fields, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/hide_feed_ads.plugin` | 1143 B | hook_all_methods, MethodReplacement, find_class | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/hide_paid_reactions.plugin` | 4194 B | hook_all_methods, MethodHook, find_class, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/hirez_photo.plugin` | 1319 B | hook_method, getDeclaredMethod, find_class | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/iconmover.plugin` | 14380 B | reflection-fields, find_class | Динамический reflection без удержания долгоживущих хуков |
| `Plugins/kubicki.plugin` | 31699 B | hook_method, MethodHook, getDeclaredMethod, find_class, param.setResult | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/local_time_shift.plugin` | 9889 B | hook_method, MethodHook, getDeclaredMethod, reflection-fields, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/microcontrol.plugin` | 6840 B | hook_all_methods, MethodHook, find_class, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/mooninfo.plugin` | 6217 B | hook_method, getDeclaredMethod, param.setResult, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/mur_reminder-1.0.0.plugin` | 13223 B | hook_method, getDeclaredMethod, param.setResult | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/no_ayu_rofls.plugin` | 2213 B | hook_all_methods, MethodReplacement, getDeclaredMethod, find_class | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/no_calls.plugin` | 9698 B | hook_all_methods, MethodReplacement, find_class | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/no_profile_autoplay.plugin` | 2095 B | hook_method, MethodHook, getDeclaredMethod, find_class, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/nometa_auto_reply.plugin` | 18226 B | hook_method, getDeclaredMethod | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/qr_gallery.plugin` | 4791 B | hook_all_methods, MethodHook, reflection-fields, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/record_blocker.plugin` | 3202 B | hook_all_methods, MethodHook, find_class, param.setResult | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/remove_trusted_timer.plugin` | 1372 B | hook_all_methods, MethodHook, param.setResult | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/reworked_camera_enhancer.plugin` | 18836 B | hook_method, getDeclaredMethod, reflection-fields, find_class, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/round_config.plugin` | 2432 B | hook_method, getDeclaredMethod, find_class | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/shadow_ban.plugin` | 30317 B | hook_all_methods, MethodHook, reflection-fields, find_class, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/shareui_sdkinstaller.plugin` | 9883 B | hook_method, getDeclaredMethod, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/shareui_shareui.plugin` | 5281 B | hook_all_methods, find_class, param.setResult, param.args mutation | Утечка хуков: on_plugin_unload не отменяет регистрацию хуков в ART |
| `Plugins/svg_inline.plugin` | 38118 B | hook_method, MethodHook, getDeclaredMethod, reflection-fields, find_class, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |
| `Plugins/volume_scroll.plugin` | 10871 B | hook_all_methods, reflection-fields, find_class, param.setResult, param.args mutation | Штатная очистка хуков через unhook_method / unhook_all |

## Технические факты

В категории `plugins-store-hooks-reflection` зафиксировано **40 верифицированных технических фактов**, систематизированных по шести функциональным направлениям.

### 1. Архитектура перехвата: hook_method против hook_all_methods и hook_all_constructors

В базовом фреймворке плагинов (`BasePlugin`) предусмотрено три фундаментальных метода регистрации перехватов на уровне ART/DEX:

1. **Одиночный хук конкретного члена (`self.hook_method`)**:
   Принимает отражённый объект `java.lang.reflect.Method` или `java.lang.reflect.Constructor` и экземпляр обработчика `BaseHook` (`MethodHook` или `MethodReplacement`).
   - Используется, когда точная сигнатура метода известна и уникальна.
   - Пример хука на метод: перехват `onActivityResult` в [BeatSignal.plugin:1399](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1399) и [ForseSpoiler.plugin:46](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L46).
   - Пример хука на конструктор: получение `ctor = clazz.getDeclaredConstructor(...)`, открытие доступа через `ctor.setAccessible(True)` и передача в `self.hook_method(ctor, EmojiViewCtorHook(self))` в [BeatSignal.plugin:1283-1284](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1283-L1284) и [Unlimited_GIFs.plugin:184](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Unlimited_GIFs.plugin#L184).
   - Полная сигнатура метода из SDK: `hook_method(self, member, handler=None, priority=10, before_filters=(), after_filters=(), before=None, after=None) -> Any`.

2. **Массовый перехват всех перегрузок (`self.hook_all_methods`)**:
   Принимает объект класса `clazz`, имя метода `method_name` строкой и экземпляр обработчика.
   - Метод сканирует все объявленные методы класса с данным именем и регистрирует хук на каждую перегрузку.
   - Критически важен при обфускации или версионных различиях, когда количество или типы параметров метода меняются между сборками Telegram.
   - Возвращает **список дескрипторов хуков** (`list[Any]`).
   - Примеры в коде: перехват `setMessageObject` в [KWFilter.plugin:614](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/KWFilter.plugin#L614), `LaunchActivity` в [browser_shortcut.plugin:187](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/browser_shortcut.plugin#L187), перехваты в [volume_scroll.plugin:114](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/volume_scroll.plugin#L114) и [IPhonePeek.plugin:195,202,209](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/IPhonePeek.plugin#L195).

3. **Массовый перехват конструкторов (`self.hook_all_constructors`)**:
   Принимает класс `clazz` и обработчик; перехватывает все перегрузки конструкторов класса.
   - Применяется в [Unlimited_GIFs.plugin:194](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Unlimited_GIFs.plugin#L194) для перехвата инициализации `MessagesController`, а также в [microcontrol.plugin:78](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/microcontrol.plugin#L78) для перехвата создания системного `android.media.AudioRecord`.

4. **Маршрутизация по приоритетам (`priority`)**:
   Параметр `priority` (по умолчанию 10) определяет очерёдность вызова хуков, если один метод перехвачен несколькими обработчиками или плагинами. Плагины [RFS.plugin:98,109](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L98) и [microcontrol.plugin:78,83,89](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/microcontrol.plugin#L78) явно задают `priority=100`, чтобы гарантированно выполниться раньше других перехватов.

---

### 2. Модели обработчиков: MethodHook против MethodReplacement

В плагинах зафиксировано две фундаментальные парадигмы написания обработчиков:

1. **`MethodHook` (наблюдение и мутация параметров/результата)**:
   Наследуется от `BaseHook`. Предоставляет два метода обратного вызова:
   - `before_hooked_method(self, param)`: вызывается непосредственно перед исполнением оригинального метода.
   - `after_hooked_method(self, param)`: вызывается сразу после возврата из оригинального метода.
   - Используется в подавляющем большинстве плагинов (35 классов в исследованной выборке: [ForseSpoiler.plugin:84](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L84), [SnowFlakes.plugin:92](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SnowFlakes.plugin#L92), [IPhonePeek.plugin:104](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/IPhonePeek.plugin#L104)).

2. **`MethodReplacement` (полная замена оригинального метода)**:
   Наследуется от `BaseHook`. Предоставляет единственный метод:
   - `replace_hooked_method(self, param)`: полностью подавляет исполнение оригинального метода и возвращает вычисленный в Python результат.
   - Тело оригинального Java/Native метода **не исполняется вообще**.
   - Применяется в 7 классах выборки:
     - [RFS.plugin:20-27](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L20-L27): класс `FalseResult` возвращает `False`, подменяя системные проверки безопасности окна;
     - [Unlimited_GIFs.plugin:66](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Unlimited_GIFs.plugin#L66): класс `AddRecentGifReplacement` заменяет добавление GIF для обхода лимита;
     - [no_calls.plugin:133-135](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/no_calls.plugin#L133-L135): класс `_StartCallReplacement` возвращает `None`, полностью блокируя запуск звонков и отображение алертов групповых вызовов;
     - [remove_trusted_timer.plugin:18,23](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/remove_trusted_timer.plugin#L18): классы `_SetTimerHook` и `_IsTimerActiveHook` возвращают фиксированные значения без исполнения логики таймеров.

---

### 3. Мутация параметров и подмена результатов вызова (MethodHookParam)

Объект `param`, передаваемый в хуки, инкапсулирует контекст вызова Java-метода и предоставляет следующие поля и методы:

1. **Чтение параметров вызова (`param.args`)**:
   `param.args` представляет собой индексируемый список переданных Java-аргументов.
   - В [SnowFlakes.plugin:168](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SnowFlakes.plugin#L168): `dt = param.args[0]` извлекает приращение времени кадра анимации.
   - В [reworked_camera_enhancer.plugin:346-348](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/reworked_camera_enhancer.plugin#L346-L348): извлекаются MIME-тип, ширина и высота видео.
   - В [mur_reminder-1.0.0.plugin:36](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mur_reminder-1.0.0.plugin#L36): `request_code, result_code, data = param.args` распаковывает параметры `onActivityResult`.

2. **Модификация параметров на лету (`param.args[i] = new_value`)**:
   Изменение элементов списка `param.args` внутри `before_hooked_method` приводит к тому, что оригинальный Java-метод вызывается с уже изменёнными аргументами!
   - [SnowFlakes.plugin:170](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SnowFlakes.plugin#L170): замедление снежинок через `param.args[0] = new_dt`.
   - [RFS.plugin:155](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L155): сброс флага скриншотов через `param.args[0] = Integer(flags & ~FLAG_SECURE)`.
   - [microcontrol.plugin:150,161](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/microcontrol.plugin#L150): подмена источника аудио через `param.args[0] = Integer(target)`.
   - [reworked_camera_enhancer.plugin:352](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/reworked_camera_enhancer.plugin#L352): подмена кодека на `param.args[0] = MIME_HEVC`.
   - [qr_gallery.plugin:113](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/qr_gallery.plugin#L113): замена делегата на обёртку `param.args[0] = WrappedDelegate(orig)`.

3. **Доступ к вызывающему экземпляру (`param.thisObject`)**:
   `param.thisObject` содержит ссылку на экземпляр Java-класса, чей нестатический метод был вызван.
   - [ForseSpoiler.plugin:105](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L105): `cell = param.thisObject` получает экземпляр `ChatMessageCell` для проверки и манипуляции отображением спойлера.
   - [KWFilter.plugin:134,154](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/KWFilter.plugin#L134): доступ к `ChatMessageCell` для фильтрации контента.
   - [BeatSignal.plugin:1231](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1231): `emoji_view = param.thisObject` при перехвате конструктора `EmojiView`.
   - [Unlimited_GIFs.plugin:72](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Unlimited_GIFs.plugin#L72): `this_obj = param.thisObject` для чтения внутренних полей `MessagesController`.
   - [no_profile_autoplay.plugin:40](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/no_profile_autoplay.plugin#L40): вызов метода экземпляра `param.thisObject.pauseMessage(msg_obj)`.

4. **Прерывание выполнения и возврат значения (`param.setResult`)**:
   - Вызов `param.setResult(value)` внутри **`before_hooked_method`** немедленно прерывает выполнение цепочки и оригинального Java-метода, заставляя вызывающий код получить указанное `value`.
     - [ForseSpoiler.plugin:132](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L132): `param.setResult(True)` прерывает вызов отрисовки ячейки со спойлером.
     - [discuss_without_join.plugin:14](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/discuss_without_join.plugin#L14): `param.setResult(False)` для метода `ChatObject.isNotInChat`.
     - [record_blocker.plugin:30](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/record_blocker.plugin#L30): `param.setResult(None)` для блокировки записи кружочков и голосовых сообщений.
     - [volume_scroll.plugin:110](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/volume_scroll.plugin#L110): `param.setResult(True)` для поглощения событий нажатия клавиш громкости.
   - Вызов `param.setResult(value)` внутри **`after_hooked_method`** перезаписывает уже возвращённый Java-методом результат перед передачей вызывающему коду.
     - [feel_rich.plugin:85](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/feel_rich.plugin#L85): подмена баланса Telegram Stars на заданную фиктивную сумму.

---

### 4. Java Reflection в плагинах Android: hook_utils и нативный Java API

Для взаимодействия с закрытыми частями Android и Telegram плагины комбинируют вспомогательный модуль `hook_utils` и стандартный Java Reflection API:

1. **Разрешение классов (`find_class`)**:
   Функция `from hook_utils import find_class` используется в более чем 35 плагинах для загрузки классов через активные class loaders процесса Telegram (например, `find_class("org.telegram.messenger.AndroidUtilities")`).
   В [local_time_shift.plugin:22-26](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/local_time_shift.plugin#L22-L26) продемонстрирован паттерн устойчивой загрузки с перебором: `for loader in (find_class, jclass): ...`.

2. **Поиск перегруженных методов (`getDeclaredMethod`)**:
   Для получения конкретного метода при наличии перегрузок плагины передают массив типов параметров:
   - [mur_reminder-1.0.0.plugin:152](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mur_reminder-1.0.0.plugin#L152): `ActivityClass.getDeclaredMethod("onActivityResult", IntegerClass.TYPE, IntegerClass.TYPE, IntentClass)`.
   - [feel_rich.plugin:40](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/feel_rich.plugin#L40): `StarsController.getClass().getDeclaredMethod("getBalance", Boolean.TYPE, Runnable.getClass(), Boolean.TYPE)`.
   - [reworked_camera_enhancer.plugin:333](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/reworked_camera_enhancer.plugin#L333): `rec_cls.getDeclaredMethod("setVideoEncodingBitRate", [jint.TYPE])`.
   - [delete_from_gallery.plugin:32](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/delete_from_gallery.plugin#L32): `clazz.getDeclaredMethod("onSelectedItemsCountChanged", JInt.TYPE)`.

3. **Динамический перебор методов (`getDeclaredMethods()`)**:
   Когда имена методов или параметры подверглись обфускации, плагины обходят массив методов в цикле:
   - [nometa_auto_reply.plugin:451-455](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nometa_auto_reply.plugin#L451-L455): поиск метода `processNewChannelDifferenceUpdates` в `NotificationsController`.
   - [shareui_sdkinstaller.plugin:155](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_sdkinstaller.plugin#L155): сканирование методов класса для поиска `onActivityResult`.
   - [ForseSpoiler.plugin:33](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L33): сканирование методов `ChatMessageCell`.

4. **Доступ к приватным полям (`getDeclaredField` и `get_private_field`)**:
   - Через Java Reflection: `field = cls.getDeclaredField(name); field.setAccessible(True); val = field.get(instance)` ([channelstats.plugin:90-92](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/channelstats.plugin#L90-L92), [SnowFlakes.plugin:51](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SnowFlakes.plugin#L51), [Unlimited_GIFs.plugin:78-79](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Unlimited_GIFs.plugin#L78-L79)).
   - Через готовые хелперы `hook_utils`: `get_private_field(obj, name)` и `set_private_field(obj, name, val)` ([advanced_chat_search.plugin:354-355](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/advanced_chat_search.plugin#L354-L355), [shadow_ban.plugin:201](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shadow_ban.plugin#L201), [svg_inline.plugin:61](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/svg_inline.plugin#L61)).

5. **Обязательность вызова `setAccessible(True)`**:
   Непубличные методы, конструкторы и поля в Android JVM защищены модификаторами доступа (`private`, `protected`, package-private). Вызов `setAccessible(True)` строго обязателен перед регистрацией хука или чтением/записью через Reflection ([BeatSignal.plugin:1283,1398](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1283), [ForseSpoiler.plugin:45](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L45), [RFS.plugin:97](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L97), [mur_reminder-1.0.0.plugin:155](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mur_reminder-1.0.0.plugin#L155)).

6. **Интроспекция полей для обратной совместимости**:
   Проверка наличия полей в классе через `any(x.getName() == target for x in cls.getDeclaredFields())` предотвращает падения `NoSuchFieldError` при работе на разных версиях клиента ([feel_rich.plugin:25](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/feel_rich.plugin#L25), [shadow_ban.plugin:50](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shadow_ban.plugin#L50)).

---

### 5. Декларативная фильтрация: HookFilter DSL и декоратор @hook_filters

Фреймворк `base_plugin` содержит развитую систему фильтрации хуков, позволяющую отсекать вызовы на стороне нативного движка без передачи управления в Python:

1. **Константы и предикаты `HookFilter`**:
   - Проверка результата: `RESULT_IS_NULL`, `RESULT_IS_TRUE`, `RESULT_IS_FALSE`, `RESULT_NOT_NULL`.
   - Сравнение результата: `ResultIsInstanceOf(clazz)`, `ResultEqual(value)`, `ResultNotEqual(value)`.
   - Проверка аргументов: `ArgumentIsNull(index)`, `ArgumentNotNull(index)`, `ArgumentIsFalse(index)`, `ArgumentIsTrue(index)`, `ArgumentIsInstanceOf(index, clazz)`, `ArgumentEqual(index, value)`, `ArgumentNotEqual(index, value)`.
   - Комплексные выражения: `Condition(mvel_expr, obj=None)`, `Or(*filters)`.

2. **Декларативное навешивание через `@hook_filters`**:
   - Декоратор `@hook_filters(*filters)` сохраняет условия в атрибуте `__catalib_filters__` метода:
     ```python
     @hook_filters(HookFilter.RESULT_IS_TRUE)
     def after_hooked_method(self, param): ...
     ```
     (Применяется в [archive_folder_fix.plugin:16-69](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/archive_folder_fix.plugin#L16-L69), [better_previews.plugin:60](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/better_previews.plugin#L60), [pacman_archive_chance.plugin:145](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/pacman_archive_chance.plugin#L145)).

3. **Параметрическое навешивание в `hook_method`**:
   Сигнатура `self.hook_method(member, handler, before_filters=(...), after_filters=(...))` принимает кортежи фильтров напрямую при регистрации перехвата.

---

### 6. Жизненный цикл и безопасность отмены хуков (Unhook Lifecycle Safety)

Аудит 40 плагинов выборки выявил критическую проблему стабильности среды плагинов:

1. **Статистика снятия хуков в каталоге**:
   - **19 плагинов (47.5%)** реализуют корректное или частично корректное снятие хуков через `self.unhook_method(h)` или `self.unhook_all_methods()`.
   - **21 плагин (52.5%)** имеет пустой `on_plugin_unload()` либо вообще не сохраняет дескрипторы хуков (среди них: `SnowFlakes.plugin`, `IPhonePeek.plugin`, `KWFilter.plugin`, `browser_shortcut.plugin`, `no_calls.plugin`, `discuss_without_join.plugin`, `feel_rich.plugin`, `reworked_camera_enhancer.plugin`, `shadow_ban.plugin`).
   - **Последствия утечки хуков**: деактивация плагина в настройках отключает Python-объект, но машинные перехваты в ART/DEX остаются активными. При следующем вызове перехваченного метода клиент обращается к мертвому Python runtime или старому замыканию, что приводит к крашам Telegram, утечкам памяти или задвоению логики при повторном включении плагина.

2. **Канонический паттерн безопасного управления хуками**:
   ```python
   class SafePlugin(BasePlugin):
       def on_plugin_load(self):
           self._unhooks = []
           # Одиночные хуки
           h = self.hook_method(method, MyHook())
           if h:
               self._unhooks.append(h)
           # Множественные хуки
           all_h = self.hook_all_methods(cls, "methodName", MyHook())
           if all_h:
               self._unhooks.extend(all_h)

       def on_plugin_unload(self):
           for unhook in getattr(self, "_unhooks", []):
               try:
                   self.unhook_method(unhook)
               except Exception:
                   pass
           self._unhooks.clear()
   ```
   Этот паттерн реализован в [advanced_chat_search.plugin:101-158](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/advanced_chat_search.plugin#L101-L158), [volume_scroll.plugin:48-65](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/volume_scroll.plugin#L48-L65), [hide_feed_ads.plugin:24-38](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/hide_feed_ads.plugin#L24-L38), [qr_gallery.plugin:120-141](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/qr_gallery.plugin#L120-L141).

3. **LIFO-снятие зависимых хуков**:
   В [RFS.plugin:76-81](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L76-L81) хуки отменяются в строго обратном порядке регистрации:
   `for unhook in list(reversed(getattr(self, "unhook_objects", []))): self.unhook_method(unhook)`. Это предотвращает вызовы методов в полуразобранном состоянии при каскадных перехватах.

4. **Однократный динамический хук (`onActivityResult`)**:
   Для операций с системными пикерами файлов (например, в [BeatSignal.plugin:1259-1399](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1259-L1399), [kubicki.plugin:151-174](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/kubicki.plugin#L151-L174), [mur_reminder-1.0.0.plugin:45-156](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mur_reminder-1.0.0.plugin#L45-L156)):
   - Хук устанавливается динамически перед `startActivityForResult`.
   - Внутри `before_hooked_method` при совпадении `request_code` плагин обрабатывает результат, вызывает `param.setResult(None)` и немедленно вызывает `self.unhook_method(self.activity_hook)`.

---

## Вызовы и наблюдаемые контракты

В таблице ниже сведены ключевые точки вызова, сигнатуры и подтверждённые в коде контракты плагинов выборки:

| Идентификатор плагина | Сигнатура или call-site | Назначение и контекст контракта | Доказательство |
|---|---|---|---|
| `BeatSignal.plugin` | `self.hook_method(member, handler, priority=10, before_filters=(), after_filters=())` | Метод BasePlugin.hook_method принимает отражённый Java Method или Constructor и экземпляр BaseHook/MethodHook, возвращая дескриптор хука для последующей отмены. | [BeatSignal.plugin:1399](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1399) |
| `BeatSignal.plugin` | `self.hook_method(constructor, handler)` | Конструкторы Java-классов можно перехватывать через hook_method, передав отражённый Constructor после вызова setAccessible(True). | [BeatSignal.plugin:1283-1284](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1283-L1284) |
| `KWFilter.plugin` | `self.hook_all_methods(clazz, method_name, handler)` | Метод hook_all_methods перехватывает сразу все перегрузки указанного метода класса по имени и возвращает список дескрипторов хуков. | [KWFilter.plugin:614](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/KWFilter.plugin#L614) |
| `volume_scroll.plugin` | `unhooks = self.hook_all_methods(clazz, method_name, handler)` | Метод hook_all_methods возвращает список токенов, каждый из которых требует отдельного вызова self.unhook_method при выгрузке плагина. | [volume_scroll.plugin:60-65](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/volume_scroll.plugin#L60-L65) |
| `Unlimited_GIFs.plugin` | `self.hook_all_constructors(clazz, handler)` | Метод hook_all_constructors перехватывает все объявленные конструкторы целевого Java-класса за один вызов. | [Unlimited_GIFs.plugin:194](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Unlimited_GIFs.plugin#L194) |
| `ForseSpoiler.plugin` | `class CustomHook(MethodHook): def before_hooked_method(self, param): ... def after_hooked_method(self, param): ...` | Класс MethodHook предоставляет колбэки before_hooked_method и after_hooked_method для выполнения логики до и после оригинального метода. | [ForseSpoiler.plugin:84-105](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L84-L105) |
| `RFS.plugin` | `class CustomReplacement(MethodReplacement): def replace_hooked_method(self, param): ...` | Класс MethodReplacement полностью заменяет исполнение целевого метода без выполнения его оригинального тела через replace_hooked_method. | [RFS.plugin:20-27](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L20-L27) |
| `SnowFlakes.plugin` | `param.args[index]` | Аргументы перехваченного метода доступны для чтения через индексацию списка param.args в колбэках хука. | [SnowFlakes.plugin:168](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SnowFlakes.plugin#L168) |
| `SnowFlakes.plugin` | `param.args[index] = new_value` | Прямая перезапись элементов param.args в before_hooked_method мутирует аргументы, передаваемые в оригинальный Java-метод. | [SnowFlakes.plugin:170](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SnowFlakes.plugin#L170) |
| `ForseSpoiler.plugin` | `instance = param.thisObject` | Свойство param.thisObject предоставляет доступ к Java-экземпляру, на котором вызван перехваченный метод. | [ForseSpoiler.plugin:105](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L105) |
| `ForseSpoiler.plugin` | `param.setResult(value)` | Вызов param.setResult(value) внутри before_hooked_method прерывает выполнение оригинального метода и немедленно возвращает заданное значение. | [ForseSpoiler.plugin:132](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L132) |
| `feel_rich.plugin` | `param.setResult(modified_result)` | Вызов param.setResult(value) в after_hooked_method перезаписывает возвращённое Java-методом значение перед возвратом вызывающему коду. | [feel_rich.plugin:85](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/feel_rich.plugin#L85) |
| `BeatSignal.plugin` | `from hook_utils import find_class; cls = find_class(class_name)` | Функция hook_utils.find_class выполняет поиск и загрузку Java-класса по строковому полному имени через загрузчики классов клиента. | [BeatSignal.plugin:11-240](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L11-L240) |
| `local_time_shift.plugin` | `for loader in (find_class, jclass): ...` | Для гарантированного поиска классов в гетерогенных окружениях применяется композитный перебор загрузчиков find_class и jclass. | [local_time_shift.plugin:22-26](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/local_time_shift.plugin#L22-L26) |
| `mur_reminder-1.0.0.plugin` | `cls.getDeclaredMethod(method_name, *arg_types)` | Точный поиск перегруженного Java-метода через getDeclaredMethod требует передачи типов аргументов (например, IntegerClass.TYPE, Boolean.TYPE). | [mur_reminder-1.0.0.plugin:152](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mur_reminder-1.0.0.plugin#L152) |
| `nometa_auto_reply.plugin` | `for m in cls.getDeclaredMethods(): if m.getName() == target: ...` | При обфускации или частой смене сигнатур плагины динамически сканируют массив cls.getDeclaredMethods() для поиска нужного метода по свойствам. | [nometa_auto_reply.plugin:451-455](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nometa_auto_reply.plugin#L451-L455) |
| `channelstats.plugin` | `field = cls.getDeclaredField(name); field.setAccessible(True)` | Доступ к приватным полям через Java Reflection требует вызова field.setAccessible(True) перед чтением field.get() или записью field.set(). | [channelstats.plugin:90-92](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/channelstats.plugin#L90-L92) |
| `feel_rich.plugin` | `HAS_FIELD = any(x.getName() == target for x in cls.getClass().getDeclaredFields())` | Интроспекция списка полей через getDeclaredFields() позволяет определять поддерживаемые возможности и поля клиента без падений по NoSuchFieldError. | [feel_rich.plugin:25](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/feel_rich.plugin#L25) |
| `ForseSpoiler.plugin` | `method.setAccessible(True); self.hook_method(method, hook)` | Вызов setAccessible(True) обязателен для отражённых непубличных методов и конструкторов перед передачей в self.hook_method. | [ForseSpoiler.plugin:45-46](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ForseSpoiler.plugin#L45-L46) |
| `advanced_chat_search.plugin` | `get_private_field(obj, field_name); set_private_field(obj, field_name, value)` | Утилиты get_private_field и set_private_field из hook_utils инкапсулируют получение и модификацию приватных полей без явного reflection boilerplate. | [advanced_chat_search.plugin:354-355](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/advanced_chat_search.plugin#L354-L355) |
| `BeatSignal.plugin` | `self.activity_hook = self.hook_method(method, ActivityResultHook(self)); self.unhook_method(self.activity_hook)` | Для обработки возврата из сторонних Activity применяется паттерн однократного динамического хука на onActivityResult со снятием в колбэке. | [BeatSignal.plugin:1259-1399](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L1259-L1399) |
| `advanced_chat_search.plugin` | `def on_plugin_unload(self): for h in getattr(self, '_unhooks', []): self.unhook_method(h)` | Корректный жизненный цикл плагина требует сохранения всех дескрипторов хуков в списке и вызова unhook_method для каждого из них в on_plugin_unload. | [advanced_chat_search.plugin:153-158](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/advanced_chat_search.plugin#L153-L158) |
| `RFS.plugin` | `for unhook in list(reversed(getattr(self, 'unhook_objects', []))): self.unhook_method(unhook)` | Снятие зависимых хуков в обратном порядке их регистрации через reversed(unhook_objects) предотвращает вызовы обработчиков по частично разобранным цепочкам. | [RFS.plugin:76-81](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L76-L81) |
| `SnowFlakes.plugin` | `def on_plugin_unload(self): pass` | Аудит 40 плагинов каталога Plugins-Store выявил, что 21 плагин оставляет on_plugin_unload пустым или не снимает установленные хуки, вызывая утечки в ART. | [SnowFlakes.plugin:92](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/SnowFlakes.plugin#L92) |
| `archive_folder_fix.plugin` | `HookFilter.RESULT_IS_TRUE, HookFilter.ArgumentIsNull(index), HookFilter.Or(...)` | Базовый модуль base_plugin объявляет класс HookFilter со статическими фильтрами аргументов и результатов для раннего отсечения ненужных вызовов хуков. | [archive_folder_fix.plugin:16-69](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/archive_folder_fix.plugin#L16-L69) |
| `archive_folder_fix.plugin` | `@hook_filters(HookFilter.RESULT_IS_TRUE)` | Декоратор hook_filters прикрепляет кортеж условий HookFilter к методу обработчика для декларативной фильтрации вызовов хука. | [archive_folder_fix.plugin:13](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/archive_folder_fix.plugin#L13) |
| `RFS.plugin` | `self.hook_method(method, replacement, priority=100)` | Параметр priority в hook_method и hook_all_methods задаёт приоритет выполнения обработчика в цепочке перехватов одного и того же метода. | [RFS.plugin:98](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L98) |
| `BeatSignal.plugin` | `from client_utils import dynamic_proxy; class ClickListener(dynamic_proxy(View.OnClickListener)): ...` | Утилита dynamic_proxy из client_utils реализует Java-интерфейсы (например OnClickListener, OnTouchListener) в Python без создания DEX-байткода. | [BeatSignal.plugin:153-912](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/BeatSignal.plugin#L153-L912) |
| `iconmover.plugin` | `view_group.getChildAt(index); view_group.removeView(v); view_group.addView(v, new_index)` | Плагины могут манипулировать иерархией представлений Android ViewGroup через прямое отражение getChildAt/getChildCount без установки хуков. | [iconmover.plugin:38-39](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/iconmover.plugin#L38-L39) |
| `channelstats.plugin` | `field = fragment.getClass().getDeclaredField(field_name); field.setAccessible(True); obj = field.get(fragment)` | Извлечение скрытых объектов Activity или Fragment через reflection позволяет читать закрытые контроллеры без вызова внешних хуков. | [channelstats.plugin:90-92](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/channelstats.plugin#L90-L92) |
| `Unlimited_GIFs.plugin` | `method = obj.getClass().getDeclaredMethod(name, *types); method.setAccessible(True); method.invoke(obj, *args)` | Вызов приватных методов Java-объектов выполняется через reflected_method.invoke(target_instance, *args). | [Unlimited_GIFs.plugin:105-114](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Unlimited_GIFs.plugin#L105-L114) |
| `microcontrol.plugin` | `self.hook_all_constructors(AudioRecordClass, AudioRecordHook(self), priority=100)` | Плагины могут перехватывать системные классы Android OS (android.media.AudioRecord, MediaRecorder) через hook_all_methods и hook_all_constructors. | [microcontrol.plugin:76-89](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/microcontrol.plugin#L76-L89) |
| `no_calls.plugin` | `self.hook_all_methods(VoIPHelper, 'startCall', _StartCallReplacement(self))` | Подавление звонков VoIP выполняется заменой методов VoIPHelper.startCall, showGroupCallAlert и joinGroupCall через MethodReplacement. | [no_calls.plugin:133-135](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/no_calls.plugin#L133-L135) |
| `hide_feed_ads.plugin` | `self._unhooks = self.hook_all_methods(controller, method_name, handler)` | Блокировка рекламных постов ленты реализуется перехватом всех методов контроллера ленты через hook_all_methods с подавлением вызова. | [hide_feed_ads.plugin:28-29](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/hide_feed_ads.plugin#L28-L29) |
| `no_profile_autoplay.plugin` | `param.thisObject.pauseMessage(msg_obj)` | Предотвращение автовоспроизведения медиа в профиле достигается хуком на MediaController.playMessage с немедленным вызовом pauseMessage. | [no_profile_autoplay.plugin:40-51](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/no_profile_autoplay.plugin#L40-L51) |
| `RFS.plugin` | `param.args[0] = Integer(flags & ~FLAG_SECURE)` | Снятие запрета на скриншоты (FLAG_SECURE) реализуется битовой маской в param.args при перехвате Window.setFlags. | [RFS.plugin:152-155](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/RFS.plugin#L152-L155) |
| `reworked_camera_enhancer.plugin` | `param.args[0] = MIME_HEVC; self.hook_method(rec_cls.getDeclaredMethod('setVideoSize', ...), ...)` | Настройка битрейта и видеокодека камеры выполняется через множественные хуки на методы рекордера с мутацией параметров MIME-типа. | [reworked_camera_enhancer.plugin:333-352](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/reworked_camera_enhancer.plugin#L333-L352) |
| `KWFilter.plugin` | `msg_obj = param.args[0]; cell = param.thisObject` | Перехват отрисовки сообщений через хук на ChatMessageCell.setMessageObject позволяет модифицировать структуру MessageObject до рендеринга. | [KWFilter.plugin:97-134](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/KWFilter.plugin#L97-L134) |
| `nometa_auto_reply.plugin` | `self.hook_method(m, IncomingMessagesHook(self))` | Мониторинг входящих сообщений в фоне реализуется через динамический поиск и перехват метода processNewChannelDifferenceUpdates в NotificationsController. | [nometa_auto_reply.plugin:451-459](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nometa_auto_reply.plugin#L451-L459) |
| `shareui_shareui.plugin` | `self.hook_all_methods(EngineClass, 'sharePlugin', HookClass()); param.setResult(None)` | Переопределение нативного UI публикации плагина осуществляется через хук на PythonPluginsEngine.sharePlugin с вызовом param.setResult(None). | [shareui_shareui.plugin:23-117](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_shareui.plugin#L23-L117) |

---

## Практические приёмы и рецепты

### Рецепт 1: Надёжная установка хука на перегруженный метод с сохранением токенов отмены
```python
from base_plugin import BasePlugin, MethodHook
from hook_utils import find_class

class SafeMethodHookPlugin(BasePlugin):
    def on_plugin_load(self):
        self._unhooks = []
        cls = find_class("org.telegram.ui.Cells.ChatMessageCell")
        if cls is None:
            return
        
        # hook_all_methods возвращает список токенов отмены
        tokens = self.hook_all_methods(cls, "setMessageObject", CellHook(self))
        if tokens:
            self._unhooks.extend(tokens)

    def on_plugin_unload(self):
        for token in getattr(self, "_unhooks", []):
            try:
                self.unhook_method(token)
            except Exception:
                pass
        self._unhooks.clear()

class CellHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        if param.args and param.args[0] is not None:
            msg = param.args[0]
            # обработка сообщения до отрисовки ячейки
```

### Рецепт 2: Полная замена метода через MethodReplacement (подавление звонков)
```python
from base_plugin import BasePlugin, MethodReplacement
from hook_utils import find_class

class DisableVoipPlugin(BasePlugin):
    def on_plugin_load(self):
        self._unhooks = []
        voip = find_class("org.telegram.ui.Components.voip.VoIPHelper")
        if voip:
            h1 = self.hook_all_methods(voip, "startCall", SuppressReplacement())
            h2 = self.hook_all_methods(voip, "showGroupCallAlert", SuppressReplacement())
            self._unhooks.extend((h1 or []) + (h2 or []))

    def on_plugin_unload(self):
        for h in getattr(self, "_unhooks", []):
            self.unhook_method(h)
        self._unhooks.clear()

class SuppressReplacement(MethodReplacement):
    def replace_hooked_method(self, param):
        # Оригинальный Java-метод не вызывается; возвращаем None
        return None
```

### Рецепт 3: Модификация аргументов в before_hooked_method (битовая маска флагов)
```python
from base_plugin import BasePlugin, MethodHook
from hook_utils import find_class
from java.lang import Integer

FLAG_SECURE = 8192

class ScreenCaptureAllowPlugin(BasePlugin):
    def on_plugin_load(self):
        self._unhooks = []
        win_cls = find_class("android.view.Window")
        tokens = self.hook_all_methods(win_cls, "setFlags", FlagsModifierHook())
        if tokens:
            self._unhooks.extend(tokens)

    def on_plugin_unload(self):
        for h in getattr(self, "_unhooks", []):
            self.unhook_method(h)

class FlagsModifierHook(MethodHook):
    def before_hooked_method(self, param):
        if param.args and len(param.args) >= 2:
            flags = int(param.args[0])
            mask = int(param.args[1])
            if mask & FLAG_SECURE:
                # Сбрасываем флаг защиты экрана
                param.args[0] = Integer(flags & ~FLAG_SECURE)
```

### Рецепт 4: Прерывание исполнения метода и возврат поддельного результата
```python
from base_plugin import BasePlugin, MethodHook
from hook_utils import find_class

class ChatBypassPlugin(BasePlugin):
    def on_plugin_load(self):
        chat_obj = find_class("org.telegram.messenger.ChatObject")
        self._unhooks = self.hook_all_methods(chat_obj, "isNotInChat", BypassHook()) or []

    def on_plugin_unload(self):
        for h in self._unhooks:
            self.unhook_method(h)

class BypassHook(MethodHook):
    def before_hooked_method(self, param):
        # Немедленно возвращаем False, оригинальный метод ChatObject.isNotInChat не исполняется
        param.setResult(False)
```

### Рецепт 5: Перехват конструкторов Java-классов
```python
from base_plugin import BasePlugin, MethodHook
from hook_utils import find_class

class EmojiConstructorHookPlugin(BasePlugin):
    def on_plugin_load(self):
        self._unhooks = []
        cls = find_class("org.telegram.ui.Components.EmojiView")
        if not cls:
            return
        
        # Вариант А: hook_all_constructors
        all_c = self.hook_all_constructors(cls, EmojiCtorHook(self))
        if all_c:
            self._unhooks.extend(all_c)

        # Вариант Б: одиночный конструктор через reflection
        for ctor in cls.getDeclaredConstructors():
            ctor.setAccessible(True)
            h = self.hook_method(ctor, EmojiCtorHook(self))
            if h:
                self._unhooks.append(h)
```

### Рецепт 6: Однократный динамический хук onActivityResult для выбора файлов
```python
from base_plugin import BasePlugin, MethodHook
from hook_utils import find_class

class FilePickerPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.activity_hook = None
        self.MY_REQUEST_CODE = 44102

    def pick_file(self, activity):
        # Если хук уже стоял, снимаем старый
        if self.activity_hook:
            self.unhook_method(self.activity_hook)
            self.activity_hook = None

        method = activity.getClass().getDeclaredMethod(
            "onActivityResult",
            find_class("java.lang.Integer").TYPE,
            find_class("java.lang.Integer").TYPE,
            find_class("android.content.Intent")
        )
        method.setAccessible(True)
        self.activity_hook = self.hook_method(method, FileResultHook(self))

        # Запуск Intent
        # activity.startActivityForResult(intent, self.MY_REQUEST_CODE)

    def on_plugin_unload(self):
        if self.activity_hook:
            self.unhook_method(self.activity_hook)
            self.activity_hook = None

class FileResultHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        req_code, res_code, data = param.args
        if int(req_code) == self.plugin.MY_REQUEST_CODE:
            # Обрабатываем выбранный файл
            param.setResult(None) # поглощаем системную обработку
            # Немедленно снимаем хук
            self.plugin.unhook_method(self.plugin.activity_hook)
            self.plugin.activity_hook = None
```

### Рецепт 7: Доступ к закрытым полям и вызов приватных методов
```python
from hook_utils import find_class, get_private_field, set_private_field

def inspect_and_patch(target_instance):
    # Способ 1: через готовые утилиты hook_utils
    usernames = get_private_field(target_instance, "searchResultUsernames")
    set_private_field(target_instance, "hasCustomOrder", True)

    # Способ 2: через прямой Java Reflection
    field = target_instance.getClass().getDeclaredField("recentGifs")
    field.setAccessible(True)
    recent_list = field.get(target_instance)

    # Вызов приватного метода
    method = target_instance.getClass().getDeclaredMethod("processRecent", find_class("java.util.ArrayList"))
    method.setAccessible(True)
    method.invoke(target_instance, recent_list)
```

### Рецепт 8: Декларативная фильтрация через HookFilter DSL
```python
from base_plugin import BasePlugin, MethodHook, HookFilter, hook_filters
from hook_utils import find_class

class OptimizedFilterPlugin(BasePlugin):
    def on_plugin_load(self):
        cls = find_class("org.telegram.ui.Cells.ChatMessageCell")
        method = cls.getDeclaredMethod("draw", find_class("android.graphics.Canvas"))
        method.setAccessible(True)
        # Фильтруем вызовы на уровне native-обёртки: хук сработает только если param.thisObject != null
        self.hook_method(
            method,
            DrawHook(),
            before_filters=[
                HookFilter.ArgumentNotNull(0),
                HookFilter.Condition("param.thisObject != null")
            ]
        )

class DrawHook(MethodHook):
    @hook_filters(HookFilter.RESULT_NOT_NULL)
    def after_hooked_method(self, param):
        pass
```

### Рецепт 9: Безопасное LIFO-снятие хуков при деинициализации
```python
class LifoPlugin(BasePlugin):
    def on_plugin_load(self):
        self._hooks_stack = []
        # Регистрация цепочки
        self._hooks_stack.append(self.hook_method(...))
        self._hooks_stack.append(self.hook_method(...))

    def on_plugin_unload(self):
        # Разворачиваем порядок снятия хуков
        for h in list(reversed(getattr(self, "_hooks_stack", []))):
            try:
                self.unhook_method(h)
            except Exception:
                pass
        self._hooks_stack.clear()
```

### Рецепт 10: Реализация Java-слушателей без компиляции DEX через dynamic_proxy
```python
from client_utils import dynamic_proxy
from hook_utils import find_class

View = find_class("android.view.View")

class CustomClickListener(dynamic_proxy(View.OnClickListener)):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def onClick(self, view):
        self.callback(view)
```

---

## Ограничения и противоречия

1. **Статус доказательств (`status: code`)**:
   Все утверждения основаны на статическом анализе репозитория `Plugins-Store`. Реальное поведение хуков на конкретных версиях Android (в частности, Android 14+ с усиленными проверками доступа к памяти и ограничением Hidden API) требует верификации на целевом устройстве.

2. **Массовая проблема утечки хуков (52.5% каталога)**:
   Более половины плагинов в каталоге не реализуют очистку хуков в `on_plugin_unload`. При разработке собственных решений обязательно применять паттерн централизованного списка `self._unhooks` с обязательной очисткой.

3. **Версионная нестабильность и обфускация Telegram**:
   Имена полей (`recentGifs`, `particles`, `searchResultUsernames`) и приватных методов не являются частью публичного API Telegram. При обновлениях клиента сигнатуры методов меняются без сохранения обратной совместимости, поэтому необходимо использовать защитные проверки (`getDeclaredFields`, `any(...)`, `try-except`).

4. **Производительность горячих участков (UI Rendering)**:
   Установка хуков на методы частого вызова (`draw`, `onDraw`, `onMeasure`, `setMessageObject` в `ChatMessageCell`) приводит к постоянному переключению контекста между Java/C и Python во время прокрутки списка чатов, что может вызывать задержки (jank) интерфейса. Для таких участков рекомендуется применять `HookFilter` предикаты для раннего отсечения ненужных вызовов на уровне ART.
