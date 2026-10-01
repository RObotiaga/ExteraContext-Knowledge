---
type: source
source_id: plugins-store-ui-customization
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-ui-customization.md
date: 2026-10-01
---

# KPM Plugins-Store: UI, темы, кастомизация интерфейса и графические эффекты

Источник: подмножество `plugins-store-ui-customization` (84 плагина) из каталога [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store) на ветке `main`. Срез включает в себя плагины, ориентированные на глубокую кастомизацию пользовательского интерфейса Telegram/ExteraGram: кастомные плашки PillStack, отключение и настройку размытия (blur), режим Edge-to-Edge, системные оверлеи через Android `WindowManager`, перехват жестов и анимаций, модификацию бокового меню (drawer), инжекцию кастомных ячеек в профили и чаты, управление сессиями, а также встроенные интерактивные мини-игры на View и Canvas.

## Роль и границы источника

Этот источник аккумулирует практические приёмы расширения интерфейса Android-клиента Telegram (ExteraGram, AyuGram), реализованные сторонними разработчиками на Python через мост Chaquopy. В отличие от абстрактной документации SDK, данный срез демонстрирует реальные call-site вызовы Telegram UI классов (`ActionBar`, `BottomSheet`, `AlertDialog`, `Bulletin`, `Theme`, `ItemOptions`, `ChatMessageCell`, `DialogCell`), внутренних компонентов ExteraGram (`PillRegistry`, `MainTabsUiHelper`, `PluginsActivity`, `UniversalAdapter`), а также низкоуровневых механизмов Android Framework (`WindowManager.addView`, `Choreographer.FrameCallback`, `ValueAnimator`, `Canvas`, `Paint`).

**Границы применимости:**
1. Код исследован методом статического анализа файлов каталога. Вызовы не валидировались на живых устройствах всех версий Android, поэтому статус свидетельств — `code`.
2. Многие плагины обращаются к приватным и недокументированным полям Telegram через reflection (`find_class`, `getDeclaredMethod`, `getDeclaredField`), что делает их чувствительными к изменениям структуры классов между релизами Telegram.
3. Некоторые плагины содержат неполную реализацию `on_plugin_unload()` (например, не удаляют добавленные оверлейные View или не снимают хуки), что фиксируется в разделе «Ограничения и противоречия».

## Покрытие

