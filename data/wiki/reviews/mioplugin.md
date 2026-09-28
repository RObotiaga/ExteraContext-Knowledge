# Независимая проверка: mioplugin

- Вердикт: **accepted-with-gaps**.
- Область: источник `fuckramochka/mioplugin`, ветка `main`, snapshot `b5eb7ee542635ae52cf5eabc622f1944e4148a56`, зафиксированный 2026-09-27. `snapshot.json` и `tree.json` указывают один SHA и `tree_truncated: false`; дерево содержит 48 файловых blobs. Прочитаны radar-context и весь доступный acquisition по этому SHA.
- Результат: проверены source page и все записи `work/mioplugin-facts.json`; добавлены отсутствовавшие факты, уточнены формулировки, исправлены статус доказательства GPL/MIT и англоязычный claim о Custom Profile. Всего **36 уникальных фактов** с ID `mioplugin-001`…`mioplugin-036`.
- Работа была статической: исходники, документация, manifests и metadata только прочитаны. Ничего из проекта не запускалось, не собиралось и не устанавливалось; runtime-поведение не проверялось.

## Независимое покрытие

Сопоставлены `tree.json`, `file-manifest.json`, `snapshot.json`, `radar-context.md` и пустой `radar-urls.json`. В raw acquisition доступны корневые `README.md`, `LICENSE`, `catalog.json`, `HOOKS_REFERENCE.md`, `PLUGINS_DEV_GUIDE.md`; все 11 файлов `plugins/*/{README.md,manifest.json,plugin.py}`; и Rust SDK `Cargo.toml`, README, `src/lib.rs`, `src/envelope.rs`, `examples/echo.rs`. Проверены также манифесты каталога и статусы/ссылки source page.

Все 11 Python examples прочитаны целиком: `antispam_guard`, `auto_reaction`, `code_formatter`, `custom_profile`, `dice_roller`, `in_app_notifications`, `link_cleaner`, `message_counter`, `message_styler`, `quick_tools`, `text_transformer`. Отдельно сверены их README и manifest с фактическими entrypoints и кодом. Rust SDK сверялся по исходникам, тестам, примеру, `Cargo.toml` и собственному README, без запуска Cargo.

Дерево содержит 48 blobs, acquisition — 43. Не получены корневой и crate `.gitignore`, SDK `Cargo.lock` и два бинарных архива `Custom Profile.plugin` (корневой и в `plugins/custom_profile/`). `.gitignore` не влияет на API обзор; отсутствие lockfile ограничивает проверку crate metadata/dependency snapshot; содержимое архивов не проверялось. Большой встроенный DEX payload внутри `plugins/custom_profile/plugin.py` также не декодировался и не исследовался как Android-реализация.

## Исправления и важные findings

- Добавлено расхождение `message_styler`: module metadata заявляет `.pixel`, `.sparkle`, `.needy`, а фактические ветви send-hook реализуют `.sparkle`, `.needy`, `.small`. `.pixel` не реализована, `.small` не заявлена; README/manifest не дают точного списка команд.
- Machine facts ранее не фиксировали заявленные в `PLUGINS_DEV_GUIDE.md` Chaquopy 3.11, Java/Kotlin и WASM runtimes, а также ключевое расхождение framework/manifest API. Добавлены отдельные записи со статусами `docs` и `inference`.
- Факт о лицензиях получил статус `inference`, поскольку это сравнение деклараций из разных файлов: root README/`LICENSE` дают MIT, Cargo metadata Rust SDK — `GPL-3.0`. В снимке нет объяснения или разрешения этого расхождения; лицензию SDK нельзя выводить только из корневого README.
- Две схемы Python нельзя считать одним контрактом: guide описывает `miogram.plugins.Plugin`, `on_load`/`on_message_send` и `plugin.json` с `entrypoint`/`minAppVersion`, тогда как HOOKS_REFERENCE и включённые примеры используют `BasePlugin`, `on_plugin_load`/`on_send_message_hook` и manifests с `entry_point`/`min_app_version`. README/guide claims не подтверждены host implementation.
- Permission claims, runtime permission review, Java hooks, TL request interception, AccountClient, settings/storage, app lifecycle и host cleanup остаются документированными заявлениями: реализация движка отсутствует. В доступных manifests permission fields не объявлены.
- Уточнены источники WASM-контракта: `src/envelope.rs` задаёт magic `MIOG`, а SDK README ошибочно называет `HYPR`; README сводит ошибку ABI к `-1`, а код отображает semantic code как `-(code)-1`. Объявленный envelope `MAX_TOTAL` фактически не ограничивает payload, поскольку `payload_len_hint` всегда возвращает ноль.
- Зафиксирована воспроизводимость загрузки: все 11 catalog URLs используют mutable `main`; Custom Profile catalog URL ведёт на `.plugin`, а per-plugin manifest — на `plugin.py`.
- Каталог JSON содержит 11 plugins, root README перечисляет пять. README/manifest Auto Reaction обещают фильтры по ключевым словам/чатам, но sample реагирует на каждое входящее сообщение при включённом setting. Quick Tools и In-App Notifications также обещают возможности, отсутствующие в доступных sample entrypoints.
- `Custom Profile` использует Android bridge и `DexClassLoader`; Python wrapper объявляет app/SDK markers и упоминает ExteraGram 12.5.1/12.8.1, но это не доказывает общую совместимость SDK с ExteraGram/AyuGram.

## Повторы и канонические темы

Повторяющихся `topic + нормализованный claim` внутри 35 записей не обнаружено; ID уникальны. Общие темы допустимо объединять позднее по `lifecycle`, `hooks`, `accounts`, `ui`, `storage`, `network`, `security`, `build`, `testing` и `portability`, сохраняя `mioplugin` как отдельный provenance. Контракты Miogram не объединять с похожими ExteraGram/AyuGram API: в самом источнике совместимость не подтверждена, а документация и примеры расходятся.

## Остаточные gaps и verdict

- Нет host/plugin-engine реализации, host ABI, WAMR runner, permission enforcement, Android build/CI или установленного клиента; поэтому callback dispatch, threading, account routing, cleanup, sandbox и установки не подтверждены.
- Не просмотрены два бинарных `.plugin` и содержимое embedded DEX. Отдельные README описывают функции, которые не видны в соответствующих доступных Python entrypoints.
- `Cargo.lock` отсутствует в raw acquisition, хотя присутствует в tree; команды cargo и описанный CI не проверялись запуском.
- Документация внутренне противоречива, особенно manifest/lifecycle schema и WASM ABI. Извлечённые API следует считать snapshot-specific evidence, а не стабильным или переносимым контрактом.

Имеющиеся первичные файлы достаточны для полезного статического описания каталога, 11 Python examples и guest-side Rust SDK, но вышеуказанные ограничения существенны. Поэтому итоговый статус — **accepted-with-gaps**, без гарантии абсолютной полноты по отсутствующим бинарным/host материалам.
