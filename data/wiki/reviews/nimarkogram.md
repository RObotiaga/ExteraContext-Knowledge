# Независимая проверка Ettacent/NimarkoGram

- Verdict: `accepted-with-gaps`
- Reviewed snapshot: `main` at `881d0ea1ce5f6a3a234f46d0e928bb0d95305f6b` (README badge 12.10.5)
- Radar scope: источник упомянут как Telegram-клиент, проверенный для даты последнего содержательного коммита; feature claim к строке не привязан. Радар отдельно приводит старую отметку 12.10.1 и широкий перечень возможных клиентских функций, которые нельзя приписывать этому источнику без проверки.
- Result: принято 36 уникальных фактов; первоначальные 34 проверены, 2 добавлены по результатам независимой проверки.

## Проверенное покрытие

Сопоставлены `raw/nimarkogram/tree.json`, `radar-context.md`, `radar-urls.json`, source page и исходный `work/nimarkogram-facts.json`. Проверены README на английском и русском, BUILDING, метаданные релиза, Python plugin API/runtime/import/settings/intents и compatibility code, Java plugin controller/engine/hooks/bridge/PipController/UI/DEX attribution, перечисленные Telegram call-sites request/update/send/lifecycle, а также выборочные Python lifecycle/install/settings/UI tests и JVM callback test. Перечень точных paths и scopes оставлен в таблице покрытия source page.

Все первоначальные evidence paths существуют в сохранённом снимке, их GitHub ссылки содержат проверенный SHA. У всех 34 первоначальных facts есть provenance `code` или `docs`; source inspection нигде не выдан за runtime verification. Особенно проверены сигнатуры `BasePlugin` hooks, event/intent APIs, safe-mode поведение Pine hook, settings completion, account forwarding, install candidate/ticket checks и toolchain/build claims. На момент проверки не было одинаковых fact IDs или дословно дублированных normalized claims.

## Найденное и исправленное

- Source page не показывала два полезных plugin integration point: добавлены `BasePlugin.add_file_hook` и `add_menu_item`/`remove_menu_item` с точными сигнатурами и pinned links; добавлено новое code fact `nimarkogram-035`.
- README заявляет DEX loading, а registry/`PluginDexTracking` дают evidence только о регистрации загруженных классов для crash attribution. В source page раньше этот разрыв не был объяснён достаточно явно. Добавлена граница и новое `inference` fact `nimarkogram-036`; прямой сторонний artifact loader этим источником не подтверждён.
- Идентификаторы исходных facts идут не по порядку (033 и 034 встроены в конце), но уникальны; пере-нумерация могла бы повредить ссылки, поэтому ID сохранены.
- Обновлён source frontmatter: `review_status: accepted-with-gaps` и ссылка `../reviews/nimarkogram.md`.

## Остаточные пробелы

Полный Python client utility surface и все UI/menu call-sites не инвентаризированы. Не установлена реализация и lifecycle сторонних DEX/JAR/APK артефактов. Wheel resolver и package ownership PipController не проверены исчерпывающе. Не выполнен отдельный полный security audit parser/installer boundary; compatibility и lifecycle не проверялись на устройстве. Сборка, тесты и приложение не запускались. Исторический ряд Quote/QR изменений из radar не сравнивался построчно с коммитами. Эти ограничения сохраняют verdict `accepted-with-gaps`.
