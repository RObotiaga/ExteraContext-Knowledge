---
type: source
source_id: nekox
platform: Android
review_status: unavailable-verified
date: 2026-09-28
review: ../reviews/nekox.md
---

# NekoX — источник недоступен, сохранилась копия README

Заданный источник: [Nekogram/NekoX](https://github.com/Nekogram/NekoX). GitHub API и `work/acquire.py` вернули HTTP 404; в исходной папке `raw/nekox` до попытки восстановления были только ошибка получения и контекст радара, без snapshot/tree/manifest. Поэтому SHA и версию исходного `Nekogram/NekoX` установить нельзя, а клиентский код, объявления API и call-sites не изучены.

Проверен текущий [NekoX-Dev/NekoX](https://github.com/NekoX-Dev/NekoX), snapshot `3581a10f8ecaa0f6d42d7a77442742caf95c6a13` (`master`, захвачен 2026-09-27). Это тот же GitHub URL, на который архивный README Nagram ссылается как на NekoX, поэтому объявлять проекты несвязанными было бы слишком сильным выводом. Однако GitHub API указывает создание доступного сейчас repository record в 2026 году; его README описывает официальный Telegram Android, а дерево содержит `org/telegram` без отдельного NekoX feature namespace. Этого достаточно, чтобы не считать текущий snapshot подтверждённым историческим кодом NekoX, но не чтобы установить точную историю удаления/повторного создания или исключить преемственность.

## Роль и границы

NekoX задуман в радаре как Android-клиент Telegram, а не plugin SDK. Единственный доступный NekoX-специфичный материал — `README.NekoX.md`, сохранённый в другом проекте `NextAlone/Nagram` на SHA `b8db62a65e1e4dee34d92bff412548ef628ddb06`. Его ссылки ведут на NekoX-Dev и он выглядит как копия README проекта, но это вторичное свидетельство: перечисленные функции и инструкции нельзя считать проверенными по исходникам NekoX. Не найдено подтверждённых plugin hooks, SDK контрактов, сигнатур, callback thread guarantees или стабильных account APIs.

## Покрытие

| Материал | Извлечено | Пропуски |
|---|---|---|
| `raw/nekox/acquisition-error.json`, запрос GitHub API для `Nekogram/NekoX` | зафиксирован HTTP 404 и отсутствие исходного pinned snapshot | исторический удалённый код и SHA не восстановлены |
| Текущий `NekoX-Dev/NekoX` snapshot `3581a10f8ecaa0f6d42d7a77442742caf95c6a13`: `README.md`, `tree.json`, `repository.json` | проверены описание репозитория, дата создания, Telegram README и package roots; Nagram ссылается на этот же URL через Wayback | commit lineage до исторического NekoX неизвестна; текущий snapshot не подтверждён как снимок старого клиента |
| `NextAlone/Nagram` snapshot `b8db62a65e1e4dee34d92bff412548ef628ddb06`: `README.NekoX.md` | только вторичная документация: заявленные функции клиента, build prerequisites/variants и описанный способ включить crash log | поведение, API и call-sites, совпадение с какой-либо версией NekoX, фактическая сборка |
| `raw/nekox/radar-context.md`, `radar-urls.json` | найдено лишь общее замечание радара о том, что NekoX отстал; прямых URL нет | радар не задаёт конкретных функций/API и не заменяет исходник |

Исходники и приложения не запускались. Сборка не проверялась. Статус `runtime-verified` не применим.

## Документальные признаки, не подтверждённые кодом

Сохранённая вторичная README-копия перечисляет неограниченное число логинов и account-specific предупреждения, импорт/экспорт и разбор форматов proxy, proxy subscriptions, переключатель proxy, отключение proxy при включённом VPN, добавление proxy из QR/link, кастомные emoji packs, добавление stickers без sticker pack, InstantView/selected-text translation и text replacer. Это полезные направления для поиска feature areas в будущем восстановленном дереве. По README нельзя определить их классы, границы account scope, поток выполнения, lifecycle, доступность извне клиента или пригодность для ExteraGram plugin. QR/link import относится к proxy workflow; QR sharing других сущностей не дублируется как отдельный факт.

README также описывает Full/Mini и Debug/Release/ReleaseNoGcm варианты, инициализацию submodules, Android SDK/NDK, Go 1.16, Rust targets, нативную сборку через `./run`, значения Telegram App ID/Hash, Firebase-конфигурацию и подпись. Там отдельно заявлено отсутствие поддержки Windows. Это старые инструкции из копии README; они не являются проверенными требованиями актуального NekoX. Crash-инструкция предлагает включить log через нажатие номера версии в настройках; код и формат выгрузки логов не доступны.

## Таблица вызовов и предполагаемые точки интеграции

| Модуль/класс | Сигнатура или call-site | Назначение | Lifecycle/thread/account | Evidence |
|---|---|---|---|---|
| — | Подтверждённых объявлений или call-sites нет | API-каталог по этому источнику построить нельзя | Не установлено | исходный snapshot недоступен; README-копия не содержит сигнатур |
| Proxy / QR | Только описание функций README, без класса/метода | возможные точки исследования: импорт ссылки и QR, подписка, выбор proxy | Не установлено | [README.NekoX.md](https://github.com/NextAlone/Nagram/blob/b8db62a65e1e4dee34d92bff412548ef628ddb06/README.NekoX.md#L23-L32), secondary |
| Translation / text replacement | Только названия функций README, без контракта | возможные feature areas для будущего поиска | Не установлено | [README.NekoX.md](https://github.com/NextAlone/Nagram/blob/b8db62a65e1e4dee34d92bff412548ef628ddb06/README.NekoX.md#L38-L39), [line 70](https://github.com/NextAlone/Nagram/blob/b8db62a65e1e4dee34d92bff412548ef628ddb06/README.NekoX.md#L70), secondary |

## Применение и ограничения

- Рассматривать README только как вторичный список функций и исторические build/debug подсказки; не копировать оттуда API-контракты — их там нет.
- При появлении доступного исходника сначала сверить Git remote/README, commit lineage и NekoX-specific пакеты, затем заново пройти account scoping, proxy/QR call-sites, translation и text replacement.
- Не объявлять этот клиент ExteraGram/AyuGram plugin SDK и не выводить из него совместимость с plugin runtime.
- Радар утверждает, что NekoX устарел и не является хорошим источником свежих функций; имеющиеся данные подтверждают только то, что первичный snapshot сейчас недоступен, а не текущее состояние проекта.

## Gaps

Не удалось установить нужный SHA, состояние последнего исходного дерева, кодовые точки интеграции, thread/lifecycle/account contracts, тесты и точные build/debug требования. Для полной source review необходим подтверждённый архив или commit `Nekogram/NekoX` либо надёжный официальный mirror с проверяемой историей. Первичный источник независимо проверен как недоступный (HTTP 404); итоговый вердикт — `unavailable-verified`. В базе 8 уникальных документированных фактов, все вторичны либо описывают недоступность/идентификацию; ни один не подтверждает код или runtime behavior.
