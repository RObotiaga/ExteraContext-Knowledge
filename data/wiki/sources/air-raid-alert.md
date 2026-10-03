---
type: plugin
source_id: air-raid-alert
platform: Android
review_status: unavailable-verified
review: ../reviews/air-raid-alert.md
date: 2026-09-28
---

# exteraGram-air-raid-alert: источник пока не идентифицирован

## Вердикт

Источник нельзя однозначно найти по переданным данным. В `work/radar-source-candidates.json` для имени `exteraGram-air-raid-alert` нет URL и namespace `owner/repo`; кандидат помечен `unresolved_repository_identity`. Точный запрос GitHub REST Search Repositories по имени с `in:name` вернул 0 результатов. Имя может быть display name, названием удалённого/переименованного репозитория или неточным пересказом, но доступные материалы не позволяют выбрать между этими вариантами.

Независимая проверка завершена с вердиктом `unavailable-verified`: подтверждённый снимок целевого первоисточника не получен, и его identity по имеющимся данным не установлена. Это не доказывает, что репозитория никогда не существовало. Дополнительные точные запросы и проверки зеркал не установили его identity; каталожная запись с похожим названием использует другой формат артефакта и не содержит связи с искомой GitHub identity.

## Что сообщает радар

Радар за 16 сентября 2026 сообщает, что новый репозиторий был создан 16 сентября в 10:12 UTC, автор называл его `Plugin exteraGram`, а дерево состояло из README и `air_raid_alert.elyx` размером около 21 КБ. Радар также говорит, что `.elyx` — упакованный формат и не описывает функции без чтения содержимого.

В предоставленном тексте отсутствуют URL и owner; candidate registry также не содержит namespace. Следовательно, дата, описание автора, размер и наличие файла являются только вторичными поисковыми признаками. Они не дают доступа к README, commit SHA, manifest или самому файлу. Кодовые и поведенческие выводы не делаются.

## Проверка идентичности и поиска

