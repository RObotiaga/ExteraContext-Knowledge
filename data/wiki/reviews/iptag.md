---
type: review
source_id: iptag
review_status: accepted-with-gaps
date: 2026-09-28
---

# Независимая проверка: wsp2ch/iptag-plugin-Exteragramm-

- **Вердикт: accepted-with-gaps.** Короткий snapshot полностью получен, независимые checksums совпали, а source page точно описывает наблюдаемые сетевые, hook и UI call-sites. Уточнены границы декларативной IPv4 metadata и непроверенного host API; добавлены неописанные worker-failure и unload ограничения.
- **Snapshot и покрытие:** `wsp2ch/iptag-plugin-Exteragramm-`, `main`, commit `5fcd2df5465e25b7316ac1cf750a2e976c2dd62e`, capture `2026-09-27T15:46:52.687076Z`. `snapshot.json` указывает тот же repo и commit; `tree.json` не усечён и содержит ровно четыре blobs: `README.md`, `iptag.plugin`, `iptag.py`, `iptag.txt`. Прочитаны README, все три копии реализации, `snapshot.json`, `tree.json`, `file-manifest.json`, `repository.json`, `radar-context.md` и `radar-urls.json`. Три implementation-файла побайтно одинаковы. Независимые SHA-256 и Git blob SHA всех четырёх файлов совпали с manifest/tree: README `48e2b94c…808a58` / `8d7eb68b…da173`; три копии кода `01c14e03…e2ac0` / `a0aea44c…f5076a`.
- **Граница проверки:** весь малый релевантный snapshot изучен; исходники не запускались, не собирались, не устанавливались и не проверялись на устройстве. Radar называет проект минимальным примером `.iptag → HTTP → popup`; README также описывает всплывающий IP и сообщает о проверке автора, но это заявление документации, не runtime-доказательство. Код дополнительно делает геолокационные запросы. В дереве нет tests, CI, build/dependency manifest или реализации host SDK.

## Найденные проблемы и внесённые исправления

- Добавлено пропущенное metadata field `__description__`; теперь оно помечено как декларация исходника вместе с id/name/version/author/app-version.
- Уточнено, что `fetch_ipv4()` только читает поле `ip`: код не проверяет HTTP status и не валидирует, что ответ действительно IPv4. Тип зависит от API/комментария, а не от проверки внутри плагина.
- Уточнено, что `HookResult(strategy=CANCEL)` и `run_on_ui_thread(...)` — наблюдаемые call-sites. Их фактический host-контракт, выполнение callback на UI thread и отмена отправки не доказаны этим репозиторием и не проверялись runtime.
- Добавлены два факта: `_fetch_and_render()` не имеет внешней обработки/finally на весь worker path, поэтому неожиданное исключение может оставить spinner без закрытия; в классе отсутствует unload/cancel/join cleanup, поэтому поведение pending работы при выгрузке неизвестно. Оба последствия отмечены как статический вывод, не runtime observation.
- Перепроверены API descriptions: `fetch_location` пробует ipwho, затем ipapi с отдельными timeout 4s; пустые поля или `error` второго provider сами по себе не инициируют fallback; `fetch_ip_info` включает ошибку IPv4 в текст; message hook сравнивает строку после `strip()` с точным регистрозависимым `.iptag`; activity/dialog/bulletin пути соответствуют исходнику. Поля account не используются.
- После исправлений `iptag-facts.json` содержит **18 фактов с 18 уникальными ID** (`iptag-001`…`iptag-018`); полностью дублирующихся claims или повторных ID внутри набора не обнаружено. `iptag-016` фиксирует состояние pinned tree/хэшей как provenance, не повторяемый API-тезис.

## Дубликаты и канонические темы

В других источниках базы описаны общие patterns `add_on_send_message_hook`, `HookResult`/`HookStrategy.CANCEL` и вызовы UI helper-ов. Это независимые provenance одного plugin call-site, а не дубли утверждений об этом конкретном snapshot. При синтезе сопоставлять их с темами `hooks`, `threading`, `ui`, `lifecycle`, `network` и `security`; не приписывать этим общим примерам совместимость `iptag` с конкретной версией клиента. Внешние endpoints и передача IP — специфичны для этого источника. Другие source pages, темы, API и индекс этим review не менялись.

## Остаточные пробелы

- Не проверены на целевом клиенте контракты/доступность `BasePlugin`, `HookResult`, `HookStrategy.CANCEL`, `run_on_ui_thread`, `get_last_fragment`, `AlertDialogBuilder` и `BulletinHelper`; в частности, действительное поведение отправки команды и поток callback неизвестны.
- Не проверены runtime наличие/упаковка `requests`, разрешения host приложения, соответствие декларации `__app_version__ = ">=12.5.1"`, доступность сервисов и фактическая точность IP/geolocation.
- Не изучались privacy/retention правила ipify/ipwho/ipapi и реальный сетевой маршрут; вывод о передаче IP следует из URL и кода, не из захвата трафика.
- README говорит, что автор проверил плагин с включёнными плагинами; конкретный client version, устройство, сценарий и результат в источнике не приведены, поэтому утверждение осталось `docs`.
