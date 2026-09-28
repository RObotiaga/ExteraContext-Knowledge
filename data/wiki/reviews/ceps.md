# Независимая проверка: m4rker20-rgb/CEPS

- Вердикт: **accepted-with-gaps**.
- Объём: единственный назначенный источник `m4rker20-rgb/CEPS`, закреплённый commit `8c1a4dc70387d782e012732f3868317851414012`; работа охватывает `wiki/sources/ceps.md` и `work/ceps-facts.json`. Сверялись `snapshot.json`, полный `tree.json`, `file-manifest.json`, исходники CEPS builder/runtime/installer и тестов, корневой и внутренний README, LICENSE, SECURITY policy, минимальный example и встроенные docs по lifecycle/hooks/settings/account/thread/client/file/dependency интеграциям.
- Идентичность снимка: SHA в snapshot совпадает с SHA tree и permalink файлов. Tree не усечён: 56 blobs и 9 записей каталогов. Manifest содержит 55 файлов; SHA-256 и наличие каждого локального файла из manifest проверены чтением снимка, ошибок нет. Единственная отсутствующая запись tree — `.gitignore`; она не нужна для описанных API, но могла бы подтвердить defaults ignore-файла.
- Ограничение охвата: CEPS-specific builder, loader, security, packaging и CI исследованы по сохранённым исходникам. Из большого приложенного справочника SDK проверены relevant-интеграции и точечные API-разделы; справочные страницы `class-proxy`, `intents`, `text-formatting`, `bulletin-helper`, части `file-utils` и Elyx-разделы не каталогизировались целиком, поскольку это самостоятельные host/Elyx API и не реализация CEPS. Это оставлено как явный gap, а не выдано за полную проверку всех API ExteraGram.
- Ничего из README не запускалось; команды, сборка, тесты, установка и Android runtime не выполнялись. Проверка статическая. Нет криптографического аудита реализации или подтверждения поведения на целевой сборке приложения.

## Независимая сверка покрытия

1. **Builder и CLI.** Сверены конфиг/defaults, `new`, keygen, file selection, builder pipeline и артефакты, `watch` fingerprint/`--once`, `verify`, selftest, env collector, Python 3.11 compilation, obfuscation/guard paths и Elyx wrapper. README claims отделены от реализации. Конкретный CLI содержит `keygen`, `new`, `build`, `watch`, `verify`, `selftest`, `collect-env`.
2. **Формат и loader.** Сверены структура manifest/chain, подпись Ed25519, Merkle и delivered-file hashes, файловая схема ChaCha20/`enc_v2` HMAC, structural versus payload verification, CEPS-3 env slots/KDF/fallback, anti-debug, guard seals, unmarshalling, proxy callbacks, cache materialization и optional in-memory DEX.
3. **Installer и граница SDK.** Сверены оба installer представления (`installer_template.py`, generated `ceps_installer.py`) и сборщик generated файла. `FilesController`, `FileInfo`, `BasePlugin`, hooks, settings, client queues/request/account helpers — контракты host/client из приложенных docs, а не CEPS runtime API; документационное описание не считается runtime-проверкой. Proxy callbacks в CEPS runtime ограничены перечисленными lifecycle/settings/request/update/send callbacks.
4. **Сборка и CI.** Workflow закрепляет Ubuntu/Python 3.11 и запускает glob `CEPSbuilder/test_*.py`; `test_env311.py` ищет жёстко заданный Windows CPython 3.11.15 под `%APPDATA%`. Это достоверное статическое несоответствие, но результат CI не проверялся.
5. **25 исходных facts.** ID уникальны и все 25 claims различаются по смыслу; точные локальные evidence paths и commit permalinks сверены выборочно по реализации и docs. Исправлены две неточности: expected guard seal сверяется только когда builder вшивает его для `--rt-pyc`; `ceps_dex` возвращает данные лишь если DEX найден и иначе равен `None`. Добавлен `ceps-026` про default `embed_shares` и отказ installer для обычного `.ceps` без shares. Итог: **26 уникальных facts**.
6. **Повторы и канонизация.** В JSON нет дублирующих fact IDs или одинаковых контрактов, которые следует схлопнуть. Общий текст source page повторяет структурированные facts как объяснение и не создаёт вторых записей. Hook/lifecycle/account/settings/thread/client API совпадают по теме с независимой страницей `official-sdk` и другими SDK-derived источниками: сохранять CEPS как отдельное provenance. Темы для последующей канонической агрегации: `topics/build.md`, `security.md`, `distribution.md`, `hooks.md`, `lifecycle.md`, `accounts.md`, `threading.md`, `ui.md`, `storage.md`, `testing.md`; эти общие страницы в рамках назначенного source review не менялись.

## Исправления в source и facts

- Уточнено, что `EXPECTED_GUARD_SEAL` сравнивается только в builder output с `--rt-pyc`; обычный source runtime начинает с `None` и пропускает эту вторую проверку. Уточнён порядок: optional anti-debug запускается до чтения архива.
- Уточнено, что `ceps_dex` — optional callable в payload namespace и может быть `None`.
- Добавлено ограничение installer для `embed_shares: false` в обычном archive flow; для env-архива действует отдельная structural-verification ветвь.
- Обновлена таблица покрытия: указаны проверка целостности 55 сохранённых файлов и исключение `.gitignore`.
- Frontmatter source page обновлён ссылкой на этот review и статусом `accepted-with-gaps`.

## Остаточные gaps и ограничения

- Не получен `.gitignore`; выводов о нём не делается.
- Справочник SDK в репозитории шире CEPS-интеграционного scope. Ряд независимых Java class proxy, intents, text formatting, bulletin, Elyx API и отдельные file utility методы не каталогизированы полностью.
- Упакованный SDK reference — docs, не код ExteraGram/plugin engine; совместимость сигнатур и поведения с какой-либо установленной версией runtime не подтверждена.
- GitHub Actions не исполнялся. Python 3.11 workflow mismatch основан на статическом чтении двух файлов.
- Не выполнялись Android/Chaquopy checks, install flow, тесты, сборка и криптографическая проверка; абсолютная полнота и runtime security не заявляются.

Итоговая страница источника: [`../sources/ceps.md`](../sources/ceps.md). Машинные факты: [`карточка фактов`](../facts/ceps.json).
