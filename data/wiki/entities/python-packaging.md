---
type: entity
entity_id: python-packaging
date: 2026-09-27
---

# Упаковка многофайлового Python

Bundling исходников в один файл и Elyx-архив с entry/assets/refmap дают разные модели импорта. Границу выбирают по существующему loader и поведению зависимостей, а выводы про один упаковщик не распространяют на другой.

## Проверенные материалы

| Источник | Сведения для применения | Доказательства и проверка |
|---|---|---|
| [catalib](../sources/catalib.md) | catalib преобразует дерево `src/` в один Python bundle, встраивая исходный текст каждого найденного модуля и runtime-загрузчик.<br>Embedded finder регистрирует подмодули из словаря в `sys.meta_path`, а package globals восстанавливаются так, чтобы пакетные и относительные импорты разрешались по имени `<plugin_id>.*`.<br>Pipeline записывает одинаковое содержимое в `<id>.py` и `<id>.plugin` внутри настроенного out-каталога (по умолчанию `dist`). | [первичный материал](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/bundler/compiler.py#L86-L120), [первичный материал](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/runtime/bootstrap.py#L53-L69), [первичный материал](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/cli/_pipeline.py#L59-L73) · [проверка](../reviews/catalib.md) |
| [official-sdk](../sources/official-sdk.md) | Introduction указывает SDK 1.4.4.3, Python 3.11 и рекомендует exteraGram 12.5.1+.<br>Метаданные single-file плагина статически разбираются из констант верхнего уровня; обязательны __id__ и __name__.<br>file_utils предоставляет helpers каталогов приложения, ensure_dir_exists, list_dir, чтение и запись текста/байтов, а также delete_file; ошибка чтения возвращает None и записывается в log. | [первичный материал](https://plugins.exteragram.app/docs), [первичный материал](https://plugins.exteragram.app/docs/plugin-class), [первичный материал](https://plugins.exteragram.app/docs/file-utils) · [проверка](../reviews/official-sdk.md) |
| [elyxbuilder-shareui](../sources/elyxbuilder-shareui.md) | CLI-инструмент регистрирует `elyb` как `elyb.cli:main`; команда build передаёт режимы AST и compile в одну функцию `runBuild`. | [первичный материал](https://github.com/shareui/ElyxBuilder/blob/e45963fe787938ebc9a8abb3a3794b232fb72e97/package/src/cli.py#L14-L35) · [проверка](../reviews/elyxbuilder-shareui.md) |
| [elyxbuilder-kangel](../sources/elyxbuilder-kangel.md) | README и EN docs заявляют Python >=3.10, Python 3.11 только для .pyc compilation, pyzipper только для шифрования архива.<br>elyb new генерирует refmap yaml/json, metadata yaml/json, .elyxbuilder config, source/resource/locales каталоги и JSON-файлы strings_en.json/strings_ru.json. | [первичный материал](https://github.com/Kangel-Plugins/ElyxBuilder/blob/b6db59093324dc5148f811c9058a6c1414fbb849/docs/en/en.md#L13-L18), [первичный материал](https://github.com/Kangel-Plugins/ElyxBuilder/blob/b6db59093324dc5148f811c9058a6c1414fbb849/package/src/cmds/new.py#L604-L710) · [проверка](../reviews/elyxbuilder-kangel.md) |
| [packit](../sources/packit.md) | packit/meta.yml объявляет ID shareui_packit, версию 1.0.0-dev.1, минимум приложения >=12.9.0 и SDK >=1.4.5.0; это требования этого снимка PackIt.<br>InstallIndex.set_pending записывает plugin_info и repository ID под lock; commit_pending извлекает и очищает pending под тем же lock перед записью результата установки.<br>DexLoader кэширует единый InMemoryDexClassLoader и Class objects, загружая packit.dex из ByteBuffer с parent classloader хост-приложения. | [первичный материал](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/meta.yml#L1-L8), [первичный материал](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/utils/InstallIndex.py#L122-L144), [первичный материал](https://github.com/shareui/packit-source/blob/01e9673c49b9a44929fe017b61b664fbaaaa159e/packit/src/python/core/DexLoader.py#L35-L70) · [проверка](../reviews/packit.md) |

## Связанные понятия

- [build](../topics/build.md)
- [storage](../topics/storage.md)
- [portability](../topics/portability.md)
- [distribution](../topics/distribution.md)

[Все сущности](index.md) · [Наблюдаемые вызовы](../apis/index.md) · [Рецепты](../recipes/index.md) · [Пробелы и версии](../gaps.md)