- GitHub REST Search Repositories: точный `exteraGram-air-raid-alert in:name` — 0 результатов: [ответ API](https://api.github.com/search/repositories?q=exteraGram-air-raid-alert+in%3Aname).
- GitHub REST Search Repositories: точная строка `"exteraGram-air-raid-alert"` — 0 результатов: [ответ API](https://api.github.com/search/repositories?q=%22exteraGram-air-raid-alert%22).
- Поиск по `exteragram in:name created:2026-09-16` — 0 результатов: [ответ API](https://api.github.com/search/repositories?q=exteragram+in%3Aname+created%3A2026-09-16). Это согласуется с указанной датой, но ограничено текущим поисковым индексом GitHub.
- Поиск по `air_raid_alert.elyx` в repository search — 0 результатов: [ответ API](https://api.github.com/search/repositories?q=air_raid_alert.elyx). Вариант `in:readme` выдал `MightyM17/CSI_Task_App_22`, созданный в 2022 году: [ответ API](https://api.github.com/search/repositories?q=air_raid_alert.elyx+in%3Areadme). Это совпадение текста поиска в README, а не подтверждение наличия артефакта.
- GitHub REST Search Code для `air_raid_alert.elyx` и точного названия вернул `401 Unauthorized`; этот канал поиска не подтвердил и не опроверг наличие файла ([API endpoint](https://api.github.com/search/code?q=air_raid_alert.elyx)).
- Общий repo search по `air-raid-alert` возвратил проекты про API воздушных тревог, устройства, desktop wallpaper и tray apps ([ответ API](https://api.github.com/search/repositories?q=air-raid-alert)). Никакой из этих результатов не указывает на ExteraGram; по одному имени их нельзя приписать этому источнику.
- Sourcegraph global search для точного `air_raid_alert.elyx` с включёнными archived и forks завершился с `matchCount: 0`: [поиск](https://sourcegraph.com/search?q=context%3Aglobal+%22air_raid_alert.elyx%22+archived%3Ayes+fork%3Ayes&patternType=literal). Поиск точного `exteraGram-air-raid-alert` также не вернул совпадений, но отчёт отметил shard match limit: [поиск](https://sourcegraph.com/search?q=context%3Aglobal+%22exteraGram-air-raid-alert%22+archived%3Ayes+fork%3Ayes&patternType=literal).
- GitLab project search и Codeberg repository search по точному имени `exteraGram-air-raid-alert` вернули пустые списки ([GitLab API](https://gitlab.com/api/v4/projects?search=exteraGram-air-raid-alert&simple=true&per_page=100), [Codeberg API](https://codeberg.org/api/v1/repos/search?q=exteraGram-air-raid-alert&limit=50)). Codeberg search по точному имени файла также вернул пустой список ([Codeberg API](https://codeberg.org/api/v1/repos/search?q=air_raid_alert.elyx&limit=50)).
- Запросы Wayback CDX для wildcard-страниц `github.com/*/exteraGram-air-raid-alert` и `github.com/*/air_raid_alert.elyx` завершились timeout/503, поэтому архивную проверку подтвердить не удалось ([запрос 1](https://web.archive.org/cdx/search/cdx?url=github.com/*/exteraGram-air-raid-alert&output=json&filter=statuscode:200&collapse=urlkey), [запрос 2](https://web.archive.org/cdx/search/cdx?url=github.com/*/air_raid_alert.elyx&output=json&filter=statuscode:200&collapse=urlkey)).
- Локальный снимок KPM каталога `Kangel-Plugins/Plugins-Store` на SHA `513e29a07858e5dec3a8dcdc6a860fe4296f1d43` содержит отдельную запись `Air Raid Alert – alerts.in.ua`, ID `air_raid_alert`, версия `1.2.0`, автор `@cobra_S0FT | @excess_plugins`; [запись каталога](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/store.json#L472-L505) указывает на `air_raid_alert.eaf`. Это кандидат с похожим названием, но сведения не связывают его с GitHub repo/file `.elyx` из радара. Поэтому эта запись не меняет identity verdict.
- Веб-поиск по точным строкам `"exteraGram-air-raid-alert"` и `"air_raid_alert.elyx"` не дал результатов, идентифицирующих репозиторий.

Результаты поисков воспроизводимы по ссылкам API, но отражают состояние публичного поиска на дату сбора. Удалённые, приватные, переименованные или неиндексированные репозитории могут быть ими не обнаружены. Для подтверждения нужен первичный указатель: ссылка, namespace, Telegram post с ссылкой либо commit/release URL.

## Покрытие и ограничения

| Материал | Результат |
|---|---|
| `outputs/plugin-wiki/raw/radar.md:3643-3655` | Прочитано; использовано только как вторичное описание и как набор поисковых признаков. |
| `work/radar-source-candidates.json` | Точная запись прочитана; URL и owner/repo отсутствуют, identity статус unresolved. |
| GitHub REST Search Repositories | Проверены точное имя, имя файла, имя с датовым фильтром и общее тематическое имя. |
| GitHub REST Search Code | Запросы сделаны; доступ закрыт ответом 401. |
| Веб-поиск по точному имени и файлу | Индексированных результатов не найдено. |
| README, manifest, `.elyx`, commit SHA, snapshot/tree | Не получены, так как целевой репозиторий не идентифицирован. `.elyx` не запускался и не распаковывался. |
| KPM/catalog | Независимо проверен локальный снимок `Kangel-Plugins/Plugins-Store@513e29a07858e5dec3a8dcdc6a860fe4296f1d43`; в `store.json:472-505` найдена отдельная запись `air_raid_alert` для артефакта `.eaf`. SHA-256 локального `store.json` — `f155aff2470dba54ebb2584c93646330e5ec0bbf80447719e292214e7cd7d79d`, совпадает с `file-manifest.json`. Связь с `.elyx` из радара не установлена. |

Технические утверждения о функциях плагина отсутствуют. Сведения о дате, авторском описании и составе файлов приведены как `secondary`, а не как подтверждённые свойства конкретного GitHub source.

## Факты

Четыре структурированные записи: [карточки фактов](../facts/air-raid-alert.json) (пакетируемый путь; сгенерированный файл может отсутствовать до сборки wiki). Они фиксируют недоступность, вторичные сведения и неразрешённую связь с похожей записью KPM; утверждений о реализации или поведении `.elyx` нет.
