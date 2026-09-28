---
type: source-review
source_id: amegram
reviewer: /root/review_amegram
model: gpt-6-luna
verdict: accepted-with-gaps
reviewed_at: 2026-09-28
accepted_facts: 42
---

# Независимая проверка fuckramochka/amegram

## Версия и граница проверки

Проверен `fuckramochka/amegram`, ветка `main`, snapshot SHA [`8a5819b6c931e661a73d422890fca995d0a7ff5b`](https://github.com/fuckramochka/amegram/tree/8a5819b6c931e661a73d422890fca995d0a7ff5b), captured 2026-09-27. `snapshot.json`, `repository.json` и `tree.json` указывают тот же репозиторий и SHA; дерево не усечено. Rадар описывает донорный Amegram и прежде всего Python/Xposed и новую Miogram plugin систему; `radar-urls.json` пуст. Изучались собственные extension/runtime subsystems и связанные точки входа, не весь Telegram upstream. Код и runtime не запускались.

Независимо проверены собранные 324 manifest-записи, включая полный custom `app.miogram` Java/Kotlin контур (129 Java и 42 Kotlin исходника по pinned tree), `app.exteraless.plugins`, его Python SDK, Rust SDK, WASM/FlatBuffers bridge, Forge, конкретные AI/STT реализационные классы и build/hotpatch/anti-block файлы. Для call-site проверки добавлены `MiogramPluginsActivity`, `PluginsController`, `MiogramInAppNotifications`, AI/feed/vault/userbot/preset/player call-sites и Android chat/UI integration files. Все приведённые GitHub-ссылки в source page закреплены на указанном SHA. В acquisition manifest есть три неудачных обращения к неверному/устаревшему пути; правильные Kotlin WASM runtime и UI `LaunchActivity` получены отдельно, эти ошибки не скрыты как missing code.

## Результат по покрытию и точности

- Источник описывает действующий legacy Python/Chaquopy/Xposed plugin path отдельно от MioHook и WASM core. Сигнатуры Python `BasePlugin`, Xposed bridge, Rust SDK и Kotlin engine сверены с pinned объявлениями. Расхождения `PLUGINS_DEV_GUIDE.md` с Python/Rust SDK оставлены как `docs` claims, а не смешаны с рабочими кодовыми контрактами.
- Существенно уточнена зрелость WASM: `MiogramPluginsActivity` в кодовом комментарии говорит, что WASM manager в этом дереве не поставлялся, а экран наследует Python plugin UI. `MiogramPluginEngine` в проверенной main/test области используется только в unit tests, причём тестовая runtime — `FakeWasmRuntime`. Legacy `PluginsController` принимает `.wasm` в каталог и отмечает entry загруженной, но не инстанцирует guest; Forge передаёт ему собранный `.wasm`. Это не working WASM execution path.
- Сериализация WASM не описана одной совместимой схемой: Rust SDK использует `MIOG`, architecture doc пишет `HYPR`, `host_api.fbs` объявляет FlatBuffers, общий `WasmRuntime` передаёт байты, а JNI только копирует их в guest. `MiogramPluginEngine.dispatch` применяет `op` для capability lookup, но не кодирует его в переданный payload. Поэтому исходное утверждение об уже работающем FlatBuffers/guest API было сужено до конфликта контрактов; `FakeWasmRuntime` tests этого не разрешают.
- Уточнены реальные MioHook seams. Внутренние производители dispatch обнаружены в уведомлениях, Smart Feed, AI/tool, cloud vault, preset и Apple Music. `MiogramHerokuManager` регистрирует pre-send listener, но соответствующий dispatch в tree идёт только через facade без найденного caller; UI/dialog dispatch тоже не подтверждён. Явный bridge от external plugin runtime к MioHook не найден, поэтому это нельзя цитировать как общий plugin SDK.
- LiteRT-LM/Gemini Nano/Gemma/Qwen implementation в просмотренном snapshot не найдена. Есть две раздельные STT реализации: legacy `AmegramLocalTranscriber` с Android recognizer/optional ONNX/Gemini fallback и новый `LocalSttEngine`. Последний требует backend attachment; фабрика его не подключает, `OnnxWhisperTranscriber` нигде в main source не создаётся, а call-site transcriber API не найден. `LocalSttEngine` catalog SHA-256 null и register path проверяет размер, не hash. Добавленные факты отделяют эту кодовую/roadmap поверхность от production-ready inference.
- Hotpatch вывод подтверждён: startup wiring существует; bytecode patch скачивается и вызывается через `DexClassLoader`. В менеджере не найдена подпись/hash проверка, JSON `min_version`/`max_version` не enforce-ится. Это удалённое выполнение DEX из HTTPS endpoint; код просмотрен статически, безопасность endpoint/runtime не проверялась.
- Anti-block тезисы ограничены тем, что подтверждается исходниками: observer wiring, TCP probes/DC checks, таймауты и эвристика. Утверждения об эффективности обхода сетевой цензуры оставлены как не проверенные runtime claims.
- Build prerequisites помечены как документация; сборка, устройство, native WAMR availability, тесты и сетевые прогоны не запускались.

## Факты и повторы

Было 39 фактов, после исправления зрелости WASM, production call-sites MioHook и разделения параллельных STT путей — 42 уникальных ID. Проверены уникальность ID и непустые pinned evidence. Повторы внутри страницы/JSON не обнаружены: engine policy (023–027), engine wiring gap (040), observed event call-sites (041) и protocol mismatch (025–026) описывают разные утверждения. Перекрывающиеся Python/Xposed сведения с `exteraless`/Miogram источниками относятся к отдельным репозиториям и должны сохранять отдельный provenance; canonical темы для последующего синтеза — plugin lifecycle, Java hooks, WASM protocol/security, hotpatch supply chain, local inference readiness.

## Остаточные пробелы

- Не каталогизированы все Python callback-ы и все subtleties manifest/permission/install/scan UI; область намеренно ограничена API и главными lifecycle/bridge points. Ревью не является полным справочником для всего Exteraless-derived runtime.
- Проверка MioHook dispatch завершена по custom app source, но не прослежен каждый upstream Telegram call-site `MiogramHookManager` facade за пределами захваченных integration files. Отрицательные результаты call-site поиска не являются runtime доказательством.
- Не проверялись WAMR submodule checkout/build guards и фактическая загрузка native symbols на устройстве. Rust/Go generated guest frames и host schema не запускались совместно.
- Не изучались веса/реальные model assets и production transcription flows на устройстве; остаётся неопределённым, есть ли внешний/reflection caller для legacy transcriber.
- Эффективность anti-block, удалённого DEX endpoint и trust model hotpatch требуют отдельной сетевой и operational проверки; здесь подтверждены только статические механизмы и отсутствующие проверки в изученном manager.
- Полный Android build, test suite, ELF alignment, APK installation, plugin catalog lifecycle и AI inference не выполнялись.

Вердикт: **accepted-with-gaps**. Страница и 42 факта пригодны как pinned static reference при явной маркировке не поставленного WASM runtime, несогласованного wire contract, STT backend gaps и непроверенных operational claims.
