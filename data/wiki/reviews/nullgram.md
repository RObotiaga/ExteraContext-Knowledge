# Независимая проверка Nullgram

## Область и snapshot

Проверена только source page `wiki/sources/nullgram.md` и её 23 исходные карточки (`work/nullgram-facts.json`); по результатам добавлена одна отдельная карточка об ограничениях SOCKS5. Репозиторий `qwq233/Nullgram`, закреплённый commit `b3d4f45e1ebd1a15576b46f87172ce076cf390f1` (`master`), snapshot от `2026-09-27T15:57:17.807785Z`. Локальный `tree.json` содержит 30 706 записей и тот же SHA; SHA-256 всех 43 сохранённых файлов совпадает с `file-manifest.json`.

Назначение в радаре — клиент-донор networking: `raw/nullgram/radar-context.md:10` фиксирует добавление Nullgram `tcp2ws`, а `:32` описывает его как tcp2ws из Nullgram в NiagramX. Это мотивирует подробный разбор transport и точки интеграции в клиенте. Радарные исторические заявления о дате/первенстве не подтверждены этим snapshot; `radar-urls.json` пуст.

## Независимое покрытие

Прочитаны README на английском, китайском и японском языках, LICENSE, `docs/CONTRIBUTING.md`, оба workflow, Gradle settings/dependencies; целиком исходники `libs/tcp2ws` (`ProxyHandler`, `Socks4Impl`, `Socks5Impl`, `SocksConstants`, `Utils`, `tcp2wsServer`), README/NOTICE/LICENSE модуля; точки интеграции `WebSocketHelper`, `WsSettingsActivity`, `ConfigManager`, `Defines`, `Annotations`, KSP `ConfigSwitch`, `ConnectionsHelper`, `CloudStorage`, `BaseTranslator`, `TranslateHelper` и Google provider. Прочитан manifest и проверены все его 43 checksum. Весь upstream Telegram tree (30 706 entries) построчно не исследовался: граница соответствует донорской функции радара и выбранным практикам клиента.

Проверены точные method/API формы, control flow, defaults, retry, branch-specific SOCKS commands, frame options/headers, lifecycle и описания build workflow. Факты опираются на код pinned commit или явно помечены `docs`/`inference`; выполнение приложения, Gradle, CI, сети и runtime-компонентов не заявлено.

## Проблемы и исправления

- Уточнена карточка `nullgram-006`: UDP branch вызывается диспетчером, но `Socks4Impl.udp()` явно отказывает; SOCKS5 UDP code path создаёт `DatagramSocket`; BIND implementation закомментирована. Обновлены claim/API/evidence/recipe и описание source page.
- Добавлена карточка `nullgram-024`: SOCKS5 command parser отвергает ATYP `0x03`, а ATYP `0x04` уходит в `Inet4Address.getByAddress` с 16 байтами; helper ловит исключение и возвращает `null`. Это вывод из статического кода, не runtime-эксперимент. Добавлена строка API table и ограничение в source page.
- Уточнено описание translator cache: ключ — пара source object/target language; `BaseTranslator.translate` принимает строки и poll objects. HTTP client создаётся полем экземпляра базового класса и не подтверждён как глобальный singleton.
- Остальные карточки `nullgram-001..005`, `007..023` сверены по path/ranges из pinned snapshot. Отдельная проверка подтвердила module dependency, setter/call signatures, per-account request flow, preference/KSP contracts и исключительно декларативную природу CI steps. Публичным API плагина внутренние классы Nullgram не названы.

## Повторы

В исходных 23 карточках не было повторных ID или одинаковых утверждений: transport setup/lifecycle/relay, SOCKS command dispatch, configuration, account RPC и translation orchestration описывают разные аспекты. `nullgram-013..015` разделяют account scoping, удалённый bot protocol и чувствительное логирование — это разные выводы из одного файла. Совпадающие темы tcp2ws/networking с NiagramX и сетевыми plugin источниками являются независимыми provenance; для последующей тематической консолидации используйте `wiki/topics/network.md` и API карточки networking, сохраняя различия контрактов. Nullgram остаётся client implementation, не plugin SDK.

## Остаточные пробелы и вердикт

- Нет runtime evidence для SOCKS/WS протокола, DNS, TLS/custom endpoint, UDP, retry, bind-address exposure, listener shutdown и socket-pool races. Серверный socket создаётся без явного loopback bind; свободный ephemeral port выбирается по схеме reserve-close-rebind; listener использует per-client threads без видимого лимита, а `stop()` передаёт остановку через polling timeout.
- Полнота по upstream Telegram-клиенту намеренно не заявлена. Не исследовалась совместимость внутренних классов Nullgram с ExteraGram/AyuGram host plugin APIs; внутренние seams не являются доказательством plugin contract.
- Не устанавливались происхождение/исторический приоритет tcp2ws в NiagramX сверх тех утверждений, которые приведены во вторичном радаре.

**Вердикт: `accepted-with-gaps`.** Материал полезен как source-grounded пример Android-клиентской интеграции TCP-over-WebSocket, settings/config и coroutine/provider patterns. Он не документирует публичную систему плагинов и не доказывает runtime-работоспособность. Всего уникальных карточек после правки: **24**.
