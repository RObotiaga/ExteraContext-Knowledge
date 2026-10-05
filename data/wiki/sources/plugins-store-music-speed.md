---
type: source
source_id: plugins-store-music-speed
title: "Источник: Music Speed"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: 4f29ece39d5110e8f14292ae5a6c22c43827d82c
path: "Plugins/music_speed.plugin"
artifact_sha256: c4a8e438da8394006d3605c046280c90c2b90864d143e233cd4d86fce6dba2b8
plugin_id: "music_speed"
plugin_version: "1.0.1"
author: "@binbash_0"
min_version: ">=12.5.1"
app_version: ">=12.5.1"
sdk_version: ">=1.4.3.3"
platform: Android
evidence_status: code
review_status: accepted
collector_model: "google-antigravity/gemini-3.8-flash"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-music-speed.md
date: "2026-10-03"
---

# Источник: Music Speed

- Репозиторий: `Kangel-Plugins/Plugins-Store`
- Файл: `Plugins/music_speed.plugin`
- Версия: `1.0.1`
- Commit: `4f29ece39d5110e8f14292ae5a6c22c43827d82c`
- Проверенный файл: [music_speed.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/4f29ece39d5110e8f14292ae5a6c22c43827d82c/Plugins/music_speed.plugin)

## Проверенные факты

1. Совместимость с Media3/ExoPlayer2: выбор классов `PlaybackParameters` и `AuxEffectInfo`, попытка `setAuxEffectInfo` и резервный вызов `sendRendererMessage`. [Строки 16–23, 551–590](https://github.com/Kangel-Plugins/Plugins-Store/blob/4f29ece39d5110e8f14292ae5a6c22c43827d82c/Plugins/music_speed.plugin#L16-L23).
2. Установка хуков на `FragmentContextView.checkPlayer`, `AudioPlayerAlert.updateTitle` и `MediaController.playMessage`. [Строки 156–175](https://github.com/Kangel-Plugins/Plugins-Store/blob/4f29ece39d5110e8f14292ae5a6c22c43827d82c/Plugins/music_speed.plugin#L156-L175).
3. Использование существующей `playbackSpeedButton`, настройка ее видимости и состояния; вычисление правого padding заголовка как `AndroidUtilities.dp(44.0) + joinButtonWidth`. [Строки 608–653](https://github.com/Kangel-Plugins/Plugins-Store/blob/4f29ece39d5110e8f14292ae5a6c22c43827d82c/Plugins/music_speed.plugin#L608-L653).
4. Управление pitch через `PlaybackParameters` и reverb через `PresetReverb`/`AuxEffectInfo`. [Строки 271–289, 469–489, 517–549](https://github.com/Kangel-Plugins/Plugins-Store/blob/4f29ece39d5110e8f14292ae5a6c22c43827d82c/Plugins/music_speed.plugin#L517-L549).
5. Очистка ресурсов при выгрузке: вызов `release_reverb`, `unhook_method` для зарегистрированных хуков; отключение эффекта и `PresetReverb.release()`. [Строки 139–154, 592–606](https://github.com/Kangel-Plugins/Plugins-Store/blob/4f29ece39d5110e8f14292ae5a6c22c43827d82c/Plugins/music_speed.plugin#L139-L154).
