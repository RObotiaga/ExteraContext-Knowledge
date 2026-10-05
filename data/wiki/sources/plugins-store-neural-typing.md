---
type: source
source_id: plugins-store-neural-typing
title: Neural Typing
source_type: plugin
repository: Kangel-Plugins/Plugins-Store
commit: f8f49767fc304856fdbdbbb5cba896f634f19fd1
path: Plugins/neural_typing.plugin
version: 2.3.1
plugin_id: neural_typing
author: "@van1lLove (идея: @calm_rio)"
min_version: 12.5.1
platform: Android
review_status: accepted
review: ../reviews/plugins-store-neural-typing.md
date: 2026-10-03
---

# Neural Typing

Исходный код плагина: [Plugins/neural_typing.plugin](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767fc304856fdbdbbb5cba896f634f19fd1/Plugins/neural_typing.plugin).

## Подтверждённые факты

1. Клиентская косметическая анимация входящих сообщений и десять вариантов оформления (девять именованных пресетов плюс «Свой»): [строки 3–7, 81–97](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767fc304856fdbdbbb5cba896f634f19fd1/Plugins/neural_typing.plugin#L3-L7).
2. Встроенный Base64 DEX и загрузка `com.neuraltyping.NeuralTypingCore` (`nt-core-9`) через `InMemoryDexClassLoader` с fallback через `DexClassLoader`: [строки 40–43, 315–358](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767fc304856fdbdbbb5cba896f634f19fd1/Plugins/neural_typing.plugin#L40-L43).
3. Хук классического режима на `ChatMessageCell.setMessageObject`; проверка свежести отсеивает сообщения старше 15 секунд: [строки 44–46, 450–459, 590–611](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767fc304856fdbdbbb5cba896f634f19fd1/Plugins/neural_typing.plugin#L44-L46).
4. Выявление конфликтов `typewriter` и `text_animation`, запись предупреждения в лог; отключение конфликтующих плагинов не производится: [строки 50–53, 505–524](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767fc304856fdbdbbb5cba896f634f19fd1/Plugins/neural_typing.plugin#L50-L53).
5. Выгрузка снимает нативные хуки, останавливает таймеры классического режима, восстанавливает текст и снимает классический hook, очищая ссылки: [строки 420–433, 837–860, 526–543](https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f49767fc304856fdbdbbb5cba896f634f19fd1/Plugins/neural_typing.plugin#L420-L433).
