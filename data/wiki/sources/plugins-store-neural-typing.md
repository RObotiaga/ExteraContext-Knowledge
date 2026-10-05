---
type: source
source_id: plugins-store-neural-typing
title: "Neural Typing"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: f8f49767cb38dacde721ff0d566377d501c031ec
path: "Plugins/neural_typing.plugin"
artifact_sha256: 88ce09b6cebcf1a373c79730453a74049bbcc59f289cd7394b6648cff09e5c1f
plugin_id: "neural_typing"
plugin_version: "2.3.1"
author: "@van1lLove (идея: @calm_rio)"
min_version: "12.5.1"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "gpt-6-luna"
reviewer_model: "gpt-6-luna"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-neural-typing.md
date: "2026-10-03"
---

# Neural Typing

Исходный код плагина: [Plugins/neural_typing.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767cb38dacde721ff0d566377d501c031ec/Plugins/neural_typing.plugin).

## Подтверждённые факты

1. Клиентская косметическая анимация входящих сообщений и десять вариантов оформления (девять именованных пресетов плюс «Свой»): [строки 3–7, 81–97](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767cb38dacde721ff0d566377d501c031ec/Plugins/neural_typing.plugin#L3-L7).
2. Встроенный Base64 DEX и загрузка `com.neuraltyping.NeuralTypingCore` (`nt-core-9`) через `InMemoryDexClassLoader` с fallback через `DexClassLoader`: [строки 40–43, 315–358](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767cb38dacde721ff0d566377d501c031ec/Plugins/neural_typing.plugin#L40-L43).
3. Хук классического режима на `ChatMessageCell.setMessageObject`; проверка свежести отсеивает сообщения старше 15 секунд: [строки 44–46, 450–459, 590–611](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767cb38dacde721ff0d566377d501c031ec/Plugins/neural_typing.plugin#L44-L46).
4. Выявление конфликтов `typewriter` и `text_animation`, запись предупреждения в лог; отключение конфликтующих плагинов не производится: [строки 50–53, 505–524](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767cb38dacde721ff0d566377d501c031ec/Plugins/neural_typing.plugin#L50-L53).
5. Выгрузка снимает нативные хуки, останавливает таймеры классического режима, восстанавливает текст и снимает классический hook, очищая ссылки: [строки 420–433, 837–860, 526–543](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767cb38dacde721ff0d566377d501c031ec/Plugins/neural_typing.plugin#L420-L433).
