# Независимое ревью: `fuckramochka/miogram`

**Вердикт:** `accepted-with-gaps`  
**Проверяющий:** `/root/review_miogram` · **модель:** `gpt-6-luna`  
**Закреплённый SHA:** [`8ce2a35dfc396a524e156eecc4797f0cd664c91d`](https://github.com/fuckramochka/miogram/tree/8ce2a35dfc396a524e156eecc4797f0cd664c91d)  
**Уникальных фактов после исправлений:** 38

## Объём независимой проверки

Проверена страница `wiki/sources/miogram.md`, все 32 исходных записи `work/miogram-facts.json`, исходный `tree.json` и `radar-context.md` с `radar-urls.json`. Snapshot сообщает 32 597 записей дерева; локальный file manifest содержит 78 выбранных файлов после независимого получения пропущенных первичных файлов. Сборка, приложение и тесты не запускались.

По pinned snapshot независимо прочитаны релевантные первичные материалы:

- `README.md`, `docs/PLUGINS_DEV_GUIDE.md`, `docs/ARCHITECTURE.md`, `docs/BUILD.md`, `docs/SECURITY.md`; Rust SDK `README.md`, `Cargo.toml`, `src/lib.rs`, `src/envelope.rs`, `examples/echo.rs`.
- Python manager и installation/security path: `PluginsController.java`, `PythonPluginsEngine.java`, `Plugin.java`, `PluginRuntime.java`, `PluginPermissions.java`, `PluginInstallHelper.java`, `PluginCapabilityScan.java`, `PluginAuditJournal.java`, `PythonBridge.java`, `plugin_loader.py`, `capability_scan.py`, `audit_gate.py`; Java hook bus и Forge classes.
- Полный найденный Kotlin `core/plugins` и `core/wasm` слой, `WamrWasmRuntime.kt`, `miogram_wasm.c`, `host_api.fbs`, CMake; relevant build files.
- Radar paths: `AmegramPatchManager`, `MiogramAntiBlockEngine`, `MiogramCloudVaultEngine`/`MiogramCloudVaultFile`, lyrics/player integration and online-halo call-sites.
- Radar feature paths: Smart Feed service/activity, Kanban activity/storage, split-chat/floating-chat service, `AndroidManifest.xml`, and the relevant `ChatActivity`, `DialogsActivity`, `LaunchActivity` call-sites.

## Проблемы, исправления и подтверждения

1. Coverage утверждала, что Kotlin `app.miogram.core.*` layer не найден, а комментарий `MiogramPluginsActivity` трактовался как факт отсутствия этого кода. Оба положения были исправлены: core engine, trust, capabilities и WASM contract существуют в этом pinned tree; комментарий alias противоречит физическому составу snapshot. Наличие слоя не приравнивается к его интеграции.
2. Проверенный Forge путь отправляет собранный `.wasm` в Exteraless `PluginsController`. Его `.wasm` ветви создают обычную запись `Plugin` и отмечают её loaded; вызова `MiogramPluginEngine`/`WamrWasmRuntime` в этом call path не видно. Это исправляет впечатление, будто наличие Forge build/import/catalog означает исполнение Rust module.
3. Добавлено описание отдельного core engine: `PluginSignatures` проверяет trust anchor и Ed25519 manifest signature, затем code size/hash; `PluginEngine` применяет operation/capability policy и quarantines plugin после трёх trap. Это вывод о коде, не о работающем продукте.
4. Исправлено неверное описание wire документации. Rust `envelope.rs` использует `MIOG`, SDK README и `docs/ARCHITECTURE.md` в том же snapshot ещё указывают `HYPR`; core `WasmRuntime` KDoc описывает FlatBuffers. `PluginEngine.dispatch` проверяет `op`, затем передаёт `payload` в `miogram_call`, но явный encoder для MIOG frame в проверенном dispatch path не найден. Совместимость частей поэтому не заявляется.
5. Уточнено, что C-комментарий «only trusted signed modules» — заявленная политика, а не доказанная гарантия JNI loader: `nativeLoadModule` получает байты WASM без manifest/signature; подпись проверяет другой core API. `WamrWasmRuntime.loadModule` не передаёт `SandboxConfig` native bridge, а `consumedFuelMs()` возвращает ноль. CMake опускает runtime без optional WAMR submodule; preemption отсутствует.
6. Добавлены пропущенные radar feature facts. Smart Feed реализует недельную выборку/Gemini digest с бюджетами prompt и raw fallback, но отдельный launcher не найден среди проверенных entrypoints; найденный пункт `News Feed` ведёт в другой Exteraless Feed. Kanban имеет локальную JSON/SharedPreferences storage и message references; split-chat имеет два `ChatActivity` view и меню-вызовы; floating chat выделен в overlay service. Описано только source-level поведение.
7. Обновлены доказательства и статус в fact records; записи `miogram-001..038` имеют уникальные ID. Точных повторов внутри страницы/JSON не обнаружено. Сходные темы с отдельными источниками Exteraless/Amegram остаются раздельными подтверждениями; при последующем тематическом слиянии подходят canonical topics: plugin manager/lifecycle, hook dispatch/capabilities, WASM trust and wire ABI, hotpatch integrity, AI feed, local task storage, Android UI overlays, Cloud Vault and media/player integration. Общий index/topics и другие source pages в этом ревью не менялись.

## Оставшиеся пробелы

- Не проверялись Android runtime, WAMR execution, SDK/NDK/Gradle build, CI, реальные Gemini/network/proxy ответы, patch manifest transport/signature, Cloud Vault пользовательский поток и window permission/lifecycle. В отчёте и странице нет утверждений `runtime-verified`.
- Проверена выбранная область из 78 файлов, а не все 32 597 файлов Telegram-клиента. Telegram upstream целиком исключён из scope.
- Entry point Smart Feed остаётся неопределённым в проверенных навигационных файлах. Не исследованы все возможные reflection/string-based launchers.
- Wire-format и подписной trust path между Forge, catalog manager, Kotlin core, JNI и Rust SDK остаётся несведённым; code presence не доказывает production installation/execution.
- Для hotpatch изучен `AmegramPatchManager`, но не весь удалённый manifest/repository/transport; отсутствие integrity gate в этом классе не доказывает отсутствие проверки в иных слоях.
- Несколько исходных утверждений основаны на документации и радаре; они сохранены как docs/secondary claims, не как подтверждённый runtime. Полнота не абсолютна для большого клиента и недоступных пользовательских сценариев.

Подтверждённые из кода сигнатуры, поведения и ограничения относятся только к указанному SHA. Проверка источников не заменяет build или device acceptance.