| Путь плагина / категория | Что извлечено и проанализировано | Границы и специфические особенности |
|---|---|---|
| `Plugins/ram_info_pill.plugin` | Архитектура PillStack в ExteraGram, класс `PillRegistry`, `PillCreator` через `dynamic_proxy`, меню `ItemOptions.makeOptions` | Требует ExteraGram `>= 12.5.1` со встроенным модулем `pillstack.core` |
| `Plugins/NoMoreBlur.plugin`, `squares.plugin`, `liquid_glass_blur.plugin` | Глобальное отключение размытия через `SharedConfig` и подавление отрисовки `BlurredBackgroundDrawable.draw`, регулировка радиусов скругления блюра | Модифицирует низкоуровневый `org.telegram.ui.Components.blur3` |
| `Plugins/forceedge2edge.plugin`, `hide_system_bars.plugin`, `md3_navbars_everywhere.plugin` | Принудительный Edge-to-Edge через замену `BaseFragment.isSupportEdgeToEdge`, скрытие StatusBar/NavBar флагами окна, адаптация цвета NavBar под MD3 | Зависит от версии Android SDK (`Build.VERSION.SDK_INT`) и оконных insets |
| `Plugins/floating_rounds.plugin`, `sticky_notes_overlay.plugin`, `log_overlay.plugin` | Системные плавающие оверлеи через `WindowManager.addView` с типом `TYPE_APPLICATION_OVERLAY`, перетаскивание (drag-and-drop), безопасное удаление в unload | Требует системного разрешения `Settings.canDrawOverlays` |
| `Plugins/usernotes.plugin`, `scam_base_writer.plugin` | Тройной скоординированный хук профиля: `ProfileActivity.updateRowsIds`, `ListAdapter.getItemViewType`, `ListAdapter.onBindViewHolder` для инжекции кастомных рядов | Жесткая привязка к именам методов и типам строк в `ProfileActivity` |
| `Plugins/ReadAllButton.plugin`, `read_all.plugin`, `plugin_drawer.plugin` | Добавление элементов в боковой ящик (`MenuItemType.DRAWER_MENU`), массовая пометка прочитанными через `MessagesStorage.readAllDialogs(-1)` | Вызовы хранилища сообщений выполняются синхронно или в фоне |
| `Plugins/auto_marquee.plugin`, `titleChanger.plugin`, `hide_members_count-1.4.0.plugin` | Бегущая строка в заголовках через `ActionBar.setTitle` и флаг `MARQUEE`, скрытие счетчиков подписчиков в `ChatActivity.updateSubtitle` | Работает через манипуляцию свойствами внутреннего `TextView` / `SimpleTextView` |
| `Plugins/ArticleViewerFix.plugin`, `ripple_touch.plugin`, `animtou.plugin`, `roundseekbarpausefix.plugin` | Перехват тач-событий в `ArticleViewer$WindowView.handleTouchEvent`, отрисовка глобального Ripple на Canvas через `Activity.dispatchTouchEvent` | Хук тач-диспетчера вызывается при каждом касании экрана (hot path) |
| `Plugins/theme_tweaker.plugin`, `pincolor_plugin.plugin`, `NoColorButton.plugin`, `fake_stars.plugin` | Динамическая смена цветов темы через `Theme.setThemeColor`, перекраска значка закрепа в `DialogCell.onDraw`, фильтрация стилей кнопок ботов | Позволяет изменять палитру интерфейса в реальном времени без рестарта |
| `Plugins/fucklottie.plugin` | Замена ресурсоемких Lottie-анимаций на статические Vector Drawable в `MainTabsUiHelper` и `ChatAttachAlert` | Существенно снижает нагрузку на CPU при переключении нижних вкладок |
| `Plugins/spoiler_remover.plugin`, `hide_recent_reactions.plugin`, `hide_bot_open_button.plugin` | Отключение блюра спойлеров в `ChatMessageCell`, подавление панели быстрых реакций, скрытие кнопки запуска WebApp в ячейках диалогов | Модификация ячеек списка сообщений и диалогов |
| `Plugins/sessions_manager.plugin`, `rename_sessions.plugin`, `session_duplicator.plugin` | Локальные псевдонимы устройств в `SessionCell.setSession`, добавление кнопок управления в `SessionsActivity.createView` | Интеграция с сессиями и устройствами Telegram |
| `Plugins/sorter_plus.plugin`, `plugins_settings.plugin` | Модификация `PluginsActivity` через `UniversalAdapter.fillItems`, перехват внутренней навигации в `ActionBarLayout.presentFragment`, настройка `Bulletin.show` | Кастомизация встроенного менеджера плагинов и уведомлений |
| `Plugins/Chess_Game.plugin`, `Sudoku.plugin`, `dinorunner.plugin` | Встраивание HTML5 веб-игр через `WebView` в `BottomSheet`, нативные игры на `GridLayout` и аркадный Game Loop через `Choreographer.FrameCallback` | Полноценные интерактивные приложения внутри диалоговых окон Telegram |
| `Plugins/All_Telegram_Icons.plugin`, `DevSettingsIcons.plugin`, `ExComponents.plugin` | Галерея компонентов, просмотрщик встроенных иконок и анимаций через `BottomSheet.Builder` и `GridLayout` | Инструменты разработчика для инспекции Telegram ресурсов |
| 69 остальных плагинов выборки | Аудит вызовов `AlertDialog.Builder`, `BulletinHelper`, меню, настроек и утилит форматирования | Включает различные мелкие твики интерфейса и юзабилити |

## Технические факты

