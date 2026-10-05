---
type: review
source_id: plugins-store-iphone-like-portret
reviewer: verifier
repository: Kangel-Plugins/Plugins-Store
commit: 1ce808e03ef3fecbaec83226a42a0b12bc1209b5
plugin_id: iphone_like_Portret
review_status: accepted
date: 2026-10-03
---

# Review: iphone_like_Portret v1.2

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверка выполнена независимо по исходнику `Plugins/iphone_like_Portret.plugin` на pinned commit `1ce808e03ef3fecbaec83226a42a0b12bc1209b5`.

| ID | Вердикт | Проверка |
|---|---|---|
| `iphone-like-portret-001` | Принят | Шейдерное размытие GLES20 с выборками вокруг центра лица подтверждено строками 56–113. |
| `iphone-like-portret-002` | Принят | _find_texture_view определена, но не вызывается вне рекурсии, подтверждено строками 34–46. |
| `iphone-like-portret-003` | Принят | Загрузка MLKitDekma через InMemoryDexClassLoader подтверждена строками 451–470. |
| `iphone-like-portret-004` | Принят | _start_polling и _stop_polling содержат pass; вызовов threading.Thread нет (строки 433–437). |
| `iphone-like-portret-005` | Принят | Настройки боке и сброс состояния при unload подтверждены строками 526–563. |
