---
type: review
source_id: plugins-store-iphone-like-portret
title: "iPhone Like Portret (v1.2)"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 1ce808e7cefd9de80cb4f76e387a1030fb740bf4
artifact_sha256: 93e8616afcd951b104cdb45632287137d5b1dd0039abba2aa47f585b71e05727
plugin_id: "iphone_like_Portret"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Review: iphone_like_Portret v1.2

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверка выполнена независимо по исходнику `Plugins/iphone_like_Portret.plugin` на pinned commit `1ce808e7cefd9de80cb4f76e387a1030fb740bf4`.

| ID | Вердикт | Проверка |
|---|---|---|
| `iphone-like-portret-001` | Принят | Шейдерное размытие GLES20 с выборками вокруг центра лица подтверждено строками 56–113. |
| `iphone-like-portret-002` | Принят | _find_texture_view определена, но не вызывается вне рекурсии, подтверждено строками 34–46. |
| `iphone-like-portret-003` | Принят | Загрузка MLKitDekma через InMemoryDexClassLoader подтверждена строками 451–470. |
| `iphone-like-portret-004` | Принят | _start_polling и _stop_polling содержат pass; вызовов threading.Thread нет (строки 433–437). |
| `iphone-like-portret-005` | Принят | Настройки боке и сброс состояния при unload подтверждены строками 526–563. |
