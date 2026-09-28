# Независимая проверка: `plugins-store`

**Вердикт: `accepted-with-gaps`.** Проверен снимок `Kangel-Plugins/Plugins-Store` на commit [`513e29a07858e5dec3a8dcdc6a860fe4296f1d43`](https://github.com/Kangel-Plugins/Plugins-Store/commit/513e29a07858e5dec3a8dcdc6a860fe4296f1d43), захваченный 2026-09-27. Это отдельная проверка после сборщика. Чтение репозитория и вложенного исходника было статическим; Android-клиент не запускался, сборок/установок и сетевой проверки зеркал не было.

## Provenance и охват

`snapshot.json` указывает `main`, тот же commit SHA и `tree_truncated: false`; API-дерево содержит 1 583 записи. Независимо пересчитаны 688 `Plugins/*.plugin`, 12 `Plugins/*.eaf`, 616 файлов `.plugin`/`.eaf`/`.elyx` в `legacy_versions/`; захваченный `store.json` разбирается как объект с 698 ключами. SHA-256 каждого файла, перечисленного в `file-manifest.json` (15 файлов, включая добавленный при проверке `Plugins/kangel_plugins_manager.eaf`), совпал с manifest.

Прочитаны `README.md`, `AGENTS.md`, весь `store.json`, весь `.github/workflows/mirror.yml`, выбранные `ReadAllButton`, `ArticleViewerFix`, `NoMoreBlur`, весь короткий файл `NoColorButton.plugin` (19 строк), а также ZIP-контейнер `Plugins/kangel_plugins_manager.eaf`. В пакете прочитаны `refmap.json`, `metainfo.json`, `src/store.py`, `src/security/verify.py`, `src/elyx_parser.py`, `src/mixins/store_ops.py`, релевантные install/update-фрагменты `src/mixins/installer.py` и вызов обновления в `src/views/plugin_list.py`. Внешний архив имеет SHA-256 `554815b906a155210f02fdd4de76c66ce4cf1fcba34b4e4651f143bc0b216625`; чтение архива не исполняло его содержимое.

Радар описывает именно каталог актуального `Kangel-Plugins/Plugins-Store`, включая GitHub/Codeberg/GitVerse URL и отдельные исторические проблемы старого имени организации. URL-снимок и repository metadata совпадают с назначенным репозиторием; выводы привязаны к pinned commit, не к изменяемой `main`.

## Найденные проблемы и исправления

- Страница сборщика ошибочно утверждала, что в репозитории нет исходника KPM. В каталоге находится `Plugins/kangel_plugins_manager.eaf`; его внутренний `metainfo.json` называет KPM 1.5.4 и задаёт `app_version >=12.9.0`, `sdk_version >=1.4.5.3`. В review исправлена граница: это реализация менеджера распространения/установки, но не исходник штатного движка плагинов ExteraGram и не SDK.
- Документация `AGENTS.md` не описывает `signature`, и сборщик оставил её проверку неизвестной. В KPM 1.5.4 `security/verify.py` загружает встроенный `public_key.pem` и использует `SHA256withRSA` для UTF-8 сообщения `plugin_id:version:file_hash`. `StoreOpsMixin._check_plugin_data` принимает совпавший текущий SHA без подписи, а при заданной подписи требует успешной проверки. `install_plugin_by_id` вызывает data check при включённой настройке `block_untrusted_plugins` с default `True`.
- Обнаружено существенное различие путей: `update_selected_plugins` напрямую устанавливает изменившиеся байты и сам не вызывает data check; UI вызывает этот метод напрямую. Зафиксировано как статическое ограничение проверки целостности именно этого заархивированного KPM, без заявления о подтверждённом runtime-эксплойте.
- Уточнено, что runtime-логика зеркал отличается от GitHub Actions workflow. В коде Store auto-порядок — Kangel/Forgejo, GitHub, Codeberg, GitVerse; при недоступном API SHA имеющийся кэш может считаться валидным, что позволяет не обращаться к другим URL при обычном refresh. Workflow описывает отдельную последовательность переписывания ссылок и force-push.
- Добавлена наблюдаемая `.eaf`-ветка: URL определяется по расширению, целевой каталог удаляется, архив распаковывается, метаданные разбираются с refmap, затем устанавливаются найденные `dex`, `wheels`, `native`. Эти утверждения ограничены конкретным call-site KPM 1.5.4.
- Удалена неподкреплённая обобщающая фраза о matching методов по числу параметров во всём каталоге; для `NoMoreBlur` оставлено только подтверждённое данным файлом matching по именам.
- В `NoColorButton.plugin` прочитан весь короткий файл и отражён before-hook `BotInlineKeyboard.ButtonBot.getColor` с фильтром и результатом `BackgroundColor.NONE`; поведение SDK не объявлено проверенным.

Доказательства вложенного исходника записаны в виде `Plugins/kangel_plugins_manager.eaf!<member path>:<line>` и ведут на pinned permalink самого архива. Сигнатуры `BasePlugin`/`hook_method` из обычных `.plugin` оставлены как конкретные call-site, не нормативный API SDK. README/`AGENTS.md` помечены как документационные утверждения; статический осмотр кода не обозначен как `runtime-verified`.

## Факты и повторы

В `work/plugins-store-facts.json` после проверки **21 факт с 21 уникальным ID**; точных повторяющихся claim-строк нет. Повторяющиеся общие темы намеренно остаются с разным provenance: документационный формат каталога отдельно от поведения KPM; наличие поля `signature` отдельно от конкретного алгоритма проверки; workflow зеркал отдельно от runtime-порядка fallback. Для последующего тематического сведения канонические темы: `distribution`, `security`, `tool`, `lifecycle`, `ui`, `storage`, `hooks`, `portability`.

## Остаточные пробелы

- Не анализировались реализации 688 текущих `.plugin`, 11 других `.eaf` и 616 исторических файлов; не сопоставлялись все 698 store-записей с файлами, актуальными хешами и подписями.
- Из исходника KPM рассмотрены перечисленные модули и вызовы, а не весь пакет UI/hooks/compatibility. Связь его менеджера со штатными загрузчиком и API ExteraGram отдельно не прослежена.
- Состояние и содержимое Codeberg/GitVerse/Forgejo в сети, реальные срабатывания workflow и результат проверки подписи на Android не проверялись. Порядок KPM является кодовым выводом из одного вложенного релиза.
- Архив/код не устанавливались и не запускались; совместимость примеров и описанных путей с другими версиями клиента не утверждается.

Статус страницы источника выставлен `accepted-with-gaps`. Утверждений об абсолютной полноте для неизученного кода нет.
