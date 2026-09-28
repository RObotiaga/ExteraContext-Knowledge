---
type: review
source_id: packit
reviewer: /root/review_packit
model: gpt-6-luna
date: 2026-09-28
verdict: accepted-with-gaps
---

# Независимая проверка shareui/packit-source

## Область и pinned source

Проверен `shareui/packit-source`, commit `01e9673c49b9a44929fe017b61b664fbaaaa159e`, снимок от 2026-09-27. Идентичность repo, commit permalink и commit description сверены с GitHub; страница GitHub подтверждает Watcha (#308), изменения metadata/locales и исправления deeplink call-sites. Поле `sha` в сохранённом `tree.json` повторяет requested commit SHA, а не отдельный корневой Git tree object SHA, поэтому source page больше не называет его tree object hash.

Рекурсивное дерево содержит 430 записей: 341 blob-файл и каталоги. После независимого получения трёх пропущенных текстовых файлов (`libs/libexport/crypto.hpp`, `libs/libexport/exportbin.hpp`, `packit/LICENSE`) manifest содержит 276 файлов; SHA-256 каждого локального файла совпадает с manifest. Nested `packit/LICENSE` также GPLv3. Оставшиеся 65 файлов в основном compiled DEX/`.so` и ресурсы; они не запускались и не проверялись как package artifacts.

## Независимое покрытие

Сверены source README/CONTRIBUTING, `refmap.yml`, metadata, build workflows и оба build scripts; Python entrypoint/lifecycle, сетевые и repository managers, install/cache/index/hash path, SettingsActivity и deeplink hooks; SCL Python binding/docs/native implementation; выбранные AI-search/version-picker UI paths и Install deeplink; Python Writer/Reader и native `.packit` codec. Проверены фактические call-sites по pinned snapshot и evidence line ranges в source page и machine facts.

GitHub pinned commit page независимо подтверждает сведения, извлечённые из `radar-context.md`; claim о сентябрьском rich-messages fix этим commit не подтверждён. Одинаковых фактов внутри source page и JSON не найдено; все 36 machine facts имеют уникальные IDs и отражают разные call-sites или отдельные грани контракта. Совпадения с общими правилами других sources являются отдельными provenance, не дубликатами PackIt. Для последующей тематической агрегации новые сведения относятся к `ai`, `distribution`, `requests`, `storage` и `security`; общие страницы по заданию review не менялись.

## Найденные проблемы и исправления

- Первоначальное описание считало 430 записей tree файлами; исправлено на 341 blob-файл плюс записи каталогов. Зафиксировано различие commit SHA поля wrapper и Git tree object SHA.
- Покрытие AI-поиска и истории версий было только перечислено среди пропусков. Добавлены подтверждённые call-sites: AI-запрос отправляет каталог plugin names/descriptions и пользовательский запрос Google Gemini, а VersionPicker разрешает links из `plugin.versions`, учитывает `app_version` и помечает старые записи `Outdated` вместо digest.
- Уточнена установка: PackIt передаёт temp archive в `PluginsController.showInstallDialog`, а Elyx при необходимости идёт через direct `ElyxEngine.showInstallDialog`. Код downstream host отсутствует, поэтому подпись/digest verification и фактическое поведение installer неизвестны.
- Статический межмодульный разбор выявил, что plugin deeplink вызывает `install_plugin` без известного `repoId` как `rm_rid`; default пустой ID затем пропускает `InstallIndex.commit_pending`. Записано как статический inference об индексации, не как runtime failure установки.
- Добавлено краткое покрытие `.packit` PCKT v3: экспортируемые блоки, C/ctypes boundary, KDF/AAD inputs и reader call-site. Указано, что `urandom_rng` при ошибке открытия `/dev/urandom` использует фиксированный xorshift seed; повторное использование nonce с тем же выводимым key — условный code-derived риск fallback, не измеренный на Android.
- Сборка, CI, криптографические тесты, установка и устройство не запускались. Статическое исследование не объявлялось runtime verification.

## Остаточные пробелы

- В host SDK/client коде за `PluginsController` и `ElyxEngine` нельзя проверить содержимое архива, checksum/signature policy и установочный UI.
- 65 файлов snapshot не сохранены локально: преимущественно compiled DEX/`.so`, fonts/sounds/images/videos, плюс вспомогательные файлы. Package outputs и ресурсы не валидировались.
- Не разобраны подробно все UI, decorations/chat hooks, icon/font installation workflows, export/import screens и achievements. В частности, экспортный codec прочитан, но legacy backup compatibility и реальный restore не проверялись.
- Нет device/runtime проверки callbacks, reflective hooks, сетевых моделей, native loader, криптографической реализации или целевых SDK/client compatibility. SHA pin подтверждён commit permalink и capture metadata; underlying tree object hash отдельно не захватывался.

## Вердикт

**accepted-with-gaps** — исходная страница и machine facts исправлены и подкреплены pinned-source ссылками в изученной области. Статическая проверка полезна для архитектуры/call-sites PackIt, но не подтверждает host installer, runtime совместимость, работу Gemini или криптографические свойства реализации.
