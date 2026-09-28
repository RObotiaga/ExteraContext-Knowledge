# Независимая проверка NiagramX

**Вердикт: `accepted-with-gaps`.** Проверенные утверждения соответствуют коду pinned-снимка; исправлены один пропуск о настройке VPN/proxy и дублирование факта о plugin API. Остаются статические проверки без запуска клиента/сборки и без проверки совместимости с конкретным plugin host.

## Снимок и область ревью

Источник: [`HSSkyBoy/NiagramX`](https://github.com/HSSkyBoy/NiagramX), ветка `dev`, SHA `f97133c55ff6594564b82fc6d2dffa74a960e639`, зафиксирован 2026-09-27. В [snapshot.json](../../raw/niagramx/snapshot.json) указано `tree_truncated: false`; полный tree содержит 29 814 записей. Сверены source page, radar context/URL list, `file-manifest.json`, исходники под `raw/niagramx/files/` и 27 записей `work/niagramx-facts.json`. Проверены хэши manifest для релевантных полученных материалов; отсутствующий в tree `gradle/libs.versions.toml` дал HTTP 404 и не является пропущенным tracked-файлом.

Независимо просмотрены README, LICENSE, `.gitmodules`, root и app Gradle-конфигурации, настройки NyaConfig и UI, PR/staging/release workflow, а также следующие subsystem-файлы:

- Audio и UI: `MediaController.java`, `ChatMessageCell.java`, `NotificationsController.java`, `NekoGeneralSettingsActivity.java`, `NekoChatSettingsActivity.java`, `NekoExperimentalSettingsActivity.java`, `NyaConfig.kt`, iOS sound resources.
- LLM translation: `Translator.kt`, `LLMTranslator.kt`, `TranslationCache.kt`, `LlmTransport.kt`, `LlmResponse.kt`, `GeminiNativeClient.kt`, `OpenAICompatClient.kt`, `UrlNormalizer.kt`, `PresetRegistry.kt`, `LlmConfig.kt`, `HttpClient.kt` и связанные settings/call-sites.
- Proxy/VPN: `ProxyUtil.kt`, `WebSocketHelper.kt`, `WebProxyManager.kt`, `ProxyRotationController.java`, `SharedConfig.java`, `ApplicationLoader.java`, `ProxySettings.java`, `libs/tcp2ws/README.txt`, build file и Java реализации tcp2ws.

Это целевое чтение собственных feature seams и интеграционных точек по радару, не построчное чтение 29 814 путей. Upstream-классы Telegram, JNI/WebRTC, сторонние зависимости и все UI-контракты целиком не проверялись.

## Радар, покрытие и точность

Сопоставлены radar-context, предоставленные URL и pinned-код. Три historical commit URLs проверены по GitHub: `b8c3db1` — настройка счётчика пересылок, `ee415d4` — input text animations, `fa093d9` — fastest proxy. Эти commit snapshots не использовались как доказательство поведения текущего SHA; функции Repeat One, локальной галочки, iOS sounds и LLM cache подтверждены отдельно кодом `f97133c…`. Указание радара на Python/Java hook оставлено идеей портирования, не API NiagramX.

Перепроверены API claims и line ranges всех source facts: все 27 evidence paths существуют, диапазоны строк входят в соответствующие файлы, версии совпадают с pinned SHA, идентификаторы уникальны. `MediaController.checkIsNextMusicFileDownloaded(int)` — приватный instance `void` метод; Repeat One guard идёт после download-policy/playlist checks и до вычисления следующего индекса и FileLoader-вызова. Таблица call-sites не представляет эти внутренние вызовы как plugin SDK. Статусы `docs`, `code` и `inference` использованы соответственно для README, реализации конкретного SHA и выводов из ограниченного участка кода; runtime-claims не добавлялись.

Проверка подтвердила локальность `HideReadReceiptsLocally` в вычислении drawable bitmask, выбор входного/исходящего SoundPool sample и сброс закэшированных IDs/loaded flags. В LLM-пути подтверждены context propagation, cache lookup до запроса, успешная запись очищенного результата, transport и prompt/key logging. В proxy-пути подтверждены VPN callbacks, авторство отключения/восстановления, account scope ping-вызовов, порог 80 ms и регистрация tcp2ws через внутренний proxy entry.

Найдены и исправлены:

- В разделе VPN/proxy не были указаны default и место настройки. Добавлено, что `DisableProxyWhenVpnEnabled` выключен по умолчанию, включается checkbox-ом в Experimental → Connections, а обработчик настройки немедленно вызывает `checkVpnState()`.
- `niagramx-001` и `niagramx-026` повторяли одно и то же утверждение об отсутствии описанного внешнего plugin SDK/lifecycle в README. Формулировка объединена в `niagramx-001`; дублирующий факт удалён.
- Для учета пропущенного default добавлен отдельный факт `niagramx-027` с pinned-ссылкой на boolean config. Бывший `niagramx-027` о приватности Repeat One метода перенумерован в `niagramx-026`.

Проверка повторов охватила факты страницы: local UI checkmark и сетевой read receipt оставлены как разные уровни; выбор звукового ресурса и инвалидирование SoundPool IDs являются разными шагами; VPN/proxy disable/restore и ping-based selection — отдельными механизмами. Сравнение со всеми каноническими темами других источников не выполнялось; возможные межисточниковые совпадения следует объединять на уровне topics с сохранением provenance.

## Остаточные gaps

- Нет сборки, тестов, runtime/network/device-проверок; source inspection не подтверждает фактическое поведение при гонках, VPN toggle, нагрузке tcp2ws или повторной загрузке SoundPool ресурсов.
- Не исследованы все providers, транспортные edge cases и пользовательские настройки LLM. Межпровайдерное совпадение cache key выводится из полей ключа, но collision в работе не проверялся.
- Не проверены доступность private-method early return в конкретном ExteraGram/KPM/DEX runtime и совместимость с их версиями. Снимок NiagramX не задаёт plugin lifecycle/API.
- Внешнее содержимое submodules не входит в снимок; release signing и реальный результат CI не проверены. README содержит build hints, которые отличаются от pinned Gradle/workflow значений; source page явно отдаёт приоритет конфигурации этого SHA.

После ревью остаётся **27 уникальных фактов**. Проверка статическая; verdict не является гарантией полноты по непрочитанным upstream и submodule-кодам.
