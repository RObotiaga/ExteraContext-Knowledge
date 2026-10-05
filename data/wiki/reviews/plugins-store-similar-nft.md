---
type: review
source_id: plugins-store-similar-nft
title: "Similar NFT plugin source"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: d49a79536e8e0186ac788ea2699db20779cd2c61
artifact_sha256: e6dcb460d729248da7c79735d22774c30df6723a08f7855a56c59670c7d77cbc
plugin_id: "similar_nft"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: Plugins Store — similar_nft

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверены соответствие фактов исходному коду и точность формулировок. Все пять утверждений подтверждаются pinned snapshot `Plugins/similar_nft.plugin` на commit `d49a79536e8e0186ac788ea2699db20779cd2c61`. Ссылки закреплены на SHA; пути доказательств содержат точные диапазоны строк.

1. **fact-001 — принят.** Код проходит BottomSheet, Dialog и `_SHEET_CLASSES` (где указан StarGiftSheet), находит метод `show` и назначает `_ShowHook`. Термин «рефлексивный» корректен ввиду разрешения класса/метода, но факт не утверждает, что hook гарантированно сработает на каждом runtime.
2. **fact-002 — принят.** Идентификатор дедупликации строится как имя declaring class плюс `.show`; повторный идентификатор пропускается внутри цикла регистрации.
3. **fact-003 — принят.** `hook_all_methods` является условным fallback только при `n == 0`; перебираются BottomSheet и Dialog, после успеха цикл прекращается.
4. **fact-004 — принят.** Меню создается через `MenuItemData`, добавляется через `add_menu_item`, а при отключении ранее включенного пункта вызывается `remove_menu_item`.
5. **fact-005 — принят.** При unload код пытается синхронизировать меню в выключенное состояние, затем очищает `_CACHE` и `self._captured` в блоках с обработкой исключений.

**Ограничение:** это проверка статического кода, а не runtime-тестирование Android/ExteraGram. Метаданные версии, ID, автора и минимальной версии приложения соответствуют контексту задания и не трактуются как доказательство runtime-совместимости.
