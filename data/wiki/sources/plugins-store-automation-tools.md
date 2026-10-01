---
type: source
source_id: plugins-store-automation-tools
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-automation-tools.md
date: 2026-10-01
---

# KPM Plugins-Store: автоматизация, системные инструменты, оверлеи и служебные утилиты

Источник: репозиторий [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store), подмножество `plugins-store-automation-tools` (22 плагина). Данный срез каталога охватывает прикладную автоматизацию Telegram, управление боковым меню (Drawer) и контекстными меню, пакетные действия над сообщениями и диалогами, перехват и отмену сетевых запросов MTProto, генерацию системных и внутриприложенных оверлеев, адаптацию к клиенту AyuGram, а также управление жизненным циклом плагинов через `PluginsController`.

## Роль и границы источника

В этом источнике зафиксированы фактические call-site контракты и приёмы, используемые авторами плагинов для клиентов ExteraGram и AyuGram на платформе Android. Анализ выполнен статически по исходным кодам 22 плагинов ветки `main`.

Код плагинов демонстрирует как штатные механизмы SDK (`BasePlugin`, `MenuItemData`, `HookStrategy`, `BulletinHelper`, `ui.settings`), так и глубокую интеграцию в среду Android и Telegram посредством рефлексии Java-классов (`find_class`, `getDeclaredMethod`), манипуляции системным сервисом `WindowManager`, внедрения представлений в `LaunchActivity.getWindow().getDecorView()`, а также низкоуровневых запросов MTProto (`TLRPC`).

Ни один из плагинов не тестировался в runtime-окружении физического устройства в рамках данной сессии; все факты имеют статус `code`.

## Покрытие

