---
type: source-review
source_id: reqgram
reviewer: /root/review_reqgram
model: gpt-6-luna
verdict: accepted-with-gaps
reviewed_at: 2026-09-28
---

# Независимая проверка voterol/ReqGram

## Область и закреплённая версия

Проверен `voterol/ReqGram`, commit [`0400a92db3415411c0430d5bbc360efc1b5ee175`](https://github.com/voterol/ReqGram/tree/0400a92db3415411c0430d5bbc360efc1b5ee175), указанный в `snapshot.json`; `tree.json` помечен как полный. Сборщик — `/root/collect_reqgram`, проверяющий — `/root/review_reqgram`, модель `gpt-6-luna`.

Повторно сверены файлы и относящиеся к заданию разделы snapshot, `file-manifest.json`, `radar-context.md`, `radar-urls.json`, идентичность репозитория/снимка, README (149 строк), конфигурация версий и workflow. В коде независимо прослежены Bazel BUILD, AyuGram storage/message/filter/remote-badge/streamer реализации, TelegramCore hooks/delete intent/synthetic marker, TelegramUI badge mapping, settings entry points, ReqGram gift flow и animation preview. Отдельно прочитаны релевантные build/version/Watch участки `build-system/Make/Make.py` и `ProjectGeneration.py`; выполнение сборки, runtime и тестов не проводилось.

## Независимое покрытие

По `tree.json` (33 401 entries, `truncated: false`) для AyuGram/ReqGram выделены `Swiftgram/AyuGram/BUILD`, `REQGRAM_BADGES_SPEC.md`, и `Sources/{AyuFilters,AyuMessageStore,AyuRemoteConfig,AyuSavedMessage,AyuStorage,AyuStreamerMode,AyuUtils,ReqGramBadgeConfiguration}.swift`; `submodules/TelegramCore/Sources/AyuGram/{AyuDeleteIntent,AyuHooks,AyuSettingsSignal,AyuSyntheticMessageAttribute}.swift`; `submodules/TelegramUI/Components/EmojiStatusComponent/Sources/{AyuBadges,ProjectBadgeInfoController}.swift`; `Swiftgram/SGSettingsUI/Sources/{AyuSettingsController,ReqGramSettingsController}.swift`, `SGProUI/Sources/AppBadgeSelectorController.swift`, `SGItemListUI/Sources/SGTextAnimationPreviewItem.swift`, `SGAppBadgeOffset/Sources/SGAppBadgeOffset.swift`; а также `versions.json`, `.gitmodules`, `.github/workflows/build.yml` и `build-system/Make/{Make.py,ProjectGeneration.py}`. README указывает на `Swiftgram/SGAppGroupIdentifier/Sources/SGAppGroupIdentifier.swift`, но этот файл отсутствует в manifest и не был запущен/получен. Это согласуется с выбранной границей «полезные донорские примеры», а не полный обход всех upstream entries.

Радар описывает ReqGram как свежий iOS-порт AyuGram с Ghost Mode, локальной историей, Gift ID, текстовыми анимациями и бейджами. README подтверждает собственное позиционирование, но описывает дополнительно импорт/экспорт локальной истории, оформление и ограничения приватности. Источник правильно квалифицирован как iOS client/module, а его Swift/Postbox hooks не представлены Android plugin API.

## Результаты проверки и исправления

- Основные 30 исходных фактов подтверждаются соответствующими pinned source paths. Точные версии, storage/path guards, delete/edit ordering, account-scoped one-shot intent, bounded media capture, regex policies, source-isolated badge fetch/cache/parsing, project badge UI и send-by-ID flow имеют конкретные первичные доказательства. Заявлений о выполненных runtime-проверках нет.
- Исправлена ссылка `reqgram-030`: она теперь ведёт к реализации `ReqGramBadgeConfiguration.swift`, а evidence path указывает реальные фрагменты спецификации с её статусом и перечнем ещё ожидаемых значений. Несовпадение между спецификацией и константами кода оставлено явно: наличие endpoint/donation URL в этом SHA не доказывает доступность production service.
- Покрытие README/build было слишком узким. Добавлены существенные наблюдения о локальной конфигурации и требованиях к clone, App Group fallback без авто-миграции, различии iOS extensions и ReqGram plugins, IPA signing, Xcode version override и известной диагностике. Изучение build scripts дополнено замечанием о `--disableProvisioningProfiles`, которое объявлено в `Make.py`, но не передаётся в Bazel из `ProjectGeneration.py`, и отдельными требованиями `--embedWatchApp` к device config, Watch API credentials и distribution profile.
- Расширена таблица покрытия и раздел сборки source page; документационные утверждения отделены от статического наблюдения кода. Перед генерацией Xcode source page теперь предупреждает о закрытии уже запущенного Xcode, а сборка/подпись не объявлены выполненными.
- В `work/reqgram-facts.json` теперь 34 уникальных ID (`reqgram-001`…`reqgram-034`), без повторяющихся ID и точных повторов claim. `reqgram-027` расширен требованиями локальной среды/секретов; добавлены `reqgram-031`…`reqgram-034` для App Group документации и сборки/диагностики. Связанные факты о metadata vs bytes, hook vs store semantics и README vs кодовом badge contract оставлены раздельными, так как фиксируют разные доказательства или ограничения. Canonical topics для последующего межисточникового синтеза — `storage`, `security`, `hooks`, `requests`, `ui`, `build`, `debug`, `portability`, `accounts`, `media`.

## Остаточные пробелы

1. `Swiftgram/SGAppGroupIdentifier/Sources/SGAppGroupIdentifier.swift`, на который ссылается README при описании fallback, отсутствует среди полученных файлов. Переход между App Group и `Application Support/TelegramContainer` подтверждён только как заявление README; его реальное условие выбора и возможные миграционные детали по коду не установлены.
2. Ghost Mode, импорт/экспорт локального архива, полные настройки медиа, premium/appearance hooks и все шесть встроенных плагинов не прослежены по всем UI/core call-sites. README/настройки доказывают заявленную или отображаемую поверхность функций, не каждый runtime эффект.
3. Не прочитаны все тесты и все integration call-sites большого upstream дерева; отдельный test target ReqGram/AyuGram по имени в дереве не выделен. Сборка CI, устройство, серверы бейджей и совместимость разных версий iOS не проверялись. README говорит, что сборка проверялась на iOS 16.7.10, но воспроизводимого протокола для этого заявления нет.
4. README указывает CI runner `macos-13` и workflow выбирает Xcode 26.2; совместимость этой пары и успешный запуск по одному workflow файлу неизвестны. GitHub metadata сообщает `license: null`; требования upstream-лицензий изложены в README, но конкретная лицензия данного репозитория не определена.
5. Внешние Android-аналоги ReqGram-плагинов не исследовались. Любой перенос остаётся идеей для отдельной реализации на фактическом Android plugin SDK.

## Вердикт

**accepted-with-gaps.** Снимок подтверждает ценные клиентские примеры, и исправленные 34 факта имеют ограниченную, конкретную доказательную область. Открытые ограничения по отсутствующему App Group файлу, неполной трассировке остальных продуктовых функций и отсутствию runtime/build-проверки перечислены выше; вердикт не подразумевает совместимость iOS/Android или работоспособность неподтверждённых функций.
