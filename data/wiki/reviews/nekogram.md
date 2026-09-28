# Независимая проверка Nekogram

- Источник: `Nekogram/Nekogram`
- Snapshot: [`e924154e8d3b99a645b0521013ff9b501b28e8ce`](https://github.com/Nekogram/Nekogram/tree/e924154e8d3b99a645b0521013ff9b501b28e8ce), branch `main`, сохранён 2026-09-27
- Локальный снимок: `outputs/plugin-wiki/raw/nekogram/`; tree полный (`truncated=false`), 21 220 записей
- Проверены: source page, 31 исходных фактов, tree, manifest, snapshot/repository metadata, radar context/URL и выбранные первичные файлы
- Вердикт: **accepted-with-gaps**
- Принято после правок: **36 уникальных фактов**

## Scope и coverage

Граница — подтверждённые client-side примеры, полезные для plugin development: настройки и их перенос, аккаунтный контекст, внутренние network/helper seams, media handoff, translation, build/release и ограничения переносимости. Это крупный Telegram client, поэтому tree служит инвентарём, а обзор не претендует на полный разбор upstream или каждой Nekogram feature. Radar context говорит, что после v12.10.3 (19 сентября) новых самостоятельных функций в рассматриваемом интервале не выявлено; это вторичный контекст, а не доказательство реализации в snapshot. В сохранённом radar URL есть только ссылка releases.

Независимо просмотрены README, LICENSE, `.gitmodules`, root/module Gradle settings и properties, workflows build/release; `Extra`, `NekoConfig`, `AccountsHelper`, `PasscodeHelper`, `CloudSettingsHelper`, `CloudStorageHelper`, `BaseRemoteHelper`, `InlineBotHelper`, `WebAppHelper`, `CronetHelper`, `MessageFilterHelper`, `MediaStreamingProvider`, `MediaStreamingServer`, `Translator`, `TextWithEntitiesTranslator`, `TelegramTranslator`, `TranslatorApps`, DeepL OAuth implementation/WebView и связанные настройки. Выбранные tree paths существуют в полном snapshot; у каждого принятого fact path/range проверены на существование и line bound. README statements сохранены как `docs`, code inspection как `code`, отсутствие публичного SDK обозначено `inference`. Ни одно source inspection не названо runtime verification.

## Найденное и исправления

1. В импорте настроек исходный текст дважды сообщал, что неизвестные поля теряются. Повтор убран; отдельно оставлена практическая рекомендация проверить формат до очистки namespace.
2. В исходной coverage narrative перечислялись `ConfigHelper`/`UpdateHelper`, но runtime behavior этих классов в статье не раскрывалось. Оставлено явное ограничение покрытия remote updater/config flows, чтобы перечень не создавал впечатления полного исследования.
3. Source page проходила мимо `InlineBotHelper`, `WebAppHelper`, `CronetHelper`, `MessageFilterHelper` и реализации `TelegramTranslator`, хотя это существенные внутренние integration points. Загружены штатным `work/acquire.py`, сверены по снимку и добавлены пять отдельных фактов и evidence rows.
4. Первоначальные 31 fact имели уникальные ID и различающиеся claims; полностью идентичных claims нет. Уровни детализации соседних настроечных/network/media/translation фактов различаются по механизму или поведению и сохранены отдельными. С учётом добавленных пяти фактов всего принято 36 уникальных facts. Повторный смысл в source prose импорта устранён.
5. Build steps/secrets остаются документированными требованиями клиента; runtime availability и конфиденциальность внешних services не утверждаются. Внутренние Android classes и Telegram API не являются публичным plugin contract.

## Остаточные gaps

- Не просмотрены все feature UI/call sites в package `tw.nekomimi.nekogram`, полный caller graph, tests и runtime behavior; thread/account assumptions за пределами выбранных методов не обобщаются.
- Внешние bot/backend/provider services и OAuth/network behavior не исполнялись; DeepL/Telegram integration описывается только по коду.
- `.gitmodules` submodule contents и vendor/native upstream components не анализировались.
- Android build, CI workflow, installed app/device и media players не запускались; никаких runtime-verified claims нет.
- Snapshot — конкретный commit; утверждения не переносятся на другие Nekogram distributions/версии.

Canonical topics для будущего синтеза: Android preferences/config migration, account-scoped helpers, privacy-aware message filtering, WebView bridge validation, inline-bot networking/cache, HTTP engine readiness, content URI media streaming, entity-aware translation, Android build/release.
