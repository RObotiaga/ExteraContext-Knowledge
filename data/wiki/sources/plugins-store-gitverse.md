---
type: source
source_id: plugins-store-gitverse
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-gitverse.md
date: 2026-09-28
---

# GitVerse `bigfishtheory/Plugins-Store` — собственное состояние зеркала KPM

Источник: [GitVerse: bigfishtheory/Plugins-Store](https://gitverse.ru/bigfishtheory/Plugins-Store), ветка `main`, pinned commit `08ddcb84661a148b66d691f4f06fd6779e67b793`. Проверено 2026-09-28. Закреплённый commit создан `mirror-bot`, его сообщение — `chore: rewrite Forgejo links to GitVerse [mirror-bot]`. Снимок и дерево получены через GitVerse Git smart HTTP; `HEAD` и `refs/heads/main` указывали на один SHA. GitVerse REST-путь `/api/v1/repos/bigfishtheory/Plugins-Store` вернул 404, но веб-страница проекта доступна, а собственный raw endpoint `/api/repos/.../raw/branch/main/...` ответил 200. Метаданные, commit, полное дерево и SHA-256 выбранных файлов сохранены в [raw snapshot](../../raw/plugins-store-gitverse/snapshot.json), [repository metadata](../../raw/plugins-store-gitverse/repository.json), [tree](../../raw/plugins-store-gitverse/tree.json) и [file manifest](../../raw/plugins-store-gitverse/file-manifest.json).

## Роль и границы

README описывает проект как место хранения плагинов для Kangel Plugins Manager. Это зеркало каталога и артефактов, а не отдельный SDK или руководство по созданию плагинов. Здесь важны GitVerse URL и содержимое закреплённого каталога: ссылки ведут на GitVerse raw API, а workflow содержит отдельный этап переписывания ссылок и отправки на GitVerse. Сам `.eaf` менеджера совпадает побайтно с файлами GitHub snapshot `513e29a07858e5dec3a8dcdc6a860fe4296f1d43` и Codeberg snapshot `3a9417b85597127d843b0411792721f111297a0a` (SHA-256 `554815b906a155210f02fdd4de76c66ce4cf1fcba34b4e4651f143bc0b216625`); нового кода менеджера по этому файлу не обнаружено.

Сравнение выполнено по leaf-файлам (`type=blob`) и Git blob SHA закреплённого GitVerse снимка и сохранённого GitHub снимка: набор путей совпадает (1 321 файл), 1 319 файлов имеют одинаковый blob SHA. GitHub tree содержит ещё 262 directory entries (1 583 entries всего); они не включены в сравнение файлов. Отличаются только `.github/workflows/mirror.yml` и `store.json`, что согласуется с переписыванием ссылок в зеркало. В `store.json` GitVerse все 698 ID совпадают с GitHub снимком; после рекурсивного удаления полей `url` содержимое записей также совпадает. Следовательно, различия каталога на этих refs — адреса зеркала. Это вывод только о сравниваемых SHA, не гарантия постоянной синхронности.

Codeberg snapshot старше и имеет другой каталог. В нём есть два ID, которых нет в GitVerse (`custom_gifts`, `spam_collapse`), а `plugin_guard` и `camera_enhancer` содержат другие версии и связанные hash/signature; в GitVerse эти записи совпадают с сохранённым GitHub snapshot. Сравнение не переносит данные Codeberg на GitVerse и не предполагает единую текущую версию каталога.

Исследованы README, `LICENSE`, `AGENTS.md`, весь `store.json`, mirror workflow и только один релевантный пакет менеджера. Остальные плагины и архивы не открывались. Код приложения и плагины не запускались; работы KPM на устройстве не проверяли.

## Покрытие

| Путь в GitVerse snapshot | Что проверено | Границы |
|---|---|---|
| `snapshot.json`, `repository.json`, `tree.json` | Идентичность проекта, ветка, pinned SHA, автор и сообщение commit; 1 321 leaf entry, дерево не помечено усечённым | REST metadata endpoint отдельно не подтвердился: конкретный `/api/v1/repos/...` вернул HTTP 404; источник доступен через Git и веб-страницу |
| `README.md:1-7`, `LICENSE:1-5`, `AGENTS.md:1-74` | README о назначении каталога KPM; лицензия GPL-3.0; формат `.plugin`/Elyx, структура `store.json`, SHA-256 и правило имён legacy-файлов по документации проекта | `AGENTS.md` — авторская документация, не спецификация клиентского API; его URL-пример относится к GitHub и расходится с текущим GitVerse каталогом |
| `store.json:1-12201` | Весь JSON: 698 ID, объединённый набор полей, URL-паттерны; сравнён с GitHub snapshot после исключения URL на всех уровнях и с Codeberg snapshot по общей части | Каталог не сопоставлялся с байтами всех 698 плагинов; значения hash/signature не валидировались для каждого артефакта |
| `.github/workflows/mirror.yml:1-120` | Push/manual triggers, замена базового Forgejo URL на ссылки GitVerse и отдельный force-push в GitVerse | Workflow прочитан статически; успешные запуски и состояние других веток/тегов не проверялись |
| `Plugins/kangel_plugins_manager.eaf` | SHA-256, размер 372 407 bytes, ZIP inventory; сравнение целого файла с тремя refs | Исходники архива не анализировались повторно: файл побайтно равен уже описанным копиям в [Codeberg источнике](plugins-store-codeberg.md) и [GitHub источнике](plugins-store.md) |

При ревью заново получены HTTP 200 с commit-pinned raw URL для `README.md`, `store.json`, `AGENTS.md`, `.github/workflows/mirror.yml`, `Plugins/kangel_plugins_manager.eaf` и `LICENSE`; все шесть SHA-256 совпали с manifest. Также повторно проверен branch raw URL `store.json`: HTTP 200 и тот же SHA-256, что у pinned commit. Это точечная проверка HTTP-ресурсов, не проверка KPM или Android runtime.

## GitVerse каталог и ссылки

`store.json` — JSON object по ID плагина. В этом commit 698 ключей; по объединению записей встречаются `url`, `name`, `version`, `author`, `description`, локализованные `description_*`, `hash`, `signature`, `status`, `min_version`, `app_version`, `icon`, `requirements`, `dependencies` и `legacy_version`. Наличие поля в объединённом наборе не означает, что оно заполнено в каждой записи.

Текущие и архивные URL записей используют `https://gitverse.ru/api/repos/bigfishtheory/Plugins-Store/raw/branch/main/...`. Это плавающий branch URL: для воспроизводимости сохраняйте commit вместе с каталогом и проверяйте байты артефакта по его hash; строка в JSON сама по себе не доказывает подлинность файла. Во время сбора raw branch endpoint отдал байты каталога с тем же SHA-256, что и pinned GitVerse `store.json`.

Workflow указывает три целевых площадки. Для шага GitVerse он сбрасывается к checkout базового SHA, заменяет ссылки Forgejo на GitVerse raw API URL и адрес репозитория на `gitverse.ru/bigfishtheory/Plugins-Store`, затем отправляет `HEAD:main` и tags. При неудаче полной отправки workflow пробует отправку в нескольких checkpoint commits. Это описанный процесс CI, а не подтверждение, что каждый запуск или push завершился успешно.

`AGENTS.md` всё ещё показывает GitHub raw URL в схеме и примере `store.json`, тогда как GitVerse `store.json` содержит GitVerse API URL. Для использования этого источника ориентируйтесь на фактический файл закреплённого GitVerse commit; пример в документации указывает GitHub URL, а фактический GitVerse endpoint берётся из pinned каталога.

## Наблюдаемые вызовы

Пакет `Plugins/kangel_plugins_manager.eaf` в GitVerse имеет тот же SHA-256, что и пакет в двух ранее собранных снимках, поэтому применимые методы относятся к тому же опубликованному KPM 1.5.4. Это наследование сведений о неизменившемся бинарном файле, не отдельное исследование GitVerse-специфичной реализации.

| Модуль / объект | Сигнатура или call-site | Назначение и контекст | Доказательство |
|---|---|---|---|
| `Store` в `kpmplugin/src/store.py` пакета KPM | `get_latest_commit_sha()`; `refresh(force=False)` | Проверка и обновление каталога в общем KPM пакете; вызывающий lifecycle, worker thread и account scope здесь заново не прослеживались — детали реализации приведены в [Codeberg странице KPM](plugins-store-codeberg.md) | [GitVerse пакет, commit `08ddcb…`](https://gitverse.ru/api/repos/bigfishtheory/Plugins-Store/raw/commit/08ddcb84661a148b66d691f4f06fd6779e67b793/Plugins/kangel_plugins_manager.eaf); SHA-256 архива совпадает с Codeberg/GitHub refs |

## Практическое применение

1. Для запросов к этому зеркалу используйте GitVerse raw URL из `store.json`, но фиксируйте SHA каталога: ссылка содержит `branch/main` и меняется вместе с веткой.
2. При сравнении зеркал исключайте URL-рекурсивно, в том числе внутри `legacy_version`; затем отдельно сравнивайте ID, версии, hashes, signatures и ограничения совместимости. В данном сравнении это отделяет простую замену домена от содержательных изменений.
3. При сверке README/инструкций с каталогом следуйте pinned каталогу для GitVerse endpoint; `AGENTS.md` пока содержит GitHub-ссылки.
4. Если требуется понять логику самого менеджера, сверяйте пакет и выводы Codeberg-страницы: архив в этих snapshot идентичен. Этот источник не добавляет самостоятельный API или подтверждение совместимости.

## Ограничения

- Утверждения о схеме и мирроринге относятся к конкретному GitVerse commit. Текущий номер commit и содержимое каталога могут измениться.
- Git smart HTTP, веб-страница и raw API доступны при сборе; REST-style metadata URL `/api/v1/repos/bigfishtheory/Plugins-Store` ответил 404. Работоспособность прочих API-путей этим не устанавливается.
- Статусы `version`, `min_version`, `hash`, `signature`, зависимости и ссылки описывают каталог, но все файлы, подписи и совместимость с целевыми клиентами отдельно не проверялись.
- Ни workflow, ни KPM, ни плагины не запускались. Runtime-проверки на Android нет.
