# Независимая проверка источника: for-vibecoders

## Область и решение

Проверен репозиторий [`corerudo/for-vibecoders`](https://github.com/corerudo/for-vibecoders): main на `01cb2bfee889da331d348ad190862a03093c592d` и точный исторический файл animtou 2.1.0 из `ebdb543a6819915baa0ce62c3e5e15852d3a3fa0`. Сверялись source-lock, recursive tree, README, индекс, repo-vs-context7, все четыре каталога примеров и доступные analysis-документы. Назначение из радара зафиксировано в `raw/radar.md:1872-1917`: практические примеры ExteraGram/AyuGram, с особым интересом к animtou 2.1.0, LodraBu и muztep. Собственный `radar-context.md`/`radar-urls.json` источника ещё отсутствует; назначение сверено по `raw/radar.md:1872-1917`, а источник и SHA — по сохранённым GitHub metadata/tree и permalinks.

**Вердикт: `accepted-with-gaps`.** Страница полезна и в целом аккуратно разделяет код, документацию и авторские runtime сообщения. Внесены исправления на lifecycle, reflection uncertainty и declared dependency. В JSON теперь 30 фактов с уникальными ID `fvb-001`–`fvb-030`. Источник остаётся примерной базой, не официальным SDK-контрактом.

## Независимое покрытие

Прочитаны и сверены заголовки и содержательные разделы трёх analysis-документов: animtou (904 строки), LodraBu (662) и muztep (614). Проверен весь исполняемый код relevant-плагинов: animtou 2.3.0 (520 строк) и исторический 2.1.0 (358), LodraBu (200), muztep (796); jaxtools analysis и `.plugin` по 35 байт каждый, badge note (5 строк). Также сверены README (42 строки), plugins-index (7), repo-vs-context7 (104) и recursive tree на указанном SHA.

- animtou: reflection на `View.dispatchTouchEvent`, `MotionEvent` и дедупликация, raw/local координаты, обход `WindowManagerGlobal.mViews`, polling новых окон, собственный `SuperRipple`, shader/field/method reflection, `RuntimeShader`/`RenderEffect`, ограниченный ripple cache, настройки/seekbar proxy, UI dispatcher, optional updater, load/unload, priority и версия Android. Версионные отличия 2.1.0 → 2.3.0 сохранены раздельно; открытый дефект контекстного меню помечен как author-reported, его причина как гипотеза.
- LodraBu: три постоянных UI hooks и динамический listener hook, точные reflection signatures, `MethodHook`/`hook_method`/`add_hook`, `find_class` против `Class.forName`, пользовательские menu/settings элементы, account switching и диагностика исключений.
- muztep: требования metadata, message command hook и отмена отправки, очередь `PLUGINS_QUEUE`, URI `MethodReplacement` и снятие через `finally`, Java reflection hooks, UI/cache boundary, inline markup/buttons, сохранение и восстановление сессий, redraw, загрузка/удаление временных файлов и media metadata.
- jaxtools: пустые stub-файлы отмечены как недостаток материала; server submission endpoints не относятся к Android plugin API. Workflow, license и backend не включены в область plugin-integration знаний.

Покрытие достаточное для фактов, которые даёт этот репозиторий, и для границ его полезности. В страницу добавлены конкретные пробелы: runtime/device matrix, loader behavior для `mutagen`, распаковка/подпись `.plugin`, официальная SDK реализация, отсутствующее mini-tutorial, stub jaxtools и отсутствие DEX/build recipes.

## Найденные проблемы и правки

1. Анализ LodraBu сообщает, что `find_class`-обёртка в наблюдавшейся автором среде не имела `getDeclaredMethod`, и рекомендует `jclass("java.lang.Class").forName(...)`. Между тем muztep использует `find_class("java.lang.Class").forName(...)`, получает parameter classes через `find_class`, а исключения в reflection hook installers подавляются. Страница теперь прямо связывает эти два source claims и отмечает возможный тихий отказ регистрации hooks как **inference**, а не установленный runtime факт. Добавлен `fvb-029`.
2. Lifecycle не был достаточно явно отмечен. В muztep unload снимает URI replacement, но `_btn_unhooks` остаётся пустым: hook handles туда не добавляются; handles `_CellSetupHook`/`_ChatOpenHook` тоже не сохраняются для явной очистки. В LodraBu нет собственного unload/сохранения handles, а profile-menu listener hook ставится при каждом создании меню. Возможное дублирование зависит от host и осталось непроверенным. Исправлена source page и добавлен `fvb-028`.
3. Пропущена зависимость muztep: `__requirements__ = ["mutagen"]`; поведение host packaging/install неизвестно. Отмечено на странице и добавлен `fvb-030`.
4. Frontmatter отсутствовал; добавлены `review_status`, относительная ссылка на этот review, SHA scope и число фактов.

Точные сигнатуры из кода совпадают с приведёнными на странице: `ProfileActivity.createActionBarMenu(Boolean.TYPE)`, `SettingsActivity.fillItems(ArrayList, UniversalAdapter)`, `SettingsActivity.onClick(UItem, View, Integer.TYPE, Float.TYPE, Float.TYPE)`, `View.dispatchTouchEvent(MotionEvent)`; muztep hooks перечисляются по имени метода без фильтрации перегрузок. Ни один просмотр исходника не переобозначен как независимый runtime test. Авторские device/runtime наблюдения LodraBu сохранены с этой оговоркой.

## Дубликаты и тематическая нормализация

Локально проверены 30 JSON ID: повторы ID отсутствуют. Совпадающие принципы (точная reflection-сигнатура, retention/unhook lifecycle, UI thread boundary, синхронный cache-only render hook, bounded cache и cache invalidation) изложены как разные конкретные примеры с собственным version/provenance; не объединялись несовместимые plugin contracts или версии animtou. При будущей консолидации направлять их в канонические темы `reflection`, `hook lifecycle`, `threading/UI`, `cache`, `plugin dependencies`, `runtime compatibility`; не переносить author-reported SDK behavior как универсальную гарантию.

## Остаточные пробелы

- Нет независимого запуска plugin на конкретной ExteraGram/AyuGram сборке, Android API matrix, reproducible device log или executable host test harness. Даже заявления исходных analysis-документов о реально работавших версиях остаются provenance автора.
- Не скачивались внешние official docs и Telegram/ExteraGram APK/decompiled internals, на которые README ссылается; их содержимое — отдельная задача. Поэтому публичные SDK contracts и class/member stability этим review не подтверждаются.
- Не воспроизводились `find_class` wrapper behavior, возможный silent failure muztep, очистка hooks framework-ом и потенциальная повторная регистрация listener-а LodraBu.
- Зависимость muztep `mutagen`, runtime package installation, `.plugin` сборка/подпись/загрузка не проверялись.
- Нет DEX loading/build recipe. jaxtools source почти пуст; каталог содержит server-side submission code, который не документирует client plugin API.
- Это review фиксированных SHA; последующие коммиты upstream потребуют нового review.


