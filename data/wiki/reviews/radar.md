# Независимая проверка radar corpus и source registry

**Вердикт: `accepted-with-gaps`.** Страница теперь отражает уникальные идентичности кандидатов и отделяет их от технологических упоминаний. Сам radar — вторичный отчёт, а не доказательство того, что каждый названный репозиторий, API или commit был действительно открыт и изучен.

## Scope и снимок

Проверены:

- `raw/radar.md`: 5 253 строки, SHA256 `B7074AEA3FB2D4A20367C3DB971856E93D617936558AD852CCD6099C74A73100`.
- `raw/radar-export.json`: 39 сообщений (8 user, 31 assistant), SHA256 `F76C499B06C688924AEBF5F4390298FE0C5E4C47C406A18313D8E52260297D24`.
- `raw/radar-export-text.md`: 5 512 строк, SHA256 `6DFDE68FF7AB9C8EA86528D4A8E67C36A46533292BB989BFDC170806B0848591`.
- `work/radar-source-candidates.json`: первоначальный список 73 кандидатов и 10 references; также проверены `work/repos.json`, соответствующие raw repository metadata, source page и source line ranges.

У радарного корпуса нет применимого Git tree/commit `tree.json`: это экспорт переписки и её текстовая проекция. SHA256 выше фиксируют точное содержимое файлов, доступное для этой проверки. Никакой API-сигнатуре или первичному implementation claim здесь не присвоен статус code/runtime-verified.

## Покрытие и изменения

Сопоставлены тематические диапазоны исходной страницы с corpus: ранние runtime/plugin кандидаты (1–779), каталоги, клиенты и SDK (780–1 863), срезы 11–22 сентября (1 864–5 010), поздние находки и MCP (5 011–5 253), а также добавленный диалог 26 сентября (`export:5176–5512`). Отдельно сверены прямые GitHub URL и URL-пути в экспорте: все самостоятельные GitHub repo URL, оставленные в сообщениях, отображены в реестре или как явно связанные альтернативные пути; `topics` URL не выданы за репозитории.

Реестр преобразован в **66 записей с 66 уникальными `canonical_source_id`** и 15 `non_source_references`. Каждая запись source candidate содержит `canonical_source_id`, `relationship` и `identification_status`. `non_source_references` сохраняет десять групп упомянутых зависимостей и пять платформенных/технологических ссылок; это не означает просмотр их самостоятельной документации.

Исправлены конкретные дубли и пропуски:

- ExteraGram official Plugin Docs и SDK/PySDK — одна source identity; версии документации и runtime в radar остаются раздельными утверждениями, поскольку датированы по-разному.
- KPM оставлен одной канонической записью. Codeberg и GitVerse связаны как зеркала, а `KangelPlugins/Plugins-Store` сохранён как legacy spelling/repository reference с неустановленным равенством. Зеркальная синхронность и тождество старого пути не доказаны.
- Потерянное имя skill в `export:5253–5255` сопоставлено с `fossSquad/exteraSkill`: точное совпадение GitHub description, тем `exteragram`, `ayugram`, `xposed` и времени обновления 31 июля 2026. Второй source candidate не создавался.
- Старый `n08i40k/exteragram-plugin-template` и `exteraStuff/pydex-plugin-template` сведены в один canonical record с прежним адресом как alias. Инвентарь указывает redirect, однако история репозитория и сохранность исходной истории не проверялись.
- В `cataIystdev/exteragram-mcp` добавлена отдельная запись npm distribution `@catalystdev/exteragram-mcp`. URL и версия 1.0.0 заявлены в radar; tarball, provenance и соответствие коду GitHub ещё нужно проверить.
- Beta4 APK Opexgram и `yearningss/opexgram-docs` beta6 представлены как разные источники. APK отсутствует; Telegram announcement подтверждает лишь часть описания. Beta6 docs не использованы как замена beta4.
- Добавлены или разрешены owner/repo: `DedyaSergey/Chat-Stats-Plugin`, `DedyaSergey/Smooth-Scroll-Plugin`, `cataIystdev/catalib`, `fossSquad/exteralib`, `Islite/AniList.co`; `qwq233/Nullgram` внесён как вероятный источник для `tcp2ws`, пока без точной привязки к path/commit.
- API Telegram/TLRPC, GitHub REST/Contents API, GitHub Actions, Gradle/Kotlin/R8 и названия ExteraGram/AyuGram как платформ перемещены в список контекста. Так они не создают ложное впечатление, что отдельные официальные docs/API были просмотрены.

## Повторы

Исходная страница уже отмечала повтор функций внутри радара: ViboGram ASCII art и text effects; Mercurygram drafts; Miogram Vault/AI/Presence; повторные клиентские feature/status checks; NiagramX media/proxy/UI. Они оставлены с единой темой и диапазонами сообщений — повторные ежедневные пересказы не считаются независимой проверкой факта. Идентичность ExteraGram docs/SDK и `fossSquad/exteraSkill` теперь также не дублируется как несколько источников. Разные версии, форки и платформы не слиты без доказательства общей истории.

## Остаточные gaps

- Точная идентичность `exteragram-utils`, air-raid-alert plugin и `NagramXTurbo` не установлена. `AyuGram Desktop PLEngine / plugin sample` упомянут без конкретного репозитория/URL. Эти четыре записи имеют unresolved canonical IDs и не дополнены догадками.
- `Nullgram` — вероятная, но не подтверждённая точная идентичность для `tcp2ws`; проверить файл/commit.
- Недоступный Opexgram beta4 APK остаётся непроверенным. Beta6 docs и Telegram-анонс не заменяют его.
- Проверка этого задания закрывает идентичность и полноту реестра radar corpus. Она не проверяет исходники перечисленных репозиториев и не подтверждает их API, функции, лицензии, состояние зеркал, публикацию пакетов либо совместимость с текущим APK. Для этого нужны отдельные пары по каждому реальному source artifact.

Полный нормализованный список, aliases и relationship/status поля находятся в [`work/radar-source-candidates.json`](../source-candidates.json); исправленная обзорная страница — [`sources/radar.md`](../sources/radar.md).
