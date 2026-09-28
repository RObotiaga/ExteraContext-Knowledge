# Независимая проверка: Kangel-Plugins/ElyxBuilder

**Вердикт: `accepted-with-gaps`.** Проверена ревизия `b6db59093324dc5148f811c9058a6c1414fbb849` (`main` на снимке); в `package/pyproject.toml` указана версия `0.6.3.2`. Локальные `raw/elyxbuilder-kangel/{snapshot,repository,tree}.json` подтверждают репозиторий и SHA; tree не усечено. В дереве 47 blob-файлов, в file manifest получено 46; единственный недостающий blob — `.gitignore`. Проверялась только Kangel-Plugins/ElyxBuilder, выводы страницы `shareui/ElyxBuilder` не принимались за его контракт.

## Независимое покрытие

Сверены назначение и ссылки радара (`raw/elyxbuilder-kangel/radar-context.md`, `radar-urls.json`): оба ElyxBuilder названы для сравнения build tools, контрактов Kangel радар не задаёт. Прочитаны README, LICENSE, `package/README.md`, `package/pyproject.toml`, `package/src/config.json`; все документы `docs/en/` и `docs/ru/`; CLI и исходники `package/src/cmds/` (включая `components/`), а также lexer, AST nodes, parser и ошибки в `package/src/elyxdsl/`. По `tree.json` и manifest проверены все пути и пропуск `.gitignore`.

Покрытие охватывает scaffold/refmap/metadata/locales, CLI dispatch, обычный ZIP и шифрование, filters/ignore lists, AST check, compile/cache, obfuscation/mapping/stubs, watch, stats, version и script/DSL call-site. Тридцать исходных facts имеют по одному уникальному ID и уникальной формулировке; evidence paths и pinned SHA сопоставлены со снимком. Build/CLI/runtime команды не запускались. Релевантные точные файлы: `package/src/cli.py`, `package/src/cmds/{new,build,obfuscate,watch,cached,ignore,stats,script,version}.py`, `package/src/cmds/components/{progress,rawterm}.py`, `package/src/elyxdsl/{lexer,ast_nodes,errors}.py`, `package/src/elyxdsl/parser/{__init__,parser}.py` и оба каталога docs.

## Результаты и исправления

- Проверено, что `elyb build` ищет `refmap.yml`, `refmap.yaml`, затем `refmap.json`, но dispatcher `elyb stats` требует именно `refmap.yml` и читает YAML. Поэтому JSON-only проект допустим для build, но не для этих stats-команд без обходного решения. Это зафиксировано отдельно в fact 025 и на source page.
- Подтверждено отсутствие в Kangel tree `package/src/elyxdsl/interpreter.py`, хотя `cmds/script.py` импортирует `elyb.elyxdsl.interpreter.run` после parsing `.edsl`. Parser/lexer не доказывают рабочее исполнение DSL; page и fact 027 оставляют runtime неизвестным.
- Сверено расхождение `stringSplitting`: config default и docs включают флаг, но `EncodeStringsAdvanced` лишь сохраняет `useStringSplitting`, `visit_Constant` всегда зовёт `_makeXorStringExpr`, а `_makeSplitStringExpr` не вызывается и заканчивается обращением к неопределённому `decoder_call`. Source page и fact 014 точно обозначают это статическим выводом, без предположения о runtime.
- Проверен dynamic loader fallback: без `loaderStubDynamicKey` build-time ключ берётся как SHA-256 от байта `xorKey` и первых байтов compressed payload; сгенерированный loader вычисляет ключ от конкатенации отсортированных непубличных имён `LayoutHelper`. Кодовое соответствие не прослеживается. При заданном hex ключе код использует переданные digest bytes; docs описывает получение digest на целевом устройстве. Указание на несовпадающие алгоритмы fallback, явный ключ и подавление runtime исключений дополнено на source page и в fact 030; это не runtime-проверка.
- Сверено с отдельным snapshot ShareUI, чтобы не переносить несовпадающие контракты. Kangel добавляет/меняет `obfuscationIgnore`, mapping и расширенную обфускацию; принимает `zipformat` в `runNew` и исправляет связанный вызов `writePlugin`; имеет свои watch error-handling изменения. При этом `script.py` и `stats.py` совпадают по строкам между двумя захваченными версиями, и отсутствие interpreter относится к обоим snapshots. Страницы и provenance форков остаются раздельными.
- Claims о loader sandbox/runtime, совместимости `.eaf`/шифрования, locale loader/fallback и тестовом покрытии не расширялись сверх доказательств: это границы репозитория или документационные заявления. История коммитов помечена вторичным источником, а не заменой проверки SHA.

Повторов внутри набора из 30 facts не обнаружено. Парные claims про loader и отсутствие loader consumer фиксируют разные факты: builder генерирует код, но сам клиентский loader не поставляет. Совпадающие общие сведения с ShareUI допустимы как отдельное provenance; канонические темы для дальнейшего синтеза — `build`, `obfuscation`, `archive`, `workflow`, `metadata`, `DSL`.

## Остаточные gaps

- `.gitignore` — единственный blob из полного, неусечённого tree, отсутствующий в полученном file manifest; он не нужен для заявленных build/runtime contracts, но прочитан не был.
- Нет клиентского ElyxCore loader/import resolver, sandbox, plugin lifecycle/hook implementation, resource/locales consumer или client-side EAF/шифрования кода. Поэтому реальная совместимость scaffold, archive, Python bytecode и loader stubs не установлена.
- В snapshot нет `tests/` и `.github/workflows/`; регрессионные и CI проверки инструмента этим источником не подтверждены. Код не запускался, зависимости не устанавливались, сборки и архивы не создавались.
- У DSL отсутствует импортируемый interpreter; lexer/parser покрыты, семантика и безопасность исполнения остаются недоступными.
- Dynamic loader key pairing и string splitting проверены статически; runtime-поведение на target app/device остаётся непроверенным.

Ограничения обоснованы полным локальным tree snapshot и его manifest, а не попыткой вывести поведение клиента из документации. Этот review принимает страницу как полезный снимок инструментального контракта Kangel SHA с перечисленными gaps, но не утверждает абсолютную полноту runtime-интеграции.
