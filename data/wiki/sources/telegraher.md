---
type: source
source_id: telegraher
platform: Android
review_status: unavailable-verified
review: ../reviews/telegraher.md
date: 2026-09-28
---

# Telegraher (`phxc/telegraher`) — исходный репозиторий пуст

## Идентичность и доступность

Целевой источник — именно публичный GitHub repository [phxc/telegraher](https://github.com/phxc/telegraher), а не любой проект с названием Telegraher. GitHub API подтверждает точную запись `id=552598807`, `full_name=phxc/telegraher`, `private=false`, `fork=false`, `created_at=2022-10-16T23:33:52Z`, `updated_at=2023-03-22T11:59:23Z`, `pushed_at=2022-10-16T23:33:53Z`, `size=0`, `default_branch=main`. Проверка выполнена 2026-09-28; search API также возвращает цель, но прямой repository endpoint является основным evidence.

У репозитория нет доступного снимка кода: `/commits` отвечает HTTP 409 `Git Repository is empty`; `/branches` и `/tags` возвращают `[]`; `/git/refs` и matching refs отвечают HTTP 409; contents endpoint сообщает HTTP 404 `This repository is empty`. Независимая проверка 2026-09-28 совпала с acquisition от 2026-09-27. Поэтому SHA/версию, README и tree для назначенного источника установить невозможно. Публичную запись удалось идентифицировать, но её Git-история и содержимое недоступны.

Прямые metadata endpoints показывают отдельные `nikitasius/Telegraher` и `pegioner/Telegraher`: это forks с parent/source lineage `DrKLO/Telegram`, а не доказанные forks цели `phxc/telegraher`; их материалы не использовались как замена источнику. ID цели `552598807`, `fork=false`, `size=0`; родство с этими проектами не подтверждено. У `nikitasius/Telegraher` metadata указывает push 2026-09-17, поэтому общее утверждение радара о давней неактивности одноимённых проектов нельзя распространять на текущую активность этого fork.

## Роль и покрытие

В радаре `phxc/telegraher` включён в список клиентов, проверенных на изменения; конкретных функций, API или технических находок для этого репозитория не названо. Сохранённый вторичный радар говорит, что старые направления Telegraher давно не развивались и что за рассмотренный интервал новых функций не обнаружено. Это характеристика радара о старых проектах с таким названием, а не доказательство истории конкретной пустой записи `phxc/telegraher`.

| Материал | Результат | Пропуск |
|---|---|---|
| `raw/telegraher/acquisition-error.json` | Зафиксирован ответ acquisition: `Git Repository is empty (HTTP 409)` для `phxc/telegraher` | SHA и snapshot отсутствуют |
| GitHub repository API `https://api.github.com/repos/phxc/telegraher` | HTTP 200; ID `552598807`, exact `full_name`, public, `fork=false`, даты создания/обновления/push, `size=0`, default branch `main` | Метаданные не раскрывают исходный код или возможную историю вне текущего GitHub repo |
| GitHub commits, branches, tags, git refs и contents API | `/commits`: 409; branches/tags: `[]`; `/git/refs` и matching refs: 409 empty repository; contents: 404 empty repository | Нельзя получить SHA, версию, дерево, лицензии или файлы; exact evidence/endpoints — в [review](../reviews/telegraher.md) |
| `raw/telegraher/radar-context.md:10,35`; `radar-urls.json` | Только вторичный контекст о давнем отсутствии активности и отсутствии новых находок; исторические URL списка пусты | Радар не устанавливает связь между `phxc/telegraher` и другими Telegraher проектами, не содержит конкретных API или permalink на код |

Исходники и приложения не запускались; сборка и runtime-поведение не проверялись. Статусы `code` и `runtime-verified` неприменимы.

## API и точки интеграции

Подтверждённых классов, сигнатур и call-sites нет. Нельзя извлечь из этого источника plugin hooks, account/thread lifecycle, UI, сетевые или storage контракты. Теlegraher фигурирует как Telegram-клиент, а не как подтверждённый ExteraGram/AyuGram plugin SDK.

## Применение и ограничения

Использовать эту запись только как подтверждение недоступности точного `phxc/telegraher` репозитория и как место фиксации пробела в корпусе. Не переносить сюда выводы из `nikitasius/Telegraher` или его форков без проверяемого источника/истории, устанавливающей их связь с целевым репозиторием.

## Gaps

Не установлены код, SHA, версия, лицензия, история, feature implementations, API, тесты и build contract назначенного источника. Исторические URLs радара отсутствуют, а Wayback/CDX запрос во время сбора ответил, что сервис временно недоступен. Радар не даёт feature-specific permalink. Требуется доступный архив/commit именно `phxc/telegraher` либо достоверная внешняя запись его lineage. В машинном слое сохранено 3 уникальных факта: два `unavailable` о доступности точного источника и один `secondary` о радаре. Ни один не выдан за `code` или `runtime-verified`. Независимая проверка: [review](../reviews/telegraher.md).
