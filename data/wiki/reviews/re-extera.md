# Независимое ревью источника `fossSquad/re-extera`

- **Scope:** исходный код и документация репозитория `fossSquad/re-extera` на `master`, commit SHA `3be81ef0c25e842f3a8be669c235e783839c4716`.
- **Snapshot:** `snapshot.json` указывает этот SHA и `tree_truncated: false`; в `tree.json` 182 tree entries / 130 blob entries. Manifest теперь содержит 120 захваченных файлов; SHA-256 каждого локального файла совпал с manifest. Дополнительно получен `gradle/wrapper/gradle-wrapper.properties` именно для закреплённого SHA.
- **Вердикт:** `accepted-with-gaps`.

## Независимое покрытие

Сверены README, LICENSE и репозиторные метаданные; loader целиком (`metadata`, imports, constants, config, utils, plugin, dex и builder); Gradle configuration, Wrapper properties, ProGuard, manifest и GitHub Actions workflow; `Main`, `Defaults`, полный `hooks/**`, settings/UI/localization, database entities и `ReExteraDb`, `utils/**`, unit и instrumentation examples. Особое внимание уделено Python plugin callbacks, DEX classloader/update/cache paths, сохранению и снятию hooks, overload resolution, Telegram request callback behavior, account routing, background/UI/DB threads, SharedPreferences, CI artifacts и manual update paths. Чтение upstream Telegram/exteraGram кода и запуск исходников не выполнялись.

У дерева 130 blob entries; в текстовый manifest не входят `.gitignore`, `gradlew`, `gradlew.bat`, `gradle-wrapper.jar`, пять картинок README и бинарный `libs/exteragram.jar`. Wrapper properties получен отдельно и его distribution URL зафиксирован; launcher и JAR wrapper не анализировались. `libs/exteragram.jar` — compile-only host snapshot — не декомпилировался, поэтому он не подтверждает экспортированные host signatures или наличие SettingsRegistry в какой-либо конкретной сборке.

## Найденные ошибки и исправления

- Исправлен `re-extera-012`: `sendRequestInternal` содержит **четыре** callback/delegate параметра (`RequestDelegate`, `RequestDelegateTimestamp`, `QuickAckDelegate`, `WriteToSocketDelegate`), затем три `int`, `boolean` и последний `int`; раньше было ошибочно сказано «три типа delegate».
- Уточнён `re-extera-025`: SharedPreferences файл общий, ключи обычно не несут account id; premium-cache явно включает account id. Формулировка не приписывает всем настройкам проверенную per-account семантику.
- Слит повтор `re-extera-036` с `re-extera-026`. Теперь один fact описывает два optional class-name lookup и оговорку, что успешное разрешение зависит от внешнего host classpath.
- Исправлен `re-extera-031`: при наличии local DEX loader вызывает `start_from_bytes()` и безусловно возвращается; внутренние ошибки загрузки класса тот метод ловит. Следовательно, неудача может пропустить cache/download/update fallback. Источник страницы дополнен этой оговоркой.
- Исправлена provenance часть `re-extera-040`: `repository.json` — это сохранённый GitHub API metadata snapshot, а не файл Git tree; evidence path теперь указывает `raw/re-extera/repository.json` и capture time. README остаётся привязан к pinned commit.
- Дополнен coverage: Wrapper properties теперь включён в snapshot и список чтения.

После правок в source facts **43 уникальных fact ID**; дубликатов нормализованных topic/claim нет. У всех фактов проверены SHA, формат evidence path и существование файла/диапазона строк. `re-extera-026` — canonical topic для optional SettingsRegistry lookup; повторные похожие сведения в других источниках остаются отдельными provenance. Fork `SHAJON-404/re-extera` не смешивался с этим репозиторием.

## Radar provenance и версия клиента

Четыре commit URL из `radar-urls.json` независимо открыты на GitHub: [5a03579](https://github.com/fossSquad/re-extera/commit/5a0357902c243c18f08ef549908a2caddff3f25d) — создание regex из message context menu; [c8f2c29](https://github.com/fossSquad/re-extera/commit/c8f2c296affff9d08f9b72832b784d458ae1a25d) — flexible hook resolution и Local Premium; [d143386](https://github.com/fossSquad/re-extera/commit/d1433864637aa211103da9bf802a5d043ddd9020) — client-side reading toggle; [d8bfc48](https://github.com/fossSquad/re-extera/commit/d8bfc482894747b1c94753af113359d2f59e3fcc) — Filtered Posts и shortcuts из chat menu. Это исторический контекст; текущие claims опираются на код SHA `3be81ef…`.

Более широкое утверждение радара «активно адаптирован под ExteraGram 12.10.1» не подтверждено как совместимость этого pinned source: loader metadata задаёт только минимум `12.8.1`, а комментарий в `HookInit` сообщает об изменениях внутренних Telegram deletion signatures в `12.9.0`. Эти признаки не устанавливают поддержку конкретной сборки `12.10.1`. Исходная metadata API snapshot называет репозиторий `fork: false`; README называет его AyuGram feature port. Точный code ancestor в снимке отсутствует, поэтому feature lineage не представлен как построчно проверенный fork diff.

## Остаточные gaps

- Runtime/DexClassLoader, Python host bridge, hooks, callbacks, UI и настройки не запускались на клиенте; build, install и device tests не выполнялись.
- `libs/exteragram.jar` не декомпилирован, а точная целевая ExteraGram build не указана. Реальные host ABI, overload resolution, SettingsRegistry class/signature и совместимость с 12.10.1 остаются неподтверждёнными.
- Telegram upstream internals не изучались; указанные `org.telegram.*` signatures — намерения и reflection targets плагина, не стабильный SDK contract.
- Не делался security audit клиента/host. В просмотренных HTTP download paths loader не видно checksum/signature verification; это наблюдение ограничено указанными путями и SHA.
- Unit/instrumented tests являются примерами; их host hook/DEX lifecycle coverage не подтверждена и tests не запускались.

Исходник принят как статическое описание указанного commit с этими ограничениями; абсолютная полнота/совместимость для недоступного host-кода не утверждается.
