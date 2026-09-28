# Независимое ревью: `Kratapand26/AyugramX`

**Вердикт:** `accepted-with-gaps`  
**Проверяющий:** `/root/review_ayugramx` · **модель:** `gpt-6-luna`  
**Закреплённый SHA:** [`e61bc31e0d06b4a92d39845e4031d90bf3fd34ff`](https://github.com/Kratapand26/AyugramX/tree/e61bc31e0d06b4a92d39845e4031d90bf3fd34ff)  
**Уникальных фактов:** 18 из 18

## Объём и сверка снимка

Независимо сверены source page, `outputs/plugin-wiki/work/ayugramx-facts.json`, `raw/ayugramx/snapshot.json`, `tree.json`, `file-manifest.json`, `repository.json`, `radar-context.md` и `radar-urls.json`. SHA снимка совпадает с назначенным; дерево содержит 6 894 записи и не усечено. Манифест захватывает выбранные исходники, `LICENSE` и `changelog.txt`; корневой `README.md` и `docs/README.md` имеют сохранённую ошибку HTTP 404, и в дереве этих путей нет. При независимой проверке к pinned snapshot дополнительно захвачены `Telegram/SourceFiles/boxes/filters/edit_filter_box.cpp`, `.h`, `edit_filter_chats_list.cpp` и `edit_filter_chats_preview.cpp`; все относятся к тому же SHA.

По дереву и code call-sites повторно прослежены диапазоны ID, девять переключателей `Quick Local Folders`, формирование фильтров и порядок исключений, сохранение local custom folder, account-keyed JSON, загрузка local entries до cloud list, merge при server refresh, полный локальный порядок и его cloud-only MTProto payload. Дополнительно проверена ветка общего editor: `EditExistingFilter` сохраняет local ID через `saveLocalFolder` и возвращается, тогда как cloud ID применяет обновление и отправляет `messages.updateDialogFilter`. Изучение исходников — статическая проверка; приложение, сборка и тесты не запускались.

Актуальный canonical facts-файл находится в `work/ayugramx-facts.json`; исходный collector artifact оставлен также в `outputs/plugin-wiki/work/ayugramx-facts.json`. Файл содержит 18 уникальных ID (`ayugramx-001`…`ayugramx-018`), все с единым pinned SHA.

## Проблемы и исправления

- Добавлены в coverage table четыре дополнительно полученных файла стандартного `EditFilterBox` и отдельные соседние Ayu regex-filter файлы, чтобы не создавать впечатление, что весь набор сохранённых файлов был перечислен или изучен полностью.
- Source page дополнена доказанным разделением local/cloud save path в `EditExistingFilter`. Для fact `ayugramx-010` доказательство расширено ссылкой на эту ветку редактора.
- Обновлены frontmatter review status и ссылка на этот отчёт. Canonical `work/ayugramx-facts.json` скопирован из collector artifact с тем же набором 18 фактов. В pipeline обновлена только строка `ayugramx`: reviewer `/root/review_ayugramx`, model `gpt-6-luna`, verdict `accepted-with-gaps`, `fact_count=18`, `accepted_facts=18`.
- Остальные 18 claims проверены без обнаруженных ошибок: preset flags совпадают с `createPresetFilter`, исключения и community rules — с `ChatFilter::contains`, JSON schema соответствует encode/decode, а account ID берётся из session user ID. Факт о локальном/client-only цвете и иконке прямо помечает его как workaround, а не серверную возможность.

## Повторы и границы

Все 18 fact ID уникальны; claim-повторы не найдены. Близкие записи разделяют разные утверждения: ID namespace и enum значения (002/004), форма custom-folder record и её JSON persistence (007/009), восстановление local filters и защита от cloud replacement (012/013), preset UI и логика вычисления пресетов (003/005). Повторяющиеся сведения на source page и в facts являются разными представлениями одной базы знаний, не дополнительными фактами. С Mercurygram есть общая каноническая тема local-folder storage/order/sync, но контракты сохраняются раздельно: у AyugramX desktop local IDs положительные от 1000, у Mercurygram локальные IDs отрицательные и отдельно описан Saved Messages sync.

В исходном радаре AyugramX обозначен как desktop-источник локальных папок/быстрых presets, а `Saved Messages Sync` и `Smart Rules` представлены как части идеи для будущего плагина. Страница корректно не приписывает эти функции AyugramX. Пустой `radar-urls.json` не предоставляет отдельной ссылки для исторического утверждения о коммите; текущий pinned code подтверждает наличие функции, но не дату её появления. README 404 не использовался как основание для API- или build-claims. Внутренний C++/Qt-код клиента не трактуется как Android Plugin API.

## Остаточные gaps

- Не прочитан весь огромный Telegram Desktop клиент, весь `ChatFilters`/settings framework или весь editor и связанные chatlist-link UI пути. Покрытие ограничено radar-целевой областью локальных папок и непосредственными seams.
- Снимок содержит отдельную Ayu regex-filter/import-export подсистему (`ayu/features/filters/*`, `ayu/ui/settings/filters/*`). Это отдельная функция, не заявленная для данного радара; её API, lifecycle и persistence не вошли в данную проверку.
- Политика хранения всего AyuSettings файла, миграции схемы, runtime поведение, серверные квоты и межклиентская совместимость не проверялись. Обратные README/docs заявления недоступны: обе README-проверки дали HTTP 404.
- Никакие runtime, build или test claims не делаются. Никакие выводы о доступности этих внутренних seams во внешнем Android plugin host не делаются.

Итог `accepted-with-gaps`: все 18 подготовленных фактов подтверждаются на закреплённом снимке и пригодны для индексации с явно отмеченными границами покрытия; это не гарантия абсолютной полноты большого клиента.
