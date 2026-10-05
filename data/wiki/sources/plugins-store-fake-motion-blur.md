---
type: source
source_id: plugins-store-fake-motion-blur
title: "fake_motion_blur"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 6ffd93145a9a3b025e88684d60368d2f104c76a7
path: "Plugins/fake_motion_blur.plugin"
artifact_sha256: d25cc4986b96a4a660e14af6c766d123b8fda20663e5835da3d08de152b30df6
plugin_id: "fake_motion_blur"
plugin_version: "3.0.1"
author: "sixth"
min_version: "12.5.1"
app_version: ">=12.5.1"
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-fake-motion-blur.md
date: "2026-10-03"
---

# fake_motion_blur

Исходник плагина `fake_motion_blur`, версия `3.0.1`, автор `sixth`; минимальная версия указана как `12.5.1`. Метаданные находятся в `Plugins/fake_motion_blur.plugin:8-15`.

## Проверенные сведения

- Загрузка прекращается при `SDK_INT < 31`; при допустимой версии загружаются `RenderEffect` и `Shader.TileMode.CLAMP`. [Исходный код, строки 57–61](https://github.com/Kangel-Plugins/Plugins-Store/blob/6ffd93145a9a3b025e88684d60368d2f104c76a7/Plugins/fake_motion_blur.plugin#L57-L61).
- Для эффекта вычисляются ограниченные значения `rx` и `ry`; эффект создаётся вызовом `createBlurEffect(rx, ry, _fx["clamp"])`. Если оба радиуса меньше `0.5`, эффект снимается; иначе устанавливается и планируется отложенный callback. [Исходный код, строки 79–87](https://github.com/Kangel-Plugins/Plugins-Store/blob/6ffd93145a9a3b025e88684d60368d2f104c76a7/Plugins/fake_motion_blur.plugin#L79-L87).
- Хуки регистрируются для `RecyclerView.dispatchOnScrolled`, `dispatchOnScrollStateChanged` и `onDetachedFromWindow`. [Исходный код, строки 64–108](https://github.com/Kangel-Plugins/Plugins-Store/blob/6ffd93145a9a3b025e88684d60368d2f104c76a7/Plugins/fake_motion_blur.plugin#L64-L108).
- `Reset` является dynamic proxy для `java.lang.Runnable`. При прокрутке прежний callback удаляется; при установке эффекта он повторно планируется через `postDelayed` с `RESET_DELAY = 150`. [Исходный код, строки 35–45](https://github.com/Kangel-Plugins/Plugins-Store/blob/6ffd93145a9a3b025e88684d60368d2f104c76a7/Plugins/fake_motion_blur.plugin#L35-L45).
- При выгрузке для сохранённых состояний удаляются отложенные callback-и и вызывается очистка; очистка удаляет состояние из `_v` и вызывает `setRenderEffect(None)`. [Исходный код, строки 110–116](https://github.com/Kangel-Plugins/Plugins-Store/blob/6ffd93145a9a3b025e88684d60368d2f104c76a7/Plugins/fake_motion_blur.plugin#L110-L116).
