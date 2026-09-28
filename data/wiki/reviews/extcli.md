---
type: review
source_id: extcli
review_status: accepted-with-gaps
reviewed_sha: 0eafced3fc14dd7ffd534b103b62f4041fff6339
date: 2026-09-27
---

# Независимая проверка vcvkk/extCLI

## Объём

Проверен источник `vcvkk/extCLI` из дерева `main` на SHA [`0eafced3fc14dd7ffd534b103b62f4041fff6339`](https://github.com/vcvkk/extCLI/tree/0eafced3fc14dd7ffd534b103b62f4041fff6339). В `raw/extcli/snapshot.json` записан этот SHA и `tree_truncated: false`; снимок содержит 127 файлов-копий, перечисленных в manifest. Radar-context рассмотрен как вторичный набор утверждений и направлений, не как спецификация. README, HISTORY и meta.yml помечены как заявления проекта.

Покрыты релевантные интеграционные поверхности: lifecycle и очереди (`extcli/src/{BasePlugin.py,main.py,services.py}`), диагностические и reflective adapters (`compat/{host,paths,plugins,messaging,reflect,meta,settings,store,menus}.py`), команды plugin/config/tg/host/rootfs, lexer/parser/executor и backend chain, rootfs setup/mount/path translation, `.cli` relay/LiveText, Python↔Kotlin terminal bridge, native loader/pathmap/probe исходники, CI workflow и контрактные тесты. Это граница функций extCLI из радара и полезных точек интеграции, не пересказ Telegram upstream.

Все утверждения о сигнатурах трактуются как статическое чтение конкретного SHA. Ни shell-команды из кода, ни rootfs/native бинарники, ни тесты не запускались. DEX-файл `extcli/dex/terminal.dex` не декомпилировался и не сравнивался с Kotlin исходником; Android runtime, установленный APK и CI run не проверялись.

## Проблемы и исправления

- Сборщик оставил 29 записей фактов в `outputs/plugin-wiki/work/extcli-facts.json`, хотя требуемый итоговый файл должен лежать в workspace `work/`. Итог скопирован и дополнен до **35 уникальных фактов** в `work/extcli-facts.json`; совпадений ID нет.
- Формулировка fallback для `tg get` обобщала `.jpg` на все вложения. Исправлено: документ получает `file_name`, а `.jpg` — fallback для фото. Добавлено ограничение, что повторяющиеся имена могут перезаписывать результат.
- Формулировка backend chain не отличала rootfs от host режима. Исправлено по `backends/chain.py`: без rootfs `system → linker → in-process`, с rootfs `rootfs → in-process`, а непереводящие guest paths backend удаляются.
- В source page не были описаны `config` preference-store команды как отдельный API; добавлены commands, typed writes, `--new`, policy gate и совет о перезапуске.
- Добавлены проверки Alpine SHA до распаковки, правила tar extraction, mount semantics и оговорка, что mount-настройки не являются границей безопасности.
- Старые README/HISTORY не использованы для современного списка API. История сверена с GitHub commit pages: `132c8333f89b` (tg read), `ad3ee99af368` (tg get), `9ba2a3d7f5f8` (plugin install), `6f3611ec310e` (уточнение installer method), `9ce4c2429101` (.cli chat relay) и `2ebcada9c464` (rootfs backup symlink portability). Коммит 5 сентября касается export backup для совместимости с безопасным tar extraction filter, а не общего подтверждения безопасности всех путей распаковки.
- Статический просмотр `rootfs/install.py` обнаружил вероятный symlink-parent обход: `safe_name` отклоняет абсолютные и traversal имена, но `_inside` использует `normpath`, не разрешая symlink-компоненты. Поскольку `rootfs install` принимает также путь к tarball, архив с symlink-элементом, указывающим наружу, а затем дочерним файлом может направить следующую файловую запись за каталог rootfs. Это inference по последовательности кода, не выполненная проба и не подтверждённый runtime exploit. Исходная страница теперь прямо указывает ограничение и не называет extractor полностью безопасным.

## Дубликаты

Внутри source page одинаковые утверждения об одном контракте сведены: plugin controller/install описан в одном разделе, Telegram read/get/send — в одном тематическом блоке, shell backend различает два режима. В fact JSON оставлены отдельные факты лишь там, где они дают самостоятельный API или ограничение; итоговые ID `extcli-001`–`extcli-035` уникальны. Совпадения с другими source pages не проверялись как основание для удаления provenance; последующее объединение следует вести по каноническим темам `plugin lifecycle/install`, `settings`, `Telegram messaging`, `shell/rootfs`, `terminal DEX`.

## Остаточные пробелы

- Нет runtime проверки на целевом Android/exteraGram, проверки матрицы версий или подтверждения, какая overload форма SDK реально выбрана.
- CI workflow просмотрен, но статус конкретного GitHub Actions run не получен; тесты прочитаны как кодовые контракты, не выполнены. Упоминания `653`/`694`/`700+ passing` в HISTORY, radar или commit messages не являются результатом этой проверки.
- DEX/ELF и встроенный Alpine tarball не подвергались самостоятельному бинарному анализу; Kotlin↔DEX соответствие не доказано.
- Symlink-parent ограничение в rootfs extractor требует исправления или отдельной целевой проверки, прежде чем делать security claim о распаковке недоверенных архивов.
- Остальные методы exteraGram/Telegram классов зависят от версии клиента и остаются гипотезами, пока не проверены на соответствующем APK.

## Вердикт

**accepted-with-gaps** — статически подтверждённые интеграционные факты и исправленный материал пригодны как versioned source reference; полнота runtime API и безопасность распаковки не подтверждены. Не интерпретировать этот статус как security certification или тестовый pass.
