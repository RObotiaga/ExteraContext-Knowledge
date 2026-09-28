---
type: review
source_id: ayugram-sample
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: MrCheatEugene/AyuSamplePlugin

- **Вердикт: accepted-with-gaps.** Страница отражает существенное содержание доступного sample snapshot и явно отделяет примеры кода от подтвержденного поведения. Остаётся неопределённость точной версии PLEngine, под которую собирался sample, и отсутствует runtime/build evidence.
- **Snapshot:** `MrCheatEugene/AyuSamplePlugin`, ветка `master`, commit `76d0514da1210e5f913c8c239713c2532d42cfea`, дата фиксации 2026-09-27. `tree.json` не усечён и содержит 13 blob-файлов. Все 13 присутствуют в `file-manifest.json`; сверка SHA-256 каждого локального файла с manifest совпала.
- **Независимо прочитанное покрытие:** `README.md`, `AyuPlugin.h`, `dllmain.cpp`, `AyuSamplePlugin.sln`, `AyuSamplePlugin.vcxproj`, `.vcxproj.filters`, `.vcxproj.user`, `pch.h`, `pch.cpp`, `framework.h`, `.gitignore`, `.gitattributes`, `LICENSE.txt`; также `tree.json`, `snapshot.json`, `repository.json`, `file-manifest.json`, `radar-context.md`, `radar-urls.json`, `discovery-pkgbuild.txt` и адрес из `raw/user-supplied-urls.json`. По коду сверены объявления структур/typedefs, экспортные функции, все lambda-примеры, UI/popup/preprocess/deletion/online hooks, `DllMain` и Visual Studio metadata. Ничего не запускалось и не собиралось.
- **Идентификация и радар:** первичный snapshot и `repository.json` подтверждают `MrCheatEugene/AyuSamplePlugin`; точный URL совпадает с пользовательским URL. `radar-urls.json` пуст, а `radar-context.md` содержит вторичное упоминание обновлённого Desktop PLEngine sample/API. Отдельный `acquisition-error.json` относится к старому имени `AyuGram/PluginSample` и 404, а не к каноническому репозиторию; он не опровергает полученный полный snapshot. Код подтверждает наличие GUI, popup и `std::string*` preprocess examples, но без сравнения истории коммитов нельзя независимо утверждать точный diff или дату появления.

## Найденные проблемы и исправления

- Уточнено доказательство платформы: README называет AyuGram Desktop PLEngine, а `.vcxproj` задаёт Windows `DynamicLibrary` для Win32/x64. Обновлены формулировка, evidence path и статус первого факта.
- Устранена неоднозначность о MTProto lambda `y` и `z`: тела lambdas находятся в `dllmain.cpp`; закомментированы только их вызовы через `addToQueue`, поэтому сценарии не подтверждены как исполненные.
- Сверен ABI с уже проверенным отдельным источником PLEngine, commit `55feefdb6abd702e368b12431de97313441362a0`: его `AyuPlugin.h` задаёт `AyuPlugin* (*)()`, `FilteredState (*)(HistoryItem*)`, `bool (*)(HistoryItem*)` и `bool (*)()`, а `PLEMains.cpp` вызывает `pluginInfo` как функцию с результатом `AyuPlugin*`. В sample definitions результаты объявлены типами указателей на функции и числовые/enum значения приводятся к этим типам. Это статически подтверждает несовпадение прототипов sample с typedefs и loader в проверенном engine snapshot; совпадение этого engine SHA с целевой версией sample не установлено, а runtime последствия здесь не проверялись. Аналогичное несовпадение уже описывалось на sample page; добавлена точная cross-source граница, а не предположение о фактическом отказе загрузки.
- Итоговый `work/ayugram-sample-facts.json` содержит **22 факта с 22 уникальными ID**. Повторяющихся IDs и одинаковых claims внутри этого набора не обнаружено; исходные разные API-контракты и их несоответствия не слиты.

## Дубликаты с принятыми знаниями

В проверенной source page PLEngine есть пересечение по ABI (`AyuPlugin`, `MemData`, `pluginInfo`), callbacks фильтрации/deletion/online, GUI и preprocess. Это отдельный репозиторий и отдельный SHA: PLEngine описывает ожидаемый контракт и call-sites, а sample — демонстрационные определения/ошибки и примеры использования. По правилам базы обе записи сохраняются с отдельным provenance; одинаковые пользовательские правила и рецепты можно синтезировать позднее в канонических Desktop PLEngine темах `hooks`, `lifecycle`, `threading`, `ui` и `build`. Страницы других источников, topics и общий index не менялись.

## Остаточные gaps

- Не установлен точный AyuGram Desktop/PLEngine commit, против которого автор собирал sample commit; межрепозиторное сравнение выполнено с отдельным сохранённым PLEngine SHA.
- Нет собранной DLL, таблицы экспортов бинарного файла, CI/тестов либо запуска на Desktop build. Source inspection не является `runtime-verified`.
- Внешние private headers и реализации AyuGram/Telegram, включая срок жизни переданных адресов, thread safety и полное поведение hooks, не входят в sample repository. Комментарии sample о потоках, main thread и `sendReq` остаются документацией автора, если отдельно не подтверждены выбранным engine snapshot.
- Конфигурация проекта привязана к локальным абсолютным путям и неоднородным зависимостям; переносимая или рабочая конфигурация сборки не доказана. История коммитов не изучалась, поэтому радарное утверждение о том, какие именно API были добавлены обновлением, подтверждено лишь наличием примеров в зафиксированном tree.
- PLEngine review отмечает, что invocation popup hook не найден в исследованных history/context-menu call-sites engine; sample показывает только добавление action. Это ограничение cross-source остается открытым.
