# Независимая проверка: SHAJON-404/re-extera

- Вердикт: **accepted-with-gaps**.
- Scope: отдельный источник `SHAJON-404/re-extera`, branch `master`, pinned SHA `c188c00821e1b9fbdc020c7d2080ce2699416eac`, snapshot от 2026-09-27. Для сравнения использован отдельный pinned snapshot `fossSquad/re-extera` SHA `3be81ef0c25e842f3a8be669c235e783839c4716`; контракты двух fork не объединялись.
- `snapshot.json` SHA совпадает с `tree.json`; оба дерева `tree_truncated: false`. SHAJON tree содержит 174 blob-файла, fossSquad — 130.
- Независимая проверка статическая. Никакие команды проекта, сборки, тесты, install или device/runtime действия не выполнялись.

## Первичные снимки и соответствие радара

Прочитаны `raw/re-extera-shajon/{snapshot.json,repository.json,tree.json,file-manifest.json,radar-context.md,radar-urls.json}` и сопоставлены с `work/re-extera-shajon-facts.json` и source page. `radar-urls.json` пуст; в `radar-context.md` источник упомянут как SHAJON-404/re-extera среди DEX plugin/dev sources (исходный контекст, строка 5251). Роль страницы как отдельного Android DEX-плагина и custom fork соответствует этому назначению. README на pinned SHA заявляет re:extera 2.8.9 и exteraGram 12.9.0; metadata задаёт minimum plugin engine 12.8.1. GitHub metadata указывает `fork: false`, тогда как README сам именует проект custom fork; это различие корректно отражено.

По `tree.json`/acquisition проверены root `AGENTS.md`, `README.md`, `LICENSE`, `build.gradle`, `.github/workflows/build.yml`, Gradle wrapper/configuration, все 16 `.agent/*.md` feature/reference files, все полученные `loader/*.py` fragments, `reload.py`, ruff/pyright config и selected Java lifecycle/hook/settings/DB files. Feature-note coverage включает architecture, loader, archive, deleted messages, view-once, message menu, quick buttons, ID display, gap/other features, liquid glass, translation, custom icons, settings UI и storage/path notes. Все 29 facts сверены с pinned source paths; claims из `.agent`/README/AGENTS сохранены как `docs`, где факт подтверждает именно текст документации.

