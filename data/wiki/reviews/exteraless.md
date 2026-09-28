---
type: review
source_id: exteraless
reviewer: /root/review_exteraless
model: gpt-6-luna
verdict: accepted-with-gaps
facts_count: 32
reviewed_sha: 5929d469d5dbda65da219361fa67b9b79ff31fb2
date: 2026-09-28
---

# Независимое ревью: exteraless/exteraless

## Область проверки

Проверен источник `exteraless/exteraless`, branch `main`, SHA `5929d469d5dbda65da219361fa67b9b79ff31fb2`. В первичном `tree.json` snapshot помечен как доступный и неусечённый; он содержит 31 354 записи. Область задана упоминаниями радара в `raw/exteraless/radar-context.md`: совместимый с ExteraGram/NagramX plugin SDK, Java/Python runtime, permissions, callback и reload поведение. `radar-urls.json` пуст, поэтому названные в радаре отдельные сентябрьские исправления нельзя привязать к конкретному commit или patch по предоставленным ссылкам.

Самостоятельно сверены первичные файлы по метаданным, installer/capability scan, trust/grants, Java sink gates, Python audit/loader, Java controller/engine, SDK hooks/client/account/UI dispatch, plugin storage/intents, Elyx/EAF lifecycle, watchdog, signature/port tests и README/build configuration. По дереву и первичному snapshot дополнительно получены файлы dev server, dependency manager, menu/media/plugin UI, Android manifest и release/PR workflows; код чужих проектов и приложение не запускались.

## Результаты и исправления

Основные 30 исходных фактов соответствуют коду или README указанного SHA. Сигнатуры ключевых public SDK методов и используемые callback paths сверены с исходными объявлениями и call sites. README-утверждения сохранены со статусом `docs`, а чтение исходников/тестов не обозначено как runtime verification.

В `work/exteraless-facts.json` исправлены недостаточные evidence ranges у sink gate, файловых roots и watchdog; факт о permission guard сужен до поведения, подтверждённого его диапазоном. Добавлены два отдельных факта:

- `exteraless-031`: dev-server command token, loopback bind и ограничение на локальной Android-сети; это важный debug/security gotcha.
- `exteraless-032`: требование pure-Python wheels и совместный учёт/очистка зависимостей плагинов.

В source page добавлен соответствующий раздел, уточнены остаточные gaps, заполнены `review_status` и ссылка на этот отчёт. После правок в JSON ровно 32 уникальных ID и 32 уникальных нормализованных claims. Дублирующихся фактов нет: обзор callbacks (`-016`) и регистрационные методы (`-018`), а также общий dispatcher contract (`-020`) описывают разные уровни API. Похожие правила других реализаций допустимы как независимое provenance; для последующей тематической свёртки подходят темы plugin permissions/sandbox, lifecycle and callbacks, account-scoped client helpers, Elyx/EAF, developer tooling and dependency installation.

Проверены соответствие каждого evidence path локальному файлу и допустимому диапазону строк, pinned SHA в ссылках, а также SHA-256 всех 67 сохранённых файлов по `file-manifest.json`. Ошибок и отсутствующих доказательных файлов нет.

## Остаточные пробелы

- Не подтверждены на уровне истории конкретного patch перечисленные радаром правки Python↔Java proxy, UI-thread, reload и отмены keep-alive при push-response: для них нет исходных permalink в радаре, и доступный текущий snapshot не устанавливает дату/причину изменения.
- Не инвентаризированы полностью меню, media API и все Python UI helpers/widgets, все sinks и обходы permission gates, приоритеты/сериализация hooks и каждый dev-server/package-manager edge case.
- GitHub Actions workflows были сохранены для продолжения проверки, но сам CI, Gradle сборка и установка/unload/reload на устройстве не проверялись. Факт о watchdog подтверждает обнаружение и маркер зависшего исполнения, но не безопасную остановку произвольного callback.
- Результаты описывают статический snapshot, не гарантируют runtime security или абсолютную полноту по всему клиенту.

## Вердикт

`accepted-with-gaps` — страница пригодна как источник по основному Python plugin SDK/runtime и permission model. Для выводов о конкретных исторических исправлениях, полном наборе UI/media API и runtime/build поведении нужно отдельное подтверждение.