### 1. Архитектура PillStack и интеграция в заголовки (`ram_info_pill.plugin`)
В ExteraGram начиная с версии 12.5.1 реализована нативная система плашек в заголовках — PillStack (`com.exteragram.messenger.pillstack.core`).
- Регистрация плашки выполняется через `PillRegistry.registerPill(PillInfo, PillCreator)` ([ram_info_pill.plugin:25-38](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ram_info_pill.plugin#L25-L38)).
- Класс `PillCreator` реализуется через `dynamic_proxy(self.PillCreator)` и обязан предоставлять фабричный метод создания `View`, настройки шрифтов и интервала автообновления.
- Для контекстных меню на плашках используется нативный `org.telegram.ui.Components.ItemOptions.makeOptions(fragment, pill)` ([ram_info_pill.plugin:123-134](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ram_info_pill.plugin#L123-L134)).

### 2. Модификация и отключение размытия (Blur & Glass)
Размытие фона в Telegram опирается на класс `org.telegram.ui.Components.blur3.drawable.BlurredBackgroundDrawable` и флаги в `SharedConfig`.
- **Полное устранение блюра:** плагин `NoMoreBlur.plugin` перехватывает геттеры `SharedConfig` (`deviceBlurEnabled`, `chatBlurEnabled`, `isBlurEnabled`), возвращая `False`, а также устанавливает хук на `BlurredBackgroundDrawable.draw` с пустым телом `KillDraw` ([NoMoreBlur.plugin:16-35](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/NoMoreBlur.plugin#L16-L35)). Это гарантирует отсутствие просадок FPS на GPU Mali/Adreno начального уровня.
- **Изменение геометрии блюра:** плагин `squares.plugin` перехватывает методы установки радиусов `BlurredBackgroundDrawable` и уменьшает их вдвое, превращая скругленные стеклянные поверхности в строгие прямоугольные блоки ([squares.plugin:15-58](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/squares.plugin#L15-L58)).
- **Жидкое стекло (Liquid Glass):** `liquid_glass_blur.plugin` программно перенастраивает параметры шейдеров блюра, меняя коэффициенты размытия и насыщенности.

### 3. Edge-to-Edge режим и системные панели
- **Сквозной Edge-to-Edge:** `forceedge2edge.plugin` перехватывает метод `BaseFragment.isSupportEdgeToEdge()` с помощью `MethodReplacement(True)` ([forceedge2edge.plugin:10-17](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/forceedge2edge.plugin#L10-L17)). Это принуждает все экраны отрисовываться под строкой состояния и навигационной полосой.
- **Полноэкранный режим без системных полос:** `hide_system_bars.plugin` прикрепляет слушатель к окну `Activity` и выставляет системные флаги `SYSTEM_UI_FLAG_FULLSCREEN | SYSTEM_UI_FLAG_HIDE_NAVIGATION | SYSTEM_UI_FLAG_IMMERSIVE_STICKY` ([hide_system_bars.plugin:45-75](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hide_system_bars.plugin#L45-L75)).
- **Стилизация навигационной панели под Material You:** `md3_navbars_everywhere.plugin` синхронизирует цвет системной панели навигации с цветом темы `Theme.getColor(Theme.key_windowBackgroundWhite)` через `Window.setNavigationBarColor()` и выставляет флаг `SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR` ([md3_navbars_everywhere.plugin:52-95](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/md3_navbars_everywhere.plugin#L52-L95)).

### 4. Плавающие оверлеи поверх экрана через WindowManager
Несколько плагинов реализуют независимые плавающие окна поверх всех приложений:
- **Тип оверлея и параметры:** используется `WindowManager.LayoutParams` с флагом `TYPE_APPLICATION_OVERLAY` (для Android 8.0+) и обратной совместимостью с `TYPE_SYSTEM_ALERT` для старых версий ([floating_rounds.plugin:635-645](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/floating_rounds.plugin#L635-L645), [sticky_notes_overlay.plugin:470](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sticky_notes_overlay.plugin#L470)). Обязательны флаги `FLAG_NOT_FOCUSABLE` и `PixelFormat.TRANSLUCENT`.
- **Интерактивный Drag-and-Drop:** перемещение окна рассчитывается через кастомный `OnTouchListener`. При событии `ACTION_DOWN` сохраняются начальные координаты, в `ACTION_MOVE` вычисляется смещение относительно сырых экранных координат (`event.getRawX()`, `event.getRawY()`), после чего позиция обновляется через `WindowManager.updateViewLayout(view, params)` ([sticky_notes_overlay.plugin:830-840](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sticky_notes_overlay.plugin#L830-L840)).
- **Обязательная очистка в lifecycle:** все оверлеи должны вызывать `WindowManager.removeView(view)` внутри `on_plugin_unload()` плагина, обернув вызов в `run_on_ui_thread()`, иначе возникает фатальная утечка окон Android `WindowLeaked` ([sticky_notes_overlay.plugin:240-245](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sticky_notes_overlay.plugin#L240-L245)).
- **Плавающий логгер и круглые видео:** `log_overlay.plugin` выводит плавающую панель с живым стримингом логов и фильтрами уровней, а `floating_rounds.plugin` переносит воспроизведение круглых видеосообщений в плавающий Picture-in-Picture пузырь.

### 5. Инжекция кастомных строк в профиль пользователя (`usernotes.plugin`, `scam_base_writer.plugin`)
Встраивание дополнительных информационных блоков в экран профиля (`ProfileActivity`) требует согласованного перехвата трёх методов:
1. `ProfileActivity.updateRowsIds()`: плагин перехватывает расчет идентификаторов рядов, сохраняет текущее значение `rowCount` в свою переменную (например, `self.note_row = row_count`), увеличивает `rowCount` на 1 и возвращает управление ([usernotes.plugin:226-235](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/usernotes.plugin#L226-L235)).
2. `ProfileActivity.ListAdapter.getItemViewType(int position)`: если `position == self.note_row`, метод возвращает уникальный идентификатор типа представления (например, `99`).
3. `ProfileActivity.ListAdapter.onBindViewHolder(ViewHolder holder, int position)`: при совпадении позиции плагин инфлейтит нативный `TextDetailCell`, настраивает иконку, заголовок, подпись и устанавливает обработчик клика для открытия диалога редактирования.

### 6. Боковое меню (Drawer Menu) и массовые операции
- Регистрация пунктов в шторке Telegram производится через метод базового плагина `self.add_menu_item(MenuItemData(menu_type=MenuItemType.DRAWER_MENU, text="...", on_click=..., icon="..."))` ([ReadAllButton.plugin:40-46](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ReadAllButton.plugin#L40-L46)).
- Массовая пометка диалогов прочитанными вызывается через нативное хранилище сообщений: `MessagesStorage.getInstance(account).readAllDialogs(-1)` ([ReadAllButton.plugin:49-55](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ReadAllButton.plugin#L49-L55)).

### 7. Заголовки, бегущие строки и шапка чата
- **Бегущая строка (Auto Marquee):** длинные названия чатов и секций настроек обрезаются Telegram троеточием. Плагин `auto_marquee.plugin` перехватывает вызовы `ActionBar.setTitle` и программно находит внутренний `TextView`, активируя на нем свойства `TextUtils.TruncateAt.MARQUEE`, `setMarqueeRepeatLimit(-1)` и `view.setSelected(True)` ([auto_marquee.plugin:370-389](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/auto_marquee.plugin#L370-L389)).
- **Скрытие счетчиков участников:** `hide_members_count-1.4.0.plugin` перехватывает метод `ChatActivity.updateSubtitle()` и очищает подзаголовок шапки чата, скрывая общее количество участников и подписчиков ([hide_members_count-1.4.0.plugin:215-335](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hide_members_count-1.4.0.plugin#L215-L335)).

### 8. Жесты, обработка касаний и анимации
- **Защита от закрытия Instant View свайпом:** плагин `ArticleViewerFix.plugin` перехватывает метод `ArticleViewer$WindowView.handleTouchEvent(MotionEvent)` в before-хуке и вызывает `param.setResult(False)`, блокируя жест закрытия окна просмотра статей ([ArticleViewerFix.plugin:16-30](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ArticleViewerFix.plugin#L16-L30)).
- **Глобальный тач-эффект Ripple:** `ripple_touch.plugin` перехватывает диспетчеризацию касаний `Activity.dispatchTouchEvent` и `Dialog.dispatchTouchEvent`, перенаправляя координаты нажатия на прозрачный оверлей, где `ValueAnimator` анимирует радиус и прозрачность расширяющегося круга ([ripple_touch.plugin:160-205](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ripple_touch.plugin#L160-L205)).
- **Фикс перемотки круглых видео:** `roundseekbarpausefix.plugin` перехватывает события слушателя `SeekBarView`, предотвращая непреднамеренную паузу воспроизведения при касании полосы прокрутки ([roundseekbarpausefix.plugin:25-55](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/roundseekbarpausefix.plugin#L25-L55)).

### 9. Стилизация тем, цветовые фильтры и кнопки
- **Редактор тем в реальном времени:** `theme_tweaker.plugin` предоставляет графический HSV-пикер и применяет изменения через вызов `Theme.setThemeColor(Theme.key_..., color, True)` с немедленной перерисовкой окон ([theme_tweaker.plugin:180-200](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/theme_tweaker.plugin#L180-L200)).
- **Кастомный пин диалогов:** `pincolor_plugin.plugin` перехватывает `DialogCell.onDraw(Canvas)` и программно накладывает цветовой фильтр `PorterDuffColorFilter` на значок закрепа `pinIcon` ([pincolor_plugin.plugin:135-141](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/pincolor_plugin.plugin#L135-L141)).
- **Сброс расцветки inline-кнопок:** `NoColorButton.plugin` использует `HookFilter.Condition("this.button.style != null")` при перехвате `BotInlineKeyboard.ButtonBot.getColor()`, принудительно возвращая нейтральный `BackgroundColor.NONE` ([NoColorButton.plugin:16-19](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/NoColorButton.plugin#L16-L19)).
- **Эмуляция Telegram Stars:** `fake_stars.plugin` перехватывает связку методов `StarsController.getBalance()`, `getCachedBalance()` и `balanceAvailable()`, подменяя локальное значение баланса звезд в UI ([fake_stars.plugin:110-125](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/fake_stars.plugin#L110-L125)).

### 10. Оптимизация Lottie-анимаций (`fucklottie.plugin`)
Нижняя панель навигации (`MainTabsUiHelper`) и шторка вложений (`ChatAttachAlert`) используют векторные Lottie-анимации, вызывающие микрофризы. Плагин `fucklottie.plugin` перехватывает методы `setTextAndIcon` и `createView`, подменяя анимированный `TabAnimationView` на легковесный `ImageView` со статическим векторным ресурсом ([fucklottie.plugin:40-65](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/fucklottie.plugin#L40-L65)).

### 11. Ячейки сообщений и чаты
- **Автораскрытие спойлеров:** `spoiler_remover.plugin` перехватывает привязку данных в `ChatMessageCell`, устанавливая флаг раскрытия спойлеров до начала отрисовки ([spoiler_remover.plugin:135-146](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/spoiler_remover.plugin#L135-L146)).
- **Скрытие кнопки «Открыть» у ботов:** `hide_bot_open_button.plugin` в before-хуке ячейки `DialogCell` сбрасывает флаг показа кнопки запуска WebApp, устраняя визуальный мусор в списке диалогов ([hide_bot_open_button.plugin:35-50](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hide_bot_open_button.plugin#L35-L50)).

### 12. Управление активными сессиями и устройствами
- Плагины `sessions_manager.plugin` и `rename_sessions.plugin` перехватывают метод `SessionCell.setSession(TLRPC.TL_authorization, boolean)`, считывают идентификатор сессии и заменяют текст стандартного `nameTextView` на кастомное имя, заданное пользователем ([sessions_manager.plugin:605-620](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sessions_manager.plugin#L605-L620)).

### 13. Расширение интерфейса управления плагинами
- `sorter_plus.plugin` перехватывает вызовы `PluginsActivity.createView` и `UniversalAdapter.fillItems`, динамически пересортировывая переданный список `ArrayList<UItem>` по категориям (Темы, Утилиты, Медиа) и поддерживая фильтрацию поиска ([sorter_plus.plugin:335-345](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sorter_plus.plugin#L335-L345)).
- `plugins_settings.plugin` перехватывает навигационный метод `ActionBarLayout.presentFragment(BaseFragment)` для перенаправления кликов по плагинам на кастомные диалоговые окна настроек ([plugins_settings.plugin:390-415](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/plugins_settings.plugin#L390-L415)).

### 14. Встраиваемые интерактивные игры и нативный Canvas
- `Chess_Game.plugin` демонстрирует интеграцию полноценных HTML5/JS веб-приложений внутри Telegram через размещение `android.webkit.WebView` внутри нативного `BottomSheet` или оверлея `WindowManager` ([Chess_Game.plugin:190-205](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/Chess_Game.plugin#L190-L205)).
- `Sudoku.plugin` строит игровое поле 9×9 исключительно на нативных компонентах `GridLayout` и `Button`, динамически адаптируя цвета клеток под текущую тему Telegram через `Theme.getColor` ([Sudoku.plugin:120-150](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/Sudoku.plugin#L120-L150)).
- `dinorunner.plugin` реализует 60fps аркадный игровой цикл (Game Loop) с прямой отрисовкой спрайтов на `Canvas` под управлением системного тикера `Choreographer.getInstance().postFrameCallback` ([dinorunner.plugin:85-115](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/dinorunner.plugin#L85-L115)).

### 15. Навигация по форумам и каналам
- `always-tabs-forums.plugin` принудительно заставляет Telegram отображать вкладки топиков в форумах через `MethodReplacement(True)` на вызове `ChatObject.areTabsEnabled(TLRPC.Chat)` ([always-tabs-forums.plugin:20-50](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/always-tabs-forums.plugin#L20-L50)).
- `participants_channels.plugin` перехватывает метод `ProfileActivity.switchToCurrentSelectedMode` для добавления вкладки «Каналы», привязанные к группе ([participants_channels.plugin:365-385](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/participants_channels.plugin#L365-L385)).

## Вызовы и наблюдаемые контракты

| Класс / Компонент | Наблюдаемая сигнатура вызова | Назначение и контекст | Доказательство в коде |
|---|---|---|---|
| `PillRegistry` | `registerPill(PillInfo info, PillCreator creator)` | Регистрация плашки в строке заголовка ExteraGram | [ram_info_pill.plugin#L25-L38](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ram_info_pill.plugin#L25-L38) |
| `ItemOptions` | `makeOptions(BaseFragment fragment, View anchor)` | Привязка контекстного попап-меню к элементу UI | [ram_info_pill.plugin#L123-L134](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ram_info_pill.plugin#L123-L134) |
| `SharedConfig` | `deviceBlurEnabled()`, `chatBlurEnabled()` | Глобальные флаги включения размытия | [NoMoreBlur.plugin#L16-L26](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/NoMoreBlur.plugin#L16-L26) |
| `BlurredBackgroundDrawable` | `draw(Canvas canvas)` | Низкоуровневая отрисовка размытия шейдером | [NoMoreBlur.plugin#L29-L35](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/NoMoreBlur.plugin#L29-L35) |
| `BaseFragment` | `isSupportEdgeToEdge()` | Определение поддержки Edge-to-Edge фрагментом | [forceedge2edge.plugin#L10-L17](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/forceedge2edge.plugin#L10-L17) |
| `View` | `setSystemUiVisibility(int flags)` | Управление видимостью StatusBar и NavBar | [hide_system_bars.plugin#L45-L75](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hide_system_bars.plugin#L45-L75) |
| `Window` | `setNavigationBarColor(int color)` | Установка MD3 цвета системной полосы навигации | [md3_navbars_everywhere.plugin#L52-L95](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/md3_navbars_everywhere.plugin#L52-L95) |
| `WindowManager` | `addView(View view, LayoutParams params)` | Добавление плавающего окна поверх всех экранов | [floating_rounds.plugin#L635-L645](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/floating_rounds.plugin#L635-L645) |
| `WindowManager` | `updateViewLayout(View view, LayoutParams params)` | Обновление координат оверлея при перетаскивании | [sticky_notes_overlay.plugin#L830-L840](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sticky_notes_overlay.plugin#L830-L840) |
| `WindowManager` | `removeView(View view)` | Безопасная очистка оверлея при выгрузке | [sticky_notes_overlay.plugin#L240-L245](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sticky_notes_overlay.plugin#L240-L245) |
| `ProfileActivity` | `updateRowsIds()`, `getItemViewType(int)`, `onBindViewHolder` | Тройная инжекция кастомных строк в профиль | [usernotes.plugin#L226-L235](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/usernotes.plugin#L226-L235) |
| `BasePlugin` | `add_menu_item(MenuItemData data)` | Добавление кнопки в боковое меню (DRAWER_MENU) | [ReadAllButton.plugin#L40-L46](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ReadAllButton.plugin#L40-L46) |
| `MessagesStorage` | `readAllDialogs(long folderId)` | Пакетное прочтение всех чатов папки/аккаунта | [ReadAllButton.plugin#L49-L55](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ReadAllButton.plugin#L49-L55) |
| `ActionBar` | `setTitle(CharSequence title)` | Установка заголовка экрана и бегущей строки | [auto_marquee.plugin#L370-L389](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/auto_marquee.plugin#L370-L389) |
| `ArticleViewer$WindowView` | `handleTouchEvent(MotionEvent event)` | Обработка тачей просмотрщика статей Telegram | [ArticleViewerFix.plugin#L16-L30](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ArticleViewerFix.plugin#L16-L30) |
| `ButtonBot` | `getColor()` | Определение цвета фона инлайн-кнопки бота | [NoColorButton.plugin#L16-L19](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/NoColorButton.plugin#L16-L19) |
| `DialogCell` | `onDraw(Canvas canvas)` | Отрисовка ячейки списка чатов (значок закрепа) | [pincolor_plugin.plugin#L135-L141](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/pincolor_plugin.plugin#L135-L141) |
| `StarsController` | `getBalance()`, `getCachedBalance()` | Запрос баланса Telegram Stars пользователя | [fake_stars.plugin#L110-L125](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/fake_stars.plugin#L110-L125) |
| `ChatAttachAlert$AttachButton` | `setTextAndIcon(int, CharSequence, TabAnimationView)` | Привязка Lottie-иконки кнопки вложений | [fucklottie.plugin#L40-L65](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/fucklottie.plugin#L40-L65) |
| `Activity` / `Dialog` | `dispatchTouchEvent(MotionEvent event)` | Глобальный перехват касаний для Ripple | [ripple_touch.plugin#L160-L205](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ripple_touch.plugin#L160-L205) |
| `ChatObject` | `areTabsEnabled(TLRPC$Chat chat)` | Проверка отображения вкладок топиков форума | [always-tabs-forums.plugin#L20-L50](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/always-tabs-forums.plugin#L20-L50) |
| `ChatActivity` | `updateSubtitle()` | Обновление текста подзаголовка в шапке чата | [hide_members_count-1.4.0.plugin#L215-L335](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hide_members_count-1.4.0.plugin#L215-L335) |
| `ChatMessageCell` | `setMessageObject(...)`, отрисовка | Привязка сообщения и отрисовка спойлеров | [spoiler_remover.plugin#L135-L146](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/spoiler_remover.plugin#L135-L146) |
| `SessionCell` | `setSession(TLRPC$TL_authorization, boolean)` | Отрисовка плашки активной сессии устройства | [sessions_manager.plugin#L605-L620](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sessions_manager.plugin#L605-L620) |
| `UniversalAdapter` | `fillItems(ArrayList<UItem> items, UniversalAdapter)` | Формирование списка элементов в PluginsActivity | [sorter_plus.plugin#L335-L345](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/sorter_plus.plugin#L335-L345) |
| `ActionBarLayout` | `presentFragment(BaseFragment fragment)` | Переход между экранами и навигация | [plugins_settings.plugin#L390-L415](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/plugins_settings.plugin#L390-L415) |
| `Bulletin` | `show()` | Отображение нативного тоста/плашки Bulletin | [plugins_settings.plugin#L480-L495](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/plugins_settings.plugin#L480-L495) |
| `BottomSheet$Builder` | `setCustomView(View view)` | Встраивание кастомного контейнера в шторку | [All_Telegram_Icons.plugin#L190-L205](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/All_Telegram_Icons.plugin#L190-L205) |
| `Theme` | `setThemeColor(String key, int color, boolean apply)` | Динамическое изменение цвета ключа темы | [theme_tweaker.plugin#L180-L200](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/theme_tweaker.plugin#L180-L200) |
| `Choreographer` | `postFrameCallback(FrameCallback callback)` | Синхронизация цикла отрисовки с VSYNC дисплея | [dinorunner.plugin#L85-L115](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/dinorunner.plugin#L85-L115) |

## Практические приёмы и рецепты

1. **Рецепт регистрации плашки PillStack:**
   ```python
   PillRegistry = find_class("com.exteragram.messenger.pillstack.core.PillRegistry")
   PillInfo = find_class("com.exteragram.messenger.pillstack.core.PillRegistry$PillInfo")
   PillCreator = find_class("com.exteragram.messenger.pillstack.core.PillRegistry$PillCreator")

   class CustomCreator(dynamic_proxy(PillCreator)):
       def createView(self, context):
           tv = TextView(context)
           tv.setText("RAM: 3.2 GB")
           return tv

   info = PillInfo("my_pill", "RAM Info", 0, True)
   PillRegistry.registerPill(info, CustomCreator())
   ```

2. **Рецепт принудительного Edge-to-Edge:**
   ```python
   from base_plugin import BasePlugin, MethodReplacement

   class ForceEdgePlugin(BasePlugin):
       def on_plugin_load(self):
           bf = find_class("org.telegram.ui.ActionBar.BaseFragment")
           self.hook_method(bf.getClass().getMethod("isSupportEdgeToEdge"), MethodReplacement(True))
   ```

3. **Рецепт создания перетаскиваемого плавающего оверлея:**
   ```python
   def create_floating_window(activity, custom_view):
       wm = activity.getSystemService(Context.WINDOW_SERVICE)
       p = WindowManager.LayoutParams()
       p.type = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY if Build.VERSION.SDK_INT >= 26 else WindowManager.LayoutParams.TYPE_SYSTEM_ALERT
       p.flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
       p.format = PixelFormat.TRANSLUCENT
       p.width = WindowManager.LayoutParams.WRAP_CONTENT
       p.height = WindowManager.LayoutParams.WRAP_CONTENT

       class DragTouchListener(dynamic_proxy(View.OnTouchListener)):
           def __init__(self):
               self.x = self.y = self.raw_x = self.raw_y = 0
           def onTouch(self, v, event):
               action = event.getAction()
               if action == MotionEvent.ACTION_DOWN:
                   self.x, self.y = p.x, p.y
                   self.raw_x, self.raw_y = event.getRawX(), event.getRawY()
                   return True
               elif action == MotionEvent.ACTION_MOVE:
                   p.x = int(self.x + (event.getRawX() - self.raw_x))
                   p.y = int(self.y + (event.getRawY() - self.raw_y))
                   wm.updateViewLayout(custom_view, p)
                   return True
               return False

       custom_view.setOnTouchListener(DragTouchListener())
       wm.addView(custom_view, p)
       return custom_view, wm
   ```

4. **Рецепт инжекции строки в ProfileActivity:**
   ```python
   # В хуке updateRowsIds:
   self.custom_row = param.thisObject.rowCount
   param.thisObject.rowCount += 1

   # В хуке getItemViewType(position):
   if position == self.custom_row:
       param.setResult(CUSTOM_VIEW_TYPE_ID)

   # В хуке onBindViewHolder(holder, position):
   if position == self.custom_row:
       cell = holder.itemView
       cell.setTextAndValue("Заметка", "Текст заметки", False)
   ```

5. **Рецепт авто-скролла длинного текста (Marquee):**
   ```python
   def enable_marquee(text_view):
       text_view.setEllipsize(TextUtils.TruncateAt.MARQUEE)
       text_view.setSingleLine(True)
       text_view.setMarqueeRepeatLimit(-1)  # бесконечный цикл
       text_view.setSelected(True)           # необходимо для старта анимации
   ```

## Ограничения и противоречия

- **Статус верификации:** Все представленные вызовы имеют статус `code`, так как исследованы статическим анализом без инструментального профилирования на устройствах.
- **Утечки окон WindowLeaked:** Плагины оверлеев (`sticky_notes_overlay`, `log_overlay`, `floating_rounds`) критически зависят от наличия корректного `WindowManager.removeView()` в методе `on_plugin_unload()`. Если выгрузка плагина прерывается исключением или метод не вызван, плавающее окно зависает поверх всех приложений до принудительного убийства процесса Telegram.
- **Хуки в Hot Path:** Плагины вроде `ripple_touch` и `animtou` перехватывают `Activity.dispatchTouchEvent` и выполняют рендеринг на каждом микро-перемещении пальца (`ACTION_MOVE`). В связке с мостом Python/Java (Chaquopy) это может вызывать повышенный джиттер кадров (frame drops) на дисплеях 120 Гц.
- **Версионная хрупкость Reflection:** Инжекция рядов в `ProfileActivity` (`updateRowsIds`, `onBindViewHolder`) опирается на целочисленные индексы адаптера. Любое изменение внутренней раскладки строк разработчиками Telegram может сместить позиции соседних рядов (телефон, юзернейм, био), приводя к визуальным аномалиям или `IndexOutOfBoundsException`.
- **Пустые обработчики `on_plugin_unload`:** Плагины `NoMoreBlur`, `ArticleViewerFix` и ряд других оставляют метод `on_plugin_unload()` пустым либо не сохраняют ссылки на `unhook()`, что приводит к сохранению перехватов в памяти JVM вплоть до полного перезапуска приложения.