Проверенные code evidence включают [Python plugin load/unload](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/loader/plugin.py#L341-L353), [DEX classloader/start/fallback/unload](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/loader/dex.py#L52-L125), [Main process guard и unload](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/src/main/java/ni/shikatu/re_extera/Main.java#L100-L138), [private `HookInit.tryHook` и unhook registry](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/src/main/java/ni/shikatu/re_extera/hooks/HookInit.java#L128-L139), [archive registrations](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/src/main/java/ni/shikatu/re_extera/hooks/HookInit.java#L288-L312), [translate hooks](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/src/main/java/ni/shikatu/re_extera/hooks/HookInit.java#L323-L331), [Gradle DEX configuration](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/build.gradle#L1-L139) and [workflow](https://github.com/SHAJON-404/re-extera/blob/c188c00821e1b9fbdc020c7d2080ce2699416eac/.github/workflows/build.yml#L1-L67). Все 23 pinned GitHub permalink anchors в source page ведут на локально присутствующие файлы и не выходят за конец соответствующих файлов.

## Diff с fossSquad: исправление статистики

Сравнение полных blob-путей обоих **полных, неусечённых pinned Git trees** даёт:

- 117 одинаковых путей, из них 60 с разными Git blob SHA;
- 57 путей только в SHAJON;
- 13 путей только в fossSquad.

Идентичный Git blob SHA у остальных 57 общих путей подтверждает одинаковое содержимое blob; это не утверждение об истории предков. В числе только fossSquad: `src/androidTest/.../ExampleInstrumentedTest.java`, `src/test/.../ExampleUnitTest.java`, `hooks/chatmessagecell/HideFilteredCell.java`, `hooks/messagescontroller/MarkDialogAsRead.java`, `hooks/messagesstorage/MarkMessagesAsDeletedInternalRange.java`, `settings/components/AltSeekbar.java`, `ui/FilteredLogFragment.java`, `utils/{FilterImportExportUtils,FilteredLogManager,HookLookup,ServerReadTracker,SettingsRegistryHelper,UItemUtils}.java`.

Ранее заявленные `106 common / 53 changed / 55 only SHAJON / 13 only fossSquad` смешивали два основания. Локальные `file-manifest.json` — неполные acquisition manifests (161 SHAJON и 120 fossSquad entries), по которым получается `106 / 53 / 55 / 14`. Дополнительный manifest-only fossSquad путь `gradle/wrapper/gradle-wrapper.properties` фактически присутствует в обоих полных trees, но пропущен SHAJON acquisition manifest. Полная tree-сверка поэтому даёт `117 / 60 / 57 / 13`; source page и fact `re-extera-shajon-026` исправлены, прежняя partial-manifest статистика сохранена только для объяснения расхождения.

SHAJON-only примеры подтверждены полным tree: 16 `.agent` docs, `reload.py`, loader/config files и отдельные hooks, включая archive, translate, Liquid Glass, custom tabs, deletion state и icon utility. Это fork-specific добавления/различия pinned snapshot, не переносимые на fossSquad source page.

## Проблемы и исправления

- Пересчитана статистика diff по полным trees и исправлен claim `re-extera-shajon-026`; разница с partial manifests объяснена в source page и здесь.
- Уточнено, что `HookInit.tryHook(...)` — private internal helper, а не публичный SDK API; wording fact `re-extera-shajon-012` исправлен.
- Добавлен testing fact: pinned SHAJON tree не содержит файлов `src/test` или `src/androidTest`; `AGENTS.md` говорит, что placeholder test suite удалена, а workflow ограничивается lint/build/artifact steps. Это `docs`/tree evidence, не утверждение о выполненной проверке.
- Добавлены два документационных integration facts: общий namespace/order ограничение loader fragments и шаблон settings UI/decompiled `$SwitchMap`. Source page дополняет ими recipe.
- В source page явно расширен перечень оставшихся feature-level gaps, чтобы его короткая recipe/coverage не читалась как построчное описание всех заявленных возможностей.

## Повторы и канонизация

`work/re-extera-shajon-facts.json` содержит **29 фактов**, 29 уникальных IDs; одинаковых нормализованных `topic + claim` нет. Повторяющиеся темы между двумя re-extera страницами являются отдельным provenance одного похожего проекта; их можно свести позже в темы `hooks`, `lifecycle`, `build`, `workflow`, `storage`, `ui` и `portability`, сохраняя fork/SHA/source отдельно. Сигнатуры и отличия одного fork нельзя переносить в другой только из-за одинакового пути или названия проекта.

## Остаточные gaps и основание вердикта

- Не разобраны построчно примерно 100+ hook/helper классов и все Java UI реализации. Среди оставшихся feature groups: точные message-menu IDs/условия/handlers, re:forward, Local Premium, Work in Background, custom SVG `PathIconDrawable`, profile-menu ID, protected stories/call button, полный Settings tree, Ghost Mode, Shadowban, regex filtering, message-forwarding и полная семантика SQLite schema/cache/TTL/output paths. `.agent` notes объясняют эти области, но их assertions остаются документационными, пока соответствующий code path не проверен.
- Host implementation и binary `libs/exteragram.jar` не проверялись; внешний decompiled `draft/extragram` и `draft/telegraph` не входят в pinned snapshot. Поэтому совместимость приватных host methods/fields, hooks и SDK версиями кроме заявленной не установлена.
- Build workflow описан, но его фактические CI results не проверялись. Устройство и runtime не проверялись; on-device tracing из `.agent` notes не является evidence данного review. По документации проекта тестовая suite отсутствует.
- GitHub compare REST URL в source page/collection упомянут как недоступный; точную ancestry/commit, когда SHAJON отделился, здесь не устанавливал. Полные tree snapshots достаточны для указанной статистики содержимого, но не для вывода о происхождении.

После точечных исправлений source page и 29 pinned evidence-backed facts принимаются **с перечисленными пробелами**. Абсолютная полнота по неразобранным классам и внешнему host-коду не заявляется.


