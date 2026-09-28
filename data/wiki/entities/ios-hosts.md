---
type: entity
entity_id: ios-hosts
date: 2026-09-27
---

# Хосты и плагины iOS

Python-логика и платформенная подготовка данных могут разделяться. Переносимость определяется входом, выходом и разрешенными действиями хоста; маркеры загрузчика и доступ к Swift/Objective-C устанавливают по конкретной реализации.

## Проверенные материалы

| Источник | Сведения для применения | Доказательства и проверка |
|---|---|---|
| [mioplugin](../sources/mioplugin.md) | Исходящие текстовые примеры регистрируют add_on_send_message_hook(priority=...) и возвращают HookResult(DEFAULT) либо HookResult(MODIFY, message=...).<br>Пример Message Counter регистрирует MAIN_MENU элемент через MenuItemData, а Quick Tools — MESSAGE_CONTEXT_MENU item.<br>Antispam Guard использует окно из 12 входящих текстов, пороги 4 повторов/5 invite-ссылок/6 URL и cooldown toast 90 секунд; блокирования или удаления сообщений нет. | [первичный материал](https://github.com/fuckramochka/mioplugin/blob/b5eb7ee542635ae52cf5eabc622f1944e4148a56/plugins/code_formatter/plugin.py#L18-L35), [первичный материал](https://github.com/fuckramochka/mioplugin/blob/b5eb7ee542635ae52cf5eabc622f1944e4148a56/plugins/message_counter/plugin.py#L19-L35), [первичный материал](https://github.com/fuckramochka/mioplugin/blob/b5eb7ee542635ae52cf5eabc622f1944e4148a56/plugins/antispam_guard/plugin.py#L22-L85) · [проверка](../reviews/mioplugin.md) |
| [vibogram](../sources/vibogram.md) | ViboGram описывает себя как экспериментальный личный iOS Telegram-клиент-форк и подчёркивает, что не аффилирован со Swiftgram, AyuGram4A или Margelet; README отмечает лицензионную неопределённость upstream Telegram-iOS.<br>Pinned snapshot SHA совпадает с SHA дерева; 23 сохранённых файла совпадают с manifest SHA-256, а их permalinks привязаны к тому же SHA.<br>On-send hook ищет marker в первой строке файла (с удалением пробелов по краям этой строки); для каждого отмеченного плагина вызывает transform({text: ...}), передавая результат следующему в filename-алфавитном порядке. | [первичный материал](https://github.com/vibeDN/ViboGram/blob/5f51b6befb2ce9370ea9acf40759d71053db2776/README.md#L31-L42), [первичный материал](https://github.com/vibeDN/ViboGram/commit/5f51b6befb2ce9370ea9acf40759d71053db2776), [первичный материал](https://github.com/vibeDN/ViboGram/blob/5f51b6befb2ce9370ea9acf40759d71053db2776/Swiftgram/SGPython/Sources/SGPythonRuntime.swift#L580-L613) · [проверка](../reviews/vibogram.md) |
| [reqgram](../sources/reqgram.md) | ReqGram — Swift/iOS-клиент, встроенный AyuGram модуль собран как Bazel swift_library; это не Android .plugin SDK и Swift-модуль напрямую переносимым API не является.<br>AyuGram каталог исключён из iCloud backup, защищён completeUntilFirstUserAuthentication, вложения разделены по accountId/peerId, а root каталог создаётся отдельно от чистого вычисления пути.<br>Ephemeral media capture допускает только отдельные входящие cloud voice/instant-video с явным TTL/view-once; секретные чаты, copy-protected сообщения, action media и remote-only/partial ресурсы исключаются. | [первичный материал](https://github.com/voterol/ReqGram/blob/0400a92db3415411c0430d5bbc360efc1b5ee175/Swiftgram/AyuGram/BUILD#L1), [первичный материал](https://github.com/voterol/ReqGram/blob/0400a92db3415411c0430d5bbc360efc1b5ee175/Swiftgram/AyuGram/Sources/AyuStorage.swift#L16), [первичный материал](https://github.com/voterol/ReqGram/blob/0400a92db3415411c0430d5bbc360efc1b5ee175/submodules/TelegramCore/Sources/AyuGram/AyuHooks.swift#L549) · [проверка](../reviews/reqgram.md) |
| [ayugram-ios-tweak](../sources/ayugram-ios-tweak.md) | Исходник объявляет статические типизированные указатели на original и replacement реализации для Objective-C instance method с ABI-подписью BOOL(id, SEL); replacement hook_isSecureTextEntry всегда возвращает NO.<br>На iOS 13+ код перебирает UIApplication.connectedScenes, выбирает foreground-active UIWindowScene и берет windows.firstObject как keyWindow.<br>README заявляет облачный бесплатный macOS runner GitHub Actions, сборку src/Tweak.m для arm64 в Tweak.dylib, добавление dylib в Telegram.app/Frameworks и внедрение LC_LOAD_DYLIB через optool, но эти шаги документированы только текстом. | [первичный материал](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L8-L13), [первичный материал](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L33-L40), [первичный материал](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/README.md#L3-L12) · [проверка](../reviews/ayugram-ios-tweak.md) |

## Связанные понятия

- [portability](../topics/portability.md)
- [hooks](../topics/hooks.md)
- [media](../topics/media.md)
- [security](../topics/security.md)
- [ui](../topics/ui.md)
- [build](../topics/build.md)

[Все сущности](index.md) · [Наблюдаемые вызовы](../apis/index.md) · [Рецепты](../recipes/index.md) · [Пробелы и версии](../gaps.md)
