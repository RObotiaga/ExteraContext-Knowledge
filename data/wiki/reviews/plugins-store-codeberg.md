# Независимая проверка: `plugins-store-codeberg`

**Вердикт: `accepted-with-gaps`.** Проверен `Kangel/Plugins-Store` на Codeberg commit [`3a9417b85597127d843b0411792721f111297a0a`](https://codeberg.org/Kangel/Plugins-Store/commit/3a9417b85597127d843b0411792721f111297a0a), branch `main`, по сохранённым первичным данным от 2026-09-28. Код изучался статически; KPM и workflow не запускались.

## Сверка

Recursive-tree снимок содержит первые 1 000 элементов и отмечен `truncated`. В его доступной части проверены корневые `README.md`, `AGENTS.md`, `LICENSE`, `.github/workflows/mirror.yml`, `Plugins/kangel_plugins_manager.eaf` и каталог `legacy_versions/`; `store.json` дополнительно получен по raw URL, закреплённому за commit. Полное дерево и артефакты всех записей не проверялись.

Независимо пересчитан SHA-256 каждого из **17** файлов `raw/plugins-store-codeberg/file-manifest.json`; все совпали. SHA-256 Codeberg `store.json` — `3bb0213134465062b7094ad2d156c7fb07154c461b4146514d5c517c06c7edf7`. KPM `.eaf` — `554815b906a155210f02fdd4de76c66ce4cf1fcba34b4e4651f143bc0b216625`; Git blob SHA-1 — `0331fe037f39b6a26debd0f87d50a81d546d9149`. Его bytes совпадают с архивом в GitHub snapshot `513e29a07858e5dec3a8dcdc6a860fe4296f1d43`. Равенство подтверждено только для этого файла и двух refs.

Пересчёт `store.json`: Codeberg — 700 ID, GitHub snapshot — 698; только в Codeberg `custom_gifts` и `spam_collapse`. Среди общих записей 257 значений `legacy_version` отличаются после исключения только верхнего `url`; исключение URL на всех уровнях снимает 255 различий как зеркальные переписывания ссылок. Реальные metadata-различия остаются у `plugin_guard` и `camera_enhancer` (текущие `version`, `hash`, `signature`); у второго также `min_version`. В legacy-данных этих ID отличаются хеши/подписи.

Все исходные **18 фактов** сверены с pinned raw-файлами, данными каталога и выбранными модулями `.eaf`; важные evidence hashes отражены в manifest и выше. Сборщик пропустил релевантный `AGENTS.md`, поэтому добавлены ещё три документальных факта: формат `.plugin`/Elyx ZIP, SHA-256 по bytes и правило сохранения legacy-файлов при коллизии. Это соглашения репозитория, не нормативная спецификация SDK. Итог — **21 уникальный факт, 21 уникальный ID, без точных дублей**; все внесены в root pipeline как accepted facts.

## Остаточные пробелы

Дерево Codeberg обрезано; 700 артефактов не сверялись поштучно с hash/signature. Не исследованы все модули KPM, запуск Actions, состояние остальных зеркал и поведение на Android. Эти ограничения обосновывают `accepted-with-gaps`.
