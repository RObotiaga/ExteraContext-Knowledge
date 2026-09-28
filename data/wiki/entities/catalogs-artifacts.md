---
type: entity
entity_id: catalogs-artifacts
date: 2026-09-27
---

# Каталоги и опубликованные артефакты

Исходник, индекс каталога, зеркало, wheel/npm и APK являются разными материалами. Сравнивайте версию, набор файлов и происхождение; совпадающий ID не гарантирует одинакового содержимого.

## Проверенные материалы

| Источник | Сведения для применения | Доказательства и проверка |
|---|---|---|
| [plugins-store](../sources/plugins-store.md) | README называет репозиторий местом хранения плагинов для Kangel Plugins Manager; страница README не является руководством по API разработки.<br>В документации hash описан как SHA-256 от байтов файла плагина. | [первичный материал](https://github.com/Kangel-Plugins/Plugins-Store/blob/513e29a07858e5dec3a8dcdc6a860fe4296f1d43/README.md#L1-L7), [первичный материал](https://github.com/Kangel-Plugins/Plugins-Store/blob/513e29a07858e5dec3a8dcdc6a860fe4296f1d43/AGENTS.md#L54-L59) · [проверка](../reviews/plugins-store.md) |
| [plugins-store-codeberg](../sources/plugins-store-codeberg.md) | The Codeberg source is Kangel/Plugins-Store on default branch main at commit 3a9417b85597127d843b0411792721f111297a0a; repository metadata reports mirror=false.<br>The bundled KPM package is ID kangel_plugins_manager version 1.5.4, declares app_version >=12.9.0 and sdk_version >=1.4.5.3, and marks itself compiled=false.<br>KPM's normal install path blocks data that fails its hash/signature check when block_untrusted_plugins is enabled; that setting defaults to true at this call site. | [первичный материал](https://codeberg.org/Kangel/Plugins-Store/commit/3a9417b85597127d843b0411792721f111297a0a), [первичный материал](https://codeberg.org/Kangel/Plugins-Store/src/commit/3a9417b85597127d843b0411792721f111297a0a/Plugins/kangel_plugins_manager.eaf) · [проверка](../reviews/plugins-store-codeberg.md) |
| [plugins-store-gitverse](../sources/plugins-store-gitverse.md) | GitVerse project bigfishtheory/Plugins-Store uses default branch main at commit 08ddcb84661a148b66d691f4f06fd6779e67b793; the commit is authored by mirror-bot with subject chore: rewrite Forgejo links to GitVerse [mirror-bot]. | [первичный материал](https://gitverse.ru/bigfishtheory/Plugins-Store) · [проверка](../reviews/plugins-store-gitverse.md) |
| [plugins-robot](../sources/plugins-robot.md) | parse_plugin_text разбирает исходник через ast.parse и извлекает только top-level Assign/AnnAssign, чьи значения проходят ast.literal_eval; код загруженного плагина при извлечении metadata не исполняется.<br>В этом parser обязательны непустые __id__, __name__, __author__, __version__; дополнительно обязателен либо __min_version__, либо __app_version__. Для __requires__ допускается только объект, остальные извлекаемые magic-поля должны быть строками. | [первичный материал](https://github.com/itsv1eds/exteraPluginsRobot/blob/79021a05ecb77c8d7fca875298ffbac5970331aa/plugin_parser.py#L89-L115), [первичный материал](https://github.com/itsv1eds/exteraPluginsRobot/blob/79021a05ecb77c8d7fca875298ffbac5970331aa/plugin_parser.py#L7-L24) · [проверка](../reviews/plugins-robot.md) |
| [exteragram-mcp-npm](../sources/exteragram-mcp-npm.md) | Официальный packument npm перечисляет только версию `1.0.0`; время её публикации — `2026-04-25T14:52:28.882Z` UTC.<br>Для tarball npm публикует SRI `sha512-H1BonRlPIu78bvMXKNe+Bv+jB9zWg/Kq1scabrieK+PU1CNw8vz6hnFGXfeD03dL6+Vrkp5fesabixLcUb2EzA==` и SHA-1 `be7558ecd720c6c4d6d836e5e64deca4622533b5`; локально скачанный tarball совпал с обоими, его SHA-256 — `151c790cf61d4e8b3066f8c408433fa7926442379b8c33b6a85e6c409bab052f`. В `dist` также есть registry signature metadata.<br>В архиве 24 `.js`, 24 `.d.ts` и 48 `.map` файлов; JS map-файлы ссылаются на `../../src/...`, но не содержат `sourcesContent`, а сами TypeScript-файлы не опубликованы. | [первичный материал](https://registry.npmjs.org/@catalystdev%2fexteragram-mcp/1.0.0), [первичный материал](https://registry.npmjs.org/@catalystdev/exteragram-mcp/-/exteragram-mcp-1.0.0.tgz) · [проверка](../reviews/exteragram-mcp-npm.md) |
| [opexgram-apk](../sources/opexgram-apk.md) | Публичный пост TechCsl/6548 содержит вложение с именем `OpexGram @TechCsl.apk`; Telegram preview показывает размер 78 MB и дату публикации 2026-08-24.<br>Описание поста TechCsl/6548 заявляет настройку пересылки сообщений по образцу iOS.<br>Пост TechCsl/6548 обещает экспорт выбранного сообщения в прозрачный PNG-стикер; архивный радар дополнительно описывает Quote Studio с экспортом PNG/JPEG и отправкой результата как стикера. Это два вторичных описания одной функции, её наличие и реализация в APK не подтверждены. | [первичный материал](https://t.me/TechCsl/6548) · [проверка](../reviews/opexgram-apk.md) |
| [opexgram-docs](../sources/opexgram-docs.md) | POST /v1/link/dev использует X-Opexgram-Dev-Key для прямой привязки developer user_id. | [первичный материал](https://github.com/yearningss/opexgram-docs/blob/31388f39340c210765471d235f7ab51a760177e0/docs/badges-api.md#L113-L132) · [проверка](../reviews/opexgram-docs.md) |
| [opexgram-announcement](../sources/opexgram-announcement.md) | Публичный embed первичного поста TechCsl/6548 указывает время публикации 2026-08-24 15:31:57 UTC (24 августа 2026 года). | [первичный материал](https://t.me/TechCsl/6548) · [проверка](../reviews/opexgram-announcement.md) |

## Связанные понятия

- [distribution](../topics/distribution.md)
- [security](../topics/security.md)
- [build](../topics/build.md)
- [testing](../topics/testing.md)

[Все сущности](index.md) · [Наблюдаемые вызовы](../apis/index.md) · [Рецепты](../recipes/index.md) · [Пробелы и версии](../gaps.md)