| Плагин / Файл снимка | Назначение и функционал | Что извлечено и границы анализа |
|---|---|---|
| [`FastCryptoBot_1.0.0r.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/FastCryptoBot_1.0.0r.plugin) | Навигация и быстрый переход в @CryptoBot | Регистрация и динамическое удаление `MenuItemType.DRAWER_MENU` и `CHAT_ACTION_MENU`, открытие URL через `Browser.openUrl`, вложенные фрагменты настроек (`create_sub_fragment`). |
| [`FastZovMail.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/FastZovMail.plugin) | Навигация и ссылки почтового сервиса | Приоритеты пунктов меню (`priority`), запуск ссылок через `Browser.openUrl` с fallback на `AndroidUtilities.getActivity()`. |
| [`Jelly.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Jelly.plugin) | Интерактивный антистресс-слайм на экране | Внедрение HUD в `LaunchActivity.getWindow().getDecorView()` без overlay-разрешений, покадровая анимация `Choreographer.postFrameCallback`, цепочка тактильной отдачи (`VibrationEffect`, `HapticFeedbackConstants`, `AndroidUtilities.vibrate`). |
| [`ReadAllButton.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ReadAllButton.plugin) | Кнопка «Прочитать всё» в боковом меню | Пакетный сброс непрочитанных через `get_messages_storage().readAllDialogs(-1)`, локализация через `LocaleController` и `java.util.Locale`. |
| [`activity_imitator_v2.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/activity_imitator_v2.plugin) | Имитация активности в чатах (тайпинг, аудио, видео) | Пакеты активности `TLRPC.TL_messages_setTyping` с 9 типами действий, корректный сброс статуса через `TL_sendMessageCancelAction()`, диалог выбора через `AlertDialogBuilder.set_items`. |
| [`aitools_beta.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/aitools_beta.plugin) | Всплывающий полноэкранный веб-плеер | Опрос готовности Activity через `get_last_fragment().getParentActivity()`, модальный диалог `android.app.Dialog` с полноэкранным `WebView`. |
| [`angry_rex.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/angry_rex.plugin) | Офлайн-игра T-Rex Runner | Встраивание `WebView` в диалог `AlertDialogBuilder.set_view` (учёт высоты в dp, а не px), предотвращение утечек памяти при закрытии `WebView` (`pauseTimers`, `loadUrl('about:blank')`, `destroy`). |
| [`auto_read.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_read.plugin) | Автоматическое чтение чатов, реакций и историй | Хуки `TL_update*`, разделение сетевого прочтения (`TL_channels_readHistory` vs `TL_messages_readHistory`) и локального сброса (`MessagesController.markDialogAsRead`), адаптация под Ghost-режим `AyuGhostController`. |
| [`chat_input_lines.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/chat_input_lines.plugin) | Настройка макс. строк поля ввода | Рефлексивный хук `EditTextCaption.setMaxLines(Integer.TYPE)`, модификация параметров в `before_hooked_method`. |
| [`confirm_unpin_all.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/confirm_unpin_all.plugin) | Подтверждение открепления сообщений | Перехват запросов `TL_messages_unpinAllMessages` / `TL_channels_unpinAllMessages`, отмена через `HookResult(strategy=HookStrategy.CANCEL)`, подтверждение и повторный `send_request`. |
| [`exereal_copy_any_code.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/exereal_copy_any_code.plugin) | Копирование блоков кода из сообщений | Регистрация в `MenuItemType.MESSAGE_CONTEXT_MENU`, парсинг `messageOwner.entities`, выборка `TL_messageEntityCode` и `TL_messageEntityPre` по смещениям. |
| [`forced_online.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/forced_online.plugin) | Поддержание постоянного онлайн-статуса | Периодическая фоновая отправка `TL_account.updateStatus(offline=False)` каждые 10 секунд. |
| [`lastname_time_edit.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/lastname_time_edit.plugin) | Время в фамилии профиля | Редактирование профиля `TL_account.updateProfile(flags=2, last_name=...)`, синхронизация с системным таймером минут, отправка в `GLOBAL_QUEUE`. |
| [`memory_monitor.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/memory_monitor.plugin) | Монитор потребления ОЗУ процесса | Сбор метрик через `java.lang.Runtime.getRuntime()`, перезапуск клиента через `quantahut.restart_app(fragment)`. |
| [`nowfy.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/nowfy.plugin) | Музыкальные карточки Now Playing | Шаблон модульного плагина с зависимостью `__requirements__ = "nowfy"` и наследованием от внешнего класса `_NowfyImpl`. |
| [`physics_cubes_companion.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/physics_cubes_companion.plugin) | Физические кубики поверх экрана | Системный оверлей через `WindowManager`, проверка разрешения `Settings.canDrawOverlays`, флаги `FLAG_LAYOUT_NO_LIMITS`, типы `TYPE_APPLICATION_OVERLAY`. |
| [`pingpong.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/pingpong.plugin) | Аркадный пинг-понг на экране | Получение и закрытие бокового меню `context['drawer_layout'].closeDrawer(False)`, оверлеи игровых ракеток, сохранение рекордов в настройках. |
| [`shareui_exterium.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_exterium.plugin) | Оптимизация фонового потребления ресурсов | Обработка событий `AppEvent.PAUSE` / `RESUME`, пакетное отключение/включение плагинов через `PluginsController.plugins`, всплывающее уведомление `BulletinHelper.show_with_button`. |
| [`smart_read_receipts.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/smart_read_receipts.plugin) | «Умное управление статусом прочтения» | Скрытая автоматическая отправка реакции `TL_messages_sendReaction` на жестко зашитый канал/пост при запуске плагина. |
| [`snake_game.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/snake_game.plugin) | Плавающее окно с игрой Змейка | Оверлей `WindowManager` с контейнером `LinearLayout`, содержащим `WebView` и нативную кнопку закрытия. |
| [`tgws.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/tgws.plugin) | MTProto WebSocket прокси-туннель | Обфусцированный модуль (XOR + zlib + base64), перехват соединений через `MethodHook`, внедрение плашек статуса через `PillRegistry.PillCreator` и делегата `NotificationCenter`. |
| [`wpm_test.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/wpm_test.plugin) | Тест скорости печати (WPM) | Построение сложного нативного UI в диалогах (`AlertDialogBuilder`, `ScrollView`, `LinearLayout`), фильтрация ввода `dynamic_proxy(InputFilter)`, перехват текста `dynamic_proxy(TextWatcher)`. |

