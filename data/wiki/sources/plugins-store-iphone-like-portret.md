---
type: source
source_id: plugins-store-iphone-like-portret
title: "iPhone Like Portret (v1.2)"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 1ce808e7cefd9de80cb4f76e387a1030fb740bf4
path: "Plugins/iphone_like_Portret.plugin"
artifact_sha256: 93e8616afcd951b104cdb45632287137d5b1dd0039abba2aa47f585b71e05727
plugin_id: "iphone_like_Portret"
plugin_version: "1.2"
author: "@dekma0091 && @DefinitelyNotDekma"
min_version: "12.5.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "gpt-6-luna"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-iphone-like-portret.md
date: "2026-10-03"
---

# iPhone Like Portret (v1.2)

- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Файл: [Plugins/iphone_like_Portret.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/1ce808e7cefd9de80cb4f76e387a1030fb740bf4/Plugins/iphone_like_Portret.plugin)
- Commit: `1ce808e7cefd9de80cb4f76e387a1030fb740bf4`

## Подтверждённые факты

1. **GPU blur:** `Plugins/iphone_like_Portret.plugin:56-113` — кастомные vertex/fragment shader sources; render hook создаёт/использует GLES20 program, передаёт координаты центра/радиус детектора и выполняет 16 текстурных выборок. [Строки 56–113](https://github.com/Kangel-Plugins/Plugins-Store/blob/1ce808e7cefd9de80cb4f76e387a1030fb740bf4/Plugins/iphone_like_Portret.plugin#L56-L113).
2. **Неиспользуемый view helper:** рекурсивно ищет классы с именами TextureView, PreviewView или SurfaceView. Вызовов кроме рекурсивного вызова внутри самой функции нет. [Строки 34–46](https://github.com/Kangel-Plugins/Plugins-Store/blob/1ce808e7cefd9de80cb4f76e387a1030fb740bf4/Plugins/iphone_like_Portret.plugin#L34-L46).
3. **DEX detector:** встроенный DEX декодируется/распаковывается, передаётся в InMemoryDexClassLoader; загружается `ni.dekma.MLKitDekma.MLKitDekma`. [Строки 451–470](https://github.com/Kangel-Plugins/Plugins-Store/blob/1ce808e7cefd9de80cb4f76e387a1030fb740bf4/Plugins/iphone_like_Portret.plugin#L451-L470).
4. **Polling/thread:** `_start_polling` и `_stop_polling` содержат только `pass`; `threading` импортирован, но `threading.Thread` не используется в файле. [Строки 433–437](https://github.com/Kangel-Plugins/Plugins-Store/blob/1ce808e7cefd9de80cb4f76e387a1030fb740bf4/Plugins/iphone_like_Portret.plugin#L433-L437).
5. **Settings/cleanup:** UI-настройки включают radius scale, blur intensity, mask bounds; render сбрасывает часть GL state (`glUseProgram(0)`), unload сбрасывает `initialized` и вызывает `release` детектора. [Строки 526–563](https://github.com/Kangel-Plugins/Plugins-Store/blob/1ce808e7cefd9de80cb4f76e387a1030fb740bf4/Plugins/iphone_like_Portret.plugin#L526-L563).
