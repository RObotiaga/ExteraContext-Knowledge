---
type: review
source_id: nekox
reviewer: /root/review_nekox
collector: /root/collect_nekox
model: gpt-6-luna
verdict: unavailable-verified
date: 2026-09-28
accepted_facts: 8
---

# Независимая проверка NekoX

## Scope и идентификация

Проверена заявленная цель `Nekogram/NekoX`, контекст радара, доступное текущее состояние `NekoX-Dev/NekoX`, а также NekoX-specific README-копия в `NextAlone/Nagram`. Задание ограничено проверкой доступности и идентификации источника, а не инвентаризацией Android SDK/API.

Радар (`raw/nekox/radar-context.md`, выдержки 2584–2589 и 4737) характеризует NekoX как отставший источник; прямых candidate URLs он не задаёт (`raw/nekox/radar-urls.json` — пустой список). Первоначальное назначение в pipeline — `Nekogram/NekoX`.

Прямой независимый запрос к `https://api.github.com/repos/Nekogram/NekoX` вернул HTTP 404. Сохранённый `raw/nekox/acquisition-error.json` также фиксирует 404; у этой цели нет pinned snapshot, SHA или кода. Итоговая недоступность подтверждена.

`NekoX-Dev/NekoX` существует сейчас и имеет SHA `3581a10f8ecaa0f6d42d7a77442742caf95c6a13`. Его README говорит об официальном Telegram Android; дерево содержит Telegram package roots. Но `NextAlone/Nagram` README в SHA `b8db62a65e1e4dee34d92bff412548ef628ddb06` прямо описывает Nagram как основанный на NekoX и ведёт на архивную копию того же URL `NekoX-Dev/NekoX`. GitHub metadata текущего доступного repository record сообщает дату создания 2026-02-21. Следовательно, отвергнуть нынешнее содержимое этого SHA как доказательство исторической реализации NekoX обоснованно, однако формулировка «отдельный несвязанный репозиторий/не зеркало» доказательствами не поддерживается. Нельзя определить, удалялся и создавался ли repository заново, либо каким commit он связан с архивным состоянием. Source page и fact `nekox-002` исправлены с этой оговоркой.

## Покрытие

Независимо прочитан целиком `raw/nagram/files/README.NekoX.md` (187 строк), а также README и выбранные metadata/tree записи текущего `NekoX-Dev/NekoX`. Вторичная копия README именует функции NekoX, но не представляет исходный NekoX repository, и сама содержит только документальные утверждения. Не делались выводы о классах, методах, потоках, lifecycle, SDK, permissions или runtime behavior.

По конкретным фактам:

- `nekox-001`: подтверждён 404 для назначенного URL, SHA и исходное дерево не установлены.
- `nekox-002`: идентификация уточнена: текущий URL связан с исторической ссылкой Nagram, но доступный снимок не доказывает историческую реализацию.
- `nekox-003`: README claims об unlimited accounts и поведении для non-current account остаются вторичной документацией; account API/lifecycle неизвестны.
- `nekox-004`: proxy workflows взяты из строк 23–32 и 58; это не сигнатуры и не доказанное поведение.
- `nekox-005`: оставлены только emoji packs и sticker addition; QR import удалён как повтор proxy-факта.
- `nekox-006`: InstantView/selected-text translation и text replacer имеют отдельные точные локальные line references.
- `nekox-007`: build prerequisites/commands сохранены как исторические README инструкции, не как проверенные требования.
- `nekox-008`: crash-log guidance сохранён как документация, механизм и формат данных неизвестны.

Permalinks README-копии закреплены за commit `b8db62a65e1e4dee34d92bff412548ef628ddb06`; code permalink кандидата закреплён за проверенным SHA `3581a10f8ecaa0f6d42d7a77442742caf95c6a13`. Утверждение HTTP 404 привязано к API URL и локальному capture record. Дублировавшееся QR mention удалено. Идентификаторы `nekox-001`…`nekox-008` уникальны; принято 8 фактов.

## Остаточные gaps и вердикт

Нет доступного pinned snapshot или подтверждённой истории для исходных реализаций NekoX. README-копия не заполняет этот пробел, не доказывает фактическую реализацию заявленных функций и не позволяет восстановить API, call-sites, account/thread/lifecycle contracts, tests или исполняемость build instructions. Код и приложение исторического NekoX не проверялись; runtime testing не выполнялся. Абсолютная полнота по недоступному коду не заявляется.

**Verdict: `unavailable-verified`.** Указанный `Nekogram/NekoX` независимо возвращает HTTP 404; evidence из Nagram сохранено только как вторичная документация. Текущий `NekoX-Dev/NekoX` не принят за исторический implementation snapshot, при этом связь URL с прежним NekoX оставлена явно. Уникальных принятых фактов: **8**.