## Технические факты

### 1. Меню, шторка и контекст вызовов

Клиентская инфраструктура ExteraGram предоставляет три основных типа меню:
1. `MenuItemType.DRAWER_MENU` — боковое меню приложения (шторка).
2. `MenuItemType.CHAT_ACTION_MENU` — меню действий в чате (три точки в правом верхнем углу ActionBar).
3. `MenuItemType.MESSAGE_CONTEXT_MENU` — контекстное меню отдельного сообщения.

Ключевые контракты и особенности:
* **Управление шторкой:** При клике на пункт типа `DRAWER_MENU` словарь `context`, передаваемый в колбэк `on_click`, содержит ключ `"drawer_layout"`. Это позволяет закрыть шторку программно:
  ```python
  drawer_layout = context.get("drawer_layout")
  if drawer_layout:
      drawer_layout.closeDrawer(False)
  ```
  Это предотвращает перекрытие открываемого плагином оверлея или диалога шторкой ([`pingpong.plugin:91-92`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/pingpong.plugin#L91-L92), [`snake_game.plugin:71-73`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/snake_game.plugin#L71-L73)).
* **Динамическое перестроение меню:** Для предотвращения появления дубликатов при переключении настроек плагины сначала вызывают `self.remove_menu_item(item_id)` для всех потенциальных ID, после чего заново добавляют активные элементы ([`FastCryptoBot_1.0.0r.plugin:105-115`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/FastCryptoBot_1.0.0r.plugin#L105-L115), [`FastZovMail.plugin:91-98`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/FastZovMail.plugin#L91-L98)).
* **Приоритет пунктов:** Поле `priority` в `MenuItemData` определяет порядок сортировки пунктов внутри меню (более высокие значения отображаются выше).
* **Контекстное меню сообщения (`MESSAGE_CONTEXT_MENU`):** В колбэк передаются `context.get("message")` и `context.get("fragment")`. Объект сообщения предоставляет `message.messageText` и Java-список `message.messageOwner.entities` ([`exereal_copy_any_code.plugin:23-32, 107-111`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/exereal_copy_any_code.plugin#L23-L32)).

### 2. Пакетные действия с диалогами и сообщениями

* **Сброс непрочитанных во всех чатах:** Для прочтения всех сообщений одним вызовом используется `client_utils.get_messages_storage().readAllDialogs(-1)` ([`ReadAllButton.plugin:51-53`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ReadAllButton.plugin#L51-L53)). Число `-1` указывает на сброс по всем папкам.
* **Разбор сущностей сообщения (MessageEntity):** Перебор Java-списка `message.messageOwner.entities` позволяет вычленять блоки кода без парсинга сырого текста регулярными выражениями:
  ```python
  for i in range(entities.size()):
      entity = entities.get(i)
      class_name = entity.getClass().getSimpleName()
      if "Code" in class_name or "Pre" in class_name:
          code_block = full_text[entity.offset : entity.offset + entity.length]
  ```
  Использование полей `offset` и `length` напрямую из Java-объекта `TLRPC.MessageEntity` гарантирует совпадение границ при наличии спецсимволов ([`exereal_copy_any_code.plugin:69-95`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/exereal_copy_any_code.plugin#L69-L95)).

### 3. Мониторинг обновлений и дуальное чтение (онлайн vs локально)

Плагин `auto_read.plugin` реализует продвинутую архитектуру перехвата входящих обновлений и разделения прочтения:
* **Подписка на обновления:** В `on_plugin_load()` вызывается `self.add_hook()` для списка типов:
  - `TL_updateNewMessage`, `TL_updateNewChannelMessage`
  - `TL_updateShortMessage`, `TL_updateShortChatMessage`
  - `TL_updateMessageReactions`
  - `TL_updates`, `TL_updatesCombined`
* **Обработчики хуков:**
  - `on_update_hook(self, update_name: str, account: int, update: Any) -> HookResult`
  - `on_updates_hook(self, container_name: str, account: int, updates: Any) -> HookResult`
* **Сетевое прочтение (Online Read):**
  - Для каналов (`dialog_id < 0`): строится `TLRPC.TL_channels_readHistory`, где `req.channel = mc.getInputChannel(-dialog_id)`, `req.max_id = max_id`.
  - Для групп и личных чатов: строится `TLRPC.TL_messages_readHistory`, где `req.peer = mc.getInputPeer(dialog_id)`, `req.max_id = max_id`.
  - Для реакций: строится `TLRPC.TL_messages_readReactions`, где `req.peer = mc.getInputPeer(dialog_id)`, `req.flags |= 1`, `req.top_msg_id = msg_id`.
  - Для историй: строится `TL_stories$TL_stories_readStories` ([`auto_read.plugin:308-390`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_read.plugin#L308-L390)).
* **Локальное прочтение (Local-only Read / Призрак):**
  Позволяет отметить чат прочитанным в локальной SQLite базе и на экране пользователя без отправки сетевых пакетов собеседнику:
  ```python
  mc = get_messages_controller()
  mc.markDialogAsRead(dialog_id, max_id, max_id, 0, False, 0, 0, True, 0)
  nc = NotificationCenter.getInstance(mc.currentAccount)
  nc.postNotificationName(NotificationCenter.dialogsUnreadCounterChanged)
  nc.postNotificationName(NotificationCenter.dialogsNeedReload)
  ```
  Это полностью обновляет UI приложения и счётчики на иконках папок без взаимодействия с серверами Telegram ([`auto_read.plugin:324-340`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_read.plugin#L324-L340)).

### 4. Адаптация под AyuGram Ghost Mode

Клиент AyuGram имеет встроенный контроллер скрытного режима (`AyuGhostController`). Плагины автоматизации могут динамически подстраиваться под его состояние:
```python
def _is_ghost_mode(account: int) -> bool:
    try:
        from com.radolyn.ayugram.controllers import AyuGhostController
        gc = AyuGhostController.getInstance(account)
        return bool(gc.isGhostModeActive()) if gc else False
    except Exception:
        return False
```
Если включен режим призрака, плагин автоматически переключается с сетевой отправки `TL_messages_readHistory` на локальный вызов `markDialogAsRead`, предотвращая деанонимизацию активности ([`auto_read.plugin:233-253, 280-290`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_read.plugin#L233-L253)).

### 5. Имитация пользовательской активности

Плагин `activity_imitator_v2.plugin` реализует паттерн поддержания активности в чате:
* Запрос `TLRPC.TL_messages_setTyping` принимает объект действия `req.action`.
* Доступные классы действий в `TLRPC`:
  - `TL_sendMessageTypingAction` — печатает текст.
  - `TL_sendMessageRecordAudioAction` / `TL_sendMessageUploadAudioAction` — записывает/отправляет голосовое.
  - `TL_sendMessageRecordVideoAction` / `TL_sendMessageUploadVideoAction` — записывает/отправляет видеосообщение.
  - `TL_sendMessageUploadPhotoAction` — отправляет фото.
  - `TL_sendMessageUploadDocumentAction` — отправляет файл.
  - `TL_sendMessageGeoLocationAction` — выбирает геопозицию.
  - `TL_sendMessageChooseContactAction` — выбирает контакт.
  - `TL_sendMessageGamePlayAction` — играет в игру.
* **Обязательность CancelAction:** Для прекращения показа статуса активности обязательно необходимо отправить пакет с объектом `TLRPC.TL_sendMessageCancelAction()`, иначе тайпинг будет отображаться собеседнику до истечения таймаута (~6 секунд) ([`activity_imitator_v2.plugin:268-275`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/activity_imitator_v2.plugin#L268-L275)).
* **Отзывчивый поток таймера:** Для быстрой остановки фоновый поток делит интервал ожидания (например, 4 секунды) на мелкие итерации по `time.sleep(0.1)` с непрерывной проверкой `stop_event.is_set()` ([`activity_imitator_v2.plugin:267-273`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/activity_imitator_v2.plugin#L267-L273)).

### 6. Перехват и прерывание исходящих запросов

Плагин `confirm_unpin_all.plugin` показывает механизм модального перехвата опасных операций:
1. В `on_plugin_load()` регистрируются целевые запросы: `self.add_hook("TL_messages_unpinAllMessages")`, `self.add_hook("TL_channels_unpinAllMessages")`.
2. В `pre_request_hook(self, request_name, account, request) -> HookResult`:
   - Если это не наш повторный запрос (`not self._skip_next`), сохраняем ссылку на объект `request`.
   - Запускаем отображение подтверждения: `run_on_ui_thread(self._show_confirm_dialog)`.
   - Возвращаем `HookResult(strategy=HookStrategy.CANCEL)` — это полностью блокирует отправку исходного запроса движком клиента!
3. В диалоге подтверждения при согласии выставляется `self._skip_next = True` и вызывается `send_request(request, callback)`, позволяя одобренному запросу уйти на сервер ([`confirm_unpin_all.plugin:36-52, 85-96`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/confirm_unpin_all.plugin#L36-L52)).

### 7. Архитектура оверлеев и работа с окнами

В анализируемых плагинах выявлены три принципиально разные стратегии отображения оверлеев:

#### А. In-App DecorView оверлей (без системных разрешений)
Использовано в `Jelly.plugin`. Оверлей добавляется прямо в дерево представлений текущего экрана:
```python
LA = find_class("org.telegram.ui.LaunchActivity")
act = getattr(LA, "instance", None) or LA.getLastActivity()
decor = act.getWindow().getDecorView()
decor.addView(root_view, FrameLayout.LayoutParams(-1, -1))
```
* **Преимущество:** Не требует разрешения `android.permission.SYSTEM_ALERT_WINDOW` («Отображение поверх других приложений»).
* **Ограничение:** Работает только пока приложение активно на переднем плане. При `on_plugin_unload()` обязательно: `decor.removeView(root_view)` ([`Jelly.plugin:464-486`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Jelly.plugin#L464-L486)).

#### Б. Системный оверлей через WindowManager
Использовано в `physics_cubes_companion.plugin`, `pingpong.plugin`, `snake_game.plugin`.
* Требует проверки разрешения: `Settings.canDrawOverlays(ctx)`. Если разрешения нет, пользователя перенаправляют в системные настройки:
  ```python
  intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:" + ctx.getPackageName()))
  activity.startActivity(intent)
  ```
* Параметры окна `WindowManager.LayoutParams`:
  - `p.type = LayoutParams.TYPE_APPLICATION_OVERLAY` (для Android 8.0+ / SDK >= 26) либо `TYPE_PHONE`.
  - `p.flags = FLAG_NOT_FOCUSABLE | FLAG_LAYOUT_NO_LIMITS` (позволяет рисовать за границами статус-бара и не перехватывать ввод клавиатуры).
  - `p.format = PixelFormat.TRANSLUCENT`.
* Безопасное удаление: перед вызовом `wm.removeView(v)` обязательно проверять `v.isAttachedToWindow()` ([`physics_cubes_companion.plugin:100-173, 216-221`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/physics_cubes_companion.plugin#L100-L173)).

#### В. Модальные окна с кастомными View (AlertDialogBuilder)
Использовано в `angry_rex.plugin`, `wpm_test.plugin`, `memory_monitor.plugin`.
* **Критический нюанс `set_view`:** Метод `AlertDialogBuilder.set_view(view, height)` принимает параметр `height` в **dp (density-independent pixels)**, а не в физических пикселях! Если передать `height` из метрик экрана без деления на `density`, окно на экранах с высоким DPI сожмётся или растянется некорректно ([`angry_rex.plugin:1053-1060`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/angry_rex.plugin#L1053-L1060)).

### 8. Жизненный цикл WebView и предотвращение утечек памяти

`angry_rex.plugin` демонстрирует полный эталонный контракт очистки `android.webkit.WebView`:
```python
def _destroy_specific_webview(webview):
    if webview is None: return
    try: webview.stopLoading()
    except Exception: pass
    try: webview.loadUrl("about:blank")
    except Exception: pass
    try: webview.onPause()
    except Exception: pass
    try: webview.pauseTimers()
    except Exception: pass
    try:
        parent = webview.getParent()
        if parent is not None:
            parent.removeView(webview)
    except Exception: pass
    try: webview.removeAllViews()
    except Exception: pass
    try: webview.destroy()
    except Exception: pass
```
Без вызова `pauseTimers()` внутренние потоки Chromium продолжают потреблять процессорное время, а без очистки родительского контейнера происходит утечка Activity контекста ([`angry_rex.plugin:1216-1248`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/angry_rex.plugin#L1216-L1248)).

### 9. Пакетное управление плагинами и AppEvent

Плагин `shareui_exterium.plugin` демонстрирует взаимодействие с внутренним реестром загрузчика:
* **События приложения:** Метод `on_app_event(self, event_type: AppEvent)` получает события жизненного цикла клиента:
  - `AppEvent.PAUSE` — приложение свернуто в фон.
  - `AppEvent.RESUME` — приложение развернуто пользователем.
* **Итерация и отключение плагинов:**
  ```python
  all_plugins = PluginsController.getInstance().plugins # Java Map<String, BasePlugin>
  keys = all_plugins.keySet().toArray()
  for i in range(len(keys)):
      plugin_id = keys[i]
      plugin_inst = all_plugins.get(plugin_id)
      if plugin_inst.isEnabled():
          plugin_inst.setEnabled(False)
  ```
* **Защита от сбоев (Crash Recovery):** Состояние отключенных плагинов сериализуется в persistent storage (`set_setting`), а флаг восстановления позволяет включить их обратно при следующем запуске, если процесс был убит системой в фоне ([`shareui_exterium.plugin:150-195`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_exterium.plugin#L150-L195)).
* **Bulletin с кнопкой:** `BulletinHelper.show_with_button(message, button_text, callback)` позволяет отображать интерактивные действия (например, копирование стектрейса ошибки) ([`shareui_exterium.plugin:232-236`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_exterium.plugin#L232-L236)).

### 10. Безопасность и сомнительные паттерны в каталоге

Анализ кода 22 плагинов выявил ряд паттернов, требующих осторожности:
1. **Скрытая накрутка реакций:** Плагин `smart_read_receipts.plugin` заявляет функцию «Умное управление статусом прочтения сообщений», однако в коде `on_plugin_load()` отправляет запрос `TL_messages_sendReaction` с эмодзи `❤️` на жестко зашитый канал (`DELAYED_READ_PEER = -1002349438816`, сообщение `1098`) ([`smart_read_receipts.plugin:22-60`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/smart_read_receipts.plugin#L22-L60)).
2. **Пранк-плагины:** `aitools_beta.plugin` заявляет интеграцию AI в чатах, но декодирует base64-ссылку на видеоролик и принудительно открывает его на весь экран ([`aitools_beta.plugin:27-78`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/aitools_beta.plugin#L27-L78)).
3. **Обфускация полезной нагрузки:** Плагин `tgws.plugin` поставляет весь рабочий код в виде зашифрованного блоба (симметричный XOR с составным ключом `_K1 + _K2`, сжатие `zlib`, кодирование `base64`) с динамическим исполнением через `exec(compile(...))` ([`tgws.plugin:13-33`](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/tgws.plugin#L13-L33)). Деобфускация показывает полнофункциональный MTProto WebSocket прокси-клиент с внедрением плашек статуса и хуков рендеринга текста.

## Вызовы и наблюдаемые контракты

| Класс / Модуль | Сигнатура или call-site | Назначение и контекст | Доказательство |
|---|---|---|---|
| `MessagesStorage` | `get_messages_storage().readAllDialogs(-1)` | Пакетный сброс счётчиков непрочитанных по всем диалогам | [ReadAllButton.plugin:51-53](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/ReadAllButton.plugin#L51-L53) |
| `Browser` | `Browser.openUrl(ctx, url)` | Бесшовное открытие ссылок и бот-аппов во встроенном браузере | [FastCryptoBot_1.0.0r.plugin:219](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/FastCryptoBot_1.0.0r.plugin#L219) |
| `LaunchActivity` | `act.getWindow().getDecorView().addView(root)` | Внедрение HUD-оверлея без системных разрешений на наложение | [Jelly.plugin:468-482](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Jelly.plugin#L468-L482) |
| `Choreographer` | `Choreographer.getInstance().postFrameCallback(cb)` | Синхронизация покадровой анимации с VSYNC дисплея | [Jelly.plugin:624-635](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Jelly.plugin#L624-L635) |
| `TLRPC` | `TLRPC.TL_messages_setTyping(peer, action)` | Отправка сетевого пакета активности (тайпинг, аудио, видео) | [activity_imitator_v2.plugin:301-304](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/activity_imitator_v2.plugin#L301-L304) |
| `TLRPC` | `req.action = TLRPC.TL_sendMessageCancelAction()` | Принудительный сброс индикации активности в чате | [activity_imitator_v2.plugin:270-275](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/activity_imitator_v2.plugin#L270-L275) |
| `AlertDialogBuilder` | `builder.set_view(view, height_in_dp)` | Встраивание кастомного View в модальное окно (высота строго в DP) | [angry_rex.plugin:1053-1060](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/angry_rex.plugin#L1053-L1060) |
| `WebView` | `wv.pauseTimers(); wv.destroy()` | Полное освобождение ресурсов Chromium при закрытии окна | [angry_rex.plugin:1232-1247](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/angry_rex.plugin#L1232-L1247) |
| `BasePlugin` | `def pre_request_hook(...) -> HookResult(strategy=CANCEL)` | Перехват и полная блокировка отправки исходящего MTProto запроса | [confirm_unpin_all.plugin:51](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/confirm_unpin_all.plugin#L51) |
| `MessagesController` | `mc.markDialogAsRead(dialog_id, max_id, ...)` | Локальное прочтение чата без отправки сетевых пакетов | [auto_read.plugin:329](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_read.plugin#L329) |
| `NotificationCenter` | `nc.postNotificationName(NotificationCenter.dialogsNeedReload)` | Принудительная перерисовка списка диалогов в интерфейсе | [auto_read.plugin:334-336](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_read.plugin#L334-L336) |
| `AyuGhostController` | `AyuGhostController.getInstance(account).isGhostModeActive()` | Проверка активности режима призрака в клиенте AyuGram | [auto_read.plugin:237-251](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_read.plugin#L237-L251) |
| `EditTextCaption` | `hook_method(setMaxLines_method, hook)` | Перехват и переопределение лимита строк в поле ввода чата | [chat_input_lines.plugin:58-60](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/chat_input_lines.plugin#L58-L60) |
| `WindowManager` | `wm.addView(view, params)` | Размещение системного плавающего окна поверх всех приложений | [physics_cubes_companion.plugin:212](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/physics_cubes_companion.plugin#L212) |
| `Settings` | `Settings.canDrawOverlays(context)` | Проверка наличия разрешения на отображение оверлеев | [physics_cubes_companion.plugin:100](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/physics_cubes_companion.plugin#L100) |
| `BasePlugin` | `def on_app_event(self, event_type: AppEvent)` | Перехват событий перехода приложения в фон / возвращения на экран | [shareui_exterium.plugin:83-89](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_exterium.plugin#L83-L89) |
| `PluginsController` | `PluginsController.getInstance().plugins` | Получение Java Map всех установленных плагинов для batch-контроля | [shareui_exterium.plugin:173](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_exterium.plugin#L173) |
| `BulletinHelper` | `BulletinHelper.show_with_button(msg, btn_text, fn)` | Показ всплывающего уведомления с интерактивной кнопкой действия | [shareui_exterium.plugin:232-236](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_exterium.plugin#L232-L236) |
| `TL_account` | `TL_account.updateStatus(offline=False)` | Периодическое поддержание постоянного онлайн-статуса | [forced_online.plugin:58-60](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/forced_online.plugin#L58-L60) |
| `TL_account` | `TL_account.updateProfile(flags=2, last_name=...)` | Программное обновление фамилии в профиле пользователя | [lastname_time_edit.plugin:145-148](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/lastname_time_edit.plugin#L145-L148) |
| `Runtime` | `Runtime.getRuntime().totalMemory()` | Извлечение объёма выделенной кучи JVM процесса клиента | [memory_monitor.plugin:33-37](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/memory_monitor.plugin#L33-L37) |

## Практические приёмы и рецепты

1. **Рецепт: Закрытие шторки при клике на пункт DRAWER_MENU.**
   Чтобы UI плагина не оказывался под полупрозрачной шторкой меню:
   ```python
   def on_drawer_click(self, context: dict):
       drawer = context.get("drawer_layout")
       if drawer:
           drawer.closeDrawer(False)
       run_on_ui_thread(self.open_plugin_feature)
   ```

2. **Рецепт: Безопасный модальный перехват опасного сетевого запроса.**
   ```python
   def pre_request_hook(self, request_name: str, account: int, request: Any) -> HookResult:
       if request_name == "TL_messages_unpinAllMessages":
           if self._allow_once:
               self._allow_once = False
               return HookResult()
           self._saved_request = request
           run_on_ui_thread(self._ask_user_confirmation)
           return HookResult(strategy=HookStrategy.CANCEL)
   ```

3. **Рецепт: Имитация активности с гарантированным сбросом.**
   При завершении отправки статуса обязательно шлите `TL_sendMessageCancelAction`, чтобы собеседник не видел бесконечный «печатает...»:
   ```python
   def stop_typing(self, dialog_id: int):
       peer = get_messages_controller().getInputPeer(dialog_id)
       req = TLRPC.TL_messages_setTyping()
       req.peer = peer
       req.action = TLRPC.TL_sendMessageCancelAction()
       send_request(req, None)
   ```

4. **Рецепт: Корректное внедрение кастомного View в AlertDialogBuilder.**
   ```python
   # AlertDialogBuilder принимает высоту строго в dp:
   density = activity.getResources().getDisplayMetrics().density
   height_dp = int(pixel_height / density)
   builder = AlertDialogBuilder(activity)
   builder.set_view(container_view, height_dp)
   ```

5. **Рецепт: Устранение утечек памяти в WebView.**
   Всегда вешайте слушатель на `builder.set_on_dismiss_listener(cleanup_fn)` и вызывайте `webview.pauseTimers()`, `loadUrl("about:blank")` и `destroy()`.

6. **Рецепт: Пакетное прочтение чата локально без деанонимизации.**
   ```python
   mc = get_messages_controller()
   mc.markDialogAsRead(dialog_id, max_id, max_id, 0, False, 0, 0, True, 0)
   nc = NotificationCenter.getInstance(mc.currentAccount)
   nc.postNotificationName(NotificationCenter.dialogsUnreadCounterChanged)
   nc.postNotificationName(NotificationCenter.dialogsNeedReload)
   ```

## Ограничения и противоречия

- **Статус фактов:** Все данные основаны на статическом анализе репозитория (`code`), без проверки на реальных сборках Android.
- **Риски совместимости Java Reflection:** Классы интерфейса (`EditTextCaption`, `LaunchActivity`, `Browser`) могут менять сигнатуры методов, имена внутренних полей и иерархию наследования между релизами Telegram и форков ExteraGram.
- **Системные разрешения:** Для плагинов, использующих `WindowManager` (`physics_cubes_companion`, `pingpong`, `snake_game`), обязательно наличие разрешения на наложение поверх окон (`SYSTEM_ALERT_WINDOW`), которое пользователь должен выдать вручную в системных настройках Android.
- **Неявная телеметрия и вредоносный код:** Каталог содержит плагины с сомнительным или замаскированным функционалом (`smart_read_receipts` с накруткой реакций на канал, обфусцированный `tgws.plugin`). Любой импорт сторонних плагинов из публичных репозиториев требует предварительного аудита кода.
