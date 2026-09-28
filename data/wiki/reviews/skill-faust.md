# Независимая проверка: `skill-faust`

- **Источник:** `faustyu1/exteragram-plugins-skill` — только этот owner/repository; не `fossSquad/exteraSkill` и не `makarworld/exteragram-plugin-skill`.
- **Commit:** `07ec5d517eeade413f0885339c5d50f9d0d7910f`, ветка `main`, raw capture от 2026-09-27.
- **Радарный контекст:** `raw/skill-faust/radar-context.md`, строки 1494–1501, называет репозиторий вспомогательным skill для разработки ExteraGram-плагинов. Source README действительно описывает Android/Python plugin SDK.
- **Вердикт:** `accepted-with-gaps`.
- **Объём:** весь единственный доступный файл README (1030 строк, 38 321 byte) и полное дерево этого SHA.

## Идентификация и доступность

Сверены `repository.json`, `snapshot.json`, `tree.json`, `file-manifest.json`, raw README, source page и `work/skill-faust-facts.json`. GitHub repository metadata подтверждает full name `faustyu1/exteragram-plugins-skill`; snapshot и tree используют SHA `07ec5d517eeade413f0885339c5d50f9d0d7910f`. Recursive tree сообщает `truncated: false` и содержит ровно один blob: `README.md` (blob SHA `a325808bd76973b5b33c306e9ba670db220bca1c`). Сохранённый README имеет SHA-256 `54a1ae259b1d4b67154e289a9632cc13c7380ff043d977b8a706e24b8e226eab`, совпадающий с manifest.

Отдельно запрошены по **этому же pinned SHA** `plugin-development/SKILL.md`, `SKILL.md`, `references/go-cdylib-ctypes-pattern.md`, `templates/calculator_plugin.py`, `templates/calc.go`, `LICENSE`, `tests/test_plugin.py` и `.github/workflows/ci.yml`. Каждый exact raw URL записан в `raw/skill-faust/file-manifest.json` с HTTP 404; полное неповреждённое tree также исключает эти пути. README упоминает reference/template пути в строках 775–778, 980–983 и 1027, но их содержимое на этом SHA недоступно. Ни ветка по текущему имени, ни другие ExteraGram skills для восстановления не подставлялись.

## Независимое покрытие и исправления

Полностью прочитан README. Сверены его version/trigger framing (строки 1–16), metadata и файловый формат (20–72), Go cross-build/ctypes (74–89, 846–901, 938–1023), ADB (91–98, 903–920, 1025), lifecycle/settings (130–161), hook contracts, menu/settings (165–322), Xposed/HookFilter/reflection/proxy (326–400, 538–550, 657–735), client queues/request/message helpers и NotificationCenter (404–487), Android dispatch, formatting и file/UI helpers (491–653), packages/class names (739–771), calculator sample (775–842) и Pitfalls (961–1030). Source page отражает эти направления; утверждения SDK и примеры сохранены как `docs`, без объявления их runtime-проверенными.

В source page уточнена идентичность репозитория, полный состав дерева и pinned 404 для ожидаемых файлов; добавлена явная ссылка на review. В machine facts добавлено отдельное утверждение о base64-противоречии; расширены доказательные диапазоны facts `.plugin` и ADB. Теперь `work/skill-faust-facts.json` содержит **35 фактов, 35 уникальных ID и 35 уникальных claims**.

Проверены точные README line references: файл имеет 1030 строк, все заявленные диапазоны укладываются в него; SHA во всех README facts относится к одному pinned commit. Самая заметная проблема источника не устранима редактурой wiki: README утверждает, что `.plugin` всегда bare Python и ZIP ломается при text/AST parsing (22–23, повтор 964–967), но одновременно даёт ZIP `.plugin` с `plugin.py`/`.so` и `zipfile` extractor (44–72). Он отвергает embedded base64 из-за AST и порога около 4 MB (29, 975), но позднее предлагает base64 `.so` decoder (922–936). ADB-разделы называют app-private push запрещённым без root/debuggable и предлагают `/sdcard/` + UI import (28, 91–98, 912–920), тогда как между ними дан безусловный `adb push` сразу в app-private путь (903–908). Эти три контракта помечены как неразрешённые документальные противоречия; безопасный/рабочий путь из одного README не выводился.

Дополнительно README повторяет Go cdylib build/deploy guidance в нескольких секциях, имеет два последовательных заголовка `## Pitfalls`, а ownership `C.CString` расходится: ранний пример предлагает `FreeString`, поздний говорит, что память освободит Go GC (строки 863–901, 1016–1023). Source/facts сохраняют несогласованность вместо выбора неподтверждённого контракта.

## Дубли и канонические темы

Внутри facts этого источника буквальных дублированных claims не найдено: идентификаторы и claims уникальны. В других принятых facts есть независимые подтверждения похожих правил от `official-sdk`, `skill-foss` и `skill-makarworld`: metadata/AST, lifecycle callbacks, hook registration/HookResult, UI dispatcher и ограничения pure-Python dependencies. Это разные provenance и ревизии, поэтому они остаются отдельными фактами; для будущего синтеза им соответствуют канонические темы `build`/`portability`, `lifecycle`, `hooks`, `threading` и `ui`. Упоминания Elyx ZIP в других источниках относятся к отдельному archive format и не подтверждают формат `.plugin` из этого README. ExteraGram SDK baseline в этом README — `1.4.3.6`; его нельзя смешивать с более поздними baseline других skills или выдавать за актуальную версию клиента. `distribution` здесь отражает собственную противоречивую ADB-инструкцию источника, точного совпадающего правила в других рассмотренных facts не найдено.

## Остаточные пробелы

- Дерево содержит только документацию. Реализация importer/parser, SDK и клиента отсутствует, поэтому metadata/AST behavior, `.plugin` container format, module/signature availability, filesystem semantics, package compatibility и app lifecycle не подтверждены кодом или устройством.
- Разрешить `.plugin`, base64 и ADB противоречия по этой ревизии нельзя. Go/C allocation contract также не установлен.
- README ссылается на отсутствующие reference/template files; их contents неизвестны. На этом SHA не найдены license, tests и CI/build workflow.
- Ничего не запускалось и не устанавливалось; команды, примеры, packages, app version и SDK compatibility не проверялись на runtime.

**Обоснование verdict:** `accepted-with-gaps` означает, что весь pinned tree и весь доступный README идентифицированы и отражены с корректным provenance, а перечисленные внутренние конфликты и отсутствующие реализации явно сохранены как ограничения. `unavailable-verified` не подходит: сам назначенный репозиторий и README доступны; unavailable только упомянутые файлы и подтверждающая реализация. Принятие не означает правильность README contracts или полноту за пределами этого snapshot.
