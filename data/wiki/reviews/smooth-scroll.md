---
type: review
source_id: smooth-scroll
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: DedyaSergey/Smooth-Scroll-Plugin

- **Вердикт: accepted-with-gaps.** Source page в основном точно описывает wrapper, команды и вычислительные helpers и ясно отделяет их от заявленной реальной прокрутки. Проверка нашла и исправила пропущенный файл snapshot, несколько performance/lifecycle/easing оговорок и безусловные утверждения плагина о GPU/FPS.
- **Snapshot:** `DedyaSergey/Smooth-Scroll-Plugin`, `master`, commit `3148ef2b6a9e3009ea4e04e511fbdc98f061feca`, захвачен 2026-09-27. `repository.json` подтверждает полное имя, URL и MIT; `tree.json` не усечён: 14 entries (11 blobs и 3 каталога). Исходный manifest содержал 10 файлов и упускал `.gitignore`; файл загружен отдельно по тому же commit через `work/acquire.py`. Теперь все 11 файлов из tree присутствуют, каждый совпадает с SHA-256 из manifest и Git blob SHA из tree. URL и SHA в source page совпадают с snapshot.
- **Независимое покрытие:** весь `src/SmoothScroll.plugin`; `README.md`, `SETUP_GUIDE.md`, `PROJECT_COMPLETION.txt`, `docs/FEATURES.txt`, `docs/QUICK_START.md`, `docs/README.md`, `docs/TECHNICAL.md`, `examples/USE_CASES.md`, `LICENSE`, `.gitignore`; `snapshot.json`, `tree.json`, `repository.json`, `file-manifest.json`, `radar-context.md` и `radar-urls.json`. Сверены список файлов, API call-sites, весь путь settings → сохранение/загрузка → эффект, message hook, UI callbacks, циклы/остановка, easing реализации и фактические поля статистики. `radar-context.md` указывает на тот же репозиторий и согласуется с выводом о недоказанной плавной прокрутке; `radar-urls.json` пуст. `.gitignore` не добавляет технических сведений.
- **Граница:** код и документация прочитаны статически, не запускались; исходник не собирался. В tree нет тестов, CI workflow или build-конфигурации. Внутренний API AyuGram/Android, совместимость конкретной сборки и поведение на устройстве по этому репозиторию не подтверждены.

## Найденные проблемы и исправления

- Исправлено покрытие snapshot: дерево содержит 14 entries, а не 13; оно содержит 11 файлов, а не 9. Выявленный пропуск `.gitignore` получен и сверены оба вида checksums всех файлов.
- Уточнено performance поведение: оба animation loop делают `continue` при отказе `can_render()` до `time.sleep`, поэтому FPS gate может активно крутить цикл до разрешённого интервала. Это ограничивает более общее описание счётчика/производительности.
- В обоих циклах прогресс рассчитывается как `step / steps` для `range(steps)`, поэтому вычисленный ряд не доходит до `1`, и финальный endpoint отдельно не ставится.
- Добавлена граница lifecycle: сброс `_scroll_active` останавливает только scroll loop на следующей проверке; gesture loop не проверяет stop-token или unload, а уже поставленные UI callbacks не отзываются.
- Явно разоблачены саморепортируемые возможности: `_get_plugin_info()` всегда печатает, что FPS optimization включена и GPU активно, хотя не читает ни setting, ни аппаратные метрики; эта строка не является свидетельством реализации.
- Уточнены формулы: `_ease_bounce` не содержит повторного отскока, `_ease_wave` — косинусное сглаживание, `_ease_elastic` игнорирует вычисленный `c4` и возвращает очень малые значения для внутренних точек. Наличие восьми имён/ветвей подтверждает выбор вычислений, но не описанный пользователю эффект.
- Основные UI выводы source page подтверждены: `_update_scroll_position` и `_update_gesture_position` лишь находят fragment и проверяют view; в них нет смещения, трансформации или иного изменения view. `GestureDetector` нигде не подключён к touch source. `PerformanceMonitor` измеряет только принятые/отклонённые вызовы своего метода.
- Факты дополнены отдельными записями про busy-loop, неполный endpoint, отмену задач, статический отчёт о GPU/FPS и фактическую форму некоторых кривых. После исправления набор содержит **25 фактов и 25 уникальных ID** (`smooth-scroll-001`…`smooth-scroll-025`); повторяющихся ID или полностью одинаковых claims внутри JSON не обнаружено.

## API и соответствие документации

Call-sites в `src/SmoothScroll.plugin` согласуются с описанием: `BasePlugin`, импорты hook/settings/bulletin, `add_on_send_message_hook`, чтение/запись settings, `CHAT_ACTION_MENU`, `run_on_ui_thread`, `get_last_fragment()`/`getView()`, `BulletinHelper.show_success`, `threading.Thread` и `time.sleep`. Сигнатуры API host извне этого репозитория отдельно не подтверждены, поэтому их нельзя переносить как проверенный SDK-контракт.

README и документы проекта заявляют восемь стилей, шесть жестов, ограничение FPS, GPU, переходы между чатами, инерцию и измерения ресурсов. Код содержит восемь имён/вычислительных методов и шесть названий жестов, но не подключает touch listener и не мутирует scrollable view. Опции momentum, optimization, GPU и chat transition не реализованы как заявлено; hardcoded текст `_get_plugin_info()` особенно вводит в заблуждение. Встроенная статистика считает свои вызовы, не реальные кадры/CPU/GPU/RAM/battery. Эти документационные заявления остаются `docs`, а runtime/performance не помечены как проверенные.

## Дубликаты и канонические темы

В других источниках уже есть сведения о `HookStrategy`/`HookResult`, `add_on_send_message_hook()` и `CHAT_ACTION_MENU` (`official-sdk`, `for-vibecoders`, `template-n08`, `exteragram-mcp`, другие примеры). Это повторяемые SDK/plugin patterns, а не дубли исходника: оставлены отдельные подтверждения с provenance smooth-scroll. Для будущего синтеза подходят темы `hooks` и `ui`; lifecycle cleanup — `lifecycle`, worker/dispatch — `threading`, FPS claims и собственная telemetry — `performance`/`debug`. Сведения о stub callbacks и конкретных easing ошибках принадлежат этому репозиторию и не должны сливаться с контрактами других клиентов или forks. Другие source pages, index, topics и APIs этим review не менялись.

## Остаточные gaps

- Не подтверждена работа с конкретной версией AyuGram host/Plugin SDK, включая доступность и thread semantics перечисленных host API.
- Нет runtime проверки, сборки, теста на устройстве или независимого замера заявленных кадров/ресурсов; исходный код не создаёт доказательства фактической производительности.
- Не изучены исходники host-клиента, поэтому подходящая scrollable view и безопасный способ изменения offset для этой платформы остаются неизвестными.
- Численные таблицы и инструкции установки в документации принадлежат авторам; они не были воспроизведены.
