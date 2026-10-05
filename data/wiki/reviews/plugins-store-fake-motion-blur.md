---
type: review
source_id: plugins-store-fake-motion-blur
title: "fake_motion_blur"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 6ffd93145a9a3b025e88684d60368d2f104c76a7
artifact_sha256: d25cc4986b96a4a660e14af6c766d123b8fda20663e5835da3d08de152b30df6
plugin_id: "fake_motion_blur"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью фактов fake_motion_blur

Сборщик предоставил 5 фактов. Принято 5 фактов.

Все пять утверждений сверены с исходным кодом `Plugins/fake_motion_blur.plugin` на commit `6ffd93145a9a3b025e88684d60368d2f104c76a7`. Для каждого факта указан закреплённый commit и точные строки исходника.

| Факт | Решение | Результат проверки |
|---|---|---|
| `fake-motion-blur-001` | Одобрить | Проверка `SDK_INT < 31` и получение классов `RenderEffect` и `Shader.TileMode.CLAMP` подтверждаются строками 57–61. |
| `fake-motion-blur-002` | Одобрить | В коде `createBlurEffect` вызывается только когда хотя бы один радиус не меньше 0.5; при обоих радиусах меньше 0.5 эффект снимается. Строки 79–87. |
| `fake-motion-blur-003` | Одобрить | Все три метода RecyclerView передаются в `hook_all_methods`. Строки 64–108. |
| `fake-motion-blur-004` | Одобрить | Отложенный callback — экземпляр `Reset`, реализующего proxy `Runnable`; он удаляется при следующем событии прокрутки и планируется на 150 мс только в ветке установки эффекта. Строки 35–45. |
| `fake-motion-blur-005` | Одобрить | При выгрузке удаляются callback-и и вызывается `_clear`, которая удаляет состояние и снимает эффект. Строки 110–116. |

Утверждения ограничены тем, что непосредственно подтверждается исходником. URL источника закреплён на указанном commit; ссылки `blob/main/` не используются.
