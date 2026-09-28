# Независимая проверка catalib

## Область и снимок

- Источник: `cataIystdev/catalib`, commit `5c9871245d77494f33b7e81b1050d29478dcbaa8`, версия пакета `0.3.3`; snapshot захвачен 2026-09-27.
- `raw/catalib/tree.json` помечен `truncated: false`; `file-manifest.json` содержит 223 файла, на диске найдено 223 снимка файлов. Сверка выполнена по `raw/catalib/files/`, без запуска исходников.
- `radar-context.md` содержит общий контекст о каталоге инструментов и упоминает catalib как соседний проект; конкретных технических claims о catalib там нет. `radar-urls.json` пуст. Факты страницы проверялись против снимка репозитория.
- Проверены README/pyproject/changelog; релевантные разделы `book/` о manifest, bundling, hooks, settings, SDK helpers, offline testing, CLI, deployment, Android, errors; `docs/components/`, architecture overview/ADRs/evidence и device workflow; основные реализации `manifest`, `bundler`, `runtime`, `support`, CLI, deploy, scaffold, `watching`, `diagnostics`, `devicelogs`, `testing`; целевые тесты discovery/compiler/treeshake/requirements/bootstrap/roundtrip/harness/public API/plugin/Xposed. Проверка тестовых исходников была статической. Examples и contributing-разделы не проверялись построчно.

## Результат

Вердикт: **accepted-with-gaps**. Исправленная страница теперь покрывает роль catalib как инструмента сборки, встраиваемый SDK facade, plugin lifecycle/hooks/settings, офлайн harness, scaffolding, watch, deploy, doctor и logs. Факты сверены с реализацией на указанном SHA, а документированные и выводные утверждения маркируются раздельно. Сборка, тесты, install-команды и устройство не запускались.

Обнаруженные проблемы и исправления:

1. Исходная страница почти целиком описывала bundler и пропускала основной integration surface `catalib.support` и lifecycle API. Добавлены тематический раздел, источники к handlers и настройки, плюс отдельный JSON факт о фасаде API. Заявление авторов о «полном паритете» оставлено как документационное, не как независимо установленная совместимость со всеми SDK builds.
2. Не были представлены функции разработки: `catalib.testing.PluginHarness`, четыре `init` template, `watchfiles`/stdlib polling fallback, `doctor`, `logs` и dev-server deploy. Эти сведения добавлены в источник и JSON с реализационными ссылками.
3. Факты `catalib-003` и `catalib-015` повторяли одно ограничение: namespace package без `__init__.py` не проходит discovery. Повтор `015` удалён; ограничение остается в `003`.
4. Прежний `catalib-023` говорил, что успешный status для SHA неизвестен. Независимый запрос GitHub API показал общий commit status `success` из двух GitBook context; endpoint check-runs вернул `total_count=0`. Факт и страница исправлены: build/test CI этим не подтверждается.
5. Есть расхождение документации с кодом deploy: документация говорит, что `set_plugin_enabled(true)` нужен при первом deploy, а `deploy_plugin(..., enable=True)` вызывает его при каждом обычном вызове (и повторяет reload). Это отражено как code-vs-doc distinction в JSON и странице.

## Факты и повторяемость

В `work/catalib-facts.json` сейчас **34 уникальных факта** с уникальными ID. Дубли внутри источника проверены; дополнительный повтор про namespace packages объединён. Повторение общих правил с другими источниками допускается при сохранении отдельного provenance; последующее объединение относится к существующим canonical topics `build`, `portability`, `lifecycle`, `hooks`, `debug`, `distribution`, `testing` и `workflow`.

Для CI точный внешний статус проверен для того же SHA на 2026-09-27: доступны только два успешных GitBook contexts, а GitHub check-runs отсутствуют. Текущие check runs или иное CI-состояние могли измениться после проверки.

## Остаточные gaps и ограничения

- Не выполнялось сравнение всех 14 support helper API с каждой текущей версией официальной документации/сборки ExteraGram. Ссылка на ADR-0007 подтверждает позицию проекта, а не универсальную совместимость.
- Не повторялись исторические T-011/T-081 device probes и тесты репозитория. T-011/T-081 остаются датированными записями проекта; текущая совместимость устройств, версий приложения и Chaquopy не подтверждена.
- Поддержка/миграция ElyxCore не описана в снимке; README сообщает о прекращении поддержки, а repository metadata помечает репозиторий archived.
- Полный CI pipeline для указанного SHA не установлен: найденные статусы — документационная публикация, check-runs нет.
- Проверка ограничена относящимися к интеграции материалами; примеры и документация для contributors не сверялись построчно. Не запускался runtime, поэтому все выводы о поведении, кроме датированных project records, основаны на коде/тестах snapshot.
- В уже отмеченных страницей границах остаются dynamic vendor imports, cyclic plugin imports, произвольные assets, бинарные Python wheels и версии runtime за пределами записанных probes.

Результат: **accepted-with-gaps**; проверка не является гарантией абсолютной полноты недоступного/неповторённого runtime поведения.
