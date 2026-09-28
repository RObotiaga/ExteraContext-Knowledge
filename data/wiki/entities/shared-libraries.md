---
type: entity
entity_id: shared-libraries
date: 2026-09-27
---

# Библиотеки, события и общие помощники

Библиотеки помогают уменьшить повторяемый код, но их глобальное состояние и правила cleanup требуют явного владельца. Функцию считают экспортированной после проверки объявления, импорта и публичной поверхности.

## Проверенные материалы

| Источник | Сведения для применения | Доказательства и проверка |
|---|---|---|
| [altylib](../sources/altylib.md) | Снимок AltyLib — один ExteraGram plugin-файл версии 1.0.4 с минимальной версией клиента 11.9.1; это Android/ExteraGram-модуль, не независимый Python SDK.<br>JsonCacheFile размещает JSON в cache-папке рядом с plugin-файлом, создаёт каталог и при отсутствующем/битом JSON восстанавливает default.<br>tasks_schedule использует один daemon scheduler thread с секундным polling и выполняет задачи через run_on_queue. | [первичный материал](https://github.com/Altuskhins/AltyLib/blob/f2674328a24fd24ebc01683f2f84b92ed8470630/Altylib.plugin#L54-L60), [первичный материал](https://github.com/Altuskhins/AltyLib/blob/f2674328a24fd24ebc01683f2f84b92ed8470630/Altylib.plugin#L104-L138), [первичный материал](https://github.com/Altuskhins/AltyLib/blob/f2674328a24fd24ebc01683f2f84b92ed8470630/Altylib.plugin#L1177-L1233) · [проверка](../reviews/altylib.md) |
| [zwylib](../sources/zwylib.md) | ZwyLib описана как библиотека-помощник для Python-плагинов exteraGram; вводная требует установить её и импортировать модуль zwylib, прежде чем пользоваться её API.<br>Документация заявляет один фоновый поток и asyncio event loop, общий для всех плагинов; поток запускается при первом AsyncManager.run_task.<br>Документация утверждает, что задачи, созданные через async_manager, отслеживаются по ID вызвавшего плагина и автоматически отменяются при его выгрузке. | [первичный материал](https://github.com/Zwylair/zwylib-docs/blob/69d56b4b64e5e61b47646282eb5ec749415ac142/content/index.mdx#L3-L20), [первичный материал](https://github.com/Zwylair/zwylib-docs/blob/69d56b4b64e5e61b47646282eb5ec749415ac142/content/async.mdx#L3-L44), [первичный материал](https://github.com/Zwylair/zwylib-docs/blob/69d56b4b64e5e61b47646282eb5ec749415ac142/content/async.mdx#L38-L86) · [проверка](../reviews/zwylib.md) |
| [catalib](../sources/catalib.md) | Embedded finder регистрирует подмодули из словаря в `sys.meta_path`, а package globals восстанавливаются так, чтобы пакетные и относительные импорты разрешались по имени `<plugin_id>.*`.<br>Повторная активация удаляет прежние finder и подмодули этого plugin_id из `sys.modules`, затем очищает только вендоренные `catalib.*`, сохраняя host-пакет catalib с файловым origin.<br>Публичный `catalib.support` фасад экспортирует 14 тематических SDK-модулей: декларативные hooks/menu/Xposed, настройки, Android/client/files/reflection/formatting/dialogs/bulletins/proxy/class-name helpers; документация описывает эти модули как SDK-parity слой с функциональными offline stubs, работающий на устройстве через SDK. | [первичный материал](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/runtime/bootstrap.py#L53-L69), [первичный материал](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/runtime/bootstrap.py#L108-L145), [первичный материал](https://github.com/cataIystdev/catalib/blob/5c9871245d77494f33b7e81b1050d29478dcbaa8/src/catalib/support/__init__.py#L10-L84) · [проверка](../reviews/catalib.md) |
| [exteralib](../sources/exteralib.md) | patchJar копирует ZIP/JAR записи с теми же именами; он не выбирает пакеты или Telegram/ExteraGram классы, а README-обещание извлечения core classes не подтверждено фильтрацией в коде. | [первичный материал](https://github.com/fossSquad/exteralib/blob/75edeba764a7a8ec8d30bdf5ae6c47a7f2377b0a/src/main/java/com/exteralib/Main.java#L57-L88) · [проверка](../reviews/exteralib.md) |

## Связанные понятия

- [hooks](../topics/hooks.md)
- [lifecycle](../topics/lifecycle.md)
- [requests](../topics/requests.md)
- [storage](../topics/storage.md)
- [threading](../topics/threading.md)
- [portability](../topics/portability.md)

[Все сущности](index.md) · [Наблюдаемые вызовы](../apis/index.md) · [Рецепты](../recipes/index.md) · [Пробелы и версии](../gaps.md)
