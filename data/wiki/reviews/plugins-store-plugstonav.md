---
type: review
source_id: plugins-store-plugstonav
title: "Plugins Tab (plugstonav)"
reviewer: independent-verifier
reviewer_model: "gpt-6-luna"
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 5a4efa002a7a85a232063849dc11f4c6ce7a730f
artifact_sha256: 700fdf19b33142da8e3787917595ff818bcbddd1a4703a73e96957e86f00f355
plugin_id: "plugstonav"
review_status: accepted
review_mode: independent-source-reread-nonblind
evidence_status: code
runtime_verified: false
facts_reviewed: 5
date: "2026-10-03"
---

# Ревью: plugins-store-plugstonav

Сборщик предоставил 5 фактов. Принято 5 фактов.

| ID | Вердикт | Проверка |
|---|---|---|
| `plugstonav-001` | Принят | Guard SDK < 26 завершает загрузку ошибкой до создания InMemoryDexClassLoader (строки 35–39). |
| `plugstonav-002` | Принят | Маркеры, Base64/zlib и передача ByteBuffer в загрузчик подтверждаются реализацией (строки 37–43, 84–101). |
| `plugstonav-003` | Принят | Рефлексия проверяет имя и арность; защищены случаи нескольких или нулевых совпадений (строки 67–82). |
| `plugstonav-004` | Принят | Имя класса и вызов dex.load() подтверждаются (строки 16, 104–115). |
| `plugstonav-005` | Принят | loaded=False выполняется через finally при unload; callback ловит и логирует исключения (строки 59–65, 116–121). |

Все факты подтверждены непосредственным чтением исходника на закреплённом commit `5a4efa002a7a85a232063849dc11f4c6ce7a730f`.
