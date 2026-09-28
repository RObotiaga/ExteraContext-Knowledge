---
type: source
source_id: smooth-scroll
platform: Android / AyuGram plugin (claimed)
review_status: accepted-with-gaps
review: ../reviews/smooth-scroll.md
date: 2026-09-28
---

# Smooth Scroll Plugin

Источник: [DedyaSergey/Smooth-Scroll-Plugin](https://github.com/DedyaSergey/Smooth-Scroll-Plugin), лицензия MIT. Снимок ветки `master` закреплён на commit [`3148ef2b6a9e3009ea4e04e511fbdc98f061feca`](https://github.com/DedyaSergey/Smooth-Scroll-Plugin/tree/3148ef2b6a9e3009ea4e04e511fbdc98f061feca), получен 2026-09-27T15:53:21.933843Z. Совпадение имени, repository URL и SHA проверено по `snapshot.json`; дерево снимка не усечено, а `file-manifest.json` содержит SHA-256 локальных копий всех девяти входных файлов. Содержимое изучалось только как данные: код не запускался, пакеты не устанавливались.

## Роль источника

Небольшой Python-плагин AyuGram, полезный для разбора формы `BasePlugin`, регистрации send-message hook, настроек `ui.settings`, меню действия чата и вычислительных easing-функций. Метаданные файла заявляют версию 2.0.0, AyuGram `>=12.5.0` и SDK `>=1.4.0`. Это утверждения исходника, а не подтверждение совместимости в работающем клиенте.

README и руководства обещают гладкую прокрутку, жесты, GPU-ускорение и показатели производительности. В закреплённом коде обнаруживаются hook на отправку сообщений и UI-элементы, однако `_update_scroll_position` и `_update_gesture_position` только получают fragment/view и завершаются, не меняя позицию или вид. Реального подключения к `RecyclerListView`, `ChatActivity` или иному пути прокрутки в покрытом файле нет. Поэтому источник показывает заготовки и оболочку плагина, а не подтверждённую реализацию smooth scrolling.

## Покрытие

| Прочитанные материалы | Что извлечено | Границы |
|---|---|---|
| `src/SmoothScroll.plugin` целиком | Метаданные, imports, классы `PerformanceMonitor`/`GestureDetector`, lifecycle, menu action, настройки, message hook, animation loops/easing, обновления UI и статистика | Это единственный исполняемый файл; не запускался. См. строки в таблице API ниже. |
| `README.md`, `SETUP_GUIDE.md`, `docs/QUICK_START.md`, `docs/README.md`, `docs/TECHNICAL.md`, `docs/FEATURES.txt`, `examples/USE_CASES.md`, `PROJECT_COMPLETION.txt` | Заявленные функции, настройка, команды, численные оценки производительности, примеры и developer guide; проверены заявления против исходного кода | Это документация проекта, а не runtime evidence; численные метрики и рецепты не проверялись. |
| `.gitignore` | Правила исключения Python/build/IDE/test/temp файлов | Технических сведений о плагине или API не содержит. |
| `LICENSE` | Лицензия MIT | Лицензионная совместимость не анализировалась. |
| `snapshot.json`, `tree.json`, `repository.json`, `file-manifest.json`, `radar-context.md`, `radar-urls.json` | Закреплённая идентичность/SHA, список файлов, метаданные репозитория и контекст радара | `radar-urls.json` пуст; исторические ссылки из радара отсутствуют. |

Дерево содержит 14 entries, из них 11 файлов и 3 каталога. При независимой проверке обнаружилось, что первоначальный локальный snapshot пропустил `.gitignore`; файл получен отдельно с того же commit и добавлен в manifest. После этого SHA-256 всех 11 сохранённых файлов совпадает с manifest, а вычисленные Git blob SHA всех файлов совпадают с tree. В снимке нет тестов, workflow CI или build-конфигурации. Совместимость SDK, установленный клиент, анимации на устройстве и заявленные FPS/память/батарея здесь не проверялись. Детали внутренностей Android-клиента вне этого репозитория не изучались.

## Архитектура и вызовы

Плагин наследуется от `BasePlugin`; при `on_plugin_load` регистрирует `add_on_send_message_hook`, читает пять settings и добавляет `CHAT_ACTION_MENU` item. Hook распознаёт четыре точных текстовых команды: две запускают тестовые циклы и отменяют исходную отправку, а две заменяют текст сообщения выводом статистики/информации. Это message-send interception, не отдельный публичный slash-command API.

| Модуль / точка вызова | Сигнатура или call-site | Назначение и фактическая граница |
|---|---|---|
| Метаданные модуля | `__id__`, `__version__`, `__app_version__`, `__sdk_version__` | ID `smooth_scroll`, версия `2.0.0`, заявлены AyuGram `>=12.5.0`, SDK `>=1.4.0`; требования не проверены. |
| `SmoothScrollPlugin` lifecycle | `on_plugin_load()` / `on_plugin_unload()` | Подключает send-message hook, загружает настройки, добавляет/удаляет пункт меню, сбрасывает `_scroll_active`. Видно добавление hook; снятие hook в unload не вызывается. |
| Chat menu | `add_menu_item(MenuItemData(menu_type=CHAT_ACTION_MENU, on_click=...))` | Пункт «Тестировать анимации» запускает `_test_smooth_scroll()` и показывает bulletin. |
| Settings UI | `create_settings() -> List[Any]` с `Header`, `Text`, `Selector`, `Switch`, `Divider` | Настраивает стиль/скорость, жесты, momentum, оптимизацию/FPS, GPU и переходы. Часть ключей не считывается и не влияет на кодовые пути. |
| Исходящие сообщения | `on_send_message_hook(account, params) -> HookResult` | `.scroll.test` и `.scroll.gesture` запускают демонстрационный цикл и возвращают `CANCEL`; `.scroll.stats` и `.scroll.info` меняют `params.message` и возвращают `MODIFY`. Иные тексты пропускаются. |
| Частота кадров | `PerformanceMonitor(max_fps=60).can_render() -> bool` | Считает допустимые интервалы по `time.time()` и увеличивает счётчики пропущенных/отрисованных вызовов. Это локальный gate вычислительного цикла, не настройка системного render loop/GPU. |
| Детектор касаний | `GestureDetector.on_touch_start(x,y)`, `on_touch_move(x,y)`, `on_touch_end()` | Хранит начальную координату/время и выдаёт delta/distance; не подключён к Android touch listener. `on_touch_end` рассчитывает `(0 - start)/elapsed`, а не скорость по конечной координате/пройденному пути. |
| Scroll demo | `_test_smooth_scroll()` → daemon `threading.Thread` → `_animate_scroll(0,500,duration_ms)` | Фоновый цикл вычисляет eased positions и планирует `_update_scroll_position` через `run_on_ui_thread`; callback не применяет вычисленную позицию к view. |
| Gesture demo | `_test_gesture_animation()` → `_animate_gesture(type,duration_ms)` | Перебирает прогресс и планирует `_update_gesture_position`; callback не изменяет view. Демонстрация не управляет настоящими жестами пользователя. |
| Animation curves | `_get_eased_progress(style, progress)` → `_ease_*` | В коде есть 8 математических кривых (cubic, elastic, bounce, spring, wave, bezier, decelerate); наличие функций не означает, что они подключены к прокрутке интерфейса. |
| UI position callbacks | `_update_scroll_position(position)`, `_update_gesture_position(gesture_type, progress)` | Оба callback только получают `get_last_fragment()` и проверяют `frag.getView()`; фактическое изменение scroll offset/view отсутствует. |
| Статистика | `_get_performance_stats()` | Формирует счётчики вызовов `can_render`, render-rate, выбранные параметры. Никакие аппаратные метрики не опрашиваются; это статистика внутренних счётчиков. |
| Информация о плагине | `_get_plugin_info()` | Динамически считает имена стилей и жестов, но безусловно печатает «Оптимизация FPS включена» и «GPU ускорение активно», независимо от настроек и реализации; это строки отчёта, а не свидетельство функций. |

## Полезные приёмы из исходника

- Hook для локальной команды может сравнить нормализованный текст composer, отменить распознанную команду через `HookStrategy.CANCEL` и модифицировать текст ответа через `HookStrategy.MODIFY`.
- Настройку UI можно связать с persisted setting через `get_setting`/`set_setting` и callback selector; здесь изменение стиля и длительности сохраняется отдельно.
- Для вычислительной анимации исходник отделяет easing curve от цикла планирования и передаёт lambda с захваченным значением (`p=current_pos`) в `run_on_ui_thread`.
- Любую такую интеграцию с UI нужно дополнить настоящим host API для выбора scrollable view, чтения/записи его offset, отмены/синхронизации цикла и lifecycle cleanup; эти шаги в снимке отсутствуют.

## Ограничения и расхождения

1. README, документация и `PROJECT_COMPLETION.txt` заявляют восемь стилей анимации, шесть жестов, инерцию, GPU, переходы чатов и автоматическую плавную прокрутку; код не связывает их с реальными view. В частности, обновляющие callback пусты после проверки fragment/view.
2. `GestureDetector` создан, но его методы нигде не вызываются из `SmoothScrollPlugin`; сенсорный hook/listener не регистрируется.
3. Настройки `enable_momentum`, `enable_optimization`, `use_gpu`, `smooth_transition` и `transition_style` не включают соответствующую реализацию. `_enable_momentum`/`_enable_optimization` загружаются, но дальше не используются; GPU/transition values даже не читаются из settings. `max_fps` создаёт новый monitor при изменении, но сохранённое значение при загрузке не считывается.
4. Реализация `on_touch_end` не принимает финальные координаты и поэтому не может вычислить скорость фактического свайпа; выдаваемая величина зависит от абсолютной стартовой координаты.
5. `_animate_scroll` и `_animate_gesture` выполняют `time.sleep` в фоне после принятого `can_render()` шага, а UI callback планируется асинхронно; при отклонённом шаге цикл продолжает работу без ожидания. `progress = step / steps` при `range(steps)` также не достигает `1` и не ставит отдельный финальный endpoint. Код не подтверждает синхронизацию с кадрами Android или отсутствие гонок при unload.
6. В `_ease_elastic` вычисляется `c4`, но не используется; формула возвращает лишь очень малое затухающее значение, а не обычную эластичную кривую. `_ease_bounce` состоит из двух параболических участков и не совершает отскоков; `_ease_wave` — косинусное сглаживание без волновых колебаний. Это вычисляемые easing-значения, но README-имена не гарантируют соответствующую форму эффекта.
7. Счётчик производительности считает попытки пропуска/пропускаемые вызовы собственного цикла, а не кадры реально отрисованные приложением. При отклонённом `can_render()` цикл делает `continue` без `sleep`, поэтому может активно крутиться до следующего разрешённого интервала. Таблицы CPU/GPU/RAM/battery и проценты из docs не имеют источника измерения в коде. `_get_plugin_info()` дополнительно заявляет FPS optimization и GPU active безусловно, хотя UI/runtime path этого не реализует.
8. `_animate_scroll` проверяет `_scroll_active` между шагами и unload сбрасывает этот флаг; `_animate_gesture` такого stop-check не имеет, поэтому уже запущенная gesture-задача не отменяется при unload. Уже переданные в UI очередь callbacks также отдельно не отзываются.
9. Документационные инструкции установки в каталог AyuGram, как и заявленные требования версии, не проверялись на устройстве; runtime-verified статуса нет.

## Ссылки на первоисточник

- [Основной файл плагина, закреплённый SHA](https://github.com/DedyaSergey/Smooth-Scroll-Plugin/blob/3148ef2b6a9e3009ea4e04e511fbdc98f061feca/src/SmoothScroll.plugin)
- [README](https://github.com/DedyaSergey/Smooth-Scroll-Plugin/blob/3148ef2b6a9e3009ea4e04e511fbdc98f061feca/README.md)
- [Technical guide](https://github.com/DedyaSergey/Smooth-Scroll-Plugin/blob/3148ef2b6a9e3009ea4e04e511fbdc98f061feca/docs/TECHNICAL.md)
- [Quick start](https://github.com/DedyaSergey/Smooth-Scroll-Plugin/blob/3148ef2b6a9e3009ea4e04e511fbdc98f061feca/docs/QUICK_START.md)
