---
type: code
source_id: ayugram-ios-tweak
platform: iOS
review_status: accepted-with-gaps
review: ../reviews/ayugram-ios-tweak.md
reviewer: /root/review_ayugram_ios_tweak
review_model: gpt-6-luna
accepted_facts: 15
date: 2026-09-28
---

# Ahefh/ayugram-ios-tweak

Источник: [GitHub](https://github.com/Ahefh/ayugram-ios-tweak), ветка `main`, закреплённый commit [`79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d`](https://github.com/Ahefh/ayugram-ios-tweak/tree/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d), снимок захвачен 2026-09-27 15:53:25 UTC. Полное дерево содержит `README.md` и `src/Tweak.m`; история каждого relevant path — только начальный commit `Add files via upload`. Лицензия в GitHub metadata не объявлена. SHA-256 файлов сохранён в [file-manifest.json](../../raw/ayugram-ios-tweak/file-manifest.json), снимок происхождения, история и ограничения — в [evidence.json](../../raw/ayugram-ios-tweak/evidence.json).

Это небольшой **iOS Objective-C tweak/injection пример и README о CI/CD доставке**, не Android-плагин. Исходник показывает Objective-C runtime замену UIKit метода и отложенный стартовый alert. Его нельзя представлять как ExteraGram API или Android hook contract. Фраза alert о готовности к MTProto hooks — только текст: MTProto реализация в снимке отсутствует.

## Покрытие

| Материал | Изучено | Пробелы |
|---|---|---|
| `README.md:1-48` ([pinned](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/README.md#L1-L48)) | Заявленная dylib/`optool` схема, ручной Actions запуск, `ipa_url`, artifact, Sideloadly flow | Это только docs. Workflow, сборочные команды, signing/injection scripts, IPA и подтверждение работы отсутствуют |
| `src/Tweak.m:1-54` ([pinned](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L1-L54)) | Весь код: logging macro, constructor, Objective-C runtime method lookup/replacement, main-queue callback, window lookup, alert | Нет тестов/configuration, deployment target, Telegram internal hooks, teardown/unhook или проверки на устройстве |
| `snapshot.json`, `tree.json`, `repository.json`, `file-manifest.json` | Закреплённое полное дерево, commit и хэши | Внешние Actions artifacts и состояние после pinned SHA не изучались |
| История `README.md`, `src/Tweak.m`; `radar-urls.json` | По GitHub API оба пути добавлены в одном commit; radar URLs пусты | Предыдущих ревизий релевантных путей нет |

## Runtime hook

Constructor `initializeAyuGramTweak` объявлен с `__attribute__((constructor))`; комментарий описывает вызов при загрузке dylib. Он пишет `NSLog` через макрос `AyuLog` с префиксом `[AyuGram-iOS]`, затем получает `[UITextField class]` и selector `isSecureTextEntry`. Если `class_getInstanceMethod` возвращает `Method`, код сохраняет `method_getImplementation` и заменяет её на `hook_isSecureTextEntry` через `method_setImplementation` ([код, строки 5-29](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L5-L29)). Если `Method` не найден, отдельной ошибки или повтора нет; стартовая запись «успешно загружен» выводится до этой проверки и сама по себе не подтверждает установку hook.

Replacement имеет сигнатуру `BOOL(id, SEL)` и всегда возвращает `NO`. Сохраненная `orig_isSecureTextEntry` дальше не вызывается, так что исходное поведение не делегируется. Target — общий UIKit `UITextField`, без фильтра по классам Telegram. Комментарий приписывает хуку отключение защиты содержимого на screenshots/screen recording, однако результат системой или приложением не проверялся. В коде нет teardown, восстановления IMP или отдельного unhook пути.

## UI и поток выполнения

Через 3 секунды constructor планирует блок на `dispatch_get_main_queue()` ([строки 31-32](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L31-L32)). На iOS 13+ блок выбирает первую foreground-active `UIWindowScene` из `UIApplication.connectedScenes`, затем `scene.windows.firstObject`; для более старых версий использует `UIApplication.keyWindow` ([строки 33-43](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L33-L43)). При наличии окна и `rootViewController` код показывает `UIAlertController` с кнопкой `OK` ([строки 45-50](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L45-L50)).

Это демонстрационный UI сигнал, а не надежная проверка готовности Telegram: фиксированная задержка не связана с готовностью интерфейса, `firstObject` не проверяется на key-window статус, занятая presentation hierarchy не обрабатывается. Появление alert в приложении не проверялось.

## Call-sites

| Компонент | Сигнатура/call-site | Назначение и lifecycle | Источник |
|---|---|---|---|
| Constructor | `__attribute__((constructor)) static void initializeAyuGramTweak(void)` | Инициализация при загрузке dylib, hook setup и планирование alert | [Tweak.m:15-19](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L15-L19) |
| Objective-C runtime / UIKit | `class_getInstanceMethod`, `method_getImplementation`, `method_setImplementation` для `UITextField.isSecureTextEntry` | Замена instance method, если `Method` найден; процессный iOS tweak | [Tweak.m:21-28](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L21-L28) |
| Grand Central Dispatch | `dispatch_after(..., dispatch_get_main_queue(), ^{ ... })` | Однократный callback спустя 3 секунды перед UIKit calls | [Tweak.m:31-32](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L31-L32) |
| UIKit scenes/windows | `connectedScenes`, `activationState`, `windows.firstObject`, legacy `keyWindow` | Выбор окна с ветками iOS 13+ и старых систем | [Tweak.m:33-43](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L33-L43) |
| UIKit alert | `UIAlertController`, `addAction:`, `presentViewController:animated:completion:` | Условное отображение уведомления при наличии root controller | [Tweak.m:45-50](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/src/Tweak.m#L45-L50) |

Это call-sites примера, не SDK контракт. Source не задаёт account/thread model или plugin lifecycle framework.

## README о CI/CD и установке

README заявляет использование облачного бесплатного macOS runner GitHub Actions и компиляцию `src/Tweak.m` под `arm64` в `Tweak.dylib`, копирование в `Telegram.app/Frameworks/` и добавление `LC_LOAD_DYLIB` утилитой `optool` ([строки 3-12](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/README.md#L3-L12)). Далее описан ручной запуск workflow “Build and Inject AyuGram Tweak” с необязательным `ipa_url` и ожидаемым artifact `Telegram-AyuMod-Build` ([строки 30-37](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/README.md#L30-L37)). Но полное дерево pinned commit не содержит `.github/workflows`; в нём только README и `src/Tweak.m`. Значит, инструкция CI не воспроизводится по этому снимку. Компиляция, injection, code signing и загрузка IPA не подтверждены.

README предлагает ставить `Telegram-AyuMod.ipa` на iPhone SE 2 с Windows через Sideloadly, Apple ID и доверие профилю ([строки 41-48](https://github.com/Ahefh/ayugram-ios-tweak/blob/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d/README.md#L41-L48)). Это только описанный путь, не проверенный результат установки.

## Техники и совместимость

- Для iOS tweak пример показывает цепочку constructor → lookup `Method` → сохранить original IMP → назначить replacement. Чтобы сохранить старое поведение, replacement должен явно делегировать вызов; здесь такого вызова нет.
- UIKit calls для alert отправляются на main queue. Фиксированная пауза в 3 секунды сама по себе не доказывает готовность UI.
- Текст об MTProto hooks не подкреплён imports/calls или кодом MTProto; не считайте это реализованной функцией.
- README build/injection/Actions claims имеют статус `docs`; build/runtime их не подтвердили.
- **Android/ExteraGram compatibility gap:** в коде Foundation, UIKit и Objective-C runtime, целевой артефакт — iOS dylib, описан iOS IPA injection. Нет Android `.plugin`/DEX manifest, Python/Java bridge, Android hook API или ExteraGram SDK. Общая идея method replacement не устанавливает переносимость реализации.
- Приложение, build и tests не запускались; `runtime-verified` фактов нет.
