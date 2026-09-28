# Независимая проверка NagramX

- Источник: `risin42/NagramX`
- Закреплённый commit: [`2db685af00a4352c877ecf96474cbf0494284715`](https://github.com/risin42/NagramX/tree/2db685af00a4352c877ecf96474cbf0494284715), branch `dev`
- Снимок: `outputs/plugin-wiki/raw/nagramx/`, captured 2026-09-27; tree полный (`truncated=false`), 31 233 записей
- Проверены: `work/nagramx-facts.json`, `wiki/sources/nagramx.md`, `tree.json`, `file-manifest.json`, `snapshot.json`, `repository.json`, `radar-context.md`, `radar-urls.json`, все загруженные первичные файлы
- Вердикт: **accepted-with-gaps**
- Принято: **26 уникальных фактов**

## Scope и покрытие

Граница этой страницы — полезные для разработки плагинов клиентские примеры и подтверждённые интеграционные точки, а не описание всего Telegram upstream. Радар отдельно говорит об ExteraGram-совместимом форке NagramX со своим plugin engine (radar-context physical line 35 / logical line 434). В радарном пакете нет адреса источника (`radar-urls.json` пуст), поэтому определить репозиторий/commit этого форка по данным снимка нельзя. Нельзя переносить это утверждение на `risin42/NagramX`: это разные, не отождествлённые provenance.

Сверены README и лицензия; `.gitmodules`, корневые Gradle/settings файлы, `TMessagesProj/build.gradle`; все четыре workflow (`pr`, `canary`, `staging`, `release`); NekoConfig, ConfigItem, NekoXConfig, BaseRemoteHelper, BaseNekoSettingsActivity и NekoSettingsActivity; NekoDelegateFragment; CopyItem/CopyPopupWrapper и ForwardItem/ForwardPopupWrapper. Полный tree использован для идентификации SHA и путевой инвентаризации; `file-manifest.json` содержит полученные снимки выбранных файлов. Существенные подтверждённые темы охвачены: build inputs и workflow, release/upload separation, preferences и сериализация, account-aware client access, remote metadata запрос/кэш/retry, fragment lifecycle, settings rows и фильтрация copy/forward UI actions. Статусы оставлены `docs`, `code` или `inference`; успешная сборка и runtime поведение не заявляются.

## Найденные проблемы и исправления

1. В исходном факте о build credentials environment fallback для Telegram app ID/hash был описан слишком широко. В коде signing credentials допускают env fallback независимо, а `TELEGRAM_APP_ID`/`TELEGRAM_APP_HASH` из environment рассматриваются только внутри ветки, где `properties != null`; иначе используются встроенные defaults. Исправлены факт и source page, с указанием несовпадения с широким прочтением README.
2. Утверждение об отсутствии в полном tree имён `plugin`, `sdk` или `hook` было слишком сильным: tree содержит vendored protobuf `plugin.*` и WebRTC `sdk` пути. Исправлены формулировки: в выбранных first-party docs и путях Java-приложения собственный plugin SDK/loader не обнаружен, но инвентаризация имени файла не доказывает отсутствие hooks.
3. Факт о `CopyPopupWrapper` инвертировал privacy-ветку для `ID_COPY_IN_PM`: код исключает этот пункт при `isPrivate=false`, а link — при `isPrivate=true`. Исправлены факт и описание страницы по условиям исходного кода.
4. В fact packet не было двух релевантных наблюдений, уже охваченных исходниками страницы: cleanup Bulletin delegate/message animations при fragment pause/destroy и caption-sensitive пункт пересылки. Добавлены факты `nagramx-025` и `nagramx-026` с точными путями.
5. Исправлена опечатка `NagramConfig` на `NekoConfig`.

Внутренних повторов, требующих схлопывания, в 26 фактах не найдено: соседние storage факты описывают различные механизмы; два факта BaseRemoteHelper делят один метод, но покрывают разные ветви — запрос/разбор и обновление access hash. Пересечения с другими Nagram-подобными источниками допустимы как отдельные подтверждения с собственным commit и provenance; для синтеза подходят канонические темы build configuration, Android preferences, lifecycle cleanup, account-aware requests и context-menu filtering. Не объединять утверждение о plugin engine радара с snapshot `risin42/NagramX`.

## Остаточные пробелы

- Точный ExteraGram-совместимый форк из радарной записи не идентифицирован: отсутствует URL/commit. Его plugin engine/API остаётся непроверенным.
- Содержимое большинства first-party классов, всего крупного Telegram upstream, JNI/native и vendored submodules построчно не изучено; submodules не загружались как исходники. Выборка достаточна для указанного донорского scope, но не для заявления об абсолютной полноте клиента.
- Gradle workflow не запускался, артефакты/APK не проверялись по заявленному signing certificate, live server metadata и runtime/device behavior не проверялись. CI secrets недоступны и не нужны для подтверждения заявлений о конфигурации файлов.
- В BaseRemoteHelper выбор account опирается на `UserConfig.selectedAccount`; стабильность account между async callback и переключением account в полёте не устанавливалась.
- NekoDelegateFragment — большой класс; прочитаны API объявления и выбранные callbacks/lifecycle участки, а не каждая ветвь. Полная модель его notification behavior и все message-cell hooks остаются вне охвата.

