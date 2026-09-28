---
type: source
source_id: packit
platform: Android
review_status: accepted-with-gaps
review: ../reviews/packit.md
date: 2026-09-28
---

# shareui/packit-source — большой плагин-каталог как пример клиентских интеграций

Источник: [shareui/packit-source](https://github.com/shareui/packit-source), снимок commit SHA `01e9673c49b9a44929fe017b61b664fbaaaa159e` (ветка main, локальный snapshot получен 2026-09-27). `raw/packit/tree.json` содержит этот requested commit SHA в поле верхнего уровня `sha`; это поле не является отдельной проверкой корневого Git tree object SHA. В рекурсивном дереве 430 записей: 341 blob-файл и записи каталогов; manifest содержит 276 скачанных файлов, и SHA-256 всех локальных файлов совпадает с manifest. При независимой проверке по pinned SHA дополнительно получены `libs/libexport/crypto.hpp`, `libs/libexport/exportbin.hpp` и `packit/LICENSE`. [Страница первичного GitHub-коммита](https://github.com/shareui/packit-source/commit/01e9673c49b9a44929fe017b61b664fbaaaa159e) подтверждает Watcha (#308): обновление stats/версии, YAML-локали и исправления deeplink операций. Метаданные снимка указывают GPL-3.0; вложенный `packit/LICENSE` также содержит текст GPLv3. packit/meta.yml объявляет plugin ID shareui_packit, версию 1.0.0-dev.1, минимум приложения >=12.9.0 и SDK >=1.4.5.0; это требования именно этого снимка PackIt, а не всей платформы.

Роль источника — production-пример большого Python-плагина с собственными экранами, клиентскими интеграциями, DEX/native мостами, сетевым каталогом и parser. Он полезен как образец архитектуры и call-site, но его внутренние модули не являются публичным SDK ExteraGram. Код изучался статически; установка на устройстве, runtime hooks, загрузка нативных библиотек и CI не запускались.

## Покрытие снимка

| Изученные пути | Что извлечено | Граница покрытия |
|---|---|---|
| README.md, CONTRIBUTING.md, refmap.yml, packit/meta.yml, LICENSE | назначение, структура, entrypoint, metadata, GPL-3.0 и правила вклада | заявления README/CONTRIBUTING не являются runtime-проверкой |
| .github/workflows/build.yml, .github/workflows/kotlin-build.yml, scripts/linux/kotlin-build.sh, scripts/linux/build-native.sh | CI сборки .eaf, проверка архива, единый DEX, ABI-разделение native .so | workflow и скрипты прочитаны как данные, не запускались |
| packit/src/python/BasePlugin.py, Main.py | lifecycle entrypoints, startup composition, hooks, message hook, unload cleanup | совместимость с конкретным установленным APK/SDK не проверялась |
| packit/src/python/core/Core.py, core/RepositoryManager.py, core/DexLoader.py, core/NativeLoader.py | установка, зависимости, cache/hash call-sites, repository lifecycle, Python↔Java bridge | классы client API за этими call-sites не специфицируются |
| packit/src/python/network/Storage.py, utils/CachedRepos.py, utils/InstallIndex.py, utils/HashUtil.py | HTTP-граница, форматы каталога, локальный cache, индекс, hashing | серверы репозиториев и downstream installer отдельно не проверялись |
| packit/src/python/integrations/hooks/SettingsActivityHook.py, UniversalFragmentFix.py, deeplinks/DeepHandler.py | отражательные hooks и маршрутизация tg://packit | изучены именно эти интеграции, не все integrations/** |
| packit/src/python/scl/{Scl,Native,Doc,Opts,Value}.py, packit/docs/scl/{api-docs,lang-docs}.md, libs/libscl/** | Python ctypes binding к native SCL, владение документом, типы и сериализация | native код не компилировался, документация не проверялась runtime |
| packit/src/python/ui/plugins/sheets/AISearchSheet.py, ui/plugin/VersionPicker.py, deeplinks/Install.py | каталог, версия/история и связанные AI/deeplink call-sites | клиентский запрос AI и UI/install поведение не запускались; каталог и модель отправляются внешнему API по коду |
| packit/src/python/integrations/chat/export/bin/{Writer,Reader}.py, libs/libexport/{crypto.hpp,exportbin.hpp,crypto.cpp,exportbin.cpp,exportbin_api.cpp} | экспортируемые блоки, C/ctypes граница и формат `.packit` v3 | криптография и ошибки просмотрены только статически; тесты и реальный import/export не запускались |
| packit/src/python/ui/icons/**, ui/files/**, integrations/chat/export UI, ui/achievements/**, прочие UI и integrations | границы модулей по CONTRIBUTING и дереву; отдельные выбранные call-sites | полный разбор icon/font flows, экранов импорта/экспорта, достижений и всех integrations не выполнялся |

В pinned tree 430 записей (341 файл); manifest содержит 276 файлов, включая скрипты сборки. Контрольные суммы захваченных файлов совпадают с manifest. Остальные 65 blob-путей в основном являются собранными DEX/`.so`, ресурсами и несколькими вспомогательными файлами; собранные артефакты не запускались. В дереве не найден каталог тестов. Это не доказывает отсутствие ручных или внешних runtime проверок самого проекта.

## Подтверждённые контракты и техники

### Entry point и lifecycle

refmap.yml указывает ElyxBuilder на packit/src/python/BasePlugin.py. В нём Main(BasePlugin) делегирует конструктор в Main.startInit, а on_plugin_load, on_plugin_unload, create_settings и on_send_message_hook(account, params) — внутренним функциям Main.py. Так entrypoint остаётся тонким, а startup и UI вынесены из класса загрузчика. Здесь подтверждены названия callbacks и call-sites исходника, но не полная спецификация конкретной версии SDK.

startInit(plugin, launchStart) создаёт RepositoryManager, PackItCore, chat UI, settings builder и badge manager, а также заводит поля для hook references. loadPlugin(plugin) выполняет основную инициализацию: локальный конфиг, очистку install index, подготовку декораций/ачивок, обновление repository caches и подключение integrations. Сетевые задачи в проекте уходят в background thread/serial I/O, изменения Android UI вызываются через run_on_ui_thread. Это пример разделять раннюю инициализацию, фоновую работу и Android UI.

В видимом on_plugin_unload очищаются badgeManager и сохранённый autocomplete constructor hook. loadPlugin устанавливает также другие hooks; изученная unload-функция явно их не перечисляет. Это остаточный вопрос для независимой проверки: нельзя утверждать, что они не снимаются библиотекой или другими компонентами.

### Модульная раскладка

CONTRIBUTING разделяет ui/ (собственные экраны), integrations/ (код внутри экранов клиента), core/, network/, utils/, scl/ и deeplinks/. Новая settings page помещается в ui/settings/subsettings/; вмешательство в client chat/chat list/profile — в integrations/<area>/; hooks клиентских классов — в integrations/hooks/; route tg://packit — в отдельный модуль с регистрацией в DeepHandler.py. Папки именуются lowercase, модули PascalCase, imports Python внутри пакета относительные. Это правило структуры данного репозитория, не обязательный layout SDK.

Документ предписывает использовать network/Storage.py как единую HTTP-границу, а utils/CachedRepos.py — для чтения локального reposCache/{rm_rid}.json. Пример в CONTRIBUTING получает URL через CachedRepos.plugins_url(repo), затем вызывает Storage.fetch_plugins(url) вне UI thread. Приём уменьшает дублирование сетевых политик и парсинга форматов.

### Hooks и deeplinks

setup_settings_activity_hook(plugin) находит org.telegram.ui.SettingsActivity, отражением выбирает fillItems(ArrayList, UniversalAdapter), вставляет UItem с ID 880099 после ExteraGram строки (id == -1), проверяя, что собственный item ещё не вставлен. Click hook подавляет штатный обработчик через param.setResult(None), затем на UI thread открывает PluginSettingsActivity. Методы фабрики и adapter выбираются по имени и количеству аргументов; это эвристика, уязвимая к изменениям client ABI, а не устойчивый контракт.

setup_deeplink_hook отражением ищет LaunchActivity.handleIntent с конкретной семиаргументной сигнатурой. PackItDeeplinkHook принимает ACTION_VIEW с URL tg://packit..., останавливает исходный вызов через param.setResult(None) и маршрутизирует URL на UI thread в набор внутренних handlers. proceed_deeplink в этом снимке очищает сохранённые intent/param ссылки; не следует трактовать это как универсальный способ продолжить исходный client intent.

### Репозитории, сеть и установка

Repository Manager хранит repositories в Elyx settings. В карте репозитория обязательны repometa.rm_rid, а добавление по URL также требует rm_name. При refresh некорректные ответы missing repometa/missing rm_rid удаляют запись; сетевые или parse errors сохраняют запись и прежний cache; повторяющиеся rm_rid удаляются. Так разделены ошибки источника и временная недоступность.

Storage.fetch_json(url, timeout=15) возвращает (data, error), посылает общий User-Agent и переводит HTTP status в человекочитаемую причину. Для списков плагинов и иконок timeout по умолчанию 20 секунд. normalize_entries сводит поддерживаемые формы plugins/icons к списку словарей: object с ID в ключах и array объектов с собственным id. Экраны каталога используют общий адаптер вместо собственной реализации этого разбора.

install_plugin(plugin_info, ...) сначала показывает dependency sheet для непустого поля deps; затем _do_install загружает файл в daemon thread. Сеть читается chunk-ами, обновления прогресса и UI идут через run_on_ui_thread. Расширение временного файла выбирается по tag Elyx: .eaf направляется в Elyx engine, иначе .plugin — в Python engine. Это конкретная реализация PackIt, а не API установки для сторонних плагинов.

При cache hit существующий архив сверяется через matchesStoredHash; mismatch вызывает повторную загрузку. После сетевого скачивания видимый _do_install использует hash/bithash как условие best-effort записи в cache, но прямого вызова matchesStoredHash для только что скачанного временного файла перед показом client installer в этой функции нет. Неизвестно, делает ли такую проверку downstream installer; целостность сетевого архива этим фрагментом не подтверждена.

Затем `_open_install_dialog` передаёт путь к временному файлу в `PluginsController.showInstallDialog`; для Elyx сначала проверяет engine по файлу и при отсутствии подходящего engine пробует прямой `ElyxEngine.showInstallDialog`. Код `PluginsController`/`ElyxEngine` не входит в этот репозиторий и не захвачен в snapshot, поэтому его проверку подписи/hash, разбор архива и фактическое поведение UI установить по PackIt нельзя. Это статический call-site, не доказательство поведения installer-а.

### AI-поиск и история версий

`AISearchSheet` строит текстовый каталог из имён и описаний загруженных плагинов, добавляет пользовательский запрос и отправляет оба значения в `generativelanguage.googleapis.com` методом `models/{model}:generateContent`, а API key передаёт в заголовке `x-goog-api-key`. В коде есть локальный cache результатов по модели и нормализованному запросу. Это описание фактического сетевого call-site в snapshot, а не проверка доступности Gemini, заявленного качества поиска или политики обработки данных Google.

`VersionPicker._build_version_entries` собирает latest entry и элементы `plugin.versions` с link/raw и `app_version`; UI позволяет выбрать совместимую версию и вызывает тот же installer с подменёнными link/version. Старым версиям без известного hash код присваивает `hash` и `bithash` со значением `Outdated`, поэтому это sentinel-значение, не digest. Deep link `tg://packit?install&repo=…&plugin=…&version=…` разрешает ровно выбранный plugin/version, проверяет app-version и при несовместимости пытается предложить best compatible entry. Эти детали относятся к версии PackIt по pinned SHA.

В plugin-deeplink ветке Install.py после загрузки manifest вызывается `install_plugin(plugin, all_plugins=all_plugins)` без `rm_rid=repoId`, хотя маршрут знает `repoId`. Core по умолчанию получает пустой `rm_rid`, а `InstallIndex.commit_pending()` при пустом ID пропускает запись; это статический вывод по двум call-sites о том, что этот deeplink-путь не связывает установку с repository ID во внутреннем PackIt index. Он не доказывает, что host installer не установил сам plugin, и не проверялся runtime.

Для файлового экспорта `Writer.build_binary` всегда включает `installDate` и опционально `achievements`, `localConfig` и `saved_plugins`; native codec записывает контейнер PCKT v3 с ChaCha20-Poly1305, а HKDF-ключ выводится из user ID и install timestamp. Reader получает блоки через ctypes API, после успешного чтения передаёт их на восстановление config-файлов и слияние achievements. `packit_read` игнорирует install timestamp hint и использует timestamp из внешнего заголовка как AAD/KDF input. Формат и call-sites подтверждены кодом; совместимость и сохранность данных реальным backup/restore не проверялись.

`urandom_rng` обычно читает nonce из `/dev/urandom`, но при неудаче `open` использует xorshift с фиксированным seed. Так как ключ стабилен для того же user ID/install timestamp, повторный экспорт при таком fallback, в том числе после перезапуска процесса, может повторно использовать ChaCha20-Poly1305 nonce. Это условный статический риск fallback-ветки, а не свидетельство, что на Android она срабатывает; безопаснее завершать операцию ошибкой при недоступности криптографического источника случайности.

InstallIndex использует блокируемый singleton _pending: set_pending(plugin_info, rm_rid) записывает данные перед install dialog, commit_pending забирает/очищает pending под lock и затем находит итоговый файл по plugin ID для PackIt-индекса. purge_missing при старте удаляет записи, у которых нет локального файла либо известный hash не совпадает, и убирает связанные записи ignore_list. Это внутренний индекс PackIt, не формат PluginsController.

### Kotlin/Java, native и SCL

DexLoader загружает единый packit.dex через InMemoryDexClassLoader(ByteBuffer.wrap(data), context.getClassLoader()), кэширует loader и загруженные классы и вызывает Kotlin static methods reflection helper-ом. Комментарий к коду связывает in-memory loading с Android W^X: writable dex через DexClassLoader может быть запрещён. Kotlin build script собирает один DEX с keep rule для kawaii.packetik.**; native .so собираются отдельно по ABI. В комментариях DexLoader указан API 26+, а metadata приложения указывает минимум 12.9.0; это не device matrix.

Пакет scl — собственная Python ctypes обёртка над libscl.so, не SDK Elyx/ExteraGram. parse(src, opts=None) и parseFile(path, opts=None) переводят ответ C API в Doc, копируют предупреждения и освобождают структуру результата; при ошибке поднимается ParseError. Doc поддерживает context manager и освобождает native document в __exit__/__del__; Value хранит ссылку на owning Doc, но перестаёт быть валидным после его освобождения. Документация рекомендует with scl.parse(src) as doc.

SCL docs описывают обязательную директиву @scl 1, типизированные поля, optional values, typed lists/maps, structs, enums, unions и constants. Python API Doc предлагает get/getPath/keys/items, serialize/toJson/toToml, Doc.new, newList и newStruct. toToml может поднять TomlError для типов, которые нельзя представить в TOML. Это формат и binding, использованные PackIt для своих данных/экспорта; поддержка SCL сторонними plugin loaders не подтверждается.

### Сборка и диагностика

.github/workflows/build.yml закрепляет Python 3.11 и ElyxBuilder==0.6.1, запускает elyb build -c 2 -v -nf, затем проверяет единственный .eaf, корневой refmap.yml, существование метainfo path и непустые поля id/name/version. Workflow предупреждает, что GitHub Actions artifact является ZIP-обёрткой, а не устанавливаемым .eaf. Сборка workflow в этом исследовании не запускалась.

CONTRIBUTING требует использовать packutil.logx: isDebug=False для ошибок, True для нормального потока, скрытого без Debug Logs. Пользовательский UI-текст хранится в четырёх синхронных локалях. Это локальное правило PackIt, не универсальный logging API.

## Call-sites

| Модуль/класс | Сигнатура или call-site | Назначение/lifecycle | Поток и account | Permalink |
|---|---|---|---|---|
| BasePlugin.py · Main | __init__, on_plugin_load, on_plugin_unload, on_send_message_hook(account, params), create_settings() | Elyx entrypoints делегируют в Main.py | lifecycle callbacks; hook получает account, в его видимой логике account не используется | [BasePlugin.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/BasePlugin.py#L14) |
| Main.py | startInit(plugin, launchStart), loadPlugin(plugin), on_plugin_unload(plugin) | создание managers, регистрация integrations, часть cleanup | startup/lifecycle; hook refs сохраняются в объекте plugin | [Main.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/Main.py#L44) |
| SettingsActivityHook.py | setup_settings_activity_hook(plugin); plugin.hook_method(method, hook) | settings item, click, cell bind и tint | client UI hooks; click маршалится в UI thread | [SettingsActivityHook.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/integrations/hooks/SettingsActivityHook.py#L51) |
| DeepHandler.py | before_hooked_method(param), setup_deeplink_hook(plugin) | фильтр ACTION_VIEW и обработка tg://packit | LaunchActivity; handlers запускаются через UI thread | [DeepHandler.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/deeplinks/DeepHandler.py#L36) |
| RepositoryManager.py | addRepositoryWithUrl(url), updateAllCaches(on_complete=None) | валидация repomap, обновление repository list/cache | background task; аккаунт не параметр | [RepositoryManager.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/core/RepositoryManager.py#L85) |
| Storage.py | fetch_json(url, timeout=15), fetch_repomap(...), fetch_plugins(...), fetch_icons(...) | общая HTTP-граница и payload normalization | только сеть; CONTRIBUTING запрещает UI thread | [Storage.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/network/Storage.py#L80) |
| Core.py | install_plugin(plugin_info, ...), _do_install(...), install_plugin_silent(...) | dependency prompt, загрузка и передача installer | download daemon thread; UI через run_on_ui_thread; account не параметр | [Core.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/core/Core.py#L119) |
| Install.py | handle(url, repoManager), _handleInstallPlugin(...), _handleInstallIconPack(...) | allowlist deeplink parameters, version resolution, compatibility branch and icon-pack install | network work on queue; final install dispatched to UI | [Install.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/deeplinks/Install.py#L48) |
| VersionPicker.py | _build_version_entries(plugin), _show_version_picker(...) | latest/history rows, compatibility state, historical artifact selection | UI callbacks; chosen entry is forwarded to installer | [VersionPicker.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/ui/plugin/VersionPicker.py#L50) |
| AISearchSheet.py | _build_plugins_file_content(plugins), _call_gemini(apiKey, model, pluginsCatalog, userQuery) | remote AI ranking of plugin catalog | background request; catalog and query go to Gemini | [AISearchSheet.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/ui/plugins/sheets/AISearchSheet.py#L157) |
| InstallIndex.py | set_pending(plugin_info, rm_rid), commit_pending() | связать client install с repository ID во внутреннем индексе | pending защищён threading.Lock; account не указан | [InstallIndex.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/utils/InstallIndex.py#L122) |
| DexLoader.py | _dexLoader(context), _loadClass(className, context), _callStatic(cls, method, *args) | Python→DEX→Kotlin bridge | context host app; loader/class cache в module | [DexLoader.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/core/DexLoader.py#L30) |
| scl/Scl.py · Doc.py | parse(src, opts=None), parseFile(path, opts=None), Doc.getPath(path) | ctypes binding и document API | синхронно; account неприменим | [Scl.py](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/scl/Scl.py#L25) |

## Ограничения и противоречия радара

- Radar приписывает PackIt обновление rich messages 22 сентября и одновременно говорит о последнем push 7 сентября. Репозиторные metadata действительно фиксируют pushed_at=2026-09-07, а pinned commit 01e9673 описан как изменение YAML локалей и deeplink-операций. Это не подтверждает radar claim о сентябрьском rich messages fix; возможно, речь о другом commit/source либо даты в радаре несогласованы.
- README утверждает «best interface»; это субъективное заявление проекта. Код AI search подтверждает сетевую интеграцию с Gemini, но не качество, доступность модели, настройки ключа на устройстве и фактическую обработку данных сервисом.
- Вывод downstream-проверки hash загруженного plugin archive остаётся открытым; нужен отдельный разбор installer и фактической политики repo.
- Не разобраны построчно все UI/decorations/chat hooks, icon/font workflows, полные export/import UI paths и achievements. Статически прочитаны codec и Python Writer/Reader call-sites, но не вся consumer UI и не совместимость с ранее опубликованными backup-файлами. Не изучена реализация host PluginsController/ElyxEngine за install call-sites. Нет device/runtime результата и локального прогона CI; эти ограничения сохраняются после независимой статической проверки.
