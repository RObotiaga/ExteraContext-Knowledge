---
type: source
source_id: nagramx
platform: Android
review_status: accepted-with-gaps
review: ../reviews/nagramx.md
date: 2026-09-28
---

# NagramX (`risin42/NagramX`)

Источник: [репозиторий](https://github.com/risin42/NagramX), закреплённый снимок `dev` на commit [`2db685af00a4352c877ecf96474cbf0494284715`](https://github.com/risin42/NagramX/tree/2db685af00a4352c877ecf96474cbf0494284715), получен 2026-09-27. Лицензия репозитория — GPL-3.0. README сообщает, что проект архивирован и поддержки больше нет. Это крупный Java/Android-клиент на базе Telegram/Nekogram, а не готовый ExteraGram-плагин или SDK.

## Роль и границы

Для разработки ExteraGram-плагинов NagramX полезен как донор Android-клиентских приёмов: typed preferences, настройки-фрагменты, account-aware доступ к клиентским контроллерам, обработка запросов и сборочные сценарии. Эти классы принадлежат NagramX и сами по себе не являются публичным API ExteraGram или AyuGram; использовать их напрямую из плагина можно только при наличии отдельного подтверждения совместимости.

Радар утверждает, что один из отслеживаемых ExteraGram-совместимых форков NagramX имеет собственный plugin engine (в радарном контексте: физическая строка 35, логическая строка 434). Точное соответствие упомянутого радаром форка данному репозиторию не установлено. В выбранных first-party docs и путях Java-приложения SDK/loader не обнаружен; полнотекстовая проверка дерева по именам даёт совпадения `plugin`/`sdk` в vendored protobuf и WebRTC, поэтому этот результат нельзя считать доказательством отсутствия любых hooks. Радары и snapshot относятся к разным, не отождествлённым объектам; для идентификации форка нужны URL и commit.

## Покрытие снимка

| Прочитанный путь | Что извлечено | Граница/пропуск |
|---|---|---|
| `README.md` | Архивный статус; submodules; credentials; параметры release build и сведения о подписи | Документация, не проверка сборки или APK |
| `LICENSE` | Лицензия GPL-3.0 | Юридическая интерпретация лицензии не выполнялась |
| `.gitmodules`, `build.gradle`, `settings.gradle`, `gradle.properties`, `TMessagesProj/build.gradle` | Структура Gradle, конфигурация Android, ABI split, build credentials | Исходники submodules и полная native toolchain не загружались |
| `.github/workflows/{pr,canary,staging,release}.yml` | Триггеры release workflow, JDK/SDK setup, артефакты и этап выгрузки | Actions не запускались; секреты не получались |
| `.../nekogram/NekoConfig.java`, `.../config/ConfigItem.java` | Реестр типизированных параметров, загрузка, сериализация и сохранение | Не проверялось на устройстве; это внутренний API форка |
| `.../nekogram/NekoXConfig.java` | Хранение пользовательских Telegram API credentials и fallback на BuildConfig | Не переносить секреты в общий клиентский storage без отдельного анализа |
| `.../settings/BaseNekoSettingsActivity.java`, `.../settings/NekoSettingsActivity.java` | Lifecycle экрана настроек, ряды/ключи, adapter и действия | UI связан с классами клиента и ресурсами NagramX |
| `.../ui/NekoDelegateFragment.java` | База для message-cell callbacks, перевода текста, анимаций и Bulletin delegate lifecycle | Большой класс (63 КБ); просмотрены объявления и выбранные lifecycle/callback участки, не каждая ветвь поведения; интерфейс NotificationCenter реализован, но отдельная обработка уведомлений в выбранных участках не найдена |
| `.../menu/copy/{CopyItem,CopyPopupWrapper}.java`, `.../menu/forward/{ForwardItem,ForwardPopupWrapper}.java` | Формирование контекстных пунктов меню по контексту сообщения, media и caption | Это клиентская реализация меню, не plugin hook |
| `.../helpers/remote/BaseRemoteHelper.java` | Поиск tagged JSON-сообщений в служебном канале, callback, кэш, выбор account controller | Протокол NagramX; серверный канал и runtime не проверялись |
| Полный `tree.json` | Идентичность SHA, 31 233 записей; инвентаризация путей; вендорные совпадения по словам `plugin` и `sdk` | По одному дереву нельзя подтвердить отсутствие loader/hooks; большая часть upstream/JNI/native/submodule кода не изучалась |
| `radar-context.md`, `radar-urls.json` | Радарная формулировка о plugin engine и исторические ссылки | `radar-urls.json` пуст; URL/commit для спорного утверждения отсутствует |

## Технические факты

1. **Сборка требует submodules.** README предписывает первоначальный clone с `--recursive --shallow-submodules`; для существующего checkout — `git submodule update --init --recursive --depth=1`. Пропущенные submodules делают локальную сборку неполной.
2. **Credentials читаются Gradle с неодинаковым fallback.** README перечисляет `TELEGRAM_APP_ID`, `TELEGRAM_APP_HASH`, `KEYSTORE_PASS`, `ALIAS_NAME`, `ALIAS_PASS`. `TMessagesProj/build.gradle` сначала декодирует `LOCAL_PROPERTIES` как Base64 либо читает корневой `local.properties`; signing credentials затем допускают environment fallback независимо. Telegram app ID/hash берутся из environment только внутри ветки `properties != null`, а если `properties` не создан, остаются встроенные defaults (`6` и `eb06d4abfb49dc3eeb1aeb98ae0f581e`). Это расхождение реализации с общим прочтением README следует учитывать в CI.
3. **Есть project-specific настройки, требующие замены при форке.** README указывает собственный `google-services.json` для FCM, Google Maps API key в manifest и metadata channel ID в `BaseRemoteHelper`; channel ID задаётся числом без префикса `-100`.
4. **Release workflow способен собирать несколько ABI.** GitHub Actions checkout получает submodules, использует JDK 21 и Android SDK/NDK, запускает `TMessagesProj:assembleRelease`, публикует arm64-v8a и universal APK, затем отдельный job может отправить сборку в Telegram. Это описывает CI конфигурацию, а не успешную проверенную сборку.
5. **NekoConfig — типизированный внутренний реестр, а не plugin storage API.** `NekoConfig.addConfig(key, type, default)` создаёт `ConfigItem` и добавляет его в список; статическая инициализация вызывает `init()`/`loadConfig(false)`. Настройки разделяют один `SharedPreferences` файл `nkmrcfg`.
6. **Загрузка настроек сериализована и восстанавливается после ошибочного типа.** `loadConfig(force)` синхронизирует операции через общий `sync`, пропускает повторную загрузку без `force`, читает значения по типу, а при `ClassCastException` или неверном числовом представлении логирует ошибку, возвращает default и удаляет испорченную запись.
7. **Сеттеры `ConfigItem` сохраняют значение сразу.** `setConfigBool/Int/Long/Float/String/SetInt/MapInt` обновляют объект и вызывают `saveConfig()`. Сохранение берёт тот же `NekoConfig.sync`, пишет в `SharedPreferences.Editor` и завершает `apply()`; отдельного транзакционного API здесь не видно.
8. **Типы сложных настроек имеют разное представление.** `SetInt` сохраняется как строковый набор; `MapIntInt` сериализуется Java Object Serialization и кодируется Base64. Загрузчик при ошибке map-декодирования заменяет значение пустой map. Это локальная схема NagramX, не рекомендация для переносимого формата.
9. **Map-настройка десериализуется через `ObjectInputStream`.** Следовательно, для плагина не следует повторять эту схему для импортируемого недоверенного файла: это вывод по коду о небезопасной границе сериализации; отдельного фильтра классов в изученном участке не видно.
10. **Первая загрузка регистрирует слушателя cloud settings.** После чтения конфигурации `NekoConfig.loadConfig` регистрирует `CloudSettingsHelper.listener` на изменениях preferences только при первой загрузке и создаёт пять `DatacenterInfo`.
11. **В remote helper account выбирается в момент доступа.** `getMessagesController`, `getConnectionsManager`, `getMessagesStorage` и `getFileLoader` берут singleton по `UserConfig.selectedAccount`. Это полезный пример account-aware client code; thread-safety или поведение при переключении аккаунта в полёте не доказываются.
12. **Remote metadata загружается как JSON в сообщениях канала.** `load()` ищет сообщения с query `#<getTag()>`, лимитом 10, пустым filter и offset 0, затем удаляет удалённые сообщения, проверяет prefix и парсит suffix как JSON.
13. **Remote helper обновляет access hash при неудаче запроса.** При отсутствующем peer/нулевом access hash он разрешает username `nagramx_remote_metadata`, обновляет users/chats в controller/storage и отправляет поиск с полученным channel peer; если уже готовый peer даёт ошибку, выполняет повторный `load(true, delegate)`.
14. **Кэш remote metadata отделён от обычных настроек.** `BaseRemoteHelper` использует preferences `nekoremoteconfig`; найденный JSON хранит по тегу и timestamp, а пустой результат удаляет оба ключа. Delegate сообщается об ошибке через `onError`; success delegate в базовом методе не вызывается.
15. **Custom Telegram API credentials хранятся отдельными настройками.** `NekoXConfig` держит `custom_api`, `custom_app_id` и `custom_app_hash` в `nekox_config`; `currentAppId()`/`currentAppHash()` возвращают пользовательские данные только в режиме `API_TYPE_CUSTOM`, иначе значения `BuildConfig`.
16. **Экран настроек строится через fragment lifecycle.** `BaseNekoSettingsActivity.onFragmentCreate()` вызывает `updateRows()`, а `createView(context)` создаёт RecyclerView, adapter и click listeners. `NekoSettingsActivity` предоставляет конкретные строки/обработчики, наследуясь от этой базы.
17. **Ключи строк используются для переходов и deep-link.** `addRow(String... keys)` связывает ключ с позициями в обе стороны; `scrollToRow(key, unknown)` подсвечивает и прокручивает к известной строке либо вызывает fallback. При long press базовый экран может скопировать ссылку `.../nasettings/<fragment-key>?r=<row-key>`.
18. **Контекстное меню фильтрует пункты до отображения.** `CopyPopupWrapper` исключает текущий пункт, фото-действия если сообщение не фото или preview blurred, ссылку при `isPrivate=true` и “copy to PM” при `isPrivate=false`; оставшиеся пункты делегируют click по ID. Условие для copy-to-PM важно читать буквально: предшествующее описание ошибочно обращало ветку наоборот. `ForwardPopupWrapper` дополнительно показывает вариант без caption только когда `ForwardItem.hasCaption(selectedObject, selectedObjectGroup)` возвращает true. Это логика UI-клиента, не plugin hook.
19. **Базовый fragment очищает UI delegates и анимации в lifecycle.** `NekoDelegateFragment.onResume()` регистрирует `Bulletin.Delegate`; `onPause()` и `onFragmentDestroy()` снимают его, отменяют message-cell анимации и выключают dim overlay. Этот пример показывает, что cleanup продублирован для обоих путей выхода; он не описывает lifecycle плагина или внешний hook.
20. **Репозиторий заявляет официальную подпись APK.** README приводит package names `nu.gpu.nagram`/`nu.gpu.nagramx` и SHA-256 сертификата. Эти значения относятся только к официальным APK проекта, не проверены по бинарнику в рамках сбора и не являются способом подтвердить подпись чужой сборки.

## Полезные вызовы и точки расширения

| Модуль/класс | Сигнатура или call-site | Назначение и lifecycle/account/thread | Доказательство |
|---|---|---|---|
| `NekoConfig` | `addConfig(String k, int t, Object d)`; `loadConfig(boolean force)` | Регистрация и загрузка настроек; статическая инициализация, общий registry; поток выполнения отдельно не гарантирован | [NekoConfig.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/NekoConfig.java#L202-L283) |
| `ConfigItem` | `setConfigBool(boolean)` / `setConfigString(String)` / `saveConfig()` | Изменение и персистентная запись одного параметра; синхронизация `NekoConfig.sync` | [ConfigItem.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/config/ConfigItem.java#L80-L169) |
| `BaseRemoteHelper` | `load()`; `load(Delegate)`; `getMessagesController()` | Асинхронный MTProto поиск metadata; account — `UserConfig.selectedAccount`; callback поток не установлен | [BaseRemoteHelper.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/helpers/remote/BaseRemoteHelper.java#L21-L138) |
| `NekoXConfig` | `currentAppId()` / `currentAppHash()` / `saveCustomApi()` | Выбор сохранённых app credentials либо build defaults; статическое пользовательское состояние | [NekoXConfig.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/NekoXConfig.java#L40-L63) |
| `BaseNekoSettingsActivity` | `onFragmentCreate()`, `createView(Context)`, `addRow(String...)`, `scrollToRow(String,Runnable)` | Экран предпочтений и позиционирование строки; fragment lifecycle; UI-контекст | [BaseNekoSettingsActivity.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/settings/BaseNekoSettingsActivity.java#L90-L205) и [строки/ключи](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/settings/BaseNekoSettingsActivity.java#L231-L260) |
| `CopyPopupWrapper` | `CopyPopupWrapper(ChatActivity, MessageObject, int, boolean, PopupSwipeBackLayout, ActionBarMenuItemDelegate, ResourcesProvider)` | Построение меню для выбранного сообщения; callback возвращает ID действия в вызывающий экран | [CopyPopupWrapper.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/menu/copy/CopyPopupWrapper.java#L15-L47) |
| `ForwardPopupWrapper` | `ForwardPopupWrapper(ChatActivity, MessageObject, GroupedMessages, PopupSwipeBackLayout, ActionBarMenuItemDelegate, ResourcesProvider)` | Пересылка одиночного/сгруппированного сообщения; пункт «без подписи» зависит от caption; выбор возвращает ID | [ForwardPopupWrapper.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/menu/forward/ForwardPopupWrapper.java#L15-L37) |
| `NekoDelegateFragment` | `onResume()`, `onPause()`, `onFragmentDestroy()` | Lifecycle регистрации/снятия Bulletin delegate и остановки анимаций; NagramX-specific fragment behavior | [NekoDelegateFragment.java](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/TMessagesProj/src/main/java/tw/nekomimi/nekogram/ui/NekoDelegateFragment.java#L753-L781) |
| Release workflow | `./gradlew TMessagesProj:assembleRelease` | CI сборка после checkout submodules; загружает ABI artifacts и отдельным job отправляет в Telegram | [release.yml](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/.github/workflows/release.yml#L17-L105) |

## Техники и рецепты для адаптации

- **Настройка с ограниченной схемой:** хранить собственные plugin preferences в приватном namespace плагина и задавать default/type явно. Пример NagramX — `ConfigItem`; не привязывать переносимый плагин к `NekoConfig` без подтверждения host API.
- **Аккаунтный запрос:** если API клиента мультиаккаунтный, получать controller/connection/storage из активного account на границе операции и согласовать account ID с дальнейшими callbacks. Пример `BaseRemoteHelper` читает `UserConfig.selectedAccount`, но не решает гонку при смене аккаунта.
- **Контекстное действие:** вычислить пригодность действия по media/privacy/current action до добавления пункта в меню, а нажатие передать через callback. В NagramX это реализовано в wrapper; в ExteraGram плагине нужен подтверждённый menu hook.
- **Fork build:** использовать submodules и вынести app credentials, signing passwords, Firebase и Maps keys в локальные конфиги/секреты; не коммитить секретные значения. Этот рецепт следует из README/CI конфигурации и не подтверждает её безопасность целиком.

## Ограничения, расхождения и непроверенное

- Runtime-приложение и сборка не запускались; статус всех наблюдений — `code` или `docs`, не `runtime-verified`.
- Plugin SDK, manifest, loader, lifecycle plugin и hook signatures для этого снимка не подтверждены. Классы NagramX нельзя документировать как API ExteraGram/AyuGram.
- Радарная запись про собственный plugin engine не имеет URL в приложенном `radar-urls.json`; найденная фраза в контексте относится к «форку NagramX», но точная идентичность с `risin42/NagramX` не подтверждается. Нужны ссылка/commit на этот форк или отдельный исходник.
- Снимок содержит свыше 31 тыс. файлов; полный Telegram upstream, JNI/native code, все resource paths и submodules не изучались. Выборка ограничена перечисленными изменёнными/релевантными путями.
- Репозиторий объявлен архивным. Нельзя по этому снимку заключать, что эти детали совпадают с актуальными ExteraGram/AyuGram API или поддерживаемым клиентским runtime.
- Исторические коммиты, упомянутые в радаре, для NagramX не указаны; `radar-urls.json` пуст.

## Источники

- [README.md](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/README.md)
- [Полное дерево на закреплённом commit](https://github.com/risin42/NagramX/tree/2db685af00a4352c877ecf96474cbf0494284715)
- [Лицензия](https://github.com/risin42/NagramX/blob/2db685af00a4352c877ecf96474cbf0494284715/LICENSE)
