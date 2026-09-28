# Независимое ревью: `Ahefh/ayugram-ios-tweak`

**Вердикт:** `accepted-with-gaps`  
**Проверяющий:** `/root/review_ayugram_ios_tweak` · **модель:** `gpt-6-luna`  
**Закреплённый SHA:** [`79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d`](https://github.com/Ahefh/ayugram-ios-tweak/tree/79de9c9f78e4666d4b39c3d2d72a12d1d01eae3d)  
**Уникальных фактов:** 15 из 15

## Независимое покрытие и сверка

Сверены source page, collector facts, `snapshot.json`, `tree.json`, `file-manifest.json`, `evidence.json`, `repository.json`, `radar-context.md` и `radar-urls.json`. Snapshot указывает на назначенный полный SHA, `tree_truncated` равен `false`, и дерево содержит ровно два файла: `README.md` и `src/Tweak.m`. SHA-256 сохранённых `README.md` и `src/Tweak.m` совпадают с обоими записями в file manifest.

Самостоятельно прочитаны целиком оба файла. Код занимает `src/Tweak.m:1-54`: imports Foundation/UIKit/Objective-C runtime, `AyuLog`, replacement `isSecureTextEntry`, constructor, lookup и замена IMP, задержанный main-queue callback, scene/window selection и alert. README занимает строки 1-48 и описывает заявленную dylib/`optool` схему, Actions workflow/input/artifact и установку через Sideloadly. Эти области покрыты фактами; ссылки указывают на pinned SHA и line anchors, соответствующие локальной нумерации снимка.

Радар (вторичный контекст `raw/radar.md:4327`) относит проект к iOS/build инфраструктуре, а не к Android plugin development; `radar-urls.json` пуст. Snapshot и README не содержат платформенного SDK контракта, workflow YAML, build/signing implementation или IPA. Изучение — статическая сверка исходника и документации; приложение, сборка и тесты не запускались.

## Проблемы и исправления

- Уточнён факт о constructor/hook: стартовая запись «успешно загружен» выводится до проверки `Method`, а при отсутствии метода отдельной ошибки или повторной попытки нет. Это сообщение не доказывает установку hook. Изменение отражено в source page и факте 002/010.
- Факт о README build claim дополнен документированным обещанием облачного бесплатного macOS runner; ссылка расширена до `README.md:3-12`. Статус остаётся `docs`, так как workflow отсутствует в полном pinned tree.
- Проверены все 15 ID: дубликатов ID или фактических дублей не найдено. Соседние факты намеренно сохраняют разные знания: объявления указателей/возврат `NO` и неделегирование original (001/003), hook setup и constructor lifecycle (002/010), две ветви выбора окна (007/008), а также README build, Actions artifact и install guidance (011-013). Повторное описание этих знаний в prose source page не считается отдельными фактами.
- Проверены сигнатуры и line anchors для `BOOL(id, SEL)`, `class_getInstanceMethod`, `method_getImplementation`, `method_setImplementation`, dispatch/main queue и UIKit вызовов. Все совпадают с `src/Tweak.m` на pinned SHA. Ссылки на README подтверждают только изложение документации, не успешный процесс.
- Платформенная граница сформулирована корректно: Objective-C/UIKit runtime и iOS dylib/IPA claims нельзя превращать в Android/ExteraGram plugin API. Советы остаются примерами native iOS technique; Android реализация потребовала бы отдельного источника и доказательств. Source не объявляет Theos или Xposed контракт.

## Остаточные gaps

- Внешние Actions runs/artifacts и состояние после pinned SHA не проверялись; README-ссылка на workflow не подтверждается файлом workflow в снимке.
- Не подтверждены компиляция, загрузка dylib, работоспособность замены IMP, эффект `isSecureTextEntry` на screenshots/recording, появление alert, injection, signing и установка на устройстве.
- Нет сведений о минимальной iOS версии/deployment target, teardown/unhook, обработке отсутствующего метода кроме молчаливого пропуска, готовности или занятой presentation hierarchy. Нет аккаунтной/thread модели, но для этого небольшого iOS tweak её source не заявляет.
- Лицензия отсутствует в сохранённых GitHub metadata; лицензионные права по одному снимку не установлены.
- Source page сохраняет узкую область полного репозитория из двух файлов. Выводы не дают гарантии абсолютной полноты внешних workflow, артефактов или поведения приложения.

Итог `accepted-with-gaps`: все 15 уникальных фактов подтверждены текстом файлов на закреплённом SHA или явно помечены как inference/docs, существенных Android API смешений нет. Ограничения runtime и workflow остаются явно обозначенными.
