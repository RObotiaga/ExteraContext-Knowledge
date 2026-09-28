# Независимое ревью NullcoreGram

- Вердикт: **accepted-with-gaps**.
- Область: `NullCoreDeveloper/NullcoreGram`, закреплённый tree/snapshot SHA `926c62a91c8daccd43a8ad1d6e636ee28b018307`, полученный 2026-09-27. В snapshot 24 644 записи, `truncated: false`.
- Проверено: README (русский и английские варианты, включая NekoX), license, build scripts/workflows, media confirmation helper и два send-path owner, `VideoGesturesHelper` и `PhotoViewer`, DoH resolver/settings/ConnectionsManager bridge, WebProxyManager и VPN callback integration, DNS smoke test, а также радарные контекст/URL. Релевантные исходники читаются из `raw/nullcoregram/files/`; в tree также проверено отсутствие исходного `NetworkRequestBuilder`/`NetworkResponse` по импортированному package.
- Граница: весь клиент Telegram не изучался построчно. Проверен объём собственных функций NullcoreGram, вынесенных радаром: media-send confirmations, viewer gestures и OkHttp/DoH/WebProxy/VPN networking, плюс сборка и CI как ограничения переноса.

## Результат проверки

Существующая страница в основном точно отделяла реализованный Android-код от пригодности для ExteraGram/KPM: это client fork, не plugin SDK; факты указывали конкретные call-site, lifecycle и snapshot SHA, а source inspection не выдавался за runtime verification. Раздельные DoH-пути `DnsFactory` и WebProxy, native bridge, media-send wrapping, gesture takeover/reset, build/CI и расхождение README SDK 33 с Gradle SDK 36 покрыты. Сигнатуры публичных методов helper и перечисленные code links сверены с сохранёнными файлами и номерами строк.

Исправлено: добавлены два факта и замечание в раздел DNS о process-wide cache, индексируемом только hostname, без TTL/invalidation в `DnsFactory`; а также inference о конкурентном доступе к обычным `mutableMapOf` из DNS thread pool. В таблице точек вызова разделены pool-based hostname lookups и привязанный к `currentAccount` TXT task. Изначальное количество уникальных фактов 31, после дополнения — **33**.

Идентификаторы 001–033 уникальны; повторяющихся claims внутри facts JSON не найдено. Несколько записей поддерживают взаимосвязанные, но разные контракты (helper и call-site, A/AAAA и TXT DNS, Java/native bridge, отдельный WebProxy resolver). Для последующей тематической канонизации DNS cache policy/thread safety относится к темам DNS resolution/cache, а не к универсальному HTTP client. Исторический commit `2ef1033` подтверждён по его заголовку и diff summary: он восстанавливает OkHttp, добавляет DoH resolver и удаляет Cronet/ECH артефакты; это история, не свойство runtime snapshot. Его сведения оставлены явно вторичными/историческими.

## Остаточные gaps

- Реализация импортированного `xyz.nextalone.nagram.network.NetworkRequestBuilder`/`NetworkResponse` отсутствует в полном Git tree по SHA. Manifest также отмечает 404 для ожидаемых `.kt`/`.java` путей; тип может поставляться вне исходного tree, но это не установлено. Поэтому timeout, cancellation, retry, TLS и resolver semantics этого DoH HTTP builder остаются неизвестны.
- Внешний DNS endpoint, стабильность/приватность resolver, cache/thread-safety поведение на устройстве и race conditions не испытывались; два новых cache риска — code-derived (второй `inference`), а не runtime finding.
- Не запускались приложение, build, workflow или `DnsFactoryTest`. Smoke test сам не содержит assertions. UX, производительность, совместимость с конкретной версией ExteraGram/AyuGram и точный охват всех путей пересылки/отправки media не подтверждены.
- Область исключает построчную проверку всего Telegram upstream и полный diff форка относительно NekoX/Telegram; рассмотрены только обозначенные в радаре features и связанная интеграция.

## Изменённые артефакты

- Исправлена `wiki/sources/nullcoregram.md`: статус ревью и ссылка, DNS cache/thread-safety caveat, уточнение account scope TXT task.
- Исправлен `work/nullcoregram-facts.json`: добавлены `nullcoregram-032` (`code`) и `nullcoregram-033` (`inference`).
- Обновлён `work/pipeline.json`: reviewer `/root/review_nullcoregram`, модель `gpt-6-luna`, state `accepted-with-gaps`, `facts_count: 33`.
