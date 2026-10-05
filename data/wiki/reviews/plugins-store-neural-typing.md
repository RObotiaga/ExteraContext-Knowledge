---
type: review
source_id: plugins-store-neural-typing
title: "Neural Typing"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: f8f49767cb38dacde721ff0d566377d501c031ec
artifact_sha256: 88ce09b6cebcf1a373c79730453a74049bbcc59f289cd7394b6648cff09e5c1f
plugin_id: "neural_typing"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: Neural Typing

Сборщик предоставил 5 фактов. Принято 5 фактов.

Проверка выполнена независимо по исходному файлу версии 2.3.1 на commit `f8f49767cb38dacde721ff0d566377d501c031ec`. Все пять утверждений подтверждаются указанными строками исходника.

| ID | Вердикт | Проверка |
|---|---|---|
| `neural-typing-001` | Принят | Локальная анимация и 10 стилей оформления подтверждены строками 3–7, 81–97. |
| `neural-typing-002` | Принят | Загрузка com.neuraltyping.NeuralTypingCore через InMemoryDexClassLoader с fallback подтверждена строками 40–43, 315–358. |
| `neural-typing-003` | Принят | Хук на ChatMessageCell.setMessageObject и фильтр свежести 15 секунд подтверждены строками 44–46, 590–611. |
| `neural-typing-004` | Принят | Детекция конфликтов с typewriter и text_animation подтверждена строками 50–53, 505–524. |
| `neural-typing-005` | Принят | Очистка, восстановление недопечатанного текста и uninstall ядра подтверждены строками 420–433, 837–860. |
